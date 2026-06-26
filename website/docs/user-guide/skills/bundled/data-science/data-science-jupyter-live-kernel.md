---
title: "Jupyter Live Kernel — Iterative Python via live Jupyter kernel (hamelnb)"
sidebar_label: "Jupyter Live Kernel"
description: "Iterative Python via live Jupyter kernel (hamelnb)"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# Jupyter Live 内核

通过实时 Jupyter 内核 (hamelnb) 进行迭代 Python。

## 技能元数据

| | |
|---|---|
|来源 |捆绑（默认安装）|
|路径| `技能/数据科学/jupyter-live-kernel` |
|版本 | `1.0.0` |
|作者 |爱马仕代理|
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `jupyter`、`notebook`、`repl`、`数据科学`、`探索`、`迭代` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# Jupyter Live 内核 (hamelnb)

通过实时 Jupyter 内核为您提供 **有状态的 Python REPL**。变量依然存在
跨处决。当您需要构建时，使用它而不是“execute_code”
增量状态、探索 API、检查 DataFrame 或迭代复杂代码。

## 何时使用此工具与其他工具

|工具|使用时间 |
|------|----------|
| **这个技能** |迭代探索、跨步骤状态、数据科学、ML、“让我尝试一下并检查”|
| `执行代码` |需要访问 OpenClaw 工具的一次性脚本（web_search、文件操作）。无国籍。 |
| `终端` | Shell 命令、构建、安装、git、进程管理 |

**经验法则：** 如果您需要 Jupyter 笔记本来完成该任务，请使用此技能。

## 先决条件

1. 必须安装**uv**（检查：`which uv`）
2. **JupyterLab**必须安装：`uv tool install jupyterlab`
3. Jupyter 服务器必须正在运行（请参阅下面的设置）

## 设置

hamelnb 脚本位置：
````
SCRIPT =“$HOME/.agent-skills/hamelnb/skills/jupyter-live-kernel/scripts/jupyter_live_kernel.py”
````

如果尚未克隆：
````
git 克隆 https://github.com/hamelsmu/hamelnb.git ~/.agent-skills/hamelnb
````

### 启动 JupyterLab

检查服务器是否已经在运行：
````
uv 运行“$SCRIPT”服务器
````

如果没有找到服务器，则启动一个：
````
jupyter-lab --no-browser --port=8888 --notebook-dir=$HOME/notebooks \
  --IdentityProvider.token='' --ServerApp.password='' > /tmp/jupyter.log 2>&1 &
睡觉 3
````

注意：本地代理访问禁用令牌/密码。服务器无头运行。

### 创建一个用于 REPL 的笔记本

如果您只需要 REPL（没有现有笔记本），请创建一个最小的笔记本文件：
````
mkdir -p ~/笔记本
````
使用一个空代码单元编写一个最小的 .ipynb JSON 文件，然后启动一个内核
通过 Jupyter REST API 进行会话：
````
卷曲-s -X POST http://127.0.0.1:8888/api/sessions \
  -H“内容类型：application/json”\
  -d '{“路径”：“scratch.ipynb”，“类型”：“笔记本”，“名称”：“scratch.ipynb”，“内核”：{“名称”：“python3”}}'
````

## 核心工作流程

所有命令都会返回结构化 JSON。始终使用“--compact”来保存令牌。

### 1. 发现服务器和笔记本

````
uv 运行“$SCRIPT”服务器 --compact
uv 运行“$SCRIPT”笔记本 --compact
````

### 2.执行代码（主要操作）

````
uv run "$SCRIPT" 执行 --path <notebook.ipynb> --code '<python 代码>' --compact
````

状态在执行调用中持续存在。变量、导入、对象都存活下来。

多行代码与 $'...' 引用一起使用：
````
uv run "$SCRIPT"execute --path scrap.ipynb --code $'import os\nfiles = os.listdir(".")\nprint(f"Found {len(files)} files")' --compact
````

### 3.检查实时变量

````
uv run "$SCRIPT" 变量 --path <notebook.ipynb> list --compact
uv run "$SCRIPT" 变量 --path <notebook.ipynb> 预览 --name <varname> --compact
````

### 4.编辑笔记本单元格

````
# 查看当前单元格
uv run "$SCRIPT" 内容 --path <notebook.ipynb> --compact

# 插入一个新单元格
uv run "$SCRIPT" edit --path <notebook.ipynb> 插入 \
  --at-index <N> --单元类型代码 --source '<code>' --compact

# 替换单元格源（使用内容输出中的单元格 ID）
uv run "$SCRIPT" edit --path <notebook.ipynb> 替换源 \
  --cell-id <id> --source '<新代码>' --compact

# 删除一个单元格
uv run "$SCRIPT" edit --path <notebook.ipynb> delete --cell-id <id> --compact
````

### 5.验证（重启+全部运行）

仅当用户要求进行干净验证或您需要确认时才使用
笔记本从上到下运行：

````
uv run "$SCRIPT" restart-run-all --path <notebook.ipynb> --save-outputs --compact
````

## 经验中的实用技巧

1. **服务器启动后首次执行可能会超时** — 内核需要一点时间
   初始化。如果超时，请重试。

2. **内核 Python 是 JupyterLab 的 Python** — 软件包必须安装在
   那个环境。如果您需要其他软件包，请将它们安装到
   首先是JupyterLab工具环境。

3. **--compact 标志可节省大量令牌** — 始终使用它。 JSON输出可以
   如果没有它，就会非常冗长。

4. **对于纯 REPL 使用**，创建一个 scrap.ipynb 并且不用费心进行单元格编辑。
   只需重复使用“执行”即可。

5. **参数顺序很重要** - 像 `--path` 这样的子命令标志放在
   子子命令。例如：“变量 --path nb.ipynb list”而不是“变量列表 --path nb.ipynb”。

6. **如果会话尚不存在**，您需要通过 REST API 启动一个会话
   （参见设置部分）。如果没有实时内核会话，该工具就无法执行。

7. **错误以 JSON 形式返回**并带有回溯 — 读取 `ename` 和 `evalue`
   字段以了解出了什么问题。

8. **偶尔的 websocket 超时** - 某些操作可能在第一次尝试时超时，
   特别是在内核重新启动之后。在升级之前重试一次。

## 超时默认值

该脚本每次执行的默认超时时间为 30 秒。对于长时间运行的
操作，传递`--timeout 120`。初始时使用充足的超时（60+）
设置或繁重的计算。