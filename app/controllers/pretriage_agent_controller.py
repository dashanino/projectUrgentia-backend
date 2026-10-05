from flask import request, jsonify

from app.services.pretriage_agent_service import PretriageAgentService


class PretriageAgentController:

    def __init__(self):
        self.service = PretriageAgentService()

    def evaluate(self):

        data = request.get_json()

        if not data:
            return jsonify({
                "ok": False,
                "message": "No se recibieron datos"
            }), 400

        result = self.service.evaluate(data)

        return jsonify({
            "ok": True,
            "result": result
        }), 200