% Create a new Simulink model
modelName = 'TemperaturePIDControl';
new_system(modelName);
open_system(modelName);

% Add blocks
%add_block('simulink/Sources/Constant', [modelName '/Set Temperature'], ...
add_block('simulink/Sources/In1', [modelName '/Set Temperature'], ...
    'Value', '100', 'Position', [100, 50, 150, 80]); % Constant block for setpoint

add_block('simulink/Math Operations/Sum', [modelName '/Error Calculation'], ...
    'Inputs', '+-', 'Position', [200, 50, 240, 80]); % Sum block for error calculation

add_block('simulink/Continuous/PID Controller', [modelName '/PID Controller'], ...
    'Position', [300, 30, 350, 100], 'P', '1', 'I', '1', 'D', '0.1'); % PID Controller

add_block('simulink/Continuous/Transfer Fcn', [modelName '/Thermal Process'], ...
    'Numerator', '[1]', 'Denominator', '[5 1]', 'Position', [450, 50, 500, 80]); % Thermal process transfer function

add_block('simulink/Sinks/Scope', [modelName '/Temperature Scope'], ...
    'Position', [600, 50, 650, 80]); % Scope to monitor temperature

% Connect blocks
add_line(modelName, 'Set Temperature/1', 'Error Calculation/1');
add_line(modelName, 'Error Calculation/1', 'PID Controller/1');
add_line(modelName, 'PID Controller/1', 'Thermal Process/1');
add_line(modelName, 'Thermal Process/1', 'Temperature Scope/1');
add_line(modelName, 'Thermal Process/1', 'Error Calculation/2'); % Feedback loop

% Save and open the model
save_system(modelName);
open_system(modelName);
disp(['Simulink model "', modelName, '" created successfully!']);