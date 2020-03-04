import logging
from .utils import (
    HOME,
    run_cmd,
    namespace,
    add_subparser,
    is_macos,
    is_centos_series,
    is_ubuntu_debian,
    is_win,
    update_apt_source,
    brew_install_safe,
)


def virtualbox(**kwargs):
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(
                f"{args.sudo_s} apt-get install {args._yes_s} virtualbox-qt",
            )
        elif is_macos():
            run_cmd(f"brew cask install virtualbox virtualbox-extension-pack")
        elif is_centos_series():
            pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f"{args.sudo_s} apt-get purge {args._yes_s} virtualbox-qt",
            )
        elif is_macos():
            run_cmd(
                f"brew cask uninstall virtualbox virtualbox-extension-pack",
            )
        elif is_centos_series():
            pass
    if args.config:
        pass


def _add_subparser_virtualbox(subparsers):
    add_subparser(subparsers, "VirtualBox", func=virtualbox, aliases=["vbox"])


def docker(**kwargs):
    """Install and configure Docker container.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(
                f"{args.sudo_s} apt-get install {args._yes_s} docker.io docker-compose",
            )
        elif is_macos():
            brew_install_safe(
                [
                    "docker", "docker-compose", "bash-completion@2",
                    "docker-completion", "docker-compose-completion"
                ]
            )
        elif is_centos_series():
            run_cmd(f"{args.sudo_s} yum install docker docker-compose")
    if args.config:
        run_cmd("gpasswd -a $(id -un) docker")
        logging.warning(
            'Please logout and then login to make the group "docker" effective!'
        )
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f"{args.sudo_s} apt-get purge {args._yes_s} docker docker-compose",
            )
        elif is_macos():
            run_cmd(
                f"brew uninstall docker docker-completion docker-compose docker-compose-completion",
            )
        elif is_centos_series():
            run_cmd(f"{args.sudo_s} yum remove docker docker-compose")


def _add_subparser_docker(subparsers):
    add_subparser(subparsers, "Docker", func=docker, aliases=["dock", "dk"])


def kubernetes(**kwargs):
    """Install and configure kubernetes command-line interface.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            run_cmd(
                f"curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | {args.sudo_s} apt-key add -",
            )
            run_cmd(
                f'echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | {args.sudo_s} tee -a /etc/apt/sources.list.d/kubernetes.list',
            )
            update_apt_source(seconds=-1E10)
            run_cmd(f"{args.sudo_s} apt-get install {args._yes_s} kubectl")
        elif is_macos():
            brew_install_safe(["kubernetes-cli"])
        elif is_centos_series():
            pass
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"{args.sudo_s} apt-get purge {args._yes_s} kubectl")
        elif is_macos():
            run_cmd(f"brew uninstall kubectl")
        elif is_centos_series():
            pass


def _add_subparser_kubernetes(subparsers):
    add_subparser(subparsers, "Kubernetes", func=kubernetes, aliases=["k8s"])


def _minikube_linux(sudo: bool, yes: bool = True):
    run_cmd(
        f"""curl -L https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 -o /tmp/minikube-linux-amd64 \
            && {"sudo" if sudo else ""} apt-get install {yes} /tmp/minikube-linux-amd64 /usr/local/bin/minikube""",
    )
    print("VT-x/AMD-v virtualization must be enabled in BIOS.")


def minikube(**kwargs):
    args = namespace(kwargs)
    virtualbox(**kwargs)
    kubernetes(**kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(seconds=-1E10)
            _minikube_linux(sudo=args.sudo, yes=args.yes)
        elif is_macos():
            run_cmd(f"brew install minikube")
        elif is_centos_series():
            _minikube_linux(sudo=args.sudo, yes=args.yes)
        elif is_win():
            run_cmd(f"choco install minikube")
            print("VT-x/AMD-v virtualization must be enabled in BIOS.")
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"{args.sudo_s} rm /usr/local/bin/minikube")
        elif is_macos():
            run_cmd(f"brew cask uninstall minikube")
        elif is_centos_series():
            run_cmd(f"{args.sudo_s} rm /usr/local/bin/minikube")


def _add_subparser_minikube(subparsers):
    add_subparser(subparsers, "Minikube", func=minikube, aliases=["mkb"])


def multipass(**kwargs):
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            cmd = f"{args.sudo_s} snap install multipass --classic"
            run_cmd(cmd)
        elif is_macos():
            cmd = "brew cask install multipass"
            run_cmd(cmd)
        elif is_centos_series():
            pass
        elif is_win():
            pass
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            cmd = f"{args.sudo_s} snap uninstall multipass"
            run_cmd(cmd)
        elif is_macos():
            run_cmd(f"brew cask uninstall multipass")
        elif is_centos_series():
            pass


def _add_subparser_multipass(subparsers):
    add_subparser(subparsers, "Multipass", func=multipass, aliases=["mp"])


def microk8s(**kwargs):
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            cmd = f"""{args.sudo_s} snap install microk8s --classic \
                    && {args.sudo_s} gpasswd -a $(id -un) microk8s"""
            run_cmd(cmd)
        elif is_macos():
            pass
        elif is_centos_series():
            pass
        elif is_win():
            pass
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            cmd = f"{args.sudo_s} snap uninstall microk8s"
            run_cmd(cmd)
        elif is_macos():
            pass
        elif is_centos_series():
            pass


def _add_subparser_microk8s(subparsers):
    add_subparser(subparsers, "Microk8s", func=microk8s, aliases=["mk8s"])
