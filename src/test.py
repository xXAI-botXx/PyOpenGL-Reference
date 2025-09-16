import sys

sys.path += ["."]

import wind_forge_engine as wf

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
                        goal_fps=60)

    def initialize(self):
        print("Init...")

    def update(self):
        pass


if __name__ == "__main__":
    Test().run()



