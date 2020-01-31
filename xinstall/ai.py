"""Install AI related tools.
"""
from pathlib import Path
from .utils import HOME, run_cmd, namespace, add_subparser


def kaggle(**kwargs):
    """Insert the Python package kaggle.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install --user kaggle"
        run_cmd(cmd)
    if args.config:
        home_host = Path("/home_host/dclong/")
        kaggle_home_host = home_host / ".kaggele"
        kaggle_home = HOME / ".kaggele"
        if home_host.is_dir():
            kaggle_home_host.mkdir(exist_ok=True)
            try:
                kaggle_home.symlink_to(kaggle_home_host)
            except FileExistsError:
                pass
        else:
            kaggle_home.mkdir(exist_ok=True)
    if args.uninstall:
        pass


def add_subparser_kaggle(subparsers):
    add_subparser(subparsers, "kaggle", 
        func="kaggle",
        aliases=[])


def lightgbm(**kwargs):
    """Insert the Python package kaggle.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install --user lightgbm scikit-learn pandas matplotlib scipy graphviz"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass


def add_subparser_lightgbm(subparsers):
    add_subparser(subparsers, "lightgbm", 
        func="lightgbm",
        aliases=[])


def pytorch(**kwargs):
    """Insert the Python package kaggle.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install torch==1.4.0+cpu torchvision==0.5.0+cpu -f https://download.pytorch.org/whl/torch_stable.html"
        if args.gpu:
            cmd = f"{args.pip} install torch torchvision"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass


def _pytorch_args(subparser):
    subparser.add_argument(
        "--gpu",
        dest="gpu",
        action="store_true",
        help="Install the GPU version of PyTorch."
    )


def add_subparser_pytorch(subparsers):
    add_subparser(subparsers, "PyTorch", 
        func="pytorch",
        aliases=[], add_argument=_pytorch_args)


def autogluon(**kwargs):
    """Insert the Python package kaggle.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install mxnet autogluon"
        if args.gpu:
            cmd = f"{args.pip} install mxnet-cu100 autogluon"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass


def _autogluon_args(subparser):
    subparser.add_argument(
        "--gpu",
        dest="gpu",
        action="store_true",
        help="Install the GPU version of AutoGluon."
    )


def add_subparser_autogluon(subparsers):
    add_subparser(
        subparsers, "AutoGluon", 
        func="autogluon",
        aliases=[], add_argument=_autogluon_args
    )
