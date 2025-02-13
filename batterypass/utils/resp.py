class Resp:
    def __init__(self, status, message=None, data=None):
        self.status = status
        self.message = message
        self.data = data
    
    def __str__(self):
        return f"Resp(status={self.status}, message={self.message}, data={self.data})"