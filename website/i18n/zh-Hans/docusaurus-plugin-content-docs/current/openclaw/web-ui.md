# Web 控制 UI — Dashboard 使用说明

OpenClaw Web 控制 UI（Dashboard）是一个基于浏览器的管理界面，让你通过图形化方式管理 Agent、查看状态和执行操作。

## 访问 Dashboard

启动 Gateway 后，在浏览器中访问：

```
http://localhost:8769
```

默认端口为 8769。如果你修改了端口配置，请使用对应的端口号访问。

## Dashboard 功能

### 概览面板

Dashboard 的首页显示以下信息：

- **运行状态** — Gateway 是否正常运行
- **连接数** — 当前活跃的连接数量
- **节点状态** — 已配对的节点列表及状态
- **最近活动** — Agent 最近的操��记录
- **资源使用** — CPU、内存占用情况

### 会话管理

在「会话」页面，你可以：

- 查看所有活跃会话
- 查看历史会话记录
- 查看每个会话的对话内容
- 结束异常会话

### 节点管理

在「节点」页面，你可以：

- 查看已配对的设备节点
- 添加/移除节点
- 查看节点在线状态
- 查看节点版本信息

### 配置管理

在「配置」页面，你可以：

- 查看当前配置
- 修改关键配置项
- 重新加载配置
- 导出配置备份

### 日志查看

在「日志」页面，你可以：

- 实时查看 Agent 日志
- 按级别筛选（INFO/WARN/ERROR）
- 搜索关键词
- 下载日志文件

## 安全设置

### 访问密码

建议为 Dashboard 设置访问密码：

```bash
# 设置访问密码
openclaw config set gateway.ui_password <你的密码>

# 重启 Gateway 生效
openclaw gateway restart
```

### HTTPS 配置

如果需要通过公网访问 Dashboard，建议启用 HTTPS：

```bash
# 配置 SSL 证书
openclaw config set gateway.ssl_cert /path/to/cert.pem
openclaw config set gateway.ssl_key /path/to/key.pem

# 重启 Gateway
openclaw gateway restart
```

## 自定义 Dashboard

Dashboard 支持通过插件扩展：

- **添加自定义面板** — 显示你关心的数据
- **集成第三方服务** — 在 Dashboard 内嵌外部页面
- **自定义主题** — 修改颜色和布局

## 相关资源

- [Gateway 运维指南](/openclaw/gateway-ops)
- [扩展 Dashboard](https://docs.openclaw.ai/user-guide/features/extending-the-dashboard)
- [API Server 参考](https://docs.openclaw.ai/user-guide/features/api-server)
