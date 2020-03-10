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
    """Insert the Python package kaggle.
    """
    args = namespace(kwargs)
    if args.install:
        if is_linux():
            cmd = f"{args.pip} install torch==1.4.0+cpu torchvision==0.5.0+cpu -f https://download.pytorch.org/whl/torch_stable.html"
            if args.gpu:
                cmd = f"{args.pip} install torch torchvision"
            run_cmd(cmd)
        elif is_macos():
            cmd = f"{args.pip} install torch torchvision"
            if args.gpu:
                warnings.warn("Ignore the option '--gpu' as CUDA version of PyTorch is not supported on macOS.")
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


def _add_subparser_pytorch(subparsers):
    add_subparser(
        subparsers,
        "PyTorch",
        func=pytorch,
        aliases=[],
        add_argument=_pytorch_args
    )


def autogluon(**kwargs):
    """Insert the Python package kaggle.
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
        add_argument=_autogluon_args
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


def opencv_python(**kwargs):
    """Insert the Python package opencv-python.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"""{args.sudo_s} apt-get install libsm6 libxrender-dev \
                && {args.pip} install opencv-python"""
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass


def _add_subparser_opencv_python(subparsers):
    add_subparser(
        subparsers,
        "opencv_python",
        func=opencv_python,
        aliases=["opencv", "cv2"],
    )
