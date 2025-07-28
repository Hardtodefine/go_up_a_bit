### Nginx知识精选：反向代理与正向代理中的TLS/SSL处理



本文将深入探讨 Nginx 在两种核心代理模式下处理加密流量的配置与原理。

------



#### **问一：如何在 Nginx 中实现 SSL/TLS 卸载，并进行安全与性能优化？这属于双向认证（mTLS）吗？**



**答：** SSL/TLS 卸载 (SSL/TLS Termination) 是 Nginx 作为反向代理的经典应用场景。它指由 Nginx 对外处理所有 HTTPS 加密解密工作，然后以无需加密的 HTTP 协议与内部服务器通信，从而减轻后端服务的计算压力。



##### **1. 核心配置：SSL/TLS 卸载**



以下是一个典型的 SSL 卸载配置，它实现了外部客户端使用 `HTTPS` 访问，而 Nginx 代理到内部的 `HTTP` 服务。

Nginx

```
server {
    # 1. 监听 443 端口，并启用 SSL 和 HTTP/2
    listen 443 ssl http2;
    server_name your.domain.com;

    # 2. 配置服务器证书和私钥
    ssl_certificate /path/to/your/fullchain.pem;
    ssl_certificate_key /path/to/your/private.key;

    # 3. [安全增强] 使用更健壮的 DH 参数用于密钥交换
    #    生成命令: openssl dhparam -out /path/to/dhparam.pem 2048
    ssl_dhparam /path/to/dhparam.pem;

    # 4. [性能与安全] 优先使用性能更高的椭圆曲线进行密钥交换
    ssl_ecdh_curve X25519:P-256:P-384;
    
    # 5. [性能优化] 配置 SSL Session 缓存，见下文详述
    include conf.d/options-ssl-nginx.conf;

    location / {
        # 代理到后端的 HTTP 服务
        proxy_pass http://127.0.0.1:8080;

        # 传递必要的客户端信息
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```



##### **2. 动态加载证书（`data:` 前缀）**



从 Nginx 1.25.1 版本开始，支持使用 `data:` 前缀从变量中动态加载证书和密钥，这对于自动化和密钥管理系统（如 Vault）集成非常有用。

Nginx

```
# 需在主配置中预先设置变量
# http or stream block
# map $ssl_server_name $certificate_data {
#     host.example.com "base64-encoded-cert";
# }
# map $ssl_server_name $key_data {
#     host.example.com "base64-encoded-key";
# }

server {
    ...
    ssl_certificate data:$certificate_data;
    ssl_certificate_key data:$key_data;
    ...
}
```



##### **3. 性能优化：复用 SSL/TLS 会话**



TLS 握手开销很大。通过复用会话，可以跳过完整的握手过程，大幅提升重复连接的性能。这通常在 `options-ssl-nginx.conf` 文件中统一配置。

- **`ssl_session_cache`**: 在服务器端缓存会话信息。
  - `shared:SSL:20m`: 创建一个名为 `SSL` 的共享内存区，大小为 20MB。1MB 大约能存储 4000 个会话，20MB 可缓存约 80,000 个会话。这是推荐的配置方式。
- **`ssl_session_timeout`**: 设置会话在缓存中的有效时间。
  - `1h`: 会话信息在此缓存中保留 1 小时。
- **`ssl_session_tickets`**: 一种无状态的会话复用机制，服务器将加密的会话信息（Ticket）发给客户端，由客户端保存。
  - `off`: **建议关闭**。因为如果 Ticket 密钥泄露，攻击者可以复用会T会话。若要开启，必须配合 `ssl_session_ticket_key` 指令实现密钥的定期轮换，以保证安全性。

**`options-ssl-nginx.conf` 示例:**

Nginx

```
# 推荐的协议版本
ssl_protocols TLSv1.2 TLSv1.3;

# 优先使用服务器端定义的加密套件
ssl_prefer_server_ciphers on;

# 安全的加密套件列表 (示例，请使用 Mozilla SSL Configuration Generator 生成最新配置)
ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:...';

# 启用并配置会话缓存
ssl_session_cache shared:SSL:20m;
ssl_session_timeout 1h;

# 默认关闭 Session Ticket，除非有密钥轮换机制
ssl_session_tickets off;
```



