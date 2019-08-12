from room import Room
from player import Player
from item import Item, LightSource

# Declare all the rooms

room = {
    'outside':  Room("Outside Cave Entrance",
                     "North of you, the cave mount beckons", False, [Item('sword', 'A bladed weapon for a less civilized age.'), LightSource('lamp', 'A convenient source of light.')]),

    'foyer':    Room("Foyer", """Dim light filters in from the south. Dusty
passages run north and east."""),

    'overlook': Room("Grand Overlook", """A steep cliff appears before you, falling
into the darkness. Ahead to the north, a light flickers in
the distance, but there is no way across the chasm."""),

    'narrow':   Room("Narrow Passage", """The narrow passage bends here from west
to north. The smell of gold permeates the air.""", False),

    'treasure': Room("Treasure Chamber", """You've found the long-lost treasure
chamber! Sadly, it has already been completely emptied by
earlier adventurers. The only exit is to the south."""),
}


# Link rooms together

room['outside'].n_to = room['foyer']
room['foyer'].s_to = room['outside']
room['foyer'].n_to = room['overlook']
room['foyer'].e_to = room['narrow']
room['overlook'].s_to = room['foyer']
room['narrow'].w_to = room['foyer']
room['narrow'].n_to = room['treasure']
room['treasure'].s_to = room['narrow']

#
# Main
#

# Make a new player object that is currently in the 'outside' room.

# Write a loop that:
#
# * Prints the current room name
# * Prints the current description (the textwrap module might be useful here).
# * Waits for user input and decides what to do.
#
# If the user enters a cardinal direction, attempt to move to the room there.
# Print an error message if the movement isn't allowed.
#
# If the user enters "q", quit the game.
new_player = Player('Test', room['outside'])
current_input = None

def handle_input(input):
    inputs = input.split(' ')
    cardinals = {
        'n': 'n',
        'north': 'n',
        'e': 'e',
        'east': 'e',
        's': 's',
        'south': 's',
        'w': 'w',
        'west': 'w',
    }
    if (len(inputs) == 2):
        [verb, noun] = inputs
        if (verb == 'get' or verb == 'take'):
            handle_retrieve_item(noun) if player_can_see() else print('Good luck finding that in the dark!')
        elif(verb == 'drop'):
            handle_drop_item(noun)
        elif(verb == 'go' or verb == 'walk' or verb == 'travel' or verb == 'move'):
            print('Please enter a valid direction') if cardinals.get(noun) == None else handle_move(cardinals.get(noun))
        else:
            print(f'I don\'t recognize the verb "{verb}"')
    elif(len(inputs) == 1):
        room_items = list(map(lambda item: item.name, new_player.current_room.items))
        if (cardinals.get(inputs[0]) != None):
            handle_move(inputs[0])
        elif (inputs[0] in room_items):
            if (player_can_see()):
                handle_retrieve_item(inputs[0])
            else:
                print('Please enter valid input.')
        elif (inputs[0] == 'i' or inputs[0] == 'inventory'):
            inventory = list(map(lambda item: item.name, new_player.inventory))
            inventory_list = ', '.join(inventory)
            print('You don\'t have any items') if len(inventory) == 0 else print(f'The following items are in your inventory: {inventory_list}')
        else:
            print('Please enter valid input.')
    else:
        print('Please enter valid input')

def handle_move(dir):
    try:
        new_player.current_room = getattr(new_player.current_room, f'{dir}_to')
    except AttributeError:
        print(f'There is no room in that direction.')

def handle_retrieve_item(item):
    room_items = new_player.current_room.items
    found = False
    for instance in room_items:
        if (instance.name == item):
            found = True
    if (not found):
        return print(f'You cannot find {item}.')
    retrieved_item = new_player.current_room.item_pickup(item)
    new_player.get_item(retrieved_item)
    retrieved_item.on_take()

def handle_drop_item(item):
    inventory = new_player.inventory
    found = False
    for instance in inventory:
        if (instance.name == item):
            found = True
    if (not found):
        return print(f'You don\'t have a {item} to drop.')
    dropped_item = new_player.drop_item(item)
    new_player.current_room.item_drop(dropped_item)
    dropped_item.on_drop()

def player_can_see():
    room = new_player.current_room
    inventory = new_player.inventory
    light_source_present = False
    for item in inventory:
        if (isinstance(item, LightSource)):
            light_source_present = True
    if (not light_source_present):
        for item in room.items:
            if (isinstance(item, LightSource)):
                light_source_present = True
    return room.is_light or light_source_present

while (current_input != 'q'):
    print(new_player.current_room.name)
    if (player_can_see()):
        print(new_player.current_room.description)
        items = list(map(lambda item: item.name, new_player.current_room.items))
        item_list = ', '.join(items)
        item_output = f'You see the following items: {item_list}.' if item_list != '' else 'You do not see any items.'
        print(item_output)
    else:
        print('It\'s pitch black!')
    print('What will you do?')
    current_input = input()
    print('\n')
    if (current_input != 'q'):
        handle_input(current_input)
print('Thank you for playing!')