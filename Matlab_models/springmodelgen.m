% MATLAB Script to create a Simulink model of a mass-spring-damper system
% The model takes force (F) as input and computes displacement (x).

% Parameters
modelName = 'MassSpringDamperModel'; % Name of the Simulink model
mass = 1; % Mass (m) in kg
springConstant = 100; % Spring constant (k) in N/m
dampingCoefficient = 10; % Damping coefficient (c) in Ns/m

% Create a new Simulink model
new_system(modelName);
open_system(modelName);

% Add blocks
% Input block (Force)
add_block('simulink/Sources/In1', [modelName, '/Force'], 'Position', [100, 100, 130, 120]);

% Sum block (to compute net force)
add_block('simulink/Math Operations/Sum', [modelName, '/Sum'], 'Position', [200, 90, 230, 140]);
set_param([modelName, '/Sum'], 'Inputs', '+-+-');

% Gain block for spring force (-kx)
add_block('simulink/Math Operations/Gain', [modelName, '/SpringForce'], 'Position', [300, 50, 350, 90]);
set_param([modelName, '/SpringForce'], 'Gain', num2str(-springConstant));

% Gain block for damping force (-cv)
add_block('simulink/Math Operations/Gain', [modelName, '/DampingForce'], 'Position', [300, 150, 350, 190]);
set_param([modelName, '/DampingForce'], 'Gain', num2str(-dampingCoefficient));

% Integrator blocks for velocity and displacement
add_block('simulink/Continuous/Integrator', [modelName, '/Velocity'], 'Position', [450, 100, 480, 130]);
add_block('simulink/Continuous/Integrator', [modelName, '/Displacement'], 'Position', [550, 100, 580, 130]);

% Gain block for acceleration (1/m)
add_block('simulink/Math Operations/Gain', [modelName, '/Acceleration'], 'Position', [400, 100, 430, 130]);
set_param([modelName, '/Acceleration'], 'Gain', num2str(1/mass));

% Output block (Displacement)
add_block('simulink/Sinks/Out1', [modelName, '/DisplacementOutput'], 'Position', [650, 100, 680, 130]);

% Connect blocks
add_line(modelName, 'Force/1', 'Sum/1');
add_line(modelName, 'Displacement/1', 'SpringForce/1');
add_line(modelName, 'SpringForce/1', 'Sum/2');
add_line(modelName, 'Velocity/1', 'DampingForce/1');
add_line(modelName, 'DampingForce/1', 'Sum/3');
add_line(modelName, 'Sum/1', 'Acceleration/1');
add_line(modelName, 'Acceleration/1', 'Velocity/1');
add_line(modelName, 'Velocity/1', 'Displacement/1');
add_line(modelName, 'Displacement/1', 'DisplacementOutput/1');

% Save and open the model
save_system(modelName);
open_system(modelName);

% Display a message
disp(['The Simulink model "', modelName, '" has been created.']);
