"""Test the dev module.
"""
from pathlib import Path
import shutil
import subprocess as sp
import tomlkit
from deepdiff import DeepDiff
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


def test_golang():
    """Test installing GoLANG.
    """
    cmd = "xinstall --sudo -y golang -ic"
    run_cmd(cmd)


def test_rust():
    """Test installing the Rust programming language.
    """
    cmd = "xinstall --sudo -y rust -ic"
    run_cmd(cmd)


def test_rustup():
    """Test installing the Rust programming language.
    """
    cmd = "xinstall --sudo -y rustup -ic"
    run_cmd(cmd)


def test_poetry():
    """Test installing and configuring Poetry.
    """
    cmd = "xinstall poetry -ic"
    run_cmd(cmd)


def test_ipython():
    """Test installing and configuring LightGBM.
    """
    cmd = "xinstall ipython -ic && python3 -m IPython -c ls"
    run_cmd(cmd)


def test_pg_formatter():
    """Test installing and configuring pgFormatter.
    """
    cmd = "xinstall --sudo pgfmt -ic"
    run_cmd(cmd)


def _comp_toml_cmd(src_toml, cmd) -> bool:
    """Compare TOML files after running a xinstall sub-command.
    """
    # test on 1.toml
    dir_ = BASE_DIR / "output" / cmd / src_toml.name
    dir_.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_toml, dir_ / "pyproject.toml")
    cmd = f"xinstall {cmd} -ic -d {dir_}"
    sp.run(cmd, shell=True, check=True)
    diff = DeepDiff(
        tomlkit.loads(src_toml.read_text()),
        tomlkit.loads((dir_ / "pyproject.toml").read_text()),
        ignore_order=True
    )
    print(diff)
    return not diff


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
