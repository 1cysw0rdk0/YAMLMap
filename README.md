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

### Basic Structure
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

#### Sample YAML for an FTP scan
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

### Port Specification
Ports can be specified in ranges in several ways. Separate two numbers on one line with a `-` to scan ports between them.
Additionally, simply use a `-` or `all` to specify all 65,535 ports.
```YAML
---
all:
  ports: all
    - all
    - "-"
range:
  ports:
    - 1-1000
    - 1-100
```

### Default Scan Settings
Default settings can be set in a `default` scan block. Default settings apply to all scans, however any settings
specified in a scan will override the default. 

This can be used to cut down on some repetition in config files. Defaults will only be applied to scans that occur after
they're declared in the config file. 

#### Sample YAML for a default block
```YAML
default:
  scan: sS
  out: oA
  misc:
    - --open
    - -g53
all:
  ports: all
```

## Planned Features

- [x] Host discovery settings
- [x] Timing and performance settings 
- [x] Miscellaneous settings
- [x] Default settings for all scans
- [ ] Create directory for scan results
- [ ] Aliases / scan nicknames (ex: stealth -> sS, version -> sV)
- [ ] Option to zip results
- [ ] Email alert when scan complete
  - [ ] Attach results?
