"""Test the dev module.
"""
import subprocess as sp
from xinstall.utils import is_debian_series, update_apt_source


def setup_module():
    """Setup for testing the bigdata module.
    """
    if is_debian_series():
        update_apt_source(prefix="sudo", seconds=0)


def test_spark():
    """Test installing Spark.
    """
    cmd = "xinstall --sudo spark -ic --loc /opt"
    sp.run(cmd, shell=True, check=True)


def test_pyspark():
    """Test installing PySpark.
    """
    cmd = "xinstall pyspark -ic"
    sp.run(cmd, shell=True, check=True)
