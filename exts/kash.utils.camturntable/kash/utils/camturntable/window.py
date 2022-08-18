import omni.ext
import omni.ui as ui
import omni.kit.commands
import omni.timeline
from pxr import Gf, Sdf, Usd
LABEL_WIDTH = 60
SPACING = 4

# Any class derived from `omni.ext.IExt` in top level module (defined in `python.modules` of `extension.toml`) will be
# instantiated when extension gets enabled and `on_startup(ext_id)` will be called. Later when extension gets disabled
# on_shutdown() is called.
class CamTurntableWindow(ui.Window):
    """The class that represents the window"""

    def __init__(self, title: str, delegate=None, **kwargs):
        self.__label_width = LABEL_WIDTH

        super().__init__(title, **kwargs)

        self.frame.set_build_fn(self._build_fn)
    
    def destroy(self):
        # It will destroy all the children
        super().destroy()

    @property
    def label_width(self):
        """The width of the attribute label"""
        return self.__label_width

    @label_width.setter
    def label_width(self, value):
        """The width of the attribute label"""
        self.__label_width = value
        self.frame.rebuild()

    def _build_fn(self):
       """
       The method that is called to build all the UI once the window is
       visible.
       """
       with ui.ScrollingFrame():
           with ui.VStack(
            style={
                # Set the color to all ui.Labels
                "Label": {"color": 0xFF00B976},
                # ui.Button.Labels hovered with mouse
                "Button.Label:hovered": {"color": 0xFFFFFFFF},
            }
           ):

               def clockwise_animation():
                   with omni.kit.undo.group():
                       # Delete objects created from script if they already exist in scene.
                       omni.kit.commands.execute('DeletePrims',
                       paths=['/World/MyTurntableCam','/World/MySampleModel'])
                       # Create sample Cube model in scene.    
                       omni.kit.commands.execute('CreatePrimWithDefaultXform',
                           prim_type='Cube',
                           attributes={'size': 100, 'extent': [(-50, -50, -50), (50, 50, 50)]})
                       # Create Camera in scene.       
                       omni.kit.commands.execute('CreatePrimWithDefaultXform',
                           prim_type='Camera',
                           attributes={'focusDistance': 400, 'focalLength': 24})
                       # Move Camera away from origin in scene.    
                       omni.kit.commands.execute('ChangeProperty',
                           prop_path=Sdf.Path('/World/Camera.xformOp:translate'),
                           value=Gf.Vec3d(0.0, 0.0, 700.0),
                           prev=Gf.Vec3d(0.0, 0.0, 0.0))
                       # Create Xform.     
                       omni.kit.commands.execute('CreatePrimWithDefaultXform',
                           prim_type='Xform',
                           attributes={})
                       # Select Camera.
                       omni.kit.commands.execute('SelectPrims',
                           old_selected_paths=['/World/Xform'],
                           new_selected_paths=['/World/Camera'],
                           expand_in_stage=True)
                       # Make Camera a child of TurntableCamera Xform.    
                       omni.kit.commands.execute('MovePrim',
                           path_from='/World/Camera',
                           path_to='/World/Xform/TurntableCamera')
                       # Rename Xform to MyTurntableCam.    
                       omni.kit.commands.execute('MovePrim',
                           path_from='/World/Xform',
                           path_to='/World/MyTurntableCam')
                       # Rename Cube to MySampleModel.
                       omni.kit.commands.execute('MovePrim',
                           path_from='/World/Cube',
                           path_to='/World/MySampleModel')
                       # Select MyTurntableCam in Stage.    
                       omni.kit.commands.execute('SelectPrims',
                           old_selected_paths=[],
                           new_selected_paths=['/World/MyTurntableCam'],
                           expand_in_stage=True)
                       # Create a variable to access the timeline.            
                       self._timeline = omni.timeline.get_timeline_interface()
                       # Set frames per second to 24.
                       time_codes_per_second = 24
                       self._timeline.set_time_codes_per_second(time_codes_per_second)
                       # Set the start and end time on timeline.
                       self._timeline.set_start_time(0)
                       self._timeline.set_end_time(240 / time_codes_per_second)
                       # Set a keyframe for MyTurntableCam at frame 0 with rotation at 360.
                       omni.kit.commands.execute('SetAnimCurveKey',
                           paths=['/World/MyTurntableCam.xformOp:rotateXYZ|y'],
                           time = Usd.TimeCode(0), 
                           value=360.0)
                       # Set a keyframe for MyTurntableCam at frame 0.            
                       omni.kit.commands.execute('SetAnimCurveKey',
                           paths=['/World/MyTurntableCam.xformOp:rotateXYZ|y'],
                           time = Usd.TimeCode(240), 
                           value=0.0)
                       # Select MyTurntableCam in Stage.            
                       omni.kit.commands.execute('SelectPrims',
                           old_selected_paths=[],
                           new_selected_paths=['/World/MyTurntableCam'],
                           expand_in_stage=True)
                       # Move current time on timeline to frame 0. 
                       self._timeline.set_current_time(0/24)  

               def anti_clockwise_animation():
                   with omni.kit.undo.group():
                       # Delete objects created from script if they already exist in scene.
                       omni.kit.commands.execute('DeletePrims',
                           paths=['/World/MyTurntableCam','/World/MySampleModel'])
                       # Create sample Cube model in scene.
                       omni.kit.commands.execute('CreatePrimWithDefaultXform',
                           prim_type='Cube',
                           attributes={'size': 100, 'extent': [(-50, -50, -50), (50, 50, 50)]}) 
                       # Create Camera in scene.    
                       omni.kit.commands.execute('CreatePrimWithDefaultXform',
                           prim_type='Camera',
                           attributes={'focusDistance': 400, 'focalLength': 24})
                       # Move Camera away from origin in scene.    
                       omni.kit.commands.execute('ChangeProperty',
                           prop_path=Sdf.Path('/World/Camera.xformOp:translate'),
                           value=Gf.Vec3d(0.0, 0.0, 700.0),
                           prev=Gf.Vec3d(0.0, 0.0, 0.0))
                       # Create Xform.    
                       omni.kit.commands.execute('CreatePrimWithDefaultXform',
                           prim_type='Xform',
                           attributes={})
                       # Select Camera.    
                       omni.kit.commands.execute('SelectPrims',
                           old_selected_paths=['/World/Xform'],
                           new_selected_paths=['/World/Camera'],
                           expand_in_stage=True)
                       # Make Camera a child of TurntableCamera Xform.    
                       omni.kit.commands.execute('MovePrim',
                           path_from='/World/Camera',
                           path_to='/World/Xform/TurntableCamera')
                       # Rename Xform to MyTurntableCam.    
                       omni.kit.commands.execute('MovePrim',
                           path_from='/World/Xform',
                           path_to='/World/MyTurntableCam')
                       # Rename Cube to MySampleModel.    
                       omni.kit.commands.execute('MovePrim',
                           path_from='/World/Cube',
                           path_to='/World/MySampleModel')
                       # Select MyTurntableCam in Stage.    
                       omni.kit.commands.execute('SelectPrims',
                           old_selected_paths=[],
                           new_selected_paths=['/World/MyTurntableCam'],
                           expand_in_stage=True)
                       # Create a variable to access the timeline.            
                       self._timeline = omni.timeline.get_timeline_interface()
                       # Set frames per second to 24.
                       time_codes_per_second = 24
                       self._timeline.set_time_codes_per_second(time_codes_per_second)
                       # Set the start and end time on timeline.
                       self._timeline.set_start_time(0)
                       self._timeline.set_end_time(240 / time_codes_per_second)
                       # Set a keyframe for MyTurntableCam at frame 0.
                       omni.kit.commands.execute('SetAnimCurveKey',
                           paths=['/World/MyTurntableCam.xformOp:rotateXYZ|y'],
                           time = Usd.TimeCode(0), 
                           value=0.0)
                       # Set a keyframe for MyTurntableCam at frame 100 after a full 360 rotation.            
                       omni.kit.commands.execute('SetAnimCurveKey',
                           paths=['/World/MyTurntableCam.xformOp:rotateXYZ|y'],
                           time = Usd.TimeCode(240), 
                           value=360.0)
                       # Select MyTurntableCam in Stage.    
                       omni.kit.commands.execute('SelectPrims',
                           old_selected_paths=[],
                           new_selected_paths=['/World/MyTurntableCam'],
                           expand_in_stage=True)
                       # Move current time on timeline to frame 0.    
                       self._timeline.set_current_time(0/24)


               ui.Label(
                   "Choose your turntable animation! "
                   "Chose the wrong one? Hit CTRL+Z to undo.", 
                   word_wrap=True, alignment=ui.Alignment.CENTER,
                )
                              
               ui.Button("Create Clockwise Camera!", clicked_fn=lambda: clockwise_animation())
               ui.Button("Create Anti-Clockwise Camera!", clicked_fn=lambda: anti_clockwise_animation())
