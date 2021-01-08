# Matthew Coombe, Nurayn Hashim
# 08 January 2021
# Pathfinding visualisation


import pygame
import pygame_gui
from tkinter import *
from tkinter import ttk
from structures import *
from math import sqrt
from tkinter import messagebox

T = TypeVar('T')

pygame.init()
running = True
pathing = False
steps = True

clock = pygame.time.Clock()
fps = 60

pygame.display.set_caption("Pathfinding Visualisation")

WIDTH = 551
HEIGHT = 701
width, height = 10, 10
margin = 1

screen = pygame.display.set_mode([WIDTH, HEIGHT])
manager = pygame_gui.UIManager((WIDTH, HEIGHT))
background = pygame.Surface((WIDTH, HEIGHT))
background.fill(colourPalette.DARK_GREY)

rows, columns = 50, 50
grid = [[0 for j in range(columns)] for i in range(rows)]

colours = [colourPalette.BLUE1,  # WHITE
           colourPalette.DARK_GREY,  # BLACK
           colourPalette.YELLOW,  # GREEN
           (255, 0, 0),  # RED
           (0, 0, 255),  # BLUE
           (100, 100, 100),  # GREY
           (0, 150, 0),  # LIGHT_GREEN
           (0, 150, 150),  # LIGHT_BLUE
           colourPalette.BLACK,  # ORANGE
           colourPalette.BLUE3, colourPalette.BLUE2]

bwidth, blength = 60, 100
gap = (WIDTH - (blength * 4)) / 5
bheight = (151 - bwidth) / 2

FONT = "freesansbold.ttf"

buttons = ["reset", "astar", "bfs", "dfs"]

start, end = (4, 4), (45, 45)

for i in range(len(buttons)):
    buttons[i] = pygame.Rect(gap + (gap + blength) * i, bheight, blength, bwidth)

uibuttons = []
names = ["Reset", "DFS", "BFS", "A*"]

for i in range(len(buttons)):
    uibuttons.append(pygame_gui.elements.UIButton(relative_rect=buttons[i],
                                                  text=names[i], manager=manager))


def successorsStraight(node):
    locations = []

    if node[0] + 1 < 50 and grid[node[0] + 1][node[1]] != 5:  # DOWN
        locations.append((node[0] + 1, node[1]))

    if node[0] - 1 >= 0 and grid[node[0] - 1][node[1]] != 5:  # UP
        locations.append((node[0] - 1, node[1]))

    if node[1] + 1 < 50 and grid[node[0]][node[1] + 1] != 5:  # RIGHT
        locations.append((node[0], node[1] + 1))

    if node[1] - 1 >= 0 and grid[node[0]][node[1] - 1] != 5:  # LEFT
        locations.append((node[0], node[1] - 1))

    return locations


def successorsDiag(node):
    locations = []

    if (node[1] + 1 < 50 and node[0] + 1 < 50) and grid[node[0] + 1][node[1] + 1] != 5:  # RIGHT DOWN
        locations.append((node[0] + 1, node[1] + 1))

    if (node[1] + 1 < 50 and node[0] - 1 >= 0) and grid[node[0] - 1][node[1] + 1] != 5:  # RIGHT UP
        locations.append((node[0] - 1, node[1] + 1))

    if (node[1] - 1 >= 0 and node[0] - 1 >= 0) and grid[node[0] - 1][node[1] - 1] != 5:  # LEFT UP
        locations.append((node[0] - 1, node[1] - 1))

    if (node[1] - 1 >= 0 and node[0] + 1 < 50) and grid[node[0] + 1][node[1] - 1] != 5:  # LEFT DOWN
        locations.append((node[0] + 1, node[1] - 1))

    return locations


def successors(node, algorithm):
    if algorithm == "dfs":
        return successorsDiag(node) + successorsStraight(node)
    elif algorithm == "bfs":
        return successorsStraight(node) + successorsDiag(node)

    return successorsStraight(node) + (successorsDiag(node))


def dfs(start: T, goal, successors) -> Optional[Node[T]]:
    frontier = [Node(start, None)]
    explored = {start}

    while frontier:
        current_node = frontier.pop()
        current_state = current_node.state
        if steps:
            grid[current_state[0]][current_state[1]] = 10
        for child in successors(current_state, "dfs"):
            if child == goal:
                return current_node
            if child in explored:
                continue
            explored.add(child)

            if steps:
                grid[child[0]][child[1]] = 9
            draw()
            pygame.display.update()

            frontier.append(Node(child, current_node))

    return None


def bfs(start: T, goal, successors) -> Optional[Node[T]]:
    frontier = Queue()
    frontier.push(Node(start, None))
    explored = {start}

    while not frontier.empty:
        current_node = frontier.pop()
        current_state = current_node.state
        if steps:
            grid[current_state[0]][current_state[1]] = 10
        for child in successors(current_state, "bfs"):
            if child == goal:
                return current_node
            if child in explored:
                continue
            explored.add(child)

            if steps:
                grid[child[0]][child[1]] = 9

            frontier.push(Node(child, current_node))

        draw()
        pygame.display.update()

    return None


def diagonal_distance(goal):
    def distance(loc):
        dx = abs(goal[0] - loc[0])
        dy = abs(goal[1] - loc[1])
        return 1 * (dx + dy) + (sqrt(2) - 2 * 1) * min(dx, dy)

    return distance


