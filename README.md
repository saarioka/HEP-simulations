# HEP-simulations
High Energy Physics simulations using FLUKA and Geant4

## Running FLUKA simulations
1. Create _.inp_-files
    * Format: __\<bulk identifier>__-__\<index for bulk thickness>__-__\<index for beam energy>__.inp
    * Easiest is to use Loop-tool in Flair to create runs runs iterating over a parameter and then run them with 0 repetitions. This throws an error, but the _.inp_ file is created
1. Run _generate_runs.py_
    * This runs the simulation and combines the results with _usXsuw_-programs (part of FLUKA installation)
1. Run _create_plots.py_
    * Converts results of last step from multiple binary files to a _csv_-file
