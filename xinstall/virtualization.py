"""Install virtualization related applications.
"""
import logging
from .utils import (
    USER,
    run_cmd,
    add_subparser,
    is_macos,
    is_centos_series,
    is_ubuntu_debian,
    is_win,
    update_apt_source,
    brew_install_safe,
)


def virtualbox(args) -> None:
    """Install VirtualBox.
    """
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(prefix=args.prefix)
            run_cmd(f"{args.prefix} apt-get install {args.yes_s} virtualbox-qt", )
        elif is_macos():
            run_cmd("brew cask install virtualbox virtualbox-extension-pack")
        elif is_centos_series():
            pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} virtualbox-qt", )
        elif is_macos():
            run_cmd("brew cask uninstall virtualbox virtualbox-extension-pack", )
        elif is_centos_series():
            pass
    if args.config:
        pass


def _add_subparser_virtualbox(subparsers):
    add_subparser(subparsers, "VirtualBox", func=virtualbox, aliases=["vbox"])


def docker(args):
    """Install and configure Docker container.
    """
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(prefix=args.prefix)
            run_cmd(
                f"{args.prefix} apt-get install {args.yes_s} docker.io docker-compose"
            )
        elif is_macos():
            brew_install_safe([
                "docker",
                "docker-compose",
                "bash-completion@2",
            ])
        elif is_centos_series():
            run_cmd(f"{args.prefix} yum install docker docker-compose")
    if args.config:
        if args.user_to_docker:
            if is_ubuntu_debian():
                run_cmd(f"{args.prefix} gpasswd -a {args.user_to_docker} docker")
                logging.warning(
                    "Please run the command 'newgrp docker' or logout/login"
                    " to make the group 'docker' effective!"
                )
            elif is_macos():
                cmd = f"{args.prefix} dseditgroup -o edit -a {args.user_to_docker} -t user staff"
                run_cmd(cmd)
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} docker docker-compose", )
        elif is_macos():
            run_cmd(
                "brew uninstall docker docker-completion docker-compose docker-compose-completion",
            )
        elif is_centos_series():
            run_cmd(f"{args.prefix} yum remove docker docker-compose")


def _docker_args(subparser):
    subparser.add_argument(
        "--user-to-docker",
        dest="user_to_docker",
        default="" if USER == "root" else USER,
        help="The user to add to the docker group.",
    )


def _add_subparser_docker(subparsers):
    add_subparser(
        subparsers,
        "Docker",
        func=docker,
        add_argument=_docker_args,
        aliases=["dock", "dk"]
    )


def kubernetes(args):
    """Install and configure kubernetes command-line interface.
    """
    if args.install:
        if is_ubuntu_debian():
            run_cmd(
                f"""curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg \
                    | {args.prefix} apt-key add -""",
            )
            run_cmd(
                f'''echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" \
                    | {args.prefix} tee -a /etc/apt/sources.list.d/kubernetes.list''',
            )
            update_apt_source(prefix=args.prefix, seconds=-1E10)
            run_cmd(f"{args.prefix} apt-get install {args.yes_s} kubectl")
        elif is_macos():
            brew_install_safe(["kubernetes-cli"])
        elif is_centos_series():
            pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} kubectl")
        elif is_macos():
            run_cmd("brew uninstall kubectl")
        elif is_centos_series():
            pass


def _add_subparser_kubernetes(subparsers):
    add_subparser(subparsers, "Kubernetes", func=kubernetes, aliases=["k8s"])


def _minikube_linux(args):
    url = "https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64"
    run_cmd(
        f"""curl -L {url} -o /tmp/minikube-linux-amd64 \
            && {args.prefix} apt-get install {args.yes_s} \
                /tmp/minikube-linux-amd64 /usr/local/bin/minikube""",
    )
    print("VT-x/AMD-v virtualization must be enabled in BIOS.")


def minikube(args) -> None:
    """Install MiniKube.
    """
    virtualbox(args)
    kubernetes(args)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(prefix=args.prefix, seconds=-1E10)
            _minikube_linux(args)
        elif is_macos():
            run_cmd("brew install minikube")
        elif is_centos_series():
            _minikube_linux(args)
        elif is_win():
            run_cmd("choco install minikube")
            print("VT-x/AMD-v virtualization must be enabled in BIOS.")
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"{args.prefix} rm /usr/local/bin/minikube")
        elif is_macos():
            run_cmd("brew cask uninstall minikube")
        elif is_centos_series():
            run_cmd(f"{args.prefix} rm /usr/local/bin/minikube")


def _add_subparser_minikube(subparsers):
    add_subparser(subparsers, "Minikube", func=minikube, aliases=["mkb"])


def multipass(args) -> None:
    """Install Multipass.
    """
    if args.install:
        if is_ubuntu_debian():
            cmd = f"{args.prefix} snap install multipass --classic"
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
            cmd = f"{args.prefix} snap uninstall multipass"
            run_cmd(cmd)
        elif is_macos():
            run_cmd("brew cask uninstall multipass")
        elif is_centos_series():
            pass


def _add_subparser_multipass(subparsers):
    add_subparser(subparsers, "Multipass", func=multipass, aliases=["mp"])


def microk8s(args) -> None:
    """Install MicroK8S.
    """
    if args.install:
        if is_ubuntu_debian():
            cmd = f"""{args.prefix} snap install microk8s --classic \
                    && ln -svf /snap/bin/microk8s.kubectl /snap/bin/kubectl \
                    && gpasswd -a $(id -un) microk8s"""
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
            cmd = f"{args.prefix} snap uninstall microk8s"
            run_cmd(cmd)
        elif is_macos():
            pass
        elif is_centos_series():
            pass


def _add_subparser_microk8s(subparsers):
    add_subparser(subparsers, "Microk8s", func=microk8s, aliases=["mk8s"])
