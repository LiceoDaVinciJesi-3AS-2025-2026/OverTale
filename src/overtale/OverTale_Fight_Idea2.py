import pygame
import random
import sys

pygame.init()

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 720, 520
BOX = pygame.Rect(235, 190, 250, 180)

FPS = 60
ROUND_TIME = 6 * FPS
MAX_HP = 92
SANS_HP = 80

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sans Fight Procedurale")
clock = pygame.time.Clock()

font = pygame.font.SysFont("consolas", 20)
big_font = pygame.font.SysFont("consolas", 32)

# ---------------- PLAYER ----------------
soul_w, soul_h = 16, 16
heart_img = pygame.image.load("cuore.png").convert_alpha()
heart_img = pygame.transform.scale(heart_img, (soul_w, soul_h))

def reset_player():
    return BOX.centerx - soul_w//2, BOX.bottom - soul_h

soul_x, soul_y = reset_player()
soul_hp = MAX_HP
soul_inv = 0

# Modalità blu (gravità)
blue_mode = False
vel_y = 0
gravity = 0.6
jump_power = -13   # 🔥 SALTO PIÙ ALTO
on_ground = False

# ---------------- SANS ----------------
sans_hp = SANS_HP

# ---------------- MENU ----------------
state = "menu"
selected = 0
fight_bar = BOX.left
fight_dir = 1
attack_timer = 0

# ---------------- ATTACCHI ----------------
bones = []
lasers = []

