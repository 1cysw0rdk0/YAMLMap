# YAMLMap
Leverage YAML to customize and organize Nmap results for large target lists.

## Setup
```
sudo apt install nmap
pip3 -r install requirements.txt
```

## Usage
`./YamlMap.py [-config config.yaml] [-targets target.txt]`
- -config defaults to config.yaml
- -targets defaults to target.txt

## YAML Config

YAMLMap creates the Nmap scans based off of a yaml file (default: config.yaml).

At the moment, the following fields are supported:
* A unique name for the scan
* A list of ports to scan
* A list of .nse scripts to run (.nse not required)
* A list of script arguments
* A scan type (ex: sS, sV, sU)
* An output type (ex: oA, oN, oX)
* Miscellaneous Arguments via a misc tag

Multiple scans can be specified in one Config.yaml file, and will be run sequentially.
Results from the scans will be named using the name of the target list and the scan name.

#### Config.yaml structure
```YAML
---
Scan_Name:
  ports:
    - 21
    - 22
  scripts:
    - script_name
  script_args: >
    script.arg='value',
    script2.arg='value2'
  scan_type: sS
  out_type: oA
  misc:
    - --open
    - -g53
```
Note that the order of the tags is irrelevant. Duplicating tags may break things.

#### Config.yaml for an FTP scan
```YAML
---
ftp:
  ports:
    - 21
    - 20
  scripts:
    - ftp_anon
  scan: sS
  out: oA
```
Ports can be specified in ranges, using a `-` for all ports, using `all` for all ports
#### Config.yaml for a scan which scans all TCP ports
```YAML
---
all:
  ports: all
    - all
    - "-"
  scan: sS
  out: oA
```

## Planned Features

- [x] Host discovery settings
- [x] Timing and performance settings 
- [x] Miscellaneous settings
- [ ] 'Global' settings for all scans
- [ ] Aliases / scan nicknames (ex: stealth -> sS, version -> sV)
- [ ] Option to zip results
- [ ] Email alert when scan complete
  - [ ] Attach results?
