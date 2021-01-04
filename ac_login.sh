#!/bin/bash

USERNAME=$(whoami)
VPN_ENDPOINT="vpn.somewhere.com"
GROUP=${1:-0}
CISCO_PATH="$(dirname $(find /opt/cisco -depth -name vpnagentd))"

if [[ "$GROUP" == "-d" ]]; then
    $CISCO_PATH/vpn disconnect
else
    echo "Connecting to $VPN_ENDPOINT, profile $GROUP, as $USERNAME"

    # TODO detail rsacli usage and rsapin convention
    PIN=$($(which security) find-generic-password -wl "rsapin")
    CODE=$(rsacli)
    LOGINSTR="$GROUP\n$USERNAME\n$PIN$CODE\n"

    echo -e $LOGINSTR > /tmp/answers.txt

    # make sure the anyconnect daemon is running
    [ $(pgrep vpnagentd) ] || $CISCO_PATH/vpnagentd

    # connect
    $CISCO_PATH/vpn -s < /tmp/answers.txt connect $VPN_ENDPOINT
    rm -f /tmp/answers.txt
fi
