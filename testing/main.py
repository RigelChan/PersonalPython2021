from second import ModifyFruitType


class Fruit:
    def __init__(self):
        self.type = "apple"
        self.modifyfruit = ModifyFruitType()

    def update(self):
        self.modifyfruit.update(self)

apple = Fruit()
apple.update()


print(apple.type)