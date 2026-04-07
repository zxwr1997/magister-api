# 1. 选择底盘：使用 AWS 官方提供的 Python 3.12 镜像
# 虽然你之前提到过 3.13，但为了 YOLOv8 的稳定性，目前 3.12 是最稳的选择
FROM public.ecr.aws/lambda/python:3.12

# 2. 安装系统级依赖（必做！）
# YOLOv8 和 OpenCV 需要一些底层的图形库，Lambda 的基础镜像里没带，得手动补上
RUN yum install -y \
    mesa-libGL \
    libX11 \
    && yum clean all

# 3. 设置工作目录
WORKDIR /var/task

# 4. 先安装重型装备：Ultralytics (YOLOv8) 和核心依赖
# 这里直接在 Dockerfile 里装，避免 requirements.txt 太乱
# 我们使用 --no-cache-dir 来节省空间，毕竟 C 盘刚救回来
RUN pip install --no-cache-dir ultralytics opencv-python-headless torch torchvision --extra-index-url https://download.pytorch.org/whl/cpu

# 5. 装载“赛车零件”
# 把 app.py 和咱们刚空投的公式模型都塞进去
COPY app.py ./
COPY formula_detect.pt ./

# 6. 最终指令：启动 AI 塔台调度中心
CMD ["app.lambda_handler"]