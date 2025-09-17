# -------------------------------
#        >>> Imports <<<
# -------------------------------
import sys
import os
from enum import Enum, auto
from abc import ABC, abstractmethod
import re
import ctypes

# backends
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pygame.pkgdata")
original_stdout = sys.stdout
sys.stdout = open(os.devnull, 'w')
import pygame
import glfw
sys.stdout.close()
sys.stdout = original_stdout



# -------------------------------
# >>> Variables and Constants <<<
# -------------------------------

class WindowLib(Enum):
    PYGAME = auto()
    GLFW = auto()
    # PyGLFW, PyQt, PySDL, ...

class EventType(Enum):
    WINDOW_MOVE = auto()
    WINDOW_RESIZE = auto()
    WINDOW_ACCESS = auto()  # In window?
    WINDOW_ACTIVATION = auto()  # Window Active?
    QUIT = auto()

    KEY_DOWN = auto()
    KEY_UP = auto()

    MOUSE_MOVE = auto()
    MOUSE_DOWN = auto()
    MOUSE_UP = auto()
    MOUSE_WHEEL = auto()

    CONTROLLER_ADDED = auto()
    CONTROLLER_REMOVED = auto()
    CONTROLLER_BUTTON_DOWN = auto()
    CONTROLLER_BUTTON_UP = auto()
    CONTROLLER_AXIS_MOVE = auto()

class Key(Enum):
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    E = auto()
    F = auto()
    G = auto()
    H = auto()
    I = auto()
    J = auto()
    K = auto()
    L = auto()
    M = auto()
    N = auto()
    O = auto()
    P = auto()
    Q = auto()
    R = auto()
    S = auto()
    T = auto()
    U = auto()
    V = auto()
    W = auto()
    X = auto()
    Y = auto()
    Z = auto()
    SPACE = auto()
    ENTER = auto()
    SHIFT = auto()
    CTRL = auto()
    ALT = auto()
    ESC = auto()
    TAB = auto()
    BACKSPACE = auto()
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()

class MouseButton(Enum):
    LEFT = auto()
    RIGHT = auto()
    MIDDLE = auto()
    BUTTON4 = auto()  # Extra mouse buttons
    BUTTON5 = auto()

class ControllerButton(Enum):
    """
    In Xbox-Controller Design:
    - https://xboxdesignlab.xbox.com/de-de/controllers/xbox-wireless-controller
    - https://de.wikipedia.org/wiki/Xbox_Wireless_Controller
    """
    A = auto()
    B = auto()
    X = auto()
    Y = auto()
    LB = auto()       # Left bumper
    RB = auto()       # Right bumper
    START = auto()
    SELECT = auto()
    LSTICK = auto()   # Left stick click
    RSTICK = auto()   # Right stick click
    DPAD = auto()

class ControllerAxis(Enum):
    LEFT_STICK_X = auto()
    LEFT_STICK_Y = auto()
    RIGHT_STICK_X = auto()
    RIGHT_STICK_Y = auto()
    LEFT_TRIGGER = auto()
    RIGHT_TRIGGER = auto()

class DpadState(Enum):
    NEUTRAL = auto()
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()
    UP_RIGHT = auto()
    UP_LEFT = auto()
    DOWN_RIGHT = auto()
    DOWN_LEFT = auto()



# -------------------------------
#     >>> Key Mappings <<<
# -------------------------------
# PYGAME
PYGAME_KEY_MAP = {
    pygame.K_a: Key.A,
    pygame.K_b: Key.B,
    pygame.K_c: Key.C,
    pygame.K_d: Key.D,
    pygame.K_e: Key.E,
    pygame.K_f: Key.F,
    pygame.K_g: Key.G,
    pygame.K_h: Key.H,
    pygame.K_i: Key.I,
    pygame.K_j: Key.J,
    pygame.K_k: Key.K,
    pygame.K_l: Key.L,
    pygame.K_m: Key.M,
    pygame.K_n: Key.N,
    pygame.K_o: Key.O,
    pygame.K_p: Key.P,
    pygame.K_q: Key.Q,
    pygame.K_r: Key.R,
    pygame.K_s: Key.S,
    pygame.K_t: Key.T,
    pygame.K_u: Key.U,
    pygame.K_v: Key.V,
    pygame.K_w: Key.W,
    pygame.K_x: Key.X,
    pygame.K_y: Key.Y,
    pygame.K_z: Key.Z,

    pygame.K_SPACE: Key.SPACE,
    pygame.K_RETURN: Key.ENTER,
    pygame.K_LSHIFT: Key.SHIFT,
    pygame.K_RSHIFT: Key.SHIFT,
    pygame.K_LCTRL: Key.CTRL,
    pygame.K_RCTRL: Key.CTRL,
    pygame.K_LALT: Key.ALT,
    pygame.K_RALT: Key.ALT,
    pygame.K_ESCAPE: Key.ESC,
    pygame.K_TAB: Key.TAB,
    pygame.K_BACKSPACE: Key.BACKSPACE,
    pygame.K_UP: Key.UP,
    pygame.K_DOWN: Key.DOWN,
    pygame.K_LEFT: Key.LEFT,
    pygame.K_RIGHT: Key.RIGHT,
}

PYGAME_MOUSE_BUTTON_MAP = {
    1: MouseButton.LEFT,
    2: MouseButton.MIDDLE,
    3: MouseButton.RIGHT,
    4: MouseButton.BUTTON4,
    5: MouseButton.BUTTON5,
}

