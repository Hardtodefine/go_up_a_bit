------

## ✅ 这一问：Nginx 的重写规则与路径参数动态转发（含全局变量与配置对比）

------

### 一、**重写（Rewrite）的作用与配置**

#### 🔹 1. Rewrite 的用途：

- 修改请求的 URI 或路径。
- 实现 URL 美化、SEO 友好（如 `/index.php?id=1` → `/article/1`）。
- 重定向到其他页面或主机。
- 拒绝、控制非法请求。
- 配合 if 做条件跳转。

#### 🔹 2. 语法与全局变量：

```nginx
rewrite  regex  replacement  [flag];
```

- `$host`：请求主机名。
- `$request_uri`：完整 URI。
- `$uri`：请求中的资源路径。
- `$args`：请求参数（即 ? 后面的部分）。
- `$is_args`：如果 `$args` 非空，则为 "?"，否则为 ""。

------

### 🔹 3. Rewrite 的 4 个 flag 标记：

| 标记        | 说明                                                   |
| ----------- | ------------------------------------------------------ |
| `last`      | 停止当前重写，重新进行新的 location 匹配（常用）       |
| `break`     | 停止重写，不再匹配其他 rewrite 规则，继续当前 location |
| `redirect`  | 返回临时重定向（302）                                  |
| `permanent` | 返回永久重定向（301）                                  |

------

### 🔹 4. 重写示例（含主机、路径判断）：

```nginx
server {
  listen 80;

  # 示例：匹配包含 chat.openai.com 的 Host，将其跳转至 chatgpt.com
  if ($host ~* "chat\.openai\.com") {
    rewrite ^(.*)$ https://chatgpt.com$1 permanent;
  }

  # 拒绝 reload.sh 脚本的访问
  location ~ /reload\.sh$ {
    return 403;
  }

  # 最常用重写：如 /user/123 → /user.php?id=123
  rewrite ^/user/(\d+)$ /user.php?id=$1 last;
}
```

> 🔸 **注意：** `last` 表示跳出 rewrite，重新走一次 `location` 规则流程。

------

## 二、**路径参数动态转发（应用层转发）**

#### 🔹 1. 示例 upstream 块（用于反向代理）：

```nginx
upstream compute {
  server localhost:81;
}
```

#### 🔹 2. 主 server 块（动态转发路径参数）：

```nginx
server {
  listen 80;

  location ~ ^/(.*)$ {
    # 自定义响应测试
    return 200 "compute '/$1$is_args$args' resource available.\n";
  }

  location /compute/ {
    proxy_pass http://compute/$1$is_args$args;

    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    allow all;
  }
}
```

#### 🔹 参数解释：

| 配置项             | 作用                                |
| ------------------ | ----------------------------------- |
| `proxy_pass`       | 实际转发地址，注意末尾 `/` 是否保留 |
| `$1`               | 表示正则捕获组的第一个部分          |
| `$is_args$args`    | 是否带有参数（? 和参数）            |
| `proxy_set_header` | 转发请求头                          |
| `allow all`        | 允许所有来源                        |

> 🔹 **proxy_pass 注意：**

- `proxy_pass http://upstream/` → 保留后缀路径。
- `proxy_pass http://upstream`（无斜杠）→ 替换整个 location。

------

## 三、基于 HTTP 请求头的动态代理转发

举例：基于 Cookie 中的 `prod_version` 字段来判断：

```nginx
# 1. map 块：根据 cookie 映射变量
map $cookie_prod_version $version {
  default "";
  "v2.0" "v2.0";
}

# 2. server 块中使用 version 判断分流
server {
  listen 80;

  location / {
    if ($version = "v2.0") {
      proxy_pass http://v2.backend.local;
      break;
    }

    proxy_pass http://v1.backend.local;
  }
}
```

------

## 四、Location 匹配语法与匹配顺序

```nginx
location = /exact-match        {}   # 精确匹配
location ^~ /static/           {}   # 前缀匹配，优先级高
location ~ \.php$              {}   # 正则匹配（区分大小写）
location ~* \.jpg$             {}   # 正则匹配（不区分大小写）
location /                    {}   # 默认匹配（兜底）
```

📌 **匹配优先级（从高到低）**：

```
= > ^~ > ~ / ~* > 普通前缀匹配
```

------

### 🔚 总结（十问十答形式）：

> ❓**Nginx 如何实现 URL 重写与路径参数动态转发？**

Nginx 的重写（rewrite）规则通过修改请求路径、判断请求主机或条件跳转，灵活控制 URI 流向，而路径参数动态转发（配合正则匹配、upstream 块）则实现在应用层通过参数将请求转发至不同服务节点。理解 rewrite 的 4 个 flag、常用全局变量，以及 proxy_pass 中斜杠的处理，是构建高灵活性 Nginx 代理配置的核心。同时也可结合请求头（如 Cookie）进行动态路由分发。