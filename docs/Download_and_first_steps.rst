Download_and_first_steps
************************

Download
========

Astrocanvas download is avalaible via Github in scripts version (provisional version available at `https://github.com/piexpiex/AstroCanvas <https://github.com/piexpiex/AstroCanvas>`_) and a exe version is available in this `link <https://docs.google.com/uc?export=download&id=15dlO_jCA0y5SujUVx74I48P4Tmxy_yb5>`_ .

If you download the exe version you will not need to install anything. However if you download the scripts version you will need to install the following Python libraries:

-Astropy.

.. code-block:: bash 

   conda install astropy

-Tkinter.

.. code-block:: bash 

   conda install -c anaconda tk

And make sure that you have the basic libraries already installed (Matplotlib, Numpy and sys)

First steps
===========

The exe version is very recommended if you are learning how to work with astronical data, it is easier and avoid the problems of working with scripts.

Currently Astrocanvas only works with data in fits files (a version which could work with data in other formats is not already avalaible), for this reason is recommended that you save your fits files in different folders according their classification (bias, flats, etc).

The simple way to work with this data is making list files (Some examples are shown in next sections), you write a list file with the files of each folder that you want to work with, a description of each mode is examplained in the next sections.
