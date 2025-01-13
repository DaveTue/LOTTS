#testing_script
import Matlab_API
import localInterface_gen
import intercomm_def 
import os
import py_units_model
import inspect

# directory = os.getcwd() + '\\' + 'Matlab_models'
# #directory = os.getcwd()
# print (directory)
# model_name_original = 'Gain_model'
# # model = Matlab_API.simulink(modelName = model_name_original, directory = directory)
# # model.interface_gen()

# model_name_2 = 'Time_model'
# model2 = Matlab_API.simulink(model_name_2,directory)
# model2.interface_gen()

# system = intercomm_def.intercomm([])
# print(system)

model_py = py_units_model.UnitChange(temperature=40,mass = 4000,volume = 50, time = 10)
print(model_py)
model_py.unit_transform()
model_py.step_increase()
print(model_py)

members=[]
for i in inspect.getmembers(model_py):
    members.append(i)
print(len(members))
# signature_1 = inspect.signature(model_py.step_increase)
# signature_2 = inspect.signature(model_py.unit_transform)
# print(signature_1)
# print(signature_2)
print(type(members[0]))
print(model_py.__dir__)
variables =model_py.__dict__
attributes = []
for var in variables.keys():
    #print (var)
    attributes.append(var)
#print(dir(model_py))
# elements =[attr for attr in  model_py.__dict__ if callable(getattr(model_py, attr))]
# print(elements)
# methods = [func for func in  inspect.getmembers(model_py,inspect.isroutine) if func not in {'__init_subclass__', '__subclasshook__'} ]
# print(methods)
method_list = [method for method in dir(model_py) if method.startswith('__') is False and method not in attributes ]
print(method_list)
print(attributes)
