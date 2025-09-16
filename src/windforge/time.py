# -------------------------------
#        >>> Imports <<<
# -------------------------------
import time



# -------------------------------
#        >>> Classes <<<
# -------------------------------
class Clock(object):
    """
    Clock to keep the same FPS.
    Return the delta time (time duration since the last frame),
    which can be used for updating frame independent.
    Also waits to achieve a fix FPS if faster.

    Directly starts the frame timer.

    Parameters:
        goal_fps (int): Goal FPS to keep in seconds.
    """
    def __init__(self, goal_fps):
        self.goal_fps = goal_fps
        self.frame_time = 0
        self.start_time = time.perf_counter()
        self.last_frames = list()

    def set_fps(self, new_fps):
        """
        Update the goal FPS to keep.

        Parameters:
            new_fps(int): New FPS in seconds.
        """
        self.goal_fps = new_fps

    # aliase: update, tick
    def tick(self):
        """
        Call this at the end of a frame. 
        Will wait to reach the goal FPS and
        also return the frame time (the time
        needed since the last frame).

        Returns:
            delta (float): Seconds needed for the current frame.
        """
        # Calculate frame time (delta)
        now = time.perf_counter()
        self.frame_time = now - self.start_time

        # update history queue
        if len(self.last_frames) >= 8:
            self.last_frames.pop(0)
        self.last_frames += [self.frame_time]
        
        # check if frame was too fast
        frame_duration = 1 / self.goal_fps
        if self.frame_time < frame_duration:
            time.sleep(frame_duration - self.frame_time)
        self.start_time = time.perf_counter()
        return self.frame_time

    def get_fps(self):
        """
        Returns the current FPS. Uses the average of the last 8 frame times.
        """
        if len(self.last_frames) > 0:
            return sum( (1 / t if t > 0 else 0) for t in self.last_frames) / len(self.last_frames)
        else:
            return 0
        # return 1 / self.frame_time if self.frame_time > 0 else 0



class Timer(object):
    def __init__(self, call_func, seconds_to_wait=0, frames_to_wait=0):
        self.call_func = call_func
        self.seconds_to_wait = seconds_to_wait
        self.frames_to_wait = frames_to_wait
        self.waited_frames = 0
        self.waited_seconds = 0
        self.last_time = time.perf_counter()
        self.finish = False

    # aliase: update, tick
    def tick(self):
        second_timer_finish = self.seconds_to_wait < self.waited_seconds
        frame_timer_finish = self.frames_to_wait < self.waited_frames
        if not self.finish and second_timer_finish and frame_timer_finish:
            self.call_func()
            self.finish = True
        elif not second_timer_finish:
            now = time.perf_counter()
            self.waited_seconds += now - self.last_time
        elif not frame_timer_finish:
            self.waited_frames += 1

    def get_left_seconds(self):
        return max(0.0, self.seconds_to_wait - self.waited_seconds)

    def get_left_frames(self):
        return max(0, self.frames_to_wait - self.waited_frames)

