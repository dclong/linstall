"""Install AI related tools.
"""
from pathlib import Path
import warnings
from .utils import HOME, USER, run_cmd, namespace, add_subparser, is_linux, is_macos


def kaggle(**kwargs):
    """Insert the Python package kaggle.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install --user kaggle"
        run_cmd(cmd)
    if args.config:
        home_host = Path(f"/home_host/{USER}/")
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


def _add_subparser_kaggle(subparsers):
    add_subparser(subparsers, "kaggle", func=kaggle, aliases=[])


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


def _add_subparser_lightgbm(subparsers):
    add_subparser(subparsers, "lightgbm", func=lightgbm, aliases=[])


def pytorch(**kwargs):
    """Insert PyTorch.
    """
    args = namespace(kwargs)
    if args.install:
        if is_linux():
            cmd = f"{args.pip} install torch torchvision"
            run_cmd(cmd)
        elif is_macos():
            cmd = f"{args.pip} install torch torchvision"
            run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass


#def _pytorch_args(subparser):
#    subparser.add_argument(
#        "--gpu",
#        dest="gpu",
#        action="store_true",
#        help="Install the GPU version of PyTorch."
#    )


def _add_subparser_pytorch(subparsers):
    add_subparser(
        subparsers,
        "PyTorch",
        func=pytorch,
        aliases=[],
    )


def autogluon(**kwargs):
    """Insert the Python package AutoGluon.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install mxnet autogluon"
        if args.cuda_version:
            version = args.cuda_version.replace(".", "")
            cmd = f"{args.pip} install mxnet-cu{version} autogluon"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass


def _autogluon_args(subparser):
    subparser.add_argument(
        "--cuda",
        "--cuda-version",
        dest="cuda_version",
        required=True,
        help=
        "If a valid version is specified, install the GPU version of AutoGluon with the specified version of CUDA."
    )


def _add_subparser_autogluon(subparsers):
    add_subparser(
        subparsers,
        "AutoGluon",
        func=autogluon,
        aliases=[],
        add_argument=_autogluon_args,
    )


def tensorflow(**kwargs):
    """Install the Python package TensorFlow.
    Since the most common to use TensorFlow is to install it into a Docker image 
    that already come with Nvidia CUDA support, 
    GPU support/dependencies (CUDA and CuDNN) is not handled here.
    You need to manually install CUDA and CuDNN if you need GPU support.
    For more details,
    please refer to https://www.tensorflow.org/install/gpu.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install tensorflow"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass


def _add_subparser_tensorflow(subparsers):
    add_subparser(
        subparsers,
        "tensorflow",
        func=tensorflow,
        aliases=["tf"],
    )


def gensim(**kwargs):
    """Insert the Python package GenSim.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install gensim"
        if args.cuda_version:
            pass
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass


def _add_subparser_gensim(subparsers):
    add_subparser(
        subparsers,
        "gensim",
        func=gensim,
    )


def pytext(**kwargs):
    """Insert the Python package PyText.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install pytext-nlp"
        if args.cuda_version:
            pass
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass


def _add_subparser_pytext(subparsers):
    add_subparser(
        subparsers,
        "pytext",
        func=pytext,
    )


def computer_vision(**kwargs):
    """Insert computer vision Python packages: opencv-python, scikit-image and Pillow.
    """
    args = namespace(kwargs)
    if args.install:
        if is_linux():
            cmd = f"""apt-get install {args._yes_s} libsm6 libxrender-dev \
                    && {args.pip} install opencv-python scikit-image pillow"""
            run_cmd(cmd)
        elif is_macos():
            cmd = f"{args.pip} install opencv-python scikit-image pillow"
            run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass


def _add_subparser_computer_vision(subparsers):
    add_subparser(
        subparsers,
        "computer_vision",
        func=computer_vision,
        aliases=["vision", "cv"],
    )


def nlp(**kwargs):
    """Install Python packages (PyTorch, transformers, pytext-nlp and fasttext) for NLP.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"{args.pip} install torch torchvision transformers pytext-nlp fasttext"
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass


def _add_subparser_nlp(subparsers):
    add_subparser(
        subparsers,
        "nlp",
        func=nlp,
    )
