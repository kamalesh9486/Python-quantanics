import time
from threading import Thread
from datetime import datetime
import logging
import traceback
import random
#from callback_instance import Gpio_Callbacks,Event_State,BLL


filename ="app_log/"+"test_log"+str(time.time())+".log"
logging.basicConfig(filename=filename,
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)




class Machine():

    def check_status(self,callbacks,event_state,machine_power_pin,mold_close_pin,cycle_start_pin,eject_pin,my_test_data):
        event_state.update_event_state({"MACHINE_POWER_STATUS": False}) # p_stage = 0
        event_state.update_event_state({"CYCLE_START_STATUS": False}) # c_stage = 0
        event_state.update_event_state({"MOLD_CLOSE_STATUS": False}) # m_stage = 0
        event_state.update_event_state({"EJECT_STATUS": False}) # e_stage = 0
        p_event = ""
        c_event = ""
        while True: 

            if event_state.get_event_state("MACHINE_POWER_STATUS") == False:
                ct = datetime.now()
            
                ct = ct.strftime("%Y-%m-%d %H:%M:%S")
                while True:
                    if(my_test_data['power_status']== False):
                        event_state.update_event_state({"CYCLE_START_STATUS": True})
                        c_event = "Machine ON" # But due to this line multiple time Machine OEE Data will be send incase of power fluctuations
                        p_event = c_event
                        #print("Power ON")
                        logger.info(f"PIN Status for Machine {self.get_id()} Power ON")
                        break
                    else:
                        c_event = "Machine OFF"
                        if c_event != p_event:
                            p_event = c_event
                            event_state.update_data_state({
                                "id":int(time.time()),
                                "machine_status": False,
                                "downtime_status": True,
                                "status": event_state.get_lable_state("MACHINE_OFF"),
                                "shot_status": 0,
                                "machine_id":self.get_id(),
                                "gateway_time":ct,
                            })
                            #BLL.publish_event(event_state.get_data_state(), "test/new/events")
                            #print("Power OFF")
                            logger.info(f"Event Status for Machine {self.get_id()} Power OFF")
                        else:
                            pass
            if event_state.get_event_state("CYCLE_START_STATUS") == True:
                flag = 0
                ct = datetime.now()
                ct = ct.strftime("%Y-%m-%d %H:%M:%S")
                while True:
                    if(my_test_data['cycle_start_status']== False):
                        event_state.update_event_state({"CYCLE_START_STATUS": False})
                        event_state.update_event_state({"MOLD_CLOSE_STATUS": True})
                        #print("Cycle Start ON")
                        logger.info(f"PIN Status for Machine {self.get_id()} Cycle Start ON")
                        break
                    elif(my_test_data['power_status'] == True): # This will only execute in case of Machine OFF after Inactive state
                        break
                    elif(flag == 0):
                        state = my_test_data['cycle_start_status']
                        for x in range(self.total_duration):
                            state = my_test_data['cycle_start_status']
                            if state == False:
                                event_state.update_event_state({"CYCLE_START_STATUS": False})
                                event_state.update_event_state({"MOLD_CLOSE_STATUS": True})
                                #print("Cycle Start ON")
                                logger.info(f"PIN Status for Machine {self.get_id()} Cycle Start ON")
                                break
                            elif(my_test_data['power_status'] == True):
                                state = False
                                flag = 0
                                break
                            time.sleep(self.delay_s)
                        if state == True:
                            c_event = "Inactive"
                            p_event = c_event
                            flag = 1
                            event_state.update_data_state({
                                "id":int(time.time()),
                                "machine_status": True,
                                "downtime_status": True,
                                "status": event_state.get_lable_state("INACTIVE"),
                                "shot_status": 0,
                                "machine_id":self.get_id(),
                                "gateway_time":ct,
                            })
                            #BLL.publish_event(event_state.get_data_state(), "test/new/events")
                            #print("Inactive")
                            logger.info(f"Event Status for Machine {self.get_id()} Inactiveh")
                    if flag == 0:
                        break

            if event_state.get_event_state("MOLD_CLOSE_STATUS") == True:
                flag = 0
                ct = datetime.now()
                ct = ct.strftime("%Y-%m-%d %H:%M:%S")
                while True:
                    if(random.choice([True, False]) == False):
                        event_state.update_event_state({"MOLD_CLOSE_STATUS": False})
                        event_state.update_event_state({"EJECT_PIO.input(machine_power_pin)STATUS": True})
                        #print("Mold Close ON")
                        logger.info(f"PIN Status for Machine {self.get_id()} Mold Close ON")
                        break
                    elif(my_test_data['power_status'] == True): # This will only execute in case of Machine OFF after Inactive state
                        break
                    elif(flag == 0):
                        state = my_test_data['mold_status']
                        for x in range(self.total_duration):
                            state = my_test_data['mold_status']
                            if state == False:
                                event_state.update_event_state({"MOLD_CLOSE_STATUS": False})
                                event_state.update_event_state({"EJECT_STATUS": True})
                                #print("Mold Close ON")
                                logger.info(f"PIN Status for Machine {self.get_id()} Mold Close ON")
                                break
                            elif(my_test_data['power_status'] == True):
                                state = False
                                flag = 0
                                break
                            time.sleep(self.delay_s)
                        if state == True:
                            c_event = "Inactive"
                            p_event = c_event
                            flag = 1
                            event_state.update_data_state({
                                "id":int(time.time()),
                                "machine_status": True,
                                "downtime_status": True,
                                "status": event_state.get_lable_state("INACTIVE"),
                                "shot_status": 0,
                                "machine_id":self.get_id(),
                                "gateway_time":ct,
                            })
                            #BLL.publish_event(event_state.get_data_state(), "test/new/events")
                            #print("Inactive")
                            logger.info(f"Event Status for Machine {self.get_id()} Inactivej")
                    if flag == 0:
                        break

            if event_state.get_event_state("EJECT_STATUS") == True:
                flag = 0
                ct = datetime.now()
                ct = ct.strftime("%Y-%m-%d %H:%M:%S")
                while True:
                    if flag == 1:
                        while True:
                            if my_test_data['ejection_status'] == False:
                                flag = 0
                                break
                            elif my_test_data['power_status'] == True:  # Machine OFF after Inactive state
                                flag = 0
                                break

                    if flag == 0:
                        state = my_test_data['ejection_status']
                        for x in range(self.total_duration):
                            state = my_test_data['ejection_status']

                            if state == False:
                                # Cycle restart logic: set `CYCLE_START_STATUS` to True and proceed with the next cycle
                                event_state.update_event_state({"EJECT_STATUS": False})
                                event_state.update_event_state({"CYCLE_START_STATUS": True})
                                c_event = "Active"
                                p_event = c_event
                                event_state.update_data_state({
                                    "id": int(time.time()),
                                    "machine_status": True,
                                    "downtime_status": False,
                                    "status": event_state.get_lable_state("ACTIVE"),
                                    "shot_status": 1,
                                    "machine_id": self.get_id(),
                                    "gateway_time": ct,
                                })
                                # Log active state and restart information
                                logger.info(f"PIN Status for Machine {self.get_id()} Ejection ON")
                                logger.info(f"Event Status for Machine {self.get_id()} Active")
                                logger.info(f"Cycle restart triggered after 'Inactive' status for Machine {self.get_id()}")
                                break

                            # Handling for inactive state if state remains True
                            if state == True:
                                c_event = "Inactive"
                                p_event = c_event
                                flag = 1
                                event_state.update_data_state({
                                    "id": int(time.time()),
                                    "machine_status": True,
                                    "downtime_status": True,
                                    "status": event_state.get_lable_state("INACTIVE"),
                                    "shot_status": 0,
                                    "machine_id": self.get_id(),
                                    "gateway_time": ct,
                                })
                                # Log inactive state and reset cycle
                                logger.info(f"Event Status for Machine {self.get_id()} Inactive detected; resetting cycle.")
                                # Break to allow the main loop to restart from 'CYCLE_START_STATUS'
                                break

                        if flag == 0:
                            break

                        time.sleep(0.5)
        
        return


