好的，下面我们来系统讲解一下 **Nginx 日志分析** 中常用的命令及 Linux 技巧，结合实际需求来统计不同维度的数据（PV、IP、页面、状态码、访问大小等）。日志文件默认格式是 Nginx 的 `access.log`，我们默认格式如下：

```
log_format main '$remote_addr - $remote_user [$time_local] "$request" '
                '$status $body_bytes_sent "$http_referer" '
                '"$http_user_agent"';
access_log  /var/log/nginx/access.log  main;

```

### 📌 示例日志内容

```
192.168.0.1 - - [26/Jul/2025:10:03:25 +0800] "GET /index.html HTTP/1.1" 200 1234 "-" "Mozilla/5.0"
```

------

## 🔹 1. 统计某天的 PV（页面访问量）

```bash
grep '26/Jul/2025' /var/log/nginx/access.log | wc -l
```

- `grep`：匹配某一天
- `wc -l`：统计总行数（即访问次数）

------

## 🔹 2. 统计各 IP 的访问次数（Top 10）

```bash
grep '26/Jul/2025' /var/log/nginx/access.log | awk '{ips[$1]++} END {for(i in ips){print i,ips[i]}}' | sort -k2 -rn | head -n10
```

- `$1` 是 IP 地址字段
- `awk`：将 IP 放入数组 `ips` 中计数
- `sort`：按访问量倒序排序
- `head -n10`：取前 10 条

------

## 🔹 3. 统计访问多次（如 5 次以上）的 IP

```bash
grep '26/Jul/2025' /var/log/nginx/access.log | awk '{ips[$1]++} END {for(ip in ips) if (ips[ip]>5) print ip, ips[ip]}' | sort -k2 -rn
```

------

## 🔹 4. 统计访问最多的页面（Top 10）

```bash
grep '26/Jul/2025' /var/log/nginx/access.log | awk '{urls[$7]++} END {for(u in urls){print urls[u], u}}' | sort -k1 -rn | head -n10
```

- `$7` 是请求 URL（例如 `/index.html`）

------

## 🔹 5. 统计访问内容大小（总传输字节数）

```bash
grep '26/Jul/2025' /var/log/nginx/access.log | awk '{sum += $10} END {print "Total Bytes:", sum, "≈", sum/1024/1024, "MB"}'
```

- `$10` 是响应大小（单位是字节）
- 输出结果中换算成 MB 方便查看

------

## 🔹 6. 统计各状态码的数量（如 200、404、500）

```bash
grep '26/Jul/2025' /var/log/nginx/access.log | awk '{codes[$9]++} END {for(code in codes){print code, codes[code]}}' | sort -k2 -rn
```

- `$9` 是 HTTP 状态码字段（如 `200`、`404`）
- 统计每个状态码出现的次数

------

## 🔹 Linux 命令技巧补充

- **实时查看日志输出**：

  ```bash
  tail -f /var/log/nginx/access.log
  ```

- **查看某 IP 所有访问记录**：

  ```bash
  grep '192.168.0.1' /var/log/nginx/access.log
  ```

- **查看某页面被访问的 IP 列表**：

  ```bash
  grep '/index.html' /var/log/nginx/access.log | awk '{print $1}' | sort | uniq
  ```

- **结合 `cut` 抽取字段**（有时候比 `awk` 快）：

  ```bash
  cut -d' ' -f1 /var/log/nginx/access.log | sort | uniq -c | sort -rn | head -n10
  ```

------

## ✅ 总结表

| 指标       | 命令简述          |
| ---------- | ----------------- |
| PV         | `grep + wc -l`    |
| IP 分布    | `awk ips[$1]++`   |
| 高频 IP    | `if ips[ip]>5`    |
| 高频页面   | `awk urls[$7]++`  |
| 总传输字节 | `sum += $10`      |
| 状态码统计 | `awk codes[$9]++` |