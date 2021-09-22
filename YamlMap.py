#! /usr/bin/python3

import subprocess
import argparse
import yaml
import time


class scanObject:
    def __init__(self):
        self.scanAttributes = {}


def handle_args():
    # Handle Commandline args
    parser = argparse.ArgumentParser(description='Organize and customize Nmap scans for large target sets')

    parser.add_argument('-config', metavar='c', type=str, default='config.yaml', help='YAML Config file to run.')
    parser.add_argument('-targets', metavar='i', type=str, default='targets.txt', help='List of targets separated by newlines. Can be URL\'s, CIDR\'s, or IP\'s')

    args = parser.parse_args()
    return args


def process_scripts(scripts):
    if scripts is None:
        return None
    scripts_string = "--script="
    scripts = ",".join(scripts)
    return scripts_string + scripts


def process_ports(ports):
    if "all" in ports or "-" in ports:
        return "-p-"

    ports = "-p" + ",".join([str(port) for port in ports])
    return ports


def process_script_args(args):
    return '--script-args="' + args.strip() + '"'


def process_misc_args(misc):
    print(misc)
    return misc


def main():
    # Load in data
    args = handle_args()
    conf = yaml.safe_load(open(args.config))

    nmap = '/usr/bin/nmap'
    target_name = args.targets.split(".")[0]

    # Handle each scan
    for scan_name in conf:
        scan = conf[scan_name]
        scan_object = scanObject()

        # Setup scan vars
        try:
            scan_object.scanAttributes['ports'] = process_ports(scan['ports'])
        except KeyError:
            pass

        try:
            scan_object.scanAttributes['scripts'] = process_scripts(scan['scripts'])
        except KeyError:
            scripts = None

        if scripts is not None:
            try:
                scan_object.scanAttributes['script_args'] = process_script_args(scan['script_args'])
            except KeyError:
                pass

        try:
            scan_object.scanAttributes['misc'] = process_misc_args(scan['misc'])
        except KeyError:
            pass

        scan_type = "-" + scan['scan']
        out_type = "-" + scan['out']
        out_name = target_name + "_" + scan_name

        cur_time = (time.strftime("%d %b %H:%M:%S")).upper()
        print(cur_time + "> Kicking off '" + scan_name + "' Scan")

        cmd = [nmap, scan_type, out_type, out_name, "-iL", args.targets]
        for attribute in scan_object.scanAttributes:
            if type(scan_object.scanAttributes[attribute]) is list:
                cmd.extend(scan_object.scanAttributes[attribute])
            else:
                cmd.append(scan_object.scanAttributes[attribute])

        # Print for testing
        print(cur_time + "> " + ' '.join(cmd))
        process = subprocess.run(cmd)


main()
