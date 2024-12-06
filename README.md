# lsshu/face
face_recognition 人脸对比和docker镜像

### 创建容器
```shell
docker run --restart=always -d --name A_yao_face -p 49000:80 lsshu/face
```

### 其它例子
```shell
docker run --restart=always -d --name A_yao_face -p 49000:80 -e WORKERS=16 lsshu/face
docker run --restart=always -d --name A_yao_face -v /yao_face:/app -p 49000:80 -e WORKERS=16 lsshu/face
docker run --restart=always -d --name A_yao_face -v /yao_face:/app -p 49000:80 -e NOTRELOAD='--reload' -e WORKERS=1 lsshu/face
```

### 删除容器
```shell
docker stop A_yao_face && docker rm A_yao_face
```

### 删除镜像
```shell
docker rmi lsshu/face
```

### 测试是否安装成功
```http request
http://127.0.0.1:49000/
```

### 测试对比人脸文档
```http request
http://127.0.0.1:49000/docs
```

### 可能使用到的使用命令 创建镜像
```shell
docker build -t face .
```

## 发布docker镜像
### 1.构建Docker镜像
```shell
docker build -t face .
```

### 2.标记镜像
```shell
docker tag face lsshu/face:latest
```

### 3.登录到Docker Hub
```shell
docker login -u <your-docker-username> -p <your-password>
```

### 4.推送镜像到Docker Hub
```shell
docker push lsshu/face:latest
```