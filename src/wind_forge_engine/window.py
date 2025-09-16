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
    QUIT = auto()
    KEYDOWN = auto()
    KEYUP = auto()
    MOUSEMOVE = auto()
    MOUSEDOWN = auto()
    MOUSEUP = auto()
    CONTROLLERBUTTONDOWN = auto()
    CONTROLLERBUTTONUP = auto()
    CONTROLLERAXISMOVE = auto()
    WINDOWRESIZE = auto()
    # FIXME



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

class Event:
    def __init__(self, event_type, 
                 key=None, 
                 mouse_pos=None, 
                 mouse_button=None,
                 controller_id=None, 
                 controller_button=None, 
                 axis=None, 
                 axis_value=None,
                 window_size=None):
        self.type = event_type
        self.key = key                  # keyboard key
        self.mouse_pos = mouse_pos      # (x, y)
        self.mouse_button = mouse_button
        self.controller_id = controller_id  # which controller
        self.controller_button = controller_button
        self.axis = axis                  # axis name or index
        self.axis_value = axis_value      # axis value (-1.0 .. 1.0)
        self.window_size = window_size    # (width, height)

class Window(object):
    def __init__(self, size=[512, 512],
                title="Interactive Computer-Graphics Application with Wind-Forge",
                multisample=True, 
                samples=4, 
                depth_buffer=24, 
                gl_version=None, 
                post_process=[],
                background_lib=WindowLib.PYGAME):
        self.background_lib = background_lib
        
        if background_lib == WindowLib.PYGAME:
            self.backend = PygameBackend(size=size, title=title, 
                                         multisample=multisample, samples=samples, 
                                         depth_buffer=depth_buffer, gl_version=gl_version,
                                         post_process=post_process)
        elif background_lib == WindowLib.GLFW:
            self.backend = GlfwBackend(size=size, title=title, 
                                       multisample=multisample, samples=samples, 
                                       depth_buffer=depth_buffer, gl_version=gl_version,
                                       post_process=post_process)
        else:
            raise ValueError(f"Does not know '{background_lib}' as window backend.")

    def get(self):
        return self.screen

    def events(self):
        return self.backend.get_events()

    def display(self):
        self.backend.swap_buffers()

    def quit(self):
        self.backend.quit()



# Classes for the Window Background -> Window creation + Input Processing
class WindowBackend(ABC):
    def __init__(self, size, title, multisample, samples, depth_buffer, gl_version, post_process):
        self.size = size
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
    def __init__(self, size, title, multisample, samples, depth_buffer, gl_version, post_process):
        super().__init__(size, title, multisample, samples, depth_buffer, gl_version, post_process)

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

        # init buffers to perform antialiasing
        if multisample:
            pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
            pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, samples)

        # set and get screen
        self.screen = pygame.display.set_mode(self.size, display_flags)
        pygame.display.set_caption(title)

    def get_events(self):
        events = []
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                events += [Event(EventType.QUIT)]
            elif e.type == pygame.KEYDOWN:
                events += [Event(EventType.KEYDOWN, key=e.key)]
        return events

    def swap_buffers(self):
        pygame.display.flip()

    def quit(self):
        pygame.quit()



class GlfwBackend(WindowBackend):
    def __init__(self, size, title, multisample, samples, depth_buffer, gl_version, post_process):
        super().__init__(size, title, multisample, samples, depth_buffer, gl_version, post_process)

        if not glfw.init():
            raise RuntimeError("Failed to init GLFW")

        if gl_version:
            major_v, minor_v = str_to_version(version_str=gl_version, number_amount=2)
            glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, major_v)
            glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, minor_v)
            glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

        if multisample:
            glfw.window_hint(glfw.SAMPLES, samples)  # Enable MSAA

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


