from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map≥
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']


def bfs(starting_vertex):
    q = []
    visit = []
    path = [starting_vertex]
    travel = []
    q.append(path)
    # is the node in graph
    # while queue isn't empty
    while len(q) > 0:
        # dequeue the node at the front of the line
        current_path = q.pop(0)
        # print("current path", current_path)
        current_node = current_path[-1]
        # print(current_node, "starting node")
        # print("current_node bfs", current_node)
    # if this node is a target node, return true
        if has_exits(current_node):
            # print("current_path return", current_path)
            # traversal_path.extend(travel)
            return current_path

            # return current_path
        if current_node not in visit:
            visit.append(current_node)
            # neighbors = 
            neighbors = [i for i in graph[current_node]]
            # print("neighbors", neighbors)
            for i in neighbors:
                # if graph[current_node][i] < current_node:
                # print("available", current_path + [graph[current_node][i]])
                q.append(current_path + [graph[current_node][i]])
                # else:
                #     continue
        # else:
        #     print("BAHAHA", has_exits(current_node))


def has_exits(vertex):
    free = []
    for key, value in graph[vertex].items():
        # print(key, value, "vertex", vertex)
        if value == "?":
            free.append(key)
    if len(free) > 0:
        # print("free", free)
        return free
    return False


traversal_path = []
graph = {}
current = player.current_room.id
visited = []
nodes = []
last = ''

s = []
s.append(current)
print(current, "current")
print(len(world.rooms))

while len(visited) != len(world.rooms):
    vertex = s.pop()
    nodes.append(vertex)
    # print("vertex", vertex)
    exits = player.current_room.get_exits()
    index = random.randint(0, len(exits)-1)
    random_dir = exits[index]
    free_exits = []

    if vertex not in visited:
        graph[vertex] = {}
        visited.append(vertex)
        # print("visited", visited)
        for i in exits:
            graph[vertex][i] = "?"
        if len(traversal_path) > 0:
            last = traversal_path[-1]
            # print("traversal path", traversal_path)
            # print("Nodes", nodes)
            if last == "n":
                if graph[vertex]['s'] == "?":
                    graph[vertex]['s'] = nodes[-2]
            elif last == "s":
                if graph[vertex]['n'] == "?":
                    graph[vertex]['n'] = nodes[-2]
            elif last == "w":
                if graph[vertex]['e'] == "?":
                    graph[vertex]['e'] = nodes[-2]
            elif last == "e":
                if graph[vertex]['w'] == "?":
                    graph[vertex]['w'] = nodes[-2]
        for i in exits:
            if graph[vertex][i] == "?":
                free_exits.append(i)
                # print("free exits", free_exits)
        if len(free_exits) > 1:
            index = random.randint(0, len(free_exits)-1)
            random_dir = free_exits[index]
            player.travel(random_dir)
            traversal_path.append(random_dir)
            graph[vertex][random_dir] = player.current_room.id
            s.append(player.current_room.id)
        elif len(free_exits) == 1:
            player.travel(free_exits[0])
            traversal_path.append(free_exits[0])
            graph[vertex][free_exits[0]] = player.current_room.id
            s.append(player.current_room.id)
        else:
            if len(visited) == len(world.rooms):
                break

            new_vertex = bfs(player.current_room.id)
            # print(graph)
            for i in range(len(new_vertex)-1):
                # print(new_vertex[i], "i top")
                for key, value in graph[new_vertex[i]].items():
                    # print('x top', key, value)
                    if value == new_vertex[i+1]:
                        # print(traversal_path, value, new_vertex[i+1], "before")
                        player.travel(key)
                        traversal_path.append(key)
                        # print(traversal_path, "after")
            # print("new vertex", new_vertex)
            # print("breaking new vertex top", new_vertex)
            # print(len(visited))
            # print("traversal length", len(traversal_path))
            s.append(new_vertex[-1])
    else:
        if len(traversal_path) > 0:
            last = traversal_path[-1]
            if last == "n":
                if graph[vertex]['s'] == "?":
                    graph[vertex]['s'] = nodes[-2]
            elif last == "s":
                if graph[vertex]['n'] == "?":
                    graph[vertex]['n'] = nodes[-2]
            elif last == "w":
                if graph[vertex]['e'] == "?":
                    graph[vertex]['e'] = nodes[-2]
            elif last == "e":
                if graph[vertex]['w'] == "?":
                    graph[vertex]['w'] = nodes[-2]
        for i in exits:
            if graph[vertex][i] == "?":
                free_exits.append(i)
        if len(free_exits) > 1:
            index = random.randint(0, len(free_exits)-1)
            random_dir = free_exits[index]
            player.travel(random_dir)
            traversal_path.append(random_dir)
            graph[vertex][random_dir] = player.current_room.id
            s.append(player.current_room.id)
        elif len(free_exits) == 1:
            player.travel(free_exits[0])
            traversal_path.append(free_exits[0])
            graph[vertex][free_exits[0]] = player.current_room.id
            s.append(player.current_room.id)
        else:
            # find an open exit vertex and travel there.
            if len(visited) == len(world.rooms):
                break
            new_vertex = bfs(player.current_room.id)
            for i in range(len(new_vertex)-1):
                # print(new_vertex[i], "i top")
                for key, value in graph[new_vertex[i]].items():
                    # print('x top', key, value)
                    if value == new_vertex[i+1]:
                        # print(traversal_path, "before")
                        player.travel(key)
                        traversal_path.append(key)
                        # print(traversal_path, "after")
            # print("breaking new vertex bottom", new_vertex)
            # print(graph)
            # print(len(visited))
            s.append(new_vertex[-1])


# print("final graph", graph)
print("final len visited", len(visited))
print("final len rooms", len(world.rooms))
# print(has_exits(graph[0])

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
