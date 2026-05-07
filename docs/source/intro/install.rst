Installation
============

Requirements
------------

- Python 3.8 or newer
- ``pycountry`` (installed automatically)

Install from PyPI
-----------------

.. code-block:: bash

    pip install smartfaker

Install from source
-------------------

.. code-block:: bash

    git clone https://github.com/abirxdhack/TheSmartFaker
    cd TheSmartFaker
    pip install -e .

Optional: development extras
----------------------------

.. code-block:: bash

    pip install "smartfaker[dev]"

Optional: documentation extras
------------------------------

.. code-block:: bash

    pip install "smartfaker[docs]"

Verify installation
-------------------

.. code-block:: python

    import smartfaker
    print(smartfaker.__version__)
