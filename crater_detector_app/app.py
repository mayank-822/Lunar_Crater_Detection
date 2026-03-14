from flask import Flask, render_template, request
from ultralytics import YOLO
import os
import uuid
import cv2

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

model = YOLO("model/best.pt")

@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        file = request.files["image"]

        if file:
            filename = str(uuid.uuid4()) + ".jpg"

            upload_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(upload_path)

            results = model(upload_path)

            crater_count = len(results[0].boxes)

            img = results[0].plot()

            result_path = os.path.join(RESULT_FOLDER, filename)
            cv2.imwrite(result_path, img)

            return render_template(
                "index.html",
                uploaded=True,
                crater_count=crater_count,
                result_image=result_path
            )

    return render_template("index.html", uploaded=False)

if __name__ == "__main__":
    app.run(debug=True)