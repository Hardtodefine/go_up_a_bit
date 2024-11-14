## async和defer 

script标签加入async

如果遇到没有属性的script标签浏览器暂停解析去加载和执行script

浏览器遇到 async 脚本时不会阻塞页面渲染，而是直接下载然后暂停解析html运行。这样脚本的运行

次序就无法控制，只是脚本不会阻止剩余页面的显示。当页面的脚本之间彼此独立，且不依赖于本页面的其它任何脚本时，

async 是最理想的选择。

```html
<script defer src="js/vendor/jquery.js"></script>
<script defer src="js/script2.js"></script>
<script defer src="js/script3.js"></script>
```

三者的调用顺序是不确定的。

jquery.js 可能在 script2 和 后两个脚本中依赖 script3 之前或之后调用，如果这样，

jquery 的函数将产生错误，因为脚本运行时 jquery 尚未加载。

解决这一问题可使用 defer 属性，脚本将按照在页面中出现的顺序加载和运行
