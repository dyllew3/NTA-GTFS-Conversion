class MockResponse:
    def __init__(self, data, status_code):
        self.data = data
        self.status_code = status_code

    @property
    def json(self):
        return self.data
    
    @property
    def ok(self):
        return self.status_code == 200

    @property
    def content(self):
        return self.data