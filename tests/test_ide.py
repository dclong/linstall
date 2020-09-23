"""Test the ide module.
"""
import subprocess as sp


def test_intellij_idea():
    """Test installing and configuring IntelliJ Idea.
    """
    cmd = "xinstall intellij"
    sp.run(cmd, shell=True, check=True)