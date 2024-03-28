from modules import ui_components
from modules.processing import process_images, StableDiffusionProcessing, Processed
from PIL import Image
import io
import modules.scripts as scripts
import gradio as gr
import requests

class LINENotify:
    def __init__(self, token):
        self.__headers = {"Authorization" : f"Bearer {token}"}

    def send(self, message : str, image : Image = None):
        LINE_API_URL = "https://notify-api.line.me/api/notify"
        payload = {"message" : message}
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

class SendLineScript(scripts.Script):
    def title(self):
        return "SendLINE"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with ui_components.InputAccordion(False, label = f"{self.title()}") as enable:
            with gr.Row():
                token = gr.Textbox(label = "LINE Notify token", placeholder = "*" * 43)
        return [enable, token]

    ### AlwaysVisible スクリプトの終了後に呼び出される
    def postprocess(self, p : StableDiffusionProcessing, processed : Processed, *args):
        self.enable = args[0]
        if self.enable:
            line = LINENotify(args[1])
            message = "\r\n" + processed.infotexts[0]
            line.send(message, processed.images[0])
            return

