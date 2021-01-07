"""Install big data related tools.
"""
import importlib
from typing import Union
import logging
from pathlib import Path
import re
from urllib.request import urlopen, urlretrieve
from argparse import Namespace
import tempfile
from tqdm import tqdm
import pandas as pd
import findspark
from .utils import (
    BASE_DIR,
    run_cmd,
    add_subparser,
    option_pip_bundle,
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
    logging.info("Parsing the latest version of Spark...")
    pattern = br"Latest Release \(Spark (\d.\d.\d)\)"
    resp = urlopen("https://spark.apache.org/downloads.html")
    for line in resp:
        match = re.search(pattern, line)
        if match:
            return match.group(1).decode()
    return "3.0.1"


def _download_spark(args: Namespace, spark_hdp: str, desfile: Path):
    mirrors = args.mirrors + (
        "http://archive.apache.org/dist/spark",
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
    )
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
    if not args.spark_version:
        args.spark_version = get_spark_version()
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
            f"""echo '{conf}' | {args.prefix} tee \
                {spark_home / 'conf/spark-defaults.conf'} > /dev/null"""
        )
        logging.info(
            "Spark is configured to use %s as the metastore database and %s as the Hive warehouse.",
            metastore_db, warehouse
        )
        # create databases and tables
        if args.schema_dir:
            create_dbs(spark_home, args.schema_dir)
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
    subparser.add_argument(
        "-s",
        "--schema",
        "--schema-dir",
        dest="schema_dir",
        type=Path,
        default=None,
        help="The path to a directory containing schema information." \
            "The directory contains subdirs whose names are databases to create." \
            "Each of those subdirs (database) contain SQL files of the format db.table.sql" \
            "which containing SQL code for creating tables."
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
        cmd = f"{args.pip} install {args.user_s} {args.pip_option} pyspark findspark"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = f"{args.pip} uninstall pyspark findspark"
        run_cmd(cmd)


def _pyspark_args(subparser):
    option_pip_bundle(subparser)


def _add_subparser_pyspark(subparsers):
    add_subparser(subparsers, "PySpark", func=pyspark, add_argument=_pyspark_args)


def dask(args):
    """Install the Python module dask.
    :param yes:
    :param install:
    :param config:
    :param uninstall:
    """
    if args.install:
        cmd = f"{args.pip} install {args.user_s} {args.pip_option} dask[complete]"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = f"{args.pip} uninstall dask"
        run_cmd(cmd)


def _dask_args(subparser):
    option_pip_bundle(subparser)


def _add_subparser_dask(subparsers):
    add_subparser(subparsers, "dask", func=dask, add_argument=_dask_args)


def _alter_spark_sql(sql: str, hadoop_local: Union[str, Path]) -> str:
    """Handle special paths in SQL code so that it can be used locally.

    :param path: The path to a file containing SQL code for creating a Hive table.
    :return: The altered SQL code which can be used locally.
    """
    sql = sql.replace(r"^viewfs://[^/]/", "/")
    prefixes = ["/sys/", "/apps", "/user"]
    for prefix in prefixes:
        sql = sql.replace(prefix, f"{hadoop_local}{prefix}")
    return sql


def _create_db(spark_session, dbase: Union[Path, str], hadoop_local) -> None:
    """Create a database and tables belong to the database.

    :param dbase: A path containing information about the database to create.
    The directory name of the path is the name of the database,
    and the directory containing SQL files for creating Hive tables.
    """
    print("\n\n")
    if isinstance(dbase, str):
        dbase = Path(dbase)
    dbase = dbase.resolve()
    logging.info("Creating database %s...", dbase.stem)
    spark_session.sql(f"CREATE DATABASE IF NOT EXISTS {dbase.stem}")
    tables = pd.read_parquet(dbase)
    for path in dbase.glob("*.txt"):
        with path.open("r") as fin:
            table = fin.readline().strip()
            if spark_session.catalog._jcatalog.tableExists(table):
                continue
            fields = [line.strip() for line in fin]
        sql = f"""
            CREATE TABLE {table} (
                {(",\n" + " " * 16).join(fields)}
            ) USING PARQUET
            """
            print("\n")
            logging.info("Creating the data table %s:\n%s", table, sql)
            spark_session.sql(sql)
    #for _, (table, sql) in tables[["full_name", "source_code"]].iterrows():
    #    if not spark_session.catalog._jcatalog.tableExists(table):
    #        print("\n")
    #        sql = _alter_spark_sql(sql, hadoop_local)
    #        logging.info("Creating the data table %s:\n%s", table, sql)
    #        try:
    #            spark_session.sql(sql)
    #        except Exception as err:
    #            logging.error("Failed to create the data table %s.\n%s", table, err)


def create_dbs(spark_home: Union[str, Path], schema_dir: Union[Path, str]) -> None:
    """Create databases and tables belong to them.

    :param spark_home: The home of Spark installation.
    :param schema_dir: The path to a directory containing schema information.
    The directory contains subdirs whose names are databases to create.
    Each of those subdirs (database) contain SQL files of the format db.table.sql
    which containing SQL code for creating tables.
    """
    if isinstance(spark_home, Path):
        spark_home = str(spark_home)
    findspark.init(spark_home)
    spark_session = importlib.import_module("pyspark").sql.SparkSession \
        .builder.appName("Create_Empty_Hive_Tables").enableHiveSupport().getOrCreate()
    hadoop_local = Path.home() / ".hadoop"
    if not hadoop_local.is_dir():
        hadoop_local.mkdir(parents=True, exist_ok=True)
    if isinstance(schema_dir, str):
        schema_dir = Path(schema_dir)
    for path in schema_dir.iterdir():
        if path.is_dir():
            _create_db(spark_session, path, hadoop_local)


#def _permission():
#    dirs = [
#        "/opt/spark/metastore_db",
#        "/opt/spark/warehouse",
#    ]
#    for dir_ in dirs:
#        sp.run(f"mkdir -p {dir_} && chmod -R 777 {dir_}", shell=True, check=True)
