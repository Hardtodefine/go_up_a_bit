1. **Nginx 缓存机制与浏览器缓存的区别**
2. **`split_clients` 的用法和意义**
3. **如何通过 `$http_user_agent` 区分 PC 和手机终端**
4. **缓存配置项与缓存管理模块的作用**

------

### 一、Nginx 缓存 vs 浏览器缓存

| 特性             | 浏览器缓存                                           | Nginx 缓存（反向代理缓存）  |
| ---------------- | ---------------------------------------------------- | --------------------------- |
| 存储位置         | 用户浏览器端                                         | Nginx 服务器（磁盘/内存）   |
| 控制方           | 服务端通过 HTTP 头控制（如 `Cache-Control`、`ETag`） | Nginx 管理缓存策略          |
| 缓存命中由谁判断 | 浏览器判断是否命中                                   | Nginx 根据 key 判断是否命中 |
| 应用场景         | 提升客户端体验，减少网络请求                         | 减轻后端压力，提高响应速度  |

------

### 二、`split_clients` 指令解释

```nginx
split_clients $request_uri $cache {
    50% "cache_hdd1";
    *   "cache_hdd2";
}
```

- `split_clients` 用于**对请求流量进行分流**，常用于 A/B 测试、缓存分区策略等场景。
- 语法：`split_clients <source_variable> <target_variable> { <percent> <value>; }`
- 上例中根据 `$request_uri` 的 hash 结果，将请求分为两类，其中：
  - 50% 的请求被分配到 `cache_hdd1`
  - 剩下的分配到 `cache_hdd2`

⚠️注意：它是**哈希一致性分流**，不是随机。

------

### 三、`proxy_cache_key` + `$http_user_agent` 区分终端类型

```nginx
proxy_cache_key "$scheme$proxy_host$request_uri$http_user_agent";
```

加入 `$http_user_agent` 的目的是**让手机和 PC 的请求分别缓存**，避免混淆内容。比如：

- 手机访问 `/index.html` 得到的是适配手机的 HTML
- PC 访问 `/index.html` 得到的是桌面版本

⚠️ 如果不区分 `$http_user_agent`，可能导致缓存混乱——PC 用户看到手机版页面，反之亦然。

------

### 四、缓存使用优化配置说明

| 指令                                                  | 作用                                                         |
| ----------------------------------------------------- | ------------------------------------------------------------ |
| `proxy_cache_path`                                    | 设置缓存路径和缓存区名（如 `cache`），`levels` 表示目录层级，`keys_zone` 为共享内存命名及大小 |
| `proxy_cache_key`                                     | 定义缓存键（命中与否由它决定）                               |
| `proxy_cache_valid`                                   | 针对不同状态码设置缓存时长（例如 `302` 说明可以缓存临时重定向） |
| `proxy_cache_min_uses`                                | 指定多少次访问后才缓存（避免缓存冷门请求）                   |
| `proxy_cache_methods`                                 | 只缓存 GET、HEAD 请求                                        |
| `proxy_no_cache`                                      | 设置哪些请求不缓存（如带 `Authorization` 的请求）            |
| `proxy_cache_use_stale`                               | 指定在后端出错时是否使用旧缓存内容                           |
| `cache_loader_processes` 和 `cache_manager_processes` | Nginx 在启动时加载缓存索引，用于清理过期缓存文件，节省磁盘空间 |

------

### 五、缓存清除模块：`ngx_cache_purge`

默认情况下 Nginx 不支持主动清除缓存，`ngx_cache_purge` 模块提供了这能力。配置后，可以通过特定 URL 触发清除缓存，例如：

```nginx
location ~ /purge(/.*) {
    allow 127.0.0.1;
    deny all;
    proxy_cache_purge cache $scheme$proxy_host$1;
}
```

访问 `/purge/index.html` 会清除该缓存。

------

### ✅ 总结建议

你提到的这一整套内容已经是**高级 Nginx 缓存配置**的核心了。建议你在测试环境中尝试以下几个实验：

- 加入不同的 `User-Agent` 模拟终端设备缓存差异
- 使用 `split_clients` 做缓存分流
- 启用 `ngx_cache_purge` 手动清除缓存
- 配置 `proxy_cache_min_uses`，分析冷热请求缓存行为