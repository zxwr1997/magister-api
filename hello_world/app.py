


#测试增加
import json

def lambda_handler(event, context):
    try:
        # 打印 event 方便在 AWS CloudWatch 里调试
        print(f"Received event: {json.dumps(event)}")
        
        # 安全地获取 body，防止 body 是 None 或格式不对
        body_str = event.get('body', '{}')
        if not body_str:
             body_str = '{}'
             
        body = json.loads(body_str)
        image_b64 = body.get('image_base64')
        
        if not image_b64:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No image_base64 data provided in the body"})
            }

        # 安全计算大小
        data_size_mb = len(str(image_b64)) / (1024 * 1024)

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "message": "Image received successfully!",
                "data_size_mb": round(data_size_mb, 4),
                "mock_result": "\\int_{a}^{b} x^2 dx"
            })
        }
    except Exception as e:
        # 把具体的错误信息返回出来，别再只给个干巴巴的 500 了
        print(f"Error occurred: {str(e)}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": f"Server Error: {str(e)}"})
        }