---
title: "Docker Management"
sidebar_label: "Docker Management"
description: "Manage Docker containers, images, volumes, networks, and Compose stacks — lifecycle ops, debugging, cleanup, and Dockerfile optimization"
---
{/* 此页面是通过 website/scripts/generate-skill-docs.py 从技能的 SKILL.md 自动生成的。编辑源 SKILL.md，而不是此页面。 */}

# Docker 管理

管理 Docker 容器、镜像、卷、网络和 Compose 堆栈 — 生命周期操作、调试、清理和 Dockerfile 优化。

## 技能元数据

| | |
|---|---|
|来源 |可选 — 使用 `hermes Skills installficial/devops/docker-management` 安装 |
|路径| `可选技能/de​​vops/docker 管理` |
|版本 | `1.0.0` |
|作者 | srmn24 |
|许可证|麻省理工学院 |
|平台| linux、macos、windows |
|标签 | `docker`、`容器`、`devops`、`基础设施`、`compose`、`images`、`volumes`、`networks`、`debugging` |

##参考：完整的SKILL.md

:::信息
以下是触发该技能时赫尔墨斯加载的完整技能定义。这是技能激活时代理所看到的指令。
:::

# Docker 管理

使用标准 Docker CLI 命令管理 Docker 容器、映像、卷、网络和 Compose 堆栈。除了 Docker 本身之外，没有其他依赖项。

## 何时使用

- 运行、停止、重新启动、删除或检查容器
- 构建、拉取、推送、标记或清理 Docker 镜像
- 使用 Docker Compose（多服务堆栈）
- 管理卷或网络
- 调试崩溃的容器或分析日志
- 检查 Docker 磁盘使用情况或释放空间
- 检查或优化 Dockerfile

## 先决条件

- Docker 引擎已安装并运行
- 用户添加到“docker”组（或使用“sudo”）
- Docker Compose v2（包含在现代 Docker 安装中）

快速检查：

````bash
docker --version && docker compose 版本
````

## 快速参考

|任务|命令|
|------|---------|
|运行容器（后台）| `docker run -d --name NAME IMAGE` |
|停止+删除| `docker stop 名称 && docker rm 名称` |
|查看日志（关注）| `docker 日志 --tail 50 -f NAME` |
|将壳装入容器| `docker exec -it NAME /bin/sh` |
|列出所有容器 | `docker ps -a` |
|打造形象| `docker build -t 标签。` |
|撰写 | `docker compose up -d` |
|写下来| `docker 撰写下来` |
|磁盘使用情况| `docker 系统 df` |
|清理悬空| `docker 镜像修剪 && docker 容器修剪` |

## 程序

### 1. 识别域

找出请求属于哪个区域：

- **容器生命周期** → 运行、停止、启动、重新启动、rm、暂停/取消暂停
- **容器交互** → exec、cp、日志、检查、统计
- **图像管理** → 构建、拉取、推送、标记、rmi、保存/加载
- **Docker Compose** → 向上、向下、ps、日志、执行、构建、配置
- **卷和网络** → 创建、检查、rm、修剪、连接
- **故障排除** → 日志分析、退出代码、资源问题

### 2. 容器操作

**运行一个新容器：**

````bash
# 具有端口映射的分离服务
docker run -d --name web -p 8080:80 nginx

# 带有环境变量
docker run -d -e POSTGRES_PASSWORD=秘密 -e POSTGRES_DB=mydb --name db postgres:16

# 具有持久数据（命名卷）
docker run -d -v pgdata:/var/lib/postgresql/data --name db postgres:16

# 用于开发（绑定挂载源代码）
docker run -d -v $(pwd)/src:/app/src -p 3000:3000 --name dev my-app

# 交互式调试（退出时自动删除）
docker run -it --rm ubuntu:22.04 /bin/bash

# 具有资源限制和重启策略
docker run -d --内存=512m --cpus=1.5 --restart=unless-stopped --name app my-app
````

关键标志：“-d”分离、“-it”交互式+tty、“--rm”自动删除、“-p”端口（主机：容器）、“-e”环境变量、“-v”卷、“--name”名称、“--restart”重启策略。

**管理正在运行的容器：**

````bash
docker ps # 运行容器
docker ps -a # 全部（包括停止）
docker stop NAME # 优雅停止
docker start NAME # 启动停止的容器
docker restart NAME # 停止 + 启动
docker rm NAME # 删除停止的容器
docker rm -f NAME # 强制删除正在运行的容器
docker container prune # 删除所有停止的容器
````

**与容器交互：**

````bash
docker exec -it NAME /bin/sh # shell 访问（如果可用，请使用 /bin/bash）
docker exec NAME env #查看环境变量
docker exec -u root NAME apt update # 以特定用户身份运行
docker log --tail 100 -f NAME # 跟踪最后 100 行
docker log --since 2h NAME # 过去 2 小时的日志
docker cp NAME:/path/file ./local # 从容器复制文件
docker cp ./file NAME:/path/ # 将文件复制到容器
docker检查NAME#完整的容器详细信息（JSON）
docker stats --no-stream # 资源使用情况快照
docker top NAME # 正在运行的进程
````

### 3.形象管理

````bash
# 构建
docker build -t my-app:latest 。
docker build -t my-app:prod -f Dockerfile.prod 。
docker build --no-cache -t my-app 。              # 干净重建
DOCKER_BUILDKIT=1 docker build -t my-app 。       # 使用 BuildKit 更快

# 拉和推
docker拉节点：20-alpine
docker 登录 ghcr.io
docker 标签 my-app:最新注册表/my-app:v1.0
docker 推送注册表/my-app:v1.0

