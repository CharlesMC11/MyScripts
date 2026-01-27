#!/usr/bin/env -S zsh -f

readonly   DISK_NAME=Workbench
integer -i DISK_SIZE=16
readonly   SIZE_UNIT=GiB

readonly   DISK_PATH="/Volumes/${DISK_NAME}"

readonly   SCRIPT_NAME=${0:t:r}

if [[ -d $DISK_PATH ]]; then
  print -u 2 -- "${SCRIPT_NAME}: RAM Disk already exists"
  exit 0
fi

case ${(L)SIZE_UNIT} in
  gib|gb) integer -r shift_amount=30;;
  mig|mb) integer -r shift_amount=20;;
  *)      print -u 2 -- "${SCRIPT_NAME}: Invalid unit"; exit 64  # BSD EX_USAGE
esac

integer -r block_size=512
integer -r sector_count=$(( DISK_SIZE * ( 1 << shift_amount ) / block_size ))

readonly device_path=${$(hdiutil attach -nomount ram://$sector_count)[(w)1]}
if [[ -z $device_path ]]; then
  print -u 2 -- "${SCRIPT_NAME}: Failed to allocate RAM device"
  exit 1
fi

if newfs_apfs -v "$DISK_NAME" $device_path; then
  diskutil mount "$DISK_NAME"
  touch "${DISK_PATH}/.metadata_never_index"
  mdutil -i off "$DISK_PATH"
else
  print -u 2 -- "${SCRIPT_NAME}: Formatting failed"
  hdiutil detach "$device_path"
  exit 1
fi
