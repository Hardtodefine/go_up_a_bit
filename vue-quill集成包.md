#### 1. 安装依赖

#### 2. 引入 Quill 样式

#### 3. 创建 Vue 组件

```html
<template>
  <div>
    <quill-editor
      ref="myTextEditor"
      v-model="content"
      :options="editorOption"
      @ready="onEditorReady($event)"
    ></quill-editor>
    <input ref="upload" type="file" accept="image/*" @change="fileSend" />
  </div>
</template>

<script>
import 'quill/dist/quill.core.css';
import 'quill/dist/quill.snow.css';
import 'quill/dist/quill.bubble.css';
import { quillEditor, Quill } from 'vue-quill-editor';

export default {
  name: 'NewsEdit',
  components: {
    quillEditor
  },
  data() {
    return {
      content: '',
      editorOption: {
        modules: {
          toolbar: {
            container: [
              ['bold', 'italic', 'underline', 'strike'], // 加粗，斜体，下划线，删除线
              ['blockquote', 'code-block'], // 引用，代码块
              [{ script: 'sub' }, { script: 'super' }], // 下角标，上角标
              [{ indent: '-1' }, { indent: '+1' }], // 缩进
              [{ size: ['small', false, 'large', 'huge'] }], // 字体大小
              [{ color: [] }, { background: [] }], // 颜色选择
              [{ font: [] }], // 字体
              [{ align: [] }], // 对齐方式
              ['image'], // 图片
              ['clean'] // 清除样式
            ],
            handlers: {
              image: () => {
                this.uploadImage();
              }
            }
          }
        },
        placeholder: '写点什么吧。。。'
      }
    };
  },
  computed: {
    editor() {
      return this.$refs.myTextEditor.quill;
    }
  },
  methods: {
    onEditorReady(editor) {
      console.log('Editor is ready!', editor);
    },
    uploadImage() {
      this.$refs.upload.click();
    },
    async fileSend(e) {
      this.editor.focus();
      const data = new FormData();
      data.append('image', this.$refs.upload.files[0]);
      try {
        const response = await this.$API(this.api, data);
        if (response.st === 1) {
          const index = this.editor.getSelection().index;
          this.editor.insertEmbed(index, 'image', response.data.url);
          this.editor.setSelection(index + 1, 0, 'api');
        } else {
          this.$message.error(response.msg);
        }
      } catch (error) {
        console.error('Error uploading image:', error);
        this.$message.error('上传失败');
      }
    }
  }
};
</script>

<style scoped>
/* 你可以在这里添加一些自定义样式 */
</style>
```

1. **引入 Quill 样式**：
   - `import 'quill/dist/quill.core.css';`
   - `import 'quill/dist/quill.snow.css';`
   - `import 'quill/dist/quill.bubble.css';`
2. **注册 Quill Editor 组件**：
   - `components: { quillEditor }`
3. **数据和选项**：
   - `content`：绑定到编辑器的内容。
   - `editorOption`：Quill Editor 的配置选项，包括工具栏按钮和事件处理器。
4. **计算属性**：
   - `editor`：获取 Quill 实例，用于操作编辑器。
5. **方法**：
   - `onEditorReady(editor)`：编辑器准备就绪时的回调。
   - `uploadImage()`：触发文件选择器，让用户选择图片。
   - `fileSend(e)`：处理图片上传，将图片插入到编辑器中。
6. **模板**：
   - `<quill-editor>`：Quill Editor 组件。
   - `<input>`：隐藏的文件选择器，用于选择图片。