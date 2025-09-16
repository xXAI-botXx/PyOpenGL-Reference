# -------------------------------
#        >>> Imports <<<
# -------------------------------
import sys
import os
from enum import Enum, auto
from abc import ABC, abstractmethod
import re

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
    LT = auto()       # Left trigger
    RT = auto()       # Right trigger
    START = auto()
    SELECT = auto()
    LSTICK = auto()   # Left stick click
    RSTICK = auto()   # Right stick click
    DPAD_UP = auto()
    DPAD_DOWN = auto()
    DPAD_LEFT = auto()
    DPAD_RIGHT = auto()

class ControllerAxis(Enum):
    LEFT_STICK_X = auto()
    LEFT_STICK_Y = auto()
    RIGHT_STICK_X = auto()
    RIGHT_STICK_Y = auto()
    LEFT_TRIGGER = auto()
    RIGHT_TRIGGER = auto()



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
    pygame.CONTROLLER_BUTTON_A: ControllerButton.A,
    pygame.CONTROLLER_BUTTON_B: ControllerButton.B,
    pygame.CONTROLLER_BUTTON_X: ControllerButton.X,
    pygame.CONTROLLER_BUTTON_Y: ControllerButton.Y,
    pygame.CONTROLLER_BUTTON_LEFTSHOULDER: ControllerButton.LB,
    pygame.CONTROLLER_BUTTON_RIGHTSHOULDER: ControllerButton.RB,
    pygame.CONTROLLER_BUTTON_BACK: ControllerButton.SELECT,
    pygame.CONTROLLER_BUTTON_START: ControllerButton.START,
    pygame.CONTROLLER_BUTTON_LEFTSTICK: ControllerButton.LSTICK,
    pygame.CONTROLLER_BUTTON_RIGHTSTICK: ControllerButton.RSTICK,
    pygame.CONTROLLER_BUTTON_DPAD_UP: ControllerButton.DPAD_UP,
    pygame.CONTROLLER_BUTTON_DPAD_DOWN: ControllerButton.DPAD_DOWN,
    pygame.CONTROLLER_BUTTON_DPAD_LEFT: ControllerButton.DPAD_LEFT,
    pygame.CONTROLLER_BUTTON_DPAD_RIGHT: ControllerButton.DPAD_RIGHT,
}

PYGAME_CONTROLLER_AXIS_MAP = {
    pygame.CONTROLLER_AXIS_LEFTX: ControllerAxis.LEFT_STICK_X,
    pygame.CONTROLLER_AXIS_LEFTY: ControllerAxis.LEFT_STICK_Y,
    pygame.CONTROLLER_AXIS_RIGHTX: ControllerAxis.RIGHT_STICK_X,
    pygame.CONTROLLER_AXIS_RIGHTY: ControllerAxis.RIGHT_STICK_Y,
    pygame.CONTROLLER_AXIS_TRIGGERLEFT: ControllerAxis.LEFT_TRIGGER,
    pygame.CONTROLLER_AXIS_TRIGGERRIGHT: ControllerAxis.RIGHT_TRIGGER,
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
    glfw.GAMEPAD_BUTTON_DPAD_UP: ControllerButton.DPAD_UP,
    glfw.GAMEPAD_BUTTON_DPAD_DOWN: ControllerButton.DPAD_DOWN,
    glfw.GAMEPAD_BUTTON_DPAD_LEFT: ControllerButton.DPAD_LEFT,
    glfw.GAMEPAD_BUTTON_DPAD_RIGHT: ControllerButton.DPAD_RIGHT,
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
        self.axis = axis                  # axis name or index
        self.axis_value = axis_value      # axis value (-1.0 .. 1.0), triggers = 0.0 -> 1.0
        self.window_position = window_position
        self.window_size = window_size    # (width, height)
        self.is_accessed = is_accessed
        self.is_active = is_active

class InputState(object):
    def __init__(self):
        self.keys = {}  # dict[int, bool]
        self.mouse_buttons = {}  # dict[int, bool]
        self.mouse_position = (0, 0)
        self.controllers = {}  # per controller id -> axes/buttons
        self.window = {}  # dict[name, bool]
        self.quit = False

    def update(self, events):
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
                if cid not in self.controllers:
                    self.controllers[cid] = {"buttons": {}, "axes": {}}
                self.controllers[cid]["buttons"][event.controller_button] = True
            elif event.type == EventType.CONTROLLER_BUTTON_UP:
                cid = event.controller_id
                if cid not in self.controllers:
                    self.controllers[cid] = {"buttons": {}, "axes": {}}
                self.controllers[cid]["buttons"][event.controller_button] = False

            # Controller axes
            elif event.type == EventType.CONTROLLER_AXIS_MOVE:
                cid = event.controller_id
                if cid not in self.controllers:
                    self.controllers[cid] = {"buttons": {}, "axes": {}}
                self.controllers[cid]["axes"][event.axis] = event.axis_value

            # Window
            elif event.type == EventType.QUIT:
                self.quit = True
            elif event.type == EventType.WINDOW_MOVE:
                self.window["accessed"] = event.window_position
            elif event.type == EventType.WINDOW_RESIZE:
                self.window["size"] = event.window_size
            elif event.type == EventType.WINDOW_ACCESS:
                self.window["accessed"] = event.is_accessed
            elif event.type == EventType.WINDOW_ACTIVATION:
                self.window["active"] = event.is_active

    def get_all_active(self):
        active_keys = [key for key, pressed in self.keys.items() if pressed]
        active_mouse_buttons = [btn for btn, pressed in self.mouse_buttons.items() if pressed]

        active_controllers = {}
        for cid, controller in self.controllers.items():
            active_buttons = [btn for btn, pressed in controller.get("buttons", {}).items() if pressed]
            active_axes = {axis: val for axis, val in controller.get("axes", {}).items() if val != 0.0}
            if active_buttons or active_axes:
                active_controllers[cid] = {"buttons": active_buttons, "axes": active_axes}

        return {
            "keys": active_keys,
            "mouse_buttons": active_mouse_buttons,
            "mouse_position": self.mouse_position,
            "controllers": active_controllers,
            "quit": self.quit
        }


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
                background_lib=WindowLib.PYGAME):
        self.background_lib = background_lib
        
        if background_lib == WindowLib.PYGAME:
            self.backend = PygameBackend(size=size, resizable=resizable,
                                         title=title, 
                                         multisample=multisample, samples=samples, 
                                         depth_buffer=depth_buffer, gl_version=gl_version,
                                         post_process=post_process)
        elif background_lib == WindowLib.GLFW:
            self.backend = GlfwBackend(size=size, resizable=resizable,
                                       title=title, 
                                       multisample=multisample, samples=samples, 
                                       depth_buffer=depth_buffer, gl_version=gl_version,
                                       post_process=post_process)
        else:
            raise ValueError(f"Does not know '{background_lib}' as window backend.")
        
        self.input_state = InputState()

    def get(self):
        return self.screen

    def events(self):
        events = self.backend.get_events()
        self.input_state.update(events)
        return events

    def display(self):
        self.backend.swap_buffers()

    def quit(self):
        self.backend.quit()



