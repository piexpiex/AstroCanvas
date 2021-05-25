Lightcurve
**********

Lightcurves are representations of the flux variation during a period of time, tipically they represent periodic flux variations of punctual sources and are represented with two cycles of this variation by stimating the average of the entire periods of the lightcurve.

Operation files
---------------

The lightcurves are obtained from fits tables where one column has to contain the time and could be another which contains the intensity at each time. 

First write the name of the fits image in the **xxx** entry and the extension of the fits where are contained the table in the **xx** entry.

Creation of lightcurve images
-----------------------------

To estimate the periodic lightcurve put AstroCanvas in **lightcurve** and write the name of the file and the respective extension.

To obtain the master bias, fill the following parameters and the right of the window.

- **period**: The obtained period of the flux variation.

- **time start**: The starting time of the observation (move the obtained curve along the phase axis).

- **bins number**: The number of bins in the phase axis.

- **min period**: The minimum value for the period search.

- **max period**: The maximum value for the period search.

- **period bins**: The number of period between **min period** and **max period** for the period search.

Then press the **make lightcurve** button and, after the processing, the lightcurve appears in the canvas.

.. figure:: figures/fig11.png
   :align: center

   ..

   fig. 11 screenshot of Astrocanvas in lightcurve mode plotting the average profile of a simulated lightcurve maked with some lorentz curves.

The Matplotlib toolbar is available in the right of the window with its basic functions.

.. code-block:: bash 

In this case, the program only returns the size of the image.

   Lightcurve
   ----------
   period= ( 24.324324324324323 )


Finally, you can save the lightcurve in a table writing a name and clicking on the **Save lightcurve as** button.