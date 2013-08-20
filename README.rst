Stats Tool
==========

This is a CLI tool for producing svg charts of `datagrepper
<https://apps.fedoraproject.org/datagrepper>`_ based off of Pierre-Yves
Chibon's `thisweekinfedora <https://github.com/pypingou/thisweekinfedora>`_.

Dependencies
------------

It requires a few python packages::

    $ sudo yum install python-requests python-pygal python-progressbar

Interesting options
-------------------

It has command line options.  Try::

    $ git clone https://github.com/ralphbean/fedora-stats-tools.git
    $ cd fedora-stats-tools/
    $ python stats.py --help

Try running it with these options::

    $ python stats.py --steps 30 --date-format %U
