Download_and_first_steps
************************

Download
========

Astrocanvas download is avalaible via Github in scripts version and a exe version is going to be available soon.

.. Astrocanvas download is avalaible via Github in scripts version and a exe program is as well as avalaible in ----.

.. If you download the exe version you do not need to install anything. However if you download the scripts version you will need to install the following Python libraries:

If you download the scripts version you will need to install these Python libraries:

-Astropy.

.. code-block:: bash 

   conda install astropy

-Tkinter.

.. code-block:: bash 

   conda install -c anaconda tk

And make sure that you have the basic libraries already installed (Matplotlib, Numpy and sys)

First steps
===========

.. The exe version is very recommended if you are learning how to work with astronical data, it is easier and avoid the problems of working with scripts.

Currently Astrocanvas only works with data in fits files (a version which could work with data in other formats is not already avalaible), for this reason is recommended that you save your fits files in different folders according their classification (bias, flats, etc).

The simple way to work with this data is making list files (Some examples are shown later), you write a list file with the files of each folder that you want to work with, a description of each mode is examplained in the next sections.

The Astrocanvas operation is easy, you will use these two types of files (fits and list files) and select a operation mode.
