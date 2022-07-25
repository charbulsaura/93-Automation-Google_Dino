# Assignment: Automate the Google Dinosaur Game
"""
Write Python code to play the Google Dinosaur Game.
"""
"""
On Chrome, when you try to access a website and your internet is down, you see a little dinosaur. 
(Apparently because dinosaurs have short arms and they "can't reach" your website.

On this page, there is a hidden game, if you hit space bar you can play the T-rex run game.

Alternatively you can access the game directly here:
https://elgoog.im/t-rex/

You goal today is to write a Python script to automate the playing of this game. 
Your program will look at the pixels on the screen to determine when it needs to hit the space bar and play the game automatically.
You can see what it looks like when the game is automated with a bot:
https://elgoog.im/t-rex/?bot

You might want to look up these two packages:
https://pypi.org/project/Pillow/  --- image processing python module
https://pyautogui.readthedocs.io/en/latest/  ---automates GUI /auto clicker
"""
# PyAutoGUI has several features:
"""
Moving the mouse and clicking in the windows of other applications.
Sending keystrokes to applications (for example, to fill out forms).
Take screenshots, and given an image (for example, of a button or checkbox), and find it on the screen.
Locate an application’s window, and move, resize, maximize, minimize, or close it (Windows-only, currently).
Display alert and message boxes.

...control the mouse and keyboard as well as perform basic image recognition to automate tasks on your computer
"""

# Approach
"""
0!. Using Selenium, Start up automatic chrome runner to load google dinosaur game
   --Maximize screen first, wait a few seconds before capturing screen
   (selenium maximize window)
1!. Process image using PIL 
    -- How to import snapshot of current screen? 
       >Python Pillow export image of current screen (ImageGrab)
       >Display image in python program so u can figure out what to detect
    -- How to detect objects of interest?
        >Python Pillow detect objects on image/ detect shapes?
        - USE PY AUTO GUI - https://pyautogui.readthedocs.io/en/latest/screenshot.html
        ---------------------------------------------------------
        The Locate Functions
        You can visually locate something on the screen if you have an image file of it.
        -PRELOAD DINO AND CACTUS OBSTACLE IMAGES TO pyautogui SO THAT IT CAN DETECT LOCATION OF BOTH OBJECTS
        -IF COORDINATES RETURNED ARE ALMOST SIMILAR; MAKE DINO JUMP
        -Minor problem : Has various cactus shapes & sizes + groupings... might not be able to account for every obstacle
        --------------------------------------------------------- 
        - Sample image as comparison?
        - Label object as dino
        - If another object in front of dino, trigger condition to jump (determine/measure using distance bet 2 object)
2. When to check for obstacles?
    -- Check every few frames/few seconds? (Every main loop)
3. Detect obstacles, then jump (using automatic selenium keyboard input?)
"""
import PIL
import pyautogui
import cv2
import time
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageGrab, ImageOps
import numpy as np

from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def dino_location():
    global dino, dino_coordinates
    dino = pyautogui.locateCenterOnScreen("dino.png", confidence=0.8)
    dino_coordinates = (dino.x, dino.y)
    # print(dino_coordinates)
    # print(f"Dino is at: {dino}")
    # print(f"Dino.x is at: {dino.x}")

# PIL.ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=False, xdisplay=None)
# Take a snapshot of the screen.
# The pixels inside the bounding box are returned as an “RGBA” on macOS, or an “RGB” image otherwise.
# If the bounding box is omitted, the entire screen is copied.

# PIL.ImageOps.grayscale(image)
# Convert the image to grayscale.

def dino_collision_area():
    """Zone or area of coordinates where dino will collide with cactus

    #ALTERNATIVE: Count # of white pixels in area in front of dino instead of comparing to cactus image (unreliable)
    #If sum of white pixels in area < normal sum of white pixel value, dino should jump
    #DINO WIDTH 45 PIXEL, HEIGHT 44 PIXEL
    #Trouble lies in determining ideal area of collision in front of dino
    """
    # Image recognition not working bcos of movement that blurs image; using pixel detection instead
    # dino = pyautogui.locateOnScreen("dino.png", confidence=0.8)
    # print(f"Dino is at: {dino}")
    collision_area = (dino_coordinates[0]+20 ,dino_coordinates[1], dino_coordinates[0]+125,dino_coordinates[1]+5)
    #Grabs area in front of dino for pixel analysis
    collision_analysis = ImageGrab.grab(collision_area)
    #Detects # of white pixels
    collision_detection = ImageOps.grayscale(collision_analysis)
    #Sums the # of white pixels (compare to white pixels in main loop)
    sum_of_pixels_for_incoming_object = np.array(collision_detection.getcolors()) #https://pillow.readthedocs.io/en/stable/reference/ImageColor.html
    print(sum_of_pixels_for_incoming_object.sum())
    return sum_of_pixels_for_incoming_object.sum()

def dino_jump():
    pyautogui.press("space")
    time.sleep(0.05)
    print("DINO JUMPED!")


chrome_driver_path = Service("chromedriver_win32\chromedriver.exe")
driver = webdriver.Chrome(service=chrome_driver_path)
# driver.maximize_window()
driver.get("https://elgoog.im/t-rex/")
jump = True
running = True
dino = None
dino_coordinates = (0,0)
# Wait for dino program to load, then press space to start dino race
time.sleep(3)
pyautogui.press("space")

