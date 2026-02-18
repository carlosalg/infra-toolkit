import time

def format_duration(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60 )
    secs = int(seconds % 60)

    if hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    elif minutes > 0:
        return f"{minutes}m {secs}s"
    else:
        return f"{secs}s"
    
class ScanTimer:
    def __init__(self):
        self.start_time = time.time()
        self.phases = {}
        self.current_phase = None
        self.phase_start = None

    def start_phase(self, phase_name):
        if self.current_phase:
            self.end_phase()
        
        self.current_phase = phase_name
        self.phase_start = time.time()

    def end_phase(self):
        if self.current_phase:
            elapsed = time.time() - self.phase_start
            self.phases[self.current_phase] = round(elapsed, 2)
            self.current_phase = None

    def get_total(self):
        return round(time.time() - self.start_time, 2)

    def get_summary(self):
        if self.current_phase:
            self.end_phase()
        return {
            "total_seconds": self.get_total(),
            "total_formatted": format_duration(self.get_total()),
            "phases": self.phases
        }

