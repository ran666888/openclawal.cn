---
title: Home Assistant
description: Control your smart home with OpenClaw via Home Assistant integration.
sidebar_label: Home Assistant
sidebar_position: 5
---
# 家庭助理集成

OpenClaw 通过两种方式与 [Home Assistant](https://www.home-assistant.io/) 集成：

1. **网关平台**——通过WebSocket订阅实时状态变化并响应事件
2. **智能家居工具** — 四个 LLM 可调用工具，用于通过 REST API 查询和控制设备

## 设置

### 1. 创建长期访问令牌

1. 打开您的 Home Assistant 实例
2. 转到您的**个人资料**（在侧边栏中单击您的姓名）
3. 滚动到**长期访问令牌**
4. 单击**创建令牌**，为其命名，例如“OpenClaw”
5.复制令牌

### 2.配置环境变量

````bash
# 添加到~/.hermes/.env

# 必需：您的长期访问令牌
HASS_TOKEN=您的长期访问令牌

# 可选：HA URL（默认：http://homeassistant.local:8123）
HASS_URL=http://192.168.1.100:8123
````

:::信息
设置“HASS_TOKEN”时，会自动启用“homeassistant”工具集。网关平台和设备控制工具都通过这个单一令牌激活。
:::

### 3.启动网关

````bash
爱马仕网关
````

Home Assistant 将作为一个连接平台与任何其他消息平台（Telegram、Discord 等）一起出现。

## 可用工具

Hermes Agent注册了四种智能家居控制工具：

### `ha_list_entities`

列出家庭助理实体，可以选择按域或区域过滤。

**参数：**
- `domain` *（可选）* — 按实体域过滤：`light`、`switch`、`climate`、`sensor`、`binary_sensor`、`cover`、`fan`、`media_player` 等。
- `area` *（可选）* — 按区域/房间名称过滤（与友好名称匹配）：`living room`、`kitchen`、`bedroom` 等。

**示例：**
````
列出客厅所有灯
````

返回实体 ID、状态和友好名称。

### `ha_get_state`

获取单个实体的详细状态，包括所有属性（亮度、颜色、温度设定值、传感器读数等）。

**参数：**
- `entity_id` *（必填）* — 要查询的实体，例如，`light.living_room`、`climate.thermostat`、`sensor.Temperature`

**示例：**
````
Climate.thermostat 的当前状态如何？
````

返回：状态、所有属性、上次更改/更新时间戳。

### `ha_list_services`

列出设备控制的可用服务（操作）。显示可以对每种设备类型执行哪些操作以及它们接受哪些参数。

**参数：**
- `domain` *（可选）* — 按域过滤，例如，`light`、`climate`、`switch`

**示例：**
````
气候设备可以提供哪些服务？
````

### `ha_call_service`

调用 Home Assistant 服务来控制设备。

**参数：**
- `domain` *（必填）* — 服务域：`light`、`switch`、`climate`、`cover`、`media_player`、`fan`、`scene`、`script`
- `service` *（必填）* — 服务名称：`turn_on`、`turn_off`、`toggle`、`set_Temperature`、`set_hvac_mode`、`open_cover`、`close_cover`、`set_volume_level`
- `entity_id` *（可选）* — 目标实体，例如，`light.living_room`
- `data` *(可选)* — JSON 对象形式的附加参数

**示例：**

````
打开客厅的灯
→ ha_call_service(domain="light", service="turn_on",entity_id="light.living_room")
````

````
在制热模式下将恒温器设置为 22 度
→ ha_call_service(域=“气候”，服务=“设置温度”，
    entity_id="climate.thermostat", data={"温度": 22, "hvac_mode": "热"})
````

````
将客厅灯设置为蓝色，亮度为 50%
→ ha_call_service(域=“light”，服务=“turn_on”，
    entity_id="light.living_room", data={"亮度": 128, "color_name": "蓝色"})
````

## 网关平台：实时事件

Home Assistant 网关适配器通过 WebSocket 连接并订阅“state_changed”事件。当设备状态发生更改并与您的过滤器匹配时，它会作为消息转发给代理。

### 事件过滤

:::警告 所需配置
默认情况下，**不转发任何事件**。您必须至少配置“watch_domains”、“watch_entities”或“watch_all”之一才能接收事件。如果没有过滤器，则会在启动时记录警告，并且所有状态更改都会被静默删除。
:::

配置代理在 Home Assistant 平台的“extra”部分下的“~/.hermes/config.yaml”中看到哪些事件：

````yaml
平台：
  家庭助理：
    启用：真
    额外：
      监视域：
        - 气候
        - 二进制传感器
        - 警报控制面板
        - 光
      监视实体：
        - 传感器.front_door_battery
      忽略实体：
        - 传感器正常运行时间
        - 传感器.cpu_usage
        - 传感器.内存使用情况
      冷却秒数：30
````

|设置|默认 |描述 |
|---------|---------|-------------|
| `watch_domains` | *（无）* |仅观察这些实体域（例如“climate”、“light”、“binary_sensor”）|
| `watch_entities` | *（无）* |只关注这些特定的实体ID |
| `全部观看` | `假` |设置为“true”以接收**所有**状态更改（不建议大多数设置）|
| `忽略实体` | *（无）* |始终忽略这些实体（在域/实体过滤器之前应用）|
| `冷却秒数` | `30` |同一实体的事件之间的最小秒数 |

:::提示
从一组重点领域开始——“climate”、“binary_sensor”和“alarm_control_panel”涵盖了最有用的自动化。根据需要添加更多。使用“ignore_entities”来抑制 CPU 温度或正常运行时间计数器等噪音传感器。
:::

### 事件格式

状态更改根据域格式化为人类可读的消息：

|域名 |格式|
|--------|--------|
| `气候` | “HVAC 模式从‘关闭’更改为‘加热’（当前：21，目标：23）” |
| `传感器` | “从 21°C 更改为 22°C”|
| `二进制传感器` | “触发”/“清除”|
| `灯`、`开关`、`风扇` | “打开”/“关闭”|
| `警报控制面板` | “警报状态从‘armed_away’更改为‘已触发’” |
| *（其他）* | “从‘旧’变为‘新’”|

### 代理回应

来自代理的出站消息以 **Home Assistant 持久通知** 的形式传递（通过 `persistent_notification.create`）。它们出现在 HA 通知面板中，标题为“OpenClaw”。

### 连接管理

- **WebSocket** 具有 30 秒心跳实时事件
- **自动重连**带退避：5s → 10s → 30s → 60s
- **REST API** 用于出站通知（单独的会话以避免 WebSocket 冲突）
- **授权** — HA 事件始终获得授权（不需要用户白名单，因为“HASS_TOKEN”对连接进行身份验证）

## 安全

Home Assistant 工具强制执行安全限制：

:::警告被阻止的域
**阻止**以下服务域，以防止在 HA 主机上执行任意代码：

- `shell_command` — 任意 shell 命令
- `command_line` — 执行命令的传感器/开关
- `python_script` — 脚本化的 Python 执行
- `pyscript` — 更广泛的脚本集成
- `hassio` — 插件控制，主机关闭/重启
- `rest_command` — 来自 HA 服务器的 HTTP 请求（SSRF 向量）

尝试调用这些域中的服务会返回错误。
:::

实体 ID 根据模式“^[a-z_][a-z0-9_]*\.[a-z0-9_]+$”进行验证，以防止注入攻击。

## 自动化示例

### 早上例行公事

````
用户：开始我的早晨例行公事

代理：
1. ha_call_service(域=“light”，服务=“turn_on”，
     entity_id="light.bedroom", data={"亮度": 128})
2. ha_call_service(域=“气候”，服务=“设置温度”，
     entity_id="climate.thermostat", data={"温度": 22})
3. ha_call_service(域=“media_player”，服务=“turn_on”，
     entity_id =“media_player.kitchen_speaker”）
````

### 安全检查

````
网友：房子安全吗？

代理：
1. ha_list_entities(域=“binary_sensor”)
     → 检查门/窗传感器
2. ha_get_state(entity_id="alarm_control_panel.home")
     → 检查报警状态
3. ha_list_entities(域=“锁”)
     → 检查锁定状态
4. 报告：“所有门均已关闭，警报已解除，所有锁已锁上。”
````

### 反应式自动化（通过网关事件）

当作为网关平台连接时，代理可以对事件做出反应：

````
[家庭助理]前门：触发（已清除）

自动代理：
1. ha_get_state(entity_id="binary_sensor.front_door")
2. ha_call_service(域=“light”, 服务=“turn_on”,
     entity_id="light.hallway")
3. 发送通知：“前门打开。走廊灯打开。”
````

## 故障排除

**未拾取环境变量。**
适配器从 `~/.hermes/.env` 读取凭据（启动时自动合并）或
来自“config.yaml”。仔细检查该文件是否位于活动的 OpenClaw 配置文件下
home 并且 URL/令牌周围没有杂乱的引用。重新启动网关
编辑后 - 环境更改仅在进程启动时应用。


**REST 身份验证失败（“401 未经授权”）。**
该令牌必须是根据您的 HA 用户配置文件创建的*长期访问令牌*
页面（**配置文件 → 安全性 → 长期访问令牌**）。短暂的用户界面
会话令牌将不起作用。还要验证基本 URL 是否包含方案和
端口（例如“http://homeassistant.local:8123”）并且可以从主机访问
运行 OpenClaw — `curl -H "Authorization: Bearer <token>" <url>/api/` 应该
返回 `{"message": "API 正在运行。"}`。