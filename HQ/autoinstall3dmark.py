import os
import subprocess
import sys
import time
from pathlib import Path

def read_config():
    """Read config file from EXE directory"""
    try:
        config_path = os.path.join(os.path.dirname(sys.executable), "paths.txt")
        print(f"Reading config from: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            return {k.strip(): v.strip() 
                   for line in f 
                   if '=' in line and not line.startswith('#')
                   for k, v in [line.strip().split('=', 1)]}
    except FileNotFoundError:
        print("Error: paths.txt not found in current directory")
        return None
    except Exception as e:
        print(f"Config error: {str(e)}")
        return None

def is_installed():
    """Check if 3DMark is installed"""
    return (Path("~/Desktop").expanduser().glob("3DMark*.lnk") or 
            Path("C:/Program Files/UL/3DMark/3DMark.exe").exists())

def install_3dmark(installer_path):
    """Silent installation"""
    try:
        subprocess.run([installer_path, "/S", "/D=C:\\Program Files\\UL\\3DMark"],
                      check=True, capture_output=True)
        return True
    except Exception as e:
        print(f"Installation failed: {e}")
        return False

def wait_install(timeout=600):
    """Wait for installation to complete"""
    print("Installing... Please wait")
    for _ in range(timeout//30):  # Check every 30 seconds
        if is_installed():
            print("Installation completed")
            return True
        print("Waiting for installation...")
        time.sleep(30)
    print("Timeout: Installation took too long")
    return False

def register_key(key):
    """Register license key"""
    try:
        subprocess.run(["C:\\Program Files\\UL\\3DMark\\3DMarkCmd.exe", f"--register={key}"],
                      check=True, capture_output=True)
        print("License registered successfully")
        return True
    except Exception as e:
        print(f"License registration failed: {e}")
        return False

def main():
    print("\n=== 3DMark Auto Installer ===")
    
    if not (config := read_config()):
        input("paths.txt erro！Press Enter to exit...")
        return
    
    if not all(k in config for k in ["installer_path", "key_path"]):
        print("Error: Missing required config parameters")
        return
    
    if not (install_3dmark(config["installer_path"]) and wait_install()):
        return
    
    try:
        if key := open(config["key_path"]).read().strip():
            register_key(key)
            print("All operations completed")
            time.sleep(2)
    except Exception as e:
        print(f"Key file error: {e}")

if __name__ == "__main__":
    main()