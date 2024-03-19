import os, sys
import tkinter as tk
import cv2 as cv
from tkinter import filedialog, messagebox, filedialog, Tk

# Directory for assets
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def upload_maze_image():
    rt = tk.Tk()
    rt.withdraw()

    prompt = messagebox.askokcancel("Upload A Maze Image", "Upload an image in .jpg or .png format, ensure the maze has closed walls")

    if prompt:
        fpath = filedialog.askopenfilename()
        _, file_ext = os.path.splitext(fpath)

        supported_formats = ['.png', '.jpg', '.jpeg']

        try:
            # Open an image file
            if file_ext.lower() not in supported_formats:
                raise ValueError(f"Error: invalid file {file_ext}, valid files are .jpg and .png")

            point_count = 0
            size = 512
            img = cv.imread(fpath, 0)
            img = cv.resize(img, (size, size))
            ret, thresh = cv.threshold(img, 150, 255, cv.THRESH_BINARY_INV)
            thresh = cv.resize(thresh, (size, size))
            col = cv.cvtColor(thresh, cv.COLOR_GRAY2BGR)
            h, w, d = col.shape

            cv.namedWindow('image')

            while True:
                cv.imshow('image', col)
                if point_count == 2:
                    break
            pass
            cv.destroyAllWindows()
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    upload_maze_image()