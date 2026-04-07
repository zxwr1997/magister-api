import json
import base64
import os
from ultralytics import YOLO

# --- 引擎启动区 ---
# 在函数外部加载模型，这样 Lambda 在“热启动”时不需要重复加载，速度起飞！
# 确保这个文件名和你刚才 Invoke-WebRequest 下载的文件名完全一致
MODEL_PATH = 'formula_detect.pt'
model = YOLO(MODEL_PATH)

def lambda_handler(event, context):
    """
    机长，这是你的 AI 塔台调度中心。
    它负责接收图片、调用 YOLO 引擎识别公式，并返回结果。
    """
    try:
        # 1. 接收从 API Gateway 传来的原始数据
        if 'body' not in event:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "没有接收到数据体 (Body is missing)"})
            }
            
        body = json.loads(event['body'])
        image_b64 = body.get('image_base64')
        
        if not image_b64:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "找不到 image_base64 字段"})
            }

        # 2. 解码图片并存入 Lambda 唯一的写字板：/tmp 文件夹
        image_data = base64.b64decode(image_b64)
        temp_image_path = "/tmp/detect_target.jpg"
        
        with open(temp_image_path, "wb") as f:
            f.write(image_data)

        # 3. 核心推理：让 YOLO 引擎睁开眼看公式
        # task='detect' 确保它执行目标检测任务
        results = model.predict(source=temp_image_path, conf=0.25, save=False)
        
        # 4. 战果统计
        detected_names = []
        for r in results:
            for box in r.boxes:
                # 获取类别索引并转为名称（比如 'formula'）
                class_id = int(box.cls[0])
                label = model.names[class_id]
                detected_names.append(label)

        # 5. 任务圆满完成，返回战报
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*" # 允许跨域请求
            },
            "body": json.dumps({
                "message": "AI 公式扫描任务完成！",
                "detected_objects": detected_names,
                "count": len(detected_names),
                "status": "Success"
            }),
        }

    except Exception as e:
        # 即使坠机了，也要留下黑匣子记录
        print(f"ERROR: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "引擎发生故障 (Server Error)",
                "error": str(e)
            })
        }