from flask import jsonify


class ApiResponse:
    @staticmethod
    def success(data=None, message="Success"):
        response = {"status": "success", "message": message}
        if data is not None:
            response["data"] = data
        return jsonify(response), 200

    @staticmethod
    def error(message="An error occurred", status_code=400, details=None):
        response = {"status": "error", "message": message, "details": details}
        return jsonify(response), status_code
