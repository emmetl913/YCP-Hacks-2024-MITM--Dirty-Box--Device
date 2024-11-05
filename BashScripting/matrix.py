import string
import pygame
import random
import pygetwindow as gw
import time

# Initialize pygame and set up display
pygame.init()
info = pygame.display.Info()
width, height = info.current_w, info.current_h
screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
pygame.display.set_caption("Matrix Rain")

# Set up window title and delay to ensure display initialization
window_title = "Matrix Rain"
time.sleep(0.5)  # Give time for the display to initialize

try:
    window = gw.getWindowsWithTitle(window_title)[0]
except IndexError:
    print(f"No window with title '{window_title}' found.")
    pygame.quit()
    exit()

# Colors and settings
black = (0, 0, 0)
green = (0, 255, 0)
font_size = 30
font = pygame.font.SysFont('SerifBold', font_size)
drops = [random.randint(-height // font_size, 0) for _ in range(width // font_size)]

# Function to activate window on specific event detection
def ensure_window_focus():
    for event in pygame.event.get():
        if event.type == pygame.ACTIVEEVENT:  # Detect if window gains focus
            window.activate()  # Bring the window to the front

running = True
while running:
    # Check for window focus and bring to front if needed
    ensure_window_focus()

    # Draw background and random characters
    screen.fill(black)
    for i in range(len(drops)):
        char = random.choice(string.printable)
        text = font.render(char, True, green)
        screen.blit(text, (i * font_size, drops[i] * font_size))
        drops[i] += 1
        if drops[i] * font_size >= height:
            drops[i] = random.randint(-height // font_size, 0)

    pygame.display.flip()
    pygame.time.delay(20)

    # Check for quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
