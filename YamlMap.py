#! /usr/bin/python3

import subprocess
import argparse
import yaml
import time


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


def main():
    # Load in data
    args = handle_args()
    conf = yaml.safe_load(open(args.config))

    nmap = '/usr/bin/nmap'
    target_name = ""

    # Handle each scan
    for scan_name in conf:
        scan = conf[scan_name]

        # Setup scan vars
        try:
            ports = process_ports(scan['ports'])
        except KeyError:
            ports = None

        try:
            scripts = process_scripts(scan['scripts'])
        except KeyError:
            scripts = None

        if scripts is not None:
            try:
                script_args = process_script_args(scan['script_args'])
            except KeyError:
                script_args = None
        else:
            script_args = None


        scan_type = "-" + scan['scan']
        out_type = "-" + scan['out']
        out_name = target_name + "_" + scan_name

        cur_time = (time.strftime("%d %b %H:%M:%S")).upper()
        print(cur_time + "> Kicking off " + scan_name + " Scan")

        # Print for testing
        print([nmap, scan_type, ports, scripts, out_type, out_name, "-iL", args.targets])
        #process = subprocess.run([nmap, scan_type, ports, scripts, out_type, out_name, "-iL", args.targets])

main()