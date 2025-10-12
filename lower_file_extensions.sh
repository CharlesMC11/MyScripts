#!/usr/bin/env -S zsh -f
# A script for converting file extensions to lowercase

autoload zmv || exit $?

readonly SCRIPT_NAME=${0:t:r}

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

zmv ${is_verbose:+'-v'} '(**/)(*.)(*)' '$1$2${(L)3}'
