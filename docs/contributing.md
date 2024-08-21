# Contributing

### On a Raspberry Pi
Make sure you have installed these packages via Debian package manager

```
sudo apt install python3-pytest mkdocs pre-commit python3-opencv
```

### In another environment
Install the dependencies directly into a virtual environment using Python's built-in `venv` module:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Note that `picamera2` - the library on which `picamera-zero` depends - is only installable on Linux.

## Clone the repo

Make sure that you have a SSH key set up in GitHub first.

```
git clone git@github.com:RaspberryPiFoundation/picamera-zero.git
```

## Documentation
The package is documented with mkdocs. From the directory with `mkdocs.yml` type

```
mkdocs serve
```

This will start the server. View the docs in a browser at `http://127.0.0.1:8000`

You can make changes to the docs in the .md files.


## Testing
Navigate to the `tests` directory and run the pytest command:

```
pytest
```

You can write tests in the tests directory. Each test function, and each file needs to begin with the prefix `test_`


## Build the package

From the main directory (with `pyproject.toml`) type:

```
sudo apt install python3-build
python -m build
```

The distribution will be created in the `dist` directory.


## Continuous integration

There are two CI jobs executed on each PR. The `lint` job uses `pre-commit` to check for common errors and formatting, while the `build` job simply tries to build the package using the `build` module.

### Pre-commit static checks

You may find it useful to set up `pre-commit` to run some static checks before each commit. Doing so can help catch common errors, and unify code style.

`pre-commit` should already be installed if you followed the installation instructions above - if not, install on a development pi with `sudo apt install pre-commit`. To set it up to run before every commit, execute `pre-commit install`. Once set up, `pre-commit` will check every file changed in a commit.

To make `pre-commit` check every file in the repository, execute `pre-commit run --all-files`. Alternatively, to skip verification, you can use the `--no-verify` option when committing: `git commit --no-verify`

At any time, you can uninstall `pre-commit` by running `pre-commit uninstall`.

### Deployments

Deployments should use semantic versioning (https://semver.org/).
The deployment workflow is triggered upon creation of a new Github release, and checks that the version specified in `picamzero/__init__.py.__version__` matches the tag
in the Github release. The package is then built using the `build` module before being deployed to `TestPyPI` and `PyPI`.
