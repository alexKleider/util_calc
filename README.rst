********************
utility_cost_calc.py
********************

OVERVIEW
========

USAGE::

        ./utility_cost_calc.py [input_csv_file] [> result.txt]


``utility_cost_calc.py`` is a Python (3.4.3) script developed to
meet the need of preparing a utility invoice. An input file can
be explicitly specified; if not, "readings.csv" is assumed.

The input must be a CSV file of the form of the included
``readings.csv`` file.  Its ouput is text to
``stdout`` which can be redirected to a file, an example of which is
provided as ``Utility_Bill``.

The file ``calculations`` offers some explanation as to how the
calculations are done; also consult the source code (of course.)

The code is released under the terms of the **GNU Public License**
of your choosing.

The author would welcome comments or questions should any arise.

Alex Kleider
alex@kleider.ca

See also:
file:///home/alex/HTML5/AK/UtilityApp/index.html
