import numpy as np
from . import geometry as geom
from . import triangulation as tr
import math

n=4
k=100

class NdimVar:
    def __init__(s,T,eps=0.1):
        s.T=T
        s.eps=eps
        s.sublin=False
    def set_sublin(s,C):
        s.sublin=True
        s.CC=C		
    def epsilon(s,k):
        return s.eps
    def proj(s,x):
        cc=0
        cx=0
        for i in range(len(s.CC)):
            cc+=s.CC[i].dot(s.CC[i])
            cx+=s.CC[i].dot(x[i])
            #x[i]=x[i]-s.CC[i]*cx/cc
        
        return x-s.CC*cx/cc
    def X(s,x):
        return x
    def create_subLin():
        pass

    def iteration(s,x,k):
        if s.sublin: 
            s.create_subLin()
            return x-s.epsilon(k)*s.proj(s.X(x))
        else:
            res=np.ndarray(shape=(len(x),3),dtype=float)
            Gr=s.X(x)
            for i in range(len(x)):
                res[i]=x[i]-s.epsilon(k)*Gr[i]
                # res[i][0]=x[i][0]-s.epsilon(k)*Gr[i][0]			
                # res[i][1]=x[i][1]-s.epsilon(k)*Gr[i][1]
                # res[i][2]=x[i][2]-s.epsilon(k)*Gr[i][2]
            return res#x-s.X(x)#s.epsilon(k)*s.X(x)


    def process(s,k,x0):
        x=s.iteration(x0,0)
        for i in range(1,k+1):
            x=s.iteration(x,i)
            for l in range(0,len(x)):
                s.T.P[l].P=x[l]
        s.vector=x
        return x





