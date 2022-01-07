Debugging
=========

When working with the API, chances are you'll stumble upon bugs, get stuck and start wondering how to continue. Nothing
to actually worry about since Pyrogram provides some commodities to help you in this.

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

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

    me = app.get_users("me")
    print(me)  # User

This will show a JSON representation of the object returned by :meth:`~pyrogram.Client.get_users`, which is a
:class:`~pyrogram.types.User` instance, in this case. The output on your terminal will be something similar to this:

.. code-block:: json

    {
        "_": "User",
        "id": 123456789,
        "is_self": true,
        "is_contact": false,
        "is_mutual_contact": false,
        "is_deleted": false,
        "is_bot": false,
        "is_verified": false,
        "is_restricted": false,
        "is_support": false,
        "first_name": "Pyrogram",
        "photo": {
            "_": "ChatPhoto",
            "small_file_id": "AbCdE...EdCbA",
            "small_photo_unique_id": "VwXyZ...ZyXwV",
            "big_file_id": "AbCdE...EdCbA",
            "big_photo_unique_id": "VwXyZ...ZyXwV"
        }
    }

As you've probably guessed already, Pyrogram objects can be nested. That's how compound data are built, and nesting
keeps going until we are left with base data types only, such as ``str``, ``int``, ``bool``, etc.

Accessing Attributes
--------------------

Even though you see a JSON output, it doesn't mean we are dealing with dictionaries; in fact, all Pyrogram types are
fully-fledged Python objects and the correct way to access any attribute of them is by using the dot notation ``.``:

.. code-block:: python

    photo = me.photo
    print(photo)  # ChatPhoto

.. code-block:: json

    {
        "_": "ChatPhoto",
        "small_file_id": "AbCdE...EdCbA",
        "small_photo_unique_id": "VwXyZ...ZyXwV",
        "big_file_id": "AbCdE...EdCbA",
        "big_photo_unique_id": "VwXyZ...ZyXwV"
    }

Checking an Object's Type
-------------------------

Another thing worth talking about is how to tell and check for an object's type.

As you noticed already, when printing an object you'll see the special attribute ``"_"``. This is just a visual thing
useful to show humans the object type, but doesn't really exist anywhere; any attempt in accessing it will lead to an
error. The correct way to get the object type is by using the built-in function ``type()``:

.. code-block:: python

    status = me.status
    print(type(status))

.. code-block:: text

    <class 'pyrogram.types.UserStatus'>

And to check if an object is an instance of a given class, you use the built-in function ``isinstance()``:

.. code-block:: python
    :name: this-py

    from pyrogram.types import UserStatus

    status = me.status
    print(isinstance(status, UserStatus))

.. code-block:: text

    True

.. raw:: html

    <script>
        var e = document.querySelector("blockquote p.attribution");
        var s = e.innerHTML;

        e.innerHTML = s[0] + " " + s.slice(1);
    </script>