PYGAME_CONTROLLER_BUTTON_MAP = {
    0: ControllerButton.A,
    1: ControllerButton.B,
    2: ControllerButton.X,
    3: ControllerButton.Y,
    4: ControllerButton.LB,
    5: ControllerButton.RB,
    6: ControllerButton.SELECT,
    7: ControllerButton.START,
    8: ControllerButton.LSTICK,
    9: ControllerButton.RSTICK,
    # hats/dpad often come as JOYHATMOTION, not buttons
}
    
PYGAME_CONTROLLER_DPAD_MAP = {
    ( 0,  0): DpadState.NEUTRAL,
    ( 0,  1): DpadState.UP,
    ( 0, -1): DpadState.DOWN,
    ( 1,  0): DpadState.RIGHT,
    (-1,  0): DpadState.LEFT,
    ( 1,  1): DpadState.UP_RIGHT,
    ( 1, -1): DpadState.DOWN_RIGHT,
    (-1,  1): DpadState.UP_LEFT,
    (-1, -1): DpadState.DOWN_LEFT
}

PYGAME_CONTROLLER_AXIS_MAP = {
    0: ControllerAxis.LEFT_STICK_X,
    1: ControllerAxis.LEFT_STICK_Y,
    2: ControllerAxis.RIGHT_STICK_X,   # depends on device!
    3: ControllerAxis.RIGHT_STICK_Y,   # depends on device!
    4: ControllerAxis.LEFT_TRIGGER,
    5: ControllerAxis.RIGHT_TRIGGER,
}

# GLFW
GLFW_KEY_MAP = {
    glfw.KEY_A: Key.A,
    glfw.KEY_B: Key.B,
    glfw.KEY_C: Key.C,
    glfw.KEY_D: Key.D,
    glfw.KEY_E: Key.E,
    glfw.KEY_F: Key.F,
    glfw.KEY_G: Key.G,
    glfw.KEY_H: Key.H,
    glfw.KEY_I: Key.I,
    glfw.KEY_J: Key.J,
    glfw.KEY_K: Key.K,
    glfw.KEY_L: Key.L,
    glfw.KEY_M: Key.M,
    glfw.KEY_N: Key.N,
    glfw.KEY_O: Key.O,
    glfw.KEY_P: Key.P,
    glfw.KEY_Q: Key.Q,
    glfw.KEY_R: Key.R,
    glfw.KEY_S: Key.S,
    glfw.KEY_T: Key.T,
    glfw.KEY_U: Key.U,
    glfw.KEY_V: Key.V,
    glfw.KEY_W: Key.W,
    glfw.KEY_X: Key.X,
    glfw.KEY_Y: Key.Y,
    glfw.KEY_Z: Key.Z,

    glfw.KEY_SPACE: Key.SPACE,
    glfw.KEY_ENTER: Key.ENTER,
    glfw.KEY_LEFT_SHIFT: Key.SHIFT,
    glfw.KEY_RIGHT_SHIFT: Key.SHIFT,
    glfw.KEY_LEFT_CONTROL: Key.CTRL,
    glfw.KEY_RIGHT_CONTROL: Key.CTRL,
    glfw.KEY_LEFT_ALT: Key.ALT,
    glfw.KEY_RIGHT_ALT: Key.ALT,
    glfw.KEY_ESCAPE: Key.ESC,
    glfw.KEY_TAB: Key.TAB,
    glfw.KEY_BACKSPACE: Key.BACKSPACE,
    glfw.KEY_UP: Key.UP,
    glfw.KEY_DOWN: Key.DOWN,
    glfw.KEY_LEFT: Key.LEFT,
    glfw.KEY_RIGHT: Key.RIGHT,
}

GLFW_MOUSE_BUTTON_MAP = {
    glfw.MOUSE_BUTTON_LEFT: MouseButton.LEFT,
    glfw.MOUSE_BUTTON_RIGHT: MouseButton.RIGHT,
    glfw.MOUSE_BUTTON_MIDDLE: MouseButton.MIDDLE,
    glfw.MOUSE_BUTTON_4: MouseButton.BUTTON4,
    glfw.MOUSE_BUTTON_5: MouseButton.BUTTON5,
}

GLFW_CONTROLLER_BUTTON_MAP = {
    glfw.GAMEPAD_BUTTON_A: ControllerButton.A,
    glfw.GAMEPAD_BUTTON_B: ControllerButton.B,
    glfw.GAMEPAD_BUTTON_X: ControllerButton.X,
    glfw.GAMEPAD_BUTTON_Y: ControllerButton.Y,
    glfw.GAMEPAD_BUTTON_LEFT_BUMPER: ControllerButton.LB,
    glfw.GAMEPAD_BUTTON_RIGHT_BUMPER: ControllerButton.RB,
    glfw.GAMEPAD_BUTTON_BACK: ControllerButton.SELECT,
    glfw.GAMEPAD_BUTTON_START: ControllerButton.START,
    glfw.GAMEPAD_BUTTON_LEFT_THUMB: ControllerButton.LSTICK,
    glfw.GAMEPAD_BUTTON_RIGHT_THUMB: ControllerButton.RSTICK,
    glfw.GAMEPAD_BUTTON_DPAD_UP: ControllerButton.DPAD,
    glfw.GAMEPAD_BUTTON_DPAD_DOWN: ControllerButton.DPAD,
    glfw.GAMEPAD_BUTTON_DPAD_RIGHT: ControllerButton.DPAD,
    glfw.GAMEPAD_BUTTON_DPAD_LEFT: ControllerButton.DPAD
}

