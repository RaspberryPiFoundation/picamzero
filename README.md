# Pi camera zero (picamzero)

picamzero is a Python 3 library designed to allow beginners to control a Raspberry Pi camera with Python.

## Installation

1. Open a terminal window on your Raspberry Pi.

    ![Open a terminal window](images/open-terminal.png)

2. Install packages required from apt:

    ```
    sudo apt install -y libcap-dev python3-libcamera
    ```

3. Create a virtual environment (venv)

    ```
    python3 -m venv --system-site-packages venv
    ```

4. Start the virtual environment. You will need to do this each time you want to use picamzero.
    ```
    source venv/bin/activate
    ```

5. Install picamzero

    ```
    pip3 install picamzero
    ```

## Documentation

Full, beginner-friendly documentation is provided at [http://raspberrypifoundation.github.io/picamzero]
(this link won't work yet).