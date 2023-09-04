def build():
    config.repo(url="https://github.com/tensorchord/envd", description="envd quick start example")
    base(os="ubuntu20.04", language="python3")
    # Configure pip index if needed.
    # config.pip_index(url = "https://pypi.tuna.tsinghua.edu.cn/simple")
    install.python_packages(name = [
        "numpy",
    ])
    shell("zsh")