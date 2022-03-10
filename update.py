#/usr/bin/python3
# 

import requests
import json
import subprocess
import os

from archive import extract


print("I: Rebooting device to bootloader")
subprocess.call(["adb", "reboot", "bootloader"])

def get_serialnum():
    print("I: Finding serial number")
    # Extract serial number from fastboot
    _getvar_serialno = subprocess.check_output(['fastboot', 'getvar', 'serialno'], stderr=subprocess.STDOUT)
    _serialno_string = _getvar_serialno.decode("utf-8")
    _serialno_string_split = _serialno_string.split(": ")
    serialno = _serialno_string_split[1].split("\n")
    return serialno[0]

print("I: Querrying database")
# Request firmware download url from BQ API
apiurl = "http://devices.bq.com/api/getHardReset/" + get_serialnum()
apiresponse = requests.get(apiurl)

firmware = json.loads(apiresponse.content)

print("I: Firmware found at " + firmware["url"])
firmware_target_folder = "firmware_" + firmware["product"] + "_" + firmware["version"]
firmware_target_name = "firmware_" + firmware["product"] + "_" + firmware["version"] + ".zip"

try:
    subprocess.call(["axel", "-o", firmware_target_name, firmware["url"]])
except OSError as e:
    if e.errno == os.errno.ENOENT:
        subprocess.call(["wget", "-O", firmware_target_name, firmware["url"]])
    else:
        print("Could not download the firmware")
        raise

print("I: Extracting firmware")
if not os.path.isdir(firmware_target_folder):
    os.mkdir("firmware_" + firmware["product"] + "_" + firmware["version"])
    extract(firmware_target_name, firmware_target_folder)

#print("I: Leaving control to flash script provided by the downloaded firmware")
#subprocess.call(["bash", firmware_target_folder + "/" + "*fastboot_all_images.sh"])

print("I: flashing system and boot")
print("WARN: Do not disconnect the device now or it will end up with no firmware installed!")


def flash(partition, image):
    subprocess.call(["fastboot", "flash", partition, image])

def fash_fast():
    flash("boot", firmware_target_folder + "/boot.img")
    flash("system", firmware_target_folder + "/system.img")

def flash_full():
    flash("boot", firmware_target_folder + "/boot.img")
    flash("system", firmware_target_folder + "/system.img")
    flash("tz", firmware_target_folder + "/tz.mbn")
    flash("tzbak", firmware_target_folder + "tz.mbn")
    flash("sbl1", firmware_target_folder + "sbl1.mbn")
    flash("sbl1bak", firmware_target_folder + "sbl1.mbn")
    flash("rpm", firmware_target_folder + "rpm.mbn")
    flash("rpmbak", firmware_target_folder + "rpm.mbn")
    flash("mdtp", firmware_target_folder + "mdtp.img")
    flash("aboot", firmware_target_folder + "emmc_appsboot.mbn")
    flash("abootbak", firmware_target_folder + "emmc_appsboot.mbn")
    flash("devcfg", firmware_target_folder + "devcfg.mbn")
    flash("devcfgbak", firmware_target_folder + "devcfg.mbn")
    flash("keymaster", firmware_target_folder + "keymaster.mbn")
    flash("keymasterbak", firmware_target_folder + "keymaster.mbn")
    flash("cmnkib", firmware_target_folder + "cmnlib.mbn")
    lash("cmnlibbak", firmware_target_folder + "cmnlib.mbn")
    flash("cmnkib64", firmware_target_folder + "cmnlib64.mbn")
    flash("cmnkib64bak", firmware_target_folder + "cmnlib64.mbn")

flash_fast()
