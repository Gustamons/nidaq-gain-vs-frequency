# Nidaq gain vs frequency

This repository contains a Python script which generates a sine wave using NI-DAQ analog output channels. This output voltage can be passed through an amplifying circuit, and the no-gain output can be compared to the with-gain output to obtain the gain ratio. At the end of the script, the frequency, U_input, and U_output are saved in a `.csv` file.

At the top of the code there are changeable parameters which can be adjusted for the necessary NI-DAQ pins (output, input1, input2, dev). There are also parameters which affect the generated wave (amplitude, points) and sweep parameters (cycles, freq_start, freq_end, num_data_points). The default parameters were chosen with a low "points" value (points per wave), because I used an NI-6212, and to test higher frequencies I had to use a lower number of points per sine wave.

The commented parts of the code contain plotting of the gain-vs-frequency data. It requires the matplotlib package, so by default it is commented out. An example plot is available in the repository.
