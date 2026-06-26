---
title: "OpenClaw S6 Container Supervision"
sidebar_label: "OpenClaw S6 Container Supervision"
description: "Modify, debug, or extend the s6-overlay supervision tree inside the OpenClaw Docker image — adding new services, debugging profile gateways, understandin..."
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# OpenClaw S6 容器管理

修改、调试或扩展 OpenClaw Docker 映像内的 s6-overlay 监督树 - 添加新服务、调试配置文件网关、了解架构 B 主程序模式。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/devops/hermes-s6-container-supervision` 安装 |
|路径| `可选技能/de​​vops/hermes-s6-container-supervision` |
|版本 | `1.0.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux |
|标签 | `docker`、`s6`、`supervision`、`gateway`、`profiles` |
|相关技能| [`hermes-agent`](/docs/user-guide/skills/bundled/autonomous-ai-agents/autonomous-ai-agents-openclaw)，`hermes-agent-dev` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# OpenClaw s6-overlay 容器监管

## 什么时候使用这个技能

当您从事以下工作时加载此技能：
- 在 OpenClaw Docker 映像中添加或删除静态服务（应在每个容器启动时进行监督，例如仪表板）
- 诊断为什么每个配置文件的网关无法启动、重新启动或在“docker restart”中幸存
- 了解为什么容器的 CMD 是 `/opt/hermes/docker/main-wrapper.sh` 以及前导破折号参数如何到达用户的程序
- 修改 `cont-init.d` 启动脚本（UID 重新映射、卷播种、配置文件协调）
- 更改每个配置文件网关的渲染运行脚本（第 4 阶段）

如果您只是运行 OpenClaw 并且想要使用 Docker，请参阅“website/docs/user-guide/docker.md”。

## 架构概览

<!-- ascii-guard-ignore -->
````
/init ← PID 1 (s6-overlay v3.2.3.0)
├── cont-init.d ← 一次性安装，以 root 身份运行
│ ├── 01-hermes-setup ← docker/stage2-hook.sh
│ │ ├── UID/GID 重映射
│ │ ├── chown /opt/data
│ │ ├── chown /opt/data/profiles (每次启动)
│ │ ├── 种子.env / config.yaml / SOUL.md
│ │ └── Skills_sync.py
│ └── 02-reconcile-profiles ← hermes_cli.container_boot
│ ├── chown /run/service (hermes-可写运行时寄存器)
│ └── 步行$HERMES_HOME/profiles/<name>/gateway_state.json
│ → 重新创建/run/service/gateway-<名称>/
│ → 仅自动启动那些prior_state ==“running”的
│
├── s6-rc.d（静态服务，在/etc/s6-overlay/s6-rc.d/中）
│ ├── main-hermes/run ← exec sleep Infinity (无操作槽)
│ └── 仪表板/运行 ← 如果 HERMES_DASHBOARD=1，则运行 `hermes 仪表板`
│
├── /run/service（s6-svscan 监视；tmpfs）
│ ├── gateway-coder/ ← 运行时注册的每个配置文件
│ │ ├── 类型（“longrun”）
│ │ ├── run ("#!/command/with-contenv sh ... exec s6-setuidgid hermes hermes -p 编码器网关运行")
│ │ ├── down (标记-存在表示“已注册但不自动启动”)
│ │ └── 日志/运行 (s6-log → $HERMES_HOME/logs/gateways/coder/current)
│ └── ...
│
└── CMD（“主程序”）← /opt/hermes/docker/main-wrapper.sh
    └── 路由用户参数：bare exec | Hermes 子命令 |赫尔墨斯（无参数）
        — 由 /init 执行，继承了 stdin/stdout/stderr（TTY 为 --tui）
````
<!-- ascii-guard-ignore-end -->

## 关键文件