# ---------------- MAIN LOOP ----------------
running = True
while running:
    clock.tick(FPS)
    screen.fill((0,0,0))

    # -------- SANS RECT --------
    pygame.draw.rect(screen, (255,255,255), (290, 40, 140, 90), 2)
    screen.blit(big_font.render("SANS", True, (255,255,255)), (325, 70))

    pygame.draw.rect(screen, (255,255,255), BOX, 2)

    # -------- MENU BOXES --------
    fight_rect = pygame.Rect(220, HEIGHT-70, 120, 40)
    mercy_rect = pygame.Rect(380, HEIGHT-70, 120, 40)

    pygame.draw.rect(screen, (255,255,0) if selected==0 else (255,255,255), fight_rect, 2)
    pygame.draw.rect(screen, (255,255,0) if selected==1 else (255,255,255), mercy_rect, 2)

    screen.blit(font.render("FIGHT", True, (255,255,255)), (fight_rect.x+30, fight_rect.y+10))
    screen.blit(font.render("MERCY", True, (255,255,255)), (mercy_rect.x+30, mercy_rect.y+10))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if state == "menu":
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    selected = 1 - selected

                if event.key == pygame.K_RETURN:
                    if selected == 0:
                        state = "fight"
                        fight_bar = BOX.left
                    else:
                        state = "attack"
                        attack_timer = 0
                        bones.clear()
                        lasers.clear()
                        soul_x, soul_y = reset_player()
                        blue_mode = False
                        vel_y = 0

            elif state == "fight" and event.key == pygame.K_RETURN:
                center = BOX.centerx
                dist = abs(fight_bar - center)
                damage = max(3, 25 - dist//5)
                sans_hp -= damage

                state = "attack"
                attack_timer = 0
                bones.clear()
                lasers.clear()
                soul_x, soul_y = reset_player()
                blue_mode = False
                vel_y = 0

            # Salto blu
            if blue_mode and event.key == pygame.K_UP and on_ground:
                vel_y = jump_power

    keys = pygame.key.get_pressed()

    # ---------------- FIGHT ----------------
    if state == "fight":
        pygame.draw.line(screen, (255,0,0),
                         (BOX.centerx, BOX.top),
                         (BOX.centerx, BOX.bottom), 2)

        pygame.draw.rect(screen, (255,255,0),
                         (fight_bar, BOX.top, 5, BOX.height))

        fight_bar += fight_dir * 10
        if fight_bar <= BOX.left or fight_bar >= BOX.right:
            fight_dir *= -1

    # ---------------- ATTACK ----------------
    if state == "attack":
        attack_timer += 1

        if attack_timer >= ROUND_TIME:
            state = "menu"
            blue_mode = False
            bones.clear()
            lasers.clear()

        # Attiva modalità blu dopo 2 sec
        if attack_timer == FPS * 2:
            blue_mode = True

        # SPAWN OSSA
        if attack_timer % 35 == 0:
            if blue_mode:
                y = BOX.bottom - 20
                bones.append([BOX.left-40, y, 40, 10, 5, 0, "platform"])
            else:
                x = random.randint(BOX.left, BOX.right-8)
                bones.append([x, BOX.top-40, 8, 40, 0, 6, "normal"])

        # SPAWN LASER
        if attack_timer % 180 == 0:
            t = random.choice(["vertical","horizontal"])
            pos = random.randint(BOX.left+20, BOX.right-20) if t=="vertical" else random.randint(BOX.top+20, BOX.bottom-20)
            lasers.append([t, pos, 90])

        # MOVIMENTO PLAYER
        if not blue_mode:
            dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 4
            dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) * 4
            soul_x += dx
            soul_y += dy
        else:
            dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * 4
            soul_x += dx

            vel_y += gravity
            soul_y += vel_y

        soul_x = max(BOX.left, min(BOX.right - soul_w, soul_x))
        soul_y = max(BOX.top, min(BOX.bottom - soul_h, soul_y))

        player_rect = pygame.Rect(soul_x, soul_y, soul_w, soul_h)
        on_ground = False

        # OSSA
        for bone in bones[:]:
            bone[0] += bone[4]
            bone[1] += bone[5]
            bone_rect = pygame.Rect(bone[0], bone[1], bone[2], bone[3])
            pygame.draw.rect(screen, (255,255,255), bone_rect)

            if bone[6] == "platform":
                if player_rect.colliderect(bone_rect) and vel_y >= 0:
                    soul_y = bone_rect.top - soul_h
                    vel_y = 0
                    on_ground = True
            else:
                if bone_rect.colliderect(player_rect) and soul_inv == 0:
                    soul_hp -= 5
                    soul_inv = 20

            if bone[0] > BOX.right+60:
                bones.remove(bone)

        # LASER
        for laser in lasers[:]:
            laser[2] -= 1

            if laser[2] > 45:
                if laser[0] == "vertical":
                    pygame.draw.circle(screen, (0,255,255), (laser[1], BOX.centery), 18)
                else:
                    pygame.draw.circle(screen, (0,255,255), (BOX.centerx, laser[1]), 18)
            else:
                beam = pygame.Rect(laser[1]-6, BOX.top, 12, BOX.height) if laser[0]=="vertical" else pygame.Rect(BOX.left, laser[1]-6, BOX.width, 12)
                pygame.draw.rect(screen, (0,255,255), beam)

                if beam.colliderect(player_rect) and soul_inv == 0:
                    soul_hp -= 8
                    soul_inv = 20

            if laser[2] <= 0:
                lasers.remove(laser)

        if soul_inv > 0:
            soul_inv -= 1

        if soul_inv % 6 < 3:
            screen.blit(heart_img, (soul_x, soul_y))

    # ---------------- HP ----------------
    soul_hp = max(0, soul_hp)
    sans_hp = max(0, sans_hp)

    pygame.draw.rect(screen,(255,0,0),(40,HEIGHT-40,soul_hp*2,10))
    screen.blit(font.render(f"PLAYER HP: {soul_hp}",True,(255,255,255)),(40,HEIGHT-60))

    pygame.draw.rect(screen,(0,255,255),(WIDTH-200,40,sans_hp*2,10))
    screen.blit(font.render(f"SANS HP: {sans_hp}",True,(255,255,255)),(WIDTH-200,20))

    # END GAME
    if soul_hp <= 0:
        screen.blit(big_font.render("YOU DIED",True,(255,0,0)),(WIDTH//2-90,HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        break

    if sans_hp <= 0:
        screen.blit(big_font.render("YOU WON",True,(0,255,255)),(WIDTH//2-90,HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        break

    pygame.display.flip()

pygame.quit()
sys.exit()