GLFW_CONTROLLER_DPAD_MAP = {
    glfw.HAT_CENTERED: DpadState.NEUTRAL,
    glfw.HAT_UP: DpadState.UP,
    glfw.HAT_DOWN: DpadState.DOWN,
    glfw.HAT_LEFT: DpadState.LEFT,
    glfw.HAT_RIGHT: DpadState.RIGHT,
    glfw.HAT_UP | glfw.HAT_RIGHT: DpadState.UP_RIGHT,
    glfw.HAT_UP | glfw.HAT_LEFT: DpadState.UP_LEFT,
    glfw.HAT_DOWN | glfw.HAT_RIGHT: DpadState.DOWN_RIGHT,
    glfw.HAT_DOWN | glfw.HAT_LEFT: DpadState.DOWN_LEFT,
}

GLFW_CONTROLLER_AXIS_MAP = {
    glfw.GAMEPAD_AXIS_LEFT_X: ControllerAxis.LEFT_STICK_X,
    glfw.GAMEPAD_AXIS_LEFT_Y: ControllerAxis.LEFT_STICK_Y,
    glfw.GAMEPAD_AXIS_RIGHT_X: ControllerAxis.RIGHT_STICK_X,
    glfw.GAMEPAD_AXIS_RIGHT_Y: ControllerAxis.RIGHT_STICK_Y,
    glfw.GAMEPAD_AXIS_LEFT_TRIGGER: ControllerAxis.LEFT_TRIGGER,
    glfw.GAMEPAD_AXIS_RIGHT_TRIGGER: ControllerAxis.RIGHT_TRIGGER,
}



# -------------------------------
#       >>> Functions <<<
# -------------------------------
def str_to_version(version_str, number_amount=None) -> list:
    """
    Converts a string, like 3.2 into an array of ints -> [3, 2].
    """
    numbers = [int(x) for x in re.findall(r"\d+", string=version_str)]
    
    if not number_amount:
        pass
    elif number_amount > len(numbers):
        numbers += [0]*(number_amount - len(numbers))
    elif number_amount < len(numbers):
        numbers = numbers[:number_amount]
    
    return numbers

# -------------------------------
#        >>> Classes <<<
# -------------------------------

class Event(object):
    def __init__(self, event_type, 
                 key=None, 
                 mouse_pos=None, 
                 mouse_button=None,
                 mouse_scroll=None,
                 mouse_scroll_precise=None,
                 controller_id=None, 
                 controller_button=None, 
                 controller_dpad=None,
                 axis=None, 
                 axis_value=None,
                 window_position=None,
                 window_size=None,
                 is_accessed=None,
                 is_active=None):
        self.type = event_type
        self.key = key                  # keyboard key
        self.mouse_position = mouse_pos      # (x, y)
        self.mouse_button = mouse_button
        self.mouse_scroll = mouse_scroll
        self.mouse_scroll_precise = mouse_scroll_precise
        self.controller_id = controller_id  # which controller
        self.controller_button = controller_button
        self.controller_dpad = controller_dpad
        self.axis = axis                  # axis name or index
        self.axis_value = axis_value      # axis value (-1.0 .. 1.0), triggers = 0.0 -> 1.0
        self.window_position = window_position
        self.window_size = window_size    # (width, height)
        self.is_accessed = is_accessed
        self.is_active = is_active

