FROM python:3.9-alpine
WORKDIR /app
EXPOSE 80
COPY main.py /app/
LABEL org.opencontainers.image.authors="Lsshu" org.opencontainers.image.email="admin@lsshu.cn" org.opencontainers.image.url="https://github.com/lsshu/face"
RUN apk update && apk add --no-cache build-base cmake  freetype-dev jpeg-dev zlib-dev libwebp-dev boost-libs ffmpeg-dev pkgconfig libffi-dev
RUN pip install dlib numpy==1.26.4 opencv-python face_recognition fastapi uvicorn
ENV HOST="0.0.0.0" PORT=80 LOG_LEVEL="warning" WORKERS=4 NOTRELOAD=""
CMD uvicorn main:app --host ${HOST} --port ${PORT} ${NOTRELOAD} --log-level ${LOG_LEVEL} --workers ${WORKERS}