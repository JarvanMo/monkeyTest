import os

import time

__author__ = 'shikun'
import re
import subprocess


def stop_monkey(dev):
    monkey_name = "com.android.commands.monkey"
    print("--------------------")
    pid = subprocess.Popen("adb -s " + dev + " shell ps | findstr " + monkey_name,
                           shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
    if pid == "":
        print("No monkey running in %s" % dev)
    else:
        for item in pid:
            if item.split()[8].decode() == monkey_name:
                monkey_pid = item.split()[1].decode()
                cmd_monkey = "adb -s " + dev + " shell kill %s" % (monkey_pid)
                os.popen(cmd_monkey)
                print("Monkey in %s was killed" % dev)
                time.sleep(2)
    subprocess.Popen("taskkill /f /t /im python.exe", shell=True)


def reboot(dev):
    cmd_reboot = "adb -s " + dev + " reboot"
    os.popen(cmd_reboot)


def getModel(devices):
    result = {}
    getpropCmdPrefix = ["adb", "shell", "getprop"]
    release = getpropCmdPrefix.append("ro.build.version.release")
    release = getpropCmdPrefix.append("ro.build.version.release")
    release = getpropCmdPrefix.append("ro.build.version.release")

    # output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
    result["release"] = subprocess.check_output(
        ["adb", "shell", "getprop", "ro.build.version.release"]).decode()  # Android 系统，如anroid 4.0
    result["phone_name"] = subprocess.check_output(
        ["adb", "shell", "getprop", "ro.product.model"]
    ).decode()  # 手机名
    result["phone_model"] = subprocess.check_output(
        ["adb", "shell", "getprop", "ro.product.brand"]
    ).decode()  # 手机品牌
    return result


def get_men_total(devices):
    cmd = "adb -s " + devices + " shell cat /proc/meminfo"
    print(cmd)
    output = subprocess.check_output(
        ["adb", "-s", devices, "shell", "cat", "/proc/meminfo"]).split()
    # item = [x.decode() for x in output]
    return int(output[1].decode())

# # 得到几核cpu


def get_cpu_kel(devices):
    cmd = "adb -s " + devices + " shell cat /proc/cpuinfo"
    print(cmd)
    output = subprocess.check_output(["adb","-s",devices,"shell","cat","/proc/cpuinfo"]).split()
    sitem = ".".join([x.decode() for x in output])  # 转换为string
    return str(len(re.findall("processor", sitem))) + "核"


# 得到手机分辨率
def get_app_pix(devices):
    cmd = "adb -s " + devices + " shell wm size"
    print(cmd)
    return subprocess.check_output(["adb", "-s", devices, "shell", "wm", "size"]).split()[2].decode()

#


def get_phone_Kernel(devices):
    pix = get_app_pix(devices)
    men_total = get_men_total(devices)
    phone_msg = getModel(devices)
    cpu_sum = get_cpu_kel(devices)
    return phone_msg, men_total, cpu_sum, pix


if __name__ == '__main__':
    # get_app_pix("emulator-5554")
    stop_monkey("DU2TAN15AJ049163")
