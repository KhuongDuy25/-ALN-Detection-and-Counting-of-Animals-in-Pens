import cv2
import torch
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, time
from ultralytics import YOLO
import pandas as pd
import os
import pathlib

# Khắc phục lỗi đường dẫn trên Windows
pathlib.PosixPath = pathlib.WindowsPath

# Tải mô hình YOLOv5
#model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

#test thử với yolov8
model = YOLO("bestV8-75.pt")

#tét thử với yolov5
#model = torch.hub.load('.', 'custom', path='bestV5-75.pt', source='local')


# Font Unicode
font_path = "arial.ttf"
font = ImageFont.truetype(font_path, 32)

def log_escape(animal_name, actual_count, expected_count):
    log_folder = os.path.join(os.getcwd(), "Warning")
    os.makedirs(log_folder, exist_ok=True)
    log_file = os.path.join(log_folder, "log_xong_chuong.xlsx")

    missing = expected_count - actual_count
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    new_row = {
        "Thời gian phát hiện": now,
        "Loài động vật": animal_name,
        "Số lượng thực tế": actual_count,
        "Số lượng kỳ vọng": expected_count,
        "Thiếu": missing,
        "Ghi chú": "Xổng chuồng"
    }

    if os.path.exists(log_file):
        df = pd.read_excel(log_file)
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    else:
        df = pd.DataFrame([new_row])

    df.to_excel(log_file, index=False)

def get_all_animal_names():
    return [
        'Bò', 'Gà', 'Vịt', 'Dê', 'Lợn'
    ]
    #         'Chuột lang nước', 'Bò', 'Hươu', 'Voi', 'Hồng hạc', 'Hươu cao cổ', 'Báo đốm',
    #    'Kangaroo', 'Sư tử', 'Vẹt', 'Chim cánh cụt', 'Tê giác', 'Cừu', 'Hổ',
    #    'Rùa', 'Ngựa vằn'

def start_monitoring_with_config(required_counts: dict, start_time, end_time):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Không mở được camera.")
        return

    start_time_obj = start_time 
    end_time_obj = end_time
    
    while cap.isOpened():
        now = datetime.now().time()

        # Kiểm tra nếu thời gian hiện tại nằm trong khoảng giám sát
        if start_time_obj <= end_time_obj:
            in_monitoring_time = start_time_obj <= now <= end_time_obj
        else:
            # Qua đêm (ví dụ: 22:00 đến 06:00)
            in_monitoring_time = now >= start_time_obj or now <= end_time_obj

        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)
        result = results[0]
        boxes = result.boxes

        # Convert boxes -> pandas DataFrame
        if boxes is not None and boxes.xyxy is not None and len(boxes.xyxy) > 0:
            data = {
                'xmin': boxes.xyxy[:, 0].cpu().numpy(),
                'ymin': boxes.xyxy[:, 1].cpu().numpy(),
                'xmax': boxes.xyxy[:, 2].cpu().numpy(),
                'ymax': boxes.xyxy[:, 3].cpu().numpy(),
                'confidence': boxes.conf.cpu().numpy(),
                'class': boxes.cls.cpu().numpy()
            }
            df = pd.DataFrame(data)
            df['name'] = df['class'].apply(lambda x: model.names[int(x)])
        else:
            df = pd.DataFrame(columns=['xmin', 'ymin', 'xmax', 'ymax', 'confidence', 'class', 'name'])


        filtered_df = df[df['name'].isin(required_counts.keys())]
        animal_counts = filtered_df['name'].value_counts().to_dict()

        info_str = ""

        for animal in required_counts:
            actual_count = animal_counts.get(animal, 0)
            required_count = required_counts[animal]
            missing_count = required_count - actual_count

            if missing_count > 0:
                if in_monitoring_time:
                    info_str += f"{animal}: {actual_count} (Xổng chuồng): {missing_count}\n"
                    log_escape(animal, actual_count, required_count)
                else:
                    info_str += f"{animal}: {actual_count} (Thiếu - Ngoài giờ)\n"
            else:
                info_str += f"{animal}: {actual_count}\n"

        frame_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(frame_pil)

        x, y = 10, 40
        for line in info_str.strip().split('\n'):
            draw.text((x, y), line, font=font, fill=(255, 0, 0))
            y += 40

        for _, row in filtered_df.iterrows():
            xmin, ymin, xmax, ymax = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
            label = row['name']
            confidence = row['confidence']
            draw.rectangle([xmin, ymin, xmax, ymax], outline=(0, 255, 0), width=2)
            draw.text((xmin, ymin - 30), f"{label} {confidence:.2f}", font=font, fill=(0, 255, 0))

        frame = cv2.cvtColor(np.array(frame_pil), cv2.COLOR_RGB2BGR)
        cv2.imshow("YOLOv5 Nhận Diện", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()