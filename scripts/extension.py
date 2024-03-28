from modules import ui_components
from modules.processing import process_images, StableDiffusionProcessing, Processed
import modules.scripts as scripts
import gradio as gr
import requests
import os.path

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

    ### AlwaysVisible スクリプトの開始前に呼び出される
    def process(self, p : StableDiffusionProcessing, *args):
        self.enable = args[0]
        return

    ### AlwaysVisible スクリプトの終了後に呼び出される
    def postprocess(self, p : StableDiffusionProcessing, processed : Processed, *args):
        if self.enable:
            self.token = args[1]
            self.send("Generated")
            return

    ### 画像が生成された後、すべての画像に対して呼び出される
    def postprocess_image(self, p : StableDiffusionProcessing, pp: scripts.PostprocessImageArgs, *args):
        return

    def send(self, message, image = None):
        self.LINE_API_URL = "https://notify-api.line.me/api/notify"
        self.__headers = {"Authorization" : f"Bearer {self.token}"}
        print(f"[LINE][init] {self.token}")
        payload = {
                "message" : message,
                "sticker_package_id" : None,
                "stickerId" : None,
                }
        print(f"[LINE][send] {message}")
        files = {}
        if not image is None:
            # 画像を一枚目だけに限定（今後複数画像送れるようにアップデートが必要）
            files = {"imageFile" : open(image, "rb")}
        r = requests.post(self.LINE_API_URL, headers = self.__headers, data = payload, files = files)
        return r
