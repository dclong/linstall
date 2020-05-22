"""Install big data related tools.
"""
from pathlib import Path
from .utils import (
    is_ubuntu_debian,
    is_centos_series,
    is_linux,
    is_fedora,
    update_apt_source,
    brew_install_safe,
    is_macos,
    remove_file_safe,
    run_cmd,
    namespace,
    add_subparser,
    option_user,
)


def spark(**kwargs):
    """Install Spark into /opt/spark.
    :param yes:
    :param install:
    :param config:
    :param uninstall:
    :param version:
    """
    args = namespace(kwargs)
    if args.install:
        spark_hdp = f"spark-{args.version}-bin-hadoop2.7"
        url = f"{args.mirror}/spark-{args.version}/{spark_hdp}.tgz"
        cmd = f"""curl {url} -o /tmp/{spark_hdp}.tgz \
                && tar -zxvf /tmp/{spark_hdp}.tgz -C /opt/ \
                && ln -svf /opt/{spark_hdp} /opt/spark \
                && rm /tmp/{spark_hdp}.tgz
            """
        run_cmd(cmd)
    if args.config:
        cmd = "export SPARK_HOME=/opt/spark"
        run_cmd(cmd)
    if args.uninstall:
        cmd = f"rm -rf /opt/spark*"
        run_cmd(cmd)


def _spark_args(subparser):
    subparser.add_argument(
        "-m",
        "--mirror",
        dest="mirror",
        default="http://us.mirrors.quenda.co/apache/spark/",
        help=
        f"The mirror (default http://us.mirrors.quenda.co/apache/spark/) of Spark to use."
    )
    subparser.add_argument(
        "-v",
        "--version",
        dest="version",
        default="2.4.5",
        help=f"The version of Spark to install."
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
        if not Path("/opt/spark").exists():
            spark(
                install=True,
                config=True,
                mirror="http://us.mirrors.quenda.co/apache/spark/",
                version="2.4.5",
                yes=args.yes
            )
        cmd = f"{args.pip} install {args._user_s} pyspark findspark"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = f"{args.pip} uninstall pyspark findspark"
        run_cmd(cmd)


def _add_subparser_pyspark(subparsers):
    add_subparser(subparsers, "PySpark", func=pyspark, add_argument=option_user)


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
        cmd = f"{args.pip} install {args._user_s} optimuspyspark"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = f"{args.pip} uninstall optimuspyspark"
        run_cmd(cmd)


def _add_subparser_optimuspyspark(subparsers):
    add_subparser(
        subparsers, "Optimus", func=optimuspyspark, add_argument=option_user
    )


def dask(**kwargs):
    """Install the Python module dask.
    :param yes:
    :param install:
    :param config:
    :param uninstall:
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install {args._user_s} dask[complete]"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = f"{args.pip} uninstall dask"
        run_cmd(cmd)


def _add_subparser_dask(subparsers):
    add_subparser(subparsers, "dask", func=dask, add_argument=option_user)
