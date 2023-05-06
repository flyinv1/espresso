# App entry point
from os import sys, environ
from espressomanager import EspressoManager
import dotenv


dotenv.load_dotenv()

if "ENV" in environ:
    env = environ["ENV"]
else:
    print("""`ENV` flag is not set. Please select environment:
    SIM - simulated hardware with virtual infterface, no hardware required.
    PROD - deploy to espresso machine hardware.

    Exiting""")
    exit()

if __name__ == "__main__":
    if env == "SIM":

        # Do not import hardware libraries if in simulation mode.
        from simulator import simulator

        sim = simulator.Simulator()
        
        # Start the sim
        sim.start()


    if env == "PROD":

        while True:
            

        # from iocontroller import IOController

        # io = IOController()
        # manager = EspressoManager(io)

        # while True:
        #     manager.main()


