"""Test the xinstall module.
"""
import subprocess as sp
sp.run("sudo apt-get update", shell=True, check=True)


def test_version():
    """Test the version command.
    """
    cmd = "xinstall version"
    sp.run(cmd, shell=True, check=True)


def test_wajig():
    """Test the wajig command.
    """
    cmd = "xinstall --sudo -y wajig -ic"
    sp.run(cmd, shell=True, check=True)


def test_install_py_github():
    """Test the wajig command.
    """
    cmd = "xinstall install_py_github https://github.com/dclong/dsutil --sys"
    sp.run(cmd, shell=True, check=True)


def test_nomachine():
    """Test installing and configuring NoMachine.
    """
    cmd = "xinstall nomachine"
    sp.run(cmd, shell=True, check=True)


def test_intellij_idea():
    """Test installing and configuring IntelliJ Idea.
    """
    cmd = "xinstall intellij"
    sp.run(cmd, shell=True, check=True)


def test_git():
    """Test installing and configuring Git.
    """
    cmd = "xinstall --sudo -y git -ic"
    sp.run(cmd, shell=True, check=True)


def test_pyjnius():
    """Test installing and configuring pyjnius.
    """
    cmd = "xinstall pyjnius -ic"
    sp.run(cmd, shell=True, check=True)


def test_nodejs():
    """Test installing nodejs.
    """
    cmd = "xinstall --sudo -y nodejs -ic"
    sp.run(cmd, shell=True, check=True)


def test_bash_lsp():
    """Test installing Bash Language Server.
    """
    cmd = "xinstall bash_lsp -c"
    sp.run(cmd, shell=True, check=True)


def test_spark():
    """Test installing Spark.
    """
    cmd = "xinstall --sudo spark -ic"
    sp.run(cmd, shell=True, check=True)


def test_pyspark():
    """Test installing PySpark.
    """
    cmd = "xinstall pyspark -ic"
    sp.run(cmd, shell=True, check=True)