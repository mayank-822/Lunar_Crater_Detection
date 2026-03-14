# from flask import Flask, render_template, request
# from ultralytics import YOLO
# import os
# import uuid
# import cv2

# import time

# app = Flask(__name__)

# UPLOAD_FOLDER = "static/uploads"
# RESULT_FOLDER = "static/results"

# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(RESULT_FOLDER, exist_ok=True)

# model = YOLO("model/best.pt")

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         file = request.files.get("image")
#         if file:
#             filename = str(uuid.uuid4()) + ".jpg"
#             upload_path = os.path.join(UPLOAD_FOLDER, filename)
#             file.save(upload_path)

#             start_time = time.time()
#             results = model(upload_path)
#             end_time = time.time()
#             processing_time = round(end_time - start_time, 2)

#             img = cv2.imread(upload_path)
#             height, width, _ = img.shape
#             image_area = height * width

#             img_plot = img.copy()
#             boxes = results[0].boxes
#             crater_data = []

#             stats = {
#                 "total": len(boxes),
#                 "avg_diameter": 0,
#                 "largest": 0,
#                 "smallest": float('inf'),
#                 "avg_conf": 0,
#                 "density": 0,
#                 "time": processing_time,
#                 "small": 0,
#                 "medium": 0,
#                 "large": 0
#             }

#             total_diameter = 0
#             total_conf = 0

#             for i, box in enumerate(boxes):
#                 x_c, y_c, w, h = box.xywh[0].tolist()
#                 conf = float(box.conf[0])
                
#                 diameter_px = round(max(w, h), 2)
                
#                 if diameter_px < 20:
#                     size_class = "Small"
#                     stats["small"] += 1
#                 elif diameter_px < 50:
#                     size_class = "Medium"
#                     stats["medium"] += 1
#                 else:
#                     size_class = "Large"
#                     stats["large"] += 1

#                 total_diameter += diameter_px
#                 total_conf += conf

#                 if diameter_px > stats["largest"]: stats["largest"] = diameter_px
#                 if diameter_px < stats["smallest"]: stats["smallest"] = diameter_px
                
#                 x1, y1, x2, y2 = box.xyxy[0].tolist()

#                 crater_data.append({
#                     "id": i + 1,
#                     "diameter": diameter_px,
#                     "confidence": round(conf, 2),
#                     "size": size_class,
#                     "x": x_c, "y": y_c, "w": w, "h": h,
#                     "x1": x1, "y1": y1, "x2": x2, "y2": y2
#                 })

#                 cv2.rectangle(img_plot, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
#                 cv2.circle(img_plot, (int(x_c), int(y_c)), 2, (0, 0, 255), -1)
#                 cv2.putText(img_plot, f"#{i+1}", (int(x1), int(y1)-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

#             if stats["total"] > 0:
#                 stats["avg_diameter"] = round(total_diameter / stats["total"], 2)
#                 stats["avg_conf"] = round(total_conf / stats["total"], 2)
#                 stats["density"] = round((stats["total"] / image_area) * 1000000, 2)
#             else:
#                 stats["smallest"] = 0

#             result_path = os.path.join(RESULT_FOLDER, filename)
#             cv2.imwrite(result_path, img_plot)

#             return render_template(
#                 "index.html",
#                 uploaded=True,
#                 crater_count=stats["total"],
#                 original_image=upload_path,
#                 result_image=result_path,
#                 stats=stats,
#                 crater_data=crater_data,
#                 img_width=width,
#                 img_height=height,
#                 filename=filename
#             )

#     return render_template("index.html", uploaded=False)

# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, render_template, request
from ultralytics import YOLO
import os
import uuid
import cv2

import time

app = Flask(__name__)

UPLOAD_FOLDER = "static/uploads"
RESULT_FOLDER = "static/results"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

model = YOLO("model/best.pt")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("image")
        if file:
            filename = str(uuid.uuid4()) + ".jpg"
            upload_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(upload_path)

            start_time = time.time()
            results = model(upload_path)
            end_time = time.time()
            processing_time = round(end_time - start_time, 2)

            img = cv2.imread(upload_path)
            height, width, _ = img.shape
            image_area = height * width

            img_plot = img.copy()
            boxes = results[0].boxes
            crater_data = []

            stats = {
                "total": len(boxes),
                "avg_diameter": 0,
                "largest": 0,
                "smallest": float('inf'),
                "avg_conf": 0,
                "density": 0,
                "time": processing_time,
                "small": 0,
                "medium": 0,
                "large": 0
            }

            total_diameter = 0
            total_conf = 0

            for i, box in enumerate(boxes):
                x_c, y_c, w, h = box.xywh[0].tolist()
                conf = float(box.conf[0])
                
                diameter_px = round(max(w, h), 2)
                
                if diameter_px < 20:
                    size_class = "Small"
                    stats["small"] += 1
                elif diameter_px < 50:
                    size_class = "Medium"
                    stats["medium"] += 1
                else:
                    size_class = "Large"
                    stats["large"] += 1

                total_diameter += diameter_px
                total_conf += conf

                if diameter_px > stats["largest"]: stats["largest"] = diameter_px
                if diameter_px < stats["smallest"]: stats["smallest"] = diameter_px
                
                x1, y1, x2, y2 = box.xyxy[0].tolist()

                crater_data.append({
                    "id": i + 1,
                    "diameter": diameter_px,
                    "confidence": round(conf, 2),
                    "size": size_class,
                    "x": x_c, "y": y_c, "w": w, "h": h,
                    "x1": x1, "y1": y1, "x2": x2, "y2": y2
                })

                cv2.rectangle(img_plot, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                cv2.circle(img_plot, (int(x_c), int(y_c)), 2, (0, 0, 255), -1)
                cv2.putText(img_plot, f"#{i+1}", (int(x1), int(y1)-5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            if stats["total"] > 0:
                stats["avg_diameter"] = round(total_diameter / stats["total"], 2)
                stats["avg_conf"] = round(total_conf / stats["total"], 2)
                stats["density"] = round((stats["total"] / image_area) * 1000000, 2)
            else:
                stats["smallest"] = 0

            result_path = os.path.join(RESULT_FOLDER, filename)
            cv2.imwrite(result_path, img_plot)

            return render_template(
                "index.html",
                uploaded=True,
                crater_count=stats["total"],
                original_image=upload_path,
                result_image=result_path,
                stats=stats,
                crater_data=crater_data,
                img_width=width,
                img_height=height,
                filename=filename
            )

    return render_template("index.html", uploaded=False)

if __name__ == "__main__":
    app.run(debug=True)