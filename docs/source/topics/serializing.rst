Object Serialization
====================

Serializing means converting a Pyrogram object, which exists as Python class instance, to a text string that can be
easily shared and stored anywhere. Pyrogram provides two formats for serializing its objects: one good looking for
humans and another more compact for machines that is able to recover the original structures.

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

For Humans - str(obj)
---------------------

If you want a nicely formatted, human readable JSON representation of any object in the API -- namely, any object from
:doc:`Pyrogram types <../api/types/index>`, :doc:`raw functions <../telegram/functions/index>` and
:doc:`raw types <../telegram/types/index>` -- you can use ``str(obj)``.

.. code-block:: python

    ...

    with app:
        r = app.get_chat("me")
        print(str(r))

.. tip::

    When using ``print()`` you don't actually need to use ``str()`` on the object because it is called automatically, we
    have done that above just to show you how to explicitly convert a Pyrogram object to JSON.

For Machines - repr(obj)
------------------------

If you want to share or store objects for future references in a more compact way, you can use ``repr(obj)``. While
still pretty much readable, this format is not intended for humans. The advantage of this format is that once you
serialize your object, you can use ``eval()`` to get back the original structure; just make sure to ``import pyrogram``,
as the process requires the package to be in scope.

.. code-block:: python

    import pyrogram

    ...

    with app:
        r = app.get_chat("me")

        print(repr(r))
        print(eval(repr(r)) == r)  # True

.. note::

    Type definitions are subject to changes between versions. You should make sure to store and load objects using the
    same Pyrogram version.