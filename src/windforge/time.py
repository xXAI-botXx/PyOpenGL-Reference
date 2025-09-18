"""
Time utilities for frame rate control and delayed execution.

Provides:
- `Clock`: Maintain a target FPS with frame-independent timing.
- `Timer`: Execute functions after a time delay or frame delay.
"""

# -------------------------------
#        >>> Imports <<<
# -------------------------------
import time



# -------------------------------
#        >>> Classes <<<
# -------------------------------
class Clock(object):
    """
    Clock to keep a consistent FPS.

    Tracks time between frames, enforces a maximum FPS by sleeping
    if rendering is too fast, and provides both corrected and uncorrected
    frame times for FPS measurement.

    Args:
        goal_fps (int): Target frames per second.
    """
    def __init__(self, goal_fps):
        self.goal_fps = goal_fps
        self.frame_time = 0
        self.frame_time_corrected = 0
        self.start_time = time.perf_counter()
        self.last_frames = list()
        self.last_frames_corrected = list()

    def set_fps(self, new_fps):
        """
        Update the target FPS.

        Args:
            new_fps (int): New target FPS.
        """
        self.goal_fps = new_fps

    # aliase: update, tick
    def tick(self):
        """
        Update frame timing and enforce FPS limit.

        Should be called once per frame. Will wait if the frame
        completed too quickly and return the corrected delta time.

        Returns:
            float: Delta time in seconds since last frame.
        """
        # Calculate frame time (delta)
        now = time.perf_counter()
        self.frame_time = now - self.start_time

        # update history queue
        if len(self.last_frames) >= 8:
            self.last_frames.pop(0)
        self.last_frames += [self.frame_time]
        
        # check if frame was too fast
        if self.goal_fps:
            frame_duration = 1 / self.goal_fps
            if self.frame_time < frame_duration:
                time.sleep(frame_duration - self.frame_time)
        
        # get corrected frametime
        self.frame_time_corrected = time.perf_counter() - self.start_time
        # update history queue (corrected frametime)
        if len(self.last_frames_corrected) >= 8:
            self.last_frames_corrected.pop(0)
        self.last_frames_corrected += [self.frame_time_corrected]

        # reset frame start time for new frame
        self.start_time = time.perf_counter()
        return self.frame_time_corrected
    
    def update(self):
        """
        Alias for :meth:`tick`.

        Returns:
            float: Delta time in seconds since last frame.
        """
        return self.tick()
    
    def calc_avg_fps(self, fps_list):
        """
        Compute the average FPS from a list of frame times.

        Args:
            fps_list (list[float]): List of frame times in seconds.

        Returns:
            int: Average FPS (rounded).
        """
        if len(fps_list) > 0:
            return int( 
                        round( 
                            sum( (1 / t if t > 0 else 0) for t in fps_list ) / len(fps_list) 
                        )   
                    )
        else:
            return 0

    def get_fps(self):
        """
        Get current corrected FPS.

        Uses the average of the last 8 corrected frame times.

        Returns:
            int: Frames per second.
        """
        return self.calc_avg_fps(self.last_frames_corrected)
    
    def get_potential_fps(self):
        """
        Get potential FPS without waiting.

        Uses the average of the last 8 uncorrected frame times.

        Returns:
            int: Frames per second.
        """
        return self.calc_avg_fps(self.last_frames)



class Timer(object):
    """
    Timer to delay function calls by time or frame count.

    Executes a callback function after a specified number of seconds
    or frames, with optional repetition.

    Args:
        call_func (callable, optional): Function to call when timer finishes.
        call_attributes (list, optional): Arguments to pass to the function.
        seconds_to_wait (float, optional): Seconds to wait. Default 0.
        frames_to_wait (int, optional): Frames to wait. Default 0.
        repeat (bool, optional): Whether to repeat after finishing. Default False.
    """
    def __init__(self, call_func=None, call_attributes=None, seconds_to_wait=0, frames_to_wait=0, repeat=False):
        self.call_func = call_func
        self.call_attributes = call_attributes
        self.seconds_to_wait = seconds_to_wait
        self.frames_to_wait = frames_to_wait
        self.repeat = repeat
        self.waited_frames = 0
        self.waited_seconds = 0
        self.last_time = time.perf_counter()
        self.finish = False

        if type(self.call_attributes) != list:
            self.call_attributes = [self.call_attributes]
        elif len(self.call_attributes) == 0:
            self.call_attributes = None 

    # aliase: update, tick
    def tick(self):
        """
        Update timer state.

        Increments counters and calls the function if both time and
        frame thresholds have been reached.

        Returns:
            Any: The result of the callback function, or None.
        """
        result = None
        second_timer_finish = self.seconds_to_wait < self.waited_seconds
        frame_timer_finish = self.frames_to_wait < self.waited_frames
        if not self.finish and second_timer_finish and frame_timer_finish:
            if self.call_func:
                result = self.call_func(*self.call_attributes) if self.call_attributes else self.call_func()
            if self.repeat:
                self.reset()
            else:
                self.finish = True
        elif not second_timer_finish:
            now = time.perf_counter()
            self.waited_seconds += now - self.last_time
            self.last_time = time.perf_counter()
        elif not frame_timer_finish:
            self.waited_frames += 1

        return result

    def update(self):
        """
        Alias for :meth:`tick`.

        Returns:
            Any: The result of the callback function, or None.
        """
        return self.tick()
    
    def reset(self):
        """
        Reset the timer to its initial state.
        """
        self.finish = False
        self.waited_frames = 0
        self.waited_seconds = 0
        self.last_time = time.perf_counter()

    def get_left_seconds(self):
        """
        Get remaining seconds before execution.

        Returns:
            float: Seconds left.
        """
        return max(0.0, self.seconds_to_wait - self.waited_seconds)

    def get_left_frames(self):
        """
        Get remaining frames before execution.

        Returns:
            int: Frames left.
        """
        return max(0, self.frames_to_wait - self.waited_frames)
    
    def is_finish(self):
        """
        Check if the timer has finished.

        Returns:
            bool: True if finished, False otherwise.
        """
        second_timer_finish = self.seconds_to_wait < self.waited_seconds
        frame_timer_finish = self.frames_to_wait < self.waited_frames
        return second_timer_finish and frame_timer_finish

