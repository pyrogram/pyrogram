Debugging
=========

When working with the API, chances are you'll stumble upon bugs, get stuck and start wondering how to continue. Nothing
to actually worry about -- that's normal -- and luckily for you, Pyrogram provides some commodities to help you in this.

Caveman Debugging
-----------------

    *The most effective debugging tool is still careful thought, coupled with judiciously placed print statements.*

    -- Brian Kernighan, "Unix for Beginners" (1979)

Adding ``print()`` statements in crucial parts of your code is by far the most ancient, yet efficient technique for
debugging programs, especially considering the concurrent nature of the framework itself. Pyrogram goodness in this
respect comes with the fact that any object can be nicely printed just by calling ``print(obj)``, thus giving to you
an insight of all its inner details.

Consider the following code:

.. code-block:: python

    dan = app.get_users("haskell")
    print(dan)  # User

This will show a JSON representation of the object returned by :meth:`~pyrogram.Client.get_users`, which is a
:class:`~pyrogram.User` instance, in this case. The output on your terminal will be something similar to this:

.. code-block:: json

    {
        "_": "pyrogram.User",
        "id": 23122162,
        "is_self": false,
        "is_contact": false,
        "is_mutual_contact": false,
        "is_deleted": false,
        "is_bot": false,
        "is_verified": false,
        "is_restricted": false,
        "is_support": false,
        "is_scam": false,
        "first_name": "Dan",
        "status": {
            "_": "pyrogram.UserStatus",
            "user_id": 23122162,
            "recently": true
        },
        "username": "haskell",
        "language_code": "en",
        "photo": {
            "_": "pyrogram.ChatPhoto",
            "small_file_id": "AQADBAAD8tBgAQAEJjCxGgAEo5IBAAIC",
            "big_file_id": "AQADBAAD8tBgAQAEJjCxGgAEpZIBAAEBAg"
        }
    }

As you've probably guessed already, Pyrogram objects can be nested. That's how compound data are built, and nesting
keeps going until we are left with base data types only, such as ``str``, ``int``, ``bool``, etc.

Accessing Attributes
--------------------

Even though you see a JSON output, it doesn't mean we are dealing with dictionaries; in fact, all Pyrogram types are
full-fledged Python objects and the correct way to access any attribute of them is by using the dot notation ``.``:

.. code-block:: python

    dan_photo = dan.photo
    print(dan_photo)  # ChatPhoto

.. code-block:: json

    {
        "_": "pyrogram.ChatPhoto",
        "small_file_id": "AQADBAAD8tBgAQAEJjCxGgAEo5IBAAIC",
        "big_file_id": "AQADBAAD8tBgAQAEJjCxGgAEpZIBAAEBAg"
    }

However, the bracket notation ``[]`` is also supported, but its usage is discouraged:

.. warning::

    Bracket notation in Python is not commonly used for getting/setting object attributes. While it works for Pyrogram
    objects, it might not work for anything else and you should not rely on this.

.. code-block:: python

    dan_photo_big = dan["photo"]["big_file_id"]
    print(dan_photo_big)  # str

.. code-block:: text

    AQADBAAD8tBgAQAEJjCxGgAEpZIBAAEBAg

Checking an Object's Type
-------------------------

Another thing worth talking about is how to tell and check for an object's type.

As you noticed already, when printing an object you'll see the special attribute ``"_"``. This is just a visual thing
useful to show humans the object type, but doesn't really exist anywhere; any attempt in accessing it will lead to an
error. The correct way to get the object type is by using the built-in function ``type()``:

.. code-block:: python

    dan_status = dan.status
    print(type(dan_status))

.. code-block:: text

    <class 'pyrogram.UserStatus'>

And to check if an object is an instance of a given class, you use the built-in function ``isinstance()``:

.. code-block:: python
    :name: this-py

    from pyrogram import UserStatus

    dan_status = dan.status
    print(isinstance(dan_status, UserStatus))

.. code-block:: text

    True

.. raw:: html

    <script>
        var e = document.querySelector("blockquote p.attribution");
        var s = e.innerHTML;

        e.innerHTML = s[0] + " " + s.slice(1);
    </script>