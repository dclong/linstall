"""Install AI related tools.
"""
from pathlib import Path
import logging
from .utils import (
    HOME, USER, run_cmd, add_subparser, is_linux, is_macos, option_pip_bundle
)


def kaggle(args):
    """Insert the Python package kaggle.
    """
    if args.install:
        cmd = f"{args.pip} install {args.user_s} {args.pip_option} kaggle"
        run_cmd(cmd)
    if args.config:
        home_host = Path(f"/home_host/{USER}/")
        kaggle_home_host = home_host / ".kaggele"
        kaggle_home = HOME / ".kaggele"
        if home_host.is_dir():
            kaggle_home_host.mkdir(exist_ok=True)
            try:
                kaggle_home.symlink_to(kaggle_home_host)
                logging.info(
                    "Symbolic link %s pointing to %s is created.", kaggle_home,
                    kaggle_home_host
                )
            except FileExistsError:
                pass
        else:
            kaggle_home.mkdir(exist_ok=True)
            logging.info("The directory %s is created.", kaggle_home)
    if args.uninstall:
        pass


def _kaggle_args(subparser):
    option_pip_bundle(subparser)


def _add_subparser_kaggle(subparsers):
    add_subparser(
        subparsers, "kaggle", func=kaggle, aliases=[], add_argument=_kaggle_args
    )


def lightgbm(args):
    """Insert the Python package kaggle.
    """
    if args.install:
        cmd = f"""{args.pip} install {args.user_s} {args.pip_option} \
            lightgbm scikit-learn pandas matplotlib scipy graphviz"""
        run_cmd(cmd)


def _lightgbm_args(subparser):
    option_pip_bundle(subparser)


def _add_subparser_lightgbm(subparsers):
    add_subparser(
        subparsers, "lightgbm", func=lightgbm, aliases=[], add_argument=_lightgbm_args
    )


def pytorch(args):
    """Insert PyTorch.
    """
    if args.install:
        url = "https://download.pytorch.org/whl/torch_stable.html"
        if is_linux():
            cmd = f"""{args.pip_install} -f {url} \
                    torch==1.7.0+cpu torchvision==0.8.1+cpu torchaudio==0.7.0"""
            if args.cuda:
                args.cuda = args.cuda.replace(".", "")
                cmd = f"""{args.pip_install} -f {url} \
                    torch==1.7.0+cu{args.cuda} torchvision==0.8.1+cu{args.cuda} \
                    torchaudio==0.7.0
                    """
                if args.cuda == "102":
                    cmd = f"{args.pip} install torch torchvision"
            run_cmd(cmd)
        elif is_macos():
            cmd = f"{args.pip} install torch torchvision torchaudio"
            run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass


def _pytorch_args(subparser):
    subparser.add_argument(
        "--cuda",
        dest="cuda",
        default="",
        help="The version of CUDA. If not specified, the CPU version is used."
    )
    option_pip_bundle(subparser)


def _add_subparser_pytorch(subparsers):
    add_subparser(
        subparsers, "PyTorch", func=pytorch, aliases=[], add_argument=_pytorch_args
    )


def autogluon(args):
    """Insert the Python package AutoGluon.
    """
    if args.install:
        cmd = f"{args.pip} install {args.user_s} {args.pip_option} 'mxnet<2.0.0' autogluon"
        if args.cuda_version:
            version = args.cuda_version.replace(".", "")
            cmd = f"{args.pip} install {args.user_s} {args.pip_option} 'mxnet-cu{version}<2.0.0' autogluon"
        run_cmd(cmd)


def _autogluon_args(subparser):
    subparser.add_argument(
        "--cuda",
        "--cuda-version",
        dest="cuda_version",
        required=True,
        help="If a valid version is specified, "
        "install the GPU version of AutoGluon with the specified version of CUDA."
    )
    option_pip_bundle(subparser)


def _add_subparser_autogluon(subparsers):
    add_subparser(
        subparsers,
        "AutoGluon",
        func=autogluon,
        aliases=[],
        add_argument=_autogluon_args,
    )


def pytext(args):
    """Insert the Python package PyText.
    """
    if args.install:
        cmd = f"{args.pip} install {args.user_s} {args.pip_option} pytext-nlp"
        if args.cuda_version:
            pass
        run_cmd(cmd)


def _pytext_args(subparser):
    option_pip_bundle(subparser)


def _add_subparser_pytext(subparsers):
    add_subparser(subparsers, "pytext", func=pytext, add_argument=_pytext_args)


def computer_vision(args):
    """Insert computer vision Python packages: opencv-python, scikit-image and Pillow.
    """
    if args.install:
        if is_linux():
            cmd = f"""{args.prefix} apt-get install {args.yes_s} \
                        libsm6 libxrender-dev libaec-dev \
                        libblosc-dev libbrotli-dev libghc-bzlib-dev libgif-dev \
                        libopenjp2-7-dev liblcms2-dev libjxr-dev liblz4-dev \
                        liblzma-dev libpng-dev libsnappy-dev libtiff-dev \
                        libwebp-dev libzopfli-dev libzstd-dev \
                    && {args.pip} install opencv-python scikit-image pillow"""
            run_cmd(cmd)
        elif is_macos():
            cmd = f"""{args.pip} install {args.user_s} {args.pip_option} \
                opencv-python scikit-image pillow"""
            run_cmd(cmd)


def _computer_vision_args(subparser):
    option_pip_bundle(subparser)


def _add_subparser_computer_vision(subparsers):
    add_subparser(
        subparsers,
        "computer_vision",
        func=computer_vision,
        aliases=["vision", "cv"],
        add_argument=_computer_vision_args
    )


def nlp(args):
    """Install Python packages (PyTorch, transformers, pytext-nlp and fasttext) for NLP.
    """
    if args.install:
        cmd = f"""{args.pip} install {args.user_s} {args.pip_option} \
            torch torchvision transformers pytext-nlp fasttext"""
        run_cmd(cmd)


def _nlp_args(subparser):
    option_pip_bundle(subparser)


def _add_subparser_nlp(subparsers):
    add_subparser(subparsers, "nlp", func=nlp, add_argument=_nlp_args)


def _add_subparser_ai(subparsers):
    _add_subparser_kaggle(subparsers)
    _add_subparser_lightgbm(subparsers)
    _add_subparser_pytorch(subparsers)
    _add_subparser_autogluon(subparsers)
    _add_subparser_pytext(subparsers)
    _add_subparser_computer_vision(subparsers)
    _add_subparser_nlp(subparsers)
