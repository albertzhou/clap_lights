Control Lights through clapping twice project.

Uses computer microphone to detect claps. If two claps are detected in the configured time period, computer sends a signal over serial to a microcontroller to toggle a relay controlled light or other object.

INSTRUCTIONS:

1. Adjust sensitivity parameters according to specific microphone set up.
2. Hook up microcontroller via USB to computer and select the correct com port for communication.
3. Flash microcontroller with provided code (.ino file).
4. Run Python3 audioprocessor.py

IN PROGRESS:
- Frequency based filter + high pass filter on audio for better noise rejection
- command line arguments for different modes (i.e. mode with visualizer enabled)
- Wiring diagram and hardware pinout.
- Convert to completely embedded system.
