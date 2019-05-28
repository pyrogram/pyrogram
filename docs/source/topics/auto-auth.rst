Auto Authorization
==================

Manually writing phone number, phone code and password on the terminal every time you want to login can be tedious.
Pyrogram is able to automate both **Log In** and **Sign Up** processes, all you need to do is pass the relevant
parameters when creating a new :class:`~pyrogram.Client`.

.. note:: If you omit any of the optional parameter required for the authorization, Pyrogram will ask you to
   manually write it. For instance, if you don't want to set a ``last_name`` when creating a new account you
   have to explicitly pass an empty string ""; the default value (None) will trigger the input() call.

Log In
-------

To automate the **Log In** process, pass your ``phone_number`` and ``password`` (if you have one) in the Client parameters.
If you want to retrieve the phone code programmatically, pass a callback function in the ``phone_code`` field — this
function accepts a single positional argument (phone_number) and must return the correct phone code  (e.g., "12345")
— otherwise, ignore this parameter, Pyrogram will ask you to input the phone code manually.

Example:

.. code-block:: python

    from pyrogram import Client

    def phone_code_callback(phone_number):
        code = ...  # Get your code programmatically
        return code  # e.g., "12345"


    app = Client(
        session_name="example",
        phone_number="39**********",
        phone_code=phone_code_callback,  # Note the missing parentheses
        password="password"  # (if you have one)
    )

    with app:
        print(app.get_me())

Sign Up
-------

To automate the **Sign Up** process (i.e., automatically create a new Telegram account), simply fill **both**
``first_name`` and ``last_name`` fields alongside the other parameters; they will be used to automatically create a new
Telegram account in case the phone number you passed is not registered yet.

Example:

.. code-block:: python

    from pyrogram import Client

    def phone_code_callback(phone_number):
        code = ...  # Get your code programmatically
        return code  # e.g., "12345"


    app = Client(
        session_name="example",
        phone_number="39**********",
        phone_code=phone_code_callback,  # Note the missing parentheses
        first_name="Pyrogram",
        last_name=""  # Can be an empty string
    )

    with app:
        print(app.get_me())
