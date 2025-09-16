import sys

from .window import Window, EventType, WindowLib
from .time import Clock

class GraphicsApplication():
    def __init__(self, 
                 size=[512, 512],
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

        Can be adjusted in inherent class.
        """
        pass

    def process_input(self):
        """
        Runs every frame and should process the events.<br>
        The self.window attribute should be used to get current events (button pressed/released)
        and also the state of input devices (which buttons are holded/not pressed).

        Can be adjusted in inherent class.
        """
        for event in self.window.events():
            if event.type == EventType.QUIT:
                self.should_run = False 

    def update(self):
        pass

    def generate_output(self):
        self.window.display()

    def run(self):
        # start
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

