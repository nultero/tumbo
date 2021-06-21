_tumbo() {
    COMPREPLY=()
    local cur=${COMP_WORDS[COMP_CWORD]}

    local STARTOPTS=( "new" "list" "search" "update" "source" "remove" )
    local SECONDOPTS=( "alias" "type" )
    local OPTS
    case $3 in 
    "new" | "update" | "remove")
        OPTS=${SECONDOPTS[*]}
    ;;
    "alias" | "type" | "source" | "search" | "list")
        OPTS=()
    ;;
    *)
        OPTS=${STARTOPTS[*]}
    ;;
    esac
    COMPREPLY=( `compgen -W "${OPTS[*]}" $cur` )
}

complete -F _tumbo tumbo