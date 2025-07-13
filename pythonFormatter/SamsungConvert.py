#   @author Tim Rothenhaeusler
#   @date   13.07.2025

# This Script can be used to format pictures to display them optimized on your Samsung The Frame

import os
import sys
from PIL import Image, ImageEnhance

TARGET_WIDTH = 1920
TARGET_HEIGHT = 1080
TARGET_ASPECT = TARGET_WIDTH / TARGET_HEIGHT

def resize_and_crop(image):
    orig_width, orig_height = image.size
    orig_aspect = orig_width / orig_height

    if orig_aspect > TARGET_ASPECT:
        new_width = int(orig_height * TARGET_ASPECT)
        offset = (orig_width - new_width) // 2
        image = image.crop((offset, 0, offset + new_width, orig_height))
    elif orig_aspect < TARGET_ASPECT:
        new_height = int(orig_width / TARGET_ASPECT)
        offset = (orig_height - new_height) // 2
        image = image.crop((0, offset, orig_width, offset + new_height))

    return image.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.LANCZOS)

def enhance_image(image):
    image = ImageEnhance.Color(image).enhance(0.95)
    image = ImageEnhance.Brightness(image).enhance(1.05)
    image = ImageEnhance.Contrast(image).enhance(0.98)
    return image

def process_images(apply_optimization=False):
    input_folder = "input"
    output_folder = os.path.join(input_folder, "convertedFrame")
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith((".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff")):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.jpg")

            with Image.open(input_path) as img:
                img = img.convert("RGB")
                resized = resize_and_crop(img)
                if apply_optimization:
                    resized = enhance_image(resized)
                resized.save(output_path, "JPEG", quality=95)

            print(f"✔️ Verarbeitet: {filename}")

if __name__ == "__main__":
    optimize = "--opti" in sys.argv
    process_images(apply_optimization=optimize)
