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
    cmd = "xinstall sshc -c"
    sp.run(cmd, shell=True, check=True)
    RWX_ALL = stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO
    for path in (Path.home() / ".ssh").glob("**/*"):
        st = path.stat()
        assert st.st_uid == os.getuid()
        assert st.st_gid == os.getgid()
        if path.is_file():
            assert st.st_mode & RWX_ALL == stat.S_IRUSR | stat.S_IWUSR
        else:
            assert st.st_mode & RWX_ALL == stat.S_IRWXU