class InputState(object):
    def __init__(self, controller_event_tolerance=0.01, controllers={}):
        self.controller_event_tolerance = controller_event_tolerance
        self.keys = {}  # dict[int, bool]
        self.mouse_buttons = {}  # dict[int, bool]
        self.mouse_position = (0, 0)
        self.controllers = controllers  # per controller id -> Controller
        self.missed_controllers = {}
        self.window = {"position": [0, 0],
                       "size": [512, 512],
                       "accessed": True,
                       "active": True}
        self.quit = False

    def update(self, events):
        new_events = []
        for event in events:
            # Keyboard
            if event.type == EventType.KEY_DOWN:
                self.keys[event.key] = True
            elif event.type == EventType.KEY_UP:
                self.keys[event.key] = False

            # Mouse
            elif event.type == EventType.MOUSE_DOWN:
                self.mouse_buttons[event.mouse_button] = True
            elif event.type == EventType.MOUSE_UP:
                self.mouse_buttons[event.mouse_button] = False
            elif event.type == EventType.MOUSE_MOVE:
                self.mouse_position = event.mouse_position

            # Controller buttons
            elif event.type == EventType.CONTROLLER_BUTTON_DOWN:
                cid = event.controller_id
                if cid in self.controllers.keys():
                    self.controllers[cid].update_button(button=event.controller_button, pressed=True)
                else:
                    new_events += self.missing_controller_process(event=event)
            elif event.type == EventType.CONTROLLER_BUTTON_UP:
                cid = event.controller_id
                if cid in self.controllers.keys():
                    self.controllers[cid].update_button(button=event.controller_button, pressed=False)
                else:
                    new_events += self.missing_controller_process(event=event)

            # Controller axes
            elif event.type == EventType.CONTROLLER_AXIS_MOVE:
                cid = event.controller_id
                if cid in self.controllers.keys():
                    if abs(self.controllers[cid].get_axis(axis=event.axis) - event.axis_value) < self.controller_event_tolerance:
                        continue
                    self.controllers[cid].update_axis(axis=event.axis, value=event.axis_value)
                else:
                    new_events += self.missing_controller_process(event=event)
            elif event.type == EventType.CONTROLLER_ADDED:
                self.controllers[event.controller_id] = Controller(controller_id=event.controller_id)
            elif event.type == EventType.CONTROLLER_REMOVED:
                # del self.controllers[event.controller_id]
                self.controllers.pop(event.controller_id, None)

            # Window
            elif event.type == EventType.QUIT:
                self.quit = True
            elif event.type == EventType.WINDOW_MOVE:
                self.window["position"] = event.window_position
            elif event.type == EventType.WINDOW_RESIZE:
                self.window["size"] = event.window_size
            elif event.type == EventType.WINDOW_ACCESS:
                self.window["accessed"] = event.is_accessed
            elif event.type == EventType.WINDOW_ACTIVATION:
                self.window["active"] = event.is_active

            new_events += [event]
        return new_events

    def missing_controller_process(self, event):
        new_event_list = []
        cid = event.controller_id
        print(f"[WARNING] Catched Controller Event with missed Controller ID ({cid})")
        self.missed_controllers[cid] = self.missed_controllers.get(cid, 0) + 1
        if self.missed_controllers[cid] >= 3:
            new_event_list = [Event(EventType.CONTROLLER_ADDED, controller_id=cid)]
            self.controllers[cid] = Controller(controller_id=cid)
            print(f"[INFO] Wind-Forge added Controller by itself -> window backend did not added the device.")
        return new_event_list

    def get_all_active(self, as_string=False):
        active_keys = [key for key, pressed in self.keys.items() if pressed]
        active_mouse_buttons = [btn for btn, pressed in self.mouse_buttons.items() if pressed]
        print(active_mouse_buttons)

        active_controllers = {}
        for cid, controller in self.controllers.items():
            actives = controller.get_active(as_string=as_string)
            # if actives:
            active_controllers[cid] = actives

        return {
            "keys": list(map(lambda x: x.name, active_keys)) if as_string else active_keys,
            "mouse": list(map(lambda x: x.name, active_mouse_buttons)) if as_string else active_mouse_buttons,
            "controllers": active_controllers
        }



class Controller(object):
    """
    Class to represent the state of one controller.
    """
    def __init__(self, controller_id):
        self.controller_id = controller_id

        # Press Buttons -> holded or not
        self.A = False
        self.B = False
        self.X = False
        self.Y = False
        self.LB = False       # Left bumper
        self.RB = False       # Right bumper
        self.START = False
        self.SELECT = False
        self.LSTICK = False   # Left stick click
        self.RSTICK = False   # Right stick click
        self.DPAD = False
        self.dpad_state = DpadState.NEUTRAL

        # Axis -> analog values
        self.LEFT_STICK_X = 0.0
        self.LEFT_STICK_Y = 0.0
        self.RIGHT_STICK_X = 0.0
        self.RIGHT_STICK_Y = 0.0
        self.LEFT_TRIGGER = 0.0
        self.RIGHT_TRIGGER = 0.0

        # maps for lookup
        self._button_map = {
            ControllerButton.A: "A",
            ControllerButton.B: "B",
            ControllerButton.X: "X",
            ControllerButton.Y: "Y",
            ControllerButton.LB: "LB",
            ControllerButton.RB: "RB",
            ControllerButton.START: "START",
            ControllerButton.SELECT: "SELECT",
            ControllerButton.LSTICK: "LSTICK",
            ControllerButton.RSTICK: "RSTICK",
            ControllerButton.DPAD: "DPAD"
        }

        self._axis_map = {
            ControllerAxis.LEFT_STICK_X: "LEFT_STICK_X",
            ControllerAxis.LEFT_STICK_Y: "LEFT_STICK_Y",
            ControllerAxis.RIGHT_STICK_X: "RIGHT_STICK_X",
            ControllerAxis.RIGHT_STICK_Y: "RIGHT_STICK_Y",
            ControllerAxis.LEFT_TRIGGER: "LEFT_TRIGGER",
            ControllerAxis.RIGHT_TRIGGER: "RIGHT_TRIGGER"
        }

    def get_button(self, button:ControllerButton):
        attr = self._button_map.get(button)
        return getattr(self, attr) if attr else None

    def get_axis(self, axis:ControllerAxis):
        attr = self._axis_map.get(axis)
        return getattr(self, attr) if attr else None

    def update_button(self, button, pressed: bool, dpad_state=None):
        """
        Update digital button state.
        """
        attr = self._button_map.get(button)
        if attr:
            setattr(self, attr, pressed)

        if dpad_state:
            self.dpad_state = dpad_state

    def update_axis(self, axis, value: float):
        """
        Update analog axis state.
        """
        attr = self._axis_map.get(axis)
        if attr:
            setattr(self, attr, value)
    
    def get_pressed_buttons(self):
        """
        Return list of pressed buttons.
        """
        return [btn for btn, pressed in {
                                        ControllerButton.A: self.A, ControllerButton.B: self.B, 
                                        ControllerButton.X: self.X, ControllerButton.Y: self.Y,
                                        ControllerButton.LB: self.LB, ControllerButton.RB: self.RB,
                                        ControllerButton.START: self.START, ControllerButton.SELECT: self.SELECT,
                                        ControllerButton.LSTICK: self.LSTICK, ControllerButton.RSTICK: self.RSTICK,
                                        ControllerButton.DPAD: self.DPAD
                                        }.items() if pressed]

    def get_active(self, as_string=False):
        """
        Return dict of current buttons and axis values.
        """
        precision = 0.1
        active = self.get_pressed_buttons()
        active += [axis_name for axis_name, active in {
                                                        ControllerAxis.LEFT_STICK_X: -precision > self.LEFT_STICK_X or self.LEFT_STICK_X > precision,
                                                        ControllerAxis.LEFT_STICK_Y: -precision > self.LEFT_STICK_Y or self.LEFT_STICK_Y > precision,
                                                        ControllerAxis.RIGHT_STICK_X: -precision > self.RIGHT_STICK_X or self.RIGHT_STICK_X > precision,
                                                        ControllerAxis.RIGHT_STICK_Y: -precision > self.RIGHT_STICK_Y or self.RIGHT_STICK_Y > precision,
                                                        ControllerAxis.LEFT_TRIGGER: self.LEFT_TRIGGER > precision,
                                                        ControllerAxis.RIGHT_TRIGGER: self.RIGHT_TRIGGER > precision,
                                                      }.items() if active] 
        return list(map(lambda x: x.name, active)) if as_string else active
        

    def get_dpad_state(self):
        return self.dpad_state


