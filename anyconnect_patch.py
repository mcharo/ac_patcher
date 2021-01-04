#!/usr/bin/env python3

import os
import r2pipe
import argparse
from datetime import datetime
from shutil import copyfile

def patch_vpnagent(file):
    # backup existing file
    filetime = datetime.now().strftime("%Y_%m_%d")
    filename = os.path.basename(file)
    backup_file = f"{filename}.{filetime}"
    copyfile(file, backup_file)
    print(f"Backed up existing file to {backup_file}")

    # patch file
    r = r2pipe.open(file, flags=['-w'])
    print(f"Analyzing {file} with radare2")
    r.cmd('aaa')
    method_location = r.cmd("afl | grep StartInterfaceAndRouteMonitoring | awk \'{print $1}\'").rstrip()
    if method_location:
        r.cmd('s' + method_location)
        method_name = r.cmd('fd').rstrip()
        print(f"Found {method_name} at {method_location}")
        called_from = r.cmd("axt | awk \'{print $2}\'").rstrip()
        if called_from:
            print(f"Found call to {method_name} at {called_from}")
            r.cmd('s ' + called_from)
            write_result = r.cmd('wx 9090909090')
            if write_result == "":
                print("Successfully updated file")
                return True
            else:
                print(f"Unable to write to file, message from radare2: {write_result}")
                return False
        else:
            print(f"Unable to find call to {method_name}, maybe you already patched this file")
    else:
        print("Unable to find reference to 'StartInterfaceAndRouteMonitoring'")
    r.cmd('q')

if __name__ == '__main__':
    my_parser = argparse.ArgumentParser()
    my_parser.add_argument('--file', '-f', action='store', type=str, required=True)

    args = my_parser.parse_args()

    patch_vpnagent(args.file)