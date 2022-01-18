Test Servers
============

If you wish to test your application in a separate environment, Pyrogram is able to authorize your account into
Telegram's test servers without hassle. All you need to do is start a new session (e.g.: "my_account_test") using
``test_mode=True``:

.. code-block:: python

    from pyrogram import Client

    with Client("my_account_test", test_mode=True) as app:
        print(app.get_me())

.. note::

    If this is the first time you login into test servers, you will be asked to register your account first.
    Accounts registered on test servers reside in a different, parallel instance of a Telegram server.

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

Test Mode in Official Apps
--------------------------

You can also login yourself into test servers using official desktop apps, such as Telegram Web and Telegram Desktop:

- **Telegram Web**: Login here: https://web.telegram.org/?test=1
- **Telegram Desktop**: Hold ``Alt+Shift`` and right click on "Add account", then choose "Test server".

Test Numbers
------------

Beside normal numbers, the test environment allows you to login with reserved test numbers.
Valid phone numbers follow the pattern ``99966XYYYY``, where ``X`` is the DC number (1 to 3) and ``YYYY`` are random
numbers. Users with such numbers always get ``XXXXX`` or ``XXXXXX`` as the confirmation code (the DC number, repeated
five or six times).