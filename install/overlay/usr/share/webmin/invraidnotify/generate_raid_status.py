#!/usr/bin/env python
import sys
import string
sys.path.append('/opt/inveneo/lib/python/inveneo')
import fileutils, raidutils, diskutils, constants

def get_drive_number(config,serial_num,num_expected_drives):
    if serial_num == None: 
        return -1 

    for drive_num in range(num_expected_drives+1):
        config_serial = config.get_as_str("DISK%d" % drive_num)
        if not config_serial:
                continue
        elif config_serial.lower().strip() == serial_num.lower().strip():
                return drive_num

    return -1

def get_drive_info_for_array(config,raid_dev):
        # capture the current status of the drives
        num_expected = config.get_as_int('MONITOR_EXPECTED_NUM_DRIVES')
        working_drives = raidutils.num_working_drives_in_array(raid_dev)
        drives_in_array = raidutils.drives_in_array(raid_dev)
        missing_drives = raidutils.get_missing_drives_for_array(config,raid_dev)

        # build a list of tuples for all drives with the following information:
        # ( drive_num, logical name, serial number, drive state[missing, active, fautly, spare] )
        # for missing drives the logical name will be empty
        all_drive_information = [] 

        for logical_name,drive_state in drives_in_array:
                serial_num=diskutils.id_for_device('/dev/%s' % logical_name)
                
                if serial_num==None:
                        serial_num=None
                        drive_num=None
                else:
                        drive_num=str(get_drive_number(config,serial_num,num_expected))
                all_drive_information.append( (drive_num, logical_name, serial_num, drive_state) )

        for drive_num,serial_num in missing_drives:
                logical_name='None'
                drive_state='missing'
                all_drive_information.append( (drive_num, logical_name, serial_num, drive_state) )
        
        all_drive_information.sort(lambda x,y: cmp(x[0],y[0]))

        return all_drive_information;

def print_one_drive_info(single_drive_info):
    drive_num = single_drive_info[0]
    drive_logical_name = single_drive_info[1]
    drive_serial = single_drive_info[2]
    drive_state = single_drive_info[3]

    if drive_num == None:
        drive_num = "" 
    if drive_serial == None:
        drive_serial = "" 
    else:
        drive_serial = "(%s)" % drive_serial
    if drive_state == "missing" or drive_state == "faulty":
        drive_state = "<font color='red'>%s</font>" % drive_state 

    print "<td><table><tr><td>Drive %s: %s%s</td></tr><tr><td>State: %s</td></tr></table></td>" % ( drive_num, drive_logical_name, drive_serial, drive_state )

def print_drive_info(raid_array, raid_drive_info):
        # output the html
        print "<table cellspacing='10'><tr><td align='left'>Array: %s</td></tr><tr>" % raid_array
        for single_drive_info in raid_drive_info:
                print_one_drive_info(single_drive_info)
        print "</tr></table>"

def main():
        config=fileutils.ConfigFileDict(constants.INV_RAID_MONITOR_CONFIG_FILE)

        print_drive_info('/dev/md0',get_drive_info_for_array(config,'/dev/md0'))
        print_drive_info('/dev/md1',get_drive_info_for_array(config,'/dev/md1'))
        print_drive_info('/dev/md2',get_drive_info_for_array(config,'/dev/md2'))

if __name__ == "__main__":
        main()
