class SystemState:
    def __init__(self):
        self._state = {
            "system_state": False,
            "model1": False,
            "model2": False,
        }

    def is_running(self, name: str) -> bool:
        if name not in self._state:
            raise ValueError(f"'{name}' tidak dikenal di system state.")
        return self._state[name]

    def set_running(self, name: str, value: bool):
        if name not in self._state:
            raise ValueError(f"'{name}' tidak dikenal di system state.")
        self._state[name] = value

    def set_multiple(self, states: dict[str, bool]):
        for name, value in states.items():
            self.set_running(name, value)

    def get_all_status(self) -> dict[str, bool]:
        mapping = {
            "system_state": "System",
            "model1": "Model1",
            "model2": "Model2",
        }
        return {
            f"is{mapping.get(key, key).capitalize()}Running": val
            for key, val in self._state.items()
        }

# Singleton instance
system_state = SystemState()
