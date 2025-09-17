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
                        print_missed_events=False,
                        print_catched_events=False)

    def initialize(self):
        print("Init...")
        self.counter = 0

    def process_input(self):
        # return super().process_input()

        if self.counter == 0:

            # for event in self.events:
            #     if event.type == wf.window.EventType.CONTROLLER_BUTTON_DOWN:
            #         print(f"{event.controller_button}")

            # for event in self.events:
            #     if event.type == wf.window.EventType.CONTROLLER_AXIS_MOVE:
            #         print(f"{event.axis}: {event.axis_value}")

            holded_inputs = self.window.input_state.get_all_active(as_string=True)
            print(f"Keyboard holds [{', '.join(holded_inputs['keys'])}]")
            print(f"Mouse holds [{', '.join(holded_inputs['mouse'])}]")
            for cid, holded_controller_inputs in holded_inputs["controllers"].items():
                print(f"Controller {cid} holds [{', '.join(holded_controller_inputs)}]")

    def update(self):
        self.counter += 1

        if self.counter > self.goal_fps:
            self.counter = 0


if __name__ == "__main__":
    Test().run()



