# ============================================================================
# OpenClaw 安装器（Windows 中国大陆镜像版）
# ============================================================================
# 一键安装 OpenClaw - Personal AI Assistant
# 由 OpenClaw 中文社区 (https://openclawal.cn) 提供镜像加速
#
# 用法：
#   irm https://openclawal.cn/scripts/install.ps1 | iex
#
# 带参数：
#   irm https://openclawal.cn/scripts/install.ps1 | iex
#   .\install.ps1 -SkipDaemon
#   .\install.ps1 -NoCnMirror -Debug
#
# 要求：Windows 10+ / Windows Server 2016+
# ============================================================================

param(
    [switch]$SkipDaemon,
    [switch]$NoCnMirror,
    [switch]$Debug
)

$ErrorActionPreference = "Stop"

# ============================================================================
# Configuration
# ============================================================================
$MinNodeMajor = 22
$MinNodeMinor = 19
$RecommendedNode = "24"
$OpenClawHome = "$env:USERPROFILE\.openclaw"

# 是否为非交互式（管道执行）
$IsPiped = [Console]::IsOutputRedirected

# ============================================================================
# Helper functions
# ============================================================================
function Write-Banner {
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║           🦞 OpenClaw 安装器                         ║" -ForegroundColor Cyan
    Write-Host "║           中国大陆镜像版                              ║" -ForegroundColor Cyan
    Write-Host "║                                                      ║" -ForegroundColor Cyan
    Write-Host "║           由 OpenClaw 中文社区提供镜像加速              ║" -ForegroundColor Cyan
    Write-Host "║           社区官网: https://openclawal.cn              ║" -ForegroundColor Cyan
    Write-Host "╚══════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

function Write-Info    { param([string]$Message) Write-Host "→ $Message" -ForegroundColor Cyan }
function Write-Ok      { param([string]$Message) Write-Host "✓ $Message" -ForegroundColor Green }
function Write-Warn    { param([string]$Message) Write-Host "⚠ $Message" -ForegroundColor Yellow }
function Write-Err     { param([string]$Message) Write-Host "✗ $Message" -ForegroundColor Red }
function Write-Step    { param([string]$Message) Write-Host "`n━━━ $Message ━━━" -ForegroundColor Blue }
function Write-Debug   { param([string]$Message) if ($Debug) { Write-Host "  [DEBUG] $Message" -ForegroundColor DarkYellow } }

# ============================================================================
# Step 0: Banner
# ============================================================================
Write-Banner

# ============================================================================
# Step 1: Check PowerShell version
# ============================================================================
Write-Step "检查系统环境"

$PsVersion = $PSVersionTable.PSVersion
Write-Debug "PowerShell 版本: $PsVersion"
if ($PsVersion.Major -lt 5) {
    Write-Err "需要 PowerShell 5.0+，当前版本: $PsVersion"
    Write-Info "请升级 Windows 或安装 WMF 5.1"
    exit 1
}

$OsInfo = Get-CimInstance Win32_OperatingSystem
Write-Ok "Windows: $($OsInfo.Caption) | PowerShell: $($PsVersion.Major).$($PsVersion.Minor)"

# ============================================================================
# Step 2: Check Node.js
# ============================================================================
Write-Step "检查 Node.js 运行时"

function Install-NodeViaFnm {
    Write-Info "通过 fnm 安装 Node $RecommendedNode..."

    $FnmUrl = "https://github.com/Schniz/fnm/releases/latest/download/fnm-windows.zip"
    if (-not $NoCnMirror) {
        $FnmUrl = "https://github.moeyy.xyz/https://github.com/Schniz/fnm/releases/latest/download/fnm-windows.zip"
    }

    $FnmDir = "$env:LOCALAPPDATA\fnm"
    $FnmPath = "$FnmDir\fnm.exe"
    $FnmZip = "$env:TEMP\fnm.zip"

    if (-not (Test-Path $FnmPath)) {
        Write-Info "下载 fnm..."
        try {
            New-Item -ItemType Directory -Force -Path $FnmDir | Out-Null
            Invoke-WebRequest -Uri $FnmUrl -OutFile $FnmZip -UseBasicParsing
            Expand-Archive -Path $FnmZip -DestinationPath $FnmDir -Force
            Remove-Item $FnmZip -Force
        } catch {
            Write-Warn "fnm 下载失败: $($_.Exception.Message)"
            return $false
        }
    }

    # 设置 fnm 环境
    $env:PATH = "$FnmDir;$env:PATH"
    [Environment]::SetEnvironmentVariable("PATH", "$FnmDir;$env:PATH", [EnvironmentVariableTarget]::User)

    try {
        if (-not $NoCnMirror) {
            $env:FNM_NODE_DIST_MIRROR = "https://npmmirror.com/mirrors/node"
        }
        $env:FNM_YES = "true"

        $fnmResult = & $FnmPath install $RecommendedNode 2>&1 | Out-String
        Write-Debug "fnm install 输出: $fnmResult"

        & $FnmPath default $RecommendedNode 2>&1 | Out-Null

        # 添加 fnm 到用户 PATH
        $fnmEnvPath = "$FnmDir\fnm.exe"
        $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
        if ($currentPath -notlike "*$FnmDir*") {
            [Environment]::SetEnvironmentVariable("PATH", "$FnmDir;$currentPath", "User")
        }

        # 加载 fnm 环境
        & $FnmPath env --use-on-cd | Out-String | Invoke-Expression

        return $true
    } catch {
        Write-Warn "fnm 安装失败: $($_.Exception.Message)"
        return $false
    }
}

function Install-NodeViaNvm {
    Write-Info "通过 nvm-windows 安装 Node $RecommendedNode..."

    $NvmUrl = "https://github.com/coreybutler/nvm-windows/releases/download/1.1.12/nvm-setup.zip"
    if (-not $NoCnMirror) {
        $NvmUrl = "https://github.moeyy.xyz/https://github.com/coreybutler/nvm-windows/releases/download/1.1.12/nvm-setup.zip"
    }

    $NvmDir = "$env:APPDATA\nvm"
    $NvmZip = "$env:TEMP\nvm-setup.zip"
    $NvmExe = "$env:TEMP\nvm-setup.exe"

    if (-not (Get-Command nvm -ErrorAction SilentlyContinue)) {
        Write-Info "下载 nvm-windows..."
        try {
            Invoke-WebRequest -Uri $NvmUrl -OutFile $NvmZip -UseBasicParsing
            Expand-Archive -Path $NvmZip -DestinationPath $env:TEMP -Force

            # 静默安装
            Start-Process -FilePath "$env:TEMP\nvm-setup.exe" -ArgumentList "/S" -Wait

            # 添加到 PATH
            $env:PATH = "$NvmDir;$env:PATH"
            [Environment]::SetEnvironmentVariable("PATH", "$NvmDir;$env:PATH", "User")

            Remove-Item $NvmZip -Force
        } catch {
            Write-Warn "nvm-windows 安装失败: $($_.Exception.Message)"
            return $false
        }
    }

    try {
        if (-not $NoCnMirror) {
            $env:NVM_NODEJS_ORG_MIRROR = "https://npmmirror.com/mirrors/node"
        }

        & nvm install $RecommendedNode 2>&1 | Out-String
        & nvm use $RecommendedNode 2>&1 | Out-String

        # 刷新 PATH 以包含 Node
        $env:PATH = [Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [Environment]::GetEnvironmentVariable("PATH", "User")

        return $true
    } catch {
        Write-Warn "nvm 安装失败: $($_.Exception.Message)"
        return $false
    }
}

function Install-NodeDirect {
    Write-Info "直接安装 Node $RecommendedNode..."

    if (-not $NoCnMirror) {
        $NodeUrl = "https://npmmirror.com/mirrors/node/v${RecommendedNode}.0.0/node-v${RecommendedNode}.0.0-x64.msi"
    } else {
        $NodeUrl = "https://nodejs.org/dist/v${RecommendedNode}.0.0/node-v${RecommendedNode}.0.0-x64.msi"
    }

    $MsiPath = "$env:TEMP\node-v${RecommendedNode}.msi"

    try {
        Write-Info "下载 Node.js 安装包..."
        Invoke-WebRequest -Uri $NodeUrl -OutFile $MsiPath -UseBasicParsing

        Write-Info "正在安装 Node.js... (可能需要管理员权限)"
        Start-Process msiexec.exe -ArgumentList "/i `"$MsiPath`" /quiet /norestart" -Wait

        # 刷新 PATH
        $env:PATH = [Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [Environment]::GetEnvironmentVariable("PATH", "User")

        Remove-Item $MsiPath -Force
        return $true
    } catch {
        Write-Err "Node.js 安装失败: $($_.Exception.Message)"
        return $false
    }
}

$nodeInstalled = $false
$nodeCmd = Get-Command node -ErrorAction SilentlyContinue

if ($nodeCmd) {
    $nodeVersion = & node --version
    $versionParts = $nodeVersion -replace 'v', '' -split '\.'
    $major = [int]$versionParts[0]
    $minor = [int]$versionParts[1]

    Write-Debug "Node 版本: $nodeVersion (major=$major, minor=$minor)"

    if ($major -gt $MinNodeMajor -or ($major -eq $MinNodeMajor -and $minor -ge $MinNodeMinor)) {
        Write-Ok "Node.js $nodeVersion ✓ (要求: v$MinNodeMajor.$MinNodeMinor+)"
        $nodeInstalled = $true
    } else {
        Write-Warn "Node.js $nodeVersion 版本过低，需要 v$MinNodeMajor.$MinNodeMinor+"
    }
}

if (-not $nodeInstalled) {
    Write-Info "未找到合适的 Node.js，开始安装..."

    # 尝试三种方式依次降级
    if (Install-NodeViaFnm) {
        $nodeInstalled = $true
    } elseif (Install-NodeViaNvm) {
        $nodeInstalled = $true
    } elseif (Install-NodeDirect) {
        $nodeInstalled = $true
    } else {
        Write-Err "Node.js 安装失败"
        Write-Info "请手动安装 Node.js v$MinNodeMajor.$MinNodeMinor+ 后重试"
        Write-Info "  https://nodejs.org"
        exit 1
    }
}

# 最终确认
$nodeCmd = Get-Command node -ErrorAction SilentlyContinue
if (-not $nodeCmd) {
    Write-Err "Node.js 未安装成功，请手动安装"
    exit 1
}

$nodeVersion = & node --version
Write-Ok "Node.js $nodeVersion Ready"

$npmVersion = & npm --version
Write-Ok "npm v$npmVersion"

# ============================================================================
# Step 3: Configure npm mirror
# ============================================================================
if (-not $NoCnMirror) {
    Write-Step "配置 npm 国内镜像源"

    $currentRegistry = & npm config get registry
    Write-Debug "当前 registry: $currentRegistry"

    if ($currentRegistry -match "npmmirror") {
        Write-Ok "npm 镜像源已配置: $currentRegistry"
    } else {
        Write-Info "设置 npm registry 为 npmmirror.com..."
        & npm config set registry https://registry.npmmirror.com/
        Write-Ok "registry 已设置为: https://registry.npmmirror.com/"
    }
}

# ============================================================================
# Step 4: Install OpenClaw
# ============================================================================
Write-Step "安装 OpenClaw"

Write-Info "执行: npm install -g openclaw@latest"

$installOutput = & npm install -g openclaw@latest 2>&1 | Out-String
$installExit = $LASTEXITCODE

if ($installExit -ne 0) {
    Write-Warn "npm 安装失败 (exit code: $installExit)"
    Write-Debug "输出: $installOutput"

    if (-not $NoCnMirror) {
        Write-Warn "尝试使用默认 registry 重试..."
        & npm config set registry https://registry.npmjs.org/
        $installOutput = & npm install -g openclaw@latest 2>&1 | Out-String
        $installExit = $LASTEXITCODE

        if ($installExit -ne 0) {
            Write-Err "安装失败"
            Write-Debug "输出: $installOutput"
            exit 1
        }

        # 恢复镜像
        & npm config set registry https://registry.npmmirror.com/
    } else {
        Write-Err "安装失败"
        Write-Debug "输出: $installOutput"
        exit 1
    }
}

Write-Ok "OpenClaw 安装完成"

# 验证
$openclawCmd = Get-Command openclaw -ErrorAction SilentlyContinue
if ($openclawCmd) {
    Write-Ok "openclaw 命令可用"
} else {
    Write-Warn "openclaw 命令未在 PATH 中找到"
    Write-Info "请重新打开终端后重试"

    # 尝试找到 npm global
    $npmPrefix = & npm config get prefix
    $openclawPath = "$npmPrefix\openclaw.cmd"
    if (Test-Path $openclawPath) {
        Write-Info "找到: $openclawPath"
        $currentPath = [Environment]::GetEnvironmentVariable("PATH", "User")
        if ($currentPath -notlike "*$npmPrefix*") {
            [Environment]::SetEnvironmentVariable("PATH", "$npmPrefix;$currentPath", "User")
            Write-Info "已添加 $npmPrefix 到用户 PATH，请重新打开终端"
        }
    }
}

# ============================================================================
# Step 5: Onboard
# ============================================================================
if (-not $SkipDaemon) {
    Write-Step "初始化 OpenClaw (Onboard)"

    Write-Info "首次运行会引导你完成 AI 模型和频道配置"
    Write-Info "请准备好你的 OpenAI API Key"
    Write-Host ""

    if (-not $IsPiped) {
        Write-Info "运行: openclaw onboard --install-daemon"
        try {
            & openclaw onboard --install-daemon 2>&1 | ForEach-Object { Write-Host $_ }
        } catch {
            Write-Warn "Onboard 退出 ($($_.Exception.Message))"
            Write-Info "可稍后手动运行: openclaw onboard --install-daemon"
        }
    } else {
        Write-Warn "非交互模式，跳过 Onboard 引导"
        Write-Info "安装后请手动运行: openclaw onboard --install-daemon"
    }
} else {
    Write-Info "跳过 daemon 安装"
    Write-Info "手动配置: openclaw onboard --install-daemon"
}

# ============================================================================
# Done
# ============================================================================
Write-Step "安装完成"

Write-Host ""
Write-Host "  OpenClaw 已安装成功" -ForegroundColor Green
Write-Host ""
Write-Host "  快速命令:" -ForegroundColor White
Write-Host "    openclaw onboard --install-daemon  初始化配置" -ForegroundColor Cyan
Write-Host "    openclaw gateway status            查看网关状态" -ForegroundColor Cyan
Write-Host "    openclaw doctor                    检查配置" -ForegroundColor Cyan
Write-Host "    openclaw --help                    帮助" -ForegroundColor Cyan
Write-Host ""
Write-Host "  社区支持:" -ForegroundColor White
Write-Host "    https://openclawal.cn              中文社区" -ForegroundColor Cyan
Write-Host "    https://github.com/openclaw/openclaw  GitHub" -ForegroundColor Cyan
Write-Host ""
Write-Host "  🦞 EXFOLIATE! EXFOLIATE!" -ForegroundColor Cyan
Write-Host ""
