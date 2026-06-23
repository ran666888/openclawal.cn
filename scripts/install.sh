#!/bin/bash
# ============================================================================
# OpenClaw 安装器（中国大陆镜像版）
# ============================================================================
# 一键安装 OpenClaw - Personal AI Assistant
# 由 OpenClaw 中文社区 (https://openclawal.cn) 提供镜像加速
#
# 用法：
#   curl -fsSL https://openclawal.cn/scripts/install.sh | bash
#
# 带参数：
#   curl -fsSL https://openclawal.cn/scripts/install.sh | bash -s -- --skip-daemon
#   curl -fsSL https://openclawal.cn/scripts/install.sh | bash -s -- --no-cn-mirror
#   curl -fsSL https://openclawal.cn/scripts/install.sh | bash -s -- --debug
#
# ============================================================================

set -e

# ============================================================================
# Colors
# ============================================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'
BOLD='\033[1m'

# ============================================================================
# Default configuration
# ============================================================================
OPENCLAW_HOME="${OPENCLAW_HOME:-$HOME/.openclaw}"
INSTALL_DAEMON=true
USE_CN_MIRROR=true
DEBUG=false
MIN_NODE_MAJOR=22
MIN_NODE_MINOR=19
RECOMMENDED_NODE=24

# ============================================================================
# Parse arguments
# ============================================================================
while [[ $# -gt 0 ]]; do
    case $1 in
        --skip-daemon)
            INSTALL_DAEMON=false
            shift
            ;;
        --no-cn-mirror)
            USE_CN_MIRROR=false
            shift
            ;;
        --debug)
            DEBUG=true
            shift
            ;;
        *)
            echo -e "${RED}未知参数: $1${NC}"
            echo "用法: curl -fsSL https://openclawal.cn/scripts/install.sh | bash -s -- [选项]"
            echo "  --skip-daemon    跳过 daemon 安装（只装 CLI）"
            echo "  --no-cn-mirror   不使用国内镜像源"
            echo "  --debug          输出调试信息"
            exit 1
            ;;
    esac
done

# ============================================================================
# Helper functions
# ============================================================================
info()  { echo -e "${CYAN}→${NC} $1"; }
ok()    { echo -e "${GREEN}✓${NC} $1"; }
warn()  { echo -e "${YELLOW}⚠${NC} $1"; }
err()   { echo -e "${RED}✗${NC} $1"; }
step()  { echo; echo -e "${BLUE}━━━ $1 ━━━${NC}"; }
debug() { if [ "$DEBUG" = true ]; then echo -e "  ${YELLOW}[DEBUG]${NC} $1"; fi; }

BANNER="
╔══════════════════════════════════════════════════════╗
║           🦞 OpenClaw 安装器                         ║
║           中国大陆镜像版                              ║
║                                                      ║
║           由 OpenClaw 中文社区提供镜像加速              ║
║           社区官网: https://openclawal.cn              ║
╚══════════════════════════════════════════════════════╝
"

# ============================================================================
# Step 0: Print banner
# ============================================================================
echo -e "$BANNER"

# ============================================================================
# Step 1: Detect OS
# ============================================================================
step "检测系统环境"

OS=""
OS_FAMILY=""
case "$(uname -s)" in
    Linux*)  OS="linux"; OS_FAMILY="linux" ;;
    Darwin*) OS="macos"; OS_FAMILY="darwin" ;;
    *)
        if [ -n "$TERMUX_VERSION" ]; then
            OS="termux"; OS_FAMILY="linux"
        else
            err "不支持的操作系统: $(uname -s)"
            info "OpenClaw 支持 Linux、macOS、Windows（请用 install.ps1）和 Termux"
            exit 1
        fi
        ;;
esac

ARCH="$(uname -m)"
case "$ARCH" in
    x86_64|amd64) ARCH="x64" ;;
    aarch64|arm64) ARCH="arm64" ;;
    *)
        warn "未检测到的架构: $ARCH，尝试继续安装"
        ;;
esac

ok "系统: $(uname -s) | 架构: $ARCH"
info "家目录: $HOME"
debug "OPENCLAW_HOME: $OPENCLAW_HOME"

# ============================================================================
# Step 2: Check Node.js
# ============================================================================
step "检查 Node.js 运行时"

