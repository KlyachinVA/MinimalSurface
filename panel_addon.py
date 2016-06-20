# bl_info = { 
    # "name": "Minimal surfaces",
    # "category": "3D View",
	# "author":"Klyachin V.A., Grigorieva E.G. VolSU,2016"
# }
#�������� ����-������ ������, ����� ���: ��������, ������, �����...
import bpy
from .MinSurface import triangulation as tr
from .MinSurface import minsquare as ndv
from .MinSurface import geometry as geom
from .MinSurface import tentsurface as tnt

global st
global ni
global tens
global density
st=0.09
ni=5
tens=1.0
density=0.1
def find_boundary1(v,f,t):
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
    edges=[]
    b=[]
    a=[]
    for k in range(len(edges1)):
        a=list([edges1[k][1],edges1[k][0]])
        b=list([edges1[k][0], edges1[k][1]])
        if ( a not in edges) and ( b not in edges): edges.append(edges1[k])
        #print edges  
             		
		
    #print edges	
    #print bound
    #print edges		
    return list(bound), edges 		


def createNT(v,f):
    NT=[[] for p in range(0,len(v))]
    for i in range(0,len(f)):
        
        for k in f[i]:
            NT[k].append(i)
    return NT		

def make_polygon():
    ob=bpy.context.object
    me=ob.data
    # bpy.ops.object.modifier_add(type='TRIANGULATE')
    # bpy.ops.object.modifier_apply(apply_as='DATA')
    mod = ob.modifiers.new('triangles', 'TRIANGULATE')
    bpy.ops.object.modifier_apply(apply_as='DATA',modifier='triangles')

    verts=[]
    for v in me.vertices:
        verts.append([v.co.x,v.co.y,v.co.z])
   
    faces=[]
    for p in me.polygons:
        polygon=[]
        for k in p.vertices:
            polygon.append(k)
        faces.append(polygon)

    neighbours=createNT(verts,faces)

    bpoints,edges=find_boundary1(verts,faces,neighbours)

#print(bpoints)
#print(edges)
    ob.select=False
#��������� ������ �����
    pol_me = bpy.data.meshes.new("Polygon")
#��������� ������ ������ � ������ ������
    pol_ob = bpy.data.objects.new("BPolygon", pol_me)
#�������� ������ � ������� �����
    scn = bpy.context.scene
#������������ ��������� ����� ������ � �����
    scn.objects.link(pol_ob)
#������ ������ �������� � ����������
    scn.objects.active = pol_ob
    pol_ob.select = True
    bverts=[]
    nums={}
    i=0
    for k in bpoints:
        nums[k]=i
        bverts.append(verts[k])
        i+=1
   
    bedges=[]
    for e in edges:
        bedges.append([nums[e[0]],nums[e[1]]])


    pol_me.from_pydata(bverts, bedges, [])
    pol_me.update()
def make_cmcsurface():
    global st,ni,density,tens
    t1=load_object()
    t1.createNT()
    
    t1.find_boundary1()
    	
    smin=ndv.MinimalSquare(t1,eps=st)
    smin.create_subLin()
    smin.tension(tens)	
    smin.density(density)
    xp=t1.P
    x0=[]
    for p in xp:
	    x0.append(p.P)
    y=smin.process(ni,x0)
    #t1.save_obj_points("c:/111/min.obj",y)
    make_surface(t1,y)
	
def make_capillarsurface():
    global st,ni,density,tens
    t1=load_object()
    t1.createNT()
    
    t1.find_boundary1()
    t1.createNE()
    
    smin=ndv.CapillarSurface(t1,eps=st)
    smin.create_subLin()
    smin.tension(tens)	
    smin.density(density)
    xp=t1.P
    x0=[]
    for p in xp:
	    x0.append(p.P)
    y=smin.process(ni,x0)
    #t1.save_obj_points("c:/111/min.obj",y)
    make_surface(t1,y)
	
def make_minsurface():
    global st,ni,density,tens
    t1=load_object()
    t1.createNT()
    
    t1.find_boundary1()
   	
    smin=ndv.MinimalSquare(t1,eps=st)	
    smin.tension(tens)
    xp=t1.P
    x0=[]
    for p in xp:
	    x0.append(p.P)
    y=smin.process(ni,x0)
    #t1.save_obj_points("c:/111/min.obj",y)
    make_surface(t1,y)
def make_tentsurface():
    global st,ni,density,tens
    t1=load_object()
    t1.createNT()
    
    t1.find_boundary1()
    	
    smin=tnt.MinimalTent(t1,eps=st)	
    smin.tension(tens)
    xp=t1.P
    x0=[]
    for p in xp:
	    x0.append(p.P)
    y=smin.process(ni,x0)
    #t1.save_obj_points("c:/111/min.obj",y)
    make_surface(t1,y)


def make_surface(T,Y):
    pol_me = bpy.data.meshes.new("MinSurface")
#��������� ������ ������ � ������ ������
    pol_ob = bpy.data.objects.new("MinSurface", pol_me)
#�������� ������ � ������� �����
    scn = bpy.context.scene
#������������ ��������� ����� ������ � �����
    scn.objects.link(pol_ob)
#������ ������ �������� � ����������
    scn.objects.active = pol_ob
    pol_ob.select = True
    verts=[]
    for p in Y:
        verts.append([p[0],p[1],p[2]])
    faces=T.T
    pol_me.from_pydata(verts, [], faces)
    pol_me.update()
    	

