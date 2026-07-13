#!/usr/bin/env bash

set -euo pipefail

project_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
UTILBOX_SOURCE_ONLY=1
source "$project_root/install.sh"

assert_os_packages() {
    local os_id=$1
    local expected_manager=$2
    shift 2
    local -a expected_packages=("$@")
    local -a packages=()
    local manager

    detect_linux_dependencies "$os_id" manager packages

    [[ $manager == "$expected_manager" ]]
    [[ ${packages[*]} == "${expected_packages[*]}" ]]
}

assert_unsupported_os() {
    local manager
    local -a packages=()

    if detect_linux_dependencies "$1" manager packages >/dev/null 2>&1; then
        echo "expected $1 to be unsupported" >&2
        return 1
    fi
}

assert_os_packages fedora dnf python3-tkinter google-noto-sans-cjk-vf-fonts google-noto-color-emoji-fonts
assert_os_packages ubuntu apt python3-tk fonts-noto-cjk fonts-noto-color-emoji
assert_os_packages debian apt python3-tk fonts-noto-cjk fonts-noto-color-emoji
assert_unsupported_os arch

echo "install.sh dependency selection tests passed"
