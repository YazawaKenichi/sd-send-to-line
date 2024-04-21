import io
from PIL import Image
import requests

class LINENotify:
    def __init__(self, token):
        self.__headers = {"Authorization" : f"Bearer {token}"}

    def send(self, message : str, image : Image = None, notificationDisabled = False):
        LINE_API_URL = "https://notify-api.line.me/api/notify"
        payload = {"message" : message, "notificationDisabled" : notificationDisabled}
        files = {}
        if not image is None:
            _io = self.img2io(image)
            files = {"imageFile" : _io}
        r = requests.post(LINE_API_URL, headers = self.__headers, data = payload, files = files)
        return r

    def img2io(self, image : Image):
        img_bytes = io.BytesIO()
        image.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()  # これが bytes
        return img_bytes

