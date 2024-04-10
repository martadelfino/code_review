# Visual Studio Code

A workspace configuration file is provided, which includes global settings as well as extension settings.

The file is `.vscode/settings.json` and is automatically used when the workspace is opened. It also takes precedence over the user (general) VS Code `settings.json` file.

## VS Code Configuration Settings

The file includes a set of general settings, which could be moved to the more general settings file, and a set of Python-specific settings for the extensions we are considering.

The extensions are:
- `Python`
  - includes `Pylance`, `Python Debugger`
- `Jupyter`
  -  includes `Jupyter Cell Tags`, `Jupyter Keymap`, `Jupyter Notebook Renderer`, `Jupyter Slide Show`
- `Flake8`
- `Pylint`
- `Mypy Type Checker`
- `Ruff`

To install them, open the "Extensions" tab as usual (or with `Ctrl/Cmd + Shift + X`) and search them by name.

Alternatively, they should appear on the Recommended tab, courtesy of `extensions.json`.

Remember to enable them by workspace to minimize performance degradation.
