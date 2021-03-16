"""Test the dev module.
"""
from pathlib import Path
import shutil
import subprocess as sp
from xinstall.utils import is_ubuntu_debian, update_apt_source, run_cmd

BASE_DIR = Path(__file__).resolve().parent


def setup_module():
    """Setup for testing the dev module.
    """
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


#@pytest.mark.skipif(sys.version_info >= (3, 8), reason="Doesn't work with Python 3.8 on Ubuntu LTS")
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


def test_pylint():
    """Test installing pylint.
    """
    # test on 1.toml
    dir_ = Path("/tmp/pylint/1")
    dir_.mkdir(parents=True, exist_ok=True)
    shutil.copy2(BASE_DIR / "1.toml", dir_ / "pyproject.toml")
    cmd = f"xinstall pylint -ic -d {dir_}"
    sp.run(cmd, shell=True, check=True)
    # test on 2.toml
    dir_ = Path("/tmp/pylint/2")
    dir_.mkdir(parents=True, exist_ok=True)
    shutil.copy2(BASE_DIR / "2.toml", dir_ / "pyproject.toml")
    cmd = f"xinstall pylint -ic -d {dir_}"
    sp.run(cmd, shell=True, check=True)


def test_yapf():
    """Test installing yapf.
    """
    # test on 1.toml
    dir_ = Path("/tmp/yapf/1")
    dir_.mkdir(parents=True, exist_ok=True)
    shutil.copy2(BASE_DIR / "1.toml", dir_ / "pyproject.toml")
    cmd = f"xinstall yapf -ic -d {dir_}"
    sp.run(cmd, shell=True, check=True)
    # test on 2.toml
    dir_ = Path("/tmp/yapf/2")
    dir_.mkdir(parents=True, exist_ok=True)
    shutil.copy2(BASE_DIR / "2.toml", dir_ / "pyproject.toml")
    cmd = f"xinstall yapf -ic -d {dir_}"
    sp.run(cmd, shell=True, check=True)
