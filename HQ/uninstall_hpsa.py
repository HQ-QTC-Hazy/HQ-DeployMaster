import os
import subprocess

def uninstall_hpsa():
    uninstall_hpsa_exe = r"C:\SWSetup\SP155262\UninstallHPSA.exe"

    if not os.path.isfile(uninstall_hpsa_exe):
        print("HP Support Assistant uninstaller not found")
        return "APP_No_Found" 
    print("Uninstalling HP Support Assistant...")

    try:
        result = subprocess.run(
            [uninstall_hpsa_exe, "/s"],
            capture_output=True,
            text=True,
            check=True
        )

        if result.returncode == 0:
            print("HP Support Assistant uninstalled successfully!")
            return "execute_Pass"
        else:
            print(f"Uninstall failed, return code: {result.returncode}")
            print(f"Error message: {result.stderr}")
            return "execute_Fail"
            
    except subprocess.CalledProcessError as e:
        print(f"Uninstall process error: {e.stderr}")
        return "execute_Fail"
    except Exception as e:
        print(f"Unknown error: {e}")
        return "execute_Fail"

if __name__ == "__main__":
    print("=== HP Support Assistant Uninstaller ===")
    status = uninstall_hpsa()

    if status == "execute_Pass":
        print("\n✅ Uninstall successful!")
    elif status == "APP_No_Found":
        print("\n❌ HP Support Assistant not found, may be already uninstalled or path is incorrect")
    else:
        print("\n❌ Uninstall failed, please check error messages")
    
    if os.name == 'nt':
        os.system("pause")