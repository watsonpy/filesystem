Usage
=====

Using the filesystem module is easily initialized by the following:

.. code-block:: python

    from watson.filesystem import Filesystem, backends

    fs = Filesystem(backends.Local())
    print(fs.read('path/to/file'))  # contents of file

In order to maintain a simplistic API, all the backends can be imported from watson.filesystem.backends.NAME_OF_BACKEND.

For more information regarding the various API methods avaiable, please see the reference library.
