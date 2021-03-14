class Compare:
    def __init__(self, log_item):
        self.time = log_item['created_at'][-8:]
        self.hour = int(self.time[:2])
        self.minute = int(self.time[3:5])
        self.second = int(self.time[6:])

    def __lt__(self, other):
        if self.hour != other.hour:
            return self.hour < other.hour
        elif self.hour == other.hour:
            if self.minute != other.minute:
                return self.minute < other.minute
            return self.second < other.second

    def __gt__(self, other):
        if self.hour != other.hour:
            return self.hour > other.hour
        elif self.hour == other.hour:
            if self.minute != other.minute:
                return self.minute > other.minute
            return self.second > other.second
