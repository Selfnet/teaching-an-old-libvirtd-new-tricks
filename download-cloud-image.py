#!/usr/bin/python3
import urllib.request
import subprocess
import sys
import os
distro,version = sys.argv[1].split("-")

pool = "vms"

if distro == "debian" :
    debian_releases = {
        "10": "buster",
        "11": "bullseye",
        "12": "bookworm"
    }
    debian_release = debian_releases[version]
    download_url = f"https://cloud.debian.org/images/cloud/{debian_release}/daily/latest/debian-{version}-genericcloud-amd64-daily.qcow2"
elif distro == "alma" :
    download_url = f"https://repo.almalinux.org/almalinux/{version}/cloud/x86_64/images/AlmaLinux-{version}-GenericCloud-latest.x86_64.qcow2"
else :
    print("unknown distro", distro)
    exit(1)

image_name = f"{distro}-{version}-genericcloud-amd64-daily"
image_name_tmp = f"{image_name}-tmp"
keyring = "/etc/ceph/ceph.client.libvirt.keyring"
key_id = "libvirt"

print("downloading", download_url)
local_filename, headers = urllib.request.urlretrieve(download_url)

def rbd(op, check, *args) :
    return subprocess.run(["rbd", op, f"--id={key_id}", "-k", keyring, *args], check=check)

print("removing old tmp image")
rbd("rm", False, f"{pool}/{image_name_tmp}")

print("importing image")
subprocess.run(["qemu-img", "convert", "-p", "-f", "qcow2", "-O", "raw", local_filename, f"rbd:{pool}/{image_name_tmp}:id={key_id}:keyring={keyring}"], check=True)
os.remove(local_filename)

print("moving image")
rbd("rm", False, f"{pool}/{image_name}")
rbd("mv", False, f"{pool}/{image_name_tmp}", f"{pool}/{image_name}")
