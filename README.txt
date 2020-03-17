Control Lights through clapping twice project.

Uses computer microphone to detect claps. If two claps are detected in the configured time period, computer sends a signal over serial to a microcontroller to toggle a relay controlled light or other object.

HARDWARE:
1. Teensy 2.0++ (can be used with Arduino, but connect a 10uF capacitor between reset and GND to prevent resetting when the serial port is opened)
2. Computer with microphone.

INSTRUCTIONS:

1. Adjust sensitivity parameters according to specific microphone set up.
2. Hook up microcontroller via USB to computer and select the correct com port for communication.
3. Flash microcontroller with provided code (.ino file) using Arduino IDE.
4. Run Python3 audioprocessor.py.
5. Clap twice to toggle light.

IN PROGRESS:
1. Frequency based filter + high pass filter on audio for better noise rejection
2. command line arguments for different modes (i.e. mode with visualizer enabled)
3. Wiring diagram and hardware pinout.
4. Ethernet communication instead of UART TTL
4. Convert to completely embedded processing
