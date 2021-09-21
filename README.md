# YAMLMap
Levarage YAML to organize Nmap results for large target lists

## Setup
###TODO###
Nmap and PyYAML installed.

## Usage
`python3 ./YamlMap.py [-config config.yaml] [-targets target.txt]`

## YAML Config

YAMLMap creates the Nmap scans based off of a yaml file (default: config.yaml).

At the moment, the following fields are supported:
* A unique name for the scan
* A list of ports to scan
* A list of .nse scripts to run
* A scan type (ex: sS, sV, sU)
* An output type (ex: oA, oN, oX)

Support for the following features is planned for the future:
* Host discovery settings
* Timing and Performance Settings

Multiple scans can be specified in one Config.yaml file, and will be run sequentially. Results from the scans will be named using the unique scan name as the filename.

#### Config.yaml structure
```YAML
---
Scan_Name:
  ports:
    - 21
    - 22
  scripts:
    - script_name
  scan_type:sS
  out_type:oA
```


#### Config.yaml for an FTP scan
```YAML
---
FTP:
  ports:
    - 21
    - 20
  scripts:
    - ftp_anon
  scan: sS
  out: oA

```

## Planned Features
### Short Term 
* Host discovery settings
* Timing and performance settings
* Miscellaneous settings 

### Long Term
* Aliases / scan nicknames (ex: stealth -> sS, version -> sV)
* Option to zip results
* Email alert when scan complete
  *  Attach results?
