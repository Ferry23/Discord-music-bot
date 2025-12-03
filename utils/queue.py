from collections import deque
import random

class MusicQueue:
    def __init__(self):
        self.queue = deque()
        self.repeat_mode = 'off'  # 'off', 'one', 'all'
        self.history = deque(maxlen=50)
        self.shuffled = False
        self.original_queue = None

    def add_track(self, track_info):
        self.queue.append(track_info)

    def get_next(self):
        if self.queue:
            track = self.queue.popleft()
            self.add_to_history(track)
            if self.repeat_mode == 'all' and not self.is_empty():
                self.queue.append(track)
            return track
        return None

    def clear(self):
        self.queue.clear()
        self.shuffled = False
        self.original_queue = None

    def get_queue(self):
        return list(self.queue)

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)

    def remove_at(self, index):
        if 0 <= index < len(self.queue):
            del self.queue[index]
            return True
        return False

    def shuffle(self):
        if not self.shuffled:
            self.original_queue = list(self.queue)
            random.shuffle(self.queue)
            self.shuffled = True
        else:
            if self.original_queue:
                self.queue = deque(self.original_queue)
            self.shuffled = False

    def set_repeat(self, mode):
        self.repeat_mode = mode

    def add_to_history(self, track):
        self.history.append(track)

    def get_history(self):
        return list(self.history)