# 检查
docker images # 列出本地镜像
docker 历史 IMAGE # 查看层
docker 检查 IMAGE # 完整详细信息

# 清理
docker image prune # 删除悬空（未标记）图像
docker image prune -a # 删除所有未使用的镜像（小心！）
docker image prune -a --filter "until=168h" # 超过 7 天未使用的镜像
````

### 4.Docker 组合

````bash
# 开始/停止
docker compose up -d # 启动所有分离的服务
docker compose up -d --build # 在开始之前重建镜像
docker compose down # 停止并删除容器
docker compose down -v # 还删除卷（销毁数据）

# 监控
docker compose ps # 列出服务
docker compose logs -f api # 跟踪特定服务的日志
docker compose logs --tail 50 # 最后 50 行所有服务

# 互动
docker compose exec api /bin/sh # shell 进入正在运行的服务
docker compose run --rm api npm test # 一次性命令（新容器）
docker compose restart api # 重启特定服务

# 验证
docker compose config # 验证并查看已解析的配置
````

**最小 compose.yml 示例：**

````yaml
服务：
  应用程序编程接口：
    构建： .
    端口：
      - “3000:3000”
    环境：
      - DATABASE_URL=postgres://用户:pass@db:5432/mydb
    取决于：
      数据库：
        条件：服务健康

  数据库：
    图片：postgres：16-alpine
    环境：
      POSTGRES_USER：用户
      POSTGRES_PASSWORD：通过
      POSTGRES_DB：mydb
    卷：
      - pgdata:/var/lib/postgresql/data
    健康检查：
      测试：[“CMD-SHELL”，“pg_isready -U 用户”]
      间隔：10秒
      超时：5秒
      重试次数：5

卷：
  PG数据：
````

### 5. 卷和网络

````bash
# 卷
docker volume ls # 列出卷
docker volume create mydata # 创建命名卷
dockervolumeinspectmydata#详细信息（挂载点等）
docker Volume rm mydata # 删除（如果使用则失败）
docker volume prune # 删除未使用的卷

# 网络
docker network ls # 列出网络
docker network create mynet # 创建桥接网络
docker网络检查mynet＃详细信息（连接的容器）
docker network connect mynet NAME # 将容器连接到网络
docker network disconnect mynet NAME # 分离容器
docker network rm mynet # 删除网络
docker network prune # 删除未使用的网络
````

### 6.磁盘使用和清理

清洁前务必先进行诊断：

````bash
# 检查什么正在使用空间
docker system df # 摘要
docker system df -v # 详细细分

# 有针对性的清理（安全）
docker container prune # 停止的容器
docker image prune # 悬挂图像
docker volume prune # 未使用的卷
docker network prune # 未使用的网络

# 积极清理（首先与用户确认！）
docker system prune # 容器+镜像+网络
docker system prune -a # 也未使用的镜像
docker system prune -a --volumes # 一切 — 也命名卷
````

**警告：** 在未与用户确认的情况下，切勿运行“docker system prune -a --volumes”。这将删除具有潜在重要数据的命名卷。

## 陷阱

|问题 |原因 |修复 |
|--------|--------|-----|
|容器立即退出 |主进程完成或崩溃 |检查 `docker log NAME`，尝试 `docker run -it --entrypoint /bin/sh IMAGE` |
| “端口已分配”|使用该端口的另一个进程 | `docker ps` 或 `lsof -i :PORT` 来找到它 |
| “设备上没有剩余空间”| Docker 磁盘已满 | `docker system df` 然后有针对性的修剪 |
|无法连接到容器 |应用程序绑定到容器内的 127.0.0.1 |应用程序必须绑定到 `0.0.0.0`，检查 `-p` 映射 |
|卷上的权限被拒绝 |主机与容器的 UID/GID 不匹配 |使用 `--user $(id -u):$(id -g)` 或修复权限 |
| Compose 服务无法互相访​​问 |网络或服务名称错误 |服务使用服务名称作为主机名，检查 `docker compose config` |
|构建缓存不起作用 | Dockerfile 中的层顺序错误 |将很少更改的层放在前面（源代码之前的 deps）|
|图片太大 |没有多阶段构建，没有 .dockerignore |使用多阶段构建，添加 `.dockerignore` |

## 验证

执行任何 Docker 操作后，验证结果：

- **容器已启动？** → `docker ps`（检查状态为“Up”）
- **日志干净？** → `docker log --tail 20 NAME` （没有错误）
- **端口可访问？** → `curl -s http://localhost:PORT` 或 `docker port NAME`
- **构建镜像？** → `docker images | grep 标签`
- **Compose 堆栈健康吗？** → `docker compose ps` （所有服务“运行”或“健康”）
- **磁盘已释放？** → `docker system df` （比较之前/之后）

## Dockerfile 优化技巧

在查看或创建 Dockerfile 时，提出以下改进建议：

1. **多阶段构建** - 将构建环境与运行时分开以减少最终图像大小
2. **层排序** — 将依赖项放在源代码之前，这样更改不会使缓存的层失效
3. **组合 RUN 命令** — 层数更少，图像更小
4. **使用 .dockerignore** — 排除 `node_modules`、`.git`、`__pycache__` 等。
5. **固定基础镜像版本** — `node:20-alpine` 而不是 `node:latest`
6. **以非 root 身份运行** — 添加 `USER` 指令以确保安全
7. **使用 slim/alpine 底座** — `python:3.12-slim` 而不是 `python:3.12`