def load_object():
    ob=bpy.context.object
    me=ob.data
    mod = ob.modifiers.new('triangles', 'TRIANGULATE')
    bpy.ops.object.modifier_apply(apply_as='DATA',modifier='triangles')
    verts=[]
    for v in me.vertices:
        verts.append(geom.Point([v.co.x,v.co.y,v.co.z]))
   
    faces=[]
    for p in me.polygons:
        polygon=[]
        for k in p.vertices:
            polygon.append(k)
        faces.append(polygon)
    T=tr.Triangulation(verts,faces)
    return T

#�� ����� ������������
# class ToolsPanel(bpy.types.Panel):
# #�������� ����� ������
    # bl_label = "Find boundary"
# #����������� � ���� 3D ����
    # bl_space_type = "VIEW_3D"
# #����� ����� � �� ����� ������������
    # bl_region_type = "TOOLS"
# #������ ��������-���������� ������� �� ������
    # def draw(self, context):
        # self.layout.operator("object.boundary")
class FindBoundary(bpy.types.Operator):
    bl_idname = "object.boundary"
#������� �� ������
    bl_label = "FIND"
    
#����� execute � ����������� �����, � �������
#��������
#��������� �������� ������������.
    def execute(self, context):
        make_polygon()

        return{'FINISHED'}
class Settings(bpy.types.Operator):
    bl_idname = "object.settings"
#������� �� ������
    bl_label = "Settings"
    bl_options = {'REGISTER', 'UNDO'}
    tens = bpy.props.FloatProperty(name="Surface tension",
        default=1.00, min=0.0001, max=10.0)
    density = bpy.props.FloatProperty(name="Density",
        default=0.10, min=0.0001, max=10.0)
    step = bpy.props.FloatProperty(name="Step",
            default=0.09, min=0.0001, max=10.0)
    niter = bpy.props.IntProperty(name="Number of iterations",
            description="Number of iterations",
            default=5, min=5, max=1000)

    
#����� execute � ����������� �����, � �������
#��������
#��������� �������� ������������.
    def execute(self, context):
        #make_polygon()
        global st,ni,density,tens
        st=self.step
        ni=self.niter
        tens=self.tens
        density=self.density
        #print(self.step,self.niter)
        return{'FINISHED'}

class FindMinSurface(bpy.types.Operator):
    bl_idname = "object.minsurface"
#������� �� ������
    bl_label = "FIND Minsurface"
#����� execute � ����������� �����, � �������
#��������
#��������� �������� ������������.
    def execute(self, context):
        make_minsurface()

        return{'FINISHED'}
class FindCMCSurface(bpy.types.Operator):
    bl_idname = "object.cmcsurface"
#������� �� ������
    bl_label = "FIND CMC surface"
#����� execute � ����������� �����, � �������
#��������
#��������� �������� ������������.
    def execute(self, context):
        make_cmcsurface()

        return{'FINISHED'}
class FindCapillarSurface(bpy.types.Operator):
    bl_idname = "object.capillarsurface"
#������� �� ������
    bl_label = "FIND Capillar surface"
#����� execute � ����������� �����, � �������
#��������
#��������� �������� ������������.
    def execute(self, context):
        make_capillarsurface()

        return{'FINISHED'}

class FindTentSurface(bpy.types.Operator):
    bl_idname = "object.tentsurface"
#������� �� ������
    bl_label = "FIND tent surface"
#����� execute � ����������� �����, � �������
#��������
#��������� �������� ������������.
    def execute(self, context):
        make_tentsurface()

        return{'FINISHED'}

class MinimalSurfacePanel(bpy.types.Panel): #��������� ����� � ����� ���� Panel
  bl_label = "Minimal surfaces"	        #�������� ����
  bl_space_type = 'VIEW_3D'	#���� ������������
  bl_region_type = 'TOOLS'	#������ ������������
 
  def draw(self, context):	#������� ������������ ���������� ������ ����
    layout = self.layout
    #���������� layout ������������� ��������� self.layout
    layout.label(text="Press for make the boundary")	#� ������� label ��������� ����� �����
 
    split = layout.split()
    #���������� split ������������� ��������� layout.split()
    col = split.column(align=True)
    #���������� col ������������� ��������� split.column(align=True)
 
    col.operator("object.boundary", text="FIND", icon="MESH_CUBE")
    col.label(text="Press for settings")
    col.operator("object.settings", text="Settings", icon="MESH_CUBE")
    col.label(text="Press for construct the surface")
    col.operator("object.minsurface", text="FIND Minsurface", icon="MESH_CUBE")
    col.operator("object.tentsurface", text="FIND tent surface", icon="MESH_CUBE")
    col.operator("object.cmcsurface", text="FIND CMC surface", icon="MESH_CUBE")
    col.operator("object.capillarsurface", text="FIND Capillar surface", icon="MESH_CUBE")
    #��������� ������ �������� ���� � ������� � �������
    #col.operator("mesh.primitive_monkey_add", text="Monkey", icon="MESH_MONKEY")
    #��������� ������ �������� ������� � ������� � �������
 
def register():		#������� ��������� ������ ��� ��������� ������
  bpy.utils.register_class(MinimalSurfacePanel)
 
def unregister():	#������� ��������� ������ ��� ���������� ������
  bpy.utils.unregister_class(MinimalSurfacePanel)
 
if __name__ == "__main__":
  register()
#������� ��������� ��������� ������ ��������������� �� ���������