# 1. 使用 AWS 官方 Python 3.12 镜像 (Amazon Linux 2023)
FROM public.ecr.aws/lambda/python:3.12

# 2. 使用 dnf 代替 yum 安装系统依赖
# AL2023 必须使用 dnf，这些库是让 OpenCV 睁开眼看图片的“视神经”
RUN dnf install -y \
    mesa-libGL \
    libX11 \
    && dnf clean all

# 3. 设置工作目录
WORKDIR /var/task

# 4. 安装 YOLO 引擎及相关依赖
# 我们使用 --no-cache-dir 保持镜像轻量，节省 C 盘和云端空间
RUN pip install --no-cache-dir ultralytics opencv-python-headless torch torchvision --extra-index-url https://download.pytorch.org/whl/cpu

# 5. 装载 app.py 代码和模型文件
COPY app.py ./
COPY formula_detect.pt ./

# 6. 启动指令
CMD ["app.lambda_handler"]