"""Install and configure Jupyter/Lab related tools.
"""
from pathlib import Path
import logging
import shutil
from .utils import (
    USER,
    HOME,
    BIN_DIR,
    BASE_DIR,
    run_cmd,
    add_subparser,
    option_pip_bundle,
)
from .dev import rustup, cmake


def _add_subparser_jupyter(subparsers):
    _add_subparser_jupyterlab_lsp(subparsers)
    _add_subparser_itypescript(subparsers)
    _add_subparser_nbdime(subparsers)
    _add_subparser_almond(subparsers)
    _add_subparser_evcxr_jupyter(subparsers)
    _add_subparser_jupyter_book(subparsers)
    _add_subparser_jupyterlab_vim(subparsers)
    _add_subparser_jupyterlab(subparsers)


def nbdime(args) -> None:
    """Install and configure nbdime for comparing difference of notebooks.
    """
    if args.install:
        run_cmd(f"{args.pip_install} nbdime")
    if args.uninstall:
        run_cmd(f"{args.pip_uninstall} nbdime")
    if args.config:
        run_cmd("nbdime config-git --enable --global")


def _nbdime_args(subparser) -> None:
    option_pip_bundle(subparser)


def _add_subparser_nbdime(subparsers) -> None:
    add_subparser(
        subparsers, "nbdime", func=nbdime, aliases=["nbd"], add_argument=_nbdime_args
    )


def itypescript(args) -> None:
    """Install and configure the ITypeScript kernel.
    """
    if args.install:
        run_cmd(f"{args.prefix} npm install -g --unsafe-perm itypescript")
        run_cmd(f"{args.prefix} its --ts-hide-undefined --install=global")
    if args.uninstall:
        run_cmd(f"{args.prefix} jupyter kernelspec uninstall typescript")
        run_cmd(f"{args.prefix} npm uninstall itypescript")
    if args.config:
        pass


def _add_subparser_itypescript(subparsers) -> None:
    add_subparser(subparsers, "iTypeScript", func=itypescript, aliases=["its"])


def jupyterlab_lsp(args) -> None:
    """Install jupyterlab-lsp.
    """
    if args.install:
        cmd = f"""{args.pip_install} jupyter-lsp python-language-server[all] pyls-mypy \
                && {args.prefix} {args.jupyter} labextension install @krassowski/jupyterlab-lsp
                """
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass


def _jupyterlab_lsp_args(subparser) -> None:
    option_pip_bundle(subparser)


def _add_subparser_jupyterlab_lsp(subparsers) -> None:
    add_subparser(
        subparsers,
        "jupyterlab-lsp",
        func=jupyterlab_lsp,
        aliases=["jlab-lsp", "jlab_lsp"],
        add_argument=_jupyterlab_lsp_args,
    )
    

def almond(args) -> None:
    """Install/uninstall/configure the Almond Scala kernel.
    """
    if args.almond_version:
        args.install = True
        if not args.almond_version.startswith(":"):
            args.almond_version = ":" + args.almond_version
    if args.scala_version:
        args.install = True
        args.scala_version = f"--scala {args.scala_version}"
    if args.install:
        coursier = BIN_DIR / "coursier"
        run_cmd(
            f"curl -L -o {coursier} https://git.io/coursier-cli && chmod +x {coursier}"
        )
        run_cmd(
            f"""{args.prefix} /usr/local/bin/coursier launch \
                almond{args.almond_version} {args.scala_version} \
                --quiet -- --install --global"""
        )
    if args.config:
        pass


def _almond_args(subparser) -> None:
    subparser.add_argument(
        "-a",
        "--almond-version",
        dest="almond_version",
        default="",
        help="The version (the latest supported by default) of Almond to install."
    )
    subparser.add_argument(
        "-s",
        "--scala-version",
        dest="scala_version",
        default="",
        help="The version (the latest supported by default) of Scala to install."
    )


def _add_subparser_almond(subparsers) -> None:
    add_subparser(
        subparsers,
        "Almond",
        func=almond,
        aliases=["al", "amd"],
        add_argument=_almond_args
    )


def evcxr_jupyter(args) -> None:
    """Install the evcxr Rust kernel for Jupyter/Lab server.
    """
    cargo = HOME / ".cargo/bin/cargo"
    evcxr_jupyter = HOME / ".cargo/bin/evcxr_jupyter"
    if args.install:
        rustup(args)
        cmake(args)
        cmd = f"""{cargo} install --force evcxr_jupyter \
            && {evcxr_jupyter} --install"""
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = f"""{evcxr_jupyter} --uninstall \
            && {cargo} uninstall evcxr_jupyter
            """
        run_cmd(cmd)


def _evcxr_jupyter_args(subparser) -> None:
    subparser.add_argument(
        "--link-to-dir",
        dest="link_to_dir",
        default="/usr/local/bin",
        help=
        "The directory (default /usr/local/bin) to link commands (cargo and rustc) to."
    )


def _add_subparser_evcxr_jupyter(subparsers) -> None:
    add_subparser(
        subparsers,
        "evcxr_jupyter",
        func=evcxr_jupyter,
        aliases=["evcxr"],
        add_argument=_evcxr_jupyter_args
    )


def jupyter_book(args):
    """Install jupyter-book.
    """
    if args.install:
        cmd = f"{args.pip_install} jupyter-book"
        run_cmd(cmd)
    if args.config:
        src_file = BASE_DIR / "jupyter-book/_config.yml"
        shutil.copy2(src_file, ".")
        logging.info("%s is copied to the current directory.", src_file)
    if args.uninstall:
        pass


def _jupyter_book_args(subparser):
    option_pip_bundle(subparser)


def _add_subparser_jupyter_book(subparsers):
    add_subparser(
        subparsers,
        "jupyter_book",
        func=jupyter_book,
        aliases=["jb", "jbook"],
        add_argument=_jupyter_book_args,
    )


def jupyterlab(args):
    """Install the JupyterLab.
    """
    if args.install:
        cmd = f"""{args.prefix} {args.pip_install} nbdime "nbconvert==5.6.1" "jupyterlab>=2.1.0,<3.2.0" \
                jupyterlab_widgets ipywidgets \
                jupyterlab_vim \
                jupyterlab-lsp python-language-server[all] \
                jupyter-resource-usage \
            && jupyter labextension disable @axlair/jupyterlab_vim
            """
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = f"""{args.prefix} {args.pip_uninstall} nbdime nbconvert jupyterlab \
                jupyterlab_widgets ipywidgets \
                jupyterlab_vim \
                jupyterlab-lsp python-language-server[all] \
                jupyter-resource-usage
            """
        run_cmd(cmd)


def _jupyterlab_args(subparser):
    option_pip_bundle(subparser)


def _add_subparser_jupyterlab(subparsers):
    add_subparser(
        subparsers,
        "jupyterlab",
        func=jupyterlab,
        aliases=["jlab", "jupyter"],
        add_argument=_jupyterlab_args,
    )
