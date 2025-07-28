### 一、Nginx 如何**简单支持 HTTPS**

要启用 HTTPS，核心在于使用 Nginx 的 `http_ssl_module` 模块，该模块默认已启用。你只需要在你的 `nginx.conf` 或对应虚拟主机配置中添加：

```nginx
server {
    listen 443 ssl http2;                     # 监听 HTTPS 端口并启用 HTTP/2（可选）
    server_name example.com;                  # 替换为你的域名

    ssl_certificate /path/to/cert.pem;        # 公钥（证书）
    ssl_certificate_key /path/to/key.pem;     # 私钥

    ssl_protocols TLSv1.2 TLSv1.3;            # 启用的 TLS 协议版本
    ssl_ciphers HIGH:!aNULL:!MD5;             # 使用安全的加密套件

    location / {
        root /var/www/html;
        index index.html;
    }
}
```

👉 若你已有 HTTP 配置，还可以加个 HTTP→HTTPS 跳转：

```nginx
server {
    listen 80;
    server_name example.com;
    return 301 https://$host$request_uri;
}
```

------

### ✅ 二、`mod_ssl` 和 `http_ssl_module` 的区别

| 模块              | 所属软件    | 简单功能描述                                         |
| ----------------- | ----------- | ---------------------------------------------------- |
| `mod_ssl`         | Apache HTTP | Apache 的 SSL 模块，用于开启 HTTPS                   |
| `http_ssl_module` | Nginx       | Nginx 的 SSL 模块，用于配置 HTTPS、TLS、证书、密钥等 |



> 简言之：**一个是 Apache 的模块，一个是 Nginx 的模块。**

------

### ✅ 三、证书申请方式（简要）

#### ✅ 方法一：使用 [acme.sh](https://github.com/acmesh-official/acme.sh)

- 免费、自动化、支持 Let's Encrypt。
- 自动为 Nginx 签发、续签 HTTPS 证书。
- 简单示例：

```bash
curl https://get.acme.sh | sh
source ~/.bashrc
acme.sh --issue -d example.com -w /var/www/html
acme.sh --install-cert -d example.com \
  --key-file       /etc/nginx/ssl/example.key \
  --fullchain-file /etc/nginx/ssl/example.crt \
  --reloadcmd     "nginx -s reload"
```

#### ✅ 方法二：手动生成自签名证书（开发测试用）

```bash
# 生成私钥
openssl genrsa -out /etc/nginx/ssl/server.key 2048

# 生成证书请求文件（CSR）
openssl req -new -key /etc/nginx/ssl/server.key -out /etc/nginx/ssl/server.csr

# 生成自签名证书，有效期365天
openssl x509 -req -days 365 \
  -in /etc/nginx/ssl/server.csr \
  -signkey /etc/nginx/ssl/server.key \
  -out /etc/nginx/ssl/server.crt
```

配置到 Nginx：

```nginx
ssl_certificate /etc/nginx/ssl/server.crt;
ssl_certificate_key /etc/nginx/ssl/server.key;
```