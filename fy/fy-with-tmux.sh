#!/bin/bash

WAIT=60

session_name=fy

SERVERS=(
                "log          ./logserver logserver.conf"
                "data         ./dataserver dataserver.conf"
                "mail         ./mailserver mailserver.conf"
                "world        ./worldserver worldserver.conf"
                "game1       ./gameserver gameserver.1.conf"
                "game131     ./gameserver gameserver.131.conf"
                "logon        ./logonserver logonserver.conf"
                "gate11       ./gateway gateway.11.conf"
                "route1       ./router router.1.conf"
                "uname       ./unameserver unameserver.conf"
        )

_start()
{
    ulimit -c unlimited

    # check running
    for svr in "${SERVERS[@]}"; do

        svr_name=${svr%% *}
        svr_exec=./${svr#*./}

        if [ -f $svr_name.pid ]; then
            pid=$(<$svr_name.pid)
            if [ -d /proc/$pid ] && [ "$(</proc/$pid/cmdline)" = "${svr_exec// /}" ]; then
                echo $svr_name is running
                exit 1
            else
                rm -f $svr_name.pid
            fi
        fi
    done

    # check session exist
    tmux has-session -t $session_name 2> /dev/null
    if [ $? -eq 0 ]
    then
        echo "session  $session_name already in running..."
        exit 1
    fi

    echo "create session $session_name ..."
    tmux new-session -d -s $session_name
    sleep 1

    for svr in "${SERVERS[@]}"; do

        svr_name=${svr%% *}
        svr_exec=./${svr#*./}

        echo -n starting $svr_name
        # $svr_exec </dev/null >/dev/null &
        tmux new-window -n $svr_name -t $session_name "$svr_exec"
        sleep 2

        if [ -d "/proc/$!" ]; then
            echo $! > $svr_name.pid
            echo -e "\t\t\033[1;32m[OK]\033[0m"
        else
            echo -e "\t\t\033[0;31m[Failed]\033[0m"
        fi
     done
}

_stop()
{
    for ((i=${#SERVERS[@]}-1; i>=0; i--)); do

        svr=${SERVERS[i]}

        svr_name=${svr%% *}
        svr_exec=./${svr#*./}

        pidfile=$svr_name.pid
        if [ -f $pidfile ]; then
            pid=$(<$pidfile)
            if [ -d /proc/$pid ] && [ "$(</proc/$pid/cmdline)" = "${svr_exec// /}" ]; then
                echo -n stopping $svr_name ...
                kill $pid
                cnt=0
                while [ -d /proc/$pid ]; do
                    sleep 1
                    cnt=$((cnt + 1))
                    if [ $cnt -gt $WAIT ]; then
                        kill -9 $pid
                        break
                    fi
                done
                if [ $cnt -gt $WAIT ]; then
                    echo -e "\t\t\033[0;33m[FORCE KILLING]\033[0m"
                else
                    echo -e "\t\t\033[1;32m[OK]\033[0m"
                fi

                echo $svr|grep -iq "world"
                if [ $? -eq 0 ]; then
                    sleep 10
                fi
            else
                echo -e "\t\t\033[0;33m[DEAD]\033[0m"
            fi
            rm -f $pidfile
        fi
    done

    tmux kill-session -t $session_name
}

_status()
{
    for svr in "${SERVERS[@]}"; do

        svr_name=${svr%% *}
        svr_exec=./${svr#*./}

        pidfile=$svr_name.pid
        if [ -f $pidfile ]; then
            pid=$(<$pidfile)
            if [ -d "/proc/$pid" ] && [ "$(</proc/$pid/cmdline)" = "${svr_exec// /}" ]; then
                # process is running
                echo "$svr_name is running ..."
            else
                # process dead, pidfile remains
                echo "$svr_name is DEAD"
            fi
        else
            echo "$svr_name is NOT running"
        fi
    done
}

case "$1" in
    start)
        _start
        ;;
    stop)
        _stop
        ;;
    restart)
        _stop
        sleep 60
        _start
        ;;
    status)
        _status
        ;;
    *)
        echo "Usage: fy {start|stop|restart|status}"
esac

