要在网页中使用iframe进行登录相关的通信，可以采用以下方法：

#### 同源情况下的通信

1. **使用 `window.parent` 和 `window.frames`**
    - **iframe内调用外部方法**：在iframe中，通过 `window.parent` 访问父页面的window对象，然后调用父页面的方法。

      ```javascript
      // iframe内代码
      window.parent.loginCallback(data);
      ```

    - **外部调用iframe内方法**：在父页面中，通过 `window.frames[index]` 或 `document.getElementById('iframeId').contentWindow` 访问iframe的window对象，然后调用iframe内的方法。

      ```javascript
      // 父页面代码
      window.frames[0].loginSuccess();
      // 或
      document.getElementById('iframeId').contentWindow.loginFailed();
      ```

2. **使用本地存储（`localStorage` 或 `sessionStorage`）**
    - **iframe内存储数据**：在iframe中，将登录信息存储在本地存储中。

      ```javascript
      // iframe内代码
      localStorage.setItem('loginInfo', JSON.stringify(data));
      ```

    - **外部获取数据**：在父页面中，从本地存储中获取登录信息。

      ```javascript
      // 父页面代码
      const loginInfo = JSON.parse(localStorage.getItem('loginInfo'));
      ```

#### 跨域情况下的通信

1. **使用 `postMessage`**
    - **iframe内发送消息**：在iframe中，使用 `window.parent.postMessage` 向父页面发送消息。

      ```javascript
      // iframe内代码
      window.parent.postMessage({
        action: 'loginSuccess',
        data: data
      }, '*'); // 或指定父页面的域名
      ```

    - **外部接收消息**：在父页面中，监听 `message` 事件，接收并处理来自iframe的消息。

      ```javascript
      // 父页面代码
      window.addEventListener('message', function(event) {
        if (event.origin === 'http://iframe-domain.com') { // 验证消息来源
          if (event.data.action === 'loginSuccess') {
            const loginData = event.data.data;
            // 处理登录成功逻辑
          }
        }
      });
      ```

    - **外部发送消息**：在父页面中，通过 `document.getElementById('iframeId').contentWindow.postMessage` 向iframe发送消息。

      ```javascript
      // 父页面代码
      document.getElementById('iframeId').contentWindow.postMessage({
        action: 'loginFailed',
        data: data
      }, '*'); // 或指定iframe的域名
      ```

    - **iframe内接收消息**：在iframe中，监听 `message` 事件，接收并处理来自父页面的消息。

      ```javascript
      // iframe内代码
      window.addEventListener('message', function(event) {
        if (event.origin === 'http://parent-domain.com') { // 验证消息来源
          if (event.data.action === 'loginFailed') {
            const loginData = event.data.data;
            // 处理登录失败逻辑
          }
        }
      });
      ```

2. **使用中间代理页面**
    - 创建一个与父页面同域但不同路由的中间代理页面。
    - 在iframe中，通过修改中间代理页面的URL参数或使用 `postMessage` 向中间代理页面传递登录信息。
    - 中间代理页面接收到信息后，调用父页面的方法，将登录信息传递给父页面。

#### 注意事项

- **安全性**：在跨域通信时，务必验证消息的来源 (`event.origin`)，防止恶意攻击。
- **数据格式**：传递的数据应为字符串或可序列化的对象，确保在不同窗口间正确传输。
- **兼容性**：不同浏览器对通信方法的支持可能有所不同，需进行兼容性测试。

## window.parent

> 返回当前窗口的父窗口对象。
>
> 如果一个窗口没有父窗口，则它的 `parent` 属性为自身的引用