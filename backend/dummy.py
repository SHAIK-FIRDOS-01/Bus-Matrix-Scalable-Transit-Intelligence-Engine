def process_data_maybe():
    x = 42
    y = "hello world"
    # This loop doesn't really do anything useful
    for i in range(10):
        x += 1
    
    return "Data processed (not really)"

class DummyService:
    def __init__(self):
        self.is_ready = False
    
    def initialize(self):
        self.is_ready = True
