from modules import ui_components
from modules.processing import process_images, StableDiffusionProcessing, Processed
import modules.scripts as scripts
from modules.shared import cmd_opts
import gradio as gr
from scripts.LINENotify import LINENotify

class SendLineScript(scripts.Script):
    def title(self):
        return "SendLINE"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with ui_components.InputAccordion(False, label = f"{self.title()}") as enable:
            with gr.Row():
                _tmp = getattr(cmd_opts, "LINE_Notify_Token", "")
                token = gr.Textbox(_tmp, label = "LINE Notify token", placeholder = "*" * 43, default = cmd_opts.LINE_Notify_Token)
            with gr.Row():
                notificationDisabled = gr.Checkbox(False, label = "Notification Disable")
        return [enable, token, notificationDisabled]

    ### AlwaysVisible スクリプトの終了後に呼び出される
    def postprocess(self, p : StableDiffusionProcessing, processed : Processed, *args):
        self.enable = args[0]
        if not self.enable:
            return
        line = LINENotify(args[1])
        notificationDisabled = args[2]
        message = "\r\n" + processed.infotexts[0]
        line.send(message, processed.images[0], notificationDisabled)

