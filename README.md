# quantum_macchiato
Python module in development for automating the use of Quantum Espresso, a software for DFT based physics simulations.

For now, it's pretty much a collection of functions, altough it really makes it a lot easier to use QE.

Before using, add to the run function (the first in the file) the path to the bin directory in the QE directory of your PC.

When using, you can import it in a python script just like any other library (ex: import quantum_macchiato as qm), since one of the two are met: (1) the quantum_macchiato file is in the same folder where the script will be ran; (2) the quantum_macchiato file is in the python path.

There are functions for convergency tests of variables (ex: ecutwfc) and k-points.

Some functions are based on the pandas library, namely the functions that transform files from .dat extension to .csv extension.

For now, there are not automated plots. I consider plots as something based primarily on the autor's choice - for example, when plotting bands, you might wanna calculate a lot of bands just for checking, but plot just those around the Fermi energy. Therefore, automated plots are not a priority on this module. This is the major reason for transforming .dat files do .csv: they are a lot easier to work with the data it contains in the post-processing step.

Suggestions are welcome.
