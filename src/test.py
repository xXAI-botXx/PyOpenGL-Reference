import sys

sys.path += ["."]

import windforge as wf

class Test(wf.GraphicsApplication):
    def __init__(self):
        super().__init__(size=[512, 512],
                        resizable=True,
                        title="Interactive Computer-Graphics Application with Wind-Forge",
                        multisample=True, 
                        samples=4, 
                        depth_buffer=24, 
                        gl_version=None,# "3.3", 
                        post_process=[],
                        background_lib=wf.window.WindowLib.PYGAME,
                        goal_fps=60,
                        deactivate_pre_input_processing=False,
                        print_missed_events=True,
                        print_catched_events=True)

    def initialize(self):
        print("Init...")

    def process_input(self):
        self.window.events()
        # return super().process_input()

    def update(self):
        pass


if __name__ == "__main__":
    Test().run()



