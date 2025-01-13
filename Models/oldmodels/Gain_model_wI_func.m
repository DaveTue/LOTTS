function Gain_model_wI_func(block)
% Level-2 MATLAB file S-Function for interface of the Gain_model_wI_func.

%   Developed by David Manrique
%	Last update April 17th 2023

  setup(block);
  
%endfunction

function setup(block)
  
  %% block.NumDialogPrms  = 1;
  
  %% Register number of input and output ports
  block.NumInputPorts  = 4;
  block.NumOutputPorts = 3;

  %% Setup functional port properties to dynamically
  %% inherited.
  block.SetPreCompInpPortInfoToDynamic;
  block.SetPreCompOutPortInfoToDynamic;
 
 %[init_output_loop]
 %[init_output_loop]
 %[init_output_loop]
 %[init_output_loop]
  block.InputPort(1).Dimensions        = 1;
  block.InputPort(2).Dimensions        = 1;
  block.InputPort(3).Dimensions        = 1;
  block.InputPort(4).Dimensions        = 1;
  block.InputPort(1).SamplingMode        = 'Sample';
  block.InputPort(2).SamplingMode        = 'Sample';
  block.InputPort(3).SamplingMode        = 'Sample';
  block.InputPort(4).SamplingMode        = 'Sample';
  block.InputPort(1).DirectFeedthrough = false;
  block.InputPort(2).DirectFeedthrough = false;
  block.InputPort(3).DirectFeedthrough = false;
  block.InputPort(4).DirectFeedthrough = false;
 %[end_output_loop]
 
 %[init_input_loop]
 %[init_input_loop]
 %[init_input_loop]
  block.OutputPort(1).Dimensions       = 1;
  block.OutputPort(2).Dimensions       = 1;
  block.OutputPort(3).Dimensions       = 1;
  block.OutputPort(1).SamplingMode = 'Sample';
  block.OutputPort(2).SamplingMode = 'Sample';
  block.OutputPort(3).SamplingMode = 'Sample';
% [end_input_loop] 
 
  %% Set block sample time to  ingeretance [-1 0]
  block.SampleTimes = [-1 0];
  
  %% Set the block simStateCompliance to default (i.e., same as a built-in block)
  block.SimStateCompliance = 'DefaultSimState';

  %% Register methods
  %block.RegBlockMethod('PostPropagationSetup',    @DoPostPropSetup);
  %block.RegBlockMethod('InitializeConditions',    @InitConditions);  
  block.RegBlockMethod('Outputs',                 @Output);  
  block.RegBlockMethod('Update',                  @Update);  

 %endfunction 
  %function DoPostPropSetup(block)

  %% Setup Dwork
  %block.NumDworks = 1;
  %block.Dwork(1).Name = 'x0'; 
  %block.Dwork(1).Dimensions      = 1;
  %block.Dwork(1).DatatypeID      = 0;
  %block.Dwork(1).Complexity      = 'Real';
  %block.Dwork(1).UsedAsDiscState = true;

%endfunction

%function InitConditions(block)

  %% Initialize Dwork
  %block.Dwork(1).Data = block.DialogPrm(1).Data;
  
%endfunction

function Output(block)
  
%  [init_input_loop]
%  [init_input_loop]
%  [init_input_loop]
  
  
  
  input_var_1 = evalin('base', 'temp_in');
  input_var_2 = evalin('base', 'mass_in');
  input_var_3 = evalin('base', 'vol_in');
 
 
 
  block.OutputPort(1).Data = double(input_var_1);
  block.OutputPort(2).Data = double(input_var_2);
  block.OutputPort(3).Data = double(input_var_3);
 
 
 
% [end_input_loop] 
  
%endfunction

function Update(block)

  %block.Dwork(1).Data = block.InputPort(1).Data;
  
  %[init_output_loop]
  %[init_output_loop]
  %[init_output_loop]
  %[init_output_loop]
  
  
  
  
 
 
 
 
  output_var_1 = block.InputPort(1).Data;
  output_var_2 = block.InputPort(2).Data;
  output_var_3 = block.InputPort(3).Data;
  output_var_4 = block.InputPort(4).Data;
  assignin('base','temp_out',output_var_1);
  assignin('base','mass_out',output_var_2);
  assignin('base','vol_out',output_var_3);
  assignin('base','time_out',output_var_4);
  %[end_output_loop]

%endfunction