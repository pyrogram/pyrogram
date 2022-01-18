Client started, but nothing happens
===================================

A possible cause might be network issues, either yours or Telegram's. To check this, add the following code at
the top of your script and run it again. You should see some error mentioning a socket timeout or an unreachable
network:

.. code-block:: python

    import logging
    logging.basicConfig(level=logging.INFO)