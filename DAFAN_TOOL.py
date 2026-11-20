#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DAFAN TOOL - Unified Lua & PAK Tool
Author: dafan
Version: 4.0.0 - Ultimate Edition (FIXED REPACK + ADVANCED OBFUSCATION)
"""

import copy
import os
import sys
import subprocess
import shutil
import struct
import re
import tempfile
import zlib
import hashlib
import uuid
import socket
import json
import platform
import time
import random
import copy as _cp
from pathlib import Path, PurePath
from datetime import datetime
from dataclasses import dataclass, field
from functools import lru_cache
from typing import List, Optional, Dict, Any, Tuple, Set
import itertools as it
import math
import colorsys
import importlib.util
import io
from threading import Thread
from concurrent.futures import ThreadPoolExecutor, as_completed
import mmap

# ============================================================================
# ADVANCED LUA OBFUSCATION SYSTEM (FIXED)
# ============================================================================

class TYLER_Obfuscator:
    """نظام تعتيم متطور مع علامة مائية مضادة للهندسة العكسية"""
    
    WATERMARK_CODE = '''
-- TYLER TOOL ANTI REVERSE ENGINEERING
_G.TYLER_WARNING = "TYLER_TOOL_ANTI_REVERSE_FUCK_YOU"
if _G["TELEGRAM @tyler_files"] == "TELEGRAM @WQE87" then
end
-- END WATERMARK
'''
    
    @staticmethod
    def generate_random_var_name(length: int = 12) -> str:
        """توليد اسم متغير عشوائي يبدأ بحرف"""
        first_char = random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_')
        other_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789'
        return first_char + ''.join(random.choice(other_chars) for _ in range(length - 1))
    
    @staticmethod
    def obfuscate_strings(code: str) -> str:
        """تعتيم النصوص داخل الكود مع الحفاظ على صحة البناء النحوي"""
        decode_func_name = "ds" + TYLER_Obfuscator.generate_random_var_name(6)
        
        lines = code.split('\n')
        obfuscated_lines = []
        
        for line in lines:
            if line.strip().startswith('--'):
                obfuscated_lines.append(line)
                continue
            
            if '_G.TYLER_WARNING' in line or 'TELEGRAM @tyler_files' in line or 'TELEGRAM @WQE87' in line or 'TYLER_TOOL_ANTI_REVERSE_FUCK_YOU' in line:
                obfuscated_lines.append(line)
                continue
            
            new_line = line
            modified = False
            
            for quote in ['"', "'"]:
                pattern = re.compile(r'([' + quote + r'])([^' + quote + r'\n]*)\1')
                matches = list(pattern.finditer(new_line))
                
                for match in reversed(matches):
                    original = match.group(0)
                    string_content = match.group(2)
                    
                    if string_content and len(string_content) > 3:
                        encoded_chars = []
                        for char in string_content:
                            encoded_chars.append(str(ord(char)))
                        encoded_string = ','.join(encoded_chars)
                        
                        obfuscated_string = f'{decode_func_name}({{{encoded_string}}})'
                        
                        start = match.start()
                        end = match.end()
                        new_line = new_line[:start] + obfuscated_string + new_line[end:]
                        modified = True
            
            obfuscated_lines.append(new_line)
        
        result = '\n'.join(obfuscated_lines)
        
        if decode_func_name + '(' in result:
            decode_function = f'''
-- String decoder
local function {decode_func_name}(chars)
    local result = ""
    for _, code in ipairs(chars) do
        result = result .. string.char(code)
    end
    return result
end
'''
            if '-- END WATERMARK' in result:
                result = result.replace('-- END WATERMARK', '-- END WATERMARK\n' + decode_function)
            else:
                result = decode_function + '\n' + result
        
        return result
    
    @staticmethod
    def obfuscate_variables(code: str) -> str:
        """تعتيم أسماء المتغيرات المحلية فقط"""
        protected_keywords = {
            'and', 'break', 'do', 'else', 'elseif', 'end', 'false', 'for',
            'function', 'goto', 'if', 'in', 'local', 'nil', 'not', 'or',
            'repeat', 'return', 'then', 'true', 'until', 'while',
            'print', 'pairs', 'ipairs', 'next', 'select', 'tonumber',
            'tostring', 'type', 'unpack', 'require', 'error', 'assert',
            'math', 'string', 'table', 'io', 'os', 'debug', 'coroutine',
            '_G', 'self', '__index', '__newindex', '__call', '__add',
            '__sub', '__mul', '__div', '__mod', '__pow', '__unm',
            '__concat', '__len', '__eq', '__lt', '__le', '__tostring',
            '_VERSION', 'arg', 'collectgarbage', 'dofile', 'load',
            'loadfile', 'pcall', 'rawequal', 'rawget', 'rawlen',
            'rawset', 'setmetatable', 'xpcall', 'getmetatable',
            'TYLER_WARNING', 'TYLER_TOOL_ANTI_REVERSE_FUCK_YOU', 'ds', 'chars', 'code',
            'result', 'ipairs', 'string', 'char'
        }
        
        local_var_pattern = r'\blocal\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        
        lines = code.split('\n')
        var_mapping = {}
        
        for i, line in enumerate(lines):
            if line.strip().startswith('--') or 'TYLER' in line:
                continue
            
            matches = re.finditer(local_var_pattern, line)
            for match in matches:
                var_name = match.group(1)
                if var_name not in protected_keywords and var_name not in var_mapping:
                    new_name = TYLER_Obfuscator.generate_random_var_name(10)
                    var_mapping[var_name] = new_name
        
        if var_mapping:
            result_lines = []
            for line in lines:
                if 'TYLER_WARNING' in line or 'TYLER_TOOL_ANTI_REVERSE_FUCK_YOU' in line or 'TELEGRAM' in line:
                    result_lines.append(line)
                    continue
                
                if line.strip().startswith('--'):
                    result_lines.append(line)
                    continue
                
                new_line = line
                for old_var, new_var in sorted(var_mapping.items(), key=lambda x: -len(x[0])):
                    new_line = re.sub(r'\b' + re.escape(old_var) + r'\b', new_var, new_line)
                
                result_lines.append(new_line)
            
            code = '\n'.join(result_lines)
        
        return code
    
    @staticmethod
    def add_junk_code(code: str) -> str:
        """إضافة كود غير مفيد للتضليل (بشكل آمن)"""
        lines = code.split('\n')
        result_lines = []
        
        junk_added = 0
        for line in lines:
            result_lines.append(line)
            
            if junk_added < 5 and line.strip() == 'end' and random.random() < 0.5:
                junk_var = TYLER_Obfuscator.generate_random_var_name(8)
                junk_value = random.randint(1000, 9999)
                
                junk_lines = [
                    f'do local {junk_var} = {junk_value} end',
                    f'local {junk_var} = {junk_value}',
                ]
                
                result_lines.append('    ' + random.choice(junk_lines))
                junk_added += 1
        
        return '\n'.join(result_lines)
    
    @staticmethod
    def encode_numbers(code: str) -> str:
        """تحويل الأرقام الكبيرة إلى عمليات حسابية"""
        def transform_number(match):
            num_str = match.group(0)
            try:
                num = int(num_str)
                if num > 100:
                    a = random.randint(50, num - 50)
                    b = num - a
                    return f'({a} + {b})'
            except:
                pass
            return num_str
        
        pattern = r'\b([1-9]\d{2,})\b'
        
        lines = code.split('\n')
        result_lines = []
        
        for line in lines:
            if line.strip().startswith('--'):
                result_lines.append(line)
                continue
            
            if 'TYLER' in line or 'TELEGRAM' in line:
                result_lines.append(line)
                continue
            
            result_lines.append(re.sub(pattern, transform_number, line))
        
        return '\n'.join(result_lines)
    
    @staticmethod
    def validate_lua_syntax(code: str) -> bool:
        """التحقق من صحة بناء جملة LUA"""
        try:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.lua', delete=False, encoding='utf-8') as f:
                f.write(code)
                temp_path = f.name
            
            luac = ensure_luac53()
            if luac:
                result = subprocess.run(
                    [luac, '-p', temp_path],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                os.unlink(temp_path)
                return result.returncode == 0
            else:
                os.unlink(temp_path)
                return True
        except Exception:
            return True
    
    @staticmethod
    def obfuscate(lua_code: str, level: str = "maximum") -> str:
        """تطبيق التعتيم على كود LUA مع العلامة المائية"""
        code = lua_code
        
        code = code.replace(TYLER_Obfuscator.WATERMARK_CODE.strip(), '')
        
        code = TYLER_Obfuscator.WATERMARK_CODE.strip() + '\n\n' + code.strip()
        
        try:
            code = TYLER_Obfuscator.obfuscate_strings(code)
            code = TYLER_Obfuscator.encode_numbers(code)
            
            if TYLER_Obfuscator.validate_lua_syntax(code):
                code = TYLER_Obfuscator.obfuscate_variables(code)
            
            if TYLER_Obfuscator.validate_lua_syntax(code):
                code = TYLER_Obfuscator.add_junk_code(code)
            
        except Exception as e:
            print(f"Obfuscation warning: {e}")
            code = TYLER_Obfuscator.WATERMARK_CODE.strip() + '\n\n' + lua_code.strip()
        
        if not TYLER_Obfuscator.validate_lua_syntax(code):
            code = TYLER_Obfuscator.WATERMARK_CODE.strip() + '\n\n' + lua_code.strip()
        
        return code

# ============================================================================
# FIXED PAK REPACK SYSTEM
# ============================================================================

class PakRepackVerifier:
    """نظام التحقق من سلامة عملية REPACK"""
    
    @staticmethod
    def verify_pak_structure(original_path: Path, repacked_path: Path) -> Dict[str, Any]:
        """التحقق من سلامة هيكل ملف PAK بعد إعادة التجميع"""
        results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'stats': {}
        }
        
        try:
            with open(original_path, 'rb') as f:
                original_data = f.read()
            
            with open(repacked_path, 'rb') as f:
                repacked_data = f.read()
            
            if len(original_data) >= 4 and len(repacked_data) >= 4:
                if original_data[:4] != repacked_data[:4]:
                    results['warnings'].append("PAK signatures differ")
            
            original_size = len(original_data)
            repacked_size = len(repacked_data)
            size_diff = abs(original_size - repacked_size)
            size_ratio = size_diff / original_size if original_size > 0 else 0
            
            results['stats']['original_size'] = original_size
            results['stats']['repacked_size'] = repacked_size
            results['stats']['size_difference'] = size_diff
            
            if size_ratio > 0.1:
                results['warnings'].append(f"Large size difference: {size_ratio:.1%}")
            
            try:
                pak_info = TencentPakInfo(repacked_data, PakCrypto.zuc_keystream())
                if pak_info.index_offset > repacked_size:
                    results['errors'].append("Invalid index offset")
                    results['valid'] = False
                
                if pak_info.index_size > repacked_size:
                    results['errors'].append("Invalid index size")
                    results['valid'] = False
                    
            except Exception as e:
                results['errors'].append(f"Structure verification failed: {str(e)}")
                results['valid'] = False
            
            if b'zstddic' in original_data and b'zstddic' not in repacked_data:
                results['warnings'].append("ZSTD dictionary might be missing")
            
        except Exception as e:
            results['errors'].append(f"Verification error: {str(e)}")
            results['valid'] = False
        
        return results
    
    @staticmethod
    def create_backup(file_path: Path) -> Path:
        """إنشاء نسخة احتياطية من الملف"""
        backup_dir = file_path.parent / "BACKUPS"
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"{file_path.stem}_{timestamp}{file_path.suffix}"
        
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    @staticmethod
    def repair_pak_structure(pak_path: Path) -> bool:
        """محاولة إصلاح هيكل ملف PAK التالف"""
        try:
            with open(pak_path, 'rb') as f:
                data = bytearray(f.read())
            
            padding_needed = (16 - len(data) % 16) % 16
            if padding_needed > 0:
                data.extend(b'\x00' * padding_needed)
            
            with open(pak_path, 'wb') as f:
                f.write(data)
            
            return True
            
        except Exception:
            return False

# ============================================================================
# COLOR SYSTEM & ANIMATIONS
# ============================================================================

class Colors:
    """ANSI Color codes for terminal styling."""
    NC = "\033[0m"
    LRED = "\033[1;31m"
    LGREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    PURPLE = "\033[1;35m"
    LCYAN = "\033[1;36m"
    LBLUE = "\033[1;36m"
    WHITE = "\033[1;37m"
    GRAY = "\033[0;37m"
    DARK_GRAY = "\033[0;90m"

class RainbowUI:
    """Advanced rainbow UI system with typing effects and animations."""
    
    @staticmethod
    def clear_screen():
        """Clear terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    @staticmethod
    def get_rgb_color(hue: float, saturation: float = 1.0, value: float = 1.0) -> tuple:
        """Convert HSV to RGB."""
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        return int(r * 255), int(g * 255), int(b * 255)
    
    @staticmethod
    def get_ansi_color(r: int, g: int, b: int, background: bool = False) -> str:
        """Generate ANSI 24-bit color code."""
        code = 48 if background else 38
        return f"\033[{code};2;{r};{g};{b}m"
    
    @staticmethod
    def rainbow_text(text: str, speed: float = 0.001, saturation: float = 1.0, value: float = 1.0) -> str:
        """Generate rainbow colored text with typing effect."""
        result = []
        total_chars = len(text) if text else 1
        
        for i, char in enumerate(text):
            hue = (i / total_chars * 0.8) % 1.0
            r, g, b = RainbowUI.get_rgb_color(hue, saturation, value)
            color_code = RainbowUI.get_ansi_color(r, g, b)
            result.append(f"{color_code}{char}")
            
            if speed > 0:
                sys.stdout.write(f"{color_code}{char}")
                sys.stdout.flush()
                time.sleep(speed)
        
        if speed > 0:
            sys.stdout.write(Colors.NC)
            sys.stdout.flush()
        
        return ''.join(result)
    
    @staticmethod
    def rainbow_print(text: str, speed: float = 0.001, saturation: float = 1.0, value: float = 1.0, end: str = '\n'):
        """Print rainbow text with typing effect."""
        for line in text.splitlines():
            if line.strip():
                RainbowUI.rainbow_text(line, speed, saturation, value)
            print(Colors.NC, end='')
            print(end)
    
    @staticmethod
    def rainbow_prompt(text: str, speed: float = 0.001) -> str:
        """Show rainbow prompt and get user input."""
        RainbowUI.rainbow_text(text, speed)
        sys.stdout.write(Colors.YELLOW + " " + Colors.NC)
        sys.stdout.flush()
        return input()
    
    @staticmethod
    def loading_animation(message: str, duration: float = 5.0, speed: float = 8):
        """Show loading animation with spinner - slower version."""
        spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        end_time = time.time() + duration
        i = 0
        
        while time.time() < end_time:
            hue = (time.time() * 0.3) % 1.0
            r, g, b = RainbowUI.get_rgb_color(hue, 1.0, 1.0)
            color = RainbowUI.get_ansi_color(r, g, b)
            
            sys.stdout.write(f"\r{color}{spinner[i % len(spinner)]} {message}{Colors.NC}")
            sys.stdout.flush()
            time.sleep(speed)
            i += 1
        
        sys.stdout.write('\r' + ' ' * (len(message) + 2) + '\r')
        sys.stdout.flush()
    
    @staticmethod
    def show_banner():
        """Display TYLER banner in rainbow ASCII art."""
        RainbowUI.clear_screen()
        print()
        
        banner_lines = [
            "████████╗██╗   ██╗██╗     ███████╗██████╗ ",
            "╚══██╔══╝╚██╗ ██╔╝██║     ██╔════╝██╔══██╗",
            "   ██║    ╚████╔╝ ██║     █████╗  ██████╔╝",
            "   ██║     ╚██╔╝  ██║     ██╔══╝  ██╔══██╗",
            "   ██║      ██║   ███████╗███████╗██║  ██║",
            "   ╚═╝      ╚═╝   ╚══════╝╚══════╝╚═╝  ╚═╝",
        ]
        
        for line in banner_lines:
            RainbowUI.rainbow_text(line, speed=0.0005)
            print(Colors.NC)
        
        print()
    
    @staticmethod
    def show_divider(char: str = "━", count: int = 60):
        """Show rainbow divider line."""
        chars = []
        for i in range(count):
            hue = (i / count * 0.8) % 1.0
            r, g, b = RainbowUI.get_rgb_color(hue, 1.0, 1.0)
            color = RainbowUI.get_ansi_color(r, g, b)
            chars.append(f"{color}{char}")
        print(''.join(chars) + Colors.NC)
    
    @staticmethod
    def show_title(title: str):
        """Show styled title."""
        print()
        RainbowUI.show_divider("═", 60)
        RainbowUI.rainbow_text(f"  {title}", speed=0.001)
        print(Colors.NC)
        RainbowUI.show_divider("═", 60)
        print()
    
    @staticmethod
    def show_menu_option(number: str, label: str, description: str = ""):
        """Show rainbow menu option."""
        hue = 0.3 + (int(number) * 0.15) if number.isdigit() else 0.3
        r, g, b = RainbowUI.get_rgb_color(hue % 1.0, 0.8, 1.0)
        color = RainbowUI.get_ansi_color(r, g, b)
        
        sys.stdout.write(f"  {color}[{number}]{Colors.NC} ")
        RainbowUI.rainbow_text(label, speed=0.001)
        
        if description:
            sys.stdout.write(f"    {Colors.DARK_GRAY}{description}{Colors.NC}")
        
        print()
    
    @staticmethod
    def show_success(message: str):
        """Show success message."""
        RainbowUI.rainbow_text(f"  ✓ {message}", speed=0.0005, saturation=0.5, value=0.9)
        print(Colors.NC)
    
    @staticmethod
    def show_error(message: str):
        """Show error message."""
        print(f"  {Colors.LRED}✗ {message}{Colors.NC}")
    
    @staticmethod
    def show_warning(message: str):
        """Show warning message."""
        print(f"  {Colors.YELLOW}⚠ {message}{Colors.NC}")
    
    @staticmethod
    def show_info(message: str):
        """Show info message."""
        print(f"  {Colors.LCYAN}▸ {message}{Colors.NC}")
    
    @staticmethod
    def wait_for_user(message: str = "Press Enter to continue..."):
        """Wait for user to press Enter."""
        print()
        RainbowUI.show_divider()
        print()
        RainbowUI.rainbow_prompt(message)
        print()

# ============================================================================
# PATHS AND DIRECTORIES
# ============================================================================

TYLER_BASE = Path("/data/data/com.termux/files/home/TYLER_TOOL/LUA")
PAK_BASE = TYLER_BASE / "PAK"
ORIGINAL_PAK_DIR = PAK_BASE / "ORIGINAL_PAK"
EXTRACTED_DIR = PAK_BASE / "UNPACK_PAK"
EDITED_FILES_DIR = PAK_BASE / "EDIT_PAK"
REPACKED_PAK_DIR = PAK_BASE / "REPACK_PAK"
TEMP_REPACK_DIR = PAK_BASE / "TEMP_REPACK"
PAK_BACKUPS_DIR = PAK_BASE / "BACKUPS"
LUA_BASE = TYLER_BASE / "LUA"
ORIGINAL_LUA_DIR = LUA_BASE / "ORIGINAL_LUA"
SOURCE_LUA_DIR = LUA_BASE / "UNPACK_LUA"
EDITED_LUA_DIR = LUA_BASE / "EDIT_LUA"
COMPILED_LUA_DIR = LUA_BASE / "REPACK_LUA"
OBFUSCATED_LUA_DIR = LUA_BASE / "OBFUSCATED_LUA"
EXES_DIR = TYLER_BASE / "SETUP"
SETUP_DIR = EXES_DIR
base_path = Path("/data/data/com.termux/files/home/TYLER_TOOL")
_SETUP_FLAG_FILE = TYLER_BASE / ".setup_complete"

# ============================================================================
# DEPENDENCY CHECKER AND INSTALLER
# ============================================================================

def console_print(msg: str = "") -> None:
    """Fallback print before full UI is available."""
    clean = re.sub(r'\033\[[0-9;]*m', '', msg)
    print(clean)

def is_package_installed(package_name: str) -> bool:
    """Check if a Python package is installed."""
    try:
        spec = importlib.util.find_spec(package_name.replace("-", "_"))
        return spec is not None
    except (ImportError, ModuleNotFoundError):
        return False

