FROM public.ecr.aws/lambda/python:3.13

# 增加这一段：安装缺少的系统底层库 (比如 libglib2.0 和 libxcb)
# 这两行极其关键，专门对付 OpenCV 在精简版 Linux 上的水土不服
RUN dnf install -y glib2 libxcb mesa-libGL && \
    dnf clean all

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY yolov8n.pt ./
COPY app.py ./

CMD ["app.lambda_handler"]