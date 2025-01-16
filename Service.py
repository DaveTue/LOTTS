#DT_sys
import Comm
import exeAreas
import GlOb
import time

import threading

class MainManager:
    def __init__(self, exeAreas = [], globals = None, appTime = None):
        self.threads = []
        self.exeAreas = exeAreas
        self.globals = globals
        self.appTime = appTime
        self.globals.add_appTime(self.appTime)
    
         
    def startService(self):
        """Start the execution of areas using different threads in each area"""
        
        print('---------------------------------------------')
        print(f"Service execution has started")
        print('---------------------------------------------')
        self.initAreas()
        self.appTime.re_startApp()
        for area in self.exeAreas:
            self.start_thread(target=self.areaExec, args=(area,))  # Pass the method reference and the area as an argument
    
    def start_thread(self, target, args=()):
        thread = threading.Thread(target=target, args=args, daemon=True)
        self.threads.append(thread)
        thread.start()
    
    def initAreas(self):
        """Initialize all the areas components
        """
        for area in self.exeAreas:
            print('---------------------------------------------')
            print(f"{area.name} has been initialized")
            print('---------------------------------------------')
            area.initialize()
    
    def areaExec(self,area)->None:
        starttrigg = area.startTrigger
        iter = 0
        while  self.globals.stopApp == False:
            if starttrigg.evaluate() == True and iter<6:
            # if starttrigg.evaluate() == True or iter>6:
                print('\n')
                print('+++++++++++++++++++++++++++++++++++++++++++++')
                print(f"{area.name} has started its execution")
                print('+++++++++++++++++++++++++++++++++++++++++++++')
                area.execute()
                iter += 1
                print('+++++++++++++++++++++++++++++++++++++++++++++')
                print(f"{area.name} has finished its execution")
                print('+++++++++++++++++++++++++++++++++++++++++++++')
                time.sleep(0.5)
    def join_threads(self):
        for thread in self.threads:
            thread.join()

    
    
    
    
# Example usage
# def example_task(name, duration):
#     print(f"Thread {name} starting")
#     time.sleep(duration)
#     print(f"Thread {name} finished")

# if __name__ == "__main__":
#     manager = ThreadManager()
#     manager.start_thread(example_task, "A", 2)
#     manager.start_thread(example_task, "B", 4)
#     manager.start_thread(example_task, "C", 1)
    
#     manager.join_threads()
#     print("All threads have finished")


                 


                 
class Comp_manager:
    
    COMPONENT_TYPES = {'sen': 'Sensor', 'mod': 'Model', 'op': 'Operation', 'agg': 'Aggreggator',
                       'dup': 'Dupplicator','spl': 'Splitter','conn': 'Connector','swi': 'Switch', 
                       'inp': 'Input port', 'outp': 'Output port' }
    
    def __init__(self, service_name = "name") -> None:
        self.service_name = service_name
        self.components = {'sen': [], 'mod': [], 'op': [], 'agg': [],
                       'dup': [],'spl': [],'conn': [],'swi': [], 
                       'inp': [], 'outp': [] }
        self.comp_names = {}
        
    def component_agreggate(self, comp_name = 'name', compt_type = 'mod'):
        '''
        Aggreggates components of the whole system, generate a unique ID and correlates the ID with 
        a component name (names can be the same between components, but not IDs)
        we assume that 2 components of the same type do not have the same name, 
        otherwise problems might rise
        '''
        comp_list = self.components[compt_type]
        comp_ID = str(compt_type) + str(len(comp_list) + 1)
        
        self.comp_names[comp_ID] = comp_name
        self.components[compt_type].append(comp_ID)
        #generate the component object
        # comp_ID = DSL_semantics.Component(comp_name, comp_ID)
