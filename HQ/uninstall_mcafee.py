import os
import re
import time
import pathlib
import pyautogui
from pywinauto import Application, Desktop, timings

def uninstall_mcafee(language_flag):
    try:
        Mcfee_folder = r"C:/Program Files/McAfee"
        Mcfee_folder_path = pathlib.Path(Mcfee_folder)

        if Mcfee_folder_path.exists():
            file_count = 0
            for dirpath, dirnames, filenames in os.walk(Mcfee_folder):
                file_count += len(filenames)
        else:
            return "APP_No_Found"

        try:
            app = Application(backend="uia").connect(path="explorer")
            windows = Desktop(backend="uia").windows(class_name="CabinetWClass")

            for w in windows:
                # Restore window if minimized
                if w.is_minimized():
                    w.restore()

                # Check if window can be closed
                if w.is_visible() and w.is_enabled():
                    w.close()
        except Exception as e:
            print(f"Error closing windows: {e}")
        
        time.sleep(1)
        pyautogui.hotkey('win', 'd')
        time.sleep(1)
        os.system('start appwiz.cpl')  # Open uninstall panel
        time.sleep(2)
        
        while True:
            try:
                app = Application(backend="uia").connect(class_name="CabinetWClass")
                dlg = app.window(class_name="CabinetWClass")
                time.sleep(1)
                break
            except Exception as e:
                print(f"Waiting for uninstall panel: {e}")
                time.sleep(1)

        count = 1
        Mcafee_solution_flag = 0
        while True:
            if count == 5:
                break
            try:
                timings.wait_until(2, 1, lambda: dlg.child_window(title="McAfee", control_type="ListItem").exists())
                Mcafee_solution_flag = 1
                break
            except:
                try:
                    timings.wait_until(2, 1, lambda: dlg.child_window(title_re=re.compile(r"^McAfee.*"),
                                                                      control_type="ListItem").exists())
                    Mcafee_solution_flag = 2
                    break
                except:
                    time.sleep(1)
                    count = count + 1

        if Mcafee_solution_flag == 1:
            button = dlg.child_window(title="McAfee", control_type="ListItem")
            button.double_click_input()

            time.sleep(1)
            dlg.minimize()
            time.sleep(5)

            while True:
                try:
                    app1 = Application(backend="uia").connect(class_name="InstallCoreWebViewAppWindow")
                    dlg1 = app1.window(class_name="InstallCoreWebViewAppWindow")
                    time.sleep(1)
                    width, height = pyautogui.size()
                    width_c, height_c = width/2, height/2
                    pyautogui.moveTo(width_c, height_c, duration=0.5)
                    pyautogui.doubleClick()
                    break
                except Exception as e:
                    print(f"Waiting for McAfee uninstall window: {e}")
                    time.sleep(1)

            if language_flag == "CH":
                language_list = ["不，谢谢", "删除", "删除", "关闭"]
            else:
                language_list = ["No thanks", "Remove", "Remove", "Close"]

            try:
                timings.wait_until(10, 1,
                                 lambda: dlg1.child_window(title=language_list[0], control_type="Button").exists())
            except:
                language_list = ["不，谢谢", "删除", "删除", "关闭"]

            timings.wait_until(60, 1, lambda: dlg1.child_window(title=language_list[0], control_type="Button").exists())
            nothanks_button = dlg1.child_window(title=language_list[0], control_type="Button")
            nothanks_button.click_input()
            time.sleep(1)

            timings.wait_until(20, 1, lambda: dlg1.child_window(title=language_list[1], control_type="Button").exists())
            remove_button = dlg1.child_window(title=language_list[1], control_type="Button")
            remove_button.click_input()
            time.sleep(1)

            try:
                timings.wait_until(10, 1, lambda: dlg1.child_window(title=language_list[2], control_type="Button").exists())
                remove_button_1 = dlg1.child_window(title=language_list[2], control_type="Button")
                remove_button_1.click_input()
            except:
                pass

            n = 0
            while True:
                if not Mcfee_folder_path.exists():
                    time.sleep(2)
                    break
                else:
                    if n == 60:
                        pyautogui.hotkey('win', 'd')
                        return "execute_Fail"
                    file_count_after = 0
                    for dirpath, dirnames, filenames in os.walk(Mcfee_folder):
                        file_count_after += len(filenames)

                    if file_count_after == file_count:
                        n = n + 1
                        time.sleep(2)
                    else:
                        time.sleep(2)
                        break

            close_button_1 = dlg1.child_window(title=language_list[3], control_type="Button")
            close_button_1.click_input()

            time.sleep(5)
            app.kill()
            app1.kill()
            return "execute_Pass"

        elif Mcafee_solution_flag == 2:
            button = dlg.child_window(title_re=re.compile(r"^McAfee.*"), control_type="ListItem")
            button.double_click_input()

            time.sleep(1)
            dlg.minimize()
            time.sleep(5)

            while True:
                try:
                    app1 = Application(backend="uia").connect(class_name="uninstall")
                    dlg1 = app1.window(class_name="uninstall")
                    time.sleep(1)
                    break
                except Exception as e:
                    print(f"Waiting for uninstall window: {e}")
                    time.sleep(1)

            timings.wait_until(10, 1, lambda: dlg1.child_window(auto_id="431_cb",
                                                              control_type="CheckBox").exists())
            uncheck_click = dlg1.child_window(auto_id="431_cb", control_type="CheckBox")
            uncheck_click.click_input()
            time.sleep(1)

            timings.wait_until(10, 1,
                             lambda: dlg1.child_window(auto_id="removeall_cb", control_type="CheckBox").exists())
            uncheck_click1 = dlg1.child_window(auto_id="removeall_cb", control_type="CheckBox")
            uncheck_click1.click_input()
            time.sleep(1)

            timings.wait_until(10, 1, lambda: dlg1.child_window(title="Continue", control_type="Text").exists())
            continue_button = dlg1.child_window(title="Continue", control_type="Text")
            continue_button.click_input()
            time.sleep(1)

            timings.wait_until(10, 1, lambda: dlg1.child_window(title="Continue", control_type="Text").exists())
            continue_button = dlg1.child_window(title="Continue", control_type="Text")
            continue_button.click_input()
            time.sleep(1)

            timings.wait_until(600, 1, lambda: dlg1.child_window(title="No Thanks", control_type="Text").exists())
            nothanks_button = dlg1.child_window(title="No Thanks", control_type="Text")
            nothanks_button.click_input()
            time.sleep(1)

            timings.wait_until(10, 1, lambda: dlg1.child_window(title="Restart later", control_type="Text").exists())
            norestart_button = dlg1.child_window(title="Restart later", control_type="Text")
            norestart_button.click_input()
            time.sleep(5)
            app.kill()
            app1.kill()
            return "execute_Pass"
            
        if Mcafee_solution_flag == 0:
            return "APP_No_Found"

    except Exception as e:
        print(f"Error in uninstall_mcafee: {e}")
        return "execute_Fail"

# Example usage:
if __name__ == "__main__":
    result = uninstall_mcafee("EN")  # Use "CH" for Chinese interface
    print(f"Uninstallation result: {result}")