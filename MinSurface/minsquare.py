from . import ndimvar as nv 
import numpy as np
from . import geometry as geom
from . import triangulation as tr
import math

class MinimalSquare(nv.NdimVar):
    def __init__(s,T,eps=0.1):
        s.T=T
        s.eps=eps
        s.alpha=1.0
        s.rho=1.0
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
                
                ar+=norm.P*t.square()*s.rho
            CC[j]=ar
            j+=1
        s.CC=CC	
    def tension(s,alpha):
        s.alpha=alpha
    def density(s,rho):
        s.rho=rho
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
        return s.alpha*grad
		
class CapillarSurface(MinimalSquare):
    def __init__(s,T,eps=0.1):
        MinimalSquare.__init__(s,T)

    def create_subLin(s):
        s.sublin=True
        s.T.createNT()
        n=s.T.N
        m=n-len(s.T.Bnd)
        CC=np.zeros(shape=(n,3),dtype=float)
        j=0
        for i in range(n):
            # if i in s.T.Bnd:
                # CC[j]=np.zeros(shape=(3,),dtype=float)
                # j+=1
                # continue
            ar=np.zeros(shape=(3,),dtype=float)
            for tk in s.T.NT[i]:
                t=s.T.triangle(tk)
                norm=t.normal()
                
                ar+=norm.P*t.square()*s.rho#*s.Phi(t.center())
            CC[j]=ar
            j+=1
        s.CC=CC	

    def Phi(s,x):
        return s.rho*(1.0+9.8*x[2])
		
    def X(s,x):
		
        T=s.T
        P=s.T.P
        n=s.T.N
        m=s.T.N-len(s.T.Bnd)
        grad=np.ndarray(shape=(n,3),dtype=float)
        for i in range(0,s.T.N):
            trk=s.T.NT[i]
            gd=np.zeros(shape=(3,),dtype=float)
            ar=np.zeros(shape=(3,),dtype=float)
            for k in trk:
                l=0
                for v in s.T.T[k]:
                    if i==v: 
                        i1=l
                    l+=1

                Tr=s.T.triangle(k)
                norm=Tr.normal()
                nn=Tr.orthos()
				
                gd+=nn[i1]
                ar+=norm.P*Tr.square()*s.Phi(Tr.center())
            if i in s.T.Bnd : 
                grad_e=np.zeros(shape=(3,),dtype=float)
                ########
                beta=0#math.sqrt(2)/2
                e3=np.zeros(shape=(3,),dtype=float)
                e3[2]=1
                p0=s.T.P[i].P
                p1=s.T.P[s.T.NE[i][0]].P
                p2=s.T.P[s.T.NE[i][1]].P
                l1=p0-p1
                l2=p0-p2
                z1=0.5*(p0+p1)
                z2=0.5*(p0+p2)
                d1=math.sqrt(l1.dot(l1))
                d2=math.sqrt(l2.dot(l2))
                grad_e=beta*(z1[2]*l1.dot(e3)*e3/d1+z2[2]*l2.dot(e3)*e3/d2+0.5*e3*(d1+d2))
                grad[i]=grad_e+s.alpha*gd.dot(e3)*e3+ar.dot(e3)*e3
                #grad[i]=beta*(0.5*e3*(d1+d2))
                #########
                
            else : grad[i]=s.alpha*gd+ar
        #print(grad)		
        return grad