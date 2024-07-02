# Pi camera zero (picamzero)

picamzero is a Python 3 library designed to help beginners to easily use the Raspberry Pi Camera.


## Developing
Make sure you have installed these packages via Debian package manager

```
sudo apt install python3-pytest
sudo apt install mkdocs
```

Alternatively, if not on a Raspberry Pi you may install the dependencies directly into a virtual environment using Python's built-in `venv` module:

```bash
python3 -m venv venv
source venv/bin/activate
pip install pytest mkdocs
```

Note that `picamera2` - the library on which `picamera-zero` depends - is only installable on Linux.

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
