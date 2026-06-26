# Gateway 运维 — 健康检查、远程访问与 Tailscale

OpenClaw Gateway 是 Agent 的核心网络组件，负责管理消息路由、节点连接和外部访问。本文档介绍 Gateway 的日常运维操作。

## Gateway 健康检查

### 检查 Gateway 状态

```bash
# 查看 Gateway 运行状态
openclaw gateway status

# 查看 Gateway 日志
openclaw gateway logs

# 查看连接数
openclaw gateway connections
```

### 健康检查端点

Gateway 提供 HTTP 健康检查接口：

```
GET http://localhost:8769/health
```

正常响应：

```json
{
  "status": "ok",
  "uptime": 3600,
  "connections": 5,
  "version": "0.17.0"
}
```

## 远程访问

### 配置远程访问

要让外部设备连接到你的 Gateway，需要：

1. **配置防火墙** — 开放 Gateway 端口（默认 8769）
2. **设置访问密钥** — 防止未授权访问
3. **配置 SSL/TLS** — 加密通信

```bash
# 设置访问密钥
openclaw config set gateway.secret_key <你的密钥>

# 启用远程访问
openclaw config set gateway.remote_access true

# 重启 Gateway 生效
openclaw gateway restart
```

### 安全建议

- **不要** 将 Gateway 直接暴露在公网
- 始终使用 VPN 或 Tailscale 进行远程连接
- 定期更换访问密钥
- 启用 IP 白名单

## Tailscale 集成

Tailscale 是基于 WireGuard 的零配置 VPN，适合安全地远程连接 OpenClaw 节点。

### 设置 Tailscale

```bash
# 在主节点安装 Tailscale
curl -fsSL https://tailscale.com/install.sh | sh
tailscale up

# 获取 Tailscale 分配的 IP
tailscale ip -4
```

### 通过 Tailscale 连接

配置 Gateway 仅监听 Tailscale 接口：

```bash
# 监听 Tailscale IP（而非 0.0.0.0）
openclaw config set gateway.bind_address <tailscale-ip>

# 重启 Gateway
openclaw gateway restart
```

### 多节点 Tailscale 网络

1. 在所有节点上安装并登录 Tailscale（同一账号）
2. 节点之间通过 Tailscale IP 直接通信
3. 无需开放防火墙端口

## 常见运维操作

```bash
# 重启 Gateway
openclaw gateway restart

# 查看配置
openclaw gateway config

# 测试连接
openclaw gateway ping

# 查看连接详情
openclaw gateway connections --verbose
```

## 故障排查

| 问题 | 可能原因 | 解决方法 |
|------|---------|---------|
| Gateway 无法启动 | 端口被占用 | 检查端口 `lsof -i :8769`，修改端口配置 |
| 远程连接失败 | 防火墙阻止 | 检查防火墙规则，开放对应端口 |
| 连接不稳定 | 网络延迟高 | 检查网络质量，考虑使用 Tailscale |
| 身份验证失败 | 密钥不匹配 | 重新配置 `gateway.secret_key` |

## 相关资源

- [节点配对指南](/openclaw/nodes)
- [Web 控制 UI 说明](/openclaw/web-ui)
- [Tailscale 官方文档](https://tailscale.com/docs)
