import bpy
from . import panel_addon
bl_info = { 
    "name": "Find Boundary Addon",
    "category": "3D View",
	"author":"Klyachin V.A., Grigorieva E.G. VolSU,2016"
}

def register():		
  bpy.utils.register_class(panel_addon.MyPanel)
  bpy.utils.register_class(panel_addon.FindBoundary)
  bpy.utils.register_class(panel_addon.FindMinSurface) 
def unregister():	
  bpy.utils.unregister_class(panel_addon.MyPanel)
  bpy.utils.unregister_class(panel_addon.FindBoundary)
  bpy.utils.unregister_class(panel_addon.FindMinSurface) 
# if __name__ == "__main__":
  # register()
