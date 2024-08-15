import argparse

def preload(parser: argparse.ArgumentParser):
    parser.add_argument(
            "--LINE-Notify-Token",
            dest = "LINE_Notify_Token",
            default = None,
            help = "[Send to LINE Notify] LINE Notify Token",
            )

