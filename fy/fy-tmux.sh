#!/bin/sh

session_name=fy

SERVERS=(
        "log          ./logserver logserver.conf"
        "data         ./dataserver dataserver.conf"
        "mail         ./mailserver mailserver.conf"
        "world        ./worldserver worldserver.conf"
        "game1        ./gameserver gameserver.1.conf"
        "game131      ./gameserver gameserver.131.conf"
        "logon        ./logonserver logonserver.conf"
        "gate11       ./gateway gateway.11.conf"
        "route1       ./router router.1.conf"
        "uname        ./unameserver unameserver.conf"
)


pushd ~/fy/bin

tmux has-session -t $session_name 2> /dev/null
if [ $? -eq 0 ]
then
    echo "already in running..."
    exit 0
fi


tmux new-session -d -s $session_name


for svr in "${SERVERS[@]}"; do
    svr_name=${svr%% *}
    svr_exec=./${svr#*./}

    echo "starting: $svr_name,  $svr_exec"

    tmux new-window -n "$svr_name" -t $session_name "$svr_exec"
done


popd

echo "Done!"
