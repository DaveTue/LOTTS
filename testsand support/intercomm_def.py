#Intercomm_def
import sys
import matlab.engine
import time
import Comm

class intercomm:
    def __init__(self, components=[object]) -> None:
       self.components = components
       self.relationships = []
       self.connections = []
       self.ports = {}

    def __str__(self) -> str: #stil need fixing

        #need some correction for the msg connections and msg relationships
        component_text = ''
        if self.components == []:
            msg_components = 'This system is still empty'
            msg_relationships = '' 
            msg_connections = ''
        else:
            
            for component in self.components:
                component_text= component_text + component.modelName + '\n'
            msg_components = " The components of the system are:\n " + component_text
            if self.relationships == []:
                msg_relationships = 'This system has not defined any relationshis among components'
            else:
                msg_relationships = 'The relationship between components are: ' + self.relationships
            if self.connections ==[]:
                msg_connections = "This system  has no connections defined"
            else:
                msg_connections = 'The connections of the system are: ' + self.connections
        #return (msg_components + '\n' + msg_relationships +'\n' + msg_connections)
        return (msg_components)# to avoid errors only return msg components later fix other messages
    def port_detect(self):
        '''
        Detect all possible ports in the system and generate the system port objects (sys_port)
        '''
        for component in self.components:
            modelName = component.name
            print("For {} the detected ports are:".format(component.name))
            for input in component.inputs:
                port = sys_port(component,input)
                key = modelName + ':'+port.name
                self.ports[key] = port
                print(" Input port name {}".format(key))
            for output in component.outputs:
                port = sys_port(component,output)
                key = modelName + ':'+port.name
                self.ports[key] = port
                print(" Output port name {}".format(key))
    
    def communication(self, src_port= object, src_val = 0 ,dst_port= object):
        src_name = src_port.name
        val = src_port.model.get_output(src_name)
        
        print('For model {} the output {} value is {}'.format(src_port.model.modelName,src_name,val))
        dst_name = dst_port.name
        dst_port.model.set_input(dst_name, val)
        #print('For model {} the input {} value is {}'.format(dst_port.model.modelName,dst_name,val))
            
    def def_connection(self,source = object, destination = object ):
        '''
        Define one connection each time by defining source and destination of the connection
        It also defines the relationship
        '''
        connection ={}
        if source.direction != 'out' or destination.direction != 'in':
            print('The source must be an output of a model and/or the destination must be an input of a model')
        else: 
            connection['src'] = source
            connection['dst'] = destination
            id_src = source.model.modelName +':'+source.name 
            id_dst = destination.model.modelName +':'+destination.name
            
            self.connections.append(connection)
            print('Connection generated:' + id_src + "->" + id_dst)

class sys_port:
    def __init__(self,model = object,name = 'port' )-> object:
        self.model = model
        self.name = name
        if name in model.inputs:
            self.direction = "in"
            self.index = model.inputs.index(name)
        elif name in model.outputs:
            self.direction = 'out'
            self.index = model.outputs.index(name)
    def __str__(self) -> str:
        return '(model,name,direction)=('+ self.model.modelName + ','+self.name+','+self.direction+')'
    
class execution:
    def __init__(self, models=[],triggers =[]) -> None:
        self.models = models
        self.triggers = triggers

    def continous(self,models =[],time_end = 30, system = object):
        models[0].initialize_model()
        for connection in system.connections:
            modelName = connection['src'].model.modelName
            if modelName == models[0].modelName:
                src_val = models[0].get_output(connection['src'].name)
                system.communication(connection['src'],src_val,connection['dst'])
            #system.communication(src,val,dst)
        
        print(models[0].get_status())
        
        while models[0].get_status() != ('stopped' or 'terminating'):
            models[1].resume()
            
            # for connection in system.connections:
                
            #     system.communication(connection['src'],src_val,connection['dst'])

            for connection in system.connections:
                if connection['src'].name in models[1].outputs and connection['src'].model.modelName == models[1].modelName:
                    system.communication(connection['src'],src_val,connection['dst'])
            
            #time = 0
            models[0].resume()
            #print('\n')
            for connection in system.connections:
                if connection['src'].name in models[0].outputs and connection['src'].model.modelName == models[0].modelName:
                    system.communication(connection['src'],src_val,connection['dst'])
            print('\n')
            time.sleep(1)

class execution2:
    def __init__(self, models=[],triggers =[]) -> None:
        self.models = models
        self.triggers = triggers
    def initialize(self,models =[],time_end = 30, system = object)-> str:
        """_summary_
        this method initialize all the models contained in this execution area

        Returns:
            str: _description_ returns the states of the models 
        """
        for model in models:
            # model.initialize_model2()
            model.initialize()
    def continous(self,models =[],time_end = 30, system = object):
        # models[0].initialize_model()
        for connection in system.connections:
            modelName = connection['src'].model.modelName
            if modelName == models[0].modelName:
                src_val = models[0].get_output(connection['src'].name)
                system.communication(connection['src'],src_val,connection['dst'])
            #system.communication(src,val,dst)
        
        print(models[0].get_status())
        
        while models[0].get_status() != ('stopped' or 'terminating'):
            models[1].resume()
            
            # for connection in system.connections:
                
            #     system.communication(connection['src'],src_val,connection['dst'])

            for connection in system.connections:
                if connection['src'].name in models[1].outputs and connection['src'].model.modelName == models[1].modelName:
                    system.communication(connection['src'],src_val,connection['dst'])
            
            #time = 0
            models[0].resume()
            #print('\n')
            for connection in system.connections:
                if connection['src'].name in models[0].outputs and connection['src'].model.modelName == models[0].modelName:
                    system.communication(connection['src'],src_val,connection['dst'])
            print('\n')
            time.sleep(1)
