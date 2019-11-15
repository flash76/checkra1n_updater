import os
import plistlib
import re
import time
import urllib.request
from sys import stdout

from bs4 import BeautifulSoup



def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
        return t


def check_internet_connection():
    try:
        urllib.request.urlretrieve("https://checkra.in")
        print("Connection succeeded. Continuing.")
        return True
    except:
        print("Could not establish connection to https://checkra.in.")
        return False


def get_local_version():
    if os.path.isdir("checkra1n.app"):
        with open("checkra1n.app/Contents/Info.plist", 'rb') as fp:
            pl = plistlib.load(fp)
        local_version = pl["CFBundleVersion"].split()[1].strip()
        print("\nLocal version:", local_version)
        return local_version
    else:
        print("\nLocal version not found")
        return False


def get_remote_version():
    html = BeautifulSoup(urllib.request.urlopen(
        "https://checkra.in").read(), 'html.parser')
    remote_version = html.find_all('a')[2].get_text().split()[1].strip()
    print("Remote version:", remote_version, "\n")
    return remote_version


def unpack_dmg():
    print("Unpacking dmg...")
    os.system("hdiutil attach -mountpoint /Volumes/checkra1n checkra1n.dmg")
    os.system("cp -r /Volumes/checkra1n/checkra1n.app .")
    os.system("hdiutil unmount /Volumes/checkra1n")
    os.remove("checkra1n.dmg")


def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = min(int(count * block_size * 100 / total_size), 100)
    stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                 (percent, progress_size / (1024 * 1024), speed, duration))
    stdout.flush()


def download_checkra1n():
    url = urllib.request.urlopen("https://checkra.in")
    content = url.read()
    soup = BeautifulSoup(content, features='lxml')
    for a in soup.findAll('a', href=True):
        if re.findall('downloads/macos', a['href']):
            download_link = a['href']
            urllib.request.urlretrieve(
                download_link, "checkra1n.dmg", reporthook)
            unpack_dmg()


def guide_dfu():
    print("DFU Assistant: Sending device to recovery mode...")
    uuid = str(os.popen("ideviceinfo | grep UniqueDeviceID").readlines()).split(" ")[1]
    uuid = uuid.strip("\\n\']")
    os.system("ideviceenterrecovery " + uuid)
    print("DFU Assistant: Your device should be in recovery mode. It should have a cable\npointing to a computer or "
          "iTunes icon. If not, exit and try again. Prepare to hold power and home in 3 seconds.")
    time.sleep(3)
    for x in range(1, 10):
        print("DFU Assistant: Hold power and home for " + countdown(10-x) + " seconds.")
    for x in range(1, 10):
        print("DFU Assistant: now just hold home for " + countdown(10-x) + " seconds")
    os.system("checkra1n.app/Contents/MacOS/checkra1n_gui -")


if __name__ == "__main__":
    if get_local_version() != get_remote_version():
        if check_internet_connection():
            print("Downloading newest version...")
            download_checkra1n()
            guide_dfu()
        else:
            print("Unable to download checkra1n. Connect to a different network and try again.")
    else:
        print("Newest version already downloaded...")
    print("Update done. Running checkra1n...\n")
    guide_dfu()
