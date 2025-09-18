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
        self.input_timer = wf.time.Timer(
                                    call_func=lambda x: x.timer_func_input(),
                                    call_attributes=self,
                                    seconds_to_wait=1,
                                    frames_to_wait=0,
                                    repeat=True
                            )
        self.update_timer = wf.time.Timer(
                                    call_func=lambda x: x.timer_func_update(),
                                    call_attributes=self,
                                    seconds_to_wait=1,
                                    frames_to_wait=0,
                                    repeat=True
                            )
        
    def timer_func_input(self):
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

    def process_input(self):
        # return super().process_input()

        self.input_timer.tick()

    def timer_func_update(self):
        print(f"Current FPS: {self.clock.get_fps()} (possible would be: {self.clock.get_potential_fps()} FPS)\n\n")

    def update(self):
        self.update_timer.tick()
            

    def generate_output(self):
        self.window.display()


if __name__ == "__main__":
    Test().run()