install_node() {
    info "将安装 Node.js $RECOMMENDED_NODE ..."

    local NODE_INSTALL_URL
    if [ "$USE_CN_MIRROR" = true ]; then
        NODE_INSTALL_URL="https://npmmirror.com/mirrors/node/v${RECOMMENDED_NODE}.0.0/"
        debug "Node 镜像源: $NODE_INSTALL_URL"
    fi

    # 使用 nvm 或 fnm 安装
    if command -v fnm &>/dev/null; then
        info "检测到 fnm，将使用 fnm 安装 Node $RECOMMENDED_NODE"
        if [ "$USE_CN_MIRROR" = true ]; then
            export FNM_NODE_DIST_MIRROR="https://npmmirror.com/mirrors/node"
        fi
        fnm install "$RECOMMENDED_NODE" 2>/dev/null || {
            warn "fnm 安装失败，尝试 nvm..."
            install_node_via_nvm
        }
    elif command -v nvm &>/dev/null || [ -f "$HOME/.nvm/nvm.sh" ]; then
        install_node_via_nvm
    elif command -v brew &>/dev/null && [ "$OS" = "macos" ]; then
        info "通过 Homebrew 安装 Node"
        brew install node@$RECOMMENDED_NODE 2>&1 | tail -1
    else
        info "未找到 Node，尝试通过官方脚本安装..."
        # 用 nvm 安装
        if ! command -v curl &>/dev/null; then
            err "需要 curl 来安装 nvm，请先安装 curl"
            err "或手动安装 Node.js $MIN_NODE_MAJOR.$MIN_NODE_MINOR+ 后重试"
            exit 1
        fi
        install_node_via_nvm
    fi
}

install_node_via_nvm() {
    export NVM_NODEJS_ORG_MIRROR="https://nodejs.org/dist"
    if [ "$USE_CN_MIRROR" = true ]; then
        export NVM_NODEJS_ORG_MIRROR="https://npmmirror.com/mirrors/node"
        debug "nvm 镜像源: $NVM_NODEJS_ORG_MIRROR"
    fi

    if [ ! -f "$HOME/.nvm/nvm.sh" ]; then
        info "安装 nvm..."
        curl -fsSL https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.0/install.sh | bash
    fi

    # shellcheck source=/dev/null
    [ -f "$HOME/.nvm/nvm.sh" ] && . "$HOME/.nvm/nvm.sh"

    info "通过 nvm 安装 Node $RECOMMENDED_NODE..."
    nvm install "$RECOMMENDED_NODE" 2>&1 | tail -1
    nvm use "$RECOMMENDED_NODE" 2>&1 | tail -1
}

NODE_OK=false
if command -v node &>/dev/null; then
    NODE_VERSION=$(node --version | sed 's/v//')
    NODE_MAJOR=$(echo "$NODE_VERSION" | cut -d. -f1)
    NODE_MINOR=$(echo "$NODE_VERSION" | cut -d. -f2)
    debug "Node 版本: v$NODE_VERSION (major=$NODE_MAJOR, minor=$NODE_MINOR)"

    if [ "$NODE_MAJOR" -gt "$MIN_NODE_MAJOR" ] || { [ "$NODE_MAJOR" -eq "$MIN_NODE_MAJOR" ] && [ "$NODE_MINOR" -ge "$MIN_NODE_MINOR" ]; }; then
        ok "Node.js v$NODE_VERSION ✓ (要求: v$MIN_NODE_MAJOR.$MIN_NODE_MINOR+)"
        NODE_OK=true
    else
        warn "Node.js v$NODE_VERSION 版本过低，需要 v$MIN_NODE_MAJOR.$MIN_NODE_MINOR+"
    fi
fi

if [ "$NODE_OK" != true ]; then
    install_node
fi

# 再次确认
if ! command -v node &>/dev/null; then
    err "Node.js 安装失败，请手动安装 Node $MIN_NODE_MAJOR.$MIN_NODE_MINOR+"
    err "  https://nodejs.org"
    exit 1
fi

NODE_VERSION=$(node --version)
ok "Node.js $NODE_VERSION"

# 检查 npm
if ! command -v npm &>/dev/null; then
    err "npm 未找到，请检查 Node.js 安装"
    exit 1
fi
NPM_VERSION=$(npm --version)
ok "npm v$NPM_VERSION"

# ============================================================================
# Step 3: Configure npm mirror for China
# ============================================================================
if [ "$USE_CN_MIRROR" = true ]; then
    step "配置 npm 国内镜像源"

    CURRENT_REGISTRY=$(npm config get registry)
    debug "当前 registry: $CURRENT_REGISTRY"

    if echo "$CURRENT_REGISTRY" | grep -q "npmmirror.com"; then
        ok "npm 镜像源已配置为国内镜像: $CURRENT_REGISTRY"
    else
        info "设置 npm registry 为 npmmirror.com 镜像..."
        npm config set registry https://registry.npmmirror.com/
        ok "registry 已设置为: https://registry.npmmirror.com/"
    fi
fi

# ============================================================================
# Step 4: Install OpenClaw globally
# ============================================================================
step "安装 OpenClaw"

info "执行: npm install -g openclaw@latest"
if [ "$DEBUG" = true ]; then
    # 先查最新版本号
    OPENCLAW_VERSION=$(npm view openclaw version 2>/dev/null || echo "unknown")
    info "OpenClaw 最新版本: $OPENCLAW_VERSION"
