# Installation

Picamera zero (picamzero) is designed to allow beginners to control a Raspberry Pi camera with Python.

To install the `picamzero` library:
1. Open a terminal window on your Raspberry Pi.

![Open a terminal window](images/open-terminal.png)

2. Type this command and press enter to install some packages you will need:

    ```
    sudo apt install -y libcap-dev python3-libcamera
    ```

3. Type this command to create a virtual environment (venv)

    ```
    python3 -m venv --system-site-packages venv
    ```

4. Type this command to start the virtual environment. You will need to do this each time you want to use picamzero.
    ```
    source venv/bin/activate
    ```

5. Finally, type this command to install picamzero

    ```
    pip3 install picamzero
    ```

Now you're good to go! Start by writing your [first program](hello_world.md).

