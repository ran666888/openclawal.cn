# 节点 — iOS / Android 配对

OpenClaw 支持将移动设备作为节点接入，让你的 Agent 能够利用手机端的能力（如通知、传感器、文件访问等）。

## 什么是节点？

节点是运行 OpenClaw Agent 的终端设备。除了主运行的桌面/服务器端，你还可以配对移动设备（iOS/Android）作为轻量节点，实现：

- **远程控制** — 通过手机发送指令给你的 Agent
- **通知推送** — Agent 完成任务后推送到手机
- **文件同步** — 在设备间同步 Agent 的工作成果
- **传感器接入** — 利用手机摄像头、麦克风等硬件能力

## 节点类型

| 类型 | 说明 | 适用场景 |
|------|------|---------|
| 主节点 | 运行完整 OpenClaw 的服务器/桌面端 | 核心工作站、自托管服务器 |
| 移动节点 | iOS/Android 设备 | 随身控制、通知、轻量交互 |
| 远程节点 | 通过 Tailscale 等工具连接的远程设备 | 多地点部署、远程办公 |

## 配对移动节点

### iOS 设备

1. 在 App Store 下载 OpenClaw Companion App
2. 打开应用，选择「配对节点」
3. 扫描主节点显示的二维码
4. 完成配对

### Android 设备

1. 在 Google Play 或通过 APK 安装 OpenClaw Companion
2. 打开应用，选择「配对节点」
3. 输入主节点的 IP 地址或扫描二维码
4. 完成配对

## 管理节点

在 OpenClaw 命令行中管理节点：

```bash
# 查看所有节点
openclaw node list

# 添加远程节点
openclaw node add <设备名称> --address <IP:端口>

# 移除节点
openclaw node remove <设备名称>

# 查看节点状态
openclaw node status <设备名称>
```

## 安全注意事项

- 节点通信默认使用端到端加密
- 建议在远程节点间使用 Tailscale 建立安全连接
- 定期检查已配对的设备列表，移除不再使用的节点

## 相关资源

- [Gateway 运维指南](/openclaw/gateway-ops)
- [Web 控制 UI 说明](/openclaw/web-ui)
- [Tailscale 集成文档](https://docs.openclaw.ai/guides/tailscale-setup)
