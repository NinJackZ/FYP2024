import os
import cv2
from tkinter import *
from tkinter import filedialog
import tkinter.messagebox
from queue import PriorityQueue

class Waypoint:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Waypoint):
            return Waypoint(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __lt__(self, other):
        if isinstance(other, Waypoint):
            return (self.x, self.y) < (other.x, other.y)  

def heuristic(point, end):
    # Uses Pythagoras theorem to improve efficiency
    return ((point.x - end.x) ** 2 + (point.y - end.y) ** 2) ** 0.5

def is_valid_move(point):
    # Check if the move is within bounds and not hitting a wall
    return 0 <= point.x < width and 0 <= point.y < height and not all(column[point.y][point.x][i] == 255 for i in range(3))

# A* pathfinding algorithm used to highlight path between start and end points
def pathfind(st, end):
    global column, height, width, parameters
    count = 0
    goal = False
    open_set = PriorityQueue()
    open_set.put((0, st))
    origin = [[Waypoint() for j in range(width)] for i in range(height)]
    cost_so_far = {st: 0}

    while not open_set.empty():
        _, main_point = open_set.get()
        count += 1

        if count % 100 == 0:
            result = column.copy()
            result = cv2.resize(result, (800, 800))
            cv2.imshow('Solve Maze', result)
            cv2.waitKey(1)

        if main_point == end:
            goal = True
            break

        for direction in parameters:
            next_cell = main_point + direction
            x, y = next_cell.x, next_cell.y
            if is_valid_move(next_cell):
                new_cost = cost_so_far[main_point] + 1
                if next_cell not in cost_so_far or new_cost < cost_so_far[next_cell]:
                    cost_so_far[next_cell] = new_cost
                    priority = new_cost + heuristic(next_cell, end)
                    open_set.put((priority, next_cell))
                    origin[y][x] = main_point

    route = []

    if goal:
        point = end
        while point != st:
            route.append(point)
            point = origin[point.y][point.x]
        route.append(point)
    
        for i, p in enumerate(route):
            cv2.rectangle(column, (p.x - 1, p.y - 1), (p.x + 1, p.y + 1), (0, 255, 0, 100), -1)

            if (i + 1) % 15 == 0:
                result = column.copy()
                result = cv2.resize(result, (800, 800))
                cv2.imshow('Solve Maze', result)
        result = column.copy()
        result = cv2.resize(result, (800, 800))
        cv2.imshow('Solve Maze', result)
        cv2.waitKey(0)

def handle_mouse_click(action, x, y, flags = None, params = None):
    # Place points on the maze to solve
    global column, start, end, point_count
    placement = 2
    if action == cv2.EVENT_LBUTTONUP:
        if point_count == 0:
            column = cv2.rectangle(column, (x - placement, y - placement), (x + placement, y + placement), color=(255, 0, 255), thickness=-1)
            start = Waypoint(x, y)
            point_count += 1
        elif point_count == 1:
            column = cv2.rectangle(column, (x - placement, y - placement), (x + placement, y + placement), color=(255, 0, 255), thickness=-1)
            end = Waypoint(x, y)
            point_count += 1

screen = Tk()
screen.withdraw()
prompt = tkinter.messagebox.askyesnocancel("Maze Solver", " Yes: Upload Maze Image \n No: Take Picture of Maze Image \n Cancel: Return To Main Menu")
# Use maze image from file explorer
if prompt:

    path = filedialog.askopenfilename()
    _, file_ext = os.path.splitext(path)

    try:
        if file_ext.lower() not in ['.png', '.jpeg', '.jpg']:
            raise ValueError
        point_count = 0
        start  = Waypoint()
        end = Waypoint()
        parameters = [Waypoint(0, -1), Waypoint(0, 1), Waypoint(1, 0), Waypoint(-1, 0)]
        size = 512
        img = cv2.imread(path, 0)
        img = cv2.resize(img, (size, size))
        ret, threshold = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV)
        threshold = cv2.resize(threshold, (size, size))
        column = cv2.cvtColor(threshold, cv2.COLOR_GRAY2BGR)
        height, width, d = column.shape

        cv2.namedWindow('Solve Maze')
        cv2.setMouseCallback('Solve Maze', handle_mouse_click)
        while True:
            cv2.imshow('Solve Maze', column)
            k = cv2.waitKey(100)
            if point_count == 2:
                break
        pass

        pathfind(start, end)
        cv2.destroyAllWindows()
    except ValueError:
        tkinter.messagebox.showerror("Error", "Incorrect File Format, must be .jpg or .png")

if prompt is False:
    # Save image to used to solve
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    cv2.namedWindow("Capture Image")
    img_counter = 0

    while True:
        ret, img = cam.read()
        cv2.putText(img,"SPACE to Capture   ESC to Return", (50,50),cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, cv2.LINE_AA )
        if not ret:
            print("failed to grab frame")
            break
        cv2.imshow("Capture Image", img)

        k = cv2.waitKey(1)
        if k%256 == 27:
            break
        elif k%256 == 32:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray,(5,5),0)
            ret, thresh_img = cv2.threshold(blur,91,255,cv2.THRESH_BINARY)
            contours =  cv2.findContours(thresh_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)[-2]
            for c in contours:
                cv2.drawContours(img, [c], -1, (0,255,0), 3)
            img_name = "opencv_frame_{}.png".format(img_counter)
            cv2.imwrite(img_name, img)
            print("{} written!".format(img_name))
            img_counter += 1

    cam.release()

    cv2.destroyAllWindows()