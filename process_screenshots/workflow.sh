#!/usr/bin/env dash
# A script for preparing `process_screenshots/main.sh`. It will be sourced by a
# Folder Action

readonly SCREENSHOTS_DIR="${HOME}/MyFiles/Pictures/Screenshots"
readonly PIPE="${SCREENSHOTS_DIR}/process_screenshots"

readonly EXECUTABLE_DIR="${HOME}/.local/bin/process_screenshots"
readonly TAG_FILES_DIR="${HOME}/.config/exiftool"

################################################################################

if [ -p $PIPE ]; then
    echo "Pipe '${PIPE}' exists; Folder action already in progress" 1>&2
    exit 1
fi
# Taking multiple screenshots in succession causes the Folder Action to trigger
# the same amount of times. Checking for this temporary pipe in the `elif`
# statement above ensures that only the first instance of the Folder Action
# executes the rest of the script body
mkfifo "$PIPE" && trap 'rm "$PIPE"' EXIT

"${EXECUTABLE_DIR}/main" -i "${SCREENSHOTS_DIR}/.tmp" -o "$SCREENSHOTS_DIR"\
    "${TAG_FILES_DIR}/charlesmc.args" "${TAG_FILES_DIR}/screenshot.args"