class Window(object):
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
                print_missed_events=False):
        self.background_lib = background_lib
        
        if background_lib == WindowLib.PYGAME:
            self.backend = PygameBackend(size=size, resizable=resizable,
                                         title=title, 
                                         multisample=multisample, samples=samples, 
                                         depth_buffer=depth_buffer, gl_version=gl_version,
                                         post_process=post_process, 
                                         print_missed_events=print_missed_events)
        elif background_lib == WindowLib.GLFW:
            self.backend = GlfwBackend(size=size, resizable=resizable,
                                       title=title, 
                                       multisample=multisample, samples=samples, 
                                       depth_buffer=depth_buffer, gl_version=gl_version,
                                       post_process=post_process,
                                       print_missed_events=print_missed_events)
        else:
            raise ValueError(f"Does not know '{background_lib}' as window backend.")
        
        self.input_state = InputState(controller_event_tolerance=0.01,
                                      controllers=self.backend.get_controllers())

    def get(self):
        return self.screen

    def events(self):
        return self.input_state.update(self.backend.get_events())

    def display(self):
        self.backend.swap_buffers()

    def quit(self):
        self.backend.quit()



# Classes for the Window Background -> Window creation + Input Processing
class WindowBackend(ABC):
    def __init__(self, size, resizable, title, multisample, samples, depth_buffer, gl_version, post_process,
                 print_missed_events):
        self.size = size
        self.resizable = resizable
        self.title = title
        self.multisample = multisample
        self.samples = samples
        self.depth_buffer = depth_buffer
        self.gl_version = gl_version
        self.post_process = post_process
        self.print_missed_events = print_missed_events


    @abstractmethod
    def get_events(self):
        pass

    @abstractmethod
    def get_controllers(self):
        pass

    @abstractmethod
    def swap_buffers(self):
        pass

    @abstractmethod
    def quit(self):
        pass