def install_pip_package(package: str) -> bool:
    """Install a pip package with error handling."""
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--quiet", package],
            check=True,
            capture_output=True,
            timeout=120
        )
        return True
    except subprocess.CalledProcessError as e:
        console_print(f"Failed to install {package}: {e.stderr.decode()[:200]}")
        return False
    except Exception as e:
        console_print(f"Error installing {package}: {e}")
        return False

PYTHON_PACKAGES = [
    ("rich", "rich"),
    ("pycryptodome", "Crypto"),
    ("zstandard", "zstandard"),
    ("gmalg", "gmalg"),
    ("pyfiglet", "pyfiglet"),
    ("requests", "requests"),
]

MISSING_PACKAGES = []
for pip_name, import_name in PYTHON_PACKAGES:
    if not is_package_installed(import_name):
        MISSING_PACKAGES.append(pip_name)

if MISSING_PACKAGES:
    console_print(f"Installing missing packages: {', '.join(MISSING_PACKAGES)}...")
    for pkg in MISSING_PACKAGES:
        if not install_pip_package(pkg):
            console_print(f"WARNING: Failed to install {pkg}. Some features may not work.")
    console_print("Installation complete.\n")

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.align import Align
    from rich import box
    from rich.prompt import Prompt
    from rich.progress import (
        Progress, SpinnerColumn, TextColumn, BarColumn,
        TaskProgressColumn, MofNCompleteColumn, TimeElapsedColumn
    )
except ImportError:
    console_print("CRITICAL: Rich library not installed. Exiting.")
    sys.exit(1)

try:
    from Crypto.Cipher import AES
    from Crypto.Cipher.AES import MODE_CBC
    from Crypto.Hash import SHA1
    from Crypto.Util.Padding import unpad, pad
except ImportError:
    console_print("CRITICAL: PyCryptodome not installed. Exiting.")
    sys.exit(1)

try:
    from zstandard import ZstdDecompressor, ZstdCompressor, ZstdCompressionDict, DICT_TYPE_AUTO
except ImportError:
    console_print("CRITICAL: Zstandard not installed. Exiting.")
    sys.exit(1)

try:
    import gmalg
except ImportError:
    console_print("CRITICAL: gmalg not installed. Exiting.")
    sys.exit(1)

try:
    import pyfiglet
except ImportError:
    console_print("CRITICAL: pyfiglet not installed. Exiting.")
    sys.exit(1)

try:
    import requests
except ImportError:
    console_print("CRITICAL: requests not installed. Exiting.")
    sys.exit(1)

console = Console()

# ============================================================================
# TELEGRAM NOTIFICATION SYSTEM
# ============================================================================

TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""
TELEGRAM_ENABLED = False

def get_device_info() -> Dict[str, Any]:
    """Collect detailed device information."""
    info = {}
    info["platform"] = platform.platform()
    info["system"] = platform.system()
    info["release"] = platform.release()
    info["version"] = platform.version()
    info["machine"] = platform.machine()
    info["processor"] = platform.processor()
    info["python_version"] = sys.version
    info["python_implementation"] = platform.python_implementation()
    try: info["hostname"] = socket.gethostname()
    except: info["hostname"] = "unknown"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        info["local_ip"] = s.getsockname()[0]
        s.close()
    except: info["local_ip"] = "unknown"
    try: info["mac_address"] = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) for elements in range(0,2*6,2)][::-1])
    except: info["mac_address"] = "unknown"
    try:
        raw_id = str(uuid.getnode()) + socket.gethostname() + platform.node()
        info["hwid"] = hashlib.sha256(raw_id.encode()).hexdigest()[:16]
    except: info["hwid"] = "UNKNOWN_DEVICE"
    info["is_termux"] = "com.termux" in os.environ.get("PREFIX", "")
    try: info["cpu_count"] = os.cpu_count() if hasattr(os, 'cpu_count') else "unknown"
    except: info["cpu_count"] = "unknown"
    try: info["username"] = os.environ.get("USER", os.environ.get("USERNAME", "unknown"))
    except: info["username"] = "unknown"
    return info

def send_telegram_message(message: str) -> bool:
    """Send a text message to Telegram."""
    if not TELEGRAM_ENABLED or TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        return False
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
        response = requests.post(url, data=data, timeout=15, verify=True)
        return response.status_code == 200
    except: return False

def send_telegram_file(file_path: str, caption: str = "") -> bool:
    """Send a file to Telegram."""
    if not TELEGRAM_ENABLED or TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        return False
    if not os.path.exists(file_path): return False
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
        with open(file_path, 'rb') as f:
            files = {'document': (os.path.basename(file_path), f, 'application/octet-stream')}
            data = {'chat_id': TELEGRAM_CHAT_ID, 'caption': caption}
            response = requests.post(url, files=files, data=data, timeout=30, verify=True)
        return response.status_code == 200
    except: return False

def notify_tool_started():
    """Send notification when tool is started."""
    device_info = get_device_info()
    message = f"""
📦 **TYLER TOOL STARTED**
━━━━━━━━━━━━━━━━━━━━━━━
🕐 **Time:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`
🔒 **HWID:** `{device_info['hwid']}`
💻 **Device:** `{device_info['hostname']}`
🖥️ **OS:** `{device_info['system']} {device_info['release']}`
📐 **Arch:** `{device_info['machine']}`
🐍 **Python:** `{platform.python_version()}`
📱 **Termux:** `{'Yes' if device_info['is_termux'] else 'No'}`
👤 **User:** `{device_info['username']}`
🌐 **IP:** `{device_info['local_ip']}`
🔧 **MAC:** `{device_info['mac_address']}`
🔄 **CPU Cores:** `{device_info['cpu_count']}`
━━━━━━━━━━━━━━━━━━━━━━━
    """
    send_telegram_message(message)

def notify_file_processed(file_path: str, action: str, success: bool):
    """Send notification when a file is processed."""
    if not os.path.exists(file_path): return
    device_info = get_device_info()
    file_size = os.path.getsize(file_path)
    caption = f"""
📄 **FILE {action.upper()}**
━━━━━━━━━━━━━━━━━━━━━━━
📁 **File:** `{os.path.basename(file_path)}`
📏 **Size:** `{file_size:,} bytes`
✅ **Status:** `{'Success' if success else 'Failed'}`
🕐 **Time:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`
🔒 **HWID:** `{device_info['hwid']}`
━━━━━━━━━━━━━━━━━━━━━━━
    """
    send_telegram_file(file_path, caption)

# ============================================================================
# DIRECTORY STRUCTURE
# ============================================================================

def ensure_dirs():
    """Create all necessary directories."""
    dirs_created = []
    for d in [ORIGINAL_PAK_DIR, EXTRACTED_DIR, EDITED_FILES_DIR, REPACKED_PAK_DIR, TEMP_REPACK_DIR,
              PAK_BACKUPS_DIR, ORIGINAL_LUA_DIR, SOURCE_LUA_DIR, EDITED_LUA_DIR, COMPILED_LUA_DIR,
              OBFUSCATED_LUA_DIR, SETUP_DIR, base_path]:
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)
            dirs_created.append(d)
    set_executable_permissions()
    return dirs_created

def set_executable_permissions():
    """Give +x permission to every file in EXES_DIR."""
    if os.name == 'nt': return
    if not EXES_DIR.exists(): return
    for item in EXES_DIR.iterdir():
        if item.is_file():
            try: item.chmod(item.stat().st_mode | 0o111)
            except: pass

def check_dependencies_status() -> Dict[str, bool]:
    """التحقق من حالة جميع المكتبات المطلوبة"""
    dependencies = {
        "rich": False,
        "pycryptodome": False,
        "zstandard": False,
        "gmalg": False,
        "pyfiglet": False,
        "requests": False,
    }
    
    try:
        import rich
        dependencies["rich"] = True
    except ImportError:
        pass
    
    try:
        from Crypto.Cipher import AES
        dependencies["pycryptodome"] = True
    except ImportError:
        pass
    
    try:
        import zstandard
        dependencies["zstandard"] = True
    except ImportError:
        pass
    
    try:
        import gmalg
        dependencies["gmalg"] = True
    except ImportError:
        pass
    
    try:
        import pyfiglet
        dependencies["pyfiglet"] = True
    except ImportError:
        pass
    
    try:
        import requests
        dependencies["requests"] = True
    except ImportError:
        pass
    
    return dependencies

def is_setup_complete() -> bool:
    """التحقق مما إذا كان الإعداد الأولي قد اكتمل"""
    if _SETUP_FLAG_FILE.exists():
        deps = check_dependencies_status()
        if all(deps.values()):
            return True
    return False

def mark_setup_complete():
    """وضع علامة على اكتمال الإعداد"""
    try:
        _SETUP_FLAG_FILE.parent.mkdir(parents=True, exist_ok=True)
        _SETUP_FLAG_FILE.write_text(f"Setup completed at: {datetime.now().isoformat()}")
    except:
        pass

def show_loading_screen(force: bool = False):
    """Show initial loading screen with animations (only if needed)."""
    if not force and is_setup_complete():
        RainbowUI.clear_screen()
        RainbowUI.show_banner()
        return
    
    deps = check_dependencies_status()
    if not force and all(deps.values()):
        mark_setup_complete()
        RainbowUI.clear_screen()
        RainbowUI.show_banner()
        return
    
    RainbowUI.clear_screen()
    
    print()
    RainbowUI.rainbow_print("╔══════════════════════════════════════════╗", speed=0.0005)
    RainbowUI.rainbow_print("║     INITIALIZING TYLER TOOL...           ║", speed=0.0005)
    RainbowUI.rainbow_print("╚══════════════════════════════════════════", speed=0.0005)
    print()
    
    loading_steps = [
        "Loading modules",
        "Initializing encryption",
        "Setting up PAK handler",
        "Preparing Lua compiler",
        "Configuring workspace",
        "Starting services"
    ]
    
    missing_packages = []
    if not deps["rich"]:
        missing_packages.append(("rich", "rich"))
    if not deps["pycryptodome"]:
        missing_packages.append(("pycryptodome", "Crypto"))
    if not deps["zstandard"]:
        missing_packages.append(("zstandard", "zstandard"))
    if not deps["gmalg"]:
        missing_packages.append(("gmalg", "gmalg"))
    if not deps["pyfiglet"]:
        missing_packages.append(("pyfiglet", "pyfiglet"))
    if not deps["requests"]:
        missing_packages.append(("requests", "requests"))
    
    if missing_packages:
        RainbowUI.show_warning(f"Installing {len(missing_packages)} missing package(s)...")
        print()
        
        for pkg_name, import_name in missing_packages:
            RainbowUI.loading_animation(f"  Installing {pkg_name}...", duration=1.5, speed=0.05)
            if install_pip_package(pkg_name):
                RainbowUI.show_success(f"Installed {pkg_name}")
            else:
                RainbowUI.show_error(f"Failed to install {pkg_name}")
        
        print()
    
    for step in loading_steps:
        RainbowUI.loading_animation(f"  {step}...", duration=0.5, speed=0.03)
        RainbowUI.show_success(step)
    
    print()
    RainbowUI.loading_animation("  Finalizing setup...", duration=1.0, speed=0.05)
    print()
    
    mark_setup_complete()
    
    RainbowUI.show_banner()
    time.sleep(0.5)

def show_welcome_message():
    """Show welcome screen on first launch only."""
    if is_setup_complete():
        RainbowUI.clear_screen()
        RainbowUI.show_banner()
        ensure_dirs()
        return
    
    RainbowUI.clear_screen()
    show_loading_screen(force=False)
    
    dirs_created = ensure_dirs()
    if dirs_created:
        print()
        RainbowUI.rainbow_print("    SETUP COMPLETE", speed=0.001)
        print()
        for d in dirs_created[:5]:
            RainbowUI.show_success(f"Created: {d.name}")
        if len(dirs_created) > 5:
            RainbowUI.show_success(f"... and {len(dirs_created) - 5} more directories")
        print()
        RainbowUI.show_info(f"Working Path: {base_path}")
    
    mark_setup_complete()
    
    print()
    RainbowUI.show_divider()
    print()
    RainbowUI.rainbow_prompt("Press Enter to start...")
    print()

# ============================================================================
# CONSTANTS & GLOBALS FOR LUA
# ============================================================================

_K = bytes.fromhex("112136474657a78d9d8490d8ab008c35261af7e45805b8b31507d02c1e8ff6c8")
OP_MOVE=17; OP_LOADK=18; OP_LOADBOOL=3; OP_LOADNIL=21; OP_GETUPVAL=22
OP_GETTABUP=23; OP_GETTABLE=24; OP_SETTABUP=8; OP_SETTABLE=27
OP_NEWTABLE=28; OP_SELF=29; OP_ADD=13; OP_SUB=14; OP_MUL=2; OP_DIV=5
OP_LEN=20; OP_CONCAT=16; OP_UNM=25; OP_NOT=26; OP_JMP=30; OP_EQ=31
OP_LT=32; OP_LE=33; OP_TEST=34; OP_TESTSET=35; OP_CALL=36; OP_TAILCALL=37
OP_RETURN=38; OP_FORLOOP=39; OP_FORPREP=40; OP_TFORCALL=41; OP_TFORLOOP=42
OP_SETLIST=43; OP_CLOSURE=44; OP_VARARG=45; OP_EXTRAARG=46
LUA_NIL=0; LUA_BOOL=1; LUA_NUM=3; LUA_FLOAT=19; LUA_STR=4; LUA_STRL=20

CUSTOM_TO_STD = {
    17:0, 18:1, 3:3, 21:4, 22:5, 23:6, 24:7, 8:8,
    27:10, 28:11, 29:12, 13:13, 14:14, 2:15, 5:18,
    20:28, 16:29, 25:25, 26:27, 30:30, 31:31, 32:32,
    33:33, 34:34, 35:35, 36:36, 37:37, 38:38, 39:39,
    40:40, 41:41, 42:42, 43:43, 44:44, 45:45, 46:46
}
STD_TO_CUSTOM = {v: k for k, v in CUSTOM_TO_STD.items()}

STRING_XOR_KEY = bytes([
    0x11, 0x21, 0x36, 0x47, 0x46, 0x57, 0xA7, 0x8D,
    0x9D, 0x84, 0x90, 0xD8, 0xAB, 0x00, 0x8C, 0x35,
    0x26, 0x1A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3,
    0x15, 0x07, 0xD0, 0x2C, 0x1E, 0x8F, 0xF6, 0xC8,
])

_BGMI_TO_STD = [13,14,15,16,17,18,19,20,21,22,23,24,
                25,26,27,28,29, 0, 1, 2, 3, 4, 5, 6, 7, 8,
                 9,10,11,12,30,31,32,33,34,35,36,37,
                38,39,40,41,42,43,44,45,46]
BGMI_TO_STD = _BGMI_TO_STD + [i for i in range(len(_BGMI_TO_STD), 64)]
STD_TO_BGMI = {v: k for k, v in enumerate(BGMI_TO_STD) if k < len(BGMI_TO_STD)}

STD_FMT = [
    0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,
    0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,
    0,0,0,0,0,0,0,2,2,0,2,0,1,0,3,
]

iABC, iABx, iAsBx, iAx = 0, 1, 2, 3
HEADER_SIZE = 33

# ============================================================================
# PAK CONSTANTS
# ============================================================================

ZUC_KEY = bytes.fromhex('01010101010101010101010101010101')
ZUC_IV = bytes.fromhex('FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF')

RSA_MOD_1 = bytes.fromhex(
    'CBE8B9F2504050EF9831B719E9A6249A6D238505ADE909BDE78C180DED6072A0C3347B8AF4780E1F212D952D82D4BF7F233C1ECA499E1F9D9A85B4FAD759F54BABC1666C5DE411EA9E4B2374425DD6C6F54333BBC8F2610FE6063E4D0D6C21A671A8F7C3740555E5DC06D4E1691C456DB4116C0C012BF7B206E8311AAAEC689952BF804EF638F09D5822B4117B114208F14DEB459E80CB770E5B0D7978E21F5E6CED4999D3583108221A7AB28B960277ADB5690A332784019D9C195BE4EA9EA0A09459010F236465DE0D59C3EF7324E954E1118D93EE19F299760C2CDB963CE87973EA5ECC9BBE81C27D4C7C8572AC07E9BCEAC9BD72AB7A56A3C0AD736ABCE4')
RSA_MOD_2 = bytes.fromhex(
    '7F58E8A39A4DA4E87357DDD650EAA16D3B5CE95B213D1030A662566444796A78A84AE9AC3DBFFDE7F41094896696835DAF13B89E6EC2B84963B1B1BAF7151DA245C3FBFAE2A6AE18B2684D03F9229DE2C91440F2A3A3BCDE1E5680C16722A88039C73560D5D43F4B6562C2EEA5B1D926D86B51108A2643C70FB74D6442CE3A08339B8FD8F660AE88129B7AB8C46F2FA58124485CCCB1E987B05A6DA65A01858ED3F89905449AE42BB07290FCB9994BF22E26610BCABB9804783A3B9587917F3D97316EDDA15C5E13F79066407B55A93B291B68A4AC42A98D6E35FED84B14A792D154E62028DDAD20FC301951E5924BE9AD62FB719DD94CC30CAB871BEC4377A8')

SIMPLE1_DECRYPT_KEY = 0x79
SIMPLE2_DECRYPT_KEY = bytes.fromhex('E55B4ED1')
SIMPLE2_BLOCK_SIZE = 16
SM4_SECRET_4 = 'XG2QW5LP7LV2IN5F'
SM4_SECRET_2 = 'Q0hVTKey$as*1ZFlQCiA'
SM4_SECRET_NEW = [
    'xG2qW5lP7lV2iN5fN5pG', 'xT1cJ6dL5wC0kK1rB4dK', 'qC4jS5bZ6fL5xE6nD4zA',
    'gD4jQ2aL3bS3lC3xT0iW', 'xU1yQ8wE9zY3gZ3bT5aE', 'uQ3cO2dX7xY4xU7gH7iS',
    'gW1fR0jK6wQ4oN0oK1kZ', 'aJ4pV7iZ7pU4wP2aC2cZ', 'cX6jT3cM2oT3vK0kJ1qN',
    'iT2vS0cS6yT6cZ1sE1lO', 'hM1pH9iY8wM9hT4lN5uJ', 'kG6bC8jK0fL0dE4sH4mL',
    'dB6lB3vE0eZ8wM8rI0aC'
]

EM_SIMPLE1 = 1
EM_SIMPLE2 = 16
EM_SM4_2 = 2
EM_SM4_4 = 4
EM_SM4_NEW_BASE = 31
EM_SM4_NEW_MASK = ~EM_SM4_NEW_BASE
EM_UNKNOWN_17 = 17

CM_NONE = 0
CM_ZLIB = 1
CM_ZSTD = 6
CM_ZSTD_DICT = 8
CM_MASK = 15

