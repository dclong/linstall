"""Install big data related tools.
"""
import os
import logging
from pathlib import Path
import urllib
from argparse import Namespace
from .utils import (
    run_cmd,
    namespace,
    add_subparser,
    option_user,
    option_pip,
)
logging.basicConfig(
    format=
    "%(asctime)s | %(module)s.%(funcName)s: %(lineno)s | %(levelname)s: %(message)s",
    level=logging.INFO
)


def _download_spark(args: Namespace, spark_hdp: str):
    mirrors = args.mirrors + (
            "http://apache.mirrors.hoobly.com/spark",
            "http://apache.spinellicreations.com/spark",
            "http://mirror.cc.columbia.edu/pub/software/apache/spark",
            "http://mirror.cogentco.com/pub/apache/spark",
            "http://mirror.metrocast.net/apache/spark",
            "http://mirrors.advancedhosters.com/apache/spark",
            "http://mirrors.ibiblio.org/apache/spark",
            "http://apache.claz.org/spark",
            "http://apache.osuosl.org/spark",
            "http://ftp.wayne.edu/apache/spark",
            "http://mirror.olnevhost.net/pub/apache/spark",
            "http://mirrors.gigenet.com/apache/spark",
            "http://mirrors.koehn.com/apache/spark",
            "http://mirrors.ocf.berkeley.edu/apache/spark",
            "http://mirrors.sonic.net/apache/spark",
            "http://us.mirrors.quenda.co/apache/spark",
            "http://archive.apache.org/dist/spark",
    )
    desfile = f"/tmp/{spark_hdp}.tgz"
    for mirror in mirrors:
        url = f"{mirror}/spark-{args.spark_version}/{spark_hdp}.tgz"
        try:
            logging.info("Downloading Spark from: %s", url)
            urllib.urlretrieve(url, desfile)
        except:
            logging.info("Failed to download Spark from: %s", url)


def spark(**kwargs):
    """Install Spark.
    :param yes:
    :param install:
    :param config:
    :param uninstall:
    :param version:
    """
    args = namespace(kwargs)
    dir_ = args.location.resolve()
    spark_hdp = f"spark-{args.spark_version}-bin-hadoop{args.hadoop_version}"
    spark_home = dir_ / spark_hdp
    if args.install:
        dir_.mkdir(exist_ok=True)
        _download_spark(args)
        cmd = f"""{args.prefix} tar -zxf /tmp/{spark_hdp}.tgz -C {dir_} \
                && rm /tmp/{spark_hdp}.tgz
            """
        run_cmd(cmd)
    if args.config:
        mask = os.umask(0)
        metastore_db = spark_home / "metastore_db"
        metastore_db.mkdir(parents=True, exist_ok=True)
        warehouse = spark_home / "warehouse"
        warehouse.mkdir(parents=True, exist_ok=True)
        os.umask(mask)
        (spark_home / "conf/spark-defaults.conf").write_text(
            f"spark.driver.extraJavaOptions -Dderby.system.home={spark_home}/metastore_db\n"
            f"spark.sql.warehouse.dir {spark_home}/warehouse"
        )
        logging.info(
            "Spark is configured to use %s as the metastore database and %s as the Hive warehouse.",
            metastore_db, warehouse
        )
    if args.uninstall:
        cmd = f"{args.prefix} rm -rf {spark_home}"
        run_cmd(cmd)


def _spark_args(subparser):
    subparser.add_argument(
        "-m",
        "--mirrors",
        dest="mirrors",
        nargs="+",
        default=(),
        help="The mirror of Apache Spark to use."
    )
    subparser.add_argument(
        "--sv",
        "--spark-version",
        dest="spark_version",
        default="3.0.0",
        help="The version of Spark to install."
    )
    subparser.add_argument(
        "--hv",
        "--hadoop-version",
        dest="hadoop_version",
        default="3.2",
        help="The version of Hadoop to use."
    )
    subparser.add_argument(
        "--loc",
        "--location",
        dest="location",
        type=Path,
        default="/opt",
        help="The location to install Spark to."
    )


def _add_subparser_spark(subparsers):
    add_subparser(subparsers, "Spark", func=spark, add_argument=_spark_args)


def pyspark(**kwargs):
    """Install PySpark.
    :param yes:
    :param install:
    :param config:
    :param uninstall:
    :param version:
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install {args.user_s} pyspark findspark"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = f"{args.pip} uninstall pyspark findspark"
        run_cmd(cmd)


def _pyspark_args(subparser):
    option_user(subparser)
    option_pip(subparser)


def _add_subparser_pyspark(subparsers):
    add_subparser(subparsers, "PySpark", func=pyspark, add_argument=_pyspark_args)


def optimuspyspark(**kwargs):
    """Install Optimus (a PySpark package for data profiling).
    :param yes:
    :param install:
    :param config:
    :param uninstall:
    :param version:
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install {args.user_s} optimuspyspark"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = f"{args.pip} uninstall optimuspyspark"
        run_cmd(cmd)


def _add_subparser_optimuspyspark(subparsers):
    add_subparser(subparsers, "Optimus", func=optimuspyspark, add_argument=option_user)


def dask(**kwargs):
    """Install the Python module dask.
    :param yes:
    :param install:
    :param config:
    :param uninstall:
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install {args.user_s} dask[complete]"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = f"{args.pip} uninstall dask"
        run_cmd(cmd)


def _add_subparser_dask(subparsers):
    add_subparser(subparsers, "dask", func=dask, add_argument=option_user)
