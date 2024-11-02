import string
import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
info = pygame.display.Info()  # Get screen resolution
width, height = info.current_w, info.current_h  # Use current screen width and height
# Set borderless window with an offset (10 pixels to the right)
screen = pygame.display.set_mode((width, height), pygame.NOFRAME)  # Create a borderless window
pygame.display.set_caption("Matrix Rain")

# Move the window slightly to the right
pygame.display.set_mode((width, height), pygame.NOFRAME)  # Reset to apply no frame
pygame.display.set_caption("Matrix Rain")
pygame.display.set_mode((width, height), pygame.NOFRAME)
pygame.display.set_caption("Matrix Rain")

# Set up colors
black = (0, 0, 0)
green = (0, 255, 0)

# Set up font
font_size = 30
font = pygame.font.SysFont('SerifBold', font_size)

# Create a list to hold the falling characters
drops = [0] * (width // font_size)  # Initialize drops

# Set the initial position for each drop to be above the screen
for i in range(len(drops)):
    drops[i] = random.randint(-height // font_size, 0)  # Start drops above the screen

running = True
while running:
    screen.fill(black)

    for i in range(len(drops)):
        # Randomly choose a character
        char = random.choice(string.printable)  # Use any printable character
        text = font.render(char, True, green)

        # Draw the character on the screen
        screen.blit(text, (i * font_size, drops[i] * font_size))

        # Update the drop position
        drops[i] += 1  # Move drop down by 1 unit

        # Reset the drop if it goes beyond the bottom of the screen
        if drops[i] * font_size >= height:
            drops[i] = random.randint(-height // font_size, 0)  # Reset to above the screen

    pygame.display.flip()
    pygame.time.delay(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
