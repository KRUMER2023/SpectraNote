from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import threading
import os
import sys

class SystemTrayIcon:
    def __init__(self, exit_callback=None):
        self.exit_callback = exit_callback
        self.icon = None
        self.thread = None

    def create_image(self, width, height, color1, color2):
        image = Image.new('RGB', (width, height), color1)
        dc = ImageDraw.Draw(image)
        dc.rectangle((width // 2, 0, width, height // 2), fill=color2)
        dc.rectangle((0, height // 2, width // 2, height), fill=color2)
        return image

    def on_login(self, icon, item):
        print("[Tray]: Login")

    def on_updates(self, icon, item):
        print("[Tray]: Updates")

    def on_exit(self, icon, item):
        print("[Tray]: Exit")
        if self.icon:
            self.icon.stop() 
        # Optionally force exit main app if desired, but runner handles tray structure
        # If runner calls tray.stop(), this callback is internal to tray menu.
        # But if user clicks Exit on tray, we likely want to close the whole app.
        os._exit(0)

    def setup_tray(self):
        # Determine icon path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(current_dir, "icon.png")
        
        try:
            image = Image.open(icon_path)
        except Exception as e:
            print(f"[WARN] Could not load icon.png: {e}")
            image = self.create_image(64, 64, 'black', 'white')

        menu = Menu(
            MenuItem('Login', self.on_login),
            MenuItem('Updates', self.on_updates),
            MenuItem('Exit', self.on_exit)
        )

        self.icon = Icon("SpectraNote", image, "SpectraNote", menu)

    def run(self):
        self.setup_tray()
        self.icon.run()

    def start_in_thread(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        if self.icon:
            self.icon.stop()
