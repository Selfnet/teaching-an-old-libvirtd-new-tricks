# Teaching An Old Libvirtd New Tricks

Random collection of scripts we're using at Selfnet for VM management.

## qemu

This is a libvirtd hook that takes care of extracting the IP addresses
from the XML definition of a VM and adds corresponding routes.

## download-cloud-image.py

Downloads cloud-init-enabled images for Debian and Alma Linux and 
imports them into ceph. Supposed to be called by a systemd timer.

## selfnet-sudoers-generator

Finds out who has sudo on this machine and writes it to a json file.
Only works with SSSD. Supposed to be called by a systemd timer.

## selfnet-authorized-keys

`AuthorizedKeysCommand` script that restricts non-sudo users on this 
machine to only accessing the libvirtd socket.

## selfnet-libvirt-polkit-generator

Generates polkit rules that allow users who have sudo on a VM to manage 
it to some extent. Users that have sudo on the host can do everything.
