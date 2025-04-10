import tkinter                 # to make GUI application in python
from PIL import Image, ImageTk # to use the jpg and jpeg photos. # pip install pilow
import cv2                     # we use this for video playback and review frames
from functools import partial  # to give the arguments to the function in buttons
import threading               # to create threads
import time                    # # for waits
import imutils                 # for resizing the frame

# ========================== VIDEO SETUP ==========================
stream = cv2.VideoCapture("D:\\2nd year\\Project\\final\\run_out.mp4") ## Load the run-out video
SET_WIDTH = 1200
SET_HEIGHT = 675
flag = True  # For blinking "Decision Pending" for each click

# ========================== ALL FUNCTION'S HERE ==========================
def play(speed):
    """
    Moves the video forward or backward by the given speed (frames).
    
    """
    global frame
    global flag
    frame = stream.get(cv2.CAP_PROP_POS_FRAMES)# Get current frame position
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame + speed) # Get the new frame according to the speed
    
    # Read the next frame from the video
    grabbed, frame1 = stream.read()
    if not grabbed:
        return # return if no frame is available

    frame1 = imutils.resize(frame1, width=SET_WIDTH, height=SET_HEIGHT) # reszie the frame
    frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)  # ✅ Fix BGR to RGB
    frame1 = ImageTk.PhotoImage(image=Image.fromarray(frame1)) # Convert frame to an image compatible with Tkinter

    # Display the image on the canvas
    canvas.image = frame1  # save reference to avoid garbage collection
    canvas.create_image(0, 0, image=frame1, anchor=tkinter.NW)

    # Logic for blinking "Decision Pending" 
    if flag:
        canvas.create_text(120,29,fill="black",font="Times 20 bold",text="Decision Pending")
    flag=not flag
    
def play_clip(path, on_complete=None):
    """
    Plays a clip video (pending, sponsor, or decision).
    Calls 'on_complete' function after the clip finishes. # to avoid overlapes
    """
    
    clip = cv2.VideoCapture(path)
    if not clip.isOpened():
        print("Error opening video file:", path)
        if on_complete:
            on_complete()
        return
    
    # Calculate time delay between frames (based on video FPS)
    fps = clip.get(cv2.CAP_PROP_FPS)
    delay = int(1000 / fps) if fps > 0 else 33  # in milliseconds

    def update_frame():
        ret, frame = clip.read()
        if not ret:
            clip.release()
            if on_complete:
                on_complete() # Call next function when clip ends
            return
        
        # Resize and convert frame for GUI
        frame_resized = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        img = ImageTk.PhotoImage(Image.fromarray(frame_rgb))
        
        # Display frame
        canvas.image_ref = img
        canvas.itemconfig(canvas.image_id, image=img)
        
        # Show next frame after `delay` milliseconds
        window.after(delay, update_frame)

    # Display first frame
    ret, frame = clip.read()
    if not ret:
        clip.release()
        if on_complete:
            on_complete()
        return

    frame_resized = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
    img = ImageTk.PhotoImage(Image.fromarray(frame_rgb))

    canvas.image_ref = img
    canvas.image_id = canvas.create_image(0, 0, image=img, anchor=tkinter.NW)

    window.after(delay, update_frame)


def pending(decision):
    """
    
    Plays 3 clips in order:
    1. 'Decision Pending'
    2. Sponsor Ad
    3. Final Decision (OUT or NOT OUT)
    
    """
    def play_decision():
        # Choose final clip based on decision
        decision_path = (
            "D:\\2nd year\\Project\\final\\out.mp4"
            if decision == "out"
            else "D:\\2nd year\\Project\\final\\not_out.mp4"
        )
        play_clip(decision_path)

    def play_sponsor():
        # Play sponsor video after calling pendig video
        sponsor_path = "D:\\2nd year\\Project\\final\\sponsorr.mp4"
        play_clip(sponsor_path, on_complete=play_decision)
    
    # Play pending video first, then call sponsor
    decision_pending_path = "D:\\2nd year\\Project\\final\\decision_pending.mp4"
    play_clip(decision_pending_path, on_complete=play_sponsor)


# OUT button callback
def out():
    # create sep thread for out decison so that it cant interrupt window.mainloop() flow
    thread1 = threading.Thread(target=pending, args=("out",))
    thread1.daemon = 1
    thread1.start()
    # thread1.join()
    print("Player is given out")

# NOT OUT button callback
def not_out():
    # create sep thread for not_out decison so that it cant interrupt window.mainloop() flow
    thread1 = threading.Thread(target=pending, args=("not out",))
    thread1.daemon = 1
    thread1.start()
    # thread1.join()
    print("Player is given not-out")

# ========================= GUI Setup ==============================

# Main window
window = tkinter.Tk()
window.title("DECISION REVIEW SYSTEM - by Jenis Surani")



# Create a canvas to display video frames
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
canvas.pack()  # pack the canvas first

# ================= DISPLAY WELCOME IMAGE AT START ================

# display welcome.jpg on the canvas at startup
welcome_img = Image.open("D:\\2nd year\\Project\\final\\welcome.jpg")  # Path for welcome image 
welcome_img = welcome_img.resize((SET_WIDTH, SET_HEIGHT))  # Resize to fit the canvas
welcome_img = ImageTk.PhotoImage(welcome_img)  # Convert to Tkinter-compatible image

canvas.image = welcome_img  
canvas.create_image(0, 0, image=welcome_img, anchor=tkinter.NW)  # Show image at North-West

# Create a separate frame for buttons (below the canvas)
btn_frame = tkinter.Frame(window)
btn_frame.pack(fill="x")  # horizontal layout

# # Create a frame to hold all control buttons
btn_frame = tkinter.Frame(window)
btn_frame.pack(fill="x")  # Expand the button frame to full width

# Configure grid columns to expand equally
for i in range(6):  # 6 buttons in total
    btn_frame.columnconfigure(i, weight=1)

# ========================== BUTTONS SECTION  ==========================

# 1. << Backward (slow) 
btn = tkinter.Button(btn_frame, text="<< Backward (slow)", command=partial(play, -2))
btn.grid(row=0, column=0, padx=1, pady=5, sticky="ew")

# 2. << Backward (fast)
btn = tkinter.Button(btn_frame, text="<< Backward (fast)", command=partial(play, -25))
btn.grid(row=0, column=1, padx=1, pady=5, sticky="ew")

# 3. Forward (slow) >> 
btn = tkinter.Button(btn_frame, text="Forward (slow) >>", command=partial(play, 2))
btn.grid(row=0, column=2, padx=1, pady=5, sticky="ew")

# 4. Forward (fast) >>
btn = tkinter.Button(btn_frame, text="Forward (fast) >>", command=partial(play, 25))
btn.grid(row=0, column=3, padx=1, pady=5, sticky="ew")

# 5. Signal OUT
btn = tkinter.Button(btn_frame, text="Signal_OUT", command=out)
btn.grid(row=0, column=4, padx=1, pady=5, sticky="ew")

# 6. Signal NOT_OUT
btn = tkinter.Button(btn_frame, text="Signal_NOT-OUT", command=not_out)
btn.grid(row=0, column=5, padx=1, pady=5, sticky="ew")




# ========================== START GUI LOOP ==========================
window.mainloop()


# Author : Jenis Surani
# Date   : 10/04/2025
# Topic  : DECISION-REVIEW-SYSTEM ~ Jenis Surani.