|路径|角色 |
|---|---|
| `Dockerfile` | s6-overlay 安装 + cont-init.d 接线 + `ENTRYPOINT ["/init", "/opt/hermes/docker/main-wrapper.sh"]` |
| `docker/stage2-hook.sh` | “旧的入口点逻辑”——UID 重新映射、chown、种子、技能同步。作为 cont-init.d/01-hermes-setup 运行。 |
| `docker/cont-init.d/02-reconcile-profiles` |每次启动时调用“hermes_cli.container_boot”以从持久卷恢复配置文件网关插槽。 |
| `docker/main-wrapper.sh` |容器的 CMD。路由用户参数，通过`s6-setuidgid`下降到hermes，exec选择的程序。 |
| `docker/s6-rc.d/main-hermes/run` |无操作 `sleep infinity` — 插槽存在，因此 s6-rc 用户包有效； main OpenClaw 作为 CMD 运行，而不是作为受监督的服务运行。 |
| `docker/s6-rc.d/dashboard/run` |有条件的服务——除非“HERMES_DASHBOARD”为真，否则“exec sleep infinity”。 |
| `docker/entrypoint.sh` |向后兼容垫片“exec”是 stage2 挂钩。对旧入口点路径进行硬编码的外部脚本仍然有效。 |
| `hermes_cli/service_manager.py` | `S6ServiceManager`：`register_profile_gateway`、`unregister_profile_gateway`、`启动/停止/重新启动/正在运行`、`list_profile_gateways`。 |
| `hermes_cli/container_boot.py` | `reconcile_profile_gateways()` — 遍历持久配置文件，重新生成 s6 插槽，发出 `container-boot.log`。 |
| `hermes_cli/gateway.py::_dispatch_via_service_manager_if_s6` |在容器中运行时拦截 `hermes gateway start/stop/restart` 并路由到 s6。 |

## 为什么采用架构 B（CMD 作为主程序，而不是 s6 监督的）

最初的计划（v1-v3）要求主 OpenClaw 作为受监督的 s6-rc 服务运行。两个真正的 s6-overlay v3 机制阻止了这一点：

