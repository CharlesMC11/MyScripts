#!/usr/bin/env -S zsh -f

readonly   DISK_NAME=Workbench
integer -i DISK_SIZE=16
readonly   SIZE_UNIT=GiB

readonly   SCRIPT_NAME=${0:t:r}

if [[ -d /Volumes/$DISK_NAME ]]; then
    print -u 2 -- "${SCRIPT_NAME}: RAM Disk already exists"
    exit
fi

if [[ GiB == $SIZE_UNIT || GB == $SIZE_UNIT ]]; then
    integer -r shift_amount=30
elif [[ MiB == $SIZE_UNIT || MB == $SIZE_UNIT ]]; then
    integer -r shift_amount=20
else
    print -u 2 -- "${SCRIPT_NAME}: Invalid unit"
    exit 64
fi

integer -r block_size=512
integer -r sector_count=$(( $DISK_SIZE * ( 1 << $shift_amount ) / $block_size ))

newfs_apfs -v "$DISK_NAME" $(hdiutil attach -nomount ram://$sector_count)

diskutil mount "$DISK_NAME"