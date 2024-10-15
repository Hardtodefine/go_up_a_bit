```js
document.getElementById('fileInput').addEventListener('change', (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      const dataUrl = e.target.result;
      compressImage(800, 600, dataUrl);
    };
    reader.readAsDataURL(file);
  }
});

/**
 * 压缩图片
 * @param {number} w - 压缩后的宽度
 * @param {number} h - 压缩后的高度
 * @param {string} dataUrl - 图片的 Data URL
 */
function compressImage(w, h, dataUrl) {
  // 创建一个新的 Image 对象
  const img = new Image();
  img.src = dataUrl;

  // 确保图片加载完成后执行压缩操作
  img.onload = () => {
    // 创建一个新的 Canvas 元素
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');

    // 设置 Canvas 的宽度和高度
    canvas.width = w;
    canvas.height = h;

    // 高清化处理
    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = 'high';

    // 将图片绘制到 Canvas 上
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);

    // 将 Canvas 内容转换为 Blob 对象
    canvas.toBlob((blob) => {
      // 创建一个新的 File 对象
      const compressedFile = new File([blob], 'compressed_image.jpg', { type: blob.type });

      // 检查压缩后的文件大小
      if (compressedFile.size > 5000) {
        // 更新文件对象
        this.filebus = compressedFile;

        // 显示成功消息
        this.$message({
          message: '压缩成功',
          type: 'success',
        });

        // 设置裁剪标志
        this.cropperFlag = true;
      } else {
        // 显示失败消息
        this.$message({
          message: '压缩失败',
          type: 'error',
        });
      }

      // 预览压缩后的图片
      const previewImg = document.getElementById('preview');
      previewImg.src = URL.createObjectURL(compressedFile);
      previewImg.style.display = 'block';
    }, 'image/jpeg', 0.8); // 第二个参数是质量，范围从 0 到 1
  };
}
```

