"""Test the ide module.
"""
import subprocess as sp
from xinstall.utils import run_cmd


def test_intellij_idea():
    """Test installing and configuring IntelliJ Idea.
    """
    run_cmd("xinstall intellij")


def test_bash_lsp():
    """Test installing Bash Language Server.
    """
    run_cmd("xinstall svim -ic")
    run_cmd("xinstall bash_lsp -c")
