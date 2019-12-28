"""The command-line interface for xinstall.
"""
from typing import Sequence, Union, Callable
from argparse import ArgumentParser
import re
from . import xinstall


def _wajig_args(subparser):
    subparser.add_argument(
        "-p",
        "--proxy",
        dest="proxy",
        default="",
        help="Configure apt to use the specified proxy."
    )


def _change_shell_args(subparser):
    subparser.add_argument(
        "-s",
        "--shell",
        dest="shell",
        default="/bin/bash",
        help="the shell to change to."
    )


def _homebrew_args(subparser):
    subparser.add_argument(
        "-d",
        "--install-deps",
        dest="dep",
        action="store_true",
        help="Whether to install dependencies."
    )


def _neovim_args(subparser):
    subparser.add_argument(
        "--ppa",
        dest="ppa",
        action="store_true",
        help="Install the latest version of NeoVim from PPA."
    )


def _spacevim_args(subparser):
    subparser.add_argument(
        "--enable-true-colors",
        dest="true_colors",
        action="store_true",
        default=None,
        help="enable true color (default true) for SpaceVim."
    )
    subparser.add_argument(
        "--disable-true-colors",
        dest="true_colors",
        action="store_false",
        help="disable true color (default true) for SpaceVim."
    )


def _git_args(subparser):
    subparser.add_argument(
        "-p",
        "--proxy",
        dest="proxy",
        default="",
        help="Configure Git to use the specified proxy."
    )


def _yapf_args(subparser):
    subparser.add_argument(
        "-d",
        "--dest-dir",
        dest="dst_dir",
        requested=True,
        help="The destination directory to copy the YAPF configuration file to."
    )


def _poetry_args(subparser):
    subparser.add_argument(
        "-b",
        "--bash-completion",
        dest="bash_completion",
        action="store_true",
        help="Configure Bash completion for poetry as well."
    )


def _almond_args(subparser):
    subparser.add_argument(
        "-a",
        "--almond-version",
        dest="almond_version",
        default=None,
        help="the version (0.4.0 by default) of Almond to install."
    )
    subparser.add_argument(
        "-s",
        "--scala-version",
        dest="scala_version",
        default=None,
        help="the version (2.12.8 by default) of Scala to install."
    )


def _option_sys(subparser):
    subparser.add_argument(
        "--sys",
        dest="sys",
        action="store_true",
        help=
        "Install the Python package to a system-wide location (default to install to user's local directory.)"
    )


def _option_python(subparser):
    subparser.add_argument(
        "--python",
        dest="python",
        default="python3",
        help=f"Path to the python3 command."
    )


def _option_ipython(subparser):
    subparser.add_argument(
        "--ipython",
        dest="ipython",
        default="ipython3",
        help=f"Path to the python3 command."
    )


def _option_pip(subparser):
    subparser.add_argument(
        "--pip",
        dest="pip",
        default="pip3",
        help=f"Path to the pip command."
    )


def _option_jupyter(subparser):
    subparser.add_argument(
        "--jupyter",
        dest="jupyter",
        default="jupyter",
        help=f"Path to the jupyter command."
    )

def _dsutil_args(subparser):
    _option_sys(subparser)


def _xinstall_args(subparser):
    _option_sys(subparser)


def _add_subparser_version(subparsers):
    subparser = subparsers.add_parser(
        "version",
        aliases=["ver", "v"],
        help="Print version of the xinstall package."
    )
    subparser.set_defaults(func=xinstall.version)
    return subparser


def _add_subparser_install_py_github(subparsers):
    subparser = subparsers.add_parser(
        "install_py_github",
        aliases=["inpygit", "pygit", "ipg"],
        help="Install the latest version of a Python package from GitHub."
    )
    subparser.add_argument(
        dest="url", help=f"The URL of the Python package's GitHub repository."
    )
    _option_sys(subparser)
    _option_python(subparser)
    _option_pip(subparser)
    subparser.set_defaults(func=xinstall.install_py_github)
    return subparser


