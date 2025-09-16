import sys

from .window import Window, EventType, Key, MouseButton, ControllerButton, ControllerAxis, WindowLib
from .time import Clock

class GraphicsApplication():
    """
    Base class for Wind-Forge Engine.

    Inherent from this class and overwrite (as you need):
    - initialize
    - process_input
    - update
    - generate_output
    """
    def __init__(self, 
                 size=[512, 512],
                 resizable=True,
                 title="Interactive Computer-Graphics Application with Wind-Forge",
                 multisample=True, 
                 samples=4, 
                 depth_buffer=24, 
                 gl_version=None, 
                 post_process=[],
                 background_lib=WindowLib.PYGAME,
                 goal_fps=60):
        self.goal_fps = goal_fps
        self.window = Window(size=size,
                             resizable=resizable,
                             title=title,
                             multisample=multisample, 
                             samples=samples, 
                             depth_buffer=depth_buffer, 
                             gl_version=gl_version, 
                             post_process=post_process,
                             background_lib=background_lib)

        # main-loop bool
        self.should_run = True

        # start clock (for FPS goal reaching)
        self.clock = Clock(goal_fps=self.goal_fps)

    def initialize(self):
        """
        Will be executed at the beginning of start (run method).

        Can be overwritten in inherent class.
        """
        pass

    def process_input(self):
        """
        Runs every frame and should process the events.<br>
        The self.window attribute should be used to get current events (button pressed/released)
        and also the state of input devices (which buttons are holded/not pressed).

        Can be overwritten in inherent class.
        """
        for event in self.window.events():
            if event.type == EventType.QUIT:
                self.should_run = False
            elif event.type == EventType.KEY_DOWN:
                if event.key == Key.ESC:
                    self.should_run = False
            elif event.type == EventType.MOUSE_DOWN:
                print(f"Mouse button pressed: {event.mouse_button}")
            elif event.type == EventType.MOUSE_MOVE:
                pass
                # print(f"Mouse moved to: {event.mouse_position}")

        # query current input state
        active = self.window.input_state.get_all_active()

        # check held keys
        if Key.W in active["keys"]:
            print("W is being held down!")
        if MouseButton.LEFT in active["mouse_buttons"]:
            print("Left mouse button is being held down!")

        # check controller input
        for cid, controller in active["controllers"].items():
            if ControllerButton.A in controller["buttons"]:
                print(f"Controller {cid}: Button A pressed")
            for axis, value in controller["axes"].items():
                print(f"Controller {cid}: Axis {axis} = {value}")

    def update(self):
        """
        Runs every frame and should update objects.<br>

        Can be overwritten in inherent class.
        """
        pass

    def generate_output(self):
        """
        Runs every frame and should generate outputs.<br>

        Can be overwritten in inherent class.
        """
        self.window.display()

    def run(self):
        # start
        print(" > Welcome to Wind-Forge <\n")
        self.initialize()

        # loop
        while self.should_run:
            # process input
            self.process_input()

            # update
            self.update()

            # generate output (render)
            self.generate_output()

            # pausing to come to 60 FPS (goal fps)
            frame_time = self.clock.tick()
            # frame_time = delta is the time since the last frame -> can be used for updating the objects in equal also with different FPS

        # end
        self.window.quit()
        sys.exit()

