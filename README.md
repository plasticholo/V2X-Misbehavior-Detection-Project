# V2X-Misbehavior-Detection-Project



\# V2X Misbehavior Detection



This project simulates and detects misbehavior in Vehicle-to-Everything (V2X) communication using \*\*SUMO/Veins\*\* and \*\*Python\*\*.



\## What It Does

\- Injects misbehavior into a SUMO traffic simulation:

&nbsp; - \*\*Position Spoofing\*\* (vehicle jumps to a far location)

&nbsp; - \*\*Sybil Attack\*\* (multiple fake vehicles at the same spot)

&nbsp; - \*\*Ghost Vehicles\*\* (vehicles outside of valid lanes)

\- Detects these events in real time using TraCI and prints alerts to the terminal.



\## Requirements

\- SUMO + Veins (or Instant Veins VM)

\- Python 3 with `traci` module



\## How to Run

1\. Start SUMO with two clients:

&nbsp;  ```bash

&nbsp;  sumo-gui -c erlangen.sumo.cfg --num-clients 2

2\. Run the attack controller:

&nbsp;  python3 attack\_controller.py

3\. Run the misbehavior detection:

&nbsp;  python3 misbehavior\_detection.py