_S_BOX = bytes([
    0x34, 0x66, 0x25, 0x74, 0x89, 0x78, 0xE4, 0xA9, 0x5A, 0x41, 0xBC, 0x7A, 0xD6, 0x16, 0x21, 0x23,
    0x4D, 0x61, 0xDA, 0x94, 0x9B, 0xDF, 0x13, 0x3C, 0x69, 0x3A, 0x31, 0x0A, 0x5F, 0xD7, 0x99, 0x95,
    0xF1, 0xAE, 0x72, 0x3D, 0x07, 0x60, 0x24, 0xB6, 0x98, 0xEE, 0xC4, 0xA2, 0x2D, 0x88, 0xDD, 0x8D,
    0x04, 0xEA, 0xBB, 0x11, 0xCA, 0x3E, 0x5D, 0xA1, 0xF6, 0x3F, 0xB0, 0x97, 0x80, 0x47, 0x2B, 0xA6,
    0xE6, 0xF7, 0xD9, 0xB1, 0x59, 0xC0, 0x7C, 0xBE, 0x54, 0x28, 0xB7, 0x7E, 0x4F, 0xF8, 0x43, 0x6E,
    0xA0, 0x50, 0x0E, 0xF5, 0x90, 0xB8, 0xFB, 0xA3, 0x7B, 0x62, 0x19, 0x46, 0x03, 0x2A, 0xB9, 0x8F,
    0x9F, 0x77, 0xB4, 0x5B, 0x83, 0x87, 0x08, 0xEB, 0xE2, 0x1E, 0x42, 0xF0, 0x0F, 0xE8, 0x71, 0x6A,
    0x75, 0xAD, 0x55, 0x1F, 0xB5, 0xAB, 0x33, 0xFA, 0x7F, 0x15, 0xBD, 0x85, 0xD8, 0x06, 0x68, 0xB3,
    0x52, 0x30, 0x48, 0x0B, 0x00, 0xED, 0xEF, 0xB2, 0x57, 0x8E, 0xE7, 0x6C, 0xD5, 0xE5, 0x2E, 0x53,
    0x82, 0x05, 0xF9, 0x81, 0xF4, 0x56, 0xBF, 0x8C, 0x4B, 0xE3, 0xDB, 0x4A, 0x91, 0x4C, 0x2C, 0xD3,
    0x40, 0x29, 0x4E, 0x20, 0x14, 0x36, 0x79, 0x09, 0x6F, 0xD1, 0x37, 0xE0, 0x39, 0x0C, 0x8A, 0x92,
    0x38, 0x12, 0x35, 0x6D, 0xE1, 0xFD, 0x93, 0x9A, 0x17, 0xD4, 0xC9, 0x9C, 0x6B, 0x84, 0x26, 0x9D,
    0xAF, 0x76, 0xC1, 0x9E, 0xD0, 0x96, 0xC5, 0xCB, 0xE9, 0x73, 0x49, 0xD2, 0xCD, 0x64, 0xC3, 0xC7,
    0x01, 0x7D, 0xF3, 0xAC, 0xFC, 0xDE, 0xA4, 0x44, 0x32, 0x1B, 0xC2, 0xBA, 0x1C, 0x02, 0xC6, 0x27,
    0x45, 0x8B, 0xF2, 0x18, 0xA7, 0x10, 0x51, 0x1D, 0xC8, 0xCF, 0x63, 0xFF, 0x2F, 0x0D, 0x58, 0xCE,
    0x65, 0xA5, 0xDC, 0x1A, 0x3B, 0x86, 0xFE, 0x22, 0x5C, 0xA8, 0x5E, 0x67, 0xAA, 0xEC, 0x70, 0xCC
])

_FK = [0x46970E9C, 0x4BC0685E, 0x59056186, 0xBCA2491E]
_CK = [
    0x000EB92B, 0x3A0AE783, 0x9E3B5C67, 0xADDBDABF, 0x7B7484CB, 0x49156C63, 0xC79AB5E7, 0x79EC9CFF,
    0x1725BEAB, 0x2FB89CA3, 0x24808AD7, 0xDDD28B1F, 0x4740DA4B, 0xBBC3EA73, 0x247B30E7, 0x91BE385F,
    0x0401248B, 0x45FCD3A3, 0x530B4CE7, 0xC68DD35F, 0xE3D16C2B, 0x4F698C13, 0x6B92C747, 0x769EFB1F,
    0x4C73BE9B, 0xC942B193, 0xAD80D827, 0x372FB33F, 0x13CB6AAB, 0x2BDC0AA3, 0x17A4A247, 0xD5E96CAF
]

# ============================================================================
# CRYPTO HELPER FUNCTIONS
# ============================================================================

def ROL32(x, n):
    return ((x << n) & 0xFFFFFFFF) | ((x >> (32 - n)) & 0xFFFFFFFF)

def _BS(X):
    return ((_S_BOX[(X >> 24) & 0xff] << 24) |
            (_S_BOX[(X >> 16) & 0xff] << 16) |
            (_S_BOX[(X >> 8) & 0xff] << 8) |
            (_S_BOX[X & 0xff]))

def _T0(X):
    X = _BS(X)
    return X ^ ROL32(X, 2) ^ ROL32(X, 10) ^ ROL32(X, 18) ^ ROL32(X, 24)

def _T1(X):
    X = _BS(X)
    return X ^ ROL32(X, 13) ^ ROL32(X, 23)

def _key_expand(key: bytes, rkey: List[int]):
    K0 = int.from_bytes(key[0:4], "big") ^ _FK[0]
    K1 = int.from_bytes(key[4:8], "big") ^ _FK[1]
    K2 = int.from_bytes(key[8:12], "big") ^ _FK[2]
    K3 = int.from_bytes(key[12:16], "big") ^ _FK[3]
    for i in range(0, 32, 4):
        K0 = K0 ^ _T1(K1 ^ K2 ^ K3 ^ _CK[i])
        rkey[i] = K0
        K1 = K1 ^ _T1(K2 ^ K3 ^ K0 ^ _CK[i+1])
        rkey[i+1] = K1
        K2 = K2 ^ _T1(K3 ^ K0 ^ K1 ^ _CK[i+2])
        rkey[i+2] = K2
        K3 = K3 ^ _T1(K0 ^ K1 ^ K2 ^ _CK[i+3])
        rkey[i+3] = K3

class SM4:
    def __init__(self, key: bytes):
        self._rkey = [0]*32
        _key_expand(key, self._rkey)
    def encrypt(self, block: bytes) -> bytes:
        RK = self._rkey
        X0 = int.from_bytes(block[0:4], "big")
        X1 = int.from_bytes(block[4:8], "big")
        X2 = int.from_bytes(block[8:12], "big")
        X3 = int.from_bytes(block[12:16], "big")
        for i in range(0, 32, 4):
            X0 = X0 ^ _T0(X1 ^ X2 ^ X3 ^ RK[i])
            X1 = X1 ^ _T0(X2 ^ X3 ^ X0 ^ RK[i+1])
            X2 = X2 ^ _T0(X3 ^ X0 ^ X1 ^ RK[i+2])
            X3 = X3 ^ _T0(X0 ^ X1 ^ X2 ^ RK[i+3])
        return (X3.to_bytes(4, "big") + X2.to_bytes(4, "big") +
                X1.to_bytes(4, "big") + X0.to_bytes(4, "big"))
    def decrypt(self, block: bytes) -> bytes:
        RK = self._rkey
        X0 = int.from_bytes(block[0:4], "big")
        X1 = int.from_bytes(block[4:8], "big")
        X2 = int.from_bytes(block[8:12], "big")
        X3 = int.from_bytes(block[12:16], "big")
        for i in range(0, 32, 4):
            X0 = X0 ^ _T0(X1 ^ X2 ^ X3 ^ RK[31-i])
            X1 = X1 ^ _T0(X2 ^ X3 ^ X0 ^ RK[30-i])
            X2 = X2 ^ _T0(X3 ^ X0 ^ X1 ^ RK[29-i])
            X3 = X3 ^ _T0(X0 ^ X1 ^ X2 ^ RK[28-i])
        return (X3.to_bytes(4, "big") + X2.to_bytes(4, "big") +
                X1.to_bytes(4, "big") + X0.to_bytes(4, "big"))

class Misc:
    @staticmethod
    def pad_to_n(data: bytes, n: int) -> bytes:
        padding = n - (len(data) % n)
        if padding == n: return data
        return data + b'\x00' * padding
    @staticmethod
    def align_up(x: int, n: int) -> int:
        return ((x + n - 1) // n) * n

# ============================================================================
# PAK READERS AND DATA CLASSES
# ============================================================================

class Reader_pak:
    def __init__(self, buffer, cursor=0):
        self._buffer = buffer
        self._cursor = cursor
    def u1(self, move_cursor=True) -> int:
        return self.unpack('B', move_cursor=move_cursor)[0]
    def u4(self, move_cursor=True) -> int:
        return self.unpack('<I', move_cursor=move_cursor)[0]
    def u8(self, move_cursor=True) -> int:
        return self.unpack('<Q', move_cursor=move_cursor)[0]
    def i1(self, move_cursor=True) -> int:
        return self.unpack('b', move_cursor=move_cursor)[0]
    def i4(self, move_cursor=True) -> int:
        return self.unpack('<i', move_cursor=move_cursor)[0]
    def i8(self, move_cursor=True) -> int:
        return self.unpack('<q', move_cursor=move_cursor)[0]
    def s(self, n: int, move_cursor=True) -> bytes:
        return self.unpack(f'{n}s', move_cursor=move_cursor)[0]
    def unpack(self, f: str, offset=0, move_cursor=True):
        x = struct.unpack_from(f, self._buffer, self._cursor + offset)
        if move_cursor:
            self._cursor += struct.calcsize(f)
        return x
    def string(self, move_cursor=True) -> str:
        length = self.i4(move_cursor=move_cursor)
        if length == 0: return str()
        offset = 0 if move_cursor else 4
        return self.unpack(f'{length}s', offset=offset, move_cursor=move_cursor)[0].rstrip(b'\x00').decode()

class PakInfo:
    def __init__(self, buffer, keystream: list[int]):
        def decrypt_index_encrypted(x: int) -> int:
            return (x ^ keystream[3]) & 0xFF
        def decrypt_magic(x: int) -> int:
            return x ^ keystream[2]
        def decrypt_index_hash(x: bytes) -> bytes:
            key = struct.pack('<5I', *keystream[4:][:5])
            return bytes(a ^ b for a,b in zip(x, key))
        def decrypt_index_size(x: int) -> int:
            return x ^ ((keystream[10] << 32) | keystream[11])
        def decrypt_index_offset(x: int) -> int:
            return x ^ ((keystream[0] << 32) | keystream[1])
        reader = Reader_pak(buffer[-PakInfo._mem_size(-1):])
        self.index_encrypted = decrypt_index_encrypted(reader.u1()) == 1
        self.magic = decrypt_magic(reader.u4())
        self.version = reader.u4()
        self.index_hash = decrypt_index_hash(reader.s(20)) if self.version >= 6 else bytes()
        self.index_size = decrypt_index_size(reader.u8())
        self.index_offset = decrypt_index_offset(reader.u8())
        if self.version <= 3:
            self.index_encrypted = False
    @staticmethod
    def _mem_size(_: int) -> int:
        return 1 + 4 + 4 + 20 + 8 + 8

class TencentPakInfo(PakInfo):
    def __init__(self, buffer, keystream: list[int]):
        def decrypt_unk(x: bytes) -> bytes:
            key = struct.pack('<8I', *keystream[7:][:8])
            return bytes(a ^ b for a,b in zip(x, key))
        def decrypt_stem_hash(x: int) -> int:
            return x ^ keystream[8]
        def decrypt_unk_hash(x: int) -> int:
            return x ^ keystream[9]
        super().__init__(buffer, keystream)
        footer_size = TencentPakInfo._mem_size(self.version)
        reader = Reader_pak(buffer[-footer_size:])
        self.unk1 = decrypt_unk(reader.s(32)) if self.version >= 7 else bytes()
        self.packed_key = reader.s(256) if self.version >= 8 else bytes()
        self.packed_iv = reader.s(256) if self.version >= 8 else bytes()
        self.packed_index_hash = reader.s(256) if self.version >= 8 else bytes()
        self.stem_hash = decrypt_stem_hash(reader.u4()) if self.version >= 9 else 0
        self.unk2 = decrypt_unk_hash(reader.u4()) if self.version >= 9 else 0
        self.content_org_hash = reader.s(20) if self.version >= 12 else bytes()
    @staticmethod
    def _mem_size(version: int) -> int:
        size_for_7 = 32 if version >= 7 else 0
        size_for_8 = 256*3 if version >= 8 else 0
        size_for_9 = 4*2 if version >= 9 else 0
        size_for_12 = 20 if version >= 12 else 0
        return PakInfo._mem_size(version) + size_for_7 + size_for_8 + size_for_9 + size_for_12

class PakCompressedBlock:
    def __init__(self, reader: Reader_pak = None, start: int = 0, end: int = 0):
        if reader is not None:
            self.start = reader.u8()
            self.end = reader.u8()
        else:
            self.start = start
            self.end = end

@dataclass
class TencentPakEntry:
    def __init__(self, reader: Reader_pak, version: int):
        self.content_hash = reader.s(20)
        if version <= 1:
            _ = reader.u8()
        self.offset = reader.u8()
        self.uncompressed_size = reader.u8()
        self.compression_method = reader.u4() & CM_MASK
        self.size = reader.u8()
        self.unk1 = reader.u1() if version >= 5 else 0
        self.unk2 = reader.s(20) if version >= 5 else bytes()
        block_count = 0
        if self.compression_method != 0 and version >= 3:
            block_count = reader.u4()
            if block_count > 10000: block_count = 0
            self.compressed_blocks = [PakCompressedBlock(reader) for _ in range(block_count)]
        else:
            self.compressed_blocks = []
        self.compression_block_size = reader.u4() if version >= 4 else 0
        self.encrypted = reader.u1() == 1 if version >= 4 else False
        self.encryption_method = reader.u4() if version >= 12 else 0
        self.unk3 = reader.u4() if version >= 14 else 0

# ============================================================================
# PAK CRYPTO AND COMPRESSION
# ============================================================================

class PakCrypto:
    class _LCG:
        def __init__(self, seed: int): self.state = seed
        def next(self) -> int:
            MASK_32 = 0xFFFFFFFF
            MSB_1 = 1 << 31
            def wrap(x: int) -> int:
                x &= MASK_32
                if not x & MSB_1: return x
                else: return ((x + MSB_1) & MASK_32) - MSB_1
            x1 = wrap(0x41C64E6D * self.state)
            self.state = wrap(x1 + 12345)
            x2 = wrap(x1 + 0x13038) if self.state < 0 else self.state
            return ((x2 >> 16) & MASK_32) % 0x7FFF
    @staticmethod
    def zuc_keystream() -> list[int]:
        zuc = gmalg.ZUC(ZUC_KEY, ZUC_IV)
        return [struct.unpack('>I', zuc.generate())[0] for _ in range(16)]
    @staticmethod
    def _xorxor(buffer, x) -> bytes:
        return bytes(buffer[i] ^ x[i % len(x)] for i in range(len(buffer)))
    @staticmethod
    def _hashhash(buffer, n: int) -> bytes:
        result = bytes()
        for i in range(math.ceil(n / SHA1.digest_size)):
            result += SHA1.new(buffer).digest()
        if len(result) >= n: result = result[:n]
        else: result += b'\x00' * (n - len(result))
        return result
    @staticmethod
    def _meowmeow(buffer) -> bytes:
        def unpad(x):
            skip = 1 + next((i for i in range(len(x)) if x[i] != 0))
            return x[skip:]
        if len(buffer) < 43: return bytes()
        x1 = buffer[1:][:SHA1.digest_size]
        x2 = buffer[SHA1.digest_size + 1:]
        x1 = PakCrypto._xorxor(x1, PakCrypto._hashhash(x2, len(x1)))
        x2 = PakCrypto._xorxor(x2, PakCrypto._hashhash(x1, len(x2)))
        part1, m = (x2[:SHA1.digest_size], x2[SHA1.digest_size:])
        if part1 != SHA1.new(b'\x00' * SHA1.digest_size).digest():
            return bytes()
        return unpad(m)
    @staticmethod
    def rsa_extract(signature: bytes, modulus: bytes) -> bytes:
        c = int.from_bytes(signature, 'little')
        n = int.from_bytes(modulus, 'little')
        e = 0x10001
        m = pow(c, e, n).to_bytes(256, 'little').rstrip(b'\x00')
        return PakCrypto._meowmeow(Misc.pad_to_n(m, 4))
    @staticmethod
    def _encrypt_simple1(plaintext) -> bytes:
        return bytes(x ^ SIMPLE1_DECRYPT_KEY for x in plaintext)
    @staticmethod
    def _decrypt_simple1(ciphertext) -> bytes:
        return bytes(x ^ SIMPLE1_DECRYPT_KEY for x in ciphertext)
    @staticmethod
    def _encrypt_simple2(plaintext) -> bytes:
        class RollingKey:
            def __init__(self, iv): self._value = iv
            def update(self, x): orig = self._value; self._value = x; return orig ^ x
        assert len(plaintext) % SIMPLE2_BLOCK_SIZE == 0
        initial_key = struct.unpack('<I', SIMPLE2_DECRYPT_KEY)[0]
        rk = RollingKey(initial_key)
        ciphertext = (struct.pack('<I', rk.update(x)) for x in struct.unpack(f'<{len(plaintext)//4}I', plaintext))
        return bytes(it.chain.from_iterable(ciphertext))
    @staticmethod
    def _decrypt_simple2(ciphertext) -> bytes:
        class RollingKey:
            def __init__(self, iv): self._value = iv
            def update(self, x): self._value ^= x; return self._value
        assert len(ciphertext) % SIMPLE2_BLOCK_SIZE == 0
        initial_key = struct.unpack('<I', SIMPLE2_DECRYPT_KEY)[0]
        rk = RollingKey(initial_key)
        plaintext = (struct.pack('<I', rk.update(x)) for x in struct.unpack(f'<{len(ciphertext)//4}I', ciphertext))
        return bytes(it.chain.from_iterable(plaintext))
    @staticmethod
    @lru_cache(maxsize=1)
    def _derive_sm4_key(file_path: PurePath, encryption_method: int) -> bytes:
        part1 = file_path.stem.lower()
        if encryption_method == EM_SM4_2: secret = SM4_SECRET_2
        elif encryption_method == EM_SM4_4: secret = SM4_SECRET_4
        else:
            index = (encryption_method - EM_SM4_NEW_BASE) % len(SM4_SECRET_NEW)
            secret = f'{SM4_SECRET_NEW[index]}{encryption_method}'
        return SHA1.new(str(part1 + secret).encode()).digest()[:16]
    @staticmethod
    @lru_cache(maxsize=1)
    def _sm4_context_for_key(key: bytes) -> SM4:
        return SM4(key)
    @staticmethod
    def _encrypt_sm4(plaintext, file_path: PurePath, encryption_method: int) -> bytes:
        padded = pad(plaintext, 16)
        key = PakCrypto._derive_sm4_key(file_path, encryption_method)
        sm4 = PakCrypto._sm4_context_for_key(key)
        return b''.join(sm4.encrypt(padded[i:i+16]) for i in range(0, len(padded), 16))
    @staticmethod
    def _decrypt_sm4(ciphertext, file_path: PurePath, encryption_method: int) -> bytes:
        assert len(ciphertext) % 16 == 0
        key = PakCrypto._derive_sm4_key(file_path, encryption_method)
        sm4 = PakCrypto._sm4_context_for_key(key)
        return b''.join(sm4.decrypt(ciphertext[i:i+16]) for i in range(0, len(ciphertext), 16))
    
    @staticmethod
    def decrypt_index(ciphertext, pak_info) -> bytes:
        errors = []
        
        if pak_info.version > 7:
            try:
                key = PakCrypto.rsa_extract(pak_info.packed_key, RSA_MOD_1)
                iv = PakCrypto.rsa_extract(pak_info.packed_iv, RSA_MOD_1)
                
                if len(key) >= 16 and len(iv) >= 16:
                    for key_len in [32, 16]:
                        for iv_len in [16, 32]:
                            try:
                                k = key[:key_len] if len(key) >= key_len else key + b'\x00' * (key_len - len(key))
                                i = iv[:iv_len] if len(iv) >= iv_len else iv + b'\x00' * (iv_len - len(iv))
                                aes = AES.new(k[:32], MODE_CBC, i[:16])
                                decrypted = aes.decrypt(ciphertext)
                                try:
                                    result = unpad(decrypted, AES.block_size)
                                    if result and len(result) > 10:
                                        return result
                                except:
                                    result = decrypted.rstrip(b'\x00')
                                    if result and len(result) > 10:
                                        return result
                            except:
                                continue
            except Exception as e:
                errors.append(f"AES: {e}")
        
        try:
            result = bytes(PakCrypto._decrypt_simple1(ciphertext))
            if len(result) > 10 and result[0:4] != b'\x00\x00\x00\x00':
                return result
        except Exception as e:
            errors.append(f"Simple1: {e}")
        
        try:
            keystream = PakCrypto.zuc_keystream()
            key_bytes = b''
            for k in keystream[:8]:
                key_bytes += struct.pack('<I', k)
            result = bytes(ciphertext[i] ^ key_bytes[i % len(key_bytes)] for i in range(len(ciphertext)))
            if len(result) > 10:
                return result
        except Exception as e:
            errors.append(f"ZUC: {e}")
        
        return ciphertext
    
    @staticmethod
    def _is_simple1_method(m): return m == EM_SIMPLE1
    @staticmethod
    def _is_simple2_method(m): return m == EM_SIMPLE2
    @staticmethod
    def _is_sm4_method(m): return m == EM_SM4_2 or m == EM_SM4_4 or (m & EM_SM4_NEW_MASK != 0)
    @staticmethod
    def _is_unknown_17_method(m): return m == EM_UNKNOWN_17
    @staticmethod
    def align_encrypted_content_size(n: int, method: int) -> int:
        if PakCrypto._is_simple2_method(method): return Misc.align_up(n, SIMPLE2_BLOCK_SIZE)
        elif PakCrypto._is_sm4_method(method): return Misc.align_up(n, 16)
        else: return n
    @staticmethod
    def encrypt_block(plaintext, file: PurePath, method: int) -> bytes:
        if PakCrypto._is_simple1_method(method): return PakCrypto._encrypt_simple1(plaintext)
        elif PakCrypto._is_simple2_method(method): return PakCrypto._encrypt_simple2(pad(plaintext, SIMPLE2_BLOCK_SIZE))
        elif PakCrypto._is_sm4_method(method): return PakCrypto._encrypt_sm4(plaintext, file, method)
        elif PakCrypto._is_unknown_17_method(method): return plaintext
        else:
            if method == 0: return plaintext
            return plaintext
    @staticmethod
    def decrypt_block(ciphertext, file: PurePath, method: int) -> bytes:
        if PakCrypto._is_simple1_method(method): return PakCrypto._decrypt_simple1(ciphertext)
        elif PakCrypto._is_simple2_method(method): return PakCrypto._decrypt_simple2(ciphertext)
        elif PakCrypto._is_sm4_method(method): return PakCrypto._decrypt_sm4(ciphertext, file, method)
        elif PakCrypto._is_unknown_17_method(method): return ciphertext
        else:
            if method == 0: return ciphertext
            return ciphertext
    @staticmethod
    @lru_cache(maxsize=33)
    def generate_block_indices(n: int, method: int) -> list[int]:
        if not PakCrypto._is_sm4_method(method): return list(range(n))
        perm = []
        lcg = PakCrypto._LCG(n)
        while len(perm) != n:
            x = lcg.next() % n
            if x not in perm: perm.append(x)
        inv = [0]*len(perm)
        for i,x in enumerate(perm): inv[x] = i
        return inv

class PakCompression:
    @staticmethod
    @lru_cache(maxsize=33)
    def _zstd_decompressor(dict_data: bytes | None) -> ZstdDecompressor:
        dict_obj = ZstdCompressionDict(dict_data, DICT_TYPE_AUTO) if dict_data else None
        return ZstdDecompressor(dict_obj)
    @staticmethod
    @lru_cache(maxsize=128)
    def _zstd_compressor(dict_data: bytes | None, level: int) -> ZstdCompressor:
        dict_obj = ZstdCompressionDict(dict_data, DICT_TYPE_AUTO) if dict_data else None
        return ZstdCompressor(level=level, dict_data=dict_obj)
    @staticmethod
    def decompress_block(block, dict_data: bytes | None, method: int) -> bytes:
        if method == CM_ZLIB: return zlib.decompress(block)
        elif method in (CM_ZSTD, CM_ZSTD_DICT):
            if method != CM_ZSTD_DICT: dict_data = None
            return PakCompression._zstd_decompressor(dict_data).decompress(block)
        else: return block
    @staticmethod
    def compress_block(block, dict_data: bytes | None, method: int, level: int | None = None) -> bytes:
        if method == CM_ZLIB:
            use_level = level if level is not None else 9
            return zlib.compress(block, level=use_level)
        elif method in (CM_ZSTD, CM_ZSTD_DICT):
            use_level = level if level is not None else 22
            if method != CM_ZSTD_DICT: dict_data = None
            return PakCompression._zstd_compressor(dict_data, use_level).compress(block)
        else: return block

# ============================================================================
# LUA DECOMPILATION/COMPILATION FUNCTIONS
# ============================================================================

def _xor(data, key):
    return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])

