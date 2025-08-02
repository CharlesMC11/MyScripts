#!/opt/homebrew/bin/zsh -f
# A script for isolating sidecar files without an image

readonly SCRIPT_NAME=${0:t:r}
readonly TARGET_DIR=__dangling_xmps__
readonly MISC_DIR=Misc
declare -Ua FILE_EXTENSIONS
readonly FILE_EXTENSIONS=(dng heif jpeg jpg orf png psd tif tiff)

show_usage () {
    echo "usage: ${SCRIPT_NAME} [-v | --verbose, -h | --help ] [directory]" 1>&2
}

error_on_invalid_option () {
    echo "${SCRIPT_NAME}: invalid option -- $1" 1>&2
    show_usage
    exit 1
}

################################################################################

while (($#)); do
    case $1 in
        -h | --help   ) show_usage; exit
        ;;
        -v | --verbose) integer -r is_verbose=1
        ;;
        -* | --*      ) error_on_invalid_option $1
        ;;
        *             ) if [[ -d $1 ]]; then cd $1; break
                        else error_on_invalid_option $1
                        fi
        ;;
    esac
    shift
done

mkdir ./"${TARGET_DIR}" 2>/dev/null\
    && trap 'rmdir ./"${TARGET_DIR}" 2>/dev/null' EXIT

for file in **/*.xmp(N); do
    if [[ ${file:h} == $MISC_DIR || ${file:h} == $TARGET_DIR ]]; then
        continue
    fi

    integer is_dangling=1
    for ext in ${=FILE_EXTENSIONS}; do
        if [[ -f ${file/xmp/$ext}  || -f ${file/xmp/${ext:u}} ]]; then
            is_dangling=0
            break
        fi
    done

    if ((is_dangling == 0)); then
        continue
    fi

    mv ${is_verbose:+'-v'} "$file" "${TARGET_DIR}/${file:t}"
done