def astar(start: T, goal, successors, heuristic) -> Optional[Node[T]]:
    frontier = PriorityQueue()
    frontier.push(Node(start, None, 0.0, heuristic(start)))
    explored = {start: 0.0}

    while not frontier.empty:
        current_node = frontier.pop()
        current_state = current_node.state
        if steps:
            grid[current_state[0]][current_state[1]] = 10
        if goal == current_state:
            return current_node
        for child in successors(current_state, "a*"):

            if child in successorsDiag(current_state):
                new_cost = current_node.cost + sqrt(2)
            else:
                new_cost = current_node.cost + 1

            if child not in explored or explored[child] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node, new_cost, heuristic(goal)(child)))
            if grid[child[0]][child[1]] != 10 and steps:
                grid[child[0]][child[1]] = 9
        draw()
        pygame.display.update()

    return None


def onsubmit():
    global start, end, steps
    start1 = startBox.get().split(',')[::-1]
    end1 = endBox.get().split(',')[::-1]
    if len(start1) == 2 and len(end1) == 2:
        if start1[0].isdigit() and start1[1].isdigit() and end1[0].isdigit() and end1[1].isdigit():
            start1 = tuple(map(int, start1))
            end1 = tuple(map(int, end1))
            if all(0 <= a < 50 for a in [start1[0], start1[1], end1[0], end1[1]]):
                if start1[0] != end1[0] or start1[1] != end1[1]:
                    start = tuple(map(int, start1))
                    end = tuple(map(int, end1))
                    steps = True if var.get() else False
                    window.quit()
                    window.destroy()
                else:
                    print("start and end same")
                    messagebox.showerror("Error", "Start and end cannot be the same")
                    mainloop()
            else:
                print("input out of range")
                messagebox.showerror("Error", "Input out of range")
                mainloop()
        else:
            print("input not of form int,int")
            messagebox.showerror("Error", "Input not of form int,int")
            mainloop()
    else:
        print("input incorrect form")
        messagebox.showerror("Error", "Input incorrect form")
        mainloop()


window = Tk()
window.title("Input Coords (0 - 49)")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry("300x100")
x = (window.winfo_screenwidth() - 300) / 2
y = (window.winfo_screenheight() - 100) / 2
window.geometry("+%d+%d" % (x, y))

label = Label(window, text='Start (x,y): ')
startBox = Entry(window)
label1 = Label(window, text='End (x,y): ')
endBox = Entry(window)
var = IntVar()

showPath = ttk.Checkbutton(window, text='Show Steps:', onvalue=1, offvalue=0, variable=var)
submit = Button(window, text='Submit', command=onsubmit)

label.place(relx=0.25, rely=0.0, anchor=N)
startBox.place(relx=0.6, rely=0.0, anchor=N)
label1.place(relx=0.25, rely=0.25, anchor=N)
endBox.place(relx=0.6, rely=0.25, anchor=N)
showPath.place(relx=0.5, rely=0.75, anchor=S)
submit.place(relx=0.5, rely=1.0, anchor=S)

window.update()
mainloop()


def makeText(text: str, size: int, location: tuple, colour: tuple = (0, 0, 0), font: str = FONT):
    font = pygame.font.Font(font, size)
    text = font.render(text, True, colour)
    textRect = text.get_rect()
    textRect.center = location
    screen.blit(text, textRect)
    pass


def mousePress(x, colour):
    x1 = x[0] // 11
    x2 = (x[1] - 150) // 11
    if x[0] < 550 and 150 < x[1] < 700:
        if (x1 != start[0] or x2 != start[1]) and (x1 != end[0] or x2 != end[1]):
            grid[x1][x2] = colour


def reset():
    for i in range(rows):
        for j in range(columns):
            grid[i][j] = 0
    grid[start[0]][start[1]] = 2
    grid[end[0]][end[1]] = 3


def draw():
    for i in range(0, 50):
        for j in range(0, 50):
            pygame.draw.rect(screen,
                             colours[grid[i][j]],
                             [(width + margin) * i + margin, (width + margin) * j + margin + 150, width,
                              height])
    grid[start[0]][start[1]] = 2
    grid[end[0]][end[1]] = 3


def runAlgorithm(algname, algfunc):
    global pathing
    for i in range(rows):
        for j in range(columns):
            if grid[i][j] != 2 and grid[i][j] != 3 and grid[i][j] != 5:
                grid[i][j] = 0
    pathing = True
    print(algname)

    if algname == "a*":
        finished = algfunc(start, end, successors, diagonal_distance)
    else:
        finished = algfunc(start, end, successors)

    while finished is not None and finished.parent is not None:
        grid[finished.state[0]][finished.state[1]] = 8
        finished = finished.parent
    if finished is None:
        print("sadge")
    else:
        print("happy")
    grid[end[0]][end[1]] = 3


def main():
    global pathing, running
    while running:

        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if buttons[0].collidepoint(mouse_pos):
                    print("reset")
                    reset()
                    pathing = False

                elif buttons[1].collidepoint(mouse_pos):
                    runAlgorithm("dfs", dfs)
                elif buttons[2].collidepoint(mouse_pos):
                    runAlgorithm("bfs", bfs)
                elif buttons[3].collidepoint(mouse_pos):
                    runAlgorithm("a*", astar)

            if pygame.mouse.get_pressed()[0] and not pathing:
                try:
                    mouse_pos = pygame.mouse.get_pos()
                    mousePress(mouse_pos, 5)

                except AttributeError:
                    pass
            if pygame.mouse.get_pressed()[2] and not pathing:
                try:
                    mouse_pos = pygame.mouse.get_pos()
                    mousePress(mouse_pos, 0)
                except AttributeError:
                    pass
            manager.process_events(event)

        manager.update(time_delta)
        screen.blit(background, (0, 0))
        manager.draw_ui(screen)
        draw()
        pygame.display.update()
        clock.tick(fps)

    pygame.quit()


if __name__ == '__main__':
    main()
