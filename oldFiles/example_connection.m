%example of model modification
%erase as many lines as inputs are 
%%%
%delete_line('Gain_model_wI','temp_in/1','Gain/1')
%add_line('Gain_model_wI','interface/1','Gain/1','autorouting','on')

%delete_line('Gain_model_wI','Gain/1','temp_out/1')
%add_line('Gain_model_wI','Gain/1','interface/1','autorouting','on')

%delete_line('Gain_model_wI','Gain1/1','gas_1/1')
%add_line('Gain_model_wI','Gain1/1','interface/2','autorouting','on')

%delete_line('Gain_model_wI','gas_in/1','Gain1/1')
%add_line('Gain_model_wI','interface/2','Gain1/1','autorouting','on')


%delete_line('Gain_model_wI','In1/1','Out1/1')
%add_line('Gain_model_wI','interface/3','interface/3','autorouting','on')





%create all lines


%load_system('Gain_model_WI')

% interface_block = get_param('Gain_model_wI/interface','PortConnectivity');
% class(interface_block)
% positon = interface_block.Position;
% class(positon)
% in1 = interface_block(1).Position;
% class(in1)
% in2 = interface_block(2).Position;
% in3 = interface_block(3).Position;
% out1 = interface_block(4).Position;
% out2 = interface_block(5).Position;
% out3 = interface_block(6).Position; 
% name1= 'parangacutimimicuaro'
% size_text = strlength(name1)*5; % solo para output, inputs sin multiplicacion
% input1 = Simulink.Annotation(gcs,name1);
% in1 = [in1(1)-size_text,in1(2)];
% input1.Position = in1;

%%% change size and position of block
load_system('Gain_model_wI')
names = getfullname(Simulink.findBlocks('Gain_model_wI'));
s =size(names);
most_leftPos = 0;
for i = 1:s(1)
    pos = get_param(names(i),'Position');
    x_pos = pos{1}(1);
    if (x_pos > most_leftPos)
        most_leftPos = x_pos;
        item = names(i);
    end
end

left_block = get_param('Gain_model_wI/interface','Position')
 position = get_param('Gain_model_wI/interface','Position')
 % position
 x = position(1) +most_leftPos 
 y = position(2)
 width = position(3)+x
 height = position(4)+y 
 set_param('Gain_model_wI/interface','Position',[x y width height])