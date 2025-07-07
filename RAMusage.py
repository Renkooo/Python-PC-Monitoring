import psutil
import pystray
from pystray import MenuItem as item
from PIL import Image, ImageDraw, ImageFont
import threading
import time
import math

def get_ram_usage_percentage():
    memory_info = psutil.virtual_memory()
    return math.ceil(memory_info.percent)

def create_image(text):
    width = 64
    height = 64
    image = Image.new('RGB', (width, height), color=(0, 74, 161))

    if len(text) <= 2:
        font_size = 60
    elif len(text) == 3:
        font_size = 50
    else:
        font_size = 40

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
        ram_usage = get_ram_usage_percentage()
        icon.icon = create_image(f"{ram_usage}")
        time.sleep(1)  

def quit_program(icon, item):
    icon.stop()

def setup_tray_icon():
    icon = pystray.Icon("RAM Usage Monitor")
    icon.menu = pystray.Menu(
        item('Quit', quit_program)
    )

    icon.icon = create_image("Loading")
    icon.title = "RAM Usage Monitor"

    update_thread = threading.Thread(target=update_icon, args=(icon,))
    update_thread.daemon = True
    update_thread.start()

    icon.run()

if __name__ == "__main__":
    setup_tray_icon()
