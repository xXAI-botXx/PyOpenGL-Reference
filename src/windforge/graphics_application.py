"""
Graphics application base for the Wind-Forge Engine.

Provides the `GraphicsApplication` class, which serves as the main
application loop for interactive graphics programs. It wraps window
creation, input handling, update loops, and rendering output.

Typical usage:
    class MyApp(GraphicsApplication):
        def initialize(self):
            print("App started")

        def process_input(self):
            super().process_input()  # or custom input handling

        def update(self):
            pass  # game logic

        def generate_output(self):
            pass  # rendering

    if __name__ == "__main__":
        app = MyApp()
        app.run()
"""



# -------------------------------
#        >>> Imports <<<
# -------------------------------
import sys

from .window import Window, EventType, Key, MouseButton, ControllerButton, ControllerAxis, WindowLib
from .time import Clock



# -------------------------------
#         >>> Class <<<
# -------------------------------
class GraphicsApplication():
    """
    Base class for Wind-Forge Engine applications.

    Provides a main loop with initialization, input processing,
    updating, and rendering. Applications should subclass this
    class and override the relevant methods.

    Args:
        size (list[int], optional): Initial window size [width, height]. Default [512, 512].
        resizable (bool, optional): Whether the window can be resized. Default True.
        title (str, optional): Window title. Default Wind-Forge message.
        multisample (bool, optional): Enable multisample anti-aliasing. Default True.
        samples (int, optional): Number of samples for multisampling. Default 4.
        depth_buffer (int, optional): Depth buffer size in bits. Default 24.
        gl_version (tuple[int, int], optional): OpenGL version (major, minor). Default None.
        post_process (list, optional): List of post-processing effects. Default [].
        background_lib (WindowLib, optional): Window backend (PYGAME or GLFW). Default PYGAME.
        goal_fps (int, optional): Target FPS. Default 60.
        deactivate_pre_input_processing (bool, optional): If True, disables automatic pre-input processing. Default False.
        print_missed_events (bool, optional): Print debug messages for missed events. Default False.
        print_catched_events (bool, optional): Print detailed event info for debugging. Default False.
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
                 goal_fps=60,
                 deactivate_pre_input_processing=False,
                 print_missed_events=False,
                 print_catched_events=False):
        self.goal_fps = goal_fps
        self.window = Window(size=size,
                             resizable=resizable,
                             title=title,
                             multisample=multisample, 
                             samples=samples, 
                             depth_buffer=depth_buffer, 
                             gl_version=gl_version, 
                             post_process=post_process,
                             background_lib=background_lib,
                             print_missed_events=print_missed_events)

        # main-loop bool
        self.should_run = True

        self.events = []
        self.deactivate_pre_input_processing = deactivate_pre_input_processing
        self.print_catched_events = print_catched_events

        # start clock (for FPS goal reaching)
        self.clock = Clock(goal_fps=self.goal_fps)

    def initialize(self):
        """
        Called once before the main loop starts.

        Override this in your subclass to set up resources
        such as loading assets, initializing OpenGL, etc.
        """
        pass

    def process_input(self):
        """
        Runs every frame and should process the events.<br>
        The self.window attribute should be used to get current events (button pressed/released)
        and also the state of input devices (which buttons are holded/not pressed).

        Can be overwritten in inherent class.

        If you choose `deactivate_pre_input_processing = False` you should use:
        ```python
        def process_input(self):
            events = self.window.events()

            for event in events:
                if event.type == EventType.KEY_DOWN:
                    pass
        ```

        Else you can directly use `self.events`.
        """
        events = self.pre_input_processing()

        for event in events:
            print(f"Got Event: {event.type}")
            if event.type == EventType.KEY_DOWN:
                if event.key == Key.ESC:
                    self.should_run = False
            elif event.type == EventType.MOUSE_DOWN:
                pass
                # print(f"Mouse button pressed: {event.mouse_button}")
            elif event.type == EventType.MOUSE_MOVE:
                pass
                # print(f"Mouse moved to: {event.mouse_position}")
            elif event.type == EventType.CONTROLLER_AXIS_MOVE:
                print(f"  -> Axis: {event.axis}, Value: {event.axis_value}")

        # query current input state
        active = self.window.input_state.get_all_active()

        # check held keys
        if Key.W in active["keys"]:
            print("W is being held down!")
        if MouseButton.LEFT in active["mouse_buttons"]:
            print("Left mouse button is being held down!")

        # check controller input
        for cid, actives in active["controllers"].items():
            if ControllerButton.A in actives:
                print(f"Controller {cid}: Button A pressed")

    def pre_input_processing(self):
        """
        Run standard pre-processing of input events.

        Collects events from the window, logs them if
        `print_catched_events` is True, and handles quit events.

        Returns:
            list[Event]: List of events for this frame.
        """
        events = self.window.events()
        for event in events:
            if self.print_catched_events:
                event_details = [f"{name}:{value}" for name, value in vars(event).items() if value and name != "type"]
                print(f"[INFO] Catched Event: {event.type} ({', '.join(event_details)})")
            if event.type == EventType.QUIT:
                self.should_run = False
        return events

    def update(self):
        """
        Update application state each frame.

        Override this to update objects, animations, physics, etc.
        """
        pass

    def generate_output(self):
        """
        Render output each frame.

        Override this to perform drawing calls.
        By default, swaps buffers to display content.
        """
        self.window.display()

    def run(self):
        """
        Start the main application loop.

        Handles initialization, input, updates, rendering,
        and frame timing until `self.should_run` is False.

        Raises:
            SystemExit: When the application quits.
        """
        # start
        print("> Welcome to Wind-Forge <\n")
        print("[Hint] Make sure to closed every controller control system (for example Steam). Else the systems will disturb each other.\n")
        self.initialize()

        # loop
        while self.should_run:
            # process input
            if self.deactivate_pre_input_processing == False:
                self.events = self.pre_input_processing()
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