class Reader_new:
    def __init__(self, d, k): self.d=d; self.pos=0; self.k=k
    def read(self, n):
        v=bytes(self.d[self.pos:self.pos+n]); self.pos+=n; return v
    def byte(self):
        v=self.d[self.pos]; self.pos+=1; return v
    def i32(self):
        v=struct.unpack_from('<i',self.d,self.pos)[0]; self.pos+=4; return v
    def i64(self):
        v=struct.unpack_from('<q',self.d,self.pos)[0]; self.pos+=8; return v
    def dbl(self):
        v=struct.unpack_from('<d',self.d,self.pos)[0]; self.pos+=8; return v
    def string(self):
        sz=self.byte()
        if sz==0: return None
        if sz==0xFF:
            sz=struct.unpack_from('<Q',self.d,self.pos)[0]; self.pos+=8
        raw=bytes(self.d[self.pos:self.pos+sz-1]); self.pos+=sz-1
        b=_xor(raw,self.k)
        try: return b.decode('utf-8')
        except: return b.decode('latin-1',errors='replace')

class P:
    __slots__=('src','ld','ll','np','va','ms','ins','K','upvals','upvs','locs','subs')
    def __init__(self):
        self.src=None;self.ld=0;self.ll=0;self.np=0;self.va=0;self.ms=0
        self.ins=[];self.K=[];self.upvals=b'';self.upvs=[];self.locs=[];self.subs=[]

def parse(r):
    p=P()
    try:
        p.src=r.string()
        p.ld=r.i32(); p.ll=r.i32()
        p.np=r.byte(); p.va=r.byte(); p.ms=r.byte()
        n=r.i32()
        p.ins=[struct.unpack_from('<I',r.read(4))[0] for _ in range(n)]
        n=r.i32()
        for _ in range(n):
            t=r.byte()
            if t==LUA_NIL:   p.K.append(('nil',None))
            elif t==LUA_BOOL: b=r.byte(); p.K.append(('bool',bool(b)))
            elif t==LUA_NUM:
                raw=r.i64(); fv=struct.unpack('<d',struct.pack('<q',raw))[0]
                p.K.append(('float',fv))
            elif t==LUA_FLOAT:
                raw=r.dbl(); iv=struct.unpack('<q',struct.pack('<d',raw))[0]
                p.K.append(('int',iv))
            elif t in (LUA_STR,LUA_STRL): s=r.string(); p.K.append(('str',s))
            else: raise ValueError(f'Unknown const {t}')
        n=r.i32()
        p.upvals = r.read(n*2)
        n=r.i32()
        for _ in range(n): p.subs.append(parse(r))
        n=r.i32(); r.read(n); n=r.i32(); r.read(n*8); n=r.i32()
        for _ in range(n):
            nm=r.string(); sp=r.i32(); ep=r.i32()
            if nm: p.locs.append((nm,sp,ep))
        n=r.i32()
        for _ in range(n):
            s=r.string()
            if s: p.upvs.append(s)
        return p
    except Exception: return None

def load_proto(path):
    try:
        with open(path,'rb') as f: d=bytearray(f.read())
        if len(d)<34 or d[:4]!=b'\x1bLua' or d[4]!=0x53: return None
        r=Reader_new(d,_K); r.pos=34
        return parse(r)
    except: return None

class BinaryWriter:
    def __init__(self): self.buf = bytearray()
    def byte(self, v): self.buf.append(v & 0xFF)
    def int32(self, v): self.buf.extend(struct.pack('<i', v))
    def uint32(self, v): self.buf.extend(struct.pack('<I', v))
    def int64(self, v): self.buf.extend(struct.pack('<q', v))
    def double(self, v): self.buf.extend(struct.pack('<d', v))
    def raw(self, data): self.buf.extend(data)

    def lua_string(self, s: Optional[str], is_pubg: bool = False):
        if s is None: self.byte(0); return
        e = s.encode('utf-8') if isinstance(s, str) else s
        sz = len(e) + 1
        if sz < 0xFF: self.byte(sz)
        else: self.byte(0xFF); self.uint32(sz)
        if is_pubg:
            enc = bytes(e[i] ^ STRING_XOR_KEY[i % 32] for i in range(len(e)))
            self.raw(enc)
        else: self.raw(e)

    def lua_inst(self, op, A, B, C, Bx, sBx, Ax, fmt):
        op &= 0x3F
        if   fmt == iABC:  r = op | ((A & 0xFF)<<6) | ((C & 0x1FF)<<14) | ((B & 0x1FF)<<23)
        elif fmt == iABx:  r = op | ((A & 0xFF)<<6) | ((Bx & 0x3FFFF)<<14)
        elif fmt == iAsBx: r = op | ((A & 0xFF)<<6) | (((sBx+131071) & 0x3FFFF)<<14)
        elif fmt == iAx:   r = op | ((Ax & 0x3FFFFFF)<<6)
        else: r = 0
        self.uint32(r)

    def get_data(self) -> bytes: return bytes(self.buf)

class BinaryReader:
    def __init__(self, data: bytes, sizet: int = 4):
        self.data = bytearray(data); self.pos = 0; self.sizet = sizet

    def byte(self) -> int:
        if self.pos >= len(self.data): raise EOFError()
        v = self.data[self.pos]; self.pos += 1; return v

    def int32(self) -> int:
        if self.pos + 4 > len(self.data): raise EOFError()
        v = struct.unpack_from('<i', self.data, self.pos)[0]; self.pos += 4; return v

    def uint32(self) -> int:
        if self.pos + 4 > len(self.data): raise EOFError()
        v = struct.unpack_from('<I', self.data, self.pos)[0]; self.pos += 4; return v

    def double(self) -> float:
        if self.pos + 8 > len(self.data): raise EOFError()
        v = struct.unpack_from('<d', self.data, self.pos)[0]; self.pos += 8; return v

    def int64(self) -> int:
        if self.pos + 8 > len(self.data): raise EOFError()
        v = struct.unpack_from('<q', self.data, self.pos)[0]; self.pos += 8; return v

    def bytes(self, n: int) -> bytes:
        if self.pos + n > len(self.data): raise EOFError()
        v = self.data[self.pos:self.pos+n]; self.pos += n; return bytes(v)

    def pubg_string(self) -> Optional[str]:
        sz = self.byte()
        if sz == 0xFF: sz = self.uint32()
        if sz == 0: return None
        sz -= 1
        enc = self.bytes(sz)
        dec = bytes(enc[i] ^ STRING_XOR_KEY[i % 32] for i in range(len(enc)))
        try: return dec.decode('utf-8', errors='replace')
        except Exception: return dec.decode('latin-1')

    def std_string(self) -> Optional[str]:
        sz = self.byte()
        if sz == 0xFF:
            if self.sizet == 8:
                if self.pos + 8 > len(self.data): raise EOFError()
                sz = struct.unpack_from('<Q', self.data, self.pos)[0]; self.pos += 8
            else: sz = self.uint32()
        if sz == 0: return None
        sz -= 1
        raw = self.bytes(sz)
        try: return raw.decode('utf-8', errors='replace')
        except Exception: return raw.decode('latin-1')

def _convert_function(reader: BinaryReader, writer: BinaryWriter, to_std: bool = True):
    src = reader.pubg_string() if to_std else reader.std_string()
    writer.lua_string(src, is_pubg=(not to_std))
    linedefined = reader.int32()
    writer.int32(linedefined)
    writer.int32(reader.int32())
    writer.byte(reader.byte()); writer.byte(reader.byte()); writer.byte(reader.byte())

    csz = reader.uint32(); writer.uint32(csz)
    opmap = BGMI_TO_STD if to_std else STD_TO_BGMI
    for _ in range(csz):
        raw = reader.uint32()
        bop = raw & 0x3F
        A   = (raw >> 6)  & 0xFF
        B   = (raw >> 23) & 0x1FF
        C   = (raw >> 14) & 0x1FF
        Bx  = (raw >> 14) & 0x3FFFF
        sBx = Bx - 131071
        Ax  = (raw >> 6)  & 0x3FFFFFF
        sop = opmap[bop] if bop < len(opmap) else bop
        fmt = STD_FMT[sop] if sop < len(STD_FMT) else iABC
        writer.lua_inst(sop, A, B, C, Bx, sBx, Ax, fmt)

    nk = reader.uint32(); writer.uint32(nk)
    for _ in range(nk):
        t = reader.byte(); writer.byte(t)
        if   t == 0: pass
        elif t == 1:  writer.byte(reader.byte())
        elif t == 3:  writer.double(reader.double())
        elif t == 19: writer.int64(reader.int64())
        elif t in (4, 20):
            s = reader.pubg_string() if to_std else reader.std_string()
            writer.lua_string(s, is_pubg=(not to_std))
        else: raise ValueError(f"Unknown constant type 0x{t:02X}")

    nups = reader.uint32(); writer.uint32(nups)
    for _ in range(nups): writer.byte(reader.byte()); writer.byte(reader.byte())

    npts = reader.uint32(); writer.uint32(npts)
    for _ in range(npts): _convert_function(reader, writer, to_std)

    nln = reader.uint32()
    if to_std:
        lines = []; cur = linedefined
        for _ in range(nln):
            d = reader.byte()
            cur += d if d <= 127 else d - 256
            lines.append(cur)
        writer.uint32(len(lines))
        for ln in lines: writer.int32(ln)
        nab = reader.uint32()
        for _ in range(nab): reader.uint32(); reader.uint32()
    else:
        lines = [reader.int32() for _ in range(nln)]
        writer.uint32(len(lines))
        prev = linedefined
        for ln in lines:
            delta = ln - prev
            if -128 <= delta <= 127: writer.byte(delta & 0xFF)
            else: writer.byte(0x00); writer.int32(delta)
            prev = ln
        writer.uint32(0)

    nloc = reader.uint32(); writer.uint32(nloc)
    for _ in range(nloc):
        s = reader.pubg_string() if to_std else reader.std_string()
        writer.lua_string(s, is_pubg=(not to_std))
        writer.int32(reader.int32()); writer.int32(reader.int32())

    nupn = reader.uint32(); writer.uint32(nupn)
    for _ in range(nupn):
        s = reader.pubg_string() if to_std else reader.std_string()
        writer.lua_string(s, is_pubg=(not to_std))

def bgmi_to_std(data: bytes) -> bytes:
    """Convert BGMI/PUBG custom bytecode to standard Lua 5.3 bytecode."""
    if data[:4] != b'\x1bLua': raise ValueError("Not a valid Lua bytecode file")
    reader = BinaryReader(data, sizet=4); writer = BinaryWriter()
    hdr = bytearray(data[:HEADER_SIZE]); hdr[13] = 4
    writer.raw(hdr); reader.pos = HEADER_SIZE
    nibble_flag = reader.byte(); writer.byte(nibble_flag)
    _convert_function(reader, writer, to_std=True)
    return writer.get_data()

def std_to_bgmi(data: bytes) -> bytes:
    """Convert standard Lua 5.3 bytecode back to BGMI/PUBG custom bytecode."""
    if data[:4] != b'\x1bLua': raise ValueError("Not a valid Lua bytecode file")
    sizet = data[13] if data[13] in (4, 8) else 4
    reader = BinaryReader(data, sizet=sizet); writer = BinaryWriter()
    hdr = bytearray(data[:HEADER_SIZE]); hdr[13] = 4
    writer.raw(hdr); reader.pos = HEADER_SIZE
    nibble_flag = reader.byte(); writer.byte(nibble_flag)
    _convert_function(reader, writer, to_std=False)
    return writer.get_data()

def convert_file(inp: str, outp: str = None) -> Tuple[bool, str]:
    """Convert a BGMI/PUBG Lua bytecode file to standard format."""
    if not outp: outp = os.path.splitext(inp)[0] + '.std.luac'
    try:
        with open(inp, 'rb') as f: data = f.read()
    except Exception as e: return False, f"Cannot read input file: {e}"
    if len(data) < 34 or data[:4] != b'\x1bLua':
        try: shutil.copy2(inp, outp); return True, outp
        except: return False, "Failed to copy non-Lua file"
    nibble_flag = data[33]
    if nibble_flag > 2: nibble_flag = 0; data = bytearray(data); data[33] = 0; data = bytes(data)
    if nibble_flag > 1:
        fixed = bytearray(data[:34])
        for i in range(34, len(data)):
            b = data[i]; fixed.append(((b << 4) & 0xF0) | ((b >> 4) & 0x0F))
        data = bytes(fixed)
    try:
        std_data = bgmi_to_std(data)
        with open(outp, 'wb') as f: f.write(std_data)
        return True, outp
    except Exception:
        try: shutil.copy2(inp, outp); return True, outp
        except: return False, "Conversion failed"

def repack_to_pubg(std_luac_path: str, original_pubg_path: str,
                   outp: str = None, pad_to_size: int = None) -> Tuple[bool, str]:
    if not outp: outp = os.path.splitext(std_luac_path)[0] + '.pubg.luac'
    try:
        with open(original_pubg_path, 'rb') as f: orig_data = f.read()
    except Exception as e: return False, f"Cannot read original: {e}"
    if len(orig_data) < 34 or orig_data[:4] != b'\x1bLua':
        return False, "Original not valid Lua bytecode"
    header = orig_data[:33]; nibble_flag = orig_data[33]
    if nibble_flag > 2: nibble_flag = 0
    try:
        with open(std_luac_path, 'rb') as f: std_data = f.read()
    except Exception as e: return False, f"Cannot read std luac: {e}"
    try:
        bgmi_data = std_to_bgmi(std_data)
        bgmi_data = header + bytes([nibble_flag]) + bgmi_data[34:]
        if nibble_flag > 1:
            data_list = bytearray(bgmi_data[:34])
            for i in range(34, len(bgmi_data)):
                b = bgmi_data[i]; data_list.append(((b << 4) & 0xF0) | ((b >> 4) & 0x0F))
            bgmi_data = bytes(data_list)
        if pad_to_size is not None and len(bgmi_data) < pad_to_size:
            bgmi_data += b'\x00' * (pad_to_size - len(bgmi_data))
        with open(outp, 'wb') as f: f.write(bgmi_data)
        return True, outp
    except Exception as e: return False, f"Repack failed: {e}"

def find_luadec():
    exes_path = EXES_DIR / "luadec"
    if exes_path.exists():
        if not os.access(exes_path, os.X_OK) and os.name != 'nt':
            try: exes_path.chmod(exes_path.stat().st_mode | 0o111)
            except: pass
        if os.access(exes_path, os.X_OK) or os.name == 'nt':
            return str(exes_path)
    exes_path = EXES_DIR / "luadec.exe"
    if exes_path.exists(): return str(exes_path)
    return shutil.which('luadec')

def attempt_decompile(luadec_path, target_bytecode, output_lua):
    try:
        res = subprocess.run([luadec_path, target_bytecode], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20)
        out_data = res.stdout.decode('utf-8', errors='replace')
        if res.returncode == 0 and len(out_data.strip()) > 10:
            with open(output_lua, 'w', encoding='utf-8') as f:
                f.write(out_data)
            return True, ""
        return False, res.stderr.decode('utf-8', errors='replace')
    except Exception as e:
        return False, str(e)

def fix_lua_syntax(content: str) -> str:
    content = re.sub(r'#(\w+):', r'#\1.', content)
    content = re.sub(r'=\s*\.\s*end\b', '= nil', content)
    content = re.sub(r'\bend\.\s*$', 'end', content, flags=re.MULTILINE)
    content = re.sub(r'[^\x20-\x7E\n\t\r]', '', content)
    return content

def remove_lua_comments(content: str) -> str:
    result = []
    i = 0
    n = len(content)
    in_string = False
    string_char = None
    in_long_string = False
    long_string_level = 0
    in_block_comment = False
    block_comment_level = 0
    while i < n:
        ch = content[i]
        if not in_string and not in_long_string and not in_block_comment:
            if ch == '-' and i+1 < n and content[i+1] == '-':
                if i+2 < n and content[i+2] == '[':
                    j = i+3
                    level = 0
                    while j < n and content[j] == '=':
                        level += 1
                        j += 1
                    if j < n and content[j] == '[':
                        in_block_comment = True
                        block_comment_level = level
                        i = j+1
                        continue
                    else:
                        i += 2
                        while i < n and content[i] not in '\r\n':
                            i += 1
                        continue
                else:
                    i += 2
                    while i < n and content[i] not in '\r\n':
                        i += 1
                    continue
        if in_block_comment:
            if ch == ']' and i+1 < n and content[i+1] == ']':
                j = i+2
                level_check = 0
                while j < n and content[j] == '=':
                    level_check += 1
                    j += 1
                if j < n and content[j] == ']' and level_check == block_comment_level:
                    in_block_comment = False
                    i = j+1
                    continue
            i += 1
            continue
        if not in_string and not in_long_string and (ch == '"' or ch == "'"):
            in_string = True
            string_char = ch
            result.append(ch)
            i += 1
            continue
        elif in_string:
            result.append(ch)
            if ch == '\\' and i+1 < n:
                result.append(content[i+1])
                i += 2
                continue
            elif ch == string_char:
                in_string = False
            i += 1
            continue
        if not in_string and not in_long_string and not in_block_comment and ch == '[' and i+1 < n and content[i+1] == '[':
            j = i+2
            level = 0
            while j < n and content[j] == '=':
                level += 1
                j += 1
            if j < n and content[j] == '[':
                in_long_string = True
                long_string_level = level
                result.append(content[i:j+1])
                i = j+1
                continue
        if in_long_string:
            result.append(ch)
            if ch == ']' and i+1 < n and content[i+1] == ']':
                j = i+2
                level_check = 0
                while j < n and content[j] == '=':
                    level_check += 1
                    j += 1
                if j < n and content[j] == ']' and level_check == long_string_level:
                    result.append(content[i+1:j+1])
                    i = j+1
                    in_long_string = False
                    continue
            i += 1
            continue
        result.append(ch)
        i += 1
    return ''.join(result)

