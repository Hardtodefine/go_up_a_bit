from PIL import Image
import numpy as np

def print_image_info(img, message):
    print(message)
    print(f"Image size: {img.size}")
    print(f"Image mode: {img.mode}\n")

def is_row_white(row):
    """判断给定的行是否为几乎全白色，使用方差来判断"""
    print(f"Checking row: {row[:10]} ... ({len(row)} elements)")
    mean_color = np.mean(row)
    variance = np.var(row)
    print(f"Mean color value: {mean_color}, Variance: {variance}")

    # 如果方差小于某个阈值，则认为这行是几乎相同的颜色
    threshold_variance = 5  # 根据实际情况调整这个阈值
    result = variance < threshold_variance
    print(f"Is row almost all white? {result}\n")
    return result

def binarize_image(img, threshold=128):
    """对图像进行二值化处理"""
    # 将图像转换为灰度图像
    img_gray = img.convert('L')
    print_image_info(img_gray, "Converted image to grayscale:")

    # 应用阈值进行二值化
    img_bw = img_gray.point(lambda x: 0 if x < threshold else 255, '1')
    print_image_info(img_bw, "Binarized image:")

    return img_bw

def print_last_row_pixels(img):
    """打印图像的最后一行像素信息"""
    width, height = img.size
    last_row = []
    for x in range(width):
        pixel = img.getpixel((x, height - 1))
        last_row.append(pixel)
    print(f"Last row pixels: {last_row[:10]} ... ({len(last_row)} elements)\n")

# 示例图像路径
image_path = './Snipaste_2024-09-18_10-01-56.png'  # 请替换为你的图像路径

# 加载图像
img = Image.open(image_path)

# 打印原始图像的最后一行像素信息
print_last_row_pixels(img)
print_image_info(img, "Original image:")

# 二值化图像
binarized_img = binarize_image(img)

# 打印二值化图像的最后一行像素信息
print_last_row_pixels(binarized_img)

# 检测最后一行的颜色是否为几乎全白色
width, height = binarized_img.size
last_row_pixels = [binarized_img.getpixel((x, height - 1)) for x in range(width)]
if is_row_white(last_row_pixels):
    print("The last row is almost all white.")
else:
    print("The last row is not almost all white.")