###############################
    __id: str = ""
    total_duration: int = 0
    delay_s: int = 0
    def __init__(self, id, relay_configs):
        self.__id = id
        self.total_duration = 60
        self.delay_s = 1      
        try:
            event_state = Event_State()
            callbacks = Gpio_Callbacks(event_state)

            machine_power_pin = relay_configs["MACHINE_POWER_PIN"]
            mold_close_pin = relay_configs["MOLD_CLOSE_PIN"]
            cycle_start_pin = relay_configs["CYCLE_START_PIN"]
            eject_pin = relay_configs["EJECT_PIN"]

            

            logger.info(f"Machine {self.__id} initialized with pins: {relay_configs}")
            my_test_data = {}
            my_test_data['power_status'] = False
            my_test_data['cycle_start_status'] = random.choice([False])
            my_test_data['mold_status'] = random.choice([False])
            my_test_data['ejection_status'] = random.choice([True, False])

            self.monitoring_thread = Thread(target=self.check_status, args=(callbacks,event_state,machine_power_pin,mold_close_pin,cycle_start_pin,eject_pin,my_test_data))
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()

            logger.info(f"Monitoring thread for Machine {self.__id} started.")

        
        except (RuntimeError, Exception) as err:
            logger.error(f"Failed to initialize Machine {self.__id}: {err}")
            logger.info(traceback.format_exc())
            time.sleep(60)
        
        return

    def get_id(self):
        return self.__id



