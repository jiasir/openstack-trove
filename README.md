trove-api
=========

trove-api is designed to deploy a trove-api using juju.

Overview
--------

This charm provides a trove-api of OpenStack component from juju charm.

Usage
-----

Step by step instructions on using the charm:

    juju deploy trove-api

Add relation for your charm:

    juju add-relation trove-api mysql
     

Configuration
-------------

The configuration options will be listed on the charm store, however If you're making assumptions or opinionated decisions in the charm (like setting a default administrator password), you should detail that here so the user knows how to change it immediately, etc.


Contact Information
-------------------

Though this will be listed in the charm store itself don't assume a user will know that, so include that information here:

Author: jiasir (Taio Jia) <jiasir@icloud.com>

Report bugs at: http://bugs.launchpad.net/charms/+source/trove-api

Location: http://jujucharms.com/charms/distro/trove-api

* Be sure to remove the templated parts before submitting to https://launchpad.net/charms for inclusion in the charm store.

