#!/bin/bash

ROOTFS="ubuntu-22.04.ext4"
VENV_DIR="microVM_venv"

# Mount the rootfs image
echo "Mounting the rootfs image..."
sudo mkdir -p /mnt/vm_root
if ! sudo mount -o loop $ROOTFS /mnt/vm_root; then
    echo "Failed to mount $ROOTFS"
    exit 1
fi

# Copy the Python virtual environment to the rootfs
echo "Copying Python virtual environment to the rootfs..."
if ! sudo cp -r "$VENV_DIR"/ /mnt/vm_root/root; then
    echo "Failed to copy venv..."
    sudo umount /mnt/vm_root
    exit 1
fi

# Unmount the rootfs image
echo "Unmounting the rootfs image..."
if ! sudo umount /mnt/vm_root; then
    echo "Failed to unmount /mnt/vm_root"
    exit 1
fi

echo "Rootfs image updated with Python virtual environment."