class PygameBackend(WindowBackend):
    def __init__(self, size, resizable, title, multisample, samples, depth_buffer, gl_version, post_process,
                 print_missed_events):
        super().__init__(size, resizable, title, multisample, samples, depth_buffer, gl_version, post_process,
                         print_missed_events)

        # init pygame
        pygame.init()

        # use OpenGL cores
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

        # OpenGL version
        if gl_version:
            major_v, minor_v = str_to_version(version_str=gl_version, number_amount=2)
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, major_v)
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, minor_v)

        # set depth buffer size
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, depth_buffer)

        # rendering details -> via bitwise operation
        display_flags = pygame.DOUBLEBUF | pygame.OPENGL
        if resizable:
            display_flags |= pygame.RESIZABLE

        # init buffers to perform antialiasing
        if multisample:
            pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
            pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, samples)

        # set and get screen
        self.screen = pygame.display.set_mode(self.size, display_flags)
        pygame.display.set_caption(title)

        # enable controller support
        self.controllers = dict()
        pygame.joystick.init()
        # create joystick objects for each connected device
        for controller_id in range(pygame.joystick.get_count()):
            controller = pygame.joystick.Joystick(controller_id)
            controller.init()
            self.controllers[controller_id] = controller
            print(f"[INFO] Initialized joystick {controller_id}: {controller.get_name()}")

    def get_events(self):
        events = []
        for event in pygame.event.get():
            # print(f"Event detected: {event}")
            # Window
            if event.type == pygame.QUIT:
                events += [Event(event_type=EventType.QUIT)]
            elif event.type == event.type == pygame.WINDOWMOVED:
                events += [Event(event_type=EventType.WINDOW_MOVE,
                                 window_position=(event.x, event.y))]
            elif event.type == event.type == pygame.VIDEORESIZE:
                events += [Event(event_type=EventType.WINDOW_RESIZE,
                                 window_size=(event.w, event.h))]
            elif event.type == event.type == pygame.ACTIVEEVENT:  # pygame.WINDOWENTER:
                events += [Event(event_type=EventType.WINDOW_ACCESS,
                                 is_accessed=event.gain)]
            # elif event.type == event.type == pygame.WINDOWLEAVE:
            #     events += [Event(event_type=EventType.WINDOW_ACCESS,
            #                      is_accessed=False)]
            elif event.type == event.type == pygame.WINDOWFOCUSGAINED:
                events += [Event(event_type=EventType.WINDOW_ACTIVATION,
                                 is_active=True)]
            elif event.type == event.type == pygame.WINDOWFOCUSLOST:
                events += [Event(event_type=EventType.WINDOW_ACTIVATION,
                                 is_active=False)]
                
            # Keyboard
            elif event.type == pygame.KEYDOWN:
                if event.key in PYGAME_KEY_MAP:
                    events += [Event(EventType.KEY_DOWN, key=PYGAME_KEY_MAP[event.key])]
            elif event.type == pygame.KEYUP:
                if event.key in PYGAME_KEY_MAP:
                    events += [Event(EventType.KEY_UP, key=PYGAME_KEY_MAP[event.key])]

            # Mouse
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in PYGAME_MOUSE_BUTTON_MAP:
                    events += [Event(EventType.MOUSE_DOWN, mouse_button=PYGAME_MOUSE_BUTTON_MAP[event.button], mouse_pos=event.pos)]
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in PYGAME_MOUSE_BUTTON_MAP:
                    events += [Event(EventType.MOUSE_UP, mouse_button=PYGAME_MOUSE_BUTTON_MAP[event.button], mouse_pos=event.pos)]
            elif event.type == pygame.MOUSEMOTION:
                events += [Event(EventType.MOUSE_MOVE, mouse_pos=event.pos)]
            elif event.type == pygame.MOUSEWHEEL:
                events += [Event(EventType.MOUSE_WHEEL, mouse_scroll=(event.x, event.y), mouse_scroll_precise=(event.precise_x, event.precise_y))]

            # Controller
            elif event.type == pygame.JOYDEVICEADDED:
                controller = pygame.joystick.Joystick(event.device_index)
                controller.init()
                self.controllers[event.device_index] = controller
                print(f"[INFO] Joystick added: {controller.get_name()} (id={event.device_index})")
                events += [Event(EventType.CONTROLLER_ADDED, controller_id=event.device_index)]
            elif event.type == pygame.JOYDEVICEREMOVED:
                print(f"Joystick removed: id={event.instance_id}")
                del self.controllers[event.instance_id]
            elif event.type == pygame.JOYBUTTONDOWN:  #pygame.CONTROLLERBUTTONDOWN:
                if event.button in PYGAME_CONTROLLER_BUTTON_MAP:
                    events += [Event(EventType.CONTROLLER_BUTTON_DOWN,
                                     controller_id=event.instance_id,
                                     controller_button=PYGAME_CONTROLLER_BUTTON_MAP[event.button])]
            elif event.type == pygame.JOYBUTTONUP: #  pygame.CONTROLLERBUTTONUP:
                if event.button in PYGAME_CONTROLLER_BUTTON_MAP:
                    events += [Event(EventType.CONTROLLER_BUTTON_UP,
                                     controller_id=event.instance_id,
                                     controller_button=PYGAME_CONTROLLER_BUTTON_MAP[event.button])]
            elif event.type == pygame.JOYHATMOTION:
                dpad_state = PYGAME_CONTROLLER_DPAD_MAP[event.value]
                if dpad_state == DpadState.NEUTRAL:
                    events += [Event(EventType.CONTROLLER_BUTTON_UP, controller_button=ControllerButton.DPAD,
                                    controller_dpad=dpad_state, controller_id=event.instance_id)]
                else:
                    events += [Event(EventType.CONTROLLER_BUTTON_DOWN, controller_button=ControllerButton.DPAD,
                                    controller_dpad=dpad_state, controller_id=event.instance_id)]
            elif event.type == pygame.JOYAXISMOTION: # pygame.CONTROLLERAXISMOTION:
                if event.axis in PYGAME_CONTROLLER_AXIS_MAP:
                    value = event.value
                    # change value range from [-1.0, 1.0] to [0.0, 1.0]
                    if event.axis in [pygame.CONTROLLER_AXIS_TRIGGERLEFT,
                                      pygame.CONTROLLER_AXIS_TRIGGERRIGHT]:
                        value = max(0.0, (value + 1.0) / 2.0)
                    events += [Event(EventType.CONTROLLER_AXIS_MOVE,
                                     controller_id=event.instance_id,
                                     axis=PYGAME_CONTROLLER_AXIS_MAP[event.axis],
                                     axis_value=value)]
                    
            # other
            else:
                if self.print_missed_events:
                    print(f"[INFO] Event skipped: {event}")
        return events
    
    def get_controllers(self):
        controllers = {}
        for controller in self.controllers.values():
            controllers[controller.get_id()] = Controller(controller_id=controller.get_id())
        return controllers

    def swap_buffers(self):
        pygame.display.flip()

    def quit(self):
        pygame.quit()



