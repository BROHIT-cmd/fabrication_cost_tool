from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

FREECAD_CMD = r"C:\Program Files\FreeCAD 0.21\bin\FreeCADCmd.exe"

@app.route("/process_step", methods=["POST"])
def process_step():
    file = request.files["file"]
    file.save("input.step")

    try:
        subprocess.run([FREECAD_CMD, "step_reader.py"], check=True)

        with open("output.txt", "r") as f:
            data = f.read().split(",")

        return jsonify({
            "volume": float(data[0]) / 1e9,  # convert mm³ → m³
            "length": float(data[1]),
            "width": float(data[2]),
            "height": float(data[3])
        })

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
