from bs4 import BeautifulSoup
import urllib.request
import re
import os

the_thing = BeautifulSoup(urllib.request.urlopen("https://checkra.in").read(), 'html.parser')
does_checkra1n_exist = False


download_link = ""

try:
    with open('checkra1n.dmg', 'r'):
        does_checkra1n_exist = True
except FileNotFoundError:
    does_checkra1n_exist = False


def guide_dfu():
    print("dfu mode")


def move_stuff():
    os.system("hdiutil mount checkra1n.dmg")
    os.system("cp -r /Volumes/checkra1n/checkra1n.app .")
    # os.system("mv Contents/ checkra1n.app")
    os.system("checkra1n.app/Contents/MacOS/checkra1n_gui -")
    # guide_dfu()


def update_checkrain():
    is_outdated = True
    idiot = 0

    a = str(os.popen('cat version').readlines())
    stupid = the_thing.find_all('a')[2].get_text().split()[1]

    # how 2 compare version nubmers liek b0s
    version_on_disk = [int(s) for s in a.strip('\'[]').split(".")]
    vnum2 = [int(t) for t in stupid.split(".")]

    if version_on_disk[0] < vnum2[0] or version_on_disk[1] < vnum2[1] or version_on_disk[2] < vnum2[2]:
        is_outdated = True
    elif version_on_disk[0] == vnum2[0] and version_on_disk[1] == vnum2[1] and version_on_disk[2] == vnum2[2]:
        is_outdated = False

    url = urllib.request.urlopen("https://checkra.in")
    content = url.read()
    soup = BeautifulSoup(content, features='lxml')
    for a in soup.findAll('a', href=True):
        if re.findall('downloads/macos', a['href']):
            download_link = a['href']
    if does_checkra1n_exist:
        if is_outdated:
            urllib.request.urlretrieve(download_link, filename="checkra1n.dmg")
            move_stuff()
        elif not is_outdated:
            os.system("checkra1n.app/Contents/MacOS/checkra1n_gui -")
    else:
        urllib.request.urlretrieve(download_link, filename="checkra1n.dmg")
        move_stuff()


try:
    with open('version', 'r') as version:
        update_checkrain()
except FileNotFoundError:
    open('version', 'w+').write(the_thing.find_all('a')[2].get_text().split()[1])
    update_checkrain()
