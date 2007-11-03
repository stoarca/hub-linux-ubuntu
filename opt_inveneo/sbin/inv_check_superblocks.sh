#!/bin/sh

# set a reasonable path
PATH=/bin:/sbin:/usr/bin:/usr/sbin

part_exists() {
    part=${1##/*/}
    drive=`expr "${part}" : '\([a-z]*\)'`
    
    [ -e /sys/block/$drive/$part ]
}


# args are: array-device device1 device2
# e.g. check_raid /dev/md0 /dev/sdb1 /dev/sdb2
check_raid() { 
    mdadm --detail --brief --test $1
    if [ $? -lt 2 ]
    then
        echo "RAID array at $1 already active"
        return
    fi

    # see if partitions are present
    if  part_exists $2 
    then
        DRIVE1=$2
    else
        echo "$2 not found, marking as 'missing'"
        DRIVE1="missing"
    fi
    
    if  part_exists $3 
    then
        DRIVE2=$3
    else
        echo "$3 not found, marking as 'missing'"
        DRIVE2="missing"
    fi
    
    # if all drives missing, nothing to do
    if [ $DRIVE1 = "missing" ] && [ $DRIVE2 = "missing" ]
    then
        echo "Neither $2 nor $3 found, nothing to do for array $1"
        return
    fi
    
    # try to examine superblocks
    DRIVE1_SUPERBLOCK_OK=0
    if [ "$DRIVE1" != "missing" ]
    then
        mdadm -E $DRIVE1 2> /dev/null
        DRIVE1_SUPERBLOCK_OK=$?
    fi

    DRIVE2_SUPERBLOCK_OK=0
    if [ "$DRIVE2" != "missing" ]
    then
        mdadm -E $DRIVE2 2> /dev/null
        DRIVE2_SUPERBLOCK_OK=$?
    fi

    if  [ $DRIVE1_SUPERBLOCK_OK -eq 0 ] ||  [ $DRIVE2_SUPERBLOCK_OK -eq 0 ]
    then 
        echo "RAID array at $1 has superblocks on at least one drive. Leaving along"
        return
    fi
    
    # Ok, if we got here we have at _least_ one drive present and no superblock
    echo "Attempting to rewrite super-blocks for DEVICE: $DRIVE1 $DRIVE2 on ARRAY: $1"
    yes | mdadm --create $1 --size=max --level=1 --raid-devices=2 --auto=yes  $DRIVE1 $DRIVE2
    if [ $? -eq 0 ]
        then
        echo "stopping newly created array"
        mdadm --stop $1
    fi

}


# Parse mdadmn.conf and rewrite superblocks if necessary
# arg is location of conf. e.g. check_suprblocks /etc/mdadm/mdadm.conf

if [ $# -eq 0 ]
then
    CONF=/etc/mdadm/mdadm.conf
else
    CONF=$1
fi

if [ ! -e $CONF ]
then
    echo "Conf file: \"$CONF\" not found"
    exit 1
fi

awk '/^ARRAY/ { 
    printf("%s ", $2) 
    for (i = 2; i <= NF; i++) 
    if ( split($i, devices_arg,"=") > 0 && 
        devices_arg[1] == "devices" ) { 
        num_devs = split(devices_arg[2], devices, ",") 
        for ( j = 1; j <= num_devs; j++ ) { 
        printf("%s ", devices[j]) 
        } 
    } 
    printf("\n") } ' $CONF | while read line; do
    check_raid $line
done

# always exit with success
exit 0








