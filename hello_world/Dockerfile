# 使用 AWS 官方提供的 Python 3.13 Lambda 镜像作为基础
FROM public.ecr.aws/lambda/python:3.13

# 将你的代码和依赖清单复制到容器中
COPY app.py requirements.txt ./

# 如果以后有模型文件，可以通过取消下面这行的注释来拷贝进去
# COPY models/ ./models/

# 安装 requirements.txt 里的 Python 依赖库
RUN pip install -r requirements.txt -t .

# 指定 Lambda 启动时要运行的函数入口
CMD ["app.lambda_handler"]