filename ="app_log/"+"test_log"+str(time.time())+".log"
logging.basicConfig(filename=filename,
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

class Event_State:
    def __init__(self):
        self.__event_state = {
            "MACHINE_POWER_STATUS": False,
            "CYCLE_START_STATUS": False,
            "EJECT_STATUS": False,
            "MOLD_CLOSE_STATUS": False,
        }
        self.__machine_data = {
            "id": None,
            "machine_status": None,
            "downtime_status": None,
            "status": None,
            "shot_status": None,
            "machine_id": None,
            "gateway_time": None,
        }
        self.__event_created = False
        self.__lable_data = {
            "ACTIVE": "Active",
            "INACTIVE": "Inactive1",
            "MACHINE_OFF": "Machine OFF",
            "from":"eject"
        }

    def update_event_created(self):
        self.__event_created = True
        return self.__event_created

    def get_event_created(self):
        return self.__event_created

    def update_event_state(self, keyValue):
        try:
            self.__event_state.update(keyValue)
            return self.__event_state
        except Exception as e:
            logging.error(f"Error updating event state: {e}")

    def get_event_state(self, key):
        try:
            return self.__event_state.get(key)
        except Exception as e:
            logging.error(f"Error getting event state for key {key}: {e}")

    def update_data_state(self, keyValue):
        try:
            self.__machine_data.update(keyValue)
            return self.__machine_data
        except Exception as e:
            logging.error(f"Error updating data state: {e}")

    def get_data_state(self):
        try:
            return self.__machine_data
        except Exception as e:
            logging.error(f"Error getting data state: {e}")

    def get_lable_state(self, key):
        try:
            return self.__lable_data.get(key)
        except Exception as e:
            logging.error(f"Error getting label state for key {key}: {e}")

class BLL:
    @staticmethod
    def publish_event(event_state, topic):
        try:
            payload = Mqtt.transform_payload(event_state)
            Mqtt.send(payload, topic)
            topic = DeviceStatus.replace_occurrences(topic, '/', '_', 2)
            CouchInstance.write_document(payload, topic)
        except Exception as e:
            logging.error(f"Error publishing event: {e}")

class Gpio_Callbacks:
    def __init__(self, event_state_object: Event_State):
        self.__event_state_object = event_state_object
