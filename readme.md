## About

## Quick Configuration of Linux Applications

To make it robust, 
this package has to be in `$HOME/archives/` in order to work well. 
If you want to place it some other place, 
just make a symbolic link to `$HOME/archives`.

1. Download this configuration package.

2. Go to the directory of a specific Unix/Linux distribution, 
    e.g., `$HOME/archives/code/bash/linux/debian/ubuntu`.

3. Source in the shell script `init.sh`.
        . init.sh 

4. Configure other applications of your interest (e.g., Vim).
    You can configure any application supported by this configuration package
    even if it is not installed.
    And when the application is installed,
    it works like a charm.
    If you do not like to configure every application manually,
    you can this step together with step 5 using

        linux.reconfig

## Quick Installation of Linux Packages

1. Follow steps in the section "Quick Configuration of Linux Applications" 
    to configure Linux applications.

2. Run preconfiguration.

        linux.preconfig

3. Install Linux packages of your interest.
    For example, 
    you can use the following command to install vim.

        ./linstall.ipy -- vim -i

    This installs the vim with Python, clipboard support, etc.
