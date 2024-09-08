# Training T. Rex Rush
Work developed for the evaluation of Unit 01 of the discipline Advanced Topics in Computational Intelligence, taught by Professor Ariel at SENAI CIMATEC.

If you use Windows, use chocolatey for installing things
chocolatey installation guide

Use pyenv for Python version management

pyenv installation guide

```curl https://pyenv.run | bash
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo 'eval "$(pyenv init -)"' >> ~/.bashrc
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.profile
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.profile
echo 'eval "$(pyenv init -)"' >> ~/.profile
exit```

In another shell:

```pyenv update
pyenv install 3.9.13
pyenv rehash
pyenv global 3.9.13
exit```

Use make for simplifing commands and making it explicit how to run your code
make documentation

Use poetry for managing Python dependencies

Poetry is a tool for dependency management and packaging in Python. It allows you to declare the libraries your project depends on and it will manage (install/update) them for you. Poetry offers a lockfile to ensure repeatable installs, and can build your project for distribution.

Basic commands:

```Add new dependency: poetry add <package>
Install dependencies: poetry install
Update dependencies: poetry update
Remove dependencies: poetry remove <package>
Run a command in the virtual environment: poetry run <command>
Run python in the virtual environment: poetry run python <command>```

Make sure to use the Makefile to facilitate the usage of your repository

Anyone that clones your repository should be able to relatively easily run your code with just a few commands. The Makefile should contain the following commands:

```make install
make run
Use pre-commit for running checks before committing
pre-commit is a framework for managing and maintaining multi-language pre-commit hooks. It is a client-side hook manager that can be used to automate checks before committing code. It is recommended to use pre-commit to ensure code formatting, among other things.```