fi

INSTALL_OUTPUT=$(npm install -g openclaw@latest 2>&1) || {
    INSTALL_EXIT=$?
    err "npm 安装失败 (exit code: $INSTALL_EXIT)"
    err "输出:"
    echo "$INSTALL_OUTPUT" | while IFS= read -r line; do echo "  $line"; done

    # 尝试非镜像安装
    if [ "$USE_CN_MIRROR" = true ]; then
        warn "镜像安装失败，尝试使用默认 registry 重试..."
        npm config set registry https://registry.npmjs.org/
        INSTALL_OUTPUT=$(npm install -g openclaw@latest 2>&1) || {
            err "仍然安装失败"
            echo "$INSTALL_OUTPUT" | while IFS= read -r line; do echo "  $line"; done
            exit 1
        }
        # 恢复镜像
        npm config set registry https://registry.npmmirror.com/
    else
        exit 1
    fi
}

ok "OpenClaw 安装完成"

# 验证安装
if command -v openclaw &>/dev/null; then
    OPENCLAW_VERSION=$(openclaw --version 2>/dev/null || echo "installed")
    ok "openclaw 命令可用 (版本: $OPENCLAW_VERSION)"
else
    warn "openclaw 命令未在 PATH 中找到"
    # 检查 npm global bin 路径
    NPM_PREFIX=$(npm config get prefix)
    info "npm global bin 目录: $NPM_PREFIX/bin"
    if [ -f "$NPM_PREFIX/bin/openclaw" ]; then
        info "手动添加 PATH: export PATH=\"$NPM_PREFIX/bin:\$PATH\""
        export PATH="$NPM_PREFIX/bin:$PATH"
        # 写入 shell 配置
        SHELL_CONFIG=""
        case "$SHELL" in
            */zsh) SHELL_CONFIG="$HOME/.zshrc" ;;
            */bash) SHELL_CONFIG="$HOME/.bashrc" ;;
        esac
        if [ -n "$SHELL_CONFIG" ] && ! grep -q "$NPM_PREFIX/bin" "$SHELL_CONFIG" 2>/dev/null; then
            echo "" >> "$SHELL_CONFIG"
            echo "# OpenClaw" >> "$SHELL_CONFIG"
            echo "export PATH=\"$NPM_PREFIX/bin:\$PATH\"" >> "$SHELL_CONFIG"
            info "已写入 $SHELL_CONFIG"
        fi
    else
        err "openclaw 未安装成功，请手动运行: npm install -g openclaw@latest"
        exit 1
    fi
fi

# ============================================================================
# Step 5: Onboard (install daemon)
# ============================================================================
if [ "$INSTALL_DAEMON" = true ]; then
    step "初始化 OpenClaw (Onboard)"

    info "运行: openclaw onboard --install-daemon"
    info "首次运行会引导你完成配置（AI 模型、频道绑定等）"
    echo ""
    echo -e "  ${YELLOW}提示:${NC} 请准备好你的 AI 模型 API Key (如 OpenAI)"
    echo -e "  ${YELLOW}按提示操作即可，Onboard 会一步步引导你${NC}"
    echo ""

    if [ -t 0 ]; then
        # 交互式终端，直接执行 onboard
        openclaw onboard --install-daemon 2>&1 || {
            WARN_EXIT=$?
            warn "Onboard 初始化退出 (exit code: $WARN_EXIT)"
            info "可以稍后手动运行: openclaw onboard --install-daemon"
        }
    else
        warn "非交互式安装，跳过 Onboard 交互引导"
        info "安装完成后请手动运行: openclaw onboard --install-daemon"
        info "或运行: openclaw gateway start"
    fi
else
    info "跳过 daemon 安装（--skip-daemon）"
    info "手动启动: openclaw onboard --install-daemon"
fi

# ============================================================================
# Done
# ============================================================================
step "安装完成"

echo ""
echo -e "  ${GREEN}OpenClaw 已安装成功${NC}"
echo ""
echo -e "  快速命令:"
echo -e "    ${CYAN}openclaw onboard --install-daemon${NC}  初始化配置"
echo -e "    ${CYAN}openclaw gateway status${NC}            查看网关状态"
echo -e "    ${CYAN}openclaw doctor${NC}                    检查配置"
echo -e "    ${CYAN}openclaw --help${NC}                    帮助"
echo ""
echo -e "  社区支持:"
echo -e "    ${CYAN}https://openclawal.cn${NC}              中文社区"
echo -e "    ${CYAN}https://github.com/openclaw/openclaw${NC}  GitHub"
echo ""
echo -e "  ${BLUE}🦞 EXFOLIATE! EXFOLIATE!${NC}"
echo ""
