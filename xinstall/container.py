
def docker(**kwargs):
    """Install and configure Docker container.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source()
            run_cmd(
                f'{args.sudo_s} apt-get install {args._yes_s} docker.io docker-compose',
            )
        elif is_macos():
            brew_install_safe(
                [
                    'docker', 'docker-compose', 'bash-completion@2',
                    'docker-completion', 'docker-compose-completion'
                ]
            )
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} yum install docker docker-compose')
    if args.config:
        run_cmd('gpasswd -a $(id -un) docker')
        logging.warning(
            'Please logout and then login to make the group "docker" effective!'
        )
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(
                f'{args.sudo_s} apt-get purge {args._yes_s} docker docker-compose',
            )
        elif is_macos():
            run_cmd(
                f'brew uninstall docker docker-completion docker-compose docker-compose-completion',
            )
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} yum remove docker docker-compose')


def kubernetes(**kwargs):
    """Install and configure kubernetes command-line interface.
    """
    args = namespace(kwargs)
    if args.install:
        if is_ubuntu_debian():
            run_cmd(
                f'curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | {args.sudo_s} apt-key add -',
            )
            run_cmd(
                f'echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | {args.sudo_s} tee -a /etc/apt/sources.list.d/kubernetes.list',
            )
            update_apt_source(seconds=-1E10)
            run_cmd(f'{args.sudo_s} apt-get install {args._yes_s} kubectl')
        elif is_macos():
            brew_install_safe(['kubernetes-cli'])
        elif is_centos_series():
            pass
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f'{args.sudo_s} apt-get purge {args._yes_s} kubectl')
        elif is_macos():
            run_cmd(f'brew uninstall kubectl')
        elif is_centos_series():
            pass


def _minikube_linux(sudo: bool, yes: bool = True):
    run_cmd(
        f'''curl -L https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64 -o /tmp/minikube-linux-amd64 \
            && {'sudo' if sudo else ''} apt-get install {yes} /tmp/minikube-linux-amd64 /usr/local/bin/minikube''',
    )
    print('VT-x/AMD-v virtualization must be enabled in BIOS.')


def minikube(**kwargs):
    args = namespace(kwargs)
    virtualbox(**kwargs)
    kubernetes(**kwargs)
    if args.install:
        if is_ubuntu_debian():
            update_apt_source(seconds=-1E10)
            _minikube_linux(sudo=args.sudo, yes=args.yes)
        elif is_macos():
            run_cmd(f'brew cask install minikube')
        elif is_centos_series():
            _minikube_linux(sudo=args.sudo, yes=args.yes)
        elif is_win():
            run_cmd(f'choco install minikube')
            print('VT-x/AMD-v virtualization must be enabled in BIOS.')
    if args.config:
        pass
    if args.uninstall:
        if is_ubuntu_debian():
            run_cmd(f'{args.sudo_s} rm /usr/local/bin/minikube')
        elif is_macos():
            run_cmd(f'brew cask uninstall minikube')
        elif is_centos_series():
            run_cmd(f'{args.sudo_s} rm /usr/local/bin/minikube')