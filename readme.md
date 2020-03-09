# Easy Cross-platform Installation and Configuration of Apps

## Installation
Note: It is best to install `xinstall` into a system-wide location rather than users' local directories.
You can download a copy of the latest release and install it using pip.
```
sudo pip3 install -U https://github.com/dclong/xinstall/releases/download/v0.5.2/xinstall-0.5.2-py3-none-any.whl
```
Or you can use the following script to download and install the latest version automatically.
```
curl -sSL www.legendu.net/media/install_py_github.py | python3 - https://github.com/dclong/xinstall --sudo --sys
```
## Usage

1. Run `xinstall -h` for the help doc.

2. Below is an example of install SpaceVim and configure it.

        xinstall svim -ic

## Proxy

Some tools used by xinstall respect environment variables `http_proxy` and `https_proxy`.
Exporting those 2 evironment variable will make most part of xinstall work if proxy is required. 
```
export http_proxy=http://server_ip:port
export https_proxy=http://server_ip:port
```
