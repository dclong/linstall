"""Test the xinstall module.
"""
import stat
import os
from pathlib import Path
import pytest
from xinstall.utils import is_win, run_cmd


def test_proxychains():
    """Test installing the blogging tools.
    """
    cmd = "xinstall --sudo -y pc -ic"
    run_cmd(cmd)


@pytest.mark.skipif(is_win(), reason="Skip test for Mac OS")
def test_ssh_client():
    """Test SSH client.
    """
    cmd = "xinstall sshc -c"
    run_cmd(cmd)
    RWX_ALL = stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO
    for path in (Path.home() / ".ssh").glob("**/*"):
        st = path.stat()
        assert st.st_uid == os.getuid()
        assert st.st_gid == os.getgid()
        if path.is_file():
            assert st.st_mode & RWX_ALL == stat.S_IRUSR | stat.S_IWUSR
        else:
            assert st.st_mode & RWX_ALL == stat.S_IRWXU
