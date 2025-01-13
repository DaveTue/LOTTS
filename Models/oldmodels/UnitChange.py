#Python_model
# import Matlab_API
# import localInterface_gen
# import intercomm_def
# import os
# import matlab.engine
# import time

class Model:
    
    def __init__(self,temperature = 32, mass = 10 , volume = 3, time = 0,
                 param = {'temp_param':15, 'mass_param':2000,'vol_param':200}) -> None:
        self.temp_in = temperature
        self.mass_in = mass
        self.vol_in = volume
        self.time = time
        self.temp_out = 0
        self.mass_out = 0
        self.vol_out = 0
        self.param = param

    
    def __str__(self):
        return 'Current state is \n temp_in = {}\n mass_in = {}\n volume_in = {}\n time = {}\n temp_out = {}\n mass_out = {}\n vol_out = {}'.format(self.temp_in,self.mass_in,self.vol_in,self.time,self.temp_out,self.mass_out,self.vol_out)

    def unit_transform(self):
        
        self.temp_out = self.temp_in + self.param['temp_param']
        if self.mass_in > 50000:
            self.mass_out = self.mass_in/self.param['mass_param'] + 100
        else:
            self.mass_out = self.mass_in + 800
        if self.vol_in > 4000:
            self.vol_out = self.vol_in/300 + 90
        self.vol_out = self.vol_in + self.param['vol_param']
        #return (self.temp_out,self.mass_out,self.vol_out)
    
    def step_increase(self):
        self.temp_in = self.temp_in
        #print(self.temp_out)
        
        self.mass_in = self.mass_in 
        self.vol_in = self.vol_in 
        #return self.temp_in,self.mass_in,self.vol_in
    
      
  