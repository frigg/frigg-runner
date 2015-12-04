frigg-runner |Build status| |Coverage status|
=============================================

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
      -f, --failfast   Exit if one of the tasks returns other than statuscode 0.
      -v, --verbose    Print output from every task.
      -p, --path TEXT  Working directory, the path where the friggfile lives.
      -s, --setup      Run tasks from setup_tasks list before the main tasks.
      --help           Show this message and exit.


--------------

MIT © frigg.io


.. |Build status| image:: https://ci.frigg.io/badges/frigg/frigg-runner/
        :target: https://ci.frigg.io/frigg/frigg-runner/

.. |Coverage status| image:: http://ci.frigg.io/badges/coverage/frigg/frigg-runner/
        :target: https://ci.frigg.io/frigg/frigg-runner/