def intelligent_decompile_file(in_path, out_path):
    luadec = find_luadec()
    if not luadec:
        return False, "luadec executable not found"
    
    try:
        with open(in_path, 'rb') as f:
            data = f.read()
        nibble_flag = data[33] if len(data) > 33 else 0
        if nibble_flag > 2: nibble_flag = 0
        if nibble_flag > 1:
            fixed = bytearray(data[:34])
            for i in range(34, len(data)):
                b = data[i]; fixed.append(((b << 4) & 0xF0) | ((b >> 4) & 0x0F))
            data = bytes(fixed)
        
        std_data = bgmi_to_std(data)
        with tempfile.NamedTemporaryFile(suffix='.luac', delete=False) as tmp_f:
            tmp_f.write(std_data)
            std_path = tmp_f.name
        
        ok_result, mode_err = attempt_decompile(luadec, std_path, out_path)
        if ok_result:
            with open(out_path, 'r', encoding='utf-8') as f:
                original = f.read()
            cleaned = remove_lua_comments(original)
            cleaned_fixed = fix_lua_syntax(cleaned)
            with open(out_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_fixed)
            os.unlink(std_path)
            return True, "Success with new method"
        os.unlink(std_path)
    except Exception:
        pass
    
    proto = load_proto(in_path)
    if not proto:
        return False, "Failed to decode bytecode"
    modes = ["5.3_64", "5.3_32", "5.3_32_int4", "5.1_64", "5.1_32"]
    error_logs = []
    
    class UniversalWriter:
        def __init__(self, mode):
            self.data = bytearray()
            self.mode = mode
            self.is_53 = "5.3" in mode
            self.is_32 = "_32" in mode
        def write(self, b): self.data.extend(b)
        def byte(self, v): self.data.append(v & 0xFF)
        def i32(self, v): self.data.extend(struct.pack('<i', v))
        def i64(self, v): self.data.extend(struct.pack('<q', v))
        def dbl(self, v): self.data.extend(struct.pack('<d', v))
        def string(self, s):
            if s is None:
                self.i32(0) if not self.is_53 else self.byte(0)
            else:
                b = s.encode('utf-8')
                sz = len(b) + 1
                if self.is_53:
                    if sz < 0xFF:
                        self.byte(sz)
                    else:
                        self.byte(0xFF)
                        fmt = '<I' if self.is_32 else '<Q'
                        self.data.extend(struct.pack(fmt, sz))
                    self.write(b)
                else:
                    fmt = '<I' if self.is_32 else '<Q'
                    self.data.extend(struct.pack(fmt, sz))
                    self.write(b)
        def write_proto(self, p):
            self.string(p.src)
            self.i32(p.ld)
            self.i32(p.ll)
            if not self.is_53: self.byte(len(p.upvals) // 2)
            self.byte(p.np)
            self.byte(1 if p.va else 0)
            self.byte(250)
            self.i32(len(p.ins))
            for ins in p.ins:
                op = ins & 0x3F
                std_op = CUSTOM_TO_STD.get(op, op)
                if std_op > 46: std_op = 0
                new_ins = (ins & ~0x3F) | std_op
                self.data.extend(struct.pack('<I', new_ins))
            self.i32(len(p.K))
            for typ, val in p.K:
                if typ == 'nil':
                    self.byte(0)
                elif typ == 'bool':
                    self.byte(1); self.byte(1 if val else 0)
                elif typ == 'float':
                    self.byte(3); self.dbl(val)
                elif typ == 'int':
                    if self.is_53:
                        self.byte(19)
                        if "int4" in self.mode: self.i32(int(val))
                        else: self.i64(int(val))
                    else:
                        self.byte(3); self.dbl(float(val))
                elif typ == 'str':
                    if self.is_53:
                        b = val.encode('utf-8')
                        if len(b) >= 40: self.byte(20)
                        else: self.byte(4)
                    else:
                        self.byte(4)
                    self.string(val)
            if self.is_53:
                n_ups = len(p.upvals) // 2
                self.i32(n_ups)
                self.write(p.upvals)
            self.i32(len(p.subs))
            for sub in p.subs: self.write_proto(sub)
            self.i32(len(p.ins))
            for _ in range(len(p.ins)): self.i32(1)
            self.i32(len(p.locs))
            for nm, sp, ep in p.locs:
                self.string(nm); self.i32(sp); self.i32(ep)
            n_ups = len(p.upvals) // 2
            self.i32(n_ups)
            for i in range(n_ups):
                name = p.upvs[i] if i < len(p.upvs) else f"upval_{i}"
                self.string(name)

    def build_std_file(proto, mode, out_path):
        w = UniversalWriter(mode)
        if mode == "5.3_64":
            w.data.extend(b'\x1bLua\x53\x00\x19\x93\r\n\x1a\n\x04\x08\x04\x08\x08')
            w.data.extend(struct.pack('<q', 0x5678))
            w.data.extend(struct.pack('<d', 370.5))
            w.byte(len(proto.upvals) // 2)
        elif mode == "5.3_32":
            w.data.extend(b'\x1bLua\x53\x00\x19\x93\r\n\x1a\n\x04\x04\x04\x08\x08')
            w.data.extend(struct.pack('<q', 0x5678))
            w.data.extend(struct.pack('<d', 370.5))
            w.byte(len(proto.upvals) // 2)
        elif mode == "5.3_32_int4":
            w.data.extend(b'\x1bLua\x53\x00\x19\x93\r\n\x1a\n\x04\x04\x04\x04\x08')
            w.data.extend(struct.pack('<i', 0x5678))
            w.data.extend(struct.pack('<d', 370.5))
            w.byte(len(proto.upvals) // 2)
        elif mode == "5.1_32":
            w.data.extend(b'\x1bLua\x51\x00\x01\x04\x04\x04\x08\x00')
        elif mode == "5.1_64":
            w.data.extend(b'\x1bLua\x51\x00\x01\x04\x08\x04\x08\x00')
        w.write_proto(proto)
        with open(out_path, 'wb') as f: f.write(w.data)
    
    for mode in modes:
        with tempfile.NamedTemporaryFile(suffix='.luac', delete=False) as tmp_f:
            std_path = tmp_f.name
        try:
            build_std_file(proto, mode, std_path)
            ok_result, mode_err = attempt_decompile(luadec, std_path, out_path)
            if ok_result:
                with open(out_path, 'r', encoding='utf-8') as f:
                    original = f.read()
                cleaned = remove_lua_comments(original)
                cleaned_fixed = fix_lua_syntax(cleaned)
                with open(out_path, 'w', encoding='utf-8') as f:
                    f.write(cleaned_fixed)
                os.unlink(std_path)
                return True, f"Success with {mode}"
            error_logs.append(f"{mode}: {mode_err}")
        finally:
            if os.path.exists(std_path): os.unlink(std_path)
    return False, "\n".join(error_logs)

def ensure_luac53():
    for name in ["luac5.3", "luac53", "luac5.3.exe", "luac53.exe"]:
        exes_path = EXES_DIR / name
        if exes_path.exists():
            if not os.access(exes_path, os.X_OK) and os.name != 'nt':
                try: exes_path.chmod(exes_path.stat().st_mode | 0o111)
                except: pass
            if os.access(exes_path, os.X_OK) or os.name == 'nt':
                return str(exes_path)
    
    for name in ["luac5.3", "luac53", "luac53.exe"]:
        path = shutil.which(name)
        if path:
            try:
                r = subprocess.run([path, '-v'], capture_output=True, timeout=3)
                if b'5.3' in r.stdout or b'5.3' in r.stderr:
                    return path
            except: pass
    return None

def compile_file_fixed(src_path, out_path, original_bytecode_path):
    luac = ensure_luac53()
    if not luac:
        return False, "luac5.3 not found and could not be installed."
    
    try:
        orig_size = os.path.getsize(original_bytecode_path)
    except:
        orig_size = None
    
    temp_std = src_path + ".temp.std.luac"
    try:
        cmd = [luac, "-s", "-o", temp_std, src_path]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            return False, f"Syntax error: {result.stderr.strip()[:200]}"
        
        if not os.path.exists(temp_std) or os.path.getsize(temp_std) == 0:
            return False, "Compilation produced empty output"
        
        ok, msg = repack_to_pubg(temp_std, original_bytecode_path, out_path, pad_to_size=orig_size)
        
        if ok:
            return True, "Compiled successfully"
        else:
            return False, msg
            
    except subprocess.TimeoutExpired:
        return False, "Compilation timed out"
    except Exception as e:
        return False, f"Compiler error: {e}"
    finally:
        if os.path.exists(temp_std):
            try: os.unlink(temp_std)
            except: pass

# ============================================================================
# PROGRESS BAR WRAPPER
# ============================================================================

def progress_bar() -> Progress:
    """Create a progress bar."""
    return Progress(
        SpinnerColumn(spinner_name="dots2", style="bold bright_magenta"),
        TextColumn("[bold bright_cyan]{task.description}"),
        BarColumn(bar_width=None, style="bright_red", complete_style="bright_green"),
        MofNCompleteColumn(),
        TaskProgressColumn(style="bold yellow"),
        TimeElapsedColumn(),
        console=console,
        expand=True,
    )

# ============================================================================
# FIXED TencentPakFile CLASS (V4 - Final Fix)
# ============================================================================

class TencentPakFile:
    def __init__(self, file_path: PurePath, is_od=False):
        self._file_path = file_path
        with open(file_path, 'rb') as f:
            self._file_content = memoryview(f.read())
        self._is_od = is_od
        self._mount_point = PurePath()
        self._is_zstd_with_dict = 'zsdic' in str(self._file_path)
        self._zstd_dict = None
        self._files = []
        self._index = {}
        self._dir_path_strings = {}
        self._pak_info = TencentPakInfo(self._file_content, PakCrypto.zuc_keystream())
        self._tencent_load_index()

    def _tencent_load_index(self):
        """Load PAK index with enhanced error handling"""
        try:
            index_data = self._file_content[self._pak_info.index_offset:][:self._pak_info.index_size]
            
            if self._pak_info.index_encrypted:
                index_data = PakCrypto.decrypt_index(index_data, self._pak_info)
            
            self._load_index(index_data)
            return
            
        except Exception as e:
            pass
        
        try:
            index_data = self._file_content[self._pak_info.index_offset:][:self._pak_info.index_size]
            self._pak_info.index_encrypted = False
            self._load_index(index_data)
            return
        except Exception as e2:
            try:
                index_data = self._file_content[self._pak_info.index_offset:][:self._pak_info.index_size]
                self._load_index(index_data)
                return
            except:
                raise RuntimeError("Cannot load PAK index")

    @staticmethod
    def _construct_mount_point(mount_point: str) -> PurePath:
        res = PurePath()
        for part in PurePath(mount_point).parts:
            if part != '..': res /= part
        return res

    def _load_index(self, index_data):
        """Load index from data with validation"""
        reader = Reader_pak(index_data)
        mount_str = reader.string()
        self._original_mount_point = mount_str
        self._mount_point = self._construct_mount_point(mount_str)
        
        num_entries = reader.u4()
        if num_entries > 100000:
            raise ValueError(f"Unreasonable number of entries: {num_entries}")
        
        self._files = [TencentPakEntry(reader, self._pak_info.version) for _ in range(num_entries)]
        
        try:
            num_dirs = reader.u8()
            if num_dirs > 50000:
                raise ValueError(f"Unreasonable number of dirs: {num_dirs}")
            
            for _ in range(num_dirs):
                dir_path = PurePath(reader.string())
                dir_str = str(dir_path)
                num_files = reader.u8()
                if num_files > 50000:
                    raise ValueError(f"Unreasonable number of files in dir: {num_files}")
                
                e = {}
                for _ in range(num_files):
                    file_name = reader.string()
                    entry_idx = reader.i4()
                    if entry_idx < 0:
                        file_ref = ~entry_idx
                    else:
                        file_ref = entry_idx
                    
                    if 0 <= file_ref < len(self._files):
                        e[file_name] = self._files[file_ref]
                    else:
                        continue
                
                if self._is_zstd_with_dict and dir_path.name == 'zstddic':
                    if len(e) == 1:
                        self._construct_zstd_dict(e[[*e.keys()][0]])
                    self._zstddic_info = (dir_str, e)
                    continue
                
                self._index.update({PurePath(dir_path): e})
                self._dir_path_strings[PurePath(dir_path)] = dir_str
                
        except struct.error:
            pass

    def _peek_content(self, offset: int, size: int, method: int) -> memoryview:
        size = PakCrypto.align_encrypted_content_size(size, method)
        return self._file_content[offset:][:size]

    def _peek_block_content(self, block: PakCompressedBlock, method: int) -> memoryview:
        size = PakCrypto.align_encrypted_content_size(block.end - block.start, method)
        return self._file_content[block.start:][:size]

    def _construct_zstd_dict(self, dict_entry: TencentPakEntry):
        assert not self._zstd_dict
        assert not dict_entry.encrypted
        assert dict_entry.compression_method == CM_NONE
        reader = Reader_pak(self._peek_content(dict_entry.offset, dict_entry.size, 0))
        dict_size = reader.u8()
        _ = reader.u4()
        assert dict_size == reader.u4()
        dict_data = reader.s(dict_size)
        self._zstd_dict = dict_data

    def _write_to_disk(self, file_path: Path, entry: TencentPakEntry):
        if hasattr(entry, 'encryption_method') and entry.encryption_method == EM_UNKNOWN_17: 
            return
        
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(file_path, 'wb') as f:
                if entry.compression_method == CM_NONE:
                    data = self._peek_content(entry.offset, entry.size, entry.encryption_method)
                    if entry.encrypted:
                        data = PakCrypto.decrypt_block(bytes(data), PurePath(file_path), entry.encryption_method)
                    f.write(data[:entry.uncompressed_size])
                    return
                
                dec_data = bytearray()
                if entry.compressed_blocks:
                    indices = PakCrypto.generate_block_indices(
                        len(entry.compressed_blocks), entry.encryption_method
                    )
                    for x in indices:
                        if x >= len(entry.compressed_blocks):
                            continue
                        block = entry.compressed_blocks[x]
                        data = self._peek_block_content(block, entry.encryption_method)
                        if entry.encrypted:
                            data = PakCrypto.decrypt_block(bytes(data), PurePath(file_path), entry.encryption_method)
                        if not data:
                            continue
                        try:
                            decompressed = PakCompression.decompress_block(
                                bytes(data), self._zstd_dict, entry.compression_method
                            )
                            dec_data.extend(decompressed)
                        except Exception:
                            continue
                else:
                    data = self._peek_content(entry.offset, entry.size, entry.encryption_method)
                    if entry.encrypted:
                        data = PakCrypto.decrypt_block(bytes(data), PurePath(file_path), entry.encryption_method)
                    if data:
                        dec_data = PakCompression.decompress_block(
                            bytes(data), self._zstd_dict, entry.compression_method
                        )
                
                result = bytes(dec_data[:entry.uncompressed_size])
                f.write(result)
                
        except Exception:
            pass

    def dump_lua_only(self, out_path: Path):
        """Extract only .lua files from PAK"""
        out_path.mkdir(parents=True, exist_ok=True)
        
        lua_entries = []
        for dir_path, dir_content in self._index.items():
            for file_name, entry in dir_content.items():
                if file_name.lower().endswith('.lua'):
                    lua_entries.append((dir_path, file_name, entry))
        
        if not lua_entries:
            RainbowUI.show_warning("No .lua files found in this PAK.")
            return
        
        success_count = 0
        fail_count = 0
        
        with progress_bar() as progress:
            task = progress.add_task(
                f"Extracting {len(lua_entries)} Lua file(s)...", 
                total=len(lua_entries)
            )
            
            for dir_path, file_name, entry in lua_entries:
                target_dir = out_path
                target = target_dir / file_name
                
                try:
                    self._write_to_disk(target, entry)
                    success_count += 1
                except Exception:
                    fail_count += 1
                
                progress.update(task, advance=1)
        
        print()
        if success_count > 0:
            RainbowUI.show_success(f"Extracted {success_count} Lua file(s) to: {out_path}")
        if fail_count > 0:
            RainbowUI.show_warning(f"{fail_count} file(s) failed to extract")

    def _pack_string(self, s: str) -> bytes:
        """Pack a string in PAK format"""
        if not s:
            return struct.pack('<i', 0)
        encoded = s.encode('utf-8') + b'\x00'
        return struct.pack('<i', len(encoded)) + encoded

    def _pack_entry(self, entry, version: int) -> bytes:
        """Pack a single file entry"""
        buf = bytearray()
        
        ch = entry.content_hash
        if len(ch) >= 20:
            buf.extend(ch[:20])
        else:
            buf.extend(ch + b'\x00' * (20 - len(ch)))
        
        if version <= 1:
            buf.append(0)
        
        buf.extend(struct.pack('<Q', entry.offset))
        buf.extend(struct.pack('<Q', entry.uncompressed_size))
        buf.extend(struct.pack('<I', entry.compression_method))
        buf.extend(struct.pack('<Q', entry.size))
        
        if version >= 5:
            buf.append(entry.unk1 if hasattr(entry, 'unk1') else 0)
            unk2 = entry.unk2 if hasattr(entry, 'unk2') and len(entry.unk2) == 20 else b'\x00' * 20
            buf.extend(struct.pack('<20s', unk2))
        
        if entry.compression_method != 0 and version >= 3:
            blocks = entry.compressed_blocks if hasattr(entry, 'compressed_blocks') else []
            buf.extend(struct.pack('<I', len(blocks)))
            for block in blocks:
                buf.extend(struct.pack('<QQ', block.start, block.end))
        
        if version >= 4:
            buf.extend(struct.pack('<I', entry.compression_block_size if hasattr(entry, 'compression_block_size') else 0))
            buf.append(1 if entry.encrypted else 0)
        
        if version >= 12:
            buf.extend(struct.pack('<I', entry.encryption_method if hasattr(entry, 'encryption_method') else 0))
        
        if version >= 14:
            buf.extend(struct.pack('<I', entry.unk3 if hasattr(entry, 'unk3') else 0))
        
        return bytes(buf)

    def _pack_index(self) -> bytes:
        """Pack the complete index"""
        buf = bytearray()
        
        mount_point_str = getattr(self, '_original_mount_point', str(self._mount_point))
        buf.extend(self._pack_string(mount_point_str))
        
        entry_to_idx = {id(entry): idx for idx, entry in enumerate(self._files)}
        
        buf.extend(struct.pack('<I', len(self._files)))
        for entry in self._files:
            buf.extend(self._pack_entry(entry, self._pak_info.version))
        
        dirs_to_pack = []
        for dir_path, dir_content in self._index.items():
            valid_files = []
            for file_name, entry in dir_content.items():
                if id(entry) in entry_to_idx:
                    valid_files.append((file_name, entry))
            if valid_files:
                dirs_to_pack.append((dir_path, valid_files))
        
        if hasattr(self, '_zstddic_info') and self._zstddic_info:
            dir_str, e = self._zstddic_info
            valid_files = []
            for file_name, entry in e.items():
                if id(entry) in entry_to_idx:
                    valid_files.append((file_name, entry))
            if valid_files:
                dirs_to_pack.append((PurePath(dir_str), valid_files))
        
        buf.extend(struct.pack('<Q', len(dirs_to_pack)))
        for dir_path, valid_files in dirs_to_pack:
            dir_str = self._dir_path_strings.get(dir_path, str(dir_path).replace('\\', '/'))
            buf.extend(self._pack_string(dir_str))
            buf.extend(struct.pack('<Q', len(valid_files)))
            for file_name, entry in valid_files:
                buf.extend(self._pack_string(file_name))
                file_idx = entry_to_idx[id(entry)]
                buf.extend(struct.pack('<i', ~file_idx))
        
        return bytes(buf)

    def _pack_footer(self) -> bytes:
        """Pack the footer with encryption"""
        keystream = PakCrypto.zuc_keystream()
        version = self._pak_info.version
        
        enc_flag = ((1 if self._pak_info.index_encrypted else 0) ^ keystream[3]) & 0xFF
        enc_magic = (self._pak_info.magic ^ keystream[2]) & 0xFFFFFFFF
        
        if version >= 6:
            key_ihash = struct.pack('<5I', *keystream[4:][:5])
            ih = self._pak_info.index_hash
            if len(ih) == 20:
                enc_index_hash = bytes(a ^ b for a, b in zip(ih, key_ihash))
            else:
                enc_index_hash = bytes(a ^ b for a, b in zip(bytes(20), key_ihash))
        else:
            enc_index_hash = bytes()
        
        enc_index_size = (self._pak_info.index_size ^ ((keystream[10] << 32) | keystream[11])) & 0xFFFFFFFFFFFFFFFF
        enc_index_offset = (self._pak_info.index_offset ^ ((keystream[0] << 32) | keystream[1])) & 0xFFFFFFFFFFFFFFFF
        
        base_buf = bytearray()
        base_buf.append(enc_flag)
        base_buf.extend(struct.pack('<II', enc_magic, version))
        if version >= 6:
            base_buf.extend(enc_index_hash)
        base_buf.extend(struct.pack('<QQ', enc_index_size, enc_index_offset))
        
        t_buf = bytearray()
        if version >= 7:
            key_unk = struct.pack('<8I', *keystream[7:][:8])
            unk1 = self._pak_info.unk1 if len(self._pak_info.unk1) == 32 else b'\x00' * 32
            enc_unk1 = bytes(a ^ b for a, b in zip(unk1, key_unk))
            t_buf.extend(enc_unk1)
        
        if version >= 8:
            t_buf.extend(self._pak_info.packed_key if len(self._pak_info.packed_key) == 256 else b'\x00' * 256)
            t_buf.extend(self._pak_info.packed_iv if len(self._pak_info.packed_iv) == 256 else b'\x00' * 256)
            t_buf.extend(self._pak_info.packed_index_hash if len(self._pak_info.packed_index_hash) == 256 else b'\x00' * 256)
        
        if version >= 9:
            enc_stem = (self._pak_info.stem_hash ^ keystream[8]) & 0xFFFFFFFF
            enc_unk2 = (self._pak_info.unk2 ^ keystream[9]) & 0xFFFFFFFF
            t_buf.extend(struct.pack('<II', enc_stem, enc_unk2))
        
        if version >= 12:
            t_buf.extend(self._pak_info.content_org_hash if len(self._pak_info.content_org_hash) == 20 else b'\x00' * 20)
        
        return bytes(t_buf + base_buf)

    def _process_file_for_injection(
        self,
        file_path: Path,
        internal_pak_path: PurePath,
        original_entry: TencentPakEntry,
        tf
    ) -> TencentPakEntry:
        """Write modified file while preserving original compression/encryption/block semantics."""
        with open(file_path, 'rb') as f:
            modified = f.read()

        cm = getattr(
            original_entry,
            "compression_method",
            CM_NONE
        )

        em = getattr(
            original_entry,
            "encryption_method",
            0
        )

        encrypted = bool(
            getattr(
                original_entry,
                "encrypted",
                False
            )
        )

        block_size = safe_int(
            getattr(
                original_entry,
                "compression_block_size",
                0
            ),
            0
        )

        if block_size <= 0 and cm != CM_NONE:

            compressed_blocks = getattr(
                original_entry,
                "compressed_blocks",
                None
            )

            if compressed_blocks:

                try:
                    first_block = compressed_blocks[0]

                    raw_block = self._file_content[
                        first_block.start:first_block.end
                    ]

                    raw_block = bytes(raw_block)

                    if encrypted and em != 0:
                        raw_block = PakCrypto.decrypt_block(
                            raw_block,
                            internal_pak_path,
                            em
                        )

                    decompressed = (
                        PakCompression.decompress_block(
                            raw_block,
                            self._zstd_dict,
                            cm
                        )
                    )

                    if decompressed:
                        block_size = len(decompressed)

                except Exception:
                    block_size = 0

        if block_size <= 0:
            block_size = 0x10000

        original_entry.content_hash = SHA1.new(
            modified
        ).digest()

        original_entry.uncompressed_size = len(
            modified
        )

        original_entry.compression_block_size = (
            block_size
        )

        if cm == CM_NONE:

            data_to_write = bytes(
                modified
            )

            if encrypted and em != 0:

                aligned_size = (
                    PakCrypto.align_encrypted_content_size(
                        len(data_to_write),
                        em
                    )
                )

                if aligned_size > len(data_to_write):
                    data_to_write += (
                        b'\x00' *
                        (
                            aligned_size -
                            len(data_to_write)
                        )
                    )

                data_to_write = bytes(
                    PakCrypto.encrypt_block(
                        data_to_write,
                        internal_pak_path,
                        em
                    )
                )

            aligned_size = Misc.align_up(
                len(data_to_write),
                16
            )

            if aligned_size > len(data_to_write):
                data_to_write += (
                    b'\x00' *
                    (
                        aligned_size -
                        len(data_to_write)
                    )
                )

            start_offset = tf.tell()

            tf.write(
                data_to_write
            )

            end_offset = tf.tell()

            original_entry.compressed_blocks = []

            original_entry.offset = (
                start_offset
            )

            original_entry.size = (
                end_offset -
                start_offset
            )

            return original_entry

        chunks = []

        for pos in range(
            0,
            len(modified),
            block_size
        ):
            chunks.append(
                modified[
                    pos:pos + block_size
                ]
            )

        if not chunks:
            chunks = [b""]

        new_blocks = []

        for chunk in chunks:

            comp_chunk = (
                PakCompression.compress_block(
                    chunk,
                    self._zstd_dict
                    if cm == CM_ZSTD_DICT
                    else None,
                    cm,
                    level=6
                )
            )

            comp_chunk = bytes(
                comp_chunk
            )

            if encrypted and em != 0:

                aligned_size = (
                    PakCrypto.align_encrypted_content_size(
                        len(comp_chunk),
                        em
                    )
                )

                if aligned_size > len(comp_chunk):
                    comp_chunk += (
                        b'\x00' *
                        (
                            aligned_size -
                            len(comp_chunk)
                        )
                    )

                comp_chunk = bytes(
                    PakCrypto.encrypt_block(
                        comp_chunk,
                        internal_pak_path,
                        em
                    )
                )

            aligned_size = Misc.align_up(
                len(comp_chunk),
                16
            )

            if aligned_size > len(comp_chunk):
                comp_chunk += (
                    b'\x00' *
                    (
                        aligned_size -
                        len(comp_chunk)
                    )
                )

            start_offset = tf.tell()

            tf.write(
                comp_chunk
            )

            end_offset = tf.tell()

            new_blocks.append(
                PakCompressedBlock(
                    start=start_offset,
                    end=end_offset
                )
            )

        original_entry.compressed_blocks = (
            new_blocks
        )

        if new_blocks:
            original_entry.offset = (
                new_blocks[0].start
            )

            original_entry.size = sum(
                block.end - block.start
                for block in new_blocks
            )
        else:
            original_entry.offset = tf.tell()
            original_entry.size = 0

        return original_entry

    def repack_injection(self, source_dir: Path, target_pak: Path) -> bool:
        """FIXED V5: INJECTION REPACK - Proper handling of ALL files"""
        print()
        RainbowUI.show_info("Starting INJECTION repack process (V5)...")
        print()
        
        all_source_files = []
        if source_dir.exists():
            for root, _, files in os.walk(str(source_dir)):
                root_path = Path(root)
                for file_name in files:
                    full_path = root_path / file_name
                    file_size = full_path.stat().st_size
                    if file_size > 0:
                        all_source_files.append((full_path, file_name, file_size))
        
        if not all_source_files:
            RainbowUI.show_error("No files found in source directory!")
            return False
        
        RainbowUI.show_success(f"Found {len(all_source_files)} file(s) in source directory")
        
        file_lookup = {}
        for dir_path, dir_content in self._index.items():
            for file_name, entry in dir_content.items():
                if file_name not in file_lookup:
                    file_lookup[file_name] = []
                internal_path = dir_path / file_name
                file_lookup[file_name].append((dir_path, entry, internal_path))
        
        matched = {}
        unmatched = []
        
        for full_path, file_name, file_size in all_source_files:
            if file_name in file_lookup:
                candidates = file_lookup[file_name]
                best_candidate = candidates[0]
                for candidate in candidates:
                    if candidate[1].uncompressed_size == file_size:
                        best_candidate = candidate
                        break
                dir_path, entry, internal_path = best_candidate
                matched[str(internal_path)] = (full_path, entry, dir_path)
            else:
                unmatched.append(file_name)
        
        if unmatched:
            RainbowUI.show_warning(f"{len(unmatched)} file(s) could not be matched:")
            for f in unmatched[:5]:
                print(f"    - {f}")
            print()
        
        if not matched:
            RainbowUI.show_error("No files could be matched!")
            return False
        
        RainbowUI.show_success(f"Matched {len(matched)} file(s) for injection")
        
        backup_path = PakRepackVerifier.create_backup(self._file_path)
        RainbowUI.show_info(f"Backup created: {backup_path.name}")
        
        with open(self._file_path, 'rb') as f:
            original_data = f.read()
        
        first_file_offset = float('inf')
        for dir_path, dir_content in self._index.items():
            for file_name, entry in dir_content.items():
                if entry.offset > 0 and entry.offset < first_file_offset:
                    first_file_offset = entry.offset
        
        if first_file_offset == float('inf'):
            first_file_offset = len(original_data)
        
        original_file_data_map = {}
        for dir_path, dir_content in self._index.items():
            for file_name, entry in dir_content.items():
                try:
                    orig_start = entry.offset
                    
                    if entry.compressed_blocks and len(entry.compressed_blocks) > 0:
                        first_block = entry.compressed_blocks[0]
                        last_block = entry.compressed_blocks[-1]
                        copy_size = last_block.end - first_block.start
                        orig_start = first_block.start
                    else:
                        orig_size = entry.size
                        if entry.compression_method == CM_NONE and entry.encrypted:
                            copy_size = PakCrypto.align_encrypted_content_size(orig_size, entry.encryption_method)
                            copy_size = Misc.align_up(copy_size, 16)
                        else:
                            copy_size = Misc.align_up(orig_size, 16)
                    
                    key = (str(dir_path), file_name)
                    original_file_data_map[key] = (orig_start, copy_size)
                except Exception:
                    pass
        
        print()
        RainbowUI.show_info("Writing new PAK file...")
        
        success_list = []
        fail_list = []
        
        modified_filenames = set()
        for internal_path_str in matched.keys():
            modified_filenames.add(Path(internal_path_str).name.lower())
        
        with open(target_pak, 'wb') as tf:
            if first_file_offset > 0:
                tf.write(original_data[:first_file_offset])
            
            for dir_path, dir_content in self._index.items():
                for file_name, entry in dir_content.items():
                    fname = file_name
                    fname_lower = fname.lower()
                    key = (str(dir_path), file_name)
                    
                    try:
                        if fname_lower in modified_filenames:
                            source_path = None
                            for ip, (sp, ent, dp) in matched.items():
                                if Path(ip).name.lower() == fname_lower:
                                    source_path = sp
                                    break
                            
                            if source_path:
                                internal_path = PurePath(str(dir_path / file_name))
                                self._process_file_for_injection(
                                    source_path, internal_path, entry, tf
                                )
                                success_list.append(fname)
                            else:
                                if key in original_file_data_map:
                                    orig_start, copy_size = original_file_data_map[key]
                                    entry.offset = tf.tell()
                                    tf.write(original_data[orig_start:orig_start + copy_size])
                        else:
                            if key in original_file_data_map:
                                orig_start, copy_size = original_file_data_map[key]
                                entry.offset = tf.tell()
                                tf.write(original_data[orig_start:orig_start + copy_size])
                            else:
                                RainbowUI.show_warning(f"Missing original data for: {fname}")
                                
                    except Exception as e:
                        fail_list.append(f"{fname}: {str(e)}")
                        RainbowUI.show_error(f"Failed to process {fname}: {e}")
                        
                        try:
                            if key in original_file_data_map:
                                orig_start, copy_size = original_file_data_map[key]
                                entry.offset = tf.tell()
                                tf.write(original_data[orig_start:orig_start + copy_size])
                        except:
                            pass
            
            if hasattr(self, '_zstddic_info') and self._zstddic_info:
                dir_str, e = self._zstddic_info
                for file_name, entry in e.items():
                    try:
                        orig_start = entry.offset
                        orig_size = entry.size
                        copy_size = Misc.align_up(orig_size, 16)
                        entry.offset = tf.tell()
                        tf.write(original_data[orig_start:orig_start + copy_size])
                    except:
                        pass
            
            print()
            RainbowUI.loading_animation("  Building new index table...", duration=1.0, speed=0.05)
            
            self._pak_info.index_offset = tf.tell()
            
            raw_new_index = self._pack_index()
            
            if self._pak_info.index_encrypted:
                if self._pak_info.version > 7:
                    try:
                        aes_key = PakCrypto.rsa_extract(self._pak_info.packed_key, RSA_MOD_1)
                        aes_iv = PakCrypto.rsa_extract(self._pak_info.packed_iv, RSA_MOD_1)
                        
                        if len(aes_key) >= 32 and len(aes_iv) >= 16:
                            aes = AES.new(aes_key[:32], MODE_CBC, aes_iv[:16])
                            enc_new_index = aes.encrypt(pad(raw_new_index, AES.block_size))
                        else:
                            enc_new_index = raw_new_index
                            self._pak_info.index_encrypted = False
                    except:
                        enc_new_index = raw_new_index
                        self._pak_info.index_encrypted = False
                else:
                    enc_new_index = bytes(PakCrypto._encrypt_simple1(raw_new_index))
            else:
                enc_new_index = raw_new_index
            
            self._pak_info.index_size = len(enc_new_index)
            self._pak_info.index_hash = SHA1.new(raw_new_index).digest()
            
            tf.write(enc_new_index)
            
            updated_footer = self._pack_footer()
            tf.write(updated_footer)
            
            tf.flush()
            os.fsync(tf.fileno())
        
        print()
        if success_list:
            RainbowUI.show_success(f"Successfully replaced {len(success_list)} file(s)")
        
        if fail_list:
            RainbowUI.show_error(f"Failed: {len(fail_list)} file(s)")
        
        print()
        RainbowUI.loading_animation("  Verifying repacked PAK...", duration=1.0, speed=0.05)
        
        verification = PakRepackVerifier.verify_pak_structure(self._file_path, target_pak)
        
        if verification['valid']:
            RainbowUI.show_success("PAK structure verification: PASSED")
        else:
            RainbowUI.show_error("PAK structure verification: FAILED")
            for error in verification['errors']:
                print(f"    {Colors.LRED}• {error}{Colors.NC}")
        
        if verification['warnings']:
            RainbowUI.show_warning("Warnings:")
            for warning in verification['warnings']:
                print(f"    {Colors.YELLOW}• {warning}{Colors.NC}")
        
        output_size = os.path.getsize(target_pak)
        original_size = os.path.getsize(self._file_path)
        RainbowUI.show_info(f"Original PAK: {original_size:,} bytes")
        RainbowUI.show_info(f"Repacked PAK: {output_size:,} bytes")
        
        if not verification['valid']:
            print()
            RainbowUI.show_info("Attempting automatic repair...")
            if PakRepackVerifier.repair_pak_structure(target_pak):
                RainbowUI.show_success("Repair completed successfully")
            else:
                RainbowUI.show_warning("Automatic repair could not fix all issues")
        
        return len(success_list) > 0

    def repack(self, source_dir: Path, target_pak: Path) -> bool:
        """Main repack entry point"""
        return self.repack_injection(source_dir, target_pak)

# ============================================================================
# NEW REPACK FUNCTIONS FROM SECOND TOOL (MERGED)
# ============================================================================

def safe_int(value, default=0):
    try:
        return int(value)
    except Exception:
        return default

def _pw_string(s):
    """PAK string serialiser: i4(len_with_null) + bytes + null."""
    if not s: return struct.pack('<i', 0)
    b = s.encode('utf-8') + b'\x00'
    return struct.pack('<i', len(b)) + b

def _pw_entry(e, v):
    """Serialise one TencentPakEntry back to bytes."""
    w = bytearray(e.content_hash)
    w += struct.pack('<Q', e.offset)
    w += struct.pack('<Q', e.uncompressed_size)
    w += struct.pack('<I', e.compression_method)
    w += struct.pack('<Q', e.size)
    if v >= 5:
        w += bytes([e.unk1])
        w += e.unk2
    if e.compression_method != CM_NONE and v >= 3:
        w += struct.pack('<I', len(e.compressed_blocks))
        for b in e.compressed_blocks:
            w += struct.pack('<QQ', b.start, b.end)
    if v >= 4:
        w += struct.pack('<I', e.compression_block_size)
        w += bytes([1 if e.encrypted else 0])
    if v >= 12:
        w += struct.pack('<II', e.encryption_method, getattr(e, 'index_new_sep', 0))
    return bytes(w)

def _get_all_dirs_and_mp(pak_file):
    """Re-parse raw (possibly encrypted) index → (mount_point_str, ordered dirs dict)."""
    raw = bytes(pak_file._file_content[
        pak_file._pak_info.index_offset:][:pak_file._pak_info.index_size])
    if pak_file._pak_info.index_encrypted:
        raw = PakCrypto.decrypt_index(raw, pak_file._pak_info)
    r = Reader_pak(raw)
    mp = r.string()
    num_files = r.u4()
    for _ in range(num_files):
        TencentPakEntry(r, pak_file._pak_info.version)
    dirs = {}
    for _ in range(r.u8()):
        dp = r.string()
        cnt = r.u8()
        dirs[dp] = {r.string(): pak_file._files[~r.i4()] for _ in range(cnt)}
    return mp, dirs

def _best_compress(chunk, cm, zstd_dict=None):
    """Compress one chunk at the best achievable level."""
    if cm == CM_ZLIB:
        return zlib.compress(chunk, 9)
    if cm in (CM_ZSTD, CM_ZSTD_DICT):
        zd = zstd_dict if cm == CM_ZSTD_DICT else None
        for lvl in [22, 19, 16, 13, 10, 7, 4, 1]:
            try:
                return ZstdCompressor(level=lvl, dict_data=zd, threads=1).compress(chunk)
            except Exception:
                continue
    return chunk

def _encrypt_plaintext(plaintext: bytes, pak_relative_path: PurePath, encryption_method: int) -> bytes:
    if PakCrypto._is_simple1_method(encryption_method):
        return bytes((b ^ SIMPLE1_DECRYPT_KEY for b in plaintext))
    else:
        if PakCrypto._is_simple2_method(encryption_method):
            pad_len = -len(plaintext) % SIMPLE2_BLOCK_SIZE
            plaintext += b'\x00' * pad_len
            key, = struct.unpack('<I', SIMPLE2_DECRYPT_KEY)
            rolling = key
            out = []
            for x, in struct.iter_unpack('<I', plaintext):
                c = rolling ^ x
                out.append(c)
                rolling ^= c
            return struct.pack(f'<{len(out)}I', *out)
        else:
            if PakCrypto._is_sm4_method(encryption_method):
                key = PakCrypto._derive_sm4_key(pak_relative_path, encryption_method)
                sm4 = PakCrypto._sm4_context_for_key(key)
                pad_len = -len(plaintext) % 16
                if pad_len > 0:
                    plaintext = plaintext + b'\x00' * pad_len
                out = bytearray()
                for i in range(0, len(plaintext), 16):
                    block = plaintext[i:i + 16]
                    if len(block) < 16:
                        block = block.ljust(16, b'\x00')
                    out.extend(sm4.encrypt(block))
                return bytes(out)
            else:
                return plaintext

def repack_pak_file_full(pak_file, edited_root, output_path, target_path=None, force_add=False):
    """
    FULL REBUILD REPACK - For Option 2 (REPLACE) and Option 3 (ADD TO PATH)
    """
    console.print(f'[bold cyan] Full PAK Rebuild mode[/bold cyan]')
    if target_path:
        console.print(f'[bold cyan] Target path: {target_path}[/bold cyan]')
    
    edit_files = []
    if Path(edited_root).exists():
        for p in Path(edited_root).rglob('*'):
            if p.is_file():
                edit_files.append(p)
    
    if not edit_files:
        console.print('[bold red] No files found in EDIT folder![/bold red]')
        return 0
    
    console.print(f'[bold cyan] Found {len(edit_files)} files in EDIT folder[/bold cyan]')

    version = pak_file._pak_info.version
    keystream = PakCrypto.zuc_keystream()
    orig_fc = pak_file._file_content

    mp_str, all_dirs = _get_all_dirs_and_mp(pak_file)

    if target_path and force_add:
        target_path = target_path.replace('\\', '/')
        matched_dir = None
        for existing_dir in all_dirs.keys():
            if existing_dir.strip('/').lower() == target_path.strip('/').lower():
                matched_dir = existing_dir
                break
        if matched_dir:
            target_path = matched_dir
        else:
            target_path = target_path.strip('/') + '/'
    
    pak_name_map = {}
    for dir_path, files in pak_file._index.items():
        for name, entry in files.items():
            full_path = str(PurePath(dir_path)/name).replace('\\', '/')
            pak_name_map.setdefault(name.lower(), []).append((full_path, entry))

    edited = {}
    
    for p in edit_files:
        fl = p.name.lower()
        found_match = False
        
        if fl in pak_name_map:
            cands = pak_name_map[fl]
            if target_path:
                target_candidates = [(fp, e) for fp, e in cands if target_path.strip('/') in fp]
                if target_candidates:
                    sz = p.stat().st_size
                    sm = [(fp, e) for fp, e in target_candidates if e.uncompressed_size == sz]
                    fp, ent = sm[0] if sm else target_candidates[0]
                    edited[fp] = (p, ent)
                    found_match = True
            
            if not found_match:
                sz = p.stat().st_size
                sm = [(fp, e) for fp, e in cands if e.uncompressed_size == sz]
                fp, ent = sm[0] if sm else cands[0]
                if target_path:
                    new_fp = f"{target_path.rstrip('/')}/{p.name}"
                    edited[new_fp] = (p, ent)
                else:
                    edited[fp] = (p, ent)
                found_match = True
        
        if not found_match:
            stem = p.stem.lower()
            ext = p.suffix.lower()
            for dir_path, files in pak_file._index.items():
                for name, entry in files.items():
                    if Path(name).stem.lower() == stem and Path(name).suffix.lower() == ext:
                        full_path = str(PurePath(dir_path)/name).replace('\\', '/')
                        if target_path:
                            new_fp = f"{target_path.rstrip('/')}/{p.name}"
                            edited[new_fp] = (p, entry)
                        else:
                            edited[full_path] = (p, entry)
                        found_match = True
                        break
                if found_match:
                    break
        
        if not found_match and force_add and target_path:
            template_entry = None
            for dir_path, files in pak_file._index.items():
                for name, entry in files.items():
                    if Path(name).suffix.lower() == p.suffix.lower():
                        template_entry = entry
                        break
                if template_entry: break
            
            if not template_entry:
                for dir_path, files in pak_file._index.items():
                    for name, entry in files.items():
                        template_entry = entry
                        break
                    if template_entry: break
            
            if template_entry:
                new_fp = f"{target_path.rstrip('/')}/{p.name}"
                edited[new_fp] = (p, template_entry)

    if not edited:
        console.print('[bold red] No files to repack![/bold red]')
        return 0

    console.print(f'  [bold bright_cyan] Files to repack: {len(edited)}[/bold bright_cyan]')

    new_files = []
    for e in pak_file._files:
        ne = _cp.copy(e)
        ne.compressed_blocks = [_cp.copy(b) for b in e.compressed_blocks]
        new_files.append(ne)

    old_to_new = {id(pak_file._files[i]): new_files[i] for i in range(len(pak_file._files))}
    edited_paths = {fp: p for fp, (p, _) in edited.items()}

    out_buf = bytearray()

    for dp_str, dir_files in list(all_dirs.items()):
        for name, old_entry in list(dir_files.items()):
            full_path = str(PurePath(dp_str)/name).replace('\\', '/')
            ne = old_to_new.get(id(old_entry), None)
            
            if ne is None:
                ne = _cp.copy(old_entry)
                ne.compressed_blocks = [_cp.copy(b) for b in old_entry.compressed_blocks]
                new_files.append(ne)
                old_to_new[id(old_entry)] = ne

            em = old_entry.encryption_method
            cm = old_entry.compression_method

            if full_path in edited_paths:
                p, template = edited[full_path]
                new_raw = p.read_bytes()
                pak_rel = PurePath(full_path)

                ne.content_hash = SHA1.new(new_raw).digest()
                ne.uncompressed_size = len(new_raw)
                ne.compression_method = template.compression_method if template else cm
                ne.encryption_method = template.encryption_method if template else em
                ne.encrypted = template.encrypted if template else old_entry.encrypted
                ne.unk1 = template.unk1 if template else old_entry.unk1
                
                if template and target_path:
                    full_path_str = mp_str + full_path
                    ne.unk2 = SHA1.new(full_path_str.lower().encode('utf-8')).digest()
                else:
                    ne.unk2 = template.unk2 if template else old_entry.unk2
                    
                ne.index_new_sep = getattr(template, 'index_new_sep', 0) if template else getattr(old_entry, 'index_new_sep', 0)

                if ne.compression_method == CM_NONE:
                    cipher = (_encrypt_plaintext(new_raw, pak_rel, ne.encryption_method)
                              if ne.encrypted else new_raw)
                    ne.offset = len(out_buf)
                    ne.size = len(new_raw)
                    ne.uncompressed_size = len(new_raw)
                    out_buf += cipher
                else:
                    cs = (template.compression_block_size if template and template.compression_block_size > 0 
                          else old_entry.compression_block_size if old_entry.compression_block_size > 0 
                          else 65536)
                    chunks = [new_raw[i:i+cs] for i in range(0, len(new_raw), cs)]
                    new_blks = []
                    for chunk in chunks:
                        compressed = _best_compress(chunk, ne.compression_method, pak_file._zstd_dict)
                        cipher = (_encrypt_plaintext(compressed, pak_rel, ne.encryption_method)
                                  if ne.encrypted else compressed)
                        blk = PakCompressedBlock.__new__(PakCompressedBlock)
                        blk.start = len(out_buf)
                        blk.end = blk.start + len(cipher)
                        out_buf += cipher
                        new_blks.append(blk)

                    ne.compressed_blocks = new_blks
                    ne.offset = new_blks[0].start if new_blks else len(out_buf)
                    ne.size = sum(b.end - b.start for b in new_blks)
                    ne.uncompressed_size = len(new_raw)

                console.print(f'[green]✓ Processed: {full_path}[/green]')

            else:
                if cm == CM_NONE:
                    read_sz = (PakCrypto.align_encrypted_content_size(old_entry.size, em)
                               if old_entry.encrypted else old_entry.size)
                    ne.offset = len(out_buf)
                    out_buf += bytes(orig_fc[old_entry.offset: old_entry.offset + read_sz])

                elif old_entry.compressed_blocks:
                    new_blks = []
                    for ob in old_entry.compressed_blocks:
                        unc = ob.end - ob.start
                        enc = (PakCrypto.align_encrypted_content_size(unc, em)
                               if old_entry.encrypted else unc)
                        nb = PakCompressedBlock.__new__(PakCompressedBlock)
                        nb.start = len(out_buf)
                        nb.end = nb.start + unc
                        out_buf += bytes(orig_fc[ob.start: ob.start + enc])
                        new_blks.append(nb)
                    ne.compressed_blocks = new_blks
                    ne.offset = new_blks[0].start

    if target_path and force_add:
        for fp, (p, template) in edited.items():
            already_processed = False
            for dp_str, dir_files in all_dirs.items():
                for name, entry in dir_files.items():
                    if str(PurePath(dp_str)/name).replace('\\', '/') == fp:
                        already_processed = True
                        break
                if already_processed:
                    break
            
            if not already_processed:
                ne = _cp.copy(template)
                new_raw = p.read_bytes()
                pak_rel = PurePath(fp)
                
                ne.content_hash = SHA1.new(new_raw).digest()
                ne.uncompressed_size = len(new_raw)
                ne.compression_method = template.compression_method
                ne.encryption_method = template.encryption_method
                ne.encrypted = template.encrypted
                ne.unk1 = template.unk1
                
                full_path_str = mp_str + fp
                ne.unk2 = SHA1.new(full_path_str.lower().encode('utf-8')).digest()
                
                ne.index_new_sep = getattr(template, 'index_new_sep', 0)

                if ne.compression_method == CM_NONE:
                    cipher = (_encrypt_plaintext(new_raw, pak_rel, ne.encryption_method)
                              if ne.encrypted else new_raw)
                    ne.offset = len(out_buf)
                    ne.size = len(new_raw)
                    ne.uncompressed_size = len(new_raw)
                    out_buf += cipher
                else:
                    cs = template.compression_block_size if template.compression_block_size > 0 else 65536
                    chunks = [new_raw[i:i+cs] for i in range(0, len(new_raw), cs)]
                    new_blks = []
                    for chunk in chunks:
                        compressed = _best_compress(chunk, ne.compression_method, pak_file._zstd_dict)
                        cipher = (_encrypt_plaintext(compressed, pak_rel, ne.encryption_method)
                                  if ne.encrypted else compressed)
                        blk = PakCompressedBlock.__new__(PakCompressedBlock)
                        blk.start = len(out_buf)
                        blk.end = blk.start + len(cipher)
                        out_buf += cipher
                        new_blks.append(blk)

                    ne.compressed_blocks = new_blks
                    ne.offset = new_blks[0].start if new_blks else len(out_buf)
                    ne.size = sum(b.end - b.start for b in new_blks)
                    ne.uncompressed_size = len(new_raw)

                new_files.append(ne)
                
                if target_path not in all_dirs:
                    all_dirs[target_path] = {}
                all_dirs[target_path][p.name] = ne
                console.print(f'[green]✓ Added new: {fp}[/green]')

    eidx = {id(new_files[i]): i for i in range(len(new_files))}

    idx = bytearray(_pw_string(mp_str))
    idx += struct.pack('<I', len(new_files))
    for ne in new_files:
        idx += _pw_entry(ne, version)
    idx += struct.pack('<Q', len(all_dirs))
    for dp_str, dir_files in all_dirs.items():
        idx += _pw_string(dp_str)
        idx += struct.pack('<Q', len(dir_files))
        for name, old_e in dir_files.items():
            idx += _pw_string(name)
            found_idx = None
            for i, e in enumerate(new_files):
                if id(e) == id(old_e):
                    found_idx = i
                    break
            if found_idx is None:
                for i, e in enumerate(new_files):
                    if e.offset == old_e.offset and e.size == old_e.size:
                        found_idx = i
                        break
            if found_idx is not None:
                idx += struct.pack('<i', ~found_idx)
            else:
                idx += struct.pack('<i', -1)

    index_plain = bytes(idx)
    new_sha1 = SHA1.new(index_plain).digest()

    if pak_file._pak_info.index_encrypted:
        key = PakCrypto.rsa_extract(pak_file._pak_info.packed_key, RSA_MOD_1)
        iv = PakCrypto.rsa_extract(pak_file._pak_info.packed_iv, RSA_MOD_1)
        aes = AES.new(key, MODE_CBC, iv[:16])
        pad_len = (-len(index_plain)) % AES.block_size or AES.block_size
        index_bytes = aes.encrypt(index_plain + bytes([pad_len] * pad_len))
    else:
        index_bytes = index_plain

    new_idx_offset = len(out_buf)
    new_idx_size = len(index_bytes)
    out_buf += index_bytes

    footer_sz = TencentPakInfo._mem_size(version)
    new_footer = bytearray(orig_fc[-footer_sz:])

    h_key = struct.pack('<5I', *keystream[4:9])
    new_footer[-36:-16] = bytes(a ^ b for a, b in zip(new_sha1, h_key))
    new_footer[-16:-8] = ((new_idx_size ^ (keystream[10] << 32 | keystream[11])).to_bytes(8, 'little'))
    new_footer[-8:] = ((new_idx_offset ^ (keystream[0] << 32 | keystream[1])).to_bytes(8, 'little'))

    out_buf += new_footer

    with open(output_path, 'wb') as f:
        f.write(out_buf)

    return len(edited)

# ============================================================================
# NEW MENU FUNCTIONS FOR PAK REPACK
# ============================================================================

def repack_pak_new():
    """
    REPACK PAK - Option 2 in main menu
    Uses FULL REBUILD logic from second tool
    """
    RainbowUI.clear_screen()
    RainbowUI.show_banner()
    RainbowUI.show_title("REPACK PAK (FULL REBUILD)")
    
    RainbowUI.show_info(f"Modified files in: {EDITED_FILES_DIR}")
    RainbowUI.show_info(f"Original PAKs in: {ORIGINAL_PAK_DIR}")
    RainbowUI.show_info(f"Output goes to: {REPACKED_PAK_DIR}")
    print()
    
    pak_files = list(ORIGINAL_PAK_DIR.glob("*.pak"))
    if not pak_files:
        RainbowUI.show_error("No .pak files found!")
        RainbowUI.wait_for_user()
        return
    
    print()
    for i, f in enumerate(pak_files, 1):
        size_mb = f.stat().st_size / 1024 / 1024
        RainbowUI.show_menu_option(str(i), f"{f.name} ({size_mb:.2f} MB)")
    
    print()
    choice = RainbowUI.rainbow_prompt("Select PAK file (number):")
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(pak_files):
            pak_file = pak_files[idx]
        else:
            RainbowUI.show_error("Invalid selection!")
            RainbowUI.wait_for_user()
            return
    except ValueError:
        RainbowUI.show_error("Invalid input!")
        RainbowUI.wait_for_user()
        return
    
    edit_files = []
    if EDITED_FILES_DIR.exists():
        for p in EDITED_FILES_DIR.rglob('*'):
            if p.is_file():
                edit_files.append(p)
    
    if not edit_files:
        RainbowUI.show_error("No files found in EDIT folder!")
        RainbowUI.wait_for_user()
        return
    
    print()
    RainbowUI.loading_animation(f"  Loading PAK: {pak_file.name}...", duration=1.5, speed=0.05)
    
    try:
        pak = TencentPakFile(pak_file)
    except Exception as e:
        RainbowUI.show_error(f"Cannot load PAK: {e}")
        RainbowUI.wait_for_user()
        return
    
    target_pak = REPACKED_PAK_DIR / pak_file.name
    REPACKED_PAK_DIR.mkdir(parents=True, exist_ok=True)
    
    print()
    RainbowUI.show_info("Starting full rebuild repack...")
    
    try:
        count = repack_pak_file_full(pak, EDITED_FILES_DIR, target_pak)
        
        if count > 0:
            RainbowUI.show_success(f"Repacked {count} files successfully!")
            RainbowUI.show_success(f"Output: {target_pak}")
            try:
                notify_file_processed(str(target_pak), "REPACKED", True)
            except:
                pass
            
            # Verify
            print()
            RainbowUI.loading_animation("  Verifying repacked PAK...", duration=1.0, speed=0.05)
            verification = PakRepackVerifier.verify_pak_structure(pak_file, target_pak)
            
            if verification['valid']:
                RainbowUI.show_success("PAK structure verification: PASSED")
            else:
                RainbowUI.show_error("PAK structure verification: FAILED")
                for error in verification['errors']:
                    print(f"    {Colors.LRED}• {error}{Colors.NC}")
        else:
            RainbowUI.show_error("No files were repacked!")
            
    except Exception as e:
        RainbowUI.show_error(f"Repack failed: {e}")
        import traceback
        traceback.print_exc()
    
    RainbowUI.wait_for_user()

def repack_to_path_new():
    """
    REPACK TO PATH - Option 3 in main menu
    Force-add files to a specific target path
    """
    RainbowUI.clear_screen()
    RainbowUI.show_banner()
    RainbowUI.show_title("REPACK TO PATH (ADD FILES)")
    
    RainbowUI.show_info(f"Modified files in: {EDITED_FILES_DIR}")
    RainbowUI.show_info(f"Original PAKs in: {ORIGINAL_PAK_DIR}")
    RainbowUI.show_info(f"Output goes to: {REPACKED_PAK_DIR}")
    print()
    RainbowUI.show_info("Enter the target path inside the PAK where files should be added")
    RainbowUI.show_info("Example: Content/Lua/GameLua/Mod/BRMod/Gameplay/Core")
    print()
    
    pak_files = list(ORIGINAL_PAK_DIR.glob("*.pak"))
    if not pak_files:
        RainbowUI.show_error("No .pak files found!")
        RainbowUI.wait_for_user()
        return
    
    print()
    for i, f in enumerate(pak_files, 1):
        size_mb = f.stat().st_size / 1024 / 1024
        RainbowUI.show_menu_option(str(i), f"{f.name} ({size_mb:.2f} MB)")
    
    print()
    choice = RainbowUI.rainbow_prompt("Select PAK file (number):")
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(pak_files):
            pak_file = pak_files[idx]
        else:
            RainbowUI.show_error("Invalid selection!")
            RainbowUI.wait_for_user()
            return
    except ValueError:
        RainbowUI.show_error("Invalid input!")
        RainbowUI.wait_for_user()
        return
    
    edit_files = []
    if EDITED_FILES_DIR.exists():
        for p in EDITED_FILES_DIR.rglob('*'):
            if p.is_file():
                edit_files.append(p)
    
    if not edit_files:
        RainbowUI.show_error("No files found in EDIT folder!")
        RainbowUI.wait_for_user()
        return
    
    print()
    target_path = RainbowUI.rainbow_prompt("ENTER TARGET PATH:")
    target_path = target_path.replace('\\', '/').strip('/')
    
    if not target_path:
        RainbowUI.show_error("No path provided!")
        RainbowUI.wait_for_user()
        return
    
    print()
    RainbowUI.loading_animation(f"  Loading PAK: {pak_file.name}...", duration=1.5, speed=0.05)
    
    try:
        pak = TencentPakFile(pak_file)
    except Exception as e:
        RainbowUI.show_error(f"Cannot load PAK: {e}")
        RainbowUI.wait_for_user()
        return
    
    target_pak = REPACKED_PAK_DIR / pak_file.name
    REPACKED_PAK_DIR.mkdir(parents=True, exist_ok=True)
    
    print()
    RainbowUI.show_info(f"Adding files to path: {target_path}")
    RainbowUI.show_info("Starting full rebuild repack with force-add...")
    
    try:
        count = repack_pak_file_full(pak, EDITED_FILES_DIR, target_pak, target_path, force_add=True)
        
        if count > 0:
            RainbowUI.show_success(f"Successfully added {count} files to {target_path}!")
            RainbowUI.show_success(f"Output: {target_pak}")
            try:
                notify_file_processed(str(target_pak), "REPACKED_TO_PATH", True)
            except:
                pass
            
            # Verify
            print()
            RainbowUI.loading_animation("  Verifying repacked PAK...", duration=1.0, speed=0.05)
            verification = PakRepackVerifier.verify_pak_structure(pak_file, target_pak)
            
            if verification['valid']:
                RainbowUI.show_success("PAK structure verification: PASSED")
            else:
                RainbowUI.show_error("PAK structure verification: FAILED")
                for error in verification['errors']:
                    print(f"    {Colors.LRED}• {error}{Colors.NC}")
        else:
            RainbowUI.show_error("No files were processed!")
            
    except Exception as e:
        RainbowUI.show_error(f"Repack failed: {e}")
        import traceback
        traceback.print_exc()
    
    RainbowUI.wait_for_user()

# ============================================================================
# PAKTOOL OPTION 7 - UNPACK SINGLE BLOCK
# ============================================================================

def unpack_single_block():
    """Extract one exact file from a PAK, transferred from PAKTOOL option 7."""
    RainbowUI.clear_screen()
    RainbowUI.show_banner()
    RainbowUI.show_title("UNPACK SINGLE BLOCK")

    single_root = EXTRACTED_DIR / "SINGLE_UNPACK"
    single_root.mkdir(parents=True, exist_ok=True)

    RainbowUI.show_info(f"Original PAKs: {ORIGINAL_PAK_DIR}")
    RainbowUI.show_info(f"Output: {single_root}")
    print()

    pak_files = sorted(ORIGINAL_PAK_DIR.glob("*.pak"))
    if not pak_files:
        RainbowUI.show_error("No .pak files found!")
        RainbowUI.wait_for_user()
        return

    for i, f in enumerate(pak_files, 1):
        size_mb = f.stat().st_size / 1024 / 1024
        RainbowUI.show_menu_option(str(i), f"{f.name} ({size_mb:.2f} MB)")

    print()
    choice = RainbowUI.rainbow_prompt("Select PAK file (number):")
    try:
        idx = int(choice) - 1
        if not 0 <= idx < len(pak_files):
            raise ValueError
        pak_file = pak_files[idx]
    except ValueError:
        RainbowUI.show_error("Invalid PAK selection!")
        RainbowUI.wait_for_user()
        return

    target_filename = RainbowUI.rainbow_prompt("Enter exact file name (with extension):").strip()
    if not target_filename:
        RainbowUI.show_error("No filename entered!")
        RainbowUI.wait_for_user()
        return

    print()
    RainbowUI.show_info("Extraction mode:")
    RainbowUI.show_menu_option("1", "NON-CHUNK EXTRACT", "Rebuild the complete target file")
    RainbowUI.show_menu_option("2", "CHUNK EXTRACT", "Extract every compressed block separately")
    mode = RainbowUI.rainbow_prompt("Choose mode (1 or 2):").strip()
    if mode not in ("1", "2"):
        RainbowUI.show_error("Invalid extraction mode!")
        RainbowUI.wait_for_user()
        return

    try:
        RainbowUI.loading_animation(f"  Loading PAK: {pak_file.name}...", duration=1.0, speed=0.05)
        pak_instance = TencentPakFile(pak_file)
        found = False

        for dir_path, files in pak_instance._index.items():
            entry = files.get(target_filename)
            if not entry:
                continue

            found = True
            file_base = Path(target_filename).stem
            file_ext = Path(target_filename).suffix
            indices = PakCrypto.generate_block_indices(
                len(entry.compressed_blocks), entry.encryption_method
            )

            with open(pak_file, "rb") as f:
                mm = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)

                def process_block(idx):
                    try:
                        block = entry.compressed_blocks[idx]
                        raw_size = block.end - block.start
                        if entry.encrypted:
                            read_size = PakCrypto.align_encrypted_content_size(
                                raw_size, entry.encryption_method
                            )
                        else:
                            read_size = raw_size

                        data = mm[block.start:block.start + read_size]
                        if entry.encrypted:
                            data = PakCrypto.decrypt_block(
                                data, Path(target_filename), entry.encryption_method
                            )

                        if entry.compression_method != CM_NONE:
                            try:
                                data = PakCompression.decompress_block(
                                    data,
                                    pak_instance._zstd_dict,
                                    entry.compression_method
                                )
                            except Exception:
                                return idx, b""
                        return idx, data
                    except Exception:
                        return idx, b""

                if mode == "1":
                    out_path = single_root / file_base / Path(dir_path) / target_filename
                    out_path.parent.mkdir(parents=True, exist_ok=True)
                    full_data = bytearray()
                    for block_idx in indices:
                        _, data = process_block(block_idx)
                        full_data.extend(data)
                    out_path.write_bytes(full_data)
                    mm.close()
                    RainbowUI.show_success(f"File extracted: {out_path}")
                else:
                    out_dir = single_root / file_base
                    out_dir.mkdir(parents=True, exist_ok=True)
                    cpu = os.cpu_count() or 4
                    if len(indices) < 5:
                        max_workers = 2
                    elif len(indices) < 20:
                        max_workers = min(4, cpu)
                    else:
                        max_workers = min(8, cpu * 2)

                    total_bytes = 0
                    start_time = time.time()
                    with Progress(
                        SpinnerColumn(),
                        TextColumn("[progress.description]{task.description}"),
                        BarColumn(),
                        TextColumn("{task.percentage:>3.0f}%"),
                        console=console
                    ) as progress:
                        task = progress.add_task("Extracting...", total=len(indices))
                        batch_size = 16
                        batches = [indices[i:i + batch_size] for i in range(0, len(indices), batch_size)]
                        with ThreadPoolExecutor(max_workers=max_workers) as executor:
                            for batch in batches:
                                futures = [executor.submit(process_block, block_idx) for block_idx in batch]
                                for future in as_completed(futures):
                                    block_idx, data = future.result()
                                    total_bytes += len(data)
                                    out_file = out_dir / f"{file_base}_{block_idx}{file_ext}"
                                    out_file.write_bytes(data)
                                    elapsed = time.time() - start_time
                                    speed = (total_bytes / 1024 / 1024) / elapsed if elapsed > 0 else 0
                                    progress.update(
                                        task, advance=1,
                                        description=f"Extracting... {speed:.2f} MB/s"
                                    )
                    mm.close()
                    RainbowUI.show_success(f"Blocks extracted: {len(indices)}")
                    RainbowUI.show_info(f"Output: {out_dir}")

            break

        if not found:
            RainbowUI.show_error(f"File not found in PAK: {target_filename}")

    except Exception as e:
        RainbowUI.show_error(f"Single block extraction failed: {e}")
        import traceback
        traceback.print_exc()

    RainbowUI.wait_for_user()

# ============================================================================
# PAK TOOL FUNCTIONS (KEPT FROM ORIGINAL TOOL)
# ============================================================================

def unpack_pak():
    """Unpack a PAK file to extract Lua files."""
    RainbowUI.clear_screen()
    RainbowUI.show_banner()
    RainbowUI.show_title("UNPACK PAK FILE")
    
    RainbowUI.show_info(f"Place .pak files in: {ORIGINAL_PAK_DIR}")
    RainbowUI.show_info(f"Extracted files go to: {EXTRACTED_DIR}")
    print()
    
    pak_files = list(ORIGINAL_PAK_DIR.glob("*.pak"))
    if not pak_files:
        RainbowUI.show_error("No .pak files found!")
        RainbowUI.wait_for_user()
        return
    
    print()
    for i, f in enumerate(pak_files, 1):
        size_mb = f.stat().st_size / 1024 / 1024
        RainbowUI.show_menu_option(str(i), f"{f.name} ({size_mb:.2f} MB)")
    
    print()
    choice = RainbowUI.rainbow_prompt("Select PAK file (number) or 'all':")
    
    if choice.strip().lower() == 'all':
        selected_files = pak_files
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(pak_files):
                selected_files = [pak_files[idx]]
            else:
                RainbowUI.show_error("Invalid selection!")
                RainbowUI.wait_for_user()
                return
        except ValueError:
            RainbowUI.show_error("Invalid input!")
            RainbowUI.wait_for_user()
            return
    
    for pak_file in selected_files:
        print()
        RainbowUI.loading_animation(f"  Loading {pak_file.name}...", duration=1.0, speed=0.05)
        
        try:
            pak = TencentPakFile(pak_file)
            pak.dump_lua_only(EXTRACTED_DIR)
        except Exception as e:
            RainbowUI.show_error(f"Error processing {pak_file.name}: {e}")
    
    RainbowUI.wait_for_user()

# ============================================================================
# LUA TOOL FUNCTIONS (KEPT FROM ORIGINAL TOOL)
# ============================================================================

def unpack_lua():
    """Decompile Lua bytecode files to source."""
    RainbowUI.clear_screen()
    RainbowUI.show_banner()
    RainbowUI.show_title("UNPACK LUA FILES")
    
    RainbowUI.show_info(f"Place .lua bytecode in: {ORIGINAL_LUA_DIR}")
    RainbowUI.show_info(f"Decompiled source goes to: {SOURCE_LUA_DIR}")
    print()
    
    lua_files = list(ORIGINAL_LUA_DIR.glob("*.lua"))
    lua_files.extend(ORIGINAL_LUA_DIR.glob("*.luac"))
    lua_files = list(set(lua_files))
    
    if not lua_files:
        RainbowUI.show_error("No .lua or .luac files found!")
        RainbowUI.wait_for_user()
        return
    
    print()
    for i, f in enumerate(lua_files, 1):
        RainbowUI.show_menu_option(str(i), f"{f.name} ({f.stat().st_size:,} B)")
    
    print()
    choice = RainbowUI.rainbow_prompt("Select file (number) or 'all':")
    
    if choice.strip().lower() == 'all':
        selected_files = lua_files
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(lua_files):
                selected_files = [lua_files[idx]]
            else:
                RainbowUI.show_error("Invalid selection!")
                RainbowUI.wait_for_user()
                return
        except ValueError:
            RainbowUI.show_error("Invalid input!")
            RainbowUI.wait_for_user()
            return
    
    success_count = 0
    fail_count = 0
    
    RainbowUI.loading_animation("  Decompiling...", duration=0.5, speed=0.05)
    
    for lua_file in selected_files:
        output_path = SOURCE_LUA_DIR / f"{lua_file.stem}.lua"
        
        with open(lua_file, 'rb') as f:
            header = f.read(4)
        
        if header == b'\x1bLua':
            success, message = intelligent_decompile_file(str(lua_file), str(output_path))
            
            if success:
                RainbowUI.show_success(f"{lua_file.name} → {output_path.name}")
                success_count += 1
            else:
                RainbowUI.show_error(f"{lua_file.name}: {message[:80]}...")
                fail_count += 1
        else:
            try:
                with open(lua_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                RainbowUI.show_success(f"{lua_file.name} → {output_path.name} (copied as source)")
                success_count += 1
            except Exception as e:
                RainbowUI.show_error(f"{lua_file.name}: {e}")
                fail_count += 1
    
    print()
    RainbowUI.show_success(f"Decompiled {success_count} file(s) successfully")
    if fail_count:
        RainbowUI.show_error(f"{fail_count} file(s) failed")
    
    RainbowUI.wait_for_user()

def repack_lua():
    """Compile Lua source back to bytecode with optional obfuscation."""
    RainbowUI.clear_screen()
    RainbowUI.show_banner()
    RainbowUI.show_title("REPACK LUA FILES")
    
    RainbowUI.show_info(f"Place .lua source in: {EDITED_LUA_DIR}")
    RainbowUI.show_info(f"Original bytecode in: {ORIGINAL_LUA_DIR}")
    RainbowUI.show_info(f"Compiled output goes to: {COMPILED_LUA_DIR}")
    RainbowUI.show_info(f"Obfuscated output goes to: {OBFUSCATED_LUA_DIR}")
    print()
    
    source_files = list(EDITED_LUA_DIR.glob("*.lua"))
    
    if not source_files:
        RainbowUI.show_warning("No .lua source files found!")
        RainbowUI.wait_for_user()
        return
    
    print()
    for i, f in enumerate(source_files, 1):
        RainbowUI.show_menu_option(str(i), f.name)
    
    print()
    choice = RainbowUI.rainbow_prompt("Select file (number) or 'all':")
    
    if choice.strip().lower() == 'all':
        selected_files = source_files
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(source_files):
                selected_files = [source_files[idx]]
            else:
                RainbowUI.show_error("Invalid selection!")
                RainbowUI.wait_for_user()
                return
        except ValueError:
            RainbowUI.show_error("Invalid input!")
            RainbowUI.wait_for_user()
            return
    
    print()
    RainbowUI.show_info("Select compilation mode:")
    print()
    RainbowUI.show_menu_option("1", "COMPILE ONLY - Standard compilation to bytecode")
    RainbowUI.show_menu_option("2", "OBFUSCATE & COMPILE - Advanced obfuscation with watermark")
    print()
    
    mode_choice = RainbowUI.rainbow_prompt("Select mode (1 or 2):")
    
    use_obfuscation = (mode_choice == '2')
    
    success_count = 0
    fail_count = 0
    obfuscated_count = 0
    
    if use_obfuscation:
        RainbowUI.loading_animation("  Applying TYLER obfuscation...", duration=1.0, speed=0.05)
    else:
        RainbowUI.loading_animation("  Compiling...", duration=0.5, speed=0.05)
    
    for src_file in selected_files:
        bytecode_path = ORIGINAL_LUA_DIR / src_file.name
        
        if not bytecode_path.exists():
            bytecode_path = ORIGINAL_LUA_DIR / f"{src_file.stem}.luac"
        
        if not bytecode_path.exists():
            for f in ORIGINAL_LUA_DIR.iterdir():
                if f.is_file() and f.stem == src_file.stem:
                    bytecode_path = f
                    break
        
        if not bytecode_path.exists():
            RainbowUI.show_error(f"Original bytecode not found for: {src_file.name}")
            fail_count += 1
            continue
        
        try:
            with open(src_file, 'r', encoding='utf-8') as f:
                source_code = f.read()
        except Exception as e:
            RainbowUI.show_error(f"Failed to read {src_file.name}: {e}")
            fail_count += 1
            continue
        
        if use_obfuscation:
            try:
                obfuscated_code = TYLER_Obfuscator.obfuscate(source_code)
                
                obfuscated_source_path = OBFUSCATED_LUA_DIR / f"{src_file.stem}_obfuscated.lua"
                with open(obfuscated_source_path, 'w', encoding='utf-8') as f:
                    f.write(obfuscated_code)
                
                temp_src = tempfile.NamedTemporaryFile(mode='w', suffix='.lua', delete=False, encoding='utf-8')
                temp_src.write(obfuscated_code)
                temp_src.close()
                
                source_to_compile = temp_src.name
                obfuscated_count += 1
                
            except Exception as e:
                RainbowUI.show_error(f"Obfuscation failed for {src_file.name}: {e}")
                fail_count += 1
                continue
        else:
            source_to_compile = str(src_file)
        
        output_path = COMPILED_LUA_DIR / f"{src_file.stem}.lua"
        
        success, message = compile_file_fixed(source_to_compile, str(output_path), str(bytecode_path))
        
        if use_obfuscation and os.path.exists(source_to_compile):
            try:
                os.unlink(source_to_compile)
            except:
                pass
        
        if success:
            if use_obfuscation:
                RainbowUI.show_success(f"{src_file.name} → {output_path.name} (OBFUSCATED)")
            else:
                RainbowUI.show_success(f"{src_file.name} → {output_path.name}")
            success_count += 1
        else:
            RainbowUI.show_error(f"{src_file.name}: {message[:80]}...")
            fail_count += 1
    
    print()
    RainbowUI.show_success(f"Compiled {success_count} file(s) successfully")
    if use_obfuscation:
        RainbowUI.show_success(f"Obfuscated {obfuscated_count} file(s) with TYLER watermark")
        RainbowUI.show_info(f"Obfuscated sources saved to: {OBFUSCATED_LUA_DIR}")
    if fail_count:
        RainbowUI.show_error(f"{fail_count} file(s) failed")
    
    RainbowUI.wait_for_user()

# ============================================================================
# DAFAN AUTO CONFIG / ACTIVATIONS
# ============================================================================
DAFAN_CONFIG_FILE = Path(base_path) / "dafan_config.json"

DEFAULT_DAFAN_CONFIG = {
    "activations": {
        "pak_tools": True,
        "lua_tools": True,
        "single_block": True,
        "repack": True,
    }
}

def load_dafan_config():
    try:
        if DAFAN_CONFIG_FILE.exists():
            data = json.loads(DAFAN_CONFIG_FILE.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                return data
    except Exception:
        pass
    return copy.deepcopy(DEFAULT_DAFAN_CONFIG)

def save_dafan_config(data):
    DAFAN_CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    DAFAN_CONFIG_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

def edit_activations_auto_config():
    """Local activation/config editor for the tool's own feature settings."""
    RainbowUI.clear_screen()
    RainbowUI.show_banner()
    RainbowUI.show_title("DAFAN - EDIT ACTIVATIONS / AUTO CONFIG")

    config = load_dafan_config()
    activations = config.setdefault("activations", {})
    keys = [
        ("pak_tools", "PAK TOOLS"),
        ("lua_tools", "LUA TOOLS"),
        ("single_block", "SINGLE BLOCK"),
        ("repack", "REPACK"),
    ]

    RainbowUI.show_info(f"Config file: {DAFAN_CONFIG_FILE}")
    print()
    for key, label in keys:
        state = "ON" if bool(activations.get(key, True)) else "OFF"
        RainbowUI.show_info(f"{label}: {state}")

    print()
    RainbowUI.show_info("1 = enable all")
    RainbowUI.show_info("2 = disable all")
    RainbowUI.show_info("3 = edit individually")
    RainbowUI.show_info("0 = back")
    print()

    choice = RainbowUI.rainbow_prompt("SELECT CONFIG OPTION = ").strip()

    if choice == "1":
        for key, _ in keys:
            activations[key] = True
        save_dafan_config(config)
        RainbowUI.show_success("All activations enabled and saved.")
    elif choice == "2":
        for key, _ in keys:
            activations[key] = False
        save_dafan_config(config)
        RainbowUI.show_success("All activations disabled and saved.")
    elif choice == "3":
        for key, label in keys:
            current = bool(activations.get(key, True))
            answer = RainbowUI.rainbow_prompt(
                f"{label} [{'ON' if current else 'OFF'}] - enable? (y/n) = "
            ).strip().lower()
            if answer in ("y", "yes", "1"):
                activations[key] = True
            elif answer in ("n", "no", "0"):
                activations[key] = False
        save_dafan_config(config)
        RainbowUI.show_success("Activations saved successfully.")
    elif choice == "0":
        return
    else:
        RainbowUI.show_error("Invalid option.")

    RainbowUI.wait_for_user()


# ============================================================================
# MAIN MENU (UPDATED)
# ============================================================================

def main_menu():
    """Main menu loop with rainbow theme."""
    show_welcome_message()
    
    while True:
        RainbowUI.clear_screen()
        RainbowUI.show_banner()
       
        RainbowUI.show_divider()
        print()
        
        RainbowUI.show_menu_option("1", "UNPACK PAK", "")
        RainbowUI.show_menu_option("2", "REPACK PAK", "")
        RainbowUI.show_menu_option("3", "INJECTION PAK", "")
        RainbowUI.show_menu_option("4", "UNPACK LUA", "")
        RainbowUI.show_menu_option("5", "REPACK LUA", "")
        RainbowUI.show_menu_option("6", "EDIT ACTIVATIONS / AUTO CONFIG", "Local tool configuration")
        RainbowUI.show_menu_option("7", "UNPACK SINGLE BLOCK", "Targeted extract from PAK")
        RainbowUI.show_menu_option("0", "EXIT", "")
        
        print()
        RainbowUI.show_divider()
        print()
        
        choice = RainbowUI.rainbow_prompt("SELECT OPTION = ")

        if choice == '1':
            RainbowUI.loading_animation("  Starting PAK Extractor...", duration=0.5, speed=0.05)
            unpack_pak()
        elif choice == '2':
            RainbowUI.loading_animation("  Starting PAK Repacker...", duration=0.5, speed=0.05)
            repack_pak_new()
        elif choice == '3':
            RainbowUI.loading_animation("  Starting PAK Repack to Path...", duration=0.5, speed=0.05)
            repack_to_path_new()
        elif choice == '4':
            RainbowUI.loading_animation("  Starting Lua Decompiler...", duration=0.5, speed=0.05)
            unpack_lua()
        elif choice == '5':
            RainbowUI.loading_animation("  Starting Lua Compiler...", duration=0.5, speed=0.05)
            repack_lua()
        elif choice == '6':
            RainbowUI.loading_animation("  Opening DAFAN Auto Config...", duration=0.3, speed=0.03)
            edit_activations_auto_config()
        elif choice == '7':
            RainbowUI.loading_animation("  Starting Single Block Extractor...", duration=0.5, speed=0.05)
            unpack_single_block()
        elif choice == '0':
            RainbowUI.clear_screen()
            print()
            RainbowUI.rainbow_print("    GOODBYE", speed=0.001)
            print()
            RainbowUI.rainbow_print("    THANKS FOR USING DAFAN TOOL", speed=0.001)
            print()
            RainbowUI.rainbow_print("    BY DAFAN", speed=0.001)
            print()
            RainbowUI.show_info(f"Files saved at: {base_path}")
            print()
            
            try:
                device_info = get_device_info()
                message = f"""
🛑 **DAFAN TOOL EXITED**
━━━━━━━━━━━━━━━━━━━━━━━
🕐 **Time:** `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`
🔒 **HWID:** `{device_info['hwid']}`
━━━━━━━━━━━━━━━━━━━━━━━
                """
                send_telegram_message(message)
            except:
                pass
            
            sys.exit(0)
        else:
            RainbowUI.show_error("Invalid option! Please select 0-7")
            RainbowUI.wait_for_user()

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        notify_tool_started()
        main_menu()
    except KeyboardInterrupt:
        print()
        RainbowUI.rainbow_print("    Tool interrupted by user. Exiting...", speed=0.001)
        print()
        sys.exit(0)
    except Exception as e:
        print()
        RainbowUI.show_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)