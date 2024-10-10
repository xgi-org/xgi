**********
Installing
**********


Installing the released version
===============================

To install XGI, execute the following in the command line:

.. code:: bash

   pip install xgi


XGI was developed and tested for Python 3.9-3.13 on Mac OS, Windows, and Ubuntu.

Once installed, go directly to the `User Guides <user_guides.html>`_ to get started!

Installing the development version
==================================


You can also install the development version, either to contribute or to get the latest (potentially unstable) upgrades without having to wait for a new release.
To do this, you need to first clone the repository and then pip install locally:

.. code:: bash

   git clone https://github.com/xgi-org/xgi.git
   cd xgi
   pip install -e .['all']

If the last line does not work, you may try the following instead

.. code:: zsh

   pip install -e .\[all\]


.. seealso:: 

    For more installation options, see our `guide <installing_more.html>`_.

