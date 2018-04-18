Auto Authorization
==================

Manually writing phone number, phone code and password on the terminal every time you want to login can be tedious.
Pyrogram is able to automate both **Log In** and **Sign Up** processes, all you need to do is pass the relevant
parameters when creating a new :class:`Client <pyrogram.Client>`.

.. note:: If you omit any of the optional parameter required for the authorization, Pyrogram will ask you to
   manually write it. For instance, if you don't want to set a ``last_name`` when creating a new account you
   have to explicitly pass an empty string ""; the default value (None) will trigger the input() call.

Log In
-------

To automate the **Log In** process, pass your ``phone_number`` and ``password`` (if you have one) in the Client parameters.
If you want to retrieve the phone code programmatically, pass a callback function in the ``phone_code`` field — this
function must return the correct phone code as string (e.g., "12345") — otherwise, ignore this parameter, Pyrogram will
ask you to input the phone code manually.

.. code-block:: python

    from pyrogram import Client

    def phone_code_callback():
        code = ...  # Get your code programmatically
        return code  # Must be string, e.g., "12345"


    app = Client(
        session_name="example",
        phone_number="39**********",
        phone_code=phone_code_callback,
        password="password"  # (if you have one)
    )

    app.start()
    print(app.get_me())

Sign Up
-------

To automate the **Sign Up** process (i.e., automatically create a new Telegram account), simply fill **both**
``first_name`` and ``last_name`` fields alongside the other parameters; they will be used to automatically create a new
Telegram account in case the phone number you passed is not registered yet.

.. code-block:: python

    from pyrogram import Client

    def phone_code_callback():
        code = ...  # Get your code programmatically
        return code  # Must be string, e.g., "12345"


    app = Client(
        session_name="example",
        phone_number="39**********",
        phone_code=phone_code_callback,
        first_name="Pyrogram",
        last_name=""  # Can be an empty string
    )

    app.start()
    print(app.get_me())