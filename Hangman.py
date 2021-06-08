import pygame
import math
import os
from random_words import RandomWords
rw = RandomWords()

# Display
width, height = 900, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Hangman")
fps = 60
clock = pygame.time.Clock()

# Font
pygame.init()
letter_font = pygame.font.SysFont("arial", 30)

word_font = pygame.font.SysFont("arial", 50)

# Buttons
letters = []
gap = 20  # between the buttons
radius = 22
startx = round((width - (radius * 2 + gap) * 13) / 2)
starty = 450
A = 65
for i in range(26):
    x = startx + gap * 2 + ((radius * 2 + gap) * (i % 13))
    y = starty + ((i // 13) * (gap + radius * 2))
    letters.append([x, y, chr(A + i), True])

# Stores the hangman images
images = []
for i in range(9):
    hangman_images = pygame.image.load(os.path.join("Background", "{}" + ".jpg").format(i))
    images.append(hangman_images)
# Image that appears on window
hangman_status = 0

# Word
RandomWord = rw.random_words()
word = str(','.join(str(i) for i in RandomWord)).upper()
words_guessed = []

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
light_grey = (211, 211, 211)


def display_message(text):
    pygame.time.delay(2000)
    window.fill(white)
    message = letter_font.render(text, True, red)
    window.blit(message, (width / 2 - message.get_width() / 2, height / 2 - message.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(4000)


def draw_window():
    window.fill(light_grey)

    # Draw Word
    display_word = ""
    for letter in word:
        if letter in words_guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = word_font.render(display_word, True, black)
    window.blit(text, (400, 250))

    # Draw Buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(window, black, (x, y), radius, 3)
            text = letter_font.render(ltr, True, black)
            window.blit(text, (x - text.get_width()/2, y - text.get_height()/2))
    window.blit(images[hangman_status], (100, 50))
    pygame.display.update()


def main():
    global hangman_status
    while True:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Collision
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        distance = math.sqrt((mouse_x - x) ** 2 + (mouse_y - y) ** 2)  # distance between mouse and center of button
                        if distance < radius:
                            letter[3] = False
                            words_guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
        draw_window()

        won = True
        for letter in word:
            if letter not in words_guessed:
                won = False
                break

        if won:
            display_message("You Won!")
            break

        if hangman_status == 8:
            display_message(f"You Lost! The word is {word}.")
            break

main()