while running:
    """
    USE
    locateCenterOnScreen(image, grayscale=False) - Returns (x, y) coordinates of the center of the first found instance of the image on the screen
    instead of locateOnScreen
    """
    dino_location()
    # dino_collision_area()

    # If # of white pixels != original # of white pixels, jump to avoid obstacle
    if dino_collision_area() != 772:
        dino_jump()

    # CONFIDENCE = 0.5
    # cactus_L = pyautogui.locateCenterOnScreen('CactusL.png', confidence=CONFIDENCE)
    # print(f"CactusL is at: {cactus_L}")
    # cactus_LT = pyautogui.locateCenterOnScreen('CactusLT.png', confidence=CONFIDENCE)
    # print(f"CactusLT is at: {cactus_LT}")
    # cactus_M1 = pyautogui.locateCenterOnScreen('CactusM1.png', confidence=CONFIDENCE)
    # print(f"CactusM1 is at: {cactus_M1}")
    # cactus_M2 = pyautogui.locateCenterOnScreen('CactusM2.png', confidence=CONFIDENCE)
    # print(f"CactusM2 is at: {cactus_M2}")
    # cactus_2 = pyautogui.locateCenterOnScreen('Cactusx2.png', confidence=CONFIDENCE)
    # print(f"Cactus2 is at: {cactus_2}")
    # cactus_3 = pyautogui.locateCenterOnScreen('Cactusx3.png', confidence=CONFIDENCE)
    # print(f"Cactus3 is at: {cactus_3}")
    # cactus_4 = pyautogui.locateCenterOnScreen('Cactusx4.png', confidence=CONFIDENCE)
    # print(f"Cactus4 is at: {cactus_4}")
    # cactus_5 = pyautogui.locateCenterOnScreen('Cactusx5.png', confidence=CONFIDENCE)
    # print(f"Cactus4 is at: {cactus_5}")
    #
    # cactus_collection = [cactus_L, cactus_LT, cactus_M1, cactus_M2, cactus_2, cactus_3, cactus_4, cactus_5]

    """
    # FIGURE OUT WHEN TO JUMP: Dino jumping condition (undecided yet)
    # IF dino left (no right) location near cactus left location--- jump
    # Issue 1: Cactus image only detectable when dino stops running (a.k.a crashed)

    # Now able to detect cactus but somehow dino doesnt jump/keyboard input not registering!
    # FINALLY STARTS JUMPING ONCE dino_jump FUNCTION IS CREATED!
    # Issue 2: DINO JUMPED but didnt jump
    # Issue 2.1: Dino jumping at random locations except at cactus itself - might be confidence set too low (but too high cant detect until collision)
    # Issue 3: Dino jumping after even after reference cactus is passed? - lag/ poor module response time
    
    On a 1920 x 1080 screen, the locate function calls take about 1 or 2 seconds. 
    This may be too slow for action video games, but works for most purposes and applications
    """
     #Issue 4: DINO LAG (PYTHON MODULE PROBLEM- should have nothing to do with ur code logic). ONLY JUMP AFTER CRASHING AND RELOADING
    #ALTERNATIVE: Count # of white pixels in box in front of dino instead of comparing to cactus image (unreliable)
    #If sum of white pixels in box < normal sum of white pixel value, dino should jump

    # try:
    #     for cactus in cactus_collection:
    #         distance_bet_dino_cactus = dino.x-cactus.x
    #         print(distance_bet_dino_cactus)
    #         # print(type(distance_bet_dino_cactus))
    #         if abs(distance_bet_dino_cactus) < 200:
    #             # need more distance for slow reaction time of dino #but instead it keeps jumping randomly/too early
    #             print("DINO PLS JUMP!")
    #             jump = True
    #             dino_jump()
    #         else:
    #             jump = False
    # except AttributeError:
    #     pass
    if dino is None:
        running = False

# dinosaur = ImageGrab.grab()
# dinosaur.show()

# dino = pyautogui.locateOnScreen('dino.png', confidence=0.9)
# print(f"Dino is at: {dino}")
# CONFIDENCE = 0.4
# cactus_L = pyautogui.locateOnScreen('CactusL.png', confidence=CONFIDENCE)
# print(f"CactusL is at: {cactus_L}")
# cactus_LT = pyautogui.locateOnScreen('CactusLT.png', confidence=CONFIDENCE)
# print(f"CactusLT is at: {cactus_LT}")
# cactus_M1 = pyautogui.locateOnScreen('CactusM1.png', confidence=CONFIDENCE)
# print(f"CactusM1 is at: {cactus_M1}")
# cactus_M2 = pyautogui.locateOnScreen('CactusM2.png', confidence=CONFIDENCE)
# print(f"CactusM2 is at: {cactus_M2}")
# cactus_2 = pyautogui.locateOnScreen('Cactusx2.png', confidence=CONFIDENCE)
# print(f"Cactus2 is at: {cactus_2}")
# cactus_3 = pyautogui.locateOnScreen('Cactusx3.png', confidence=CONFIDENCE)
# print(f"Cactus3 is at: {cactus_3}")
# cactus_4 = pyautogui.locateOnScreen('Cactusx4.png', confidence=CONFIDENCE)
# print(f"Cactus4 is at: {cactus_4}")
# cactus_5 = pyautogui.locateOnScreen('Cactusx5.png', confidence=CONFIDENCE)
# print(f"Cactus4 is at: {cactus_5}")