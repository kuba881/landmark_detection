from dis import dis
from ntpath import join
from os import sep
from tkinter.ttk import Separator
from turtle import shape
from scipy.io import loadmat
import pandas as pd
import matplotlib.pyplot as plt
import math
import numpy as np
import os
import seaborn as sns
from mpl_toolkits import mplot3d

#source of data (python/kinect)
source='python'
num_angles=0

#name of records, which we would like to calculate-healthy
#names=['ZM001_b','ZM002_b','ZM003_b','ZM004_b','ZM005_b','ZF006_b','ZF007_b','ZM008_b','ZM009_b','ZF010_b','ZF011_b']

#name of records, which we would like to calculate-paralyzed
#names=['SM001_bal','SM002_bal','SM003_bal','SM004_bal','SM005_bal','SF006_bar','SF007_bar','SM008_bal','SM009_bal','SF010_bar','SF011_bar']

#names=['SM020_bar','SM021_bar','SM022_bar','SM023_bar','SM024_bar']

#names python
names=['ZM001_b','ZM002_b','ZM003_b','ZM004_b','ZM005_b','SM001_bal','SM002_bal','SM003_bal','SM004_bal','SM005_bal','SM006_bar','SM007_bar','SM008_bar','SM009_bar','SM010_bar']

#latest one from kinect
#names=['ZM012_b','ZM013_b','ZM014_b','ZM015_b','ZM016_b','ZM017_b','ZF018_b','ZF019_b','ZF020_b','SM012_bal','SF013_bal','SF014_bal','SF015_bal','SF016_bal','SF017_bal','SM030_bal','SF031_bal','SM032_bal','SM033_bal','SM034_bal','SM035_bal','SM040_bar','SM041_bar','SF042_bar','SF043_bar','SF044_bar','SF045_bar','SF046_bar','SM047_bar','SM048_bar','SM049_bar','SM050_bar']

#load points of interest
if source=='kinect':
    points=pd.read_csv(r'C:\Users\kuba8\Desktop\studium\points_information_selected.csv',sep=';')#kinect
    x=0
    y=1
    z=2

elif source=='python':
    points=pd.read_csv(r'C:\Users\kuba8\Desktop\studium\points_information_selected_python.csv',sep=';')#python
    x=1
    y=2
    z=3

points=[points['index_1'],points['index_2']]

#function for calcualating distance between two points
def distance(b1,b2):
    diss=math.sqrt(math.pow(b1[x]-b2[x],2)+math.pow(b1[y]-b2[y],2)+math.pow(b1[z]-b2[z],2))
    return diss

#function to calculate norm of the reference plain
def norm(a,b,c):
    ab=np.array([(b[x]-a[x]),(b[y]-a[y]),(b[z]-a[z])])
    bc=np.array([(b[x]-c[x]),(b[y]-c[y]),(b[z]-c[z])])
    n=np.cross(ab,bc)
    return n

#function for calculating koeficients of plain equations
def surface(a,b,c):
    n=norm(a,b,c)
    d=-(n[0]*b[0]+n[1]*b[1]+n[2]*b[2])
    f=[n[0],n[1],n[2],d]
    return f

#function for calculating anble between reference plain and line conecting two points
def angle(b1,b2,n):
    b12=np.array([b2-b1])

    #calculating lenght of vectors
    nor_b12=np.linalg.norm(b12)
    nor_n=np.linalg.norm(n)

    kosphi=np.dot(b12,n)/(nor_b12*nor_n)
    ang_rad=math.acos(kosphi)
    ang=180*ang_rad/math.pi-90
    return ang


if source=='python':
    for name in names:
        #get the lenght of record
        frames=len(os.listdir(join(r'C:\Users\kuba8\Desktop\studium\Python_record',name,'coordinates')))

        #prepare matrix for saving data
        mat=np.zeros(shape=[len(points[0])+1,frames-1],dtype=float)

        for i in range(1,frames):
            #load one photo from webcam
            data=pd.read_csv(join(r'C:\Users\kuba8\Desktop\studium\Python_record',name,'coordinates\slide{}.txt'.format(str(i))),delimiter='\t',header=None)
            data=data.drop(0,axis=1).transpose()

            #load time, when the photo was taken from kinect
            timeStemp=pd.read_csv(join(r'C:\Users\kuba8\Desktop\studium\Python_record',name,'times\\time{}.txt'.format(str(i))),delimiter='\t',header=None)
        
            #calculate angles for first point
            for j in range(num_angles):#8 for python
                n=norm(data[:][1],data[:][9],data[:][18])
                ang=angle(b1=data[:][points[0][j]],b2=data[:][points[1][j]],n=n)
                mat[j][i-1]=ang
        
            #calculate distance between rest of the poins
            for j in range(num_angles,len(points[0])):
                diss=distance(b1=data[:][points[0][j]],b2=data[:][points[1][j]])
                mat[j][i-1]=diss

                #include time to the last column
                mat[j+1][i-1]=timeStemp[0]

        #save calculated data to the txt file
        np.savetxt(join(r'C:\Users\kuba8\Desktop\studium\Python_record\python_data\Only_selected',name+'_data.txt'), mat)

elif source=='kinect':
    for name in names:
        #get the lenght of record
        frames=len(os.listdir(join(r'C:\Users\kuba8\MATLAB Drive\projekt oblicej\datapropouziti',name,name+'_coordinates')))

        #prepare matrix for saving data
        mat=np.zeros(shape=[len(points[0])+1,frames-1],dtype=float)

        for i in range(1,frames):
            #load one photo from kinect
            data=loadmat(join(r'C:\Users\kuba8\MATLAB Drive\projekt oblicej\datapropouziti',name,name+'_coordinates',name+'_coordinates_'+str(i)))
            data=data['model']
        
            #load time, when the photo was taken from kinect
            timeStemp=loadmat(join(r'C:\Users\kuba8\MATLAB Drive\projekt oblicej\datapropouziti',name,name+'_times',name+'_time_'+str(i)))
            
            #calculate angles for first point
            for j in range(num_angles):#8 for python
                n=norm(data[:,22],data[:,18],data[:,28])
                ang=angle(b1=data[:,points[0][j]-1],b2=data[:,points[1][j]-1],n=n)
                mat[j][i-1]=ang
        
            #calculate distance between rest of the poins
            for j in range(num_angles,len(points[0])):
                diss=distance(b1=data[:,points[0][j]-1],b2=data[:,points[1][j]-1])
                mat[j][i-1]=diss

                #include time to the last column
                mat[j+1][i-1]=timeStemp['timeStamp']

        #save calculated data to the txt file
        np.savetxt(join(r'C:\Users\kuba8\MATLAB Drive\projekt oblicej\dataPython\Only_selected_points',name+'_data.txt'), mat)
