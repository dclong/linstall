#!/usr/bin/env python3
"""Easy installation and configuration of Linux/Mac/Windows apps.
"""
import os
import logging
import shutil
from pathlib import Path
from .utils import (
    HOME, USER, GROUP, BASE_DIR, BIN_DIR, run_cmd, add_subparser, update_apt_source,
    brew_install_safe, is_ubuntu_debian, is_macos, is_centos_series, namespace,
    option_pip
)
logging.basicConfig(
    format=
    "%(asctime)s | %(module)s.%(funcName)s: %(lineno)s | %(levelname)s: %(message)s",
    level=logging.INFO
)


def ssh_server(**kwargs) -> None:
    """Install and configure SSH server.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(prefix=args.prefix)
            run_cmd(
                f"{args.prefix} apt-get install {args.yes_s} openssh-server fail2ban"
            )
        elif is_macos():
            pass
        elif is_centos_series():
            pass
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} openssh-server fail2ban")
        elif is_macos():
            pass
        elif is_centos_series():
            pass


def _add_subparser_ssh_server(subparsers):
    add_subparser(subparsers, "SSH server", func=ssh_server, aliases=["sshs"])


def ssh_client(**kwargs) -> None:
    """Configure SSH client.
    :param kwargs: Keyword arguments.
    """
    args = namespace(kwargs)
    if args.config:
        ssh_src = Path(f"/home_host/{USER}/.ssh")
        ssh_dst = HOME / ".ssh"
        if ssh_src.is_dir():
            # inside a Docker container, use .ssh from host
            try:
                shutil.rmtree(ssh_dst)
            except FileNotFoundError:
                pass
            shutil.copytree(ssh_src, ssh_dst)
            logging.info("%s is copied to %s.", ssh_src, ssh_dst)
        ssh_dst.mkdir(exist_ok=True)
        src = BASE_DIR / "ssh/client/config"
        des = HOME / ".ssh/config"
        shutil.copy2(src, des)
        logging.info("%s is copied to %s.", ssh_src, ssh_dst)
        # file permissions
        cmd = f"{args.prefix} chown -R {USER}:{GROUP} {HOME}/.ssh && chmod 600 {HOME}/.ssh/*"
        run_cmd(cmd)
        logging.info("The permissions of ~/.ssh and its contents are corrected set.")


def _add_subparser_ssh_client(subparsers):
    add_subparser(subparsers, "SSH client", func=ssh_client, aliases=["sshc"])


def proxychains(**kwargs) -> None:
    """Install and configure ProxyChains.
    :param kwargs: Keyword arguments.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(prefix=args.prefix)
            cmd = f"""{args.prefix} apt-get install {args.yes_s} proxychains4 \
                    && {args.prefix} ln -svf /usr/bin/proxychains4 /usr/bin/proxychains"""
            run_cmd(cmd)
        elif is_macos():
            brew_install_safe(["proxychains-ng"])
        elif is_centos_series():
            run_cmd(f"{args.prefix} yum install proxychains")
    if args.config:
        print("Configuring proxychains ...")
        src_file = BASE_DIR / "proxychains/proxychains.conf"
        des_dir = os.path.join(HOME, ".proxychains")
        os.makedirs(des_dir, exist_ok=True)
        shutil.copy2(src_file, des_dir)
        logging.info("%s is copied to the directory %s.", src_file, des_dir)
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} proxychains4")
        elif is_macos():
            run_cmd("brew uninstall proxychains-ng")
        elif is_centos_series():
            run_cmd(f"{args.prefix} yum remove proxychains")


def _add_subparser_proxychains(subparsers):
    add_subparser(
        subparsers, "ProxyChains", func=proxychains, aliases=["pchains", "pc"]
    )


def dryscrape(**kwargs):
    """Install and configure dryscrape.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(prefix=args.prefix)
            cmd = f"""{args.pefix} apt-get install {args.yes_s} qt5-default libqt5webkit5-dev build-essential xvfb \
                && {args.pip} install --user dryscrape
                """
            run_cmd(cmd)
        elif is_macos():
            pass
        elif is_centos_series():
            pass
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            pass
        elif is_macos():
            pass
        elif is_centos_series():
            pass


def _add_subparser_dryscrape(subparsers):
    add_subparser(subparsers, "dryscrape", func=dryscrape, aliases=[])


def download_tools(**kwargs):
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(prefix=args.prefix)
            run_cmd(f"{args.prefix} apt-get install {args.yes_s} wget curl aria2", )
        elif is_macos():
            brew_install_safe(["wget", "curl", "aria2"])
        elif is_centos_series():
            pass
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f"{args.prefix} apt-get purge {args.yes_s} wget curl aria2")
        elif is_macos():
            run_cmd("brew uninstall wget curl aria2")
        elif is_centos_series():
            pass


def _add_subparser_download_tools(subparsers):
    add_subparser(
        subparsers, "download tools", func=download_tools, aliases=["dl", "dlt"]
    )
