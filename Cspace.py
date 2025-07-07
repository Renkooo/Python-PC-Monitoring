import psutil
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw, ImageFont
import threading
import time
import math

def get_remaining_disk_space():
    usage = psutil.disk_usage('C:\\')
    remaining_gb = usage.free / (1024 ** 3)
    return math.floor(remaining_gb)

def create_image(text):
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), color=(155 , 25 , 50))

    font_size = 60  
    font = ImageFont.truetype("arialbd.ttf", font_size)

    draw = ImageDraw.Draw(image)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_position = ((width - text_width) // 2, ((height - text_height) // 2) - 10)
    
    draw.text(text_position, text, font=font, fill="black")
    
    return image

def update_icon(icon):
    while True:
        remaining_gb = get_remaining_disk_space()
        icon.icon = create_image(f"{remaining_gb}")
        time.sleep(30)

def quit_program(icon, item):
    icon.stop()

def setup_tray_icon():
    icon = pystray.Icon("Disk Space Monitor")
    icon.menu = pystray.Menu(
        item('Quit', quit_program)
    )

    icon.icon = create_image("Loading")
    icon.title = "Disk Free Space Monitor"
    
    update_thread = threading.Thread(target=update_icon, args=(icon,))
    update_thread.daemon = True
    update_thread.start()

    icon.run()

if __name__ == "__main__":
    setup_tray_icon()
