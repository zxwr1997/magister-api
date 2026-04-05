import json
import base64
import cv2
import numpy as np
from ultralytics import YOLO

# 全局加载模型：只在赛车点火（冷启动）时加载一次
print("--- 引擎点火中：加载 YOLOv8 基础模型 ---")
try:
    model = YOLO('yolov8n.pt') 
    print("--- 引擎启动成功！ ---")
except Exception as e:
    print(f"引擎启动失败: {e}")

def lambda_handler(event, context):
    try:
        # 1. 拿到油门信号（Base64图片）
        body = json.loads(event.get('body', '{}'))
        image_b64 = body.get('image_base64')
        if not image_b64:
            return {"statusCode": 400, "body": json.dumps({"error": "没收到图片信号"})}

        # 2. 图片格式转换：从 Base64 转为 OpenCV 矩阵
        img_bytes = base64.b64decode(image_b64)
        np_arr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # 3. 开始自动驾驶（AI 推理）
        results = model(img)
        
        # 提取识别到的物体名称
        detected_objects = []
        for r in results:
            for c in r.boxes.cls:
                detected_objects.append(model.names[int(c)])

        # 4. 把结果反馈给仪表盘
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": "AI 扫描完成！",
                "detected": detected_objects,
                "count": len(detected_objects)
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"赛车抛锚了: {str(e)}"})
        }