"""Install big data related tools.
"""
import logging
from pathlib import Path
import re
from urllib.request import urlopen, urlretrieve
from argparse import Namespace
import tempfile
from tqdm import tqdm
from .utils import (
    BASE_DIR,
    run_cmd,
    add_subparser,
    option_user,
    option_pip,
    is_win,
)
logging.basicConfig(
    format=
    "%(asctime)s | %(module)s.%(funcName)s: %(lineno)s | %(levelname)s: %(message)s",
    level=logging.INFO
)


class ProgressBar(tqdm):
    """A class for reporting progress with urlretrieve.
    """
    def update_progress(self, block_num=1, block_size=1, total_size=None):
        """Update progress.
        """
        if total_size is not None:
            self.total = total_size
        self.update(block_num * block_size - self.n)


def get_spark_version() -> str:
    """Get the latest version of Spark.
    """
    pattern = b"Latest Release \(Spark (\d.\d.\d)\)"
    resp = urlopen("https://spark.apache.org/downloads.html")
    for line in resp:
        match = re.search(pattern, line)
        if match:
            return match.group(1).decode()
    return "3.0.1"


def _download_spark(args: Namespace, spark_hdp: str, desfile: Path):
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
    if not args.spark_version:
        args.spark_version = get_spark_version()
    for mirror in mirrors:
        url = f"{mirror}/spark-{args.spark_version}/{spark_hdp}.tgz"
        try:
            logging.info("Downloading Spark from: %s", url)
            with ProgressBar(unit="B", unit_scale=True, miniters=1) as progress:
                urlretrieve(url, desfile, progress.update_progress)
            return
        except Exception:
            logging.info("Failed to download Spark from: %s", url)


def spark(args):
    """Install Spark.
    :param yes:
    :param install:
    :param config:
    :param uninstall:
    :param version:
    """
    dir_ = args.location.resolve()
    spark_hdp = f"spark-{args.spark_version}-bin-hadoop{args.hadoop_version}"
    spark_home = dir_ / spark_hdp
    desfile = Path(tempfile.mkdtemp()) / f"{spark_hdp}.tgz"
    if args.install:
        dir_.mkdir(exist_ok=True)
        _download_spark(args, spark_hdp, desfile)
        cmd = f"{args.prefix} tar -zxf {desfile} -C {dir_} && rm {desfile}"
        run_cmd(cmd)
    if args.config:
        # metastore db
        metastore_db = spark_home / "metastore_db"
        run_cmd(
            f"{args.prefix} mkdir -p {metastore_db} && "
            f"{args.prefix} chmod -R 777 {metastore_db}"
        )
        # warehouse
        warehouse = spark_home / "warehouse"
        if is_win():
            warehouse.mkdir(parents=True, exist_ok=True)
        else:
            run_cmd(
                f"{args.prefix} mkdir -p {warehouse} && "
                f"{args.prefix} chmod -R 777 {warehouse}"
            )
        # spark-defaults.conf
        conf = (BASE_DIR / "spark/spark-defaults.conf"
               ).read_text().replace("$SPARK_HOME", str(spark_home))
        run_cmd(
            f"echo '{conf}' | {args.prefix} tee {spark_home / 'conf/spark-defaults.conf'} > /dev/null"
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
        default=Path(),
        help="The location to install Spark to."
    )


def _add_subparser_spark(subparsers):
    add_subparser(subparsers, "Spark", func=spark, add_argument=_spark_args)


def pyspark(args):
    """Install PySpark.
    :param yes:
    :param install:
    :param config:
    :param uninstall:
    :param version:
    """
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


def optimuspyspark(args):
    """Install Optimus (a PySpark package for data profiling).
    :param yes:
    :param install:
    :param config:
    :param uninstall:
    :param version:
    """
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


def dask(args):
    """Install the Python module dask.
    :param yes:
    :param install:
    :param config:
    :param uninstall:
    """
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
