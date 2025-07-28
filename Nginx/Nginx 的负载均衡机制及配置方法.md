#### 一、Nginx 实现四层与七层负载均衡的区别

| 层级                       | 描述                                                        | Nginx模块              |
| -------------------------- | ----------------------------------------------------------- | ---------------------- |
| **四层负载均衡（传输层）** | 基于 TCP/UDP 协议，实现 IP 与端口的转发，无需解析 HTTP 内容 | 通过 `stream` 模块实现 |
| **七层负载均衡（应用层）** | 基于 HTTP 协议内容进行调度（如 URL、Header），更灵活可控    | 通过 `http` 模块实现   |



------

#### 二、七层负载均衡配置：`upstream` 模块示例

```nginx
http {
    upstream backend {
        server 192.168.1.101 weight=3 max_fails=2 fail_timeout=30s;
        server 192.168.1.102 down;
        server 192.168.1.103 backup;
    }

    server {
        listen 80;
        location / {
            proxy_pass http://backend;
        }
    }
}
```

##### `upstream`块中的常见配置参数：

- `weight`：权重，默认为1，数值越大分配请求越多；
- `max_fails`：允许请求失败的次数；
- `fail_timeout`：失败后暂停的时间；
- `down`：临时摘除该节点；
- `backup`：备用节点，主节点全部失效才启用。

------

#### 三、常见负载均衡算法

| 算法                         | 说明                                    |
| ---------------------------- | --------------------------------------- |
| **轮询（默认）**             | 请求轮流转发给后端服务器                |
| **加权轮询（weight）**       | 根据设置的权重进行轮询                  |
| **ip_hash**                  | 根据客户端 IP 进行 hash，保持会话一致性 |
| **fair（需第三方模块）**     | 根据后端响应时间自动分配（动态权重）    |
| **url_hash（需第三方模块）** | 根据 URL hash 值分配，提高缓存命中率    |



------

#### 四、其他较少使用的调度算法（一般需借助第三方模块）：

- `DH`：Destination Hashing，目标地址哈希
- `SH`：Source Hashing，源地址哈希
- `LC`：Least Connections，最少连接调度
- `WLC`：Weighted Least Connections，加权最少连接
- `LBLC`：Locality-Based Least Connection，本地最少连接
- `LBLCR`：Locality-Based Least Connection with Replication，带复制的本地连接策略

------

#### 五、测试负载均衡的方法

1. **关闭防火墙**：避免端口拦截；
2. **虚拟机桥接网络**：确保各服务器在同一网络内互通；
3. **同步时间**：防止日志、缓存、会话失效等问题；
4. **每台服务器配置不同 Web 页面**：方便识别请求落在哪台机器上；
5. **配置 `nginx.conf` 实现负载均衡逻辑**；
6. **多次刷新浏览器或使用 `curl` 观察轮询效果**；
7. **更换不同负载均衡算法进行效果比较测试**；