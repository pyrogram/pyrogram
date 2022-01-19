What are the IP addresses of Telegram Data Centers?
===================================================

Telegram is currently composed by a decentralized, multi-DC infrastructure (currently 5 DCs, each of which can
work independently) spread across different locations worldwide. However, some of the less busy DCs have been lately
dismissed and their IP addresses are now kept as aliases to the nearest one.

.. csv-table:: Production Environment
    :header: ID, Location, IPv4, IPv6
    :widths: auto
    :align: center

    DC1, "MIA, Miami FL, USA", ``149.154.175.53``, ``2001:b28:f23d:f001::a``
    DC2, "AMS, Amsterdam, NL", ``149.154.167.51``, ``2001:67c:4e8:f002::a``
    DC3*, "MIA, Miami FL, USA", ``149.154.175.100``, ``2001:b28:f23d:f003::a``
    DC4, "AMS, Amsterdam, NL", ``149.154.167.91``, ``2001:67c:4e8:f004::a``
    DC5, "SIN, Singapore, SG", ``91.108.56.130``, ``2001:b28:f23f:f005::a``

.. csv-table:: Test Environment
    :header: ID, Location, IPv4, IPv6
    :widths: auto
    :align: center

    DC1, "MIA, Miami FL, USA", ``149.154.175.10``, ``2001:b28:f23d:f001::e``
    DC2, "AMS, Amsterdam, NL", ``149.154.167.40``, ``2001:67c:4e8:f002::e``
    DC3*, "MIA, Miami FL, USA", ``149.154.175.117``, ``2001:b28:f23d:f003::e``

.. centered:: More info about the Test Environment can be found :doc:`here <../topics/test-servers>`.

***** Alias DC