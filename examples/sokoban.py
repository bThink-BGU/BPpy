import bppy as bp
import itertools
import pygame
import time


# defining utility functions
def action_to_new_location(action, i, j):
    if action == "Up":
        return i - 1, j
    if action == "Down":
        return i + 1, j
    if action == "Left":
        return i, j - 1
    if action == "Right":
        return i, j + 1


def event_to_new_location(event):
    return action_to_new_location(action=event.name, **event.data)


def event_to_2_steps_trajectory(event):
    i, j = event_to_new_location(event)
    return event_to_new_location(bp.BEvent(event.name, {"i": i, "j": j}))


def new_location_to_events(i, j):
    return [bp.BEvent("Up", {"i": i+1, "j": j}),
            bp.BEvent("Down", {"i": i-1, "j": j}),
            bp.BEvent("Left", {"i": i, "j": j+1}),
            bp.BEvent("Right", {"i": i, "j": j-1})]


def is_adjacent(l1, l2):
    terms = list()
    terms.append(l1[0] == l2[0] and l1[1] == l2[1]+1)
    terms.append(l1[0] == l2[0] and l1[1] == l2[1]-1)
    terms.append(l1[0] == l2[0]+1 and l1[1] == l2[1])
    terms.append(l1[0] == l2[0]-1 and l1[1] == l2[1])
    return sum(terms) == 1


def find_adjacent_objects(list_1, list_2):
    return [(l1, l2) for l1 in list_1 for l2 in list_2 if is_adjacent(l1, l2)]


def find_adjacent_boxes(location, l):
    return [(location, l2) for l2 in l if is_adjacent(location, l2)]


def block_action(neighbors_list):
    def predicate(event):
        p1 = event_to_new_location(event)
        p2 = event_to_2_steps_trajectory(event)
        return (p1, p2) in neighbors_list or (p2, p1) in neighbors_list
    return predicate


def find(map, ch):
    return [(i, j) for i, row in enumerate(map) for j, c in enumerate(row) if c == ch]

# defining b-threads
@bp.thread
def player(i, j):
    directions = ["Up", "Down", "Left", "Right"]
    while True:
        e = yield bp.sync(request=[bp.BEvent(d, {"i": i, "j": j}) for d in directions])
        i, j = event_to_new_location(e)

@bp.thread
def wall():
    global walls_list
    block_list = list(itertools.chain(*[new_location_to_events(i, j) for i, j in walls_list]))  # use event_to_new_location(e)
    yield bp.sync(block=block_list)

@bp.thread
def boxes():
    global box_list, walls_list, target_list
    while True:
        neighbors_list = find_adjacent_objects(box_list, walls_list) + \
                         find_adjacent_objects(box_list, box_list)
        double_object_movement = bp.EventSet(block_action(neighbors_list))
        e = yield bp.sync(block=double_object_movement, waitFor=bp.All())
        new_player_location = event_to_new_location(e)
        if new_player_location in box_list:
            new_box_location = event_to_2_steps_trajectory(e)
            box_list.remove(new_player_location)
            box_list.append(new_box_location)

@bp.thread
def box(i, j):
    global box_list, walls_list, target_list
    while True:
        neighbors_list = find_adjacent_boxes((i, j), walls_list) + \
                         find_adjacent_boxes((i, j), box_list)
        double_object_movement = bp.EventSet(block_action(neighbors_list))
        e = yield bp.sync(block=double_object_movement, waitFor=bp.All())
        new_player_location = event_to_new_location(e)
        if new_player_location == (i, j):
            new_box_location = event_to_2_steps_trajectory(e)
            box_list.remove(new_player_location)
            box_list.append(new_box_location)
            i, j = new_box_location



@bp.thread
def map_printer(map):
    main_surface = pygame.display.set_mode((32 * len(map[0]), 32 * len(map)))
    count = 0
    while True:
        # Look for an event from keyboard, mouse, joystick, etc.
        ev = pygame.event.poll()
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break
        # Completely redraw the surface, starting with background
        main_surface.fill((255, 255, 255))
        for i in range(len(map)):
            for j in range(len(map[i])):
                # Copy map to surface
                pygame.draw.rect(main_surface, map_dict[map[i][j]], pygame.Rect(j * 32, i * 32, j * 32 + 32, i * 32 + 32))
        # Now that everything is drawn, put it on display!
        pygame.display.flip()
        time.sleep(0.3)
        # print(count)
        count += 1

        e = yield bp.sync(waitFor=bp.All())

        map = ",".join(map).replace("a", " ").split(",")
        map = ",".join(map).replace("A", "t").split(",")
        i, j = event_to_new_location(e)
        if map[i][j] == "b" or map[i][j] == "B":
            i2, j2 = event_to_2_steps_trajectory(e)
            if map[i2][j2] == "t":
                map[i2] = map[i2][:j2] + "B" + map[i2][j2 + 1:]
            else:
                map[i2] = map[i2][:j2] + "b" + map[i2][j2 + 1:]
            if map[i][j] == "b":
                map[i] = map[i][:j] + "a" + map[i][j + 1:]
            else:
                map[i] = map[i][:j] + "A" + map[i][j + 1:]
        elif map[i][j] == "t":
            map[i] = map[i][:j] + "A" + map[i][j + 1:]
        else:
            map[i] = map[i][:j] + "a" + map[i][j + 1:]


# definition of lists to store the locations of walls, boxes, and targets in the game map.
walls_list = []
box_list = []
target_list = []


# definition of a dictionary mapping the elements of the game to their color representation in the Pygame window.
map_dict = {
    " ": (0,0,0),
    "X": (153,76,0),
    "b": (255,178,102),
    "B": (255,229,204),
    "a": (255,255,255),
    "A": (204,255,204),
    "t": (0,204,0)
}


def init_bprogram():  # initializes the BProgram with the corresponding b-threads for the provided map.
    global walls_list, box_list, target_list
    map = [
        "XXXXXXXX",
        "XX   t X",
        "Xab bX X",
        "X b t  X",
        "XXXXt  X",
        "XXXXXXXX",
        "XXXXXXXX",
        "XXXXXXXX"
    ]
    walls_list = find(map, "X")
    box_list = find(map, "b") + find(map, "B")
    empty_target_list = find(map, "t") + find(map, "A")
    full_target_list = find(map, "B")
    target_list = empty_target_list + full_target_list
    player_locations = find(map, "a") + find(map, "A")
    player_location = player_locations[0]

    bthreads_list = [map_printer(map)] + [player(*player_location), wall()] + [box(*l) for l in box_list]
    return bp.BProgram(bthreads=bthreads_list, event_selection_strategy=bp.SimpleEventSelectionStrategy())

# initialize a b-program instance and run.
init_bprogram().run()