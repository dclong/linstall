## About

## Quick Configuration of Linux Applications

1. Download this configuration package.

2. Go to the root directory ("config") of this configuration package.

3. Go to subdirectory "linux/common/bash".

4. Source in the bash configuration file "bashrc" 
using 
```bash
. bashrc 
```
or 
```bash
source bashrc.
```
5. Configure shell. 
```bash
linfig.shell
```
This is the most important step. 
With this done,
you do not have to go through step 1-5 again 
when you want to configure another application next time.

6. Configure other applications of your interest 
(e.g., Vim).
You can configure any application supported by this configuration package
even if it is not installed.
And when the application is installed,
it works like a charm.
If you do not like to configure every application manually,
you can this step together with step 5 using
```bash
linux.reconfig
```
## Quick Installation of Linux Packages

1. Follow steps in the section "Quick Configuration of Linux Applications" 
to configure Linux applications.

2. Run preconfiguration.
```bash
linux.preconfig
```
3. Install Linux packages of your interest.
For example, 
you can use the following command to install vim.
```bash
linstall.vim
```
This installs the vim with Python, clipboard support, etc.

4. If you do not like to install every package manually,
you can ...