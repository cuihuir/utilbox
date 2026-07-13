#!/usr/bin/env bash
# UtilBox installer for supported Linux distributions.

set -e

detect_linux_dependencies() {
    local os_id=$1
    local -n dependency_manager=$2
    local -n dependency_packages=$3

    case "$os_id" in
        fedora)
            dependency_packages=(
                python3-tkinter
                google-noto-sans-cjk-vf-fonts
                google-noto-color-emoji-fonts
            )
            dependency_manager=dnf
            ;;
        ubuntu|debian)
            dependency_packages=(
                python3-tk
                fonts-noto-cjk
                fonts-noto-color-emoji
            )
            dependency_manager=apt
            ;;
        *)
            printf 'Unsupported Linux distribution: %s\n' "$os_id" >&2
            return 1
            ;;
    esac
}

is_package_installed() {
    local package_manager=$1
    local package_name=$2

    case "$package_manager" in
        apt) dpkg-query -W -f='${db:Status-Status}' "$package_name" 2>/dev/null | grep -qx installed ;;
        dnf) rpm -q "$package_name" &>/dev/null ;;
    esac
}

install_system_dependencies() {
    local os_id
    local package_manager
    local -a packages=()
    local -a missing_packages=()
    local package_name

    if [[ ! -r /etc/os-release ]]; then
        echo "Cannot identify the Linux distribution: /etc/os-release is unavailable." >&2
        return 1
    fi

    # shellcheck disable=SC1091
    source /etc/os-release
    os_id=$ID
    detect_linux_dependencies "$os_id" package_manager packages || return 1

    for package_name in "${packages[@]}"; do
        if is_package_installed "$package_manager" "$package_name"; then
            echo "✅ $package_name 已安装"
        else
            missing_packages+=("$package_name")
        fi
    done

    if (( ${#missing_packages[@]} == 0 )); then
        return
    fi

    echo "⚠️  正在安装系统依赖: ${missing_packages[*]}"
    case "$package_manager" in
        apt)
            sudo apt update
            sudo apt install -y "${missing_packages[@]}"
            ;;
        dnf)
            sudo dnf install -y "${missing_packages[@]}"
            ;;
    esac
    echo "✅ 系统依赖安装完成"
}

main() {
    echo "=================================="
    echo "  UtilBox 安装脚本"
    echo "=================================="
    echo ""

    if ! command -v uv &> /dev/null; then
        echo "📦 正在安装 uv 包管理器..."
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.local/bin:$PATH"
        echo "✅ uv 安装完成"
        echo ""
    else
        echo "✅ uv 已安装"
        echo ""
    fi

    echo "📋 检查系统依赖..."
    install_system_dependencies

    echo ""
    echo "📦 安装 Python 依赖..."
    uv sync

    echo ""
    echo "=================================="
    echo "  ✅ 安装完成！"
    echo "=================================="
    echo ""
    echo "运行方式："
    echo "  python utilbox.py"
    echo ""
    echo "或者："
    echo "  uv run python utilbox.py"
    echo ""
}

if [[ ${UTILBOX_SOURCE_ONLY:-0} != 1 ]]; then
    main "$@"
fi
