import time
import traceback
from io import BytesIO

from openpyxl import load_workbook

from app.services.pretriage_agent_service import (
    PretriageAgentService,
    RevisionClinicaRequerida,
)


class BulkPretriageService:
    """Procesa un Excel de casos y agrega la prioridad de Urgentia."""

    CASE_COLUMN_ALIASES = {
        "caso", "caso clinico", "caso clínico", "motivo",
        "motivo de consulta", "motivo consulta", "descripcion",
        "descripción", "relato", "situacion", "situación",
    }

    def __init__(self):
        self.agent = PretriageAgentService()

    @staticmethod
    def _normalize_header(value):
        return str(value or "").strip().lower().replace("_", " ")

    def _find_case_column(self, worksheet):
        headers = [
            self._normalize_header(worksheet.cell(row=1, column=column).value)
            for column in range(1, worksheet.max_column + 1)
        ]

        for index, header in enumerate(headers, start=1):
            if header in self.CASE_COLUMN_ALIASES:
                return index

        for index, header in enumerate(headers, start=1):
            if any(term in header for term in (
                "caso", "motivo", "relato", "descripcion", "situacion"
            )):
                return index

        return None

    def process(self, file_bytes, progress_callback=None):
        """Procesa el Excel, informa el avance y conserva las filas originales."""
        print("\n========== URGENTIA · EVALUACIÓN MASIVA ==========", flush=True)
        print("[BULK] Leyendo archivo Excel...", flush=True)

        try:
            workbook = load_workbook(filename=BytesIO(file_bytes))
        except Exception as error:
            raise ValueError(
                "No fue posible leer el archivo. Debe ser un Excel .xlsx válido."
            ) from error

        worksheet = workbook.active
        if worksheet.max_row < 2:
            raise ValueError("El Excel no contiene casos para evaluar.")

        case_column = self._find_case_column(worksheet)
        if case_column is None:
            raise ValueError(
                "No encontré la columna de casos. Usa como encabezado "
                "'caso', 'caso_clinico', 'motivo_de_consulta' o 'relato'."
            )

        cases = []
        for row in range(2, worksheet.max_row + 1):
            raw_case = worksheet.cell(row=row, column=case_column).value
            case_text = str(raw_case or "").strip()
            if case_text:
                cases.append((row, case_text))

        total = len(cases)
        if total == 0:
            raise ValueError("No encontré casos con texto para evaluar.")

        worksheet.insert_cols(case_column + 1)
        priority_column = case_column + 1
        worksheet.cell(row=1, column=priority_column, value="priorizacion_urgentia")

        processed = classified = clinical_review = errors = 0

        def report(status="procesando", current_row=None):
            if progress_callback:
                progress_callback({
                    "status": status,
                    "current": processed,
                    "total": total,
                    "row": current_row,
                    "percentage": round((processed / total) * 100) if total else 100,
                })

        print(f"[BULK] Total de casos encontrados: {total}", flush=True)
        report(status="iniciando")

        for index, (row, case_text) in enumerate(cases, start=1):
            started_at = time.perf_counter()
            print("\n" + "=" * 58, flush=True)
            print(f"[BULK][CASO {index}/{total}] INICIANDO · Fila Excel {row}", flush=True)
            print(f"[BULK][CASO {index}/{total}] Texto: {case_text[:300]}", flush=True)
            print(f"[BULK][CASO {index}/{total}] Enviando a evaluate_free_text...", flush=True)
            report(status="procesando", current_row=row)

            try:
                result = self.agent.evaluate_free_text(case_text)
                print(f"[BULK][CASO {index}/{total}] Respuesta recibida: {result}", flush=True)

                priority = result.get("prioridad")
                if result.get("accion") == "revision_clinica" or priority is None:
                    value = "revision_clinica"
                    clinical_review += 1
                else:
                    value = priority
                    classified += 1

                worksheet.cell(row=row, column=priority_column, value=value)
                print(f"[BULK][CASO {index}/{total}] RESULTADO: {value}", flush=True)

            except RevisionClinicaRequerida as error:
                worksheet.cell(row=row, column=priority_column, value="revision_clinica")
                clinical_review += 1
                print(
                    f"[BULK][CASO {index}/{total}] REVISIÓN CLÍNICA: {error}",
                    flush=True,
                )

            except Exception as error:
                worksheet.cell(row=row, column=priority_column, value="error")
                errors += 1
                print(
                    f"[BULK][CASO {index}/{total}] ERROR {type(error).__name__}: {error}",
                    flush=True,
                )
                traceback.print_exc()

            processed += 1
            elapsed = time.perf_counter() - started_at
            print(
                f"[BULK][CASO {index}/{total}] TERMINADO en {elapsed:.2f} s",
                flush=True,
            )
            report(status="procesando", current_row=row)

        print("\n========== RESUMEN DE EVALUACIÓN ==========", flush=True)
        print(f"[BULK] Procesados: {processed}/{total}", flush=True)
        print(f"[BULK] Clasificados: {classified}", flush=True)
        print(f"[BULK] Revisión clínica: {clinical_review}", flush=True)
        print(f"[BULK] Errores: {errors}", flush=True)

        output = BytesIO()
        workbook.save(output)
        output.seek(0)
        report(status="completado")
        print("[BULK] Excel de resultados generado.", flush=True)

        return output.getvalue(), {
            "procesados": processed,
            "clasificados": classified,
            "revision_clinica": clinical_review,
            "errores": errors,
        }
