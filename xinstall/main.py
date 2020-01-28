"""The command-line interface for xinstall.
"""
from argparse import ArgumentParser
from .utils import add_subparser
from .ai import add_subparser_kaggle, add_subparser_lightgbm, add_subparser_pytorch, add_subparser_autogluon
from .shell import add_subparser_change_shell, add_subparser_wajig, add_subparser_homebrew
from .ide import add_subparser_neovim, add_subparser_spacevim
from .github import add_subparser_install_py_github, add_subparser_xinstall, add_subparser_dsutil, add_subparser_pybay
from .dev import _add_subparser_git, _add_subparser_git_ignore, _add_subparser_poetry, _add_subparser_spark
from .jupyter import _add_subparser_almond
from .misc import _add_subparser_nomachine
__version__ = "0.3.8"


def version(**kwargs):
    """Print the version of xinstall.
    """
    print(__version__)


def _add_subparser_version(subparsers):
    subparser = subparsers.add_parser(
        "version",
        aliases=["ver", "v"],
        help="Print version of the xinstall package."
    )
    subparser.set_defaults(func=version)
    return subparser


def parse_args(args=None, namespace=None):
    """Parse command-line arguments for the install/configuration util.
    """
    parser = ArgumentParser(
        description="Easy installation and configuration for Unix/Linux"
    )
    parser.add_argument(
        "-s",
        "--sudo",
        dest="sudo",
        action="store_true",
        help="Run commands using sudo."
    )
    parser.add_argument(
        "-y",
        "--yes",
        dest="yes",
        action="store_true",
        help="Automatical yes (default no) to prompt questions."
    )
    subparsers = parser.add_subparsers(dest="sub_cmd", help="Sub commands.")
    # ------------------------ command-line tools ----------------------------
    add_subparser(subparsers, "CoreUtils", aliases=["cu"])
    add_subparser_change_shell(subparsers)
    add_subparser(
        subparsers, "Shell utils", aliases=["sh_utils", "shutils", "shu", "su"]
    )
    add_subparser(subparsers, "Bash-it", aliases=["shit", "bit"])
    add_subparser(subparsers, "xonsh")
    add_subparser_homebrew(subparsers)
    add_subparser(subparsers, "Hyper", aliases=["hp"])
    add_subparser(subparsers, "OpenInTerminal", aliases=["oit"])
    add_subparser(
        subparsers, "Bash completion", aliases=["completion", "comp", "cp"]
    )
    add_subparser_wajig(subparsers)
    add_subparser(subparsers, "exa")
    add_subparser(subparsers, "osquery", aliases=["osq"])
    # ------------------------ Vim & Other IDEs ----------------------
    add_subparser(subparsers, "Vim")
    add_subparser_neovim(subparsers)
    add_subparser_spacevim(subparsers)
    add_subparser(subparsers, "IdeaVim", aliases=["ivim"])
    add_subparser(subparsers, "Visual Studio Code", aliases=["vscode", "code"])
    add_subparser(subparsers, "IntelliJ IDEA", aliases=["intellij", "idea"])
    add_subparser(subparsers, "Bash LSP", aliases=["blsp"])
    # ------------------------- development related  ------------------------------
    _add_subparser_git(subparsers)
    _add_subparser_git_ignore(subparsers)
    add_subparser(subparsers, "NodeJS", aliases=["node"])
    add_subparser(subparsers, "rust")
    add_subparser(subparsers, "evcxr_jupyter", aliases=["evcxr"])
    add_subparser(subparsers, "Python3", aliases=["py3"])
    add_subparser(subparsers, "pyjnius", aliases=["pyj"])
    add_subparser(subparsers, "IPython", aliases=["ipy"])
    add_subparser(subparsers, "yapf", aliases=[])
    add_subparser_dsutil(subparsers)
    add_subparser_xinstall(subparsers)
    add_subparser_kaggle(subparsers)
    add_subparser_pybay(subparsers)
    add_subparser_lightgbm(subparsers)
    add_subparser_pytorch(subparsers)
    add_subparser_autogluon(subparsers)
    add_subparser(subparsers, "OpenJDK8", aliases=["jdk8"])
    add_subparser(subparsers, "sdkman", aliases=[])
    _add_subparser_poetry(subparsers)
    add_subparser(subparsers, "Cargo", aliases=["cgo"])
    add_subparser(subparsers, "ANTLR")
    add_subparser(subparsers, "Docker", aliases=["dock", "dk"])
    _add_subparser_spark(subparsers)
    add_subparser(subparsers, "PySpark")
    add_subparser(subparsers, "Kubernetes", aliases=["k8s"])
    add_subparser(subparsers, "Minikube", aliases=["mkb"])
    # ------------------------- web related ------------------------------
    add_subparser(subparsers, "SSH server", aliases=["sshs"])
    add_subparser(subparsers, "SSH client", aliases=["sshc"])
    add_subparser(subparsers, "blogging", aliases=["blog"])
    add_subparser(subparsers, "ProxyChains", aliases=["pchains", "pc"])
    add_subparser(subparsers, "dryscrape", aliases=[])
    add_subparser(subparsers, "download tools", aliases=["dl", "dlt"])
    add_subparser_install_py_github(subparsers)
    _add_subparser_git_ignore(subparsers)
    _add_subparser_version(subparsers)
    # ------------------------- JupyterLab related ------------------------------
    add_subparser(subparsers, "BeakerX", aliases=["bkx", "bk"])
    add_subparser(
        subparsers, "jupyterlab-lsp", aliases=["jlab-lsp", "jlab_lsp"]
    )
    _add_subparser_almond(subparsers)
    add_subparser(subparsers, "iTypeScript", aliases=["its"])
    add_subparser(subparsers, "nbdime", aliases=["nbd"])
    # ------------------------- misc applications ------------------------------
    _add_subparser_nomachine(subparsers)
    add_subparser(subparsers, "VirtualBox", aliases=["vbox"])
    # --------------------------------------------------------
    return parser.parse_args(args=args, namespace=namespace)


def main():
    """Run xinstall command-line interface.
    """
    args = parse_args()
    args.func(**vars(args))


if __name__ == "__main__":
    main()
