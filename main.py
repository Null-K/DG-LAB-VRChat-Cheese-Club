#!/usr/bin/env python3
"""芝士郊狼控制软件 - Cheese DGLAB Controller"""

import os
import sys

# Enable high DPI awareness before tkinter loads
if sys.platform == "win32":
    try:
        import ctypes
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass

# Force matplotlib to use TkAgg backend before any matplotlib import
os.environ["MPLBACKEND"] = "TkAgg"
os.environ["QT_QPA_PLATFORM"] = "offscreen"
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei UI', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def _kill_old_instances():
    """Kill any already-running instances of this EXE (avoid accumulating orphans)."""
    import subprocess, re
    my_pid = str(os.getpid())
    try:
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq 芝士郊狼控制软件*.exe", "/FO", "CSV"],
            capture_output=True, text=True, timeout=5,
        )
        for line in result.stdout.strip().split("\n")[1:]:
            pid_match = re.search(r'"(\d+)"', line)
            if pid_match:
                pid = pid_match.group(1)
                if pid == my_pid:
                    continue  # 补药自杀
                subprocess.run(["taskkill", "/F", "/PID", pid],
                             capture_output=True, timeout=3)
    except Exception:
        pass


def main():
    _kill_old_instances()
    try:
        from app import App
        app = App()
        app.run()
    except SystemExit:
        raise  # Let sys.exit() pass through

    except ImportError as e:
        print(f"缺少依赖库: {e}")
        print("请运行: pip install -r requirements.txt")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n已退出")


if __name__ == "__main__":
    main()
