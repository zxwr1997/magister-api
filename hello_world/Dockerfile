FROM public.ecr.aws/lambda/python:3.13

# 安装零件（依赖库）
COPY requirements.txt ./
RUN pip install -r requirements.txt

# 把引擎文件（模型）放进车舱
COPY yolov8n.pt ./

# 把控制程序放进车舱
COPY app.py ./

CMD ["app.lambda_handler"]