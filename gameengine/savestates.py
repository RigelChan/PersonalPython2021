import json


class Savestates:
    def __init__(self):
        self.data = None

    def open_save(self):
        with open('save.json', 'r') as d:
            self.data = json.load(d)
            d.close()

    def close_save(self):
        with open('save.json', 'w') as d:
            json.dump(self.data, d, indent=4)
            d.close()
