import tkinter
import win32gui
import time
from tkinter import PhotoImage

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 70, 68
GRAVITY = 1
JUMP_POWER = -23
MOVE_SPEED = 9 
FPS = 60
frame_counter = 0
FRAME_DELAY = 3

# ----------------------------------------

root = tkinter.Tk()
root.overrideredirect(True)
root.geometry(f"{WIDTH}x{HEIGHT}+300+300")
root.attributes("-topmost", True)
root.wm_attributes("-transparentcolor", "white")
root.config(bg="white")

image = tkinter.PhotoImage(file="small.png")
image_label = tkinter.Label(root, image=image, bg="white")
image_label.pack()

current_frame = 0

frames_walk_right = [
    tkinter.PhotoImage(file="small.png"),
    tkinter.PhotoImage(file="small run1.png"),
    tkinter.PhotoImage(file="small run2.png"),
    tkinter.PhotoImage(file="small run3.png"), 
]

# Left-facing frames
frames_walk_left = [
    tkinter.PhotoImage(file="small flip.png"),
    tkinter.PhotoImage(file="small run1 flip.png"),
    tkinter.PhotoImage(file="small run2 flip.png"),
    tkinter.PhotoImage(file="small run3 flip.png"), 
]

# Jump frames
jump_right = tkinter.PhotoImage(file="small jump.png")
jump_left = tkinter.PhotoImage(file="small jump flip.png")


vx = 0
vy = 0
on_ground = False

keys = set()

def key_down(e):
    keys.add(e.keysym.lower())

def key_up(e):
    keys.discard(e.keysym.lower())

root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)

def get_window_rects():
    rects = []

    def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            if hwnd != win32gui.GetForegroundWindow():
                try:
                    rect = win32gui.GetWindowRect(hwnd)
                    rects.append(rect)
                except:
                    pass
        return True

    win32gui.EnumWindows(callback, None)
    return rects

def game_loop():


    global vx, vy, on_ground, current_frame, frame_counter

    moving = vx != 0
    facing_left = vx < 0

    frame_counter += 1
    if frame_counter >= FRAME_DELAY:
        frame_counter = 0
        if not on_ground:
            # Jumping
            image_label.config(image=jump_left if facing_left else jump_right)
        elif moving:
            # Walking animation
            if facing_left:
                current_frame = (current_frame + 1) % len(frames_walk_left)
                image_label.config(image=frames_walk_left[current_frame])
            else:
                current_frame = (current_frame + 1) % len(frames_walk_right)
                image_label.config(image=frames_walk_right[current_frame])
        else:
            # Idle
            image_label.config(image=frames_walk_left[0] if facing_left else frames_walk_right[0])


    
    x = root.winfo_x()
    y = root.winfo_y()

    vx = 0
    if "a" in keys:
        vx = -MOVE_SPEED
    if "d" in keys:
        vx = MOVE_SPEED

    if "space" in keys and on_ground:
        vy = JUMP_POWER
        on_ground = False

    vy += GRAVITY

    new_x = x + vx
    new_y = y + vy

    on_ground = False

    for wx1, wy1, wx2, wy2 in get_window_rects():
        # landing on top of window
        if (
            new_x + WIDTH > wx1 and new_x < wx2 and
            y + HEIGHT <= wy1 and new_y + HEIGHT >= wy1
        ):
            new_y = wy1 - HEIGHT
            vy = 0
            on_ground = True

    # screen floor
    screen_h = root.winfo_screenheight()
    if new_y + HEIGHT >= screen_h:
        new_y = screen_h - HEIGHT
        vy = 0
        on_ground = True

    root.geometry(f"+{int(new_x)}+{int(new_y)}")
    root.after(int(1000 / FPS), game_loop)

game_loop()
root.mainloop()
