## 一、理论基础：浏览器的两级缓存机制

浏览器缓存机制主要包括 **强缓存** 和 **协商缓存** 两类：

### ✅ 1. 强缓存（无需发请求）

**控制字段：**

- `Expires`（HTTP/1.0，已过时但仍存在）
- `Cache-Control: max-age=秒数`（HTTP/1.1，更推荐）

**特点：**

- 浏览器发现资源命中强缓存后，**不会发请求**，直接用本地缓存资源。
- 状态码：`200 (from disk cache)` 或 `200 (from memory cache)`。

------

### ✅ 2. 协商缓存（发请求 + 返回304）

当强缓存过期后，浏览器会发送带**条件的请求头**，询问服务端资源有没有变。

| 控制字段            | 谁发出 | 放在头部 | 说明                               |
| ------------------- | ------ | -------- | ---------------------------------- |
| `Last-Modified`     | 服务器 | 响应头   | 告诉浏览器资源最后的修改时间       |
| `If-Modified-Since` | 浏览器 | 请求头   | 告诉服务器：我有这个修改时间的资源 |
| `ETag`              | 服务器 | 响应头   | 告诉浏览器资源的唯一版本标识符     |
| `If-None-Match`     | 浏览器 | 请求头   | 告诉服务器：我有这个版本号的资源   |

**返回状态码：**

- 若资源没变，服务器返回 `304 Not Modified`；
- 若资源变了，返回 `200 OK` 并附上新资源内容。

------

## 二、请求响应过程（客户端视角）

**第一次请求：**

```http
GET /main.css HTTP/1.1
Host: www.example.com
```

**服务器响应（含缓存控制字段）：**

```http
HTTP/1.1 200 OK
Last-Modified: Mon, 26 Jul 2025 07:28:00 GMT
ETag: "abc123"
Cache-Control: max-age=3600
```

浏览器缓存该资源，并记录 Last-Modified 和 ETag。

------

**第二次请求（1小时内）：命中强缓存**

```bash
→ 浏览器不会发请求，直接返回本地缓存。
```

------

**第三次请求（1小时后）：发起协商缓存请求**

```http
GET /main.css HTTP/1.1
If-Modified-Since: Mon, 26 Jul 2025 07:28:00 GMT
If-None-Match: "abc123"
```

**服务器检查后：资源未改**

```http
HTTP/1.1 304 Not Modified
```

------

## 三、Nginx 配置解析（核心）

### ✅ 配置强缓存

```nginx
location ~* \.(js|css|png|jpg|jpeg|gif|ico|woff|woff2|ttf)$ {
    expires 30d;  # 设置缓存时间为 30 天
    add_header Cache-Control "public";
}
```

效果：

- 浏览器收到响应后会将资源缓存 30 天，期间不会再次请求服务器。

### ❗ 禁止强缓存（调试时常用）

```nginx
location / {
    expires -1;  # 立即过期，触发协商缓存
    add_header Cache-Control "no-store";
}
```

`expires -1` 表示设置过去的时间，使强缓存立刻失效。

------

### ✅ 配置协商缓存（Nginx 默认开启）

```nginx
location / {
    # 不需要额外配置，nginx 静态资源默认开启 last-modified
    # 如需关闭：add_header Last-Modified "";
}
```

但默认 **不会开启 ETag**，若你希望使用 ETag，可以开启：

```nginx
etag on;
```

你也可以关闭它：

```nginx
etag off;
```

------

## 四、强缓存 vs 协商缓存总结表

| 特性             | 强缓存                  | 协商缓存                                                 |
| ---------------- | ----------------------- | -------------------------------------------------------- |
| 控制字段         | Expires / Cache-Control | Last-Modified + If-Modified-Since / ETag + If-None-Match |
| 是否发请求       | 否                      | 是                                                       |
| 状态码           | 200 (from cache)        | 304 Not Modified                                         |
| 是否节省带宽     | ✅                       | ✅                                                        |
| 是否节省响应延迟 | ✅                       | ❌（需一次往返）                                          |
| 是否需服务器判断 | ❌                       | ✅                                                        |

```nginx
http {
    include       mime.types;
    default_type  application/octet-stream;

    # 开启 Gzip 压缩（可选，提升静态资源性能）
    gzip on;
    gzip_types text/css application/javascript;

    server {
        listen       80;
        server_name  localhost;

        # 静态资源路径映射
        location /static/ {
            root D:/your_project_path/;  # 假设 index.css 在 D:/your_project_path/static/index.css

            # 强缓存控制：浏览器会缓存 index.css 60 秒，不发请求
            # Cache-Control 优先于 Expires
            expires 60s;                  # 或 expires 1h; 设置为 0 表示立即过期
            add_header Cache-Control "max-age=60";  # 60 秒强缓存
            # add_header Cache-Control "no-cache";  # 配合协商缓存使用
            # add_header Cache-Control "no-store";  # 每次都重新请求，不缓存

            # 协商缓存
            # 如果文件有变化（时间或内容），返回 200；否则返回 304
            # last_modified 是 Nginx 默认支持的
            # etag 默认是 off，可以手动开启
            etag on;

            # 可选：关闭缓存用于调试
            # expires -1;  # 永远过期，方便调试用
        }

        # 反向代理配置，代理其他 API 请求等
        location /api/ {
            proxy_pass http://localhost:3000;  # 代理到后端服务

            # 以下是 WebSocket 和长连接兼容配置
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }

        # 默认首页
        location / {
            root   D:/your_project_path/;
            index  index.html;
        }
    }
}

```

