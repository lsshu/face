# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ numpy==1.26.4 opencv-python dlib face_recognition
# pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ fastapi uvicorn
from io import BytesIO
from base64 import b64decode
from PIL import Image
from numpy import array
from fastapi import FastAPI
from pydantic import BaseModel
from cv2 import cvtColor, COLOR_BGR2RGB
import face_recognition

app = FastAPI()


def base64_image_to_nparray(base64_image):
    """
    base64图片转numpy array
    :param base64_image:
    :return:
    """
    try:
        image_data = b64decode(base64_image)
        image = array(Image.open(BytesIO(image_data)))
        return image
    except:
        return None


def different(sample_image_base64, known_image_base64, tolerance=0.6):
    image = base64_image_to_nparray(sample_image_base64)
    known_image = base64_image_to_nparray(known_image_base64)
    if image is not None and known_image is not None:
        # 获取已知人脸编码
        # print("Encoding known face...")
        img_rgb = cvtColor(known_image, COLOR_BGR2RGB)
        known_face_encoding = face_recognition.face_encodings(img_rgb)[0]

        # 人脸定位和编码
        # print("Detecting faces...")
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)

        # 如果没有找到人脸，则返回
        if len(face_locations) != 0:
            # 遍历每个人脸位置和人脸编码
            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # 比较人脸
                matches = face_recognition.compare_faces([known_face_encoding], face_encoding, tolerance=tolerance)
                # 计算相似度分数
                face_distances = face_recognition.face_distance([known_face_encoding], face_encoding)
                similarity_score = 1 - face_distances[0] if face_distances[0] <= 1 else 0
                if True in matches and similarity_score > tolerance:
                    # 人脸通过
                    return True

    return False


class InportItem(BaseModel):
    sample_image_base64: str
    known_image_base64: str
    tolerance: float = 0.5


class ResponseItem(BaseModel):
    code: int = 1
    status: int
    message: str = None


@app.get("/")
async def root():
    return ResponseItem(status=100, message="success")


@app.post("/face")
async def face(item: InportItem):
    output_path = different(item.sample_image_base64, item.known_image_base64, item.tolerance)
    return ResponseItem(status=output_path)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False, workers=4)