def _add_subparser_git_ignore(subparsers):
    subparser = subparsers.add_parser(
        "git_ignore",
        aliases=["gig", "gignore"],
        help="Append patterns to ignore into .gitignore in the current directory."
    )
    subparser.add_argument(
        "-p",
        "--python-pattern",
        dest="python_pattern",
        action="store_true",
        help=f"Gitignore patterns for Python developing."
    )
    subparser.add_argument(
        "-j",
        "--java-pattern",
        dest="java_pattern",
        action="store_true",
        help=f"Gitignore patterns for Java developing."
    )
    subparser.set_defaults(func=xinstall.git_ignore)
    return subparser


def _spark_args(subparser):
    subparser.add_argument(
        "-m",
        "--mirror",
        dest="mirror",
        default="http://us.mirrors.quenda.co/apache/spark/",
        help=f"The mirror of Spark to use."
    )
    subparser.add_argument(
        "-v",
        "--version",
        dest="version",
        default="2.4.4",
        help=f"The version of Spark to install."
    )


def _add_subparser(
    subparsers,
    name: str,
    aliases: Sequence = (),
    func: Union[Callable, None] = None,
    help_: Union[str, None] = None,
    add_argument: Union[Callable, None] = None
):
    sub_cmd = re.sub(r"(\s+)|-", "_", name.lower())
    aliases = [alias for alias in aliases if alias != sub_cmd]
    func = func if func else eval(f"xinstall.{sub_cmd}")
    help_ = help_ if help_ else f"Install and configure {name}."
    subparser = subparsers.add_parser(sub_cmd, aliases=aliases, help=help_)
    subparser.add_argument(
        "-i",
        "--install",
        dest="install",
        action="store_true",
        help=f"install {name}."
    )
    subparser.add_argument(
        "-u",
        "--uninstall",
        dest="uninstall",
        action="store_true",
        help=f"uninstall {name}."
    )
    subparser.add_argument(
        "-c",
        "--configure",
        dest="config",
        action="store_true",
        help=f"configure {name}."
    )
    subparser.add_argument(
        "-l",
        "--log",
        dest="log",
        action="store_true",
        help=f"Print the command to run."
    )
    _option_python(subparser)
    _option_pip(subparser)
    if add_argument:
        add_argument(subparser)
    subparser.set_defaults(func=func)
    return subparser


