import numpy as np
import math
#from scipy import linalg
class Point:
    def __init__(s,p):
        s.P=np.array(p)
        s.n=s.P.ndim

    def cross(s,b):
        c0=s.P[1]*b.P[2]-s.P[2]*b.P[1]
        c1=s.P[2]*b.P[0]-s.P[0]*b.P[2]
        c2=s.P[0]*b.P[1]-s.P[1]*b.P[0]
        return Point([c0,c1,c2])
class NumedPoint(Point):
    def __init__(s,p,num):
        #s.P=p
        Point.__init__(s,p)
        s.num=num

class Simplex:
    def __init__(s,v):
        s.vertexes=v
    
class Side(Simplex):
    def __init__(s,e):
        Simplex.__init__(s,e)
        s.e=e
    def length(s):
        p0=(s.e[0]).P
        p1=(s.e[1]).P
        dp=p1-p0
        
        return np.sqrt(dp.dot(dp))
    def Phi(s,p):
        e1=Side([s.e[0],p])
        e2=Side([s.e[1],p])
        d1=e1.length()
        d2=e2.length()
        if(d1*d2 >0):
            sin=math.fabs(s.Delta(p))/(d1*d2)
            return math.pi-math.asin(sin)
        return 0
    def Delta(s,p):
        p0=(s.e[0]).P
        p1=(s.e[1]).P
        A=np.array([p.P-p0,p1-p0])
        return 1#linalg.det(A)

    def in_list(s,list):
        for e in list:
            p0=(s.e[0])
            p1=(s.e[1])
            q0=(e.e[0])
            q1=(e.e[1])
            if(p0.num==q0.num and p1.num==q1.num): return True
            if(p0.num==q1.num and p1.num==q0.num): return True
        return False
    def make_sides(e,v):
        n=v.n
        
        ee=[]
        for i in range(n,-1,-1):
            ei=[]
            for j in range(0,n+1):
                if(j!= i): 
                    ei.append(e.e[j])
                else: ei.append(v)
            ee.append(Side(ei))
        #print ee
        # e1=Side([e.e[0],v])
        # e2=Side([v,e.e[1]])
        return ee#[e1,e2]
    @staticmethod
    def clean(list):
        for e1 in list:
            for e2 in list:
                p10=e1.e[0]
                p11=e1.e[1]
                p20=e2.e[0]
                p21=e2.e[1]
                if(p10.num==p21.num and p11.num==p20.num):
                    list.remove(e1)
                    list.remove(e2)


class Triangle(Simplex):
    def __init__(s,A,B,C):
        s.A=A
        s.B=B
        s.C=C
        s.order=[0,1,2]
		
    def coss(s):
        A=s.A.P
        B=s.B.P
        C=s.C.P
        AB=B-A
        AC=C-A
        BC=C-B
        lab=math.sqrt(AB.dot(AB))
        lac=math.sqrt(AC.dot(AC))
        lbc=math.sqrt(BC.dot(BC))
		
        s.cosA=AB.dot(AC)*1.0/(lab*lac)
        s.cosB=-1.0*AB.dot(BC)*1.0/(lab*lbc)
        s.cosC=AC.dot(BC)*1.0/(lbc*lac)
        return [s.cosA,s.cosB,s.cosC]
    def sins(s):
        s.coss()
        s.sinA=math.sqrt(math.fabs(1.0-s.cosA**2))
        s.sinB=math.sqrt(math.fabs(1.0-s.cosB**2))
        s.sinC=math.sqrt(math.fabs(1.0-s.cosC**2))
        return [s.sinA,s.sinB,s.sinC]

    def lengths(s):
        A=s.A.P
        B=s.B.P
        C=s.C.P
        AB=B-A
        AC=C-A
        BC=C-B
        s.ab=math.sqrt(AB.dot(AB))
        s.ac=math.sqrt(AC.dot(AC))
        s.bc=math.sqrt(BC.dot(BC))
        return [s.ab,s.ac,s.bc]

    def heights(s):
        s.sins()
        s.lengths()
        s.hA=s.ac*s.sinC
        s.hB=s.ab*s.sinA
        s.hC=s.bc*s.sinB
        return [s.hA,s.hB,s.hC]

    def square(s):
        s.heights()
        return 0.5*s.hA*s.bc
    def center(s):
        A=s.A.P
        B=s.B.P
        C=s.C.P
        return (A+B+C)/3
    def orthos(s):
        A=s.A.P
        B=s.B.P
        C=s.C.P
        AB=B-A
        AC=C-A
        BC=C-B
        s.sins()
        s.lengths()
        s.nab=(AC*s.ab/s.ac-s.cosA*AB)/s.sinA
        s.nac=(-BC*s.ac/s.bc+s.cosC*AC)/s.sinC
        s.nbc=(-AB*s.bc/s.ab-s.cosB*BC)/s.sinB
        return [s.nbc,s.nac,s.nab]
    def normal(s):
        A=s.A.P
        B=s.B.P
        C=s.C.P
        AB=Point(B-A)
        AC=Point(C-A)
        DD=AB.cross(AC)
        dd=math.sqrt(DD.P.dot(DD.P))
        DD.P=DD.P/dd
        return DD

    def normal_square(s):
        A=s.A.P
        B=s.B.P
        C=s.C.P
        AB=Point(B-A)
        AC=Point(C-A)
        DD=AB.cross(AC)
        return DD

    def OC(s):
        A=s.A.P
        B=s.B.P
        C=s.C.P
        BA=B-A
        CB=C-B
        CA=C-A
        
        s.orthos()
        
        
        O=A+0.5*(BA+(CB.dot(CA)/CA.dot(s.nab))*s.nab)
        OP=Point(O)
        s.O=OP
        return OP


		


