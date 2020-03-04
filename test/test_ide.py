"""Test the ide module.
"""
import subprocess as sp
sp.run("sudo apt-get update", shell=True, check=True)


def test_intellij_idea():
    """Test installing and configuring IntelliJ Idea.
    """
    cmd = "xinstall intellij"
    sp.run(cmd, shell=True, check=True)