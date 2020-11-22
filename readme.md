# [xinstall](https://github.com/dclong/xinstall): Easy Cross-platform Installation and Configuration of Apps

## Installation
Note: It is best to install `xinstall` into a system-wide location 
(rather than users' local directories)
so that the command `xinstall` is always on `$PATH`.
You can download a copy of the latest release and install it using pip.
```
sudo pip3 install -U https://github.com/dclong/xinstall/releases/download/v0.26.1/xinstall-0.26.1-py3-none-any.whl
```
Or you can use the following command to install the latest main branch
if you have pip 20.0+.
```
sudo pip3 install -U git+https://github.com/dclong/xinstall@main
```
## Usage

1. Run `xinstall -h` for the help doc.

2. Update xinstall.

        xinstall xinstall -ic
        
2. Below is an example of install SpaceVim and configure it.

        xinstall svim -ic
        
### sudo Permission

xinstall has 3 levels of `sudo` permission.

- (L1) Non-root user running `xinstall subcmd -ic`: no `sudo` permission
- (L2) Non-root user running `xinstall --sudo subcmd -ic`: `sudo` is called when necessary
- (L3) Non-root user running `sudo xinstall subcmd -ic`: root permission everywhere
- (L3) root user running `xinstall subcmd -ic`: root permission everywhere

The suggested way is to run `xinstal --sudo subcmd -ic` using non-root user if `sudo` permission is required.
`sudo xinstall subcmd -ic` might have side effect as some tools are installed to the local user directory,
in which case `sudo xinstall subcmd -ic` installs the tool into `/root/` 
which might not what you wwant.

## Proxy

Some tools used by xinstall respect environment variables `http_proxy` and `https_proxy`.
Exporting those 2 evironment variable will make most part of xinstall work if proxy is required. 
```
export http_proxy=http://server_ip:port
export https_proxy=http://server_ip:port
```
