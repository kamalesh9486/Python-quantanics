from test import Machine
import time



if __name__=="__main__":
     machine = [
        Machine(1, {"MACHINE_POWER_PIN" : 23, "MOLD_CLOSE_PIN" : 4, "EJECT_PIN" : 17,"CYCLE_START_PIN" : 18}),
        Machine(2, {"MACHINE_POWER_PIN" : 27, "MOLD_CLOSE_PIN" : 10, "EJECT_PIN" : 9,"CYCLE_START_PIN" : 22}),
        Machine(3, {"MACHINE_POWER_PIN" : 11, "MOLD_CLOSE_PIN" : 5, "EJECT_PIN" : 6,"CYCLE_START_PIN" : 0}),
        Machine(4, {"MACHINE_POWER_PIN" : 13, "MOLD_CLOSE_PIN" : 26, "EJECT_PIN" : 19,"CYCLE_START_PIN" : 21}),
        Machine(5, {"MACHINE_POWER_PIN" : 20, "MOLD_CLOSE_PIN" : 1, "EJECT_PIN" : 12,"CYCLE_START_PIN" : 16}),
        Machine(6, {"MACHINE_POWER_PIN" : 7, "MOLD_CLOSE_PIN" : 25, "EJECT_PIN" : 24,"CYCLE_START_PIN" : 8}),
    ]

while True:
        time.sleep(1)
