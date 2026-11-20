# NetMonitor Pro + DAFAN Python Tool

This project contains the NetMonitor Pro Android app and the DAFAN Python tool.

## DAFAN Python Tool

The repository root contains `DAFAN_TOOL.py`.

The Android app has a **DAFAN Python Tool** button. It exports the script to `Downloads/DAFAN_TOOL.py` and tries to open it with Termux.

For the original tool to run correctly, Termux must have Python and the tool's dependencies installed. The tool also expects the Lua executables `luac5.3` / `luadec` for Lua compilation/decompilation.

The packaged copy has Telegram notifications disabled.

## GitHub Actions

The workflow is:

`.github/workflows/build.yml`

It builds:

`app/build/outputs/apk/debug/app-debug.apk`
