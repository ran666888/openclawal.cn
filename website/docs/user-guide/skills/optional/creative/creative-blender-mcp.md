---
title: "Blender Mcp — Control Blender directly from OpenClaw via socket connection to the blender-mcp addon"
sidebar_label: "Blender Mcp"
description: "Control Blender directly from OpenClaw via socket connection to the blender-mcp addon"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 搅拌机MCP

通过与 Blender-mcp 插件的套接字连接，直接从 OpenClaw 控制 Blender。创建 3D 对象、材质、动画并运行任意 Blender Python (bpy) 代码。当用户想要在 Blender 中创建或修改任何内容时使用。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/creative/blender-mcp` 安装 |
|路径| `可选技能/创意/blender-mcp` |
|版本 | `1.0.0` |
|作者 |阿里雷扎78a |
|平台| linux、macos、windows |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# 搅拌机 MCP

通过 TCP 端口 9876 上的套接字从 OpenClaw 控制正在运行的 Blender 实例。

## 设置（一次性）

### 1.安装Blender插件

    curl -sL https://raw.githubusercontent.com/ahujasid/blender-mcp/main/addon.py -o ~/Desktop/blender_mcp_addon.py

在搅拌机中：
    编辑>首选项>附加组件>安装>选择blender_mcp_addon.py
    启用“接口：Blender MCP”

### 2. 在 Blender 中启动套接字服务器

在 Blender 视口中按 N 打开侧边栏。
找到“BlenderMCP”选项卡并单击“启动服务器”。

### 3. 验证连接

    nc -z -w2 本地主机 9876 && 回显“打开”||回显“已关闭”

## 协议

TCP 上的纯 UTF-8 JSON — 无长度前缀。

发送：{"type": "<command>", "params": {<kwargs>}}
接收：{“状态”：“成功”，“结果”：<值>}
          {“状态”：“错误”，“消息”：“<原因>”}

## 可用命令

|类型 |参数 |描述 |
|------------------------------------|--------------------------------|---------------------------------|
|执行代码|代码 (str) |运行任意 bpy Python 代码 |
|获取场景信息 | （无）|列出场景中的所有对象 |
|获取对象信息 |对象名称 (str) |特定对象的详细信息 |
|获取视口屏幕截图 | （无）|当前视口的屏幕截图|

## Python 助手

在execute_code工具调用中使用它：

    导入套接字，json

    def Blender_exec（代码：str，主机=“localhost”，端口= 9876，超时= 15）：
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((主机，端口))
        s.settimeout(超时)
        Payload = json.dumps({"type": "execute_code", "params": {"code": code}})
        s.sendall(payload.encode("utf-8"))
        缓冲区 = b""
        而真实：
            尝试：
                块 = s.recv(4096)
                如果不是块：
                    打破
                buf += 块
                尝试：
                    json.loads(buf.decode("utf-8"))
                    打破
                除了 json.JSONDecodeError：
                    继续
            除了套接字超时：
                打破
        s.close()
        返回 json.loads(buf.decode("utf-8"))

## 常见的 bpy 模式

### 清晰的场景
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

### 添加网格对象
    bpy.ops.mesh.primitive_uv_sphere_add(半径=1,位置=(0,0,0))
    bpy.ops.mesh.primitive_cube_add(大小=2, 位置=(3, 0, 0))
    bpy.ops.mesh.primitive_圆筒_add(半径=0.5，深度=2，位置=(-3,0,0))

### 创建并分配材质
    垫 = bpy.data.materials.new(name="MyMat")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("原则 BSDF")
    bsdf.inputs["基色"].default_value = (R,G,B,1.0)
    bsdf.inputs["粗糙度"].default_value = 0.3
    bsdf.inputs["金属"].default_value = 0.0
    obj.data.materials.append(mat)

### 关键帧动画
    对象位置 = (0, 0, 0)
    obj.keyframe_insert(data_path="位置",frame=1)
    对象位置 = (0, 0, 3)
    obj.keyframe_insert（data_path =“位置”，帧= 60）

### 渲染到文件
    bpy.context.scene.render.filepath =“/tmp/render.png”
    bpy.context.scene.render.engine = '周期'
    bpy.ops.render.render(write_still=True)

## 陷阱

- 运行前必须检查套接字是否打开（nc -z localhost 9876）
- 每个会话都必须在 Blender 内启动插件服务器（N 面板 > BlenderMCP > 连接）
- 将复杂的场景分解为多个较小的execute_code调用以避免超时
- 渲染输出路径必须是绝对路径（/tmp/...）而不是相对路径
- shade_smooth() 需要选择对象并处于对象模式