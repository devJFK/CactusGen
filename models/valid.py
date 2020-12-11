class Valid:
    def __init__(self, code, company):
        self.code = code
        self.company = company
        self.capture = {}

    def add_capture(self, key, value):
        self.capture.update({key:value})

    def get_value(self):
        return f'{self.code} | ' + ' | '.join(f'{k}: {v}' for k,v in self.capture.items())