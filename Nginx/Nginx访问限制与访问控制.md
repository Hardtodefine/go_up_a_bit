### Nginx访问限制与访问控制

Nginx 提供了一系列模块，用于限制客户端访问频率、防止滥用、实现访问权限控制，保障服务器的稳定运行和资源安全。主要包括以下几个方面：

------

#### 一、请求频率限制（`limit_req_zone` + `limit_req`）

用于限制客户端的请求速率，防止接口被频繁请求（如接口刷流量、CC攻击等）：

```nginx
# 定义请求频率限制的共享内存区域
limit_req_zone $binary_remote_addr zone=req_zone:10m rate=1r/s;
```

- `$binary_remote_addr`：以二进制形式保存客户端 IP 地址，节省内存；
- `zone=req_zone:10m`：定义一个名为 `req_zone` 的内存区域，占用 10MB；
- `rate=1r/s`：每个客户端 IP 限制请求速率为 1 次/秒。

在 server 或 location 中启用该限制：

```nginx
limit_req zone=req_zone burst=5 nodelay;
```

- `burst=5`：允许最多突发 5 个请求；
- `nodelay`：超出速率的突发请求立即执行（不延迟），去掉则启用排队延迟。

------

#### 二、连接频率限制（`limit_conn_zone` + `limit_conn`）

用于限制同时连接数，适合限制文件下载等连接持续时间长的请求：

```nginx
limit_conn_zone $binary_remote_addr zone=addr_zone:10m;

# 限制每个客户端最多并发连接1个
limit_conn addr_zone 1;
```

此限制基于连接数而非请求数，适合应用于下载或长连接接口。

------

#### 三、基于主机的访问控制（`ngx_http_access_module`）

用于根据客户端 IP 地址允许或拒绝访问：

```nginx
# 拒绝某个 IP，允许所有其他访问
deny 192.168.1.100;
allow all;
```

这种方式适用于少量 IP 控制场景。

------

#### 四、大量ACL时使用 `ngx_http_geo_module`

当需要根据大量 IP 或 IP 段进行分级控制（如黑白名单）时，`geo` 模块更高效：

```nginx
geo $limited {
    default         0;
    192.168.1.0/24  1;
    10.0.0.0/8      1;
}

map $limited $limit_burst {
    1               0;  # 被限制的IP禁止突发请求
    0               10; # 正常IP可突发10个请求
}
```

结合频率控制模块可以实现更精细化的策略。

------

#### 五、基于用户的访问控制（`ngx_http_auth_basic_module`）

提供基本的 HTTP 认证功能：

```nginx
auth_basic "Restricted Area";
auth_basic_user_file /etc/nginx/.htpasswd;
```

- `.htpasswd` 文件使用 `htpasswd` 工具生成，支持用户名密码验证；
- 适合后台管理、开发接口等敏感路径加保护。

------

### 总结

Nginx 的访问限制与控制模块可以从 **IP层面**、**连接数**、**请求速率** 到 **用户认证** 实现全方位的访问控制。组合使用可以应对多种安全与性能挑战：

| 控制类型           | 模块/指令         | 作用场景                   |
| ------------------ | ----------------- | -------------------------- |
| 请求频率限制       | `limit_req_zone`  | 限制接口调用频率           |
| 请求延迟控制       | `burst/nodelay`   | 控制请求突发速度           |
| 连接数限制         | `limit_conn_zone` | 限制并发连接，防止慢速下载 |
| 基于IP的访问控制   | `access`, `geo`   | 黑白名单管理               |
| 基于用户的访问控制 | `auth_basic`      | 后台、管理页面认证         |