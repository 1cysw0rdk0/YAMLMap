import subprocess
import argparse
import yaml
import time

# Handle Commandline args
parser = argparse.ArgumentParser(description='Organize and customize Nmap scans for large target sets')

parser.add_argument('-config', metavar='c', type=str, default='config.yaml', help='YAML Config file to run.')
parser.add_argument('-targets', metavar='i', type=str, default='targets.txt', help='List of targets separated by newlines. Can be URL\'s, CIDR\'s, or IP\'s')

args = parser.parse_args()

# Load in yaml config
conf = yaml.safe_load(open(args.config))

nmap = '/usr/bin/nmap'
target_name = ""

# Handle each scan
for scan_name in conf:
    scan = conf[scan_name]

    # Setup scan vars
    ports = "-p"+",".join([str(port) for port in scan['ports']])
    scripts = "--scripts=" + ",".join(scan['scripts'])
    scan_type = "-" + scan['scan']
    out_type = "-" + scan['out']
    out_name = target_name + "_" + scan_name

    cur_time = (time.strftime("%d %b %H:%M:%S")).upper()
    print(cur_time + "> Kicking off " + scan_name + " Scan")

    process = subprocess.run([nmap, scan_type, ports, scripts, out_type, out_name, "-iL", args.targets])
    process.wait()


