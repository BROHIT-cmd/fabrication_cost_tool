from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

FREECAD_CMD = r"Downloads\FREECAD.exe"

@app.route('/process_step', methods=['POST'])
def process_step():

    file = request.files['file']
    file.save("input.step")

    # Run FreeCAD script
    subprocess.run([FREECAD_CMD, "step_reader.py"])

    # Read output
    try:
        with open("output.txt", "r") as f:
            data = f.read().split(",")

        result = {
            "volume": float(data[0]) / 1e9,
            "length": float(data[1]),
            "width": float(data[2]),
            "height": float(data[3])
        }

        return jsonify(result)

    except:
        return jsonify({"error": "STEP processing failed"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
