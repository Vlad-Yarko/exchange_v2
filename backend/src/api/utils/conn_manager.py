from collections import defaultdict


class ConnectionManager:
    def __init__(self):
        self.active_connections = defaultdict(set)
        self.active_tasks = defaultdict(str)


connection_manager = ConnectionManager()
