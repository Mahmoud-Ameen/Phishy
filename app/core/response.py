from flask import jsonify


class ApiResponse:
    @staticmethod
    def success(data=None, message="Success"):
        response = {"status": "success", "message": message}
        if data is not None:
            response["data"] = data
        return jsonify(response), 200

    @staticmethod
    def error(message="An error occurred", status_code=400):
        response = {"status": "error", "message": message}
        return jsonify(response), status_code
