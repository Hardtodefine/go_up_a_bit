### **1. 防盗链配置：`valid_referers`**

#### ✅ **语法示例**：

```nginx
location ~* \.(jpg|png|gif|mp4|pdf)$ {
    valid_referers none blocked server_names *.example.com example.com;
    if ($invalid_referer) {
        return 403;
    }
}
```

#### ✅ **关键说明**：

- `none`：允许空的 Referer（有些浏览器或情况不发送）。
- `blocked`：允许被防火墙或浏览器移除 Referer 的请求。
- `server_names`：自动匹配当前 server_name。
- 也可以手动列出白名单域名，如 `*.yourdomain.com`。
- `$invalid_referer`：这个变量为 `1` 时表示当前请求的 Referer 不合法。

#### ✅ **用途**：

防止其他网站盗用你的资源（比如直接贴图、盗视频等），限制只能从自己站点引用。

------

### **2. Gzip 配置相关（压缩、比例、模块版本）**

#### ✅ **基本启用**：

```nginx
gzip on;
```

#### ✅ **推荐配置**（带比例和文件类型）：

```nginx
gzip on;
gzip_comp_level 6;                # 压缩级别，1-9（数字越大压缩越好，CPU越高）
gzip_min_length 1024;            # 超过这个字节数才压缩
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss;
gzip_vary on;                    # 告诉缓存服务器有压缩版本
gzip_disable "msie6";            # 避免老IE崩溃
```

#### ✅ **是否需要 `gzip_static on;`？**

- **有打包生成 `.gz` 文件的项目（如 Vue 打包器）就配上**：

```nginx
gzip_static on;
```

- 作用是：如果发现有同名的 `.gz` 文件，**直接返回它而不重新压缩**，更快。

#### ✅ **压缩比例**

- 浏览器和服务端协商支持 gzip。
- 对文本类资源通常压缩率 **60~80%**，非常显著。

#### ✅ **模块版本**

- Nginx 编译时默认就有 `ngx_http_gzip_module`，除非自己手动去掉。
- `gzip_static` 是单独模块，有些老版本没启用，需要手动编译开启。

------

### **3. 跨域问题 `Access-Control-Allow-Origin`**

#### ✅ **你说的没错**：跨域的确**通常在 Node.js 层（如 Express）处理**，但 Nginx 也可以直接处理跨域响应头。

#### ✅ **Nginx 设置跨域**：

```nginx
location /api/ {
    add_header Access-Control-Allow-Origin *;
    add_header Access-Control-Allow-Methods GET,POST,OPTIONS;
    add_header Access-Control-Allow-Headers *;
}
```

- `*` 表示允许任意域访问，适用于公开 API。
- 若有鉴权需求，需设定具体域名、允许的 headers（如 Authorization）等。

------

### 🔚 总结

| 功能       | 用法简述                                                     |
| ---------- | ------------------------------------------------------------ |
| **防盗链** | `valid_referers none blocked server_names` + 判断 `$invalid_referer` |
| **Gzip**   | `gzip on; gzip_types ...; gzip_static on;` 支持打包后的 `.gz` |
| **跨域**   | `add_header Access-Control-Allow-Origin *;` 可在 Nginx 层设置 |