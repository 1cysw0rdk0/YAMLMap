#! /usr/bin/python3

import subprocess
import argparse
import yaml
import time
import os


class scanObject:
    def __init__(self):
        self.scanAttributes = {}


def handle_args():
    # Handle Commandline args
    parser = argparse.ArgumentParser(description='Organize and customize Nmap scans for large target sets')

    parser.add_argument('-config', metavar='c', type=str, default='config.yaml', help='YAML Config file to run.')
    parser.add_argument('-targets', metavar='i', type=str, default='targets.txt', help='List of targets separated by newlines. Can be URL\'s, CIDR\'s, or IP\'s')
    parser.add_argument('-output', metavar='o', type=str, default='./', help='Parent output directory. Scans will create a directory under the parent for each scan.')

    args = parser.parse_args()

    if args.output[-1] != '/':
        args.output += '/'
    return args


'''
Join scripts in a comma separated list
'''
def process_scripts(scripts):
    if scripts is None:
        return None
    return "--script=" + ",".join(scripts)


'''
A few special cases allow for Nmap syntax for declaring all ports.
Otherwise, join them with commas.
'''
def process_ports(ports):
    if "all" in ports or "-" in ports:
        return "-p-"

    ports = "-p" + ",".join([str(port) for port in ports])
    return ports


'''
Process Script Arguments
'''
def process_script_args(args):
    return '--script-args="' + args.strip() + '"'


'''
I really thought this would be more complex.
'''
def process_misc_args(misc):
    return misc


'''
Processes the default entries added. duh.
Existing entries for scan, output type, ports, scripts and script args will NOT be overwritten.
If they do not exist, they will be pulled from the default entry.

Misc args are simply appended for simplicity. If you have a problem with that, open a pull request.
'''
def process_defaults(defaults, scan_object):
    for attribute in defaults.scanAttributes:

        if attribute == 'misc':
            if 'misc' not in scan_object.scanAttributes:
                scan_object.scanAttributes['misc'] = defaults.scanAttributes['misc']
            else:
                scan_object.scanAttributes['misc'].extend(defaults.scanAttributes['misc'])

        if attribute not in scan_object.scanAttributes:
            scan_object.scanAttributes[attribute] = defaults.scanAttributes[attribute]

    return scan_object


'''
Processes and executes a scan
'''
def process_scan(scan_name, conf, args):
    # set up vars for this scan instance
    default = False
    scan = conf[scan_name]
    scan_object = scanObject()
    nmap = '/usr/bin/nmap'
    target_name = args.targets.split(".")[0]

    # default case flag
    is_default_case = False
    if scan_name == 'default':
        is_default_case = True

    # read in port, scripts and script args
    # translate to scan_object attributes
    try:
        scan_object.scanAttributes['ports'] = process_ports(scan['ports'])
    except KeyError:
        pass

    try:
        scan_object.scanAttributes['scripts'] = process_scripts(scan['scripts'])
    except KeyError:
        scripts = None

    # if no scripts, ignore args
    if scripts is not None:
        try:
            scan_object.scanAttributes['script_args'] = process_script_args(scan['script_args'])
        except KeyError:
            pass

    try:
        scan_object.scanAttributes['misc'] = process_misc_args(scan['misc'])
    except KeyError:
        pass

    # dont attempt to execute a default case
    if is_default_case:
        default = scan_object
        return

    # add the default settings to the current scan
    if default:
        scan_object = process_defaults(default, scan_object)

    # more scan var setup
    scan_type = "-" + scan['scan']
    out_type = "-" + scan['out']
    out_name = args.output + target_name + "_" + scan_name

    # create scan dir
    if not os.path.isdir(args.output + scan_name):
        os.mkdirs(args.output + scan_name)

    # time stamp
    # nmap already has a time stamp, may remove
    cur_time = (time.strftime("%d %b %H:%M:%S")).upper()
    print(cur_time + "> Kicking off '" + scan_name + "' Scan")

    # begin subprocess cmd setup
    cmd = [nmap, scan_type, out_type, out_name, "-iL", args.targets]
    for attribute in scan_object.scanAttributes:
        if type(scan_object.scanAttributes[attribute]) is list:
            cmd.extend(scan_object.scanAttributes[attribute])
        else:
            cmd.append(scan_object.scanAttributes[attribute])

    # Execute
    # Print for testing
    print(cur_time + "> " + ' '.join(cmd))
    process = subprocess.run(cmd)


def main():

    # Load in data
    args = handle_args()
    conf = yaml.safe_load(open(args.config))

    # output dir does not exist, create it
    if not os.path.isdir(args.output):
        os.mkdirs(args.output)

    # Handle each scan
    for scan_name in conf:
        process_scan(scan_name, conf, args)


main()
