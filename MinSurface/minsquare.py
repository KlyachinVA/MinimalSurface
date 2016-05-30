from . import ndimvar as nv 
import numpy as np
from . import geometry as geom
from . import triangulation as tr
import math

class MinimalSquare(nv.NdimVar):
    def __init__(s,T,eps=0.1):
        s.T=T
        s.eps=eps
        s.sublin=False
    def create_subLin(s):
        s.sublin=True
        s.T.createNT()
        n=s.T.N
        m=n-len(s.T.Bnd)
        CC=np.zeros(shape=(n,3),dtype=float)
        j=0
        for i in range(n):
            if i in s.T.Bnd:
                CC[j]=np.zeros(shape=(3,),dtype=float)
                j+=1
                continue
            ar=np.zeros(shape=(3,),dtype=float)
            for tk in s.T.NT[i]:
                t=s.T.triangle(tk)
                norm=t.normal()
                
                ar+=norm.P*t.square()
            CC[j]=ar
            j+=1
        s.CC=CC	
    def X(s,x):
		
        T=s.T
        P=s.T.P
        n=s.T.N
        m=s.T.N-len(s.T.Bnd)
        grad=np.ndarray(shape=(n,3),dtype=float)
        for i in range(0,s.T.N):
            trk=s.T.NT[i]
            gd=np.zeros(shape=(3,),dtype=float)
            for k in trk:
                l=0
                for v in s.T.T[k]:
                    if i==v: 
                        i1=l
                    l+=1

                Tr=s.T.triangle(k)
                nn=Tr.orthos()
				
                gd+=nn[i1]
            if i in s.T.Bnd : grad[i]=[0,0,0]#np.zeros(shape=(3,),dtype=float)
            else : grad[i]=gd
        #print(grad)		
        return grad