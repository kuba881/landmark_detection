global recBut k2 adr k sex id name beard age status exercise rgbRec text kinAdr color

addpath(kinAdr);

model = zeros(3,1347);

% counting iterations
i=0;

%creation of folder name and direction
text=[status sex sprintf('%03d', id) '_' exercise];

mkdir(adr,text);
mkdir([adr text],[text '_times']);
mkdir([adr text],[text '_coordinates']);

if rgbRec ==1
    mkdir([adr text],[text '_video']);
end

%saving information about patient into the created folder
save([adr text '\age'],'age');
save([adr text '\beard'],'beard');
save([adr text '\name'],'name');

clear status sex beard name age id exercise

%time measuring
start_time=tic;

while k==0
    % Get frames from Kinect and save them on underlying buffer
    validData = k2.updateData;
    
    % Before processing the data, we need to make sure that a valid
    % frame was acquired.
    if validData
        % Get color frame and time
        color = k2.getColor;
        timeStamp=toc(start_time);
        
        faces = k2.getHDFaces('WithVertices','true'); 
        
        %preview
        if stop ==1
            imshow(color)
        end
        
        %work only with nonempty data
        if model(1,1)~=0
            i=i+1;
            
            %switch switch in GUI
            recBut.Value='On' 
            
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            %RGB saving
            if rgbRec ==1
                save([adr text '\' text '_video\' sprintf('obr_%s',num2str(i))],'color')
            end
            %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
            
            %saving coordinates ant its time
            save([adr text '\' text '_coordinates\' text '_coordinates_' num2str(i) '.mat'],'model');
            save([adr text '\' text '_times\' text '_time_' num2str(i) '.mat'],'timeStamp');
        end
        
        %Plot face model points
        if size(faces,2) > 0
             model = faces(1).FaceModel;
        end
    end
    
    %skript end after pushing ukonit button
    pause(0.05);

    clear timeStamp validData
end