import pygame
import random
import sys

pygame.init()

# Window setup
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Math Memory Match")

font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 60)

# Dark theme colors
BACKGROUND = (18, 18, 25)          # Deep dark background
CARD_BACK = (60, 60, 80)           # Dark gray-blue card back
CARD_FRONT = (100, 200, 100)       # Soft neon green for open cards
TEXT_COLOR = (240, 240, 240)       # Off-white text
BORDER_COLOR = (200, 180, 80)      # Golden border

# Sounds
win_sound = pygame.mixer.Sound("C:\\Users\\vijap\\OneDrive\\Desktop\\game\\sound\\win.wav")
lose_sound = pygame.mixer.Sound("C:\\Users\\vijap\\OneDrive\\Desktop\\game\\sound\\loose.wav")
right_sound = pygame.mixer.Sound("C:\\Users\\vijap\\OneDrive\\Desktop\\game\\sound\\right.wav")

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

def draw_text_center(text, font, color, rect):
    rendered = font.render(text, True, color)
    text_rect = rendered.get_rect(center=rect.center)
    screen.blit(rendered, text_rect)

def draw_menu():
    screen.fill(BACKGROUND)
    title = big_font.render("Math Memory Match", True, TEXT_COLOR)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

    easy = pygame.Rect(WIDTH//2 - 120, 220, 240, 55)
    medium = pygame.Rect(WIDTH//2 - 120, 300, 240, 55)
    hard = pygame.Rect(WIDTH//2 - 120, 380, 240, 55)

    for btn in [easy, medium, hard]:
        pygame.draw.rect(screen, (45, 45, 60), btn, border_radius=15)
        pygame.draw.rect(screen, BORDER_COLOR, btn, 3, border_radius=15)

    draw_text_center("Easy (3 Pairs)", font, TEXT_COLOR, easy)
    draw_text_center("Medium (5 Pairs)", font, TEXT_COLOR, medium)
    draw_text_center("Hard (8 Pairs)", font, TEXT_COLOR, hard)

    return easy, medium, hard

def draw_cards(cards, revealed, cols):
    card_width = 120
    card_height = 70
    margin = 25
    start_x = (WIDTH - (cols * (card_width + margin) - margin)) // 2
    start_y = 100

    for i, card in enumerate(cards):
        row = i // cols
        col = i % cols
        x = start_x + col * (card_width + margin)
        y = start_y + row * (card_height + margin)
        rect = pygame.Rect(x, y, card_width, card_height)
        color = CARD_FRONT if revealed[i] else CARD_BACK
        pygame.draw.rect(screen, color, rect, border_radius=10)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 2, border_radius=10)
        if revealed[i]:
            draw_text_center(str(card), font, TEXT_COLOR, rect)

def draw_stats(tries, score, feedback):
    draw_text = font.render(f"Tries: {tries}  Score: {score}", True, TEXT_COLOR)
    screen.blit(draw_text, (20, 20))
    if feedback != "":
        color = (120, 220, 120) if feedback == "Correct!" else (255, 100, 100)
        feedback_text = font.render(feedback, True, color)
        screen.blit(feedback_text, (WIDTH - 200, 20))

def draw_win_screen(tries, score):
    screen.fill(BACKGROUND)
    msg = big_font.render(f"You Win! Tries: {tries}  Score: {score}", True, TEXT_COLOR)
    screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 3))

    play_again = pygame.Rect(WIDTH//2 - 120, HEIGHT//2, 240, 55)
    main_menu = pygame.Rect(WIDTH//2 - 120, HEIGHT//2 + 80, 240, 55)

    for btn in [play_again, main_menu]:
        pygame.draw.rect(screen, (45, 45, 60), btn, border_radius=15)
        pygame.draw.rect(screen, BORDER_COLOR, btn, 3, border_radius=15)

    draw_text_center("Play Again", font, TEXT_COLOR, play_again)
    draw_text_center("Main Menu", font, TEXT_COLOR, main_menu)

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
    screen.fill(BACKGROUND)
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
                card_width = 120
                card_height = 70
                margin = 25
                start_x = (WIDTH - (cols * (card_width + margin) - margin)) // 2
                start_y = 100
                for i in range(len(cards)):
                    row = i // cols
                    col = i % cols
                    x = start_x + col * (card_width + margin)
                    y = start_y + row * (card_height + margin)
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
                right_sound.play()
            else:
                revealed[i] = False
                revealed[j] = False
                feedback = "Wrong!"
                lose_sound.play()
            selected = []
            score = max(100 - tries * 5, 0)
            check_time = 0

        draw_cards(cards, revealed, cols)
        draw_stats(tries, score, feedback)

        if matches == len(pairs):
            playing = False
            win_screen = True
            win_sound.play()

    elif menu:
        draw_menu()

    elif win_screen:
        draw_win_screen(tries, score)

    pygame.display.flip()
    clock.tick(30)
