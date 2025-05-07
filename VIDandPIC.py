import cv2
import torch
from datetime import datetime
from ultralytics import YOLO

#test thử với yolov8
model = YOLO("bestV8-75.pt")

#tét thử với yolov5
#model = torch.hub.load('.', 'custom', path='bestV5-75.pt', source='local')




# Hàm nhận diện ảnh cho cả YOLOv5 và YOLOv8
def detect_animals_in_image(img_path):
    # 1) Đọc ảnh gốc & resize về 640×480
    img = cv2.imread(img_path)
    if img is None:
        print("Không đọc được ảnh:", img_path)
        return
    frame_small = cv2.resize(img, (640, 480))

    # 2) Chạy detect
    results = model(frame_small)
    r = results[0]

    # 3) Lấy frame đã vẽ bbox
    if hasattr(r, 'render'):
        # YOLOv5
        r.render()
        frame_to_show = cv2.cvtColor(r.ims[0], cv2.COLOR_RGB2BGR)
    else:
        # YOLOv8
        frame_to_show = r.plot()

    # 4) Copy để vẽ text
    frame_to_show = frame_to_show.copy()

    # 5) Đếm & drawText
    num = len(r.xywh[0]) if hasattr(r, 'xywh') else len(r.boxes)
    cv2.putText(frame_to_show, f"Objects: {num}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    # 6) Hiển thị luôn là 640×480
    window = "Detection Image"
    cv2.namedWindow(window, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window, 640, 480)
    cv2.imshow(window, frame_to_show)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




# Hàm nhận diện video cho cả YOLOv5 và YOLOv8
def detect_animals_in_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Không thể mở video.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize nhỏ xuống
        frame_small = cv2.resize(frame, (640, 480))  # hoặc nhỏ hơn nữa

        # Run detection
        results = model(frame_small)

        # YOLOv5
        if isinstance(results, list) and hasattr(results[0], 'render'):
            r = results[0]
            r.render()
            img = r.ims[0]
            frame_to_show = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            
#PHAN DÉM SLG           
            # Tạo bản sao writable
            frame_to_show = frame_to_show.copy()
            # Đếm và vẽ text
            num_objects = len(r.xywh[0])
            cv2.putText(frame_to_show, f"số lượng: {num_objects}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # YOLOv8
        elif isinstance(results, list) and hasattr(results[0], 'plot'):
            frame_to_show = results[0].plot()
            
#PHAN DÉM SLG
            # Tạo bản sao writable
            frame_to_show = frame_to_show.copy()
            num_objects = len(results[0].boxes)
            cv2.putText(frame_to_show, f"Số lượng: {num_objects}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        else:
            print("⚠️ Không xác định được phiên bản YOLO để xử lý video.")
            break

    
        cv2.imshow("Detection Video", frame_to_show)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