1. **cont-init.d 脚本不接收 CMD 参数** — 因此 stage2 挂钩无法解析 `docker run <image> chat -q "hi"` 来设置要使用的服务 `run` 脚本的 `HERMES_ARGS`。
2. **`/run/s6/basedir/bin/halt` 不会传播写入到 `/run/s6-linux-init-container-results/exitcode` 的退出代码**。不管怎样，容器总是退出 143 (SIGTERM)。 skarnet（s6 作者）在 [issue #477](https://github.com/just-containers/s6-overlay/issues/477) 中确认：_“如果您想要关闭容器，则需要让 CMD 退出，或者，如果您没有 CMD，请编写您想要的容器退出代码，然后调用暂停”_。

因此我们使用 s6-overlay-native CMD 模式：`ENTRYPOINT ["/init", "/opt/hermes/docker/main-wrapper.sh"]`。 /init 自动将包装器添加到用户参数中 — 因此 `docker run <image> --version` 变为 `/init main-wrapper.sh --version`，并且 `--version` 不会被 /init 的 POSIX shell 拦截。包装器通过“s6-setuidgid”落入 OpenClaw，然后执行所选程序。程序的退出代码成为容器退出代码，与 s6 之前的 tini 合约完全匹配。

权衡：主要的 OpenClaw 在 s6 下是无监督的。这与它在 tini（s6 之前的映像）下的行为完全匹配。仪表板监督是唯一的**新**保证 - “/run/service/”下的每个配置文件网关得到全面的监督。

## 快速食谱

### 验证正在运行的容器中 s6 的 PID 为 1

````嘘
docker exec <c> sh -c 'cat /proc/1/comm;读取链接/proc/1/exe'
# 期望：s6-svscan 或 init / /package/admin/s6/.../s6-svscan
````

### 检查配置文件网关服务

````嘘
# /command/ 不在 docker-exec 路径上 — 使用绝对路径
docker exec <c> /command/s6-svstat /run/service/gateway-<名称>
#“up (pid …) …秒”→运行
# “down (exitcode N) … 秒，通常是 up，想要 up，…”→ s6 希望它 up，但进程不断退出（崩溃循环）
#“向下……正常向上，准备好……”→用户停止了它
````

### 手动启动/关闭服务

````嘘
docker exec <c> /command/s6-svc -u /run/service/gateway-<名称> # up
docker exec <c> /command/s6-svc -d /run/service/gateway-<名称> # down
docker exec <c> /command/s6-svc -t /run/service/gateway-<name> # SIGTERM（重新启动）
````

### 观看 cont-init 协调器日志

````嘘
docker exec <c> tail -n 50 /opt/data/logs/container-boot.log
# 2026-05-21T06:18:05+0000 profile=编码器prior_state=运行操作=开始
# 2026-05-21T06:18:05+0000 profile=writerprior_state=stoppedaction=registered
````

### 添加新的静态服务

1. 使用“longrun\n”和“docker/s6-rc.d/<name>/run”创建“docker/s6-rc.d/<name>/type”（使用“#!/command/with-contenv sh”+“# shellcheck shell=sh”）。
2. 通过运行顶部的 `s6-setuidgid hermes` 进入 OpenClaw（除非您特别需要 root）。
3. 创建空的 `docker/s6-rc.d/<name>/dependency.d/base` 以便它等待基本包。
4. 创建空的 `docker/s6-rc.d/user/contents.d/<name>` 以便它加入用户包。
5. Dockerfile 中的“COPY docker/s6-rc.d/”会自动选择它 - 没有其他更改。

### 更改每个配置文件网关运行命令

在“hermes_cli/service_manager.py”中编辑“S6ServiceManager._render_run_script”。在启动协调期间，该函数也会被 `hermes_cli/container_boot.py::_register_service` 调用，因此它是唯一的事实来源。更新 `tests/hermes_cli/test_service_manager.py::test_s6_register_creates_service_dir_and_triggers_scan` 中相应的断言。

### 运行 docker 测试工具

````嘘
docker build -t hermes-agent-harness:latest 。
HERMES_TEST_IMAGE=hermes-agent-harness:最新脚本/run_tests.sh 测试/docker/ -v
# 对于 s6 镜像，预计 19 个通过，0 个失败
````

该工具位于“tests/docker/”中，当 Docker 不可用时会跳过。每次测试超时时间增加到 180 秒（请参阅“tests/docker/conftest.py”）。

## 常见陷阱

### 通过`docker exec`“找不到命令”

“/command/”（s6-overlay 放置其二进制文件的位置）仅适用于由监督树（services、cont-init.d、main-wrapper.sh）生成的进程。 `docker exec <c> s6-svstat …` 将失败并显示“command not find”；始终使用绝对路径“/command/s6-svstat”。 `hermes` 二进制文件之所以有效，是因为 Dockerfile 将 `/opt/hermes/.venv/bin` 添加到运行时 `ENV PATH`。

### 配置文件目录所有权

cont-init 协调器作为 OpenClaw 运行（“02-reconcile-profiles”中的“s6-setuidgid hermes”）。如果配置文件目录最终由 root 拥有（例如，因为“docker exec <c> hermes profile create …”默认以 root 身份运行），则协调器无法读取 SOUL.md 并因“PermissionError”而失败。缓解措施：`stage2-hook.sh` 在**每次**启动时将 `$HERMES_HOME/profiles` chowns 为 OpenClaw，幂等。不要删除该块。

### `docker exec` 写入的文件是 root 拥有的

`docker exec` 默认为 root。要么通过 `--user hermes` 要么依赖 stage2 chown swing 下次重新启动。不要以 root 身份手动在 `$HERMES_HOME/profiles/<name>/` 下写入文件 - 下一个协调过程将清除它们，但正在进行的操作可能会遇到 Perm 错误。

### 服务槽存在，但 s6-svstat 提示“s6-supervise 未运行”

服务目录位于 tmpfs 上，并在容器重新启动时被擦除。 cont-init 协调器尚未运行（在“docker restart”后稍等片刻）或失败。检查 `docker 日志 <c> | grep '02-协调'`。

### 网关启动然后立即退出（svstat 中的“down (exitcode 1)”）

该配置文件很可能没有配置模型或身份验证。服务槽正确 - 网关本身未配置。首先运行 `hermes -p <profile> setup`。 s6 Supervisor会不断重启它；这是所需的行为（当您修复配置时，下一次尝试会成功并保持不变）。

### Reconciler 跳过了配置文件

协调器将“SOUL.md”的**存在作为“真实配置文件”标记。 `hermes profile create` 总是播种它。如果配置文件目录缺少 SOUL.md（杂散目录、部分恢复、正在进行的备份），协调器会故意跳过它。添加“SOUL.md”（甚至为空）以选择重新加入。

### “救命，容器退出 143！”

检查是否有东西正在调用 `s6-svscanctl -t` 或 `/run/s6/basedir/bin/halt` — 两者都会导致 /init 开始第 3 阶段关闭，但返回 143 (SIGTERM)，而不是所需的退出代码。这是从 A 到 B 的第二阶段架构枢轴。对于具有真正退出代码的容器关闭，您必须让 CMD (main-wrapper.sh) 正常退出； **不要**尝试控制完成脚本的退出。

## 相关技能

- `hermes-agent-dev`：通用 OpenClaw-agent 代码库导航
- `hermes-tool-quirks`：特定的 OpenClaw 工具解决方法（sed/grep/等）- 在调试 s6 堆栈与 OpenClaw 内置工具的交互时加载。