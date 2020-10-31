"""Test the xinstall module.
"""
import stat
import os
from pathlib import Path
import subprocess as sp


def test_proxychains():
    """Test installing the blogging tools.
    """
    cmd = "xinstall --sudo -y pc -ic"
    sp.run(cmd, shell=True, check=True)


def test_ssh_client():
    """Test SSH client.
    """
    cmd = "xinstall ssh -c"
    sp.run(cmd, shell=True, check=True)
    for path in (Path.home() / ".ssh").glob("**/*"):
        st = path.stat()
        assert st.st_mode & (stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO) == stat.S_IRUSR | stat.S_IWUSR
        assert st.st_uid == os.getuid()
        assert st.st_gid == os.getgid()
