# Implement a class to hold room information. This should have name and
# description attributes.
class Room:
    def __init__(self, name, description, items = []):
        self.name = name
        self.description = description
        self.items = items
    def item_drop (self, item):
        self.items = self.items + [item]
    def item_pickup(self, item):
        for index, instance in enumerate(self.items):
            if (instance.name == item):
                self.items = self.items[:index] + self.items[index+1:]
                return instance
                