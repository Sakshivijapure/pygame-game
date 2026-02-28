import pygame
import random
import sys


pygame.init()


WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Memory Match")


font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 60)


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (50, 100, 200)
GREEN = (50, 200, 100)
RED = (200, 50, 50)


clock = pygame.time.Clock()


def generate_cards(pair_count):
    pairs = []
    for _ in range(pair_count):
        a = random.randint(2, 9)
        b = random.randint(2, 9)
        equation = f"{a} x {b}"
        answer = str(a * b)
        pairs.append((equation, answer))
    cards = []
    for pair in pairs:
        cards.extend(pair)
    random.shuffle(cards)
    return cards, pairs


def draw_text(text, font, color, x, y):
    rendered = font.render(text, True, color)
    screen.blit(rendered, (x, y))


def draw_menu():
    screen.fill(WHITE)
    title = big_font.render("Math Memory Match", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    easy = pygame.Rect(WIDTH//2 - 100, 200, 200, 50)
    medium = pygame.Rect(WIDTH//2 - 100, 280, 200, 50)
    hard = pygame.Rect(WIDTH//2 - 100, 360, 200, 50)


    pygame.draw.rect(screen, BLUE, easy)
    pygame.draw.rect(screen, BLUE, medium)
    pygame.draw.rect(screen, BLUE, hard)


    draw_text("Easy (3 Pairs)", font, WHITE, easy.x + 20, easy.y + 10)
    draw_text("Medium (5 Pairs)", font, WHITE, medium.x + 20, medium.y + 10)
    draw_text("Hard (8 Pairs)", font, WHITE, hard.x + 20, hard.y + 10)


    return easy, medium, hard


def draw_cards(cards, revealed, cols):
    card_width = 100
    card_height = 60
    margin = 20
    for i, card in enumerate(cards):
        row = i // cols
        col = i % cols
        x = margin + col * (card_width + margin)
        y = margin + row * (card_height + margin) + 80
        rect = pygame.Rect(x, y, card_width, card_height)
        color = GREEN if revealed[i] else BLUE
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 2)
        if revealed[i]:
            draw_text(str(card), font, BLACK, x + 10, y + 15)


def draw_stats(tries, score, feedback):
    draw_text(f"Tries: {tries}  Score: {score}", font, BLACK, 20, 20)
    if feedback != "":
        color = GREEN if feedback == "Correct!" else RED
        draw_text(feedback, font, color, WIDTH - 200, 20)


def draw_win_screen(tries, score):
    screen.fill(WHITE)
    msg = big_font.render(f"You Win! Tries: {tries}  Score: {score}", True, BLACK)
    screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//3))


    play_again = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 50)
    main_menu = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 70, 200, 50)


    pygame.draw.rect(screen, BLUE, play_again)
    pygame.draw.rect(screen, BLUE, main_menu)


    draw_text("Play Again", font, WHITE, play_again.x + 40, play_again.y + 10)
    draw_text("Main Menu", font, WHITE, main_menu.x + 45, main_menu.y + 10)


    return play_again, main_menu


# Game variables
menu = True
playing = False
win_screen = False


cards = []
pairs = []
revealed = []
selected = []
matches = 0
tries = 0
score = 0
feedback = ""
cols = 0
check_time = 0
difficulty = 0


while True:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            if menu:
                easy_btn, med_btn, hard_btn = draw_menu()
                if easy_btn.collidepoint(mx, my):
                    difficulty = 3
                elif med_btn.collidepoint(mx, my):
                    difficulty = 5
                elif hard_btn.collidepoint(mx, my):
                    difficulty = 8
                else:
                    continue
                cards, pairs = generate_cards(difficulty)
                revealed = [False] * len(cards)
                selected = []
                matches = 0
                tries = 0
                score = 100
                feedback = ""
                cols = min(len(cards), 6)
                menu = False
                playing = True
                win_screen = False
                check_time = 0


            elif playing and not win_screen and check_time == 0:
                card_width = 100
                card_height = 60
                margin = 20
                for i in range(len(cards)):
                    row = i // cols
                    col = i % cols
                    x = margin + col * (card_width + margin)
                    y = margin + row * (card_height + margin) + 80
                    rect = pygame.Rect(x, y, card_width, card_height)
                    if rect.collidepoint(mx, my) and not revealed[i] and len(selected) < 2:
                        revealed[i] = True
                        selected.append(i)
                        if len(selected) == 2:
                            check_time = pygame.time.get_ticks() + 700


            elif win_screen:
                play_again_rect, menu_rect = draw_win_screen(tries, score)
                if play_again_rect.collidepoint(mx, my):
                    cards, pairs = generate_cards(difficulty)
                    revealed = [False] * len(cards)
                    selected = []
                    matches = 0
                    tries = 0
                    score = 100
                    feedback = ""
                    cols = min(len(cards), 6)
                    playing = True
                    win_screen = False
                    check_time = 0
                elif menu_rect.collidepoint(mx, my):
                    menu = True
                    playing = False
                    win_screen = False


    if playing and not win_screen:
        if check_time > 0 and pygame.time.get_ticks() >= check_time:
            i, j = selected
            tries += 1
            c1, c2 = cards[i], cards[j]
            if ("x" in c1 and c2.isdigit() and eval(c1.replace("x", "*")) == int(c2)) or \
               ("x" in c2 and c1.isdigit() and eval(c2.replace("x", "*")) == int(c1)):
                matches += 1
                feedback = "Correct!"
            else:
                revealed[i] = False
                revealed[j] = False
                feedback = "Wrong!"
            selected = []
            score = max(100 - tries * 5, 0)
            check_time = 0


        draw_cards(cards, revealed, cols)
        draw_stats(tries, score, feedback)


        if matches == len(pairs):
            playing = False
            win_screen = True


    elif menu:
        draw_menu()


    elif win_screen:
        draw_win_screen(tries, score)


    pygame.display.flip()
    clock.tick(30)



