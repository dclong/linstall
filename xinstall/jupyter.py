import os
from .utils import (
    USER, 
    HOME, 
    BASE_DIR, 
    BIN_DIR, 
    LOCAL_DIR, 
    USER_ID, 
    GROUP_ID, 
    is_ubuntu_debian, 
    is_centos_series, 
    is_linux, 
    is_fedora, 
    update_apt_source, 
    brew_install_safe, is_macos, run_cmd, namespace, add_subparser, intellij_idea_plugin
)


def nbdime(**kwargs):
    """Install and configure nbdime for comparing difference of notebooks.
    """
    args = namespace(kwargs)
    if args.install:
        run_cmd(f'{args.pip} install --user nbdime')
    if args.uninstall:
        run_cmd(f'{args.pip} uninstall nbdime')
    if args.config:
        run_cmd(f'nbdime config-git --enable --global')


def itypescript(**kwargs):
    """Install and configure the ITypeScript kernel.
    """
    args = namespace(kwargs)
    if args.install:
        run_cmd(f'{args.sudo_s} npm install -g --unsafe-perm itypescript')
        run_cmd(f'{args.sudo_s} its --ts-hide-undefined --install=global')
    if args.uninstall:
        run_cmd(f'{args.sudo_s} jupyter kernelspec uninstall typescript')
        run_cmd(f'{args.sudo_s} npm uninstall itypescript')
    if args.config:
        pass


def jupyterlab_lsp(**kwargs):
    args = namespace(kwargs)
    if args.install:
        cmd = '''{args.sudo_s} {args.pip} install --pre jupyter-lsp \
                && {args.sudo_s} {args.jupyter} labextension install @krassowski/jupyterlab-lsp \
                && {args.sudo_s} {args.pip} install python-language-server[all] pyls-mypy'''
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        pass


def beakerx(**kwargs):
    """Install/uninstall/configure the BeakerX kernels.
    """
    args = namespace(kwargs)
    if args.install:
        run_cmd(f'{args.pip} install --user beakerx')
        run_cmd(f'{args.sudo_s} beakerx install')
        run_cmd(
            f'{args.sudo_s} jupyter labextension install @jupyter-widgets/jupyterlab-manager',
        )
        run_cmd(
            f'{args.sudo_s} jupyter labextension install beakerx-jupyterlab',
        )
    if args.uninstall:
        run_cmd(
            f'{args.sudo_s} jupyter labextension uninstall beakerx-jupyterlab',
        )
        run_cmd(
            f'{args.sudo_s} jupyter labextension uninstall @jupyter-widgets/jupyterlab-manager',
        )
        run_cmd(f'{args.sudo_s} beakerx uninstall')
        run_cmd(f'{args.pip} uninstall beakerx')
    if args.config:
        run_cmd(f'{args.sudo_s} chown -R {USER_ID}:{GROUP_ID} {HOME}')


def almond(**kwargs):
    """Install/uninstall/configure the Almond Scala kernel.
    """
    args = namespace(kwargs)
    if args.almond_version is None:
        args.almond_version = '0.4.0'
    else:
        args.install = True
    if args.scala_version is None:
        args.scala_version = '2.12.12'
    else:
        args.install = True
    if args.install:
        coursier = os.path.join(BIN_DIR, 'coursier')
        almond = os.path.join(BIN_DIR, 'almond')
        run_cmd(f'curl -L -o {coursier} https://git.io/coursier-cli')
        run_cmd(f'chmod +x {coursier}')
        run_cmd(
            f'''{coursier} bootstrap -f -r jitpack -i user \
                -I user:sh.almond:scala-kernel-api_{args.scala_version}:{args.almond_version} \
                -o {almond} \
                sh.almond:scala-kernel_{args.scala_version}:{args.almond_version}''',
        )
        run_cmd(f'{args.sudo_s} {almond} --install --global --force')
    if args.config:
        pass


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


def _add_subparser_almond(subparsers):
    add_subparser(
        subparsers, "Almond", aliases=["al", "amd"], add_argument=_almond_args
    )
        

def evcxr_jupyter(**kwargs):
    """Install the evcxr Rust kernel for Jupyter/Lab server.
    """
    args = namespace(kwargs)
    if args.install:
        cmd = f"""{args.sudo_s} apt-get install {args._yes_s} cmake cargo \
            && cargo install --force evcxr_jupyter \
            && {HOME}/.cargo/bin/evcxr_jupyter --install
            """
        run_cmd(cmd)
    if args.config:
        pass
    if args.uninstall:
        cmd = f"""{HOME}/.cargo/bin/evcxr_jupyter --uninstall \
            && cargo uninstall evcxr_jupyter
            """
        run_cmd(cmd)