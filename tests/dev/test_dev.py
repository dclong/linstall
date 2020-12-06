"""Test the dev module.
"""
import subprocess as sp
from xinstall.utils import is_ubuntu_debian, update_apt_source, run_cmd
if is_ubuntu_debian():
    update_apt_source(prefix="sudo", seconds=0)


def test_git():
    """Test installing and configuring Git.
    """
    cmd = "xinstall --sudo -y git -ic"
    run_cmd(cmd)


def test_pyjnius():
    """Test installing and configuring pyjnius.
    """
    cmd = "xinstall pyjnius -ic"
    run_cmd(cmd)


def test_nodejs():
    """Test installing nodejs.
    """
    cmd = "xinstall --sudo -y nodejs -ic"
    run_cmd(cmd)


def test_bash_lsp():
    """Test installing Bash Language Server.
    """
    cmd = "xinstall bash_lsp -c"
    run_cmd(cmd)


def test_rust():
    """Test installing the Rust programming language.
    """
    cmd = "xinstall --sudo -y rust -ic"
    run_cmd(cmd)


def test_ipython():
    """Test installing and configuring LightGBM.
    """
    cmd = "xinstall ipython -ic"
    run_cmd(cmd)


def test_pg_formatter():
    """Test installing and configuring pgFormatter.
    """
    cmd = "xinstall --sudo pgfmt -ic"
    run_cmd(cmd)
