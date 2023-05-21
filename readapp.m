%% cteci aplikace

%adresa, ve ktere je ulozena dana nahravka
adr='C:\Users\kuba8\MATLAB Drive\projekt oblicej\datapropouziti\';

%globální proměnná pro název dat
global slozka

%zjisteni stavu
if slozka(1)=='P'
    status='paralyzed';
elseif slozka(1)=='Z'
    status='healthy';
else
    status='simulated'
end

%zjisteni pohlaví
if slozka(2)=='M'
    sex='men';
else
    sex='women';
end

%identifikacni trojcisli
id=slozka(3:5);

%cvik
exercise=slozka(7:end);
switch(exercise)
    case 'b'
        exercise='baring teeth normal';
    case 'bar'
        exercise='baring teeth with right side paralyzed';
    case 'bal'
        exercise='baring teeth with left side paralyzed';
    case 'en'
        exercise='closing eyes normal';
    case 'er'
        exercise='closing eyes with right side paralyzed';
    case 'el'
        exercise='closing eyes with left side paralyzed';
end 

%pocet snimku
a=dir([adr slozka '\' slozka '_times\' slozka '_time_' '*.mat']);
frames=length(a); 
frames=num2str(frames);

%delka zaznamu
c=load([adr slozka '\' slozka '_times\' slozka '_time_' num2str(1) '.mat']);
d=load([adr slozka '\' slozka '_times\' slozka '_time_' num2str(frames) '.mat']);
time=d.timeStamp-c.timeStamp;
time=num2str(time);

%vousy
load([adr slozka '\beard.mat']);

%vek 
load([adr slozka '\age.mat']);
age=num2str(age);

%jmeno
load([adr slozka '\name.mat']);
