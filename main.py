from math import sqrt
import pygame

WIDTH = 900
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("AiSD - 14 - Solving labirynth with A* Algorithm")
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)



class Wierzcholek:
    def __init__(self, position, symbol, start=None, end=None, wall=None, free=None):
        self.position = position
        self.symbol = symbol
        self.connections = []
        self.start = start
        self.end = end
        self.wall = wall
        self.free = free
    
    def show_info(self):
        if self.start:
            print(f"Wierzcholek {self.position} - START - {self.symbol} - {self.connections}")
        elif self.end:
            print(f"Wierzcholek {self.position} - END - {self.symbol} - {self.connections}")
        else:
            print(f"Wierzcholek {self.position} - {self.symbol} - {self.connections}")
    
    def add_connections(self, graph):
        n = len(graph)
        row_len = int(sqrt(n))
        if self.symbol == 'X':
            return
        # first row
        if self.position >= 0 and self.position < row_len:
            if self.position % row_len == 0:
                if graph[self.position + 1].symbol != 'X':
                    self.connections.append(self.position + 1)
                if graph[self.position + row_len].symbol != 'X':
                    self.connections.append(self.position + row_len)
            elif self.position % row_len == row_len - 1:
                if graph[self.position - 1].symbol != 'X':
                    self.connections.append(self.position - 1)
                if graph[self.position + row_len].symbol != 'X':
                    self.connections.append(self.position + row_len)
            else:
                if graph[self.position - 1].symbol != 'X':
                    self.connections.append(self.position - 1)
                if graph[self.position + 1].symbol != 'X':
                    self.connections.append(self.position + 1)
                if graph[self.position + row_len].symbol != 'X':
                    self.connections.append(self.position + row_len)
        # last row
        elif self.position >= n - row_len:
            if self.position % row_len == 0:
                if graph[self.position + 1].symbol != 'X':
                    self.connections.append(self.position + 1)
                if graph[self.position - row_len].symbol != 'X':
                    self.connections.append(self.position - row_len)
            elif self.position % row_len == row_len - 1:
                if graph[self.position - 1].symbol != 'X':
                    self.connections.append(self.position - 1)
                if graph[self.position - row_len].symbol != 'X':
                    self.connections.append(self.position - row_len)
            else:
                if graph[self.position - 1].symbol != 'X':
                    self.connections.append(self.position - 1)
                if graph[self.position + 1].symbol != 'X':
                    self.connections.append(self.position + 1)
                if graph[self.position - row_len].symbol != 'X':
                    self.connections.append(self.position - row_len)
        # mid rows
        else:
            if self.position % row_len == 0:
                if graph[self.position + 1].symbol != 'X':
                    self.connections.append(self.position + 1)
                if graph[self.position + row_len].symbol != 'X':
                    self.connections.append(self.position + row_len)
                if graph[self.position - row_len].symbol != 'X':
                    self.connections.append(self.position - row_len)
            elif self.position % row_len == row_len - 1:
                if graph[self.position - 1].symbol != 'X':
                    self.connections.append(self.position - 1)
                if graph[self.position + row_len].symbol != 'X':
                    self.connections.append(self.position + row_len)
                if graph[self.position - row_len].symbol != 'X':
                    self.connections.append(self.position - row_len)
            else:
                if graph[self.position - 1].symbol != 'X':
                    self.connections.append(self.position - 1)
                if graph[self.position + 1].symbol != 'X':
                    self.connections.append(self.position + 1)
                if graph[self.position + row_len].symbol != 'X':
                    self.connections.append(self.position + row_len)
                if graph[self.position - row_len].symbol != 'X':
                    self.connections.append(self.position - row_len)

class Node():
    def __init__(self, id, neighbors_id, matrix_pos, width, color=WHITE, block=None):
        self.id = id
        self.neighbors_id = neighbors_id
        self.neighbors = []
        self.block = block
        self.matrix_pos = matrix_pos
        self.color = color
        self.width = width
    
    def get_info(self):
        print(f"Node {self.id}, {self.matrix_pos}", end=" - ")
        for node in self.neighbors:
            print(node.id, end=" ")
        if self.block != None:
            print(self.block, end=" ")
        print()
        
    def draw(self, win, gap):
        pygame.draw.rect(win, self.color, (self.matrix_pos[1] * gap, self.matrix_pos[0] * gap, gap, gap))


