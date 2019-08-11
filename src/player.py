# Write a class to hold player information, e.g. what room they are in
# currently.
class Player:
    def __init__(self, name, current_room):
        self.name = name
        self.current_room = current_room
        self.inventory = []
    def get_item(self, item):
        self.inventory = self.inventory + [item]
    def drop_item(self, item):
        for index, instance in enumerate(self.inventory):
            if (instance.name == item):
                self.inventory = self.inventory[:index] + self.inventory[index+1:]
                return instance