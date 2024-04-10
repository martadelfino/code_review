Anaconda is a popular distribution of Python and R specifically aimed at scientific computing, data science, and machine learning. Mamba is a fast, drop-in replacement for the conda package manager that comes with Anaconda. Using Anaconda or Mamba can simplify package management and deployment, especially for complex dependencies.

***Disclaimer***: Just because it _can_ simplify package management, doesn't mean it _will_. If you have doubts on which package manager to use for your personal project, default to using `venv` or `virtualenv` (or `poetry`, or `uv`).

To install Mamba, follow the [official instructions](https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html).

After you install `mamba`, create and activate the environment:

```bash
mamba create --quiet --yes --name env
mamba activate env
```

Then install the packages:

```bash
mamba install -c conda-forge --file requirements.txt
```
