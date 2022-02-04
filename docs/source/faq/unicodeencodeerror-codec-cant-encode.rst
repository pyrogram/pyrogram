UnicodeEncodeError: '...' codec can't encode ...
================================================

Where ``<encoding>`` might be *ascii*, *cp932*, *charmap* or anything else other than *utf-8*. This error usually
shows up when you try to print something and has very little to do with Pyrogram itself as it is strictly related to
your own terminal. To fix it, either find a way to change the encoding settings of your terminal to UTF-8 or switch to
another terminal altogether.
