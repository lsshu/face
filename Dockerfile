FROM python:3.9
WORKDIR /app
EXPOSE 80
LABEL org.opencontainers.image.authors="Lsshu" org.opencontainers.image.email="admin@lsshu.cn" org.opencontainers.image.url="https://github.com/lsshu/face"
RUN if [ -e /etc/apt/sources.list.d/debian.sources ]; then sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources; fi
RUN if [ -e /etc/apt/sources.list ]; then sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list; fi
RUN apt update && apt install -y cmake libgl1 && rm -rf /etc/localtime && ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN pip install -i https://pypi.mirrors.ustc.edu.cn/simple/ dlib numpy==1.26.4 opencv-python face_recognition fastapi uvicorn
COPY main.py /app/
ENV HOST="0.0.0.0" PORT=80 LOG_LEVEL="warning" WORKERS=4 NOTRELOAD="" SSL_KEYFILE="" SSL_CERTFILE=""
CMD uvicorn main:app --host ${HOST} --port ${PORT} ${NOTRELOAD} --log-level ${LOG_LEVEL} --workers ${WORKERS} ${SSL_KEYFILE} ${SSL_CERTFILE}