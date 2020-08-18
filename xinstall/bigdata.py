"""Install big data related tools.
"""
import os
import logging
from pathlib import Path
import shutil
from .utils import (
    BASE_DIR,
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


def spark(**kwargs):
    """Install Spark.
    :param yes:
    :param install:
    :param config:
    :param uninstall:
    :param version:
    """
    args = namespace(kwargs)
    dir_ = Path(args.location)
    spark_hdp = f"spark-{args.spark_version}-bin-hadoop{args.hadoop_version}"
    spark_home = dir_ / spark_hdp
    if args.install:
        dir_.mkdir(exist_ok=True)
        url = f"{args.mirror}/spark-{args.spark_version}/{spark_hdp}.tgz"
        logging.info("Downloading Spark from the URL: %s", url)
        cmd = f"""curl {url} -o /tmp/{spark_hdp}.tgz \
                && {args.prefix} tar -zxf /tmp/{spark_hdp}.tgz -C {dir_} \
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
        shutil.copy2(BASE_DIR / "spark/spark-defaults.conf", dir_ / "spark/conf/")
        logging.info(
            "Spark is configured to use %s as the metastore database and %s as the Hive warehouse.",
            metastore_db, warehouse
        )
    if args.uninstall:
        cmd = f"{args.prefix} rm -rf {dir_}/spark*"
        run_cmd(cmd)


def _spark_args(subparser):
    subparser.add_argument(
        "-m",
        "--mirror",
        dest="mirror",
        default="https://archive.apache.org/dist/spark",
        help="The mirror of Spark (default https://archive.apache.org/dist/spark) to use."
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
