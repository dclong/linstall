# Easy Cross-platform Installation and Configuration of Apps

## Installation
Note: `xinstall` should always be installed into your local user directory instead of a system-wide location.
You can download a copy of the latest release and install it using pip.
```
pip3 install --user -U xinstall-0.1.1-py3-none-any.whl
```
Or you can use the following script to download and install the latest version automatically.
```
curl -sSL www.legendu.net/media/install_py_github.py | python3 - https://github.com/dclong/xinstall
```
## Usage

1. Run `xinstall -h` for the help doc.

2. Below is an example of install SpaceVim and configure it.

        xinstall svim -ic
