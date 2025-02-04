# sd-send-to-line

[![YouTube Video](https://i.ytimg.com/vi/mTh_4K-HJZI/maxresdefault.jpg)](https://youtu.be/mTh_4K-HJZI)

<sup>生成された画像のせいでイケナイ動画みたいに見える...</sup>

# 概要
画像の生成が終了したら [LINE Notify API](https://notify-bot.line.me/) を通じて LINE で生成画像とそのパラメータを送信してくれる拡張機能

使用するには LINE Notify のアクセストークンが必要

詳細 : [LINE Notify](https://notify-bot.line.me/)

> [!CAUTION]
> LINE Notify API のサービス終了に伴ってこの拡張機能は正常に動作しません。
> 代替 API を用いて当リポジトリで継続して開発をことを検討しておりますが、目途は立っておりません。

# インストール
WebUI の `Extensions` > `Install from URL` からインストール

``` bash
https://github.com/yazawakenichi/sd-send-to-line
```

または

`Stable-Diffusion-WebUI` > `extensions` で `git clone`

``` bash
git clone git@github.com:yazawakenichi/sd-send-toline
```

# 使い方
`txt2img` とか `img2img` のタブの `ControlNet` とかのタブと一緒に並ぶ

LINE Notify から取得したトークンを `LINE Notify token` に入力

あとはいつも通り画像を Generate すると生成終了時に LINE Notify から画像が届く

