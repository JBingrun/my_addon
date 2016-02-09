######################################################################################################
# An simple add-on to make your life easier                                                          #
# Author: Bingrun Jiang                                                                              #
# License: GPL v3                                                                                    #
######################################################################################################

bl_info = {
    "name": "Lazy Fire",
    "author": "Bingrun Jiang",
    "version": (0, 1),
    "blender": (2, 7, 6),
    "location": "3d View > Tool shelf > JBR TOOL",
    "description": "Tools for better life",
    "warning": "",
    "wiki_url": "nickb771223@gmail.com",
    "tracker_url": "",
    "category": "Mesh"}


import bpy , mathutils, math, os, bpy.utils.previews
from mathutils import Vector, Matrix
from bpy.props import *



#custom_input
'''
bpy.types.Scene.BakeRange_start = bpy.props.IntProperty(default= 1, min= 0, description="bake start fram")
bpy.types.Scene.BakeRange_end = bpy.props.IntProperty(default= 250, min= 0, description="bake end fram")
Snumber = bpy.types.Scene.BakeRange_start
Enumber = bpy.types.Scene.BakeRange_end
'''

#create a group
#bpy.ops.group.create(name="Group")



class LazyFire(bpy.types.Scene):
    def initSceneProperties(scn):
     
        bpy.types.Scene.MyEnum = EnumProperty(
            items = [('Eine', 'Un', 'One') ],
            name = "Group")
        scn['MyEnum'] = 2
     
        return
     
    initSceneProperties(bpy.context.scene)




#panel

class LazyFire(bpy.types.Panel):
    bl_label = "Lazy Fire"
    bl_idname = "Lazy Fire"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_category = "JBR TOOL"
    #bl_context = "objectmode"
     
    @classmethod
    def poll(cls, context):
        return context.object and context.mode == 'OBJECT' and context.object.type == 'MESH' 
    
    def draw(self, context):
        scn = context.scene
        dat = bpy.data
        layout = self.layout
        #layout.label("Bake Range")
        layout.label("Choose your object Group")
        layout.prop(scn, 'MyEnum')              
        layout.prop_search(scn, "theChosenObject", scn, "objects")
        layout.prop_search(scn, "ppp", dat, "groups")
        #layout.prop(context.scene, "BakeRange_start", text="start frame")
        #layout.prop(context.scene, "BakeRange_end", text="end frame")
        row = layout.row()
        layout.operator("showtime.button", icon_value=custom_icons["custom_icon"].icon_id)

                
# global variable to store icons in
custom_icons = None

#execon

class ShowTime(bpy.types.Operator):
    bl_idname = "showtime.button"
    bl_label = "SHOW  TIME!"
    
    @classmethod
    def poll(cls, context):
        return context.object and context.mode == 'OBJECT' and context.object.type == 'MESH' 
    
    def execute(self, context):   
        a = len(bpy.context.selected_objects) 
        bs = bpy.context.scene.frame_start
        be = bpy.context.scene.frame_end
 
        for objs in bpy.context.selected_objects:
            
            bpy.context.scene.objects.active = objs
            
            bpy.ops.nla.bake(frame_start= bs, frame_end= be, only_selected=True, visual_keying=True, clear_constraints=True, clear_parents=True, use_current_action=False, bake_types={'OBJECT'})

            bpy.ops.object.editmode_toggle()
            bpy.ops.mesh.merge(type='CENTER')
            bpy.ops.object.editmode_toggle()
            
        bpy.ops.object.join()
        bpy.ops.object.particle_system_add()
        
        #Particle def
        psys = bpy.context.object.particle_systems[-1]
        pset = psys.settings

        pset.count = a
        pset.normal_factor = 0
        pset.frame_start = 1
        pset.frame_end = 1
        pset.lifetime = 250
        pset.emit_from = 'VERT'
        pset.use_emit_random = False

        # Physics
        pset.physics_type = 'NO'
        pset.particle_size = 0.3
     
        # Effector weights
        pset.effector_weights.gravity = 0
     
        # Display and render  
        pset.render_type = 'GROUP'
        pset.dupli_group = bpy.data.groups["fire"]


        return{'FINISHED'}


      
def register():
    '''
    bpy.utils.register_class(LazyFire) 
    bpy.utils.register_class(ShowTime)
    '''
    global custom_icons
    custom_icons = bpy.utils.previews.new()
    script_path = bpy.context.space_data.text.filepath
    icons_dir = os.path.join(os.path.dirname(script_path), "icons")
    custom_icons.load("custom_icon", os.path.join(icons_dir, "head_phone.png"), 'IMAGE')
    bpy.utils.register_module(__name__)
    
    bpy.types.Scene.theChosenObject = bpy.props.StringProperty()
    bpy.types.Scene.ppp = bpy.props.StringProperty()

def unregister():
    '''
    bpy.utils.register_class(LazyFire)
    bpy.utils.register_class(ShowTime)
    '''    
    global custom_icons
    bpy.utils.previews.remove(custom_icons)
    bpy.utils.unregister_module(__name__)
    
    del bpy.types.Object.theChosenObject
    del bpy.types.Object.ppp

if __name__ == "__main__":
    register()

