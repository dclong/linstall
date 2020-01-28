
import tempfile
from pathlib import Path
from .utils import HOME, BASE_DIR, BIN_DIR, is_ubuntu_debian, is_centos_series, is_linux, is_fedora, update_apt_source, brew_install_safe, is_macos, run_cmd, namespace, add_subparser


def nomachine(**kwargs):
    """Install NoMachine.
    """
    args = namespace(kwargs)
    if args.install:
        ver = args.version[:args.version.rindex(".")]
        if is_ubuntu_debian():
            url = f"https://download.nomachine.com/download/{ver}/Linux/nomachine_{args.version}_amd64.deb"
            with tempfile.TemporaryDirectory() as tempdir:
                file = Path(tempdir) / "nomachine.deb"
                cmd = f"curl -sSL {url} -o {file} && dpkg -i {file}"
                run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass


def _nomachine_args(subparser):
    subparser.add_argument(
        "-v",
        "--version",
        dest="version",
        default="6.8.1_1",
        help="The version of NoMachine to install."
    )


def _add_subparser_nomachine(subparsers):
    add_subparser(
        subparsers,
        "NoMachine",
        aliases=["nm", "nx"],
        add_argument=_nomachine_args
    )


def virtualbox(**kwargs):
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(
                f'{args.sudo_s} apt-get install {args._yes_s} virtualbox-qt',
            )
        elif is_macos():
            run_cmd(f'brew cask install virtualbox virtualbox-extension-pack')
        elif is_centos_series():
            pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo_s} apt-get purge {args._yes_s} virtualbox-qt',
            )
        elif is_macos():
            run_cmd(
                f'brew cask uninstall virtualbox virtualbox-extension-pack',
            )
        elif is_centos_series():
            pass
    if args.config:
        pass

