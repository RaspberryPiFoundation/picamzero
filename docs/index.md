# Picamera zero (picamzero)

Picamera zero (`picamzero`) makes it easy for beginners to control a Raspberry Pi camera with Python.

---
### <a name="install"></a> Install

1. Open a terminal window on your Raspberry Pi.

    ![Open a terminal window](images/open-terminal.png)

2. Type this command to run the install script:

    ```
    curl -L --fail http://rpf.io/picamzero-install | bash
    ```

    This will create a `picamzero-venv` where picamzero can be used.


### Use in Thonny

After installing, follow these instructions to use picamzero in Thonny

1. From the Programming menu, open Thonny.

    ![Open a Python editor](images/open-editor.png)

2. Click "Switch to regular mode" on the top right, then close and reopen Thonny.

3. Click **Run** > **Configure Interpreter**

4. Click on the three dots next to "Python executable".

5. Navigate to your home directory, and then enter the `picamzero-venv` folder. Then, enter the `bin` folder and click `python3` inside that folder. Click OK to close the window.

Now you're good to go! Start by writing your [first program](hello_world.md).

