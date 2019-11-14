import os
import plistlib
import re
import time
import urllib.request
from sys import stdout

from bs4 import BeautifulSoup


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


if __name__ == "__main__":
    if get_local_version() != get_remote_version():
        print("Downloading newest version...")
        download_checkra1n()
    else:
        print("Newest version already downloaded...")
    print("Update done. Running checkra1n...\n")
    os.system("checkra1n.app/Contents/MacOS/checkra1n_gui -")
