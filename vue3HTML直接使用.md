下面是一个基于Vue 3的简单示例教程，该教程将指导您如何创建一个包含按钮和对话框组件的基本Vue应用。我们将使用Composition API来定义组件的行为，并通过插槽（slots）传递内容。

### 准备工作

首先，确保您的HTML文件结构如下所示，这将作为Vue应用的入口点。

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Vue 3 示例</title>
  <style>
    .myButton {
      display: inline-flex;
      box-sizing: border-box;
      position: relative;
      height: 32px;
      padding: 10px 12px;
      cursor: pointer;
      justify-content: center;
      align-items: center;
      background: #f3f0f1;
      color: #333;
      border: 0 solid;
      border-radius: 4px;
      transition: all 0.3s;
      box-shadow: 0px 0px 10px rgba(255, 255, 255, 1), 6px 6px 10px rgba(0, 0, 0, 0.2);
    }
  </style>
</head>
<body>
  <div id="app"></div>
  <script src="https://unpkg.com/vue@next"></script>
  <script>
    // 这里将会添加Vue 3的应用代码
  </script>
</body>
</html>
```

### 创建Vue应用

在`<script>`标签中，我们开始编写Vue 3的应用代码。这里我们将定义两个组件：一个按钮组件和一个对话框组件。

#### 定义组件

1. **Button组件** - 用于触发对话框的显示或隐藏。

```javascript
const Button = {
  props: ['disabled'],
  template: `<button
    class="myButton"
    :disabled="disabled"
  >
    <slot></slot>
  </button>`
}
```

2. **Dialog组件** - 显示一个可关闭的对话框。

```javascript
const Dialog = {
  props: {
    visible: Boolean,
    fnc1: Function,
    fnc2: Function,
    CloseByClickOverlay: Boolean
  },
  emits: ['update:visible'],
  template: `
    <div v-if="visible" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5);">
      <div style="background: white; margin: 20% auto; padding: 20px; width: 50%; text-align: center;">
        <slot name="title"></slot>
        <hr>
        <slot name="content"></slot>
        <br>
        <Button @click="$emit('update:visible', false)">关闭</Button>
      </div>
    </div>
  `
}
```

#### 创建Vue实例

接下来，我们需要创建Vue应用实例并注册这两个组件。

```javascript
const { createApp, ref } = Vue;

createApp({
  template: `
    <h1>示例1</h1>
    <Button @click="toggle">显示对话框</Button>
    <Dialog
      :visible="showon"
      :fnc1="f1"
      :fnc2="f2"
      :CloseByClickOverlay="false"
      @update:visible="showon = $event"
    >
      <template v-slot:title>
        <strong>这里是标题</strong>
      </template>
      <template v-slot:content>
        <span>这里是内容</span>
      </template>
    </Dialog>
  `,
  setup() {
    const showon = ref(false);

    const toggle = () => {
      showon.value = !showon.value;
    };

    const f1 = () => {
      console.log('Function 1 called');
    };

    const f2 = () => {
      console.log('Function 2 called');
    };

    return {
      showon,
      toggle,
      f1,
      f2
    };
  }
}).component('Button', Button).component('Dialog', Dialog).mount('#app');
```

### 测试应用

保存文件并在浏览器中打开它。你应该能看到一个按钮，点击后会弹出一个对话框。对话框中有一个关闭按钮，点击它可以关闭对话框。

这个简单的例子展示了如何使用Vue 3的Composition API来构建交互式组件。您可以根据需要修改样式和功能，以适应不同的应用场景。