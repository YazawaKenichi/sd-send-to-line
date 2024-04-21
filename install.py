import launch

packages = {
        "pillow" : "Pillow",
        "gradio" : "gradio",
        "requests" : "requests",
        }

if __name__ == "__main__":
    for package_name in packages:
        package = packages[package_name]
        try:
            if not launch.is_installed(package_name):
                launch.run_pip(f"install {package}", f"[Send to LINE Notify] : {package_name}")
        except Exception as e:
            print(e)
            print(f"Warning: Failed to install {package}, some preprocessors may not work.")

