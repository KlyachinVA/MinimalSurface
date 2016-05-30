import numpy as np
from . import geometry as geom
import re
class Triangulation:
    def __init__(s,P=[],T=[],Bnd=[]):
        s.P=P
        s.T=T
        s.N=len(P)
        s.M=len(T)
        s.Bnd=Bnd
    def add(s,e,v):
        s.T.append([e.e[0].num,e.e[1].num,v.num])
    def find_edge(s,te):
        return te([s.P[1],s.P[0]])
    
    def createNT(s):
        s.NT=[[] for p in range(0,s.N)]
        for i in range(0,s.M):
            for k in s.T[i]:
                s.NT[k].append(i)
	

			

    def triangle(s,k):
        A=s.P[s.T[k][0]]
        B=s.P[s.T[k][1]]
        C=s.P[s.T[k][2]]
        Tr=geom.Triangle(A,B,C)
        return Tr

    def get_triangles(s,k,j):
        trk=s.NT[k]
        trngls=[]
		
        for i in trk:
            if j in s.T[i]:
                trngls.append(i)
        if len(trngls)!=0:
			
            return trngls
        else:
            return None

    def save_obj(s,fname):
        file=open(fname,"w")
        n=(s.P[0]).n
        
        for p in s.P:
            if(n==1): z=0
            else: z=p.P[2]
            file.write("v "+str(p.P[0])+" "+str(p.P[1])+" "+str(z)+"\n")
        file.write("\n\n")
        for face in s.T:
            file.write("f "+str(face[0]+1)+" "+str(face[1]+1)+" "+str(face[2]+1)+"\n")
        file.close()
    def save_obj_points(s,fname,p):
        file=open(fname,"w")
        for pi in p:
            file.write("v "+str(pi[0])+" "+str(pi[1])+" "+str(pi[2])+"\n")
        file.write("\n\n")
        for face in s.T:
            file.write("f "+str(face[0]+1)+" "+str(face[1]+1)+" "+str(face[2]+1)+"\n")
        file.close()
				
    def find_vertex(s,e):
        min=None
        q=None
        for v in s.P:
            
            d=e.Delta(v)
            if(d>0):
                min=e.Phi(v)
                q=v
                break
        if q==None: return None
        for v in s.P:
            d=e.Delta(v)
            phi=e.Phi(v)
            if(d>0 and min>phi): 
                q=v
                min=phi
        return q

	
    def triangulate(s,TypeEdge):
        
        e0=s.find_edge(TypeEdge)
    
        list_edges=[]
        list_edges.append(e0)
    
        while(len(list_edges)>0):
            temp_list=[]
            
            for e in list_edges:
            
                v=s.find_vertex(e)
            
                if v!= None : 
                    s.add(e,v)
                    sides=geom.Side.make_sides(e,v)
                    for side in sides:
                        if(not( side.in_list(list_edges))): temp_list.append(side)
                
            list_edges=temp_list
            TypeEdge.clean(list_edges)
        
        return s

    def load(s,fname):
        f=open(fname)
        text=f.readlines()
        P=[]
        T=[]
        reg=re.compile(r" ([-+0-9.]+)")
        for line in text:
            parts=reg.findall(line)
            if(line[0]=='v' and line[1]!='n'): P.append(geom.Point([float(parts[0]), float(parts[1]),float(parts[2])]))
            if(line[0]=='f'): 
                T.append([int(parts[0])-1, int(parts[1])-1,int(parts[2])-1])	
                #T.append([int(parts[0])-1, int(parts[2])-1,int(parts[3])-1])	
        s.P=P
        s.T=T
        s.N=len(P)
        s.M=len(T)

    def find_boundary1(s):
        v=s.P
        f=s.T
        t=s.NT
        temp=[]
        bound=set() 	
        kol1=0
        kol2=0
        edges1=[] 	
        for i in range(len(v)):
            temp=t[i]
            kol1=len(t[i])
            a=[]  		
            for j in range(len(temp)):
            
                for k in f[temp[j]]:
                    if k!=i : 
                        a.append(k)
                    				
            for g in a:                         				
                kol2=a.count(g) 
                     
                if(kol2==1): 
                
                    edges1.append([i,g])
                    bound.add(i) 
        				
        # edges=[]
        # b=[]
        # a=[]
        # for k in range(len(edges1)):
            # a=list([edges1[k][1],edges1[k][0]])
            # b=list([edges1[k][0], edges1[k][1]])
            # if (not( (a in edges) or ( b in edges))): edges.append(edges1[k])
            # #print edges  
             		
        s.Bnd=list(bound)
        # print edges	
        # print bound
        #print edges		
        return bound#, edges 
		
    def find_boundary(s):
        v=s.P
        f=s.T
        t=s.NT
        temp=[]
        bound=[]
        kol1=0
        kol2=0
        for i in range(len(v)):
            temp=t[i]
            kol1=len(t[i])
            #print temp 
            a=set()		
            for j in range(len(temp)):
                #if (i in faces[temp[j]]):
                for k in f[temp[j]]:
                    if k!=i : a.add(k)                         				
            kol2=len(a)         
            if(kol2-kol1>0): 
                bound.append(i)
        s.Bnd=bound    
        #print bound
        return bound 
