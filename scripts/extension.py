from modules import ui_components
from modules.processing import process_images, StableDiffusionProcessing
import modules.scripts as scripts
import gradio as gr
import requests
import os.path

class SendLineScript(scripts.Script):
    def title(self):
        return "SendLINE"
    def show(self, is_img2img):
        return scripts.AlwaysVisible
    # UI の作成
    def ui(self, is_img2img):
        ### チェックボックス付きのグループの作成 ###
        # with ui_components.InputAccordion(False, label = f"{self.title()}") as enable:
        with gr.Accordion(self.title(), open = True):
            ### 拡張アプリの説明 ###
            with gr.Row():
                # 説明書き
                LINE_NOTIFY_URL = "https://notify-bot.line.me"
                gr.Markdown(f"<a href = \"{LINE_NOTIFY_URL}\">LINE Notify</a><br><sup>現在は画像を１枚のみ送信<br>今後アップデートを想定</sup>")
            ### 有効無効の切り替え
            with gr.Row():
                enable = gr.Checkbox(label = "Enable", value = False)
            ### LINE Notify トークンの入力 ###
            with gr.Row():
                # TOKEN 入力
                token = gr.Textbox(label = "LINE Notify token", placeholder = "*" * 43)
            ### 送信するデータの選択 ###
            with gr.Row():
                gr.Markdown(f"<sup>開発中</sup>")
                # グリッド画像の送信
                grid = gr.Checkbox(label = "Send Grid Image", value = True)
                # すべての画像を送信するかどうか
                all = gr.Checkbox(label = "Send All Image", value = True)
            with gr.Row():
                # チェックボックスのグループを表示
                information = ["Model", "VAE", "Path", "Prompt", "Negative", "Seed", "Sampler", "CFG Scale", "Width", "Height"]
                embeds = gr.CheckboxGroup(
                        label = "Send Image Info",
                        # 使えるチェックボックス
                        choices = information,
                        # デフォルトでチェックされている項目
                        value = information,
                        )
        return [enable, token, grid, all, embeds]
        # return [token, grid, all, embeds]
    def postprocess_image_after_composite(self, p : StableDiffusionProcessing, pp: scripts.PostprocessImageArgs, *args):
        # Processed の取得（詳細 : modules.images.py ）
        processed = process_images(p)
        path = processed.path
        basename = processed.basename
        extension = processed.extension
        impath = os.path.join(path, basename + "." + extension)
        # WebUI SaveLINE タブからの入力を保管
        enable = args[0]
        token = args[1]
        grid = args[2]
        all = args[3]
        embeds = args[3]
        # 送信機拒否
        if not enable:
            print("SendLINE is disabled.")
            return processed
        print("SendLINE is abled.")
        # トークンを文字列に変換
        token_msg = f"Token : {token}\r\n"
        print(f"TokenMsg : {token_msg}")
        # 画像のパスを文字列に変換
        path_msg = f"Image Path : {impath}\r\n"
        print(f"PathMsg : {path_msg}")
        # 画像生成の設定値を文字列に変換
        parameters = self.sdp2str(p)
        print(f"Parameters : {parameters}")
        # LINE に送信するメッセージを作成
        message = token_msg + path_msg + parameters
        print(f"Message : {message}")
        # LINE インスタンスの生成
        self.token = token
        # 送信
        self.send(message, impath)
        # Processed を返す
        return processed
    def sdp2str(p : StableDiffusionProcessing):
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
        strs = [
            f"Model : {model}\r\n",
            f"VAE : {vae}\r\n",
            # f"Path : {path}\r\n",
            f"Prompt : {prompt}\r\n",
            f"Negative : {negative}\r\n",
            f"Seed : {str(seed)}\r\n",
            f"Sampler : {sampler}\r\n",
            f"CFG Scale : {str(cfg)}\r\n",
            f"Width : {str(w)}\r\n",
            f"Height : {str(h)}\r\n",
                ]
        r = ""
        print(f"Strs : {strs}")
        for s in strs:
            print(f"s : {s}")
            r = r + s
        print(f"r : {r}")
        return r
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