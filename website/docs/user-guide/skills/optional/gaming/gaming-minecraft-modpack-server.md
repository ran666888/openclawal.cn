---
title: "Minecraft Modpack Server — Host modded Minecraft servers (CurseForge, Modrinth)"
sidebar_label: "Minecraft Modpack Server"
description: "Host modded Minecraft servers (CurseForge, Modrinth)"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# 我的世界 Modpack 服务器

托管经过修改的 Minecraft 服务器（CurseForge、Modrinth）。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/gaming/minecraft-modpack-server` 安装 |
|路径| `可选技能/游戏/minecraft-modpack-服务器` |
|平台| linux, macOS |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# Minecraft Modpack 服务器设置

## 何时使用
- 用户想要从服务器包 zip 设置修改后的 Minecraft 服务器
- 用户需要 NeoForge/Forge 服务器配置方面的帮助
- 用户询问 Minecraft 服务器性能调整或备份

## 首先收集用户偏好
在开始设置之前，请询问用户：
- **服务器名称/MOTD** — 服务器列表中应该写什么？
- **种子** — 特定种子还是随机种子？
- **困难** — 平静/简单/正常/困难？
- **游戏模式** — 生存/创意/冒险？
- **在线模式** — true（Mojang 身份验证、合法帐户）还是 false（LAN/破解友好）？
- **玩家数量** - 预计有多少玩家？ （影响 RAM 和视距调整）
- **RAM 分配** — 或者让代理根据模组数量和可用 RAM 来决定？
- **查看距离/模拟距离** — 或者让代理根据玩家数量和硬件进行选择？
- **PvP** — 开启还是关闭？
- **白名单** — 开放服务器还是仅白名单？
- **备份** — 想要自动备份？多常？

如果用户不在乎，请使用合理的默认值，但在生成配置之前始终询问。

## 步骤

### 1.下载并检查包
````bash
mkdir -p ~/minecraft-server
cd ~/minecraft-服务器
wget -O serverpack.zip "<URL>"
解压缩 -o serverpack.zip -d 服务器
ls服务器/
````
查找：`startserver.sh`、安装程序 jar (neoforge/forge)、`user_jvm_args.txt`、`mods/` 文件夹。
检查脚本以确定：mod 加载器类型、版本和所需的 Java 版本。

### 2.安装Java
- Minecraft 1.21+ → Java 21：`sudo apt install openjdk-21-jre-headless`
- Minecraft 1.18-1.20 → Java 17：`sudo apt install openjdk-17-jre-headless`
- Minecraft 1.16 及以下 → Java 8：`sudo apt install openjdk-8-jre-headless`
- 验证：`java -版本`

### 3.安装模组加载器
大多数服务器包都包含安装脚本。使用 INSTALL_ONLY 环境变量进行安装而不启动：
````bash
cd ~/minecraft-server/服务器
ATM10_INSTALL_ONLY=true bash startserver.sh
# 或者对于通用 Forge 包：
# java -jar forge-*-installer.jar --installServer
````
这会下载库、修补服务器 jar 等。

### 4.接受最终用户许可协议
````bash
echo "eula=true" > ~/minecraft-server/server/eula.txt
````

### 5.配置server.properties
modded/LAN 的关键设置：
````属性
motd=\u00a7b\u00a7l服务器名称\u00a7r\u00a78| \u00a7a模组包名称
服务器端口=25565
online-mode=true # 对于没有 Mojang 身份验证的 LAN，为 false
force-secure-profile=true # 匹配在线模式
难度 = 困难 # 大多数模组包都围绕困难进行平衡
allow-flight=true # 改装所需（飞行坐骑/物品）
spawn-protection=0 # 让每个人在spawn时构建
max-tick-time=180000 # modded需要更长的tick超时
启用命令块=true
````

性能设置（根据硬件缩放）：
````属性
# 2 名玩家，强大的机器：
视距=16
模拟距离=10

# 4-6名玩家，中等机器：
视距=10
模拟距离=6

# 8+ 玩家或较弱的硬件：
视距=8
模拟距离=4
````

### 6. 调整 JVM 参数 (user_jvm_args.txt)
根据玩家数量和模组数量调整 RAM。修改的经验法则：
- 100-200 个模组：6-12GB
- 200-350+ 模组：12-24GB
- 为操作系统/其他任务保留至少 8GB 可用空间

````
-Xms12G
-Xmx24G
-XX:+使用G1GC
-XX:+ParallelRefProcEnabled
-XX:MaxGCPauseMillis=200
-XX:+解锁实验VM选项
-XX:+禁用显式GC
-XX:+AlwaysPreTouch
-XX:G1NewSizePercent=30
-XX:G1MaxNewSizePercent=40
-XX:G1HeapRegionSize=8M
-XX:G1保留百分比=20
-XX:G1HeapWastePercent=5
-XX:G1MixedGCCountTarget=4
-XX:InitiatingHeapOccupancyPercent=15
-XX:G1MixedGCLiveThresholdPercent=90
-XX:G1RSetUpdatingPauseTimePercent=5
-XX:幸存者比率=32
-XX:+Perf禁用SharedMem
-XX:最大TenuringThreshold=1
````

### 7. 打开防火墙
````bash
sudo ufw允许25565/tcp评论“我的世界服务器”
````
检查：`sudo ufw status | grep 25565`

### 8. 创建启动脚本
````bash
猫 > ~/start-minecraft.sh << 'EOF'
#!/bin/bash
cd ~/minecraft-server/服务器
java @user_jvm_args.txt @libraries/net/neoforged/neoforge/<版本>/unix_args.txt nogui
EOF
chmod +x ~/start-minecraft.sh
````
注意：对于 Forge（不是 NeoForge），args 文件路径不同。检查“startserver.sh”的确切路径。

### 9. 设置自动备份
创建备份脚本：
````bash
猫 > ~/minecraft-server/backup.sh << '脚本'
#!/bin/bash
SERVER_DIR="$HOME/minecraft-server/服务器"
BACKUP_DIR="$HOME/minecraft-server/backups"
WORLD_DIR="$SERVER_DIR/世界"
最大备份=24
mkdir -p“$BACKUP_DIR”
[！ -d "$WORLD_DIR" ] && echo "[BACKUP] 无世界文件夹" && exit 0
时间戳=$(日期+%Y-%m-%d_%H-%M-%S)
BACKUP_FILE="$BACKUP_DIR/world_${TIMESTAMP}.tar.gz"
echo "[备份] 从 $(日期) 开始"
tar -czf“$BACKUP_FILE”-C“$SERVER_DIR”世界
大小=$(du -h "$BACKUP_FILE" | cut -f1)
echo "[BACKUP] 已保存: $BACKUP_FILE ($SIZE)"
BACKUP_COUNT=$(ls -1t "$BACKUP_DIR"/world_*.tar.gz 2>/dev/null | wc -l)
如果[“$BACKUP_COUNT”-gt“$MAX_BACKUPS”];然后
    删除=$((BACKUP_COUNT - MAX_BACKUPS))
    ls -1t "$BACKUP_DIR"/world_*.tar.gz | ls -1t "$BACKUP_DIR"/world_*.tar.gz |尾-n“$REMOVE”| xargs rm -f
    echo "[BACKUP] 已修剪 $REMOVE 旧备份"
菲
echo "[备份] 于 $(日期) 完成"
脚本
chmod +x ~/minecraft-server/backup.sh
````

添加每小时 cron：
````bash
(crontab -l 2>/dev/null | grep -v "minecraft/backup.sh"; echo "0 * * * * $HOME/minecraft-server/backup.sh >> $HOME/minecraft-server/backups/backup.log 2>&1") | crontab -
````

## 陷阱
- 始终为模组设置“allow-flight=true”——带有喷气背包/飞行的模组否则会踢玩家
- `max-tick-time=180000` 或更高 — 修改后的服务器在世界生成期间通常会有很长的时间间隔
- 第一次启动很慢（大包需要几分钟）——不要惊慌
- “跟不上！”首次启动时的警告是正常的，在初始块生成后解决
- 如果 online-mode = false，也设置force-secure-profile = false，否则客户端会被拒绝
- 该包的 startserver.sh 通常有一个自动重启循环 - 制作一个没有它的干净启动脚本
- 删除世界/文件夹以使用新种子重新生成
- 某些包具有环境变量来控制行为（例如，ATM10 使用 ATM10_JAVA、ATM10_RESTART、ATM10_INSTALL_ONLY）

## 验证
- `pgrep -fa neoforge` 或 `pgrep -fa minecraft` 检查是否正在运行
- 检查日志：`tail -f ~/minecraft-server/server/logs/latest.log`
- 寻找“完成（X）！”在日志中 = 服务器已准备就绪
- 测试连接：玩家在多人游戏中添加服务器IP