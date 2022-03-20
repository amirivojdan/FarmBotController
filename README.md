# FarmBotController
 Python software to directly control FarmBot from PC.
 
##	Project Objective and Solution

Due to the inconsistency of the connection over the internet, restrictions for research purposes, and the fact that existing libraries based on web services increases complexity of the software, implementing an independent software library to communicate and control the motors, sensors and other peripherals directly, seems inevitable.
Accordingly, a Python software is developed for basic operations on Farmbot.

It is contained of four python classes as follows:

-	**CommandBus.py**
This class is responsible for providing a full-duplex serial connection based on  PySerial module. It helps to hide all details about the serial connection configurations, encodings(ASCII)/decodings(ASCII), and the required CR+LF special characters needed for proper data transmition.
-	**CommandGenerator.py**
Because writing G-Code commands in plain text format is not only time-consuming but also a bug prone process, Command Generator class is defined to perform all those details behind the seen. It provides corresponding clean and intuitive methods for each of the commands available in G-Code table provided by the manufacturer.
-	**FarmBotStatus.py**
This class is responsible for fetching the raw packets from the CommandBus object and interepet them according to the documents available on manufacturer’s Github. The last position of the motors and internal variables are also available and updated by a thread running in specific frequency provided in its constructor. 
Note: It is important to be notified about the initialization status of the firmware. Otherwise if the Arduino receives commands it will 
-	**Farmbot.py**
The top level class containing an instance of the other classes inside, and also a thread running to transmit the user commands to the Arduino. Note that the Commandbus object is shared between the Farmbotstatus object and the Farmbot object. Since the connection is full duplex meaning reading and writing is done on separate lines simultaneously, there will be no concerns about any possible race conditions between the running threads.

