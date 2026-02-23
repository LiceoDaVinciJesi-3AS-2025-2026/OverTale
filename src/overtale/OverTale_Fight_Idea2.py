import pygame
import random
import sys

pygame.init()

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 720, 520
BOX = pygame.Rect(185, 160, 350, 240)

FPS = 60
MAX_HP = 92
SANS_HP = 80

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sans Fight Procedurale")
clock = pygame.time.Clock()

font = pygame.font.SysFont("consolas", 20)
big_font = pygame.font.SysFont("consolas", 32)

# ---------------- PLAYER ----------------
soul_x = BOX.centerx
soul_y = BOX.bottom - 20
soul_w = 14
soul_h = 14
soul_hp = MAX_HP
soul_inv = 0

# ---------------- SANS ----------------
sans_hp = SANS_HP

# ---------------- MENU ----------------
state = "menu"
selected = 0
fight_bar = BOX.left
fight_dir = 1
attack_timer = 0

# ---------------- ATTACCHI ----------------
bones = []  # ogni osso = [x, y, w, h, dx, dy]
lasers = [] # ogni laser = [type, x/y, timer, active]

# ---------------- MAIN LOOP ----------------
running = True
while running:
    clock.tick(FPS)
    screen.fill((0,0,0))

    # ---------------- Draw Sans ----------------
    pygame.draw.rect(screen, (255,255,255), (290, 40, 140, 90), 2)
    text = big_font.render("SANS", True, (255,255,255))
    screen.blit(text, (325, 60))

    pygame.draw.rect(screen, (255,255,255), BOX, 2)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if state == "menu":
                if event.key == pygame.K_LEFT:
                    selected = 0
                if event.key == pygame.K_RIGHT:
                    selected = 1
                if event.key == pygame.K_RETURN:
                    if selected == 0:
                        state = "fight"
                        fight_bar = BOX.left
                    else:
                        state = "attack"
                        attack_timer = 0

            elif state == "fight" and event.key == pygame.K_RETURN:
                center = BOX.centerx
                dist = abs(fight_bar - center)
                damage = max(3, 25 - dist//5)
                sans_hp -= damage
                state = "attack"
                attack_timer = 0

    keys = pygame.key.get_pressed()

    # ---------------- MENU ----------------
    if state == "menu":
        options = ["FIGHT", "MERCY"]
        for i, txt in enumerate(options):
            color = (255,255,0) if i == selected else (255,255,255)
            text = font.render(txt, True, color)
            screen.blit(text, (250 + i*150, HEIGHT - 50))

    # ---------------- FIGHT ----------------
    elif state == "fight":
        pygame.draw.line(screen, (255,0,0),
                         (BOX.centerx, BOX.top),
                         (BOX.centerx, BOX.bottom), 2)

        pygame.draw.rect(screen, (255,255,0),
                         (fight_bar, BOX.top, 5, BOX.height))

        fight_bar += fight_dir * 10
        if fight_bar <= BOX.left or fight_bar >= BOX.right:
            fight_dir *= -1

    # ---------------- ATTACK ----------------
    elif state == "attack":
        attack_timer += 1

        # Spawn ossa
        if attack_timer % 25 == 0:
            direction = random.choice(["down", "side"])
            if direction == "down":
                x = random.randint(BOX.left, BOX.right-8)
                y = BOX.top - 20
                bones.append([x, y, 8, 50, 0, 6])
            else:
                y = random.randint(BOX.top, BOX.bottom-8)
                x = BOX.left - 20
                bones.append([x, y, 50, 8, 6, 0])

        # Spawn laser
        if attack_timer % 180 == 0:
            laser_type = random.choice(["vertical","horizontal"])
            timer = 90
            active = False
            if laser_type == "vertical":
                x = random.randint(BOX.left + 20, BOX.right - 20)
                lasers.append([laser_type, x, timer, active])
            else:
                y = random.randint(BOX.top + 20, BOX.bottom - 20)
                lasers.append([laser_type, y, timer, active])

        # Muovi player
        dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 4
        dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 4
        soul_x += dx
        soul_y += dy
        soul_x = max(BOX.left, min(BOX.right - soul_w, soul_x))
        soul_y = max(BOX.top, min(BOX.bottom - soul_h, soul_y))

        # Muovi ossa
        for bone in bones[:]:
            bone[0] += bone[4]
            bone[1] += bone[5]
            pygame.draw.rect(screen, (255,255,255), (bone[0], bone[1], bone[2], bone[3]))
            if pygame.Rect(bone[0], bone[1], bone[2], bone[3]).colliderect(pygame.Rect(soul_x, soul_y, soul_w, soul_h)):
                if soul_inv == 0:
                    soul_hp -= 5
                    soul_inv = 15
            # Rimuovi fuori
            if bone[0] > BOX.right+50 or bone[1] > BOX.bottom+50:
                bones.remove(bone)

        # Muovi laser
        for laser in lasers[:]:
            laser[2] -= 1
            if laser[2] == 45:
                laser[3] = True
            # Draw
            if laser[2] > 45:
                if laser[0] == "vertical":
                    pygame.draw.circle(screen, (0,255,255), (laser[1], BOX.centery), 18)
                else:
                    pygame.draw.circle(screen, (0,255,255), (BOX.centerx, laser[1]), 18)
            elif laser[3]:
                if laser[0] == "vertical":
                    pygame.draw.rect(screen, (0,255,255), (laser[1]-6, BOX.top, 12, BOX.height))
                    if abs(soul_x + soul_w//2 - laser[1]) < 12 and soul_inv == 0:
                        soul_hp -= 8
                        soul_inv = 15
                else:
                    pygame.draw.rect(screen, (0,255,255), (BOX.left, laser[1]-6, BOX.width, 12))
                    if abs(soul_y + soul_h//2 - laser[1]) < 12 and soul_inv == 0:
                        soul_hp -= 8
                        soul_inv = 15
            if laser[2] <= 0:
                lasers.remove(laser)

        if soul_inv > 0:
            soul_inv -= 1

        # Draw player
        color = (255,0,0) if soul_inv == 0 else (255,255,255)
        pygame.draw.rect(screen, color, (soul_x, soul_y, soul_w, soul_h))

    # ---------------- HP ----------------
    # Limiti HP minimi
    soul_hp = max(0, soul_hp)
    sans_hp = max(0, sans_hp)

    # ---------------- PLAYER ----------------
    soul_x = BOX.centerx
    soul_y = BOX.bottom - 20
    soul_w = 14
    soul_h = 14
    soul_hp = MAX_HP
    soul_inv = 0

    # Carica immagine cuore
    heart_img = pygame.image.load("cuore.png").convert_alpha()
    heart_img = pygame.transform.scale(heart_img, (soul_w, soul_h))

    # Sans HP
    pygame.draw.rect(screen, (0,255,255), (WIDTH-180, 20, sans_hp*2, 8))
    sans_hp_text = font.render(f"HP: {sans_hp}", True, (255,255,255))
    screen.blit(sans_hp_text, (WIDTH-180, 0))

    # ---------------- CHECK VITTORIA/SCONFITTA ----------------
    if soul_hp <= 0:
        txt = big_font.render("YOU DIED", True, (255,0,0))
        screen.blit(txt, (WIDTH//2 - 90, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    if sans_hp <= 0:
        txt = big_font.render("YOU WON", True, (0,255,255))
        screen.blit(txt, (WIDTH//2 - 90, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False

    pygame.display.flip()

pygame.quit()
sys.exit()