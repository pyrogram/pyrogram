How to avoid Flood Waits?
=========================

Slow things down and make less requests. Moreover, exact limits are unknown and can change anytime based on normal
usages.

When a flood wait happens the server will tell you how much time to wait before continuing.
The following shows how to catch the exception in your code and wait the required seconds.

.. code-block:: python

  import time
  from pyrogram.errors import FloodWait

  ...
      try:
          ...  # Your code
      except FloodWait as e:
          await asyncio.sleep(e.x)  # Wait "x" seconds before continuing
  ...


More info about error handling can be found :doc:`here <../start/errors>`.