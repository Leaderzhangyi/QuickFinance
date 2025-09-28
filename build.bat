@echo off
chcp 65001 >nul
echo ================================================
echo Qt资源文件编译脚本
echo ================================================

REM 检查是否在虚拟环境中
if not defined VIRTUAL_ENV (
    echo 检测到未在虚拟环境中运行，尝试使用uv...
    uv run python build_resources.py %*
) else (
    echo 在虚拟环境中运行...
    python build_resources.py %*
)

echo.
echo 按任意键退出...
pause >nul
