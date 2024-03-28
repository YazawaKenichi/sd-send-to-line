from modules import ui_components
from modules.processing import process_images, StableDiffusionProcessing, Processed
from PIL import Image
import io
import modules.scripts as scripts
import gradio as gr
import requests
import os.path

class LINENotify:
    def __init__(self, token):
        self.__headers = {"Authorization" : f"Bearer {token}"}

    def send(self, message : str, image : Image = None):
        LINE_API_URL = "https://notify-api.line.me/api/notify"
        payload = {"message" : message}
        files = {}
        if not image is None:
            io = self.img2io(image)
            files = {"imageFile" : io}
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

    ### AlwaysVisible スクリプトの開始前に呼び出される
    def process(self, p : StableDiffusionProcessing, *args):
        self.enable = args[0]
        return

    ### AlwaysVisible スクリプトの終了後に呼び出される
    def postprocess(self, p : StableDiffusionProcessing, processed : Processed, *args):
        if self.enable:
            line = LINENotify(args[1])
            message = "\r\n" + processed.infotexts[0]
            line.send(message, processed.images[0])
            return

    ### 画像が生成された後、すべての画像に対して呼び出される
    def postprocess_image(self, p : StableDiffusionProcessing, pp: scripts.PostprocessImageArgs, *args):
        return

    def sdp2dict(self, p : Processed):
        model : str = p.sd_model_name
        vae : str = p.sd_vae_name
        # path : str= os.path.join(scripts.basedir(), p.outpath_samples)
        # print(path)
        prompt : str= p.prompt
        negative : str= p.negative_prompt
        seed : int = p.seed
        sampler : str = p.sampler_name
        cfg : float = p.cfg_scale
        w : int = p.width
        h : int = p.height
        r = {
            "Model" : model,
            "VAE" : vae,
            # "Path" : path,
            "Prompt" : prompt,
            "Negative" : negative,
            "Seed" : str(seed),
            "Sampler" : sampler,
            "CFG Scale" : str(cfg),
            "Width" : str(w),
            "Height" : str(h),
            }
        return r
    
    def dict2str(self, d):
        return "".join([f"{k} : {v}\r\n" for k, v in d.items()])
