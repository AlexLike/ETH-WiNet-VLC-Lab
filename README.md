# Wireless Networking and Mobile Computing 2021 – Assignment 5

This project attempts to demonstrate Visible Light Communication (VLC)[^1][^2] by implementing a two-way chat app between two clients. LED-equipped Arduinos Uno (flashed with an ETH driver program) serve as transceivers and are controlled by a Python script. The chat app ("VLChat") is accompanied by a stat collection program ("VLCollect") for further analysis. The notebook Findings.ipynb dives deeper into the topic.

[^1]: Dietz P., Yerazunis W., Leigh D. (2003) Very Low-Cost Sensing and Communication Using Bidirectional LEDs. In: Dey A.K., Schmidt A., McCarthy J.F. (eds) UbiComp 2003: Ubiquitous Computing. UbiComp 2003. Lecture Notes in Computer Science, vol 2864. Springer, Berlin, Heidelberg. doi: 10.1007/978-3-540-39653-6_14
[^2]: S. Schmid, D. Schwyn, K. Akşit, G. Corbellini, T. R. Gross and S. Mangold, "From sound to sight: Using audio processing to enable visible light communication," 2014 IEEE Globecom Workshops (GC Wkshps), 2014, pp. 518-523, doi: 10.1109/GLOCOMW.2014.7063484.

## Path to the first execution

To install all dependecies, run `make`. (This assumes that your PIP version is installed as `pip` in `/bin`.)

To execute the code in `./vlchat/__main__.py`, for instance, run `sudo python3 vlchat` or the equivalent command on your machine. Administrator privileges are required for the interactive CLI only.

