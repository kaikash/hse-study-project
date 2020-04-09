class Measurement:
    def __init__(self, data):
        self.data = data
        self.time = data[0]
        self.acceleration = data[1:4]
        self.rotation = data[4:7]
        self.rotationRate = data[7:10]
        self.orientation = data[10]

