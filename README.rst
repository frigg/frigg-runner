frigg-runner |Build status| |Coverage status| |pypi version| |requires|
=======================================================================

Frigg runner, execute .frigg.yml file locally.

.. code-block:: bash

    pip install frigg-runner

Run the tasks:

.. code-block:: bash

    frigg

``--help`` will show the help page below.

.. code-block:: bash

    Usage: frigg [OPTIONS]

    Options:
      -f, --failfast  Exit if one of the tasks returns other than statuscode 0.
      -v, --verbose   Print output from every task.
      -p, --path      Working directory, the path where the friggfile lives.
      --help          Show this message and exit.



--------------

MIT © frigg.io


.. |Build status| image:: https://ci.frigg.io/badges/frigg/frigg-runner/
        :target: https://ci.frigg.io/frigg/frigg-runner/

.. |Coverage status| image:: http://ci.frigg.io/badges/coverage/frigg/frigg-runner/
        :target: https://ci.frigg.io/frigg/frigg-runner/

.. |pypi version| image:: https://pypip.in/version/frigg-runner/badge.svg?style=flat
    :target: https://pypi.python.org/pypi/frigg-runner/

.. |requires| image:: https://requires.io/github/frigg/frigg-runner/requirements.svg?branch=master
     :target: https://requires.io/github/frigg/frigg-runner/requirements/?branch=master
     :alt: Requirements Status
