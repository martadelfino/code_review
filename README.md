[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

# Calculate Linkage Disequilibirum

This repo contains scripts to calculate Linkage Disequilibirum (LD) measures. Info on LD:
https://docs.google.com/presentation/d/1I6e-q22om6AiI-cYjlJ7pJ3f5w0gQTDE/edit?usp=sharing&ouid=115928088663191390220&rtpof=true&sd=true 

For the **Code Review** notes, [see](./docs/code_review.md).

## Introduction

This is an example Python repository that can be adapted to any project. To adapt your project, you can follow the [project migration notes](./docs/migrate.md).

A list of development packages and tooling is also included, to assist with *code quality* and make the application of *best practices* easier.

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Setting up a Virtual Environment](#setting-up-a-virtual-environment)
  - [Create and activate a Virtual Environment](#create-and-activate-a-virtual-environment)
  - [Install Required Packages](#install-required-packages)
  - [Using Anaconda/Mamba](#using-anacondamamba)
- [Running the application](#running-the-application)
- [Development](#development)
- [Code Quality](#code-quality)
  - [Linting](#linting)
  - [Formatting](#formatting)
  - [Testing and Coverage](#testing-and-coverage)
  - [pre-commit checks](#pre-commit-checks)
- [Visual Studio Code](#visual-studio-code)
- [License](#license)
- [Contact](#contact)
- [Appendix](#appendix)
  - [Installing `uv`](#installing-uv)
  - [Using `uv`](#using-uv)

## Prerequisites

- Linux
- Python 3.7+

## Setting up a Virtual Environment

Virtual environments are crucial for Python development as they allow you to manage dependencies for different projects separately. By using a virtual environment, you can avoid conflicts between project requirements and maintain a clean workspace.

There are several tools available to manage virtual environments. We consider `venv` which is built-in python, and `uv`, which is an experimental, extremely fast, new Rust-based Python package manager that will offer performance benefits but is less tested in production environments. Other tools include `virtualenv`, `poetry`, and others.

Information on how to use `uv` is in the Appendix. How to [install](#installing-uv) and how to [use](#using-uv) `uv`.

### Create and activate a Virtual Environment

```bash
# .venv is the name of the environment and can be changed
$ python3 -m venv .venv
$ source .venv/bin/activate
```

### Install Required Packages

```bash
$ pip3 install -r requirements.txt
```

After installing your packages, use `pip freeze > requirements.txt` to lock the dependencies to specific versions, ensuring better reproducibility. Sometimes, you may want to separate dependencies into a development branch, commonly seen as `requirements-dev.txt`.

The more modern approach is through the `pyproject.toml` file, which is used with `uv` and is compatible with a few other tools.

#### Dependency tracking

To add new dependencies/packages, in `requirements.txt` lock files, simply add the needed package name on the list.

In `pyproject.toml`, dependencies are specified under the `[project]>dependencies` section, like so:

```toml
[project]
dependencies = [
  "example-library>=1.0",
  "another-library",
]
```

In both cases, run the install to update the dependencies.

### Using Anaconda/Mamba

Anaconda is a powerful distribution for scientific computing and data science, but it might be more than needed for less complex and personal projects. For most Python development, using `venv` or `uv` as described above will be sufficient and more lightweight. Read [here](./docs/anaconda.md) for first steps.

## Running the application

To run the application, activate the virtual environment and:

- Add the current directory to `PYTHONPATH`:

```bash
$ export PYTHONPATH="$PWD:$PYTHONPATH"
```

- Start the application:

```bash
$ python3 -m src.main  # This checks the `src/` module for a script named main and runs it
```

## Development

The development process requires additional packages, installed within the virtual environment. Activate your environment, then install these development-specific packages:

```bash
$ pip3 install -r requirements-dev.txt
```

## Code Quality

High code quality can be ensured through pre-configured tools, ready for immediate use.

### Linting

Code standards are upheld by using the following packages: `ruff`, `flake8`, `pylint`, and `mypy`. The first three are linters, and perform similar, overlapping, linting functions, while `mypy` focuses on static type checking. Their configurations are predefined but can be tailored to meet the application's specific requirements. Execute the following commands to run these tools:

```bash
# To check all Python files
$ flake8 **/*.py
$ pylint **/*.py
$ mypy **/*.py
$ ruff check [optional: file]  # to list linting warnings and errors
$ ruff check --fix [optional: file]  # to fix them automatically
```

### Formatting

For code formatting, `ruff` is used, offering a customizable yet opinionated approach, similar to `black`.

```bash
$ ruff format --help  # to see all available options
$ ruff format --diff [file]  # to print the proposed changes
$ ruff format [optional: file]  # to format all files, or a single one
```

### Testing and Coverage

Testing is conducted with `pytest`, and code coverage is analyzed through `coverage`, utilizing `pytest` for data gathering.

```bash
$ pytest  # to run the whole suite of tests
$ coverage run -m pytest  # to generate a coverage report
$ coverage report -m  # to see the report
```

### pre-commit checks

`pre-commit` integrates with git, running specified hooks before certain git commands. This setup ensures that tests, linting, and formatting are automatically performed, promoting consistent code quality.

To manage hooks within your environment:

```sh
$ pre-commit install  # uninstall
pre-commit installed at .git/hooks/pre-commit
pre-commit installed at .git/hooks/pre-push
```

To bypass a hook temporarily, for instance, to address a failed test in a subsequent commit:

```sh
$ SKIP pytest-check git commit -m "Commit message.."
```

To run the hooks outside of git commands, use `pre-commit run`. To update the hooks, use `pre-commit autoupdate`, and then commit the changes.

## Visual Studio Code

Specific information about using VS Code for development are given [here](./docs/vscode.md).

## License

The project is operating under an [MIT](./LICENSE) license.

## Contact

For questions or suggestions, please contact us at [email](mailto:example@example.com) or open an issue.

## Appendix

### Installing `uv`

From your terminal, execute: `$ curl -LsSf https://astral.sh/uv/install.sh | sh`

Note: It's recommended to review scripts from the internet before executing them. You can view the script at `https://astral.sh/uv/install.sh` before running the above command.

Then restart terminal. To update it, simply invoke `uv self update`.

### Using `uv`

```bash
# Create a virtual environment
$ uv venv .venv
$ source .venv/bin/activate  # to activate

# Install dependencies
$ uv pip install -r pyproject.toml  # preferred
$ uv pip install -r requirements.txt
```
