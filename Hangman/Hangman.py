import pygame
import math
import random

# setup display
pygame.init()
WIDTH, HEIGHT = 1920, 720
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game")

# button variables
RADIUS = 30
GAP = 25
letters = []
startx = round((WIDTH - (RADIUS * 2 + GAP) * 13) / 2)
starty = 400
A = 65
for i in range(26):
        x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
        y = starty + ((i // 13) * (GAP + RADIUS * 2))
        letters.append([x, y, chr(A + i), True])

# fonts
LETTER_FONT = pygame.font.SysFont('arial', 40)
WORD_FONT = pygame.font.SysFont('calabri', 60)
TITLE_FONT = pygame.font.SysFont('comicsans', 70)

# load images
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)

# game variables
hangman_status = 0
words = ["PYTHON", "PYGAME", "CODE", "GITHUB", "VISUALSTUDIOCODE", "HANGMAN"]
word = random.choice(words)
guessed = []

# colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (213, 73, 36)


def draw():
    win.fill(WHITE)
    
    # draw title
    text = TITLE_FONT.render("Hangman", 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, 20))

    # draw word
    display_word = ""
    for letter in word:
        if letter in guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    text = WORD_FONT.render(display_word, 1, RED)
    win.blit(text, (320, 180))

    # draw buttons
    for letter in letters:
        x, y, ltr, visible = letter
        if visible:
            pygame.draw.circle(win, BLACK, (x, y), RADIUS, 2)
            text = LETTER_FONT.render(ltr, 0.5, BLACK)
            win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

    win.blit(images[hangman_status], (150, 100))
    pygame.display.update()


def display_message(message):
    pygame.time.delay(1000)
    win.fill(WHITE)
    text = WORD_FONT.render(message, 1, BLACK)
    win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/1))
    pygame.display.update()
    pygame.time.delay(2000)

# function to display an image
def display_image(image_path, scale):
    """Loads and scales an image for display."""
    try:
        image = pygame.image.load(image_path)  # Load the image
        image = pygame.transform.scale(image, (scale, scale))  # Scale the image
        return image
    except pygame.error as e:
        print(f"Error loading image {image_path}: {e}")
        return None # Return None if image loading fails

# load images.  Add trollege image
images = []
for i in range(7):
    image = pygame.image.load("hangman" + str(i) + ".png")
    images.append(image)
try:
    trollege_image = pygame.image.load("trollege.jfif")
except pygame.error as e:
    print(f"Error loading trollege.jfif: {e}")
    trollege_image = None # Handle the case where the image is not found

def main():
    global hangman_status

    FPS = 60
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for letter in letters:
                    x, y, ltr, visible = letter
                    if visible:
                        dis = math.sqrt((x - m_x)**2 + (y - m_y)**2)
                        if dis < RADIUS:
                            letter[3] = False
                            guessed.append(ltr)
                            if ltr not in word:
                                hangman_status += 1
                        

        draw()

        won = True
        for letter in word:
            if letter not in guessed:
                won = False
                break

        # Victory Screen
        if won:
            display_message("You WON!")
            break

        # Defeat screen
        if hangman_status == 6:
            display_message("You LOST!")
            if trollege_image:
                # Create a list of rects for multiple images
                trollege_rects = []
                for _ in range(50):  # Generate 50 images
                    x = random.randint(0, WIDTH - trollege_image.get_width())
                    y = random.randint(0, HEIGHT - trollege_image.get_height())
                    trollege_rects.append(trollege_image.get_rect(topleft=(x, y)))

                # Blit multiple images
                for rect in trollege_rects:
                    win.blit(trollege_image, rect)
                pygame.display.update()
                pygame.time.delay(1000)
            break

while True:

    main()
    pygame.display.quit()
pygame.quit()