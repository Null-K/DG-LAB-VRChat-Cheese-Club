@echo off
cd /d "%~dp0"
echo === 芝士郊狼控制软件 - 构建 EXE ===
echo.

echo [1/3] 生成图标...
python create_icon.py
if errorlevel 1 (
    echo 图标生成失败!
    pause
    exit /b 1
)

echo.
echo [2/3] 安装 PyInstaller...
pip install pyinstaller -q

echo.
echo [3/3] 打包 EXE...
pyinstaller ^
    --noconfirm ^
    --onefile ^
    --windowed ^
    --name "芝士郊狼控制软件" ^
    --icon app_icon.ico ^
    --add-data "settings.py;." ^
    --hidden-import qrcode ^
    --hidden-import PIL ^
    --hidden-import numpy ^
    --hidden-import websockets ^
    --hidden-import websockets.legacy ^
    --hidden-import websockets.legacy.client ^
    --hidden-import customtkinter ^
    --hidden-import pythonosc ^
    --hidden-import pythonosc.osc_server ^
    --hidden-import pythonosc.dispatcher ^
    --hidden-import pydglab_ws ^
    --collect-all customtkinter ^
    --collect-all pydglab_ws ^
    --collect-all pythonosc ^
    main.py

echo.
if exist "dist\芝士郊狼控制软件.exe" (
    echo === 构建成功! ===
    echo EXE 位置: dist\芝士郊狼控制软件.exe
    echo.
    echo 复制到项目根目录...
    copy "dist\芝士郊狼控制软件.exe" "." >nul
    echo 完成!
) else (
    echo === 构建失败，请检查错误信息 ===
)
echo.
pause