# Classes for the Window Background -> Window creation + Input Processing
class WindowBackend(ABC):
    def __init__(self, size, resizable, title, multisample, samples, depth_buffer, gl_version, post_process):
        self.size = size
        self.resizable = resizable
        self.title = title
        self.multisample = multisample
        self.samples = samples
        self.depth_buffer = depth_buffer
        self.gl_version = gl_version
        self.post_process = post_process


    @abstractmethod
    def get_events(self):
        pass

    @abstractmethod
    def swap_buffers(self):
        pass

    @abstractmethod
    def quit(self):
        pass



class PygameBackend(WindowBackend):
    def __init__(self, size, resizable, title, multisample, samples, depth_buffer, gl_version, post_process):
        super().__init__(size, resizable, title, multisample, samples, depth_buffer, gl_version, post_process)

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

    def get_events(self):
        events = []
        for event in pygame.event.get():
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
                    events += [Event(EventType.MOUSE_DOWN, key=PYGAME_MOUSE_BUTTON_MAP[event.button], mouse_pos=event.pos)]
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in PYGAME_MOUSE_BUTTON_MAP:
                    events += [Event(EventType.MOUSE_UP, key=PYGAME_MOUSE_BUTTON_MAP[event.button], mouse_pos=event.pos)]
            elif event.type == pygame.MOUSEMOTION:
                events += [Event(EventType.MOUSE_MOVE, mouse_pos=event.pos)]
            elif event.type == pygame.MOUSEWHEEL:
                events += [Event(EventType.MOUSE_WHEEL, mouse_scroll=(event.x, event.y), mouse_scroll_precise=(event.precise_x, event.precise_y))]

            # Controller
            elif event.type == pygame.CONTROLLERBUTTONDOWN:
                if event.button in PYGAME_CONTROLLER_BUTTON_MAP:
                    events += [Event(EventType.CONTROLLER_BUTTON_DOWN,
                                     controller_id=event.instance_id,
                                     controller_button=PYGAME_CONTROLLER_BUTTON_MAP[event.button])]
            elif event.type == pygame.CONTROLLERBUTTONUP:
                if event.button in PYGAME_CONTROLLER_BUTTON_MAP:
                    events += [Event(EventType.CONTROLLER_BUTTON_UP,
                                     controller_id=event.instance_id,
                                     controller_button=PYGAME_CONTROLLER_BUTTON_MAP[event.button])]
            elif event.type == pygame.CONTROLLERAXISMOTION:
                if event.axis in PYGAME_CONTROLLER_AXIS_MAP:
                    events += [Event(EventType.CONTROLLER_AXIS_MOVE,
                                     controller_id=event.instance_id,
                                     axis=PYGAME_CONTROLLER_AXIS_MAP[event.axis],
                                     axis_value=event.value)]
                    
            # other
            else:
                print(f"Event skipped: {event}\n      -> Event Type: {event.type}")
        return events

    def swap_buffers(self):
        pygame.display.flip()

    def quit(self):
        pygame.quit()



class GlfwBackend(WindowBackend):
    def __init__(self, size, resizable, title, multisample, samples, depth_buffer, gl_version, post_process):
        super().__init__(size, resizable, title, multisample, samples, depth_buffer, gl_version, post_process)

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

    def get_events(self):
        events = []
        glfw.poll_events()
        if self.screen and glfw.window_should_close(self.screen):
            events += [Event(EventType.QUIT)]
        return events

    def swap_buffers(self):
        glfw.swap_buffers(self.screen)

    def quit(self):
        pass


