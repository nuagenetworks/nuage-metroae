#!/usr/bin/env bash

MENU_STRIDE=5

_metroae_completions()
{
    MENU=()

    # Hard-coded container commands.  These should change very rarely.  Additional
    # container commands can be added dynamically from menu file.
    MENU+=(',container'                 'Manage the MetroAE container'                         'container'  ''                       '')
    MENU+=(',container,pull'            'Pull a new MetroAE image from the registry'           'container'  'pull'                   ',container,pull')
    MENU+=(',container,setup'           'Setup the MetroAE container'                          'container'  'setup'                  ',container,setup')
    MENU+=(',container,start'           'Start the MetroAE container'                          'container'  'start'                  ',container,start')
    MENU+=(',container,stop'            'Stop the MetroAE container'                           'container'  'stop'                   ',container,stop')
    MENU+=(',container,status'          'Display the status of the MetroAE container'          'container'  'status'                 ',container,status')
    MENU+=(',container,destroy'         'Destroy the MetroAE container'                        'container'  'destroy'                ',container,destroy')
    MENU+=(',container,update'          'Update the MetroAE container to the latest version'   'container'  'upgrade-engine'         ',container,update')

    if [[ -z $SETUP_FILE ]]; then
        SETUP_FILE=/opt/metroae/.metroae
    fi

    if [[ -f src/menu ]]; then
        source src/menu
    elif [[ -f $SETUP_FILE ]]; then
        while read -r line; do declare $line; done < $SETUP_FILE
        if [[ -f $METROAE_MOUNT_POINT/menu ]]; then
            source $METROAE_MOUNT_POINT/menu
        fi
    else
        COMPREPLY=()
        return
    fi

    prefix=","

    for (( i=1; i<$COMP_CWORD; i+=1 )); do
        prefix="${prefix}${COMP_WORDS[i]},"
    done

    partial="${prefix}${COMP_WORDS[$COMP_CWORD]}"

    last="nomatch"
    full_menu=()
    matches=()
    for (( i=0; i<=${#MENU[@]} - 1; i+=$MENU_STRIDE )); do
        menu_key=${MENU[@]:$i:1}
        if [[ "${menu_key}" != "${last}"* && "${menu_key}" == "${partial}"* ]]; then
            descr=${MENU[@]:$i+1:1}
            no_prefix=${menu_key#$prefix}
            key=${no_prefix%%,*}
            matches+=("${key}")
            cols=$((COLUMNS-31))
            full_menu+=("$(printf '%-20s%10s%*s' "${key}" "" "-${cols}" "${descr}")")
            last="${prefix}${key}"
        fi
    done

    if [[ "${#matches[@]}" == "1" ]]; then
        COMPREPLY=("${matches}")
    else
        COMPREPLY=("${full_menu[@]}")
    fi
}

complete -F _metroae_completions metroae