##### **4. 这不是 mTLS**



上述配置是**单向认证**，即只有客户端验证服务器的身份。

**双向认证 (mTLS)** 要求客户端也必须提供证书来证明其身份。要实现 mTLS，需要在上述配置基础上增加：

Nginx

```
# 1. 指定用于验证客户端证书的 CA 证书
ssl_client_certificate /path/to/client_ca.crt;

# 2. 开启客户端证书验证
ssl_verify_client on;
```

------



#### **问二：当 Nginx作为正向代理时，如何处理TLS（HTTPS）流量？七层代理和四层代理有何区别？**



**答：** Nginx 作为正向代理处理 HTTPS 流量时，核心区别在于 Nginx 的工作层级。它不能像反向代理一样“卸载”SSL，因为加密通信发生在客户端与最终目标服务器之间。Nginx 只能选择“隧道”或“转发”这些加密流量。



##### **1. 七层代理 (L7): HTTP CONNECT 隧道**



这种方式工作在应用层，利用 HTTP 的 `CONNECT` 方法建立一个端到端的加密隧道。

- **原理**:

  1. 客户端向 Nginx 代理发送一个 `CONNECT target-server.com:443 HTTP/1.1` 请求。
  2. Nginx 收到后，与目标服务器 `target-server.com:443` 建立一个纯粹的 TCP 连接。
  3. 连接建立成功后，Nginx 向客户端返回 `HTTP/1.1 200 Connection established`。
  4. 此后，Nginx 放弃对报文的解析，仅作为数据管道，在客户端和目标服务器之间盲目地来回转发 TCP 数据包。整个 TLS 握手和加密通信完全在客户端和目标服务器之间进行，Nginx 无法解密流量。

- **适用场景**: 传统的浏览器 HTTP(S) 代理。

- **配置 (需第三方模块)**: Nginx 默认不支持 `CONNECT` 方法，需要使用如 `ngx_http_proxy_connect_module` 模块。

  Nginx

  ```
  # 需要编译第三方模块 ngx_http_proxy_connect_module
  location / {
      proxy_connect; # 启用 CONNECT 方法
      # 配置 DNS 解析器等...
      resolver 8.8.8.8;
      proxy_pass $host; # 代理到请求头中的 Host
  }
  ```



##### **2. 四层代理 (L4): `ngx_stream_core_module` TCP 转发**



这种方式工作在传输层，Nginx 仅处理 TCP 连接，不关心上层的应用协议是什么。

- **原理**: Nginx 在 `stream` 配置块中监听一个 TCP 端口。当有连接请求时，它直接将所有 TCP 流量原封不动地转发到指定的上游服务器。Nginx 对流量内容完全无知，无论是 HTTPS、MySQL 还是其他任何基于 TCP 的协议，都一视同仁。

- **适用场景**:

  - 对任意 TCP 协议进行负载均衡或转发。
  - 构建高性能、协议无关的透明代理。

- **配置 (Nginx 核心功能)**:

  Nginx

  ```
  # 在 nginx.conf 的顶层配置 stream 块
  stream {
      server {
          # 监听一个 TCP 端口
          listen 12345;
  
          # 将所有 TCP 流量转发到目标服务器的 443 端口
          proxy_pass target-server.com:443;
      }
  }
  ```



##### **总结对比**



| 特性            | 七层代理 (HTTP CONNECT)                  | 四层代理 (Stream)               |
| --------------- | ---------------------------------------- | ------------------------------- |
| **工作层级**    | L7 (应用层)                              | L4 (传输层)                     |
| **核心模块**    | `ngx_http_proxy_connect_module` (第三方) | `ngx_stream_core_module` (核心) |
| **是否解密TLS** | ❌ **否** (仅建立隧道)                    | ❌ **否** (仅转发TCP包)          |
| **协议感知**    | 感知 `CONNECT` 请求，之后变为隧道        | 完全不感知应用层协议            |
| **主要用途**    | 浏览器或应用的 HTTP/HTTPS 代理           | 任意 TCP 协议的负载均衡与转发   |