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


def _copy_toml(src_toml, des_dir):
    des_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_toml, des_dir / "pyproject.toml")


def _comp_toml_cmd(src_toml, cmd) -> bool:
    """Compare TOML files after running a xinstall sub-command.
    """
    # test on 1.toml
    dir_ = BASE_DIR / "output" / cmd / src_toml
    _copy_toml(src_toml, dir_)
    cmd = f"xinstall {cmd} -ic -d {dir_}"
    sp.run(cmd, shell=True, check=True)
    return src_toml.read_text() == (dir_ / "pyproject.toml").read_text()
    
def test_pylint():
    """Test installing pylint.
    """
    assert _comp_toml_cmd(BASE_DIR / "1.toml", "pylint")
    assert not _comp_toml_cmd(BASE_DIR / "2.toml", "pylint")


def test_yapf():
    """Test installing yapf.
    """
    assert _comp_toml_cmd(BASE_DIR / "1.toml", "yapf")
    assert not _comp_toml_cmd(BASE_DIR / "2.toml", "yapf")
