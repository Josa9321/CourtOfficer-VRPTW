from flask import Flask, jsonify, request

import vrptw

app = Flask(__name__)

@app.route('/')
def base():
    return "VRPTW App"

@app.route('/solve', methods=["POST"])
def solve_instance():
    instance_json = request.get_json()
    if not instance_json:
        return jsonify({"error": "No JSON instance provided"}), 400

    instance = vrptw.load_json_object_instance(instance_json)
    solution = vrptw.solve_instance(instance, 0, 600)
    return jsonify(solution.set_object()), 200