def _nomachine_args(subparser):
    subparser.add_argument(
        "-v",
        "--version",
        dest="version",
        default="6.8.1_1",
        help="The version of NoMachine to install."
    )


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
    _add_subparser(subparsers, "CoreUtils", aliases=["cu"])
    _add_subparser(
        subparsers,
        "change shell",
        aliases=["chsh", "cs"],
        add_argument=_change_shell_args
    )
    _add_subparser(
        subparsers, "Shell utils", aliases=["sh_utils", "shutils", "shu", "su"]
    )
    _add_subparser(subparsers, "Bash-it", aliases=["shit", "bit"])
    _add_subparser(subparsers, "xonsh")
    _add_subparser(
        subparsers, "Homebrew", aliases=["brew"], add_argument=_homebrew_args
    )
    _add_subparser(subparsers, "Hyper", aliases=["hp"])
    _add_subparser(subparsers, "OpenInTerminal", aliases=["oit"])
    _add_subparser(
        subparsers, "Bash completion", aliases=["completion", "comp", "cp"]
    )
    _add_subparser(
        subparsers, "Wajig", aliases=["wj"], add_argument=_wajig_args
    )
    _add_subparser(subparsers, "exa")
    _add_subparser(subparsers, "osquery", aliases=["osq"])
    # ------------------------ Vim & Other IDEs ----------------------
    _add_subparser(subparsers, "Vim")
    _add_subparser(
        subparsers, "NeoVim", aliases=["nvim"], add_argument=_neovim_args
    )
    _add_subparser(
        subparsers, "SpaceVim", aliases=["svim"], add_argument=_spacevim_args
    )
    _add_subparser(subparsers, "IdeaVim", aliases=["ivim"])
    _add_subparser(subparsers, "Visual Studio Code", aliases=["vscode", "code"])
    _add_subparser(subparsers, "IntelliJ IDEA", aliases=["intellij", "idea"])
    _add_subparser(subparsers, "Bash LSP", aliases=["blsp"])
    # ------------------------- development related  ------------------------------
    _add_subparser(subparsers, "Git", add_argument=_git_args)
    _add_subparser(subparsers, "NodeJS", aliases=["node"])
    _add_subparser(subparsers, "rust")
    _add_subparser(subparsers, "evcxr_jupyter", aliases=["evcxr"])
    _add_subparser(subparsers, "Python3", aliases=["py3"])
    _add_subparser(subparsers, "pyjnius", aliases=["pyj"])
    _add_subparser(subparsers, "IPython3", aliases=["ipy3", "ipy"])
    _add_subparser(subparsers, "yapf", aliases=[])
    _add_subparser(subparsers, "dsutil", aliases=[], add_argument=_dsutil_args)
    _add_subparser(
        subparsers, "xinstall", aliases=[], add_argument=_xinstall_args
    )
    _add_subparser(subparsers, "kaggle", aliases=[])
    _add_subparser(subparsers, "OpenJDK8", aliases=["jdk8"])
    _add_subparser(subparsers, "sdkman", aliases=[])
    _add_subparser(
        subparsers, "Poetry", aliases=["pt"], add_argument=_poetry_args
    )
    _add_subparser(subparsers, "Cargo", aliases=["cgo"])
    _add_subparser(subparsers, "ANTLR")
    _add_subparser(subparsers, "Docker", aliases=["dock", "dk"])
    _add_subparser(subparsers, "Spark", add_argument=_spark_args)
    _add_subparser(subparsers, "PySpark")
    _add_subparser(subparsers, "Kubernetes", aliases=["k8s"])
    _add_subparser(subparsers, "Minikube", aliases=["mkb"])
    # ------------------------- web related ------------------------------
    _add_subparser(subparsers, "SSH server", aliases=["sshs"])
    _add_subparser(subparsers, "SSH client", aliases=["sshc"])
    _add_subparser(subparsers, "blogging", aliases=["blog"])
    _add_subparser(subparsers, "ProxyChains", aliases=["pchains", "pc"])
    _add_subparser(subparsers, "dryscrape", aliases=[])
    _add_subparser(subparsers, "download tools", aliases=["dl", "dlt"])
    _add_subparser_install_py_github(subparsers)
    _add_subparser_git_ignore(subparsers)
    _add_subparser_version(subparsers)
    # ------------------------- JupyterLab related ------------------------------
    _add_subparser(subparsers, "BeakerX", aliases=["bkx", "bk"])
    _add_subparser(
        subparsers, "jupyterlab-lsp", aliases=["jlab-lsp", "jlab_lsp"]
    )
    _add_subparser(
        subparsers, "Almond", aliases=["al", "amd"], add_argument=_almond_args
    )
    _add_subparser(subparsers, "iTypeScript", aliases=["its"])
    _add_subparser(subparsers, "nbdime", aliases=["nbd"])
    # ------------------------- misc applications ------------------------------
    _add_subparser(
        subparsers,
        "NoMachine",
        aliases=["nm", "nx"],
        add_argument=_nomachine_args
    )
    _add_subparser(subparsers, "VirtualBox", aliases=["vbox"])
    # --------------------------------------------------------
    return parser.parse_args(args=args, namespace=namespace)


def main():
    """Run xinstall command-line interface.
    """
    args = parse_args()
    args.func(**vars(args))


if __name__ == "__main__":
    main()
