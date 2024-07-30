# Pi camera zero (picamzero)

picamzero is a Python 3 library designed to help beginners to easily use the Raspberry Pi Camera.


## Developing
Make sure you have installed these packages via Debian package manager

```
sudo apt install python3-pytest mkdocs pre-commit
```

Alternatively, if not on a Raspberry Pi you may install the dependencies directly into a virtual environment using Python's built-in `venv` module:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Note that `picamera2` - the library on which `picamera-zero` depends - is only installable on Linux.

### Pre-commit static checks

You may find it useful to set up `pre-commit` to run some static checks before each commit. Doing so can help catch common errors, and unify code style.

`pre-commit` should already be installed if you followed the installation instructions above. To set it up to run before every commit, execute `pre-commit install`. Once set up, `pre-commit` will check every file changed in a commit. To make `pre-commit` check every file in the repository, execute `pre-commit run --all-files`. Alternatively, to skip verification, you can use the `--no-verify` option when committing: `git commit --no-verify`

At any time, you can uninstall `pre-commit` by running `pre-commit uninstall`.

### Clone the repo
On your Raspberry Pi (Bookworm):

```
git clone git@github.com:RaspberryPiFoundation/picamera-zero.git
```

### Documenting
The package is documented with mkdocs. From the directory with `mkdocs.yml` type

```
mkdocs serve
```

This will start the server. View the docs in a browser at `http://127.0.0.1:8000`

You can make changes to the docs in the .md files.

Do **NOT** use `mkdocs gh-deploy` command until the package is live - even though the repo is private, this will still publish a public website!

### Testing
Navigate to the `tests` directory and run the pytest command:

```
pytest
```

You can write tests in the tests directory. Each test function, and each file needs to begin with the prefix `test_`


## Build the package

From the main directory (with `pyproject.toml`) type:

```
python -m build
```

The distribution will be created in the `dist` directory.

(You might need to `sudo apt install python3-build` I can't remember!)


### Continuous integration

There are two CI jobs executed on each PR. The `lint` job uses `pre-commit` to check for common errors and formatting, while the `build` job simply tries to build the package using the `build` module. Since `picamera2` is only available on a real Raspberry Pi, and Github workers are not Raspberry Pis, it is not possible to run integration tests in the CI pipeline.

### Deployments

Deployments should use semantic versioning (https://semver.org/).
The deployment workflow is triggered upon creation of a new Github release, and checks that the version specified in `picamzero/__init__.py.__version__` matches the tag
in the Github release. The package is then built using the `build` module before being deployed to `TestPyPI` and `PyPI`.
