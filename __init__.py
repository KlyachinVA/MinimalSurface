import bpy
from . import panel_addon
bl_info = { 
    "name": "Construct minimal surfaces addon",
    "category": "3D View",
	"author":"Klyachin V.A., Grigorieva E.G. VolSU,2016"
}

def register():		
  bpy.utils.register_class(panel_addon.MinimalSurfacePanel)
  bpy.utils.register_class(panel_addon.FindBoundary)
  bpy.utils.register_class(panel_addon.FindMinSurface)
  bpy.utils.register_class(panel_addon.FindCMCSurface)
  bpy.utils.register_class(panel_addon.FindCapillarSurface)
  bpy.utils.register_class(panel_addon.FindTentSurface)  
  bpy.utils.register_class(panel_addon.Settings)
def unregister():	
  bpy.utils.unregister_class(panel_addon.MinimalSurfacePanel)
  bpy.utils.unregister_class(panel_addon.FindBoundary)
  bpy.utils.unregister_class(panel_addon.FindMinSurface)
  bpy.utils.unregister_class(panel_addon.FindCMCSurface)
  bpy.utils.unregister_class(panel_addon.FindCapillarSurface)
  bpy.utils.unregister_class(panel_addon.FindTentSurface)
  bpy.utils.unregister_class(panel_addon.Settings)  
# if __name__ == "__main__":
  # register()
