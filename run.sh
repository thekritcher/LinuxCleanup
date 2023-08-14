#!/bin/bash

# Function to perform maintenance tasks for Debian-based systems
debian_maintenance() {
    echo "Performing maintenance tasks for Debian-based system..."

    apt update
    apt upgrade -y
    apt autoremove -y
    apt clean
    apt autoremove --purge -y

    find /home/*/.thumbnails -type f -atime +7 -delete
    find /home/*/.cache -type f -atime +7 -delete

    journalctl --vacuum-time=7d

    echo "Maintenance tasks completed!"
}

# Function to perform maintenance tasks for Arch-based systems
arch_maintenance() {
    echo "Performing maintenance tasks for Arch-based system..."

    pacman -Syu --noconfirm
    paccache -r -k0

    find /home/*/.thumbnails -type f -atime +7 -delete
    find /home/*/.cache -type f -atime +7 -delete

    journalctl --vacuum-time=7d

    echo "Maintenance tasks completed!"
}

# Function to perform maintenance tasks for Fedora-based systems
fedora_maintenance() {
    echo "Performing maintenance tasks for Fedora-based system..."

    dnf update -y
    dnf autoremove -y
    dnf clean packages

    find /home/*/.thumbnails -type f -atime +7 -delete
    find /home/*/.cache -type f -atime +7 -delete

    journalctl --vacuum-time=7d

    echo "Maintenance tasks completed!"
}

# Detect the distribution and run the appropriate maintenance function
if [ -f /etc/debian_version ]; then
    debian_maintenance
elif [ -f /etc/arch-release ]; then
    arch_maintenance
elif [ -f /etc/fedora-release ]; then
    fedora_maintenance
else
    echo "Unsupported distribution."
fi