class GlfwBackend(WindowBackend):
    def __init__(self, size, resizable, title, multisample, samples, depth_buffer, gl_version, post_process,
                 print_missed_events):
        super().__init__(size, resizable, title, multisample, samples, depth_buffer, gl_version, post_process,
                         print_missed_events)

        if not glfw.init():
            raise RuntimeError("Failed to init GLFW")

        # OpenGL Version
        if gl_version:
            major_v, minor_v = str_to_version(version_str=gl_version, number_amount=2)
            glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, major_v)
            glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, minor_v)
            glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        # MSAA -> smoothing
        if multisample:
            glfw.window_hint(glfw.SAMPLES, samples)  # Enable MSAA

        # window resizable or not
        glfw.window_hint(glfw.RESIZABLE, glfw.TRUE if resizable else glfw.FALSE)

        # create window
        self.screen = glfw.create_window(size[0], size[1], title, None, None)
        if self.screen is None:
            raise Exception("GLFW window creation failed")
        glfw.make_context_current(self.screen)

        # event queue for callbacks
        self._raw_event_queue = []
        # store previous joystick state: { cid: {"axes": tuple, "buttons": tuple, "hats": tuple } }
        self._joystick_prev = {}

        # register callbacks to capture GLFW events
        def _key_cb(window, key, scancode, action, mods):
            # action: glfw.PRESS, glfw.RELEASE, glfw.REPEAT
            self._raw_event_queue += [("key", {"key": key, "action": action, "mods": mods})]

        def _mouse_button_cb(window, button, action, mods):
            # button: glfw.MOUSE_BUTTON_LEFT etc.
            # action: glfw.PRESS / glfw.RELEASE
            x, y = glfw.get_cursor_pos(self.screen)
            self._raw_event_queue += [("mouse_button", {"button": button, "action": action, 
                                                        "pos": (int(x), int(y)), "mods": mods})]

        def _cursor_pos_cb(window, xpos, ypos):
            self._raw_event_queue += [("cursor_pos", {"pos": (int(xpos), int(ypos))})]

        def _scroll_cb(window, xoffset, yoffset):
            # store precise offsets too
            self._raw_event_queue += [("scroll", {"x": xoffset, "y": yoffset})]

        def _window_size_cb(window, width, height):
            self._raw_event_queue += [("window_resize", {"size": (width, height)})]

        def _window_pos_cb(window, xpos, ypos):
            self._raw_event_queue += [("window_move", {"pos": (xpos, ypos)})]

        def _window_focus_cb(window, focused):
            # focused == 1/True => gained, 0/False => lost
            self._raw_event_queue += [("window_focus", {"focused": bool(focused)})]

        # set callbacks
        glfw.set_key_callback(self.screen, _key_cb)
        glfw.set_mouse_button_callback(self.screen, _mouse_button_cb)
        glfw.set_cursor_pos_callback(self.screen, _cursor_pos_cb)
        glfw.set_scroll_callback(self.screen, _scroll_cb)
        glfw.set_window_size_callback(self.screen, _window_size_cb)
        glfw.set_window_pos_callback(self.screen, _window_pos_cb)
        glfw.set_window_focus_callback(self.screen, _window_focus_cb)

        # initialize joystick prev states for currently connected devices
        for cid in range(glfw.JOYSTICK_1, glfw.JOYSTICK_LAST + 1):
            if glfw.joystick_present(cid):
                axes = glfw.get_joystick_axes(cid) or ()
                buttons = glfw.get_joystick_buttons(cid) or ()
                hats = glfw.get_joystick_hats(cid) or ()
                self._joystick_prev[cid] = {
                    "axes": tuple(axes),
                    "buttons": tuple(buttons),
                    "hats": tuple(hats)
                }

    def get_events(self):
        events = []

        glfw.poll_events()

        if self.screen and glfw.window_should_close(self.screen):
            events += [Event(EventType.QUIT)]

        # convert raw queued callbacks first
        while self._raw_event_queue:
            ev_type, ev = self._raw_event_queue.pop(0)
            # Keyboard -> map GLFW key to your Key enum via GLFW_KEY_MAP
            if ev_type == "key":
                k = ev["key"]
                action = ev["action"]
                if action == glfw.PRESS:
                    if k in GLFW_KEY_MAP:
                        events.append(Event(EventType.KEY_DOWN, key=GLFW_KEY_MAP[k]))
                elif action == glfw.RELEASE:
                    if k in GLFW_KEY_MAP:
                        events.append(Event(EventType.KEY_UP, key=GLFW_KEY_MAP[k]))
                # ignore REPEAT for now (or treat as KEY_DOWN depending on your needs)

            # Mouse button
            elif ev_type == "mouse_button":
                btn = ev["button"]
                action = ev["action"]
                pos = ev["pos"]
                if action == glfw.PRESS:
                    if btn in GLFW_MOUSE_BUTTON_MAP:
                        events.append(Event(EventType.MOUSE_DOWN, mouse_button=GLFW_MOUSE_BUTTON_MAP[btn], mouse_pos=pos))
                elif action == glfw.RELEASE:
                    if btn in GLFW_MOUSE_BUTTON_MAP:
                        events.append(Event(EventType.MOUSE_UP, mouse_button=GLFW_MOUSE_BUTTON_MAP[btn], mouse_pos=pos))

            # Cursor movement
            elif ev_type == "cursor_pos":
                events.append(Event(EventType.MOUSE_MOVE, mouse_pos=ev["pos"]))

            # Scroll / wheel
            elif ev_type == "scroll":
                # you might want to provide both integer and precise values: GLFW gives float offsets
                events.append(Event(EventType.MOUSE_WHEEL,
                                    mouse_scroll=(int(ev["x"]), int(ev["y"])),
                                    mouse_scroll_precise=(ev["x"], ev["y"])))

            # Window events
            elif ev_type == "window_resize":
                events.append(Event(EventType.WINDOW_RESIZE, window_size=ev["size"]))
            elif ev_type == "window_move":
                events.append(Event(EventType.WINDOW_MOVE, window_position=ev["pos"]))
            elif ev_type == "window_focus":
                events.append(Event(EventType.WINDOW_ACTIVATION, is_active=ev["focused"]))

        # Joystick / Gamepad polling
        # iterate all possible controller ids and compare with previous snapshot
        for cid in range(glfw.JOYSTICK_1, glfw.JOYSTICK_LAST + 1):
            present = glfw.joystick_present(cid)
            prev = self._joystick_prev.get(cid)

            if present and prev is None:
                # newly added
                self._joystick_prev[cid] = {
                    "axes": tuple(glfw.get_joystick_axes(cid) or ()),
                    "buttons": tuple(glfw.get_joystick_buttons(cid) or ()),
                    "hats": tuple(glfw.get_joystick_hats(cid) or ())
                }
                events.append(Event(EventType.CONTROLLER_ADDED, controller_id=cid))

            elif not present and prev is not None:
                # removed
                del self._joystick_prev[cid]
                events.append(Event(EventType.CONTROLLER_REMOVED, controller_id=cid))

            elif present and prev is not None:
                # still present -> compare axes/buttons/hats for changes
                axes = tuple(glfw.get_joystick_axes(cid) or ())
                buttons = tuple(glfw.get_joystick_buttons(cid) or ())
                hats = tuple(glfw.get_joystick_hats(cid) or ())

                # Buttons (digital)
                # compare length carefully
                max_buttons = max(len(prev["buttons"]), len(buttons))
                for i in range(max_buttons):
                    prev_b = prev["buttons"][i] if i < len(prev["buttons"]) else 0
                    cur_b = buttons[i] if i < len(buttons) else 0
                    if prev_b != cur_b:
                        # map raw button index i to ControllerButton via GLFW_CONTROLLER_BUTTON_MAP if available
                        if i in GLFW_CONTROLLER_BUTTON_MAP:
                            mapped = GLFW_CONTROLLER_BUTTON_MAP[i]
                            if cur_b:  # pressed
                                events.append(Event(EventType.CONTROLLER_BUTTON_DOWN,
                                                    controller_id=cid,
                                                    controller_button=mapped))
                            else:      # released
                                events.append(Event(EventType.CONTROLLER_BUTTON_UP,
                                                    controller_id=cid,
                                                    controller_button=mapped))
                        else:
                            # unmapped: you might want to emit a raw event or ignore
                            if self.print_missed_events:
                                print(f"[INFO] Controller {cid} button {i} changed to {cur_b} (no mapping)")

                # Axes (analog)
                max_axes = max(len(prev["axes"]), len(axes))
                for i in range(max_axes):
                    prev_a = prev["axes"][i] if i < len(prev["axes"]) else 0.0
                    cur_a = axes[i] if i < len(axes) else 0.0
                    if type(cur_a) not in [int, float]:
                        cur_a = cur_a[0]
                    if prev_a != cur_a:
                        # normalize triggers if axis index maps to triggers
                        if i in GLFW_CONTROLLER_AXIS_MAP:
                            mapped_axis = GLFW_CONTROLLER_AXIS_MAP[i]
                            # handle triggers mapping (convert [-1,1] -> [0,1] for triggers)
                            if mapped_axis in (ControllerAxis.LEFT_TRIGGER, ControllerAxis.RIGHT_TRIGGER):
                                normalized = (cur_a + 1.0) / 2.0
                            else:
                                normalized = cur_a
                            events.append(Event(EventType.CONTROLLER_AXIS_MOVE,
                                                controller_id=cid,
                                                axis=mapped_axis,
                                                axis_value=normalized))
                        else:
                            if self.print_missed_events:
                                print(f"[INFO] Joystick {cid} axis {i} changed to {cur_a} (no mapping)")

                # DPAD (Hats)
                max_hats = max(len(prev["hats"]), len(hats))
                for i in range(max_hats):
                    prev_h = prev["hats"][i] if i < len(prev["hats"]) else (0, 0)
                    cur_h = hats[i] if i < len(hats) else (0, 0)
                    dpad_state = GLFW_CONTROLLER_DPAD_MAP.get(cur_h[0] if type(cur_h) != int else cur_h, 
                                                              DpadState.NEUTRAL)
                    if prev_h != cur_h:
                        if dpad_state == DpadState.NEUTRAL:
                            events.append(Event(EventType.CONTROLLER_BUTTON_UP,
                                                controller_id=cid,
                                                controller_button=ControllerButton.DPAD,
                                                controller_dpad=dpad_state))
                        else:
                            events.append(Event(EventType.CONTROLLER_BUTTON_DOWN,
                                                controller_id=cid,
                                                controller_button=ControllerButton.DPAD,
                                                controller_dpad=dpad_state))

                # update prev snapshot
                self._joystick_prev[cid] = {"axes": tuple(axes), "buttons": tuple(buttons), "hats": tuple(hats)}


        # else:
        #     if self.print_missed_events:
        #         print(f"[Info] Event skipped: {event}")
        return events
    
    def get_controllers(self):
        # GLFW itself doesn’t have a high-level controller API like pygame
        # FIXME -> return an empty dict
        return {}

    def swap_buffers(self):
        glfw.swap_buffers(self.screen)

    def quit(self):
        pass