# end class
def create_adjacency_matrix(graph):
    n = len(graph)
    A = [[0 for x in range(n)] for y in range(n)]
    i = 0
    j = 0
    for wierzcholek in graph:
        if len(wierzcholek.connections) > 0:
            for j in wierzcholek.connections:
                A[i][j] = 1
        i += 1
    ad_matrix = open("adj_matrix.txt",'w')
    for row in A:
        str_row = ""
        for char in row:
            str_row += str(char)
        ad_matrix.write(str_row+'\n')
        
    return A

def h(n1, n2):
    x1, y1 = n1.matrix_pos
    x2, y2 = n2.matrix_pos
    return abs(x1 - x2) + abs(y1 - y2)

def astar_algorithm(draw, graph):
    for node in graph:
        if node.block == "START":
            start_node = node
        elif node.block == "END":
            end_node = node
    Q = []
    S = []
    n = len(graph)
    g = [float("inf") for x in range(n)]
    g[start_node.id] = 0
    f = [float("inf") for x in range(n)]
    f[start_node.id] = h(start_node, end_node)
    pred = [0 for x in range(n)]
    Q.append(start_node)
    
    while len(Q) > 0:
        min_f = Q[0]
        for node in Q:
            if f[node.id] < f[min_f.id]:
                min_f = node
        if min_f.block == "END":
            reconstruct_path(draw, graph, pred, start_node, end_node)
            return True
        for neighbor in min_f.neighbors:
            temp_g = g[min_f.id] + 1
            if neighbor not in Q and neighbor not in S:
                Q.append(neighbor)
                g[neighbor.id] = temp_g
                f[neighbor.id] = h(neighbor, end_node) + g[neighbor.id]
                pred[neighbor.id] = min_f.id
        Q.remove(min_f)
        S.append(min_f)

def reconstruct_path(draw, graph, pred, start_node, end_node):
    path = []
    path.append(end_node.id)
    current_node = pred[end_node.id]
    while current_node != start_node.id:
        path.append(current_node)
        current_node = pred[current_node]
    path.append(start_node.id)
    path.reverse()

    for node in path:
        graph[node].color = ORANGE
        draw()
        

    for i, node in enumerate(path):
        if i != len(path) -  1:
            print(f"{node} -> ",end="")
        else:
            print(f"{node}")
    

# pygame functions
def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    gap = width // rows
    win.fill(WHITE)
    for node in grid:
        node.draw(win, gap)

    draw_grid(win, rows, width)
    pygame.display.update()

# algorithm main
maze = open("maze5.txt",'r')
maze_matrix = []
graph = []
for row in maze.readlines():
    maze_row = ""
    for char in row.replace('\n',""):
        maze_row += char
    maze_matrix.append(maze_row)

i = 0
for row in maze_matrix:
    for char in row:
        if char == 'S':
            graph.append(Wierzcholek(i, char,start=True))
            i += 1
        elif char == "E":
            graph.append(Wierzcholek(i, char,end=True))
            i += 1
        elif char == "X":
            graph.append(Wierzcholek(i, char,wall=True))
            i += 1
        elif char == "O":
            graph.append(Wierzcholek(i, char,free=True))
            i += 1

for wierzcholek in graph:
    wierzcholek.add_connections(graph)
    # wierzcholek.show_info()

create_adjacency_matrix(graph)
adj_matrix = open("adj_matrix.txt", 'r')

final_graph = []
n = len(graph)
row_len = int(sqrt(n))
ROWS = row_len
gap = WIDTH// ROWS
i = 0
k = 0
for row in adj_matrix.readlines():
    j = 0
    current_neighbors = []
    for char in row.replace("\n",''):
        if char != '0':
            current_neighbors.append(j)
        j += 1
    if graph[i].start:
        final_graph.append(Node(i, current_neighbors, matrix_pos=(k, i%row_len), width=gap, color=RED, block="START"))
    elif graph[i].end:
        final_graph.append(Node(i, current_neighbors, matrix_pos=(k, i%row_len), width=gap, color=GREEN, block="END"))
    elif graph[i].wall:
        final_graph.append(Node(i, current_neighbors, matrix_pos=(k, i%row_len), width=gap, color=BLACK))
    elif graph[i].free:
        final_graph.append(Node(i, current_neighbors, matrix_pos=(k, i%row_len), width=gap, color=WHITE))
    i += 1
    if i % row_len == 0:
        k += 1
    
for node in final_graph:
    for neighbors_id in node.neighbors_id:
        for n in final_graph:
            if neighbors_id == n.id:
                node.neighbors.append(n)


# main pygame program
grid = 0
run = True
while run:
    draw(WIN, final_graph, ROWS, WIDTH)
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    astar_algorithm(lambda: draw(WIN, final_graph, ROWS, WIDTH), final_graph)
    
    


        
