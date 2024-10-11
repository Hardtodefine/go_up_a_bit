wasm全称WebAssembly

wasm是一种低级汇编语言,js是高级脚本语言

这两种语言都可以在现代浏览器中运行,不过wasm需要一些处理才可以运行

浏览器兼容性见 [MDN](https://link.juejin.cn?target=https%3A%2F%2Fdeveloper.mozilla.org%2Fzh-CN%2Fdocs%2FWebAssembly%2FJavaScript_interface%2FinstantiateStreaming)

本以为wasm是直接在浏览器上运行c代码,其实不是的

c/c++需要先通过编译成.wasm文件

需要使用[Emscripten](https://link.juejin.cn?target=https%3A%2F%2Femscripten.org%2F)来进行编译

也可以参考[MDN](https://link.juejin.cn?target=https%3A%2F%2Fdeveloper.mozilla.org%2Fzh-CN%2Fdocs%2FWebAssembly%2FC_to_Wasm%23emscripten_%E7%8E%AF%E5%A2%83%E5%AE%89%E8%A3%85)

可以选择只编译出.wasm和.js

.wasm文件不能在script标签中直接运行

```js
js 代码解读复制代码下面是两个官方例子
较老的api需要转换arraybuffer
WebAssembly.instantiate()
fetch("simple.wasm")
  .then((res) => res.arrayBuffer())
  .then((bytes) => WebAssembly.instantiate(bytes, importObject))
  .then((results) => {
    results.instance.exports.exported_func();
  });
较新的则不需要
WebAssembly.instantiateStreaming()
var importObject = { imports: { imported_func: (arg) => console.log(arg) } };

WebAssembly.instantiateStreaming(fetch("simple.wasm"), importObject).then(
  (obj) => obj.instance.exports.exported_func(),
);
```

### 像script标签加载js一样运行wasm

```html
html 代码解读复制代码<script>
async function loadWasm (){
const module = await WebAssembly.compileStreaming(fetch('your.wasm'));
const instance = await module.instantiate()
}
loadWasm()
</script>
```

[instantiateStreaming(MDN)](https://link.juejin.cn?target=https%3A%2F%2Fdeveloper.mozilla.org%2Fzh-CN%2Fdocs%2FWebAssembly%2FJavaScript_interface%2FinstantiateStreaming)

[compileStreaming(MDN)](https://link.juejin.cn?target=https%3A%2F%2Fdeveloper.mozilla.org%2Fzh-CN%2Fdocs%2FWebAssembly%2FJavaScript_interface%2FcompileStreaming)

这篇帖子介绍了调用较老的api来运行wasm

[blog.csdn.net/ResumeProje…](https://link.juejin.cn?target=https%3A%2F%2Fblog.csdn.net%2FResumeProject%2Farticle%2Fdetails%2F126441261)

c/c++编译

[developer.mozilla.org/zh-CN/docs/…](https://link.juejin.cn?target=https%3A%2F%2Fdeveloper.mozilla.org%2Fzh-CN%2Fdocs%2FWebAssembly%2FC_to_Wasm%23emscripten_%E7%8E%AF%E5%A2%83%E5%AE%89%E8%A3%85)

Rust等其他语言则需要其他的编译和环境