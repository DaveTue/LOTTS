%Matlab interface script tests
set_param('dummy_test','StartTime','10','StopTime','40','FixedStep','0.5')
set_param('dummy_test', 'EnablePacing', 'on', 'PacingRate', 0.8) 
set_param('dummy_test','SimulationCommand','start')
set_param('dummy_test','SimulationCommand','pause')