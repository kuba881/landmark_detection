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
#name of records, which we would like to calculate-healthy
#names=['ZM001_b','ZM002_b','ZM003_b','ZM004_b','ZM005_b','ZF006_b','ZF007_b','ZM008_b','ZM009_b','ZF010_b','ZF011_b']

#name of records, which we would like to calculate-paralyzed
names=['SM001_bal','SM002_bal','SM003_bal','SM004_bal','SM005_bal','SF006_bar','SF007_bar','SM008_bal','SM009_bal','SF010_bar','SF011_bar']

#load points of interest
points=pd.read_csv(r'C:\Users\kuba8\Desktop\studium\points_informationA.csv',sep=';')
points=[points['index_1'],points['index_2']]

#function for calcualating distance between two points
def distance(b1,b2):
    diss=math.sqrt(math.pow(b1[0]-b2[0],2)+math.pow(b1[1]-b2[1],2)+math.pow(b1[2]-b2[2],2))
    return diss

#function to calculate norm of the reference plain
def norm(a,b,c):
    ab=np.array([(b[0]-a[0]),(b[1]-a[1]),(b[2]-a[2])])
    bc=np.array([(b[0]-c[0]),(b[1]-c[1]),(b[2]-c[2])])
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


for name in names:
    #get the lenght of record
    frames=len(os.listdir(join(r'C:\Users\kuba8\MATLAB Drive\projekt oblicej\datapropouziti',name,name+'_coordinates')))

    #prepare matrix for saving data
    mat=np.zeros(shape=[len(points[0])+1,frames-1],dtype=float)

    for i in range(1,frames):
        #load one photo
        data=loadmat(join(r'C:\Users\kuba8\MATLAB Drive\projekt oblicej\datapropouziti',name,name+'_coordinates',name+'_coordinates_'+str(i)))
        data=data['model']
        
        #load time, when the photo was taken
        timeStemp=loadmat(join(r'C:\Users\kuba8\MATLAB Drive\projekt oblicej\datapropouziti',name,name+'_times',name+'_time_'+str(i)))

        #calculate angles for first 12 points
        for j in range(0,12):
            n=norm(data[:,22],data[:,18],data[:,28])
            ang=angle(b1=data[:,points[0][j]-1],b2=data[:,points[1][j]-1],n=n)
            mat[j][i-1]=ang

        #calculate distance between rest of the poins
        for j in range(12,len(points[0])):
            diss=distance(b1=data[:,points[0][j]-1],b2=data[:,points[1][j]-1])
            mat[j][i-1]=diss

            #include time to the last column
            mat[j+1][i-1]=timeStemp['timeStamp']

    #save calculated data to the txt file
    np.savetxt(join(r'C:\Users\kuba8\MATLAB Drive\projekt oblicej\dataPython',name+'_data.txt'), mat)
