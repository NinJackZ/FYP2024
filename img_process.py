import os
import sys
import tkinter as tk
import cv2 as cv
from tkinter import filedialog, messagebox

# Directory for assets
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Waypoint:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def add(self, other):
        return Waypoint(self.x + other.x, self.y + other.y)

    def check_meet(self, target):
        return self.x == target.x and self.y == target.y

def sort(queue, en):
    index = [(cell.x - en.x) ** 2 + (cell.y - en.y) ** 2 for cell in queue]
    sorted_queue = [x for _, x in sorted(zip(index, queue), reverse=True)]
    return sorted_queue

def mouse_event(event, x, y, flags, params):
    global col, start, end, point_count
    s = 2
    if event == cv.EVENT_LBUTTONUP:
        if point_count == 0:
            col = cv.rectangle(col, (x - s, y - s), (x + s, y + s), color=(0, 0, 255), thickness=-1)
            start = Waypoint(x, y)
            print(f'start: {start.x}, {start.y}')
            point_count += 1
        elif point_count == 1:
            col = cv.rectangle(col, (x - s, y - s), (x + s, y + s), color=(255, 255, 0), thickness=-1)
            end = Waypoint(x, y)
            print(f'end: {end.x}, {end.y}')
            point_count += 1

def upload_maze_image():
    root = tk.Tk()
    root.withdraw()

    prompt = messagebox.askokcancel("Upload A Maze Image", "Upload an image in .jpg or .png format, ensure the maze has closed walls")

    if prompt:
        file_path = filedialog.askopenfilename()
        _, file_ext = os.path.splitext(file_path)

        supported_formats = ['.png', '.jpg', '.jpeg']

        try:
            # Open an image file
            if file_ext.lower() not in supported_formats:
                raise ValueError(f"Error: invalid file {file_ext}, valid files are .jpg and .png")
            elif not file_ext:
                pass
            global point_count, col, start, end, directions, ret, h, w, d
            point_count = 0
            start = Waypoint()
            end = Waypoint()
            directions = [Waypoint(0, -1), Waypoint(0, 1), Waypoint(1, 0), Waypoint(-1, 0)]
            size = 512
            img = cv.imread(file_path, 0)
            img = cv.resize(img, (size, size))
            ret, thresh = cv.threshold(img, 150, 255, cv.THRESH_BINARY_INV)
            thresh = cv.resize(thresh, (size, size))
            col = cv.cvtColor(thresh, cv.COLOR_GRAY2BGR)
            h, w, d = col.shape
            cv.namedWindow('image')
            cv.setMouseCallback('image', mouse_event)
            while True:
                cv.imshow('image', col)
                k = cv.waitKey(100)
                if point_count == 2:
                    break
            cv.destroyAllWindows()
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    upload_maze_image()