import os
from PIL import Image
import numpy as np

def is_row_white(row):
    """判断给定的行是否为全白色"""
    return np.all(row == 255)

def binarize_image(img, threshold=128):
    """对图像进行二值化处理"""
    # 将图像转换为灰度图像
    img_gray = img.convert('L')
    # 应用阈值进行二值化
    img_bw = img_gray.point(lambda x: 0 if x < threshold else 255, '1')
    return img_bw

# Function to crop the image into two halves and save with _a and _b suffixes
def split_image_half(image_path, output_dir):
    # Open an image file
    with Image.open(image_path) as img:
        # Get image dimensions
        width, height = img.size
        filename = os.path.splitext(os.path.basename(image_path))[0]  # Extract filename without extension

        # Top half (_a)
        top_half = img.crop((0, 0, width, height // 2))
        top_half.save(os.path.join(output_dir, f"{filename}_a.jpg"))

        # Bottom half (_b)
        bottom_half = img.crop((0, height // 2, width, height))
        bottom_half.save(os.path.join(output_dir, f"{filename}_b.jpg"))

        print(f"Saved {filename}_a.jpg and {filename}_b.jpg")

# Function to process all jpg files in a directory
def process_images_in_directory(input_dir, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Process each image file
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.jpg'):
            input_path = os.path.join(input_dir, filename)
            split_image_half(input_path, output_dir)

# Define your input and output directories
input_directory = './'  # Update this path
output_directory = './img2'  # Update this path

# Process images
process_images_in_directory(input_directory, output_directory)
