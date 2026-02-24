import pygame
import random
import sys

def undertale_fight():
    pygame.init()
    WIDTH, HEIGHT = 900, 700
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sans Fight System")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 28)

    arena = pygame.Rect(150, 250, WIDTH-300, HEIGHT-350)

    # Player
    player_img = pygame.image.load("Undertale.png")
    player_img = pygame.transform.scale(player_img, (30, 30))
    player_rect = player_img.get_rect(center=arena.center)
    player_hp = 100

    # Sans (rettangolo)
    sans_rect = pygame.Rect(WIDTH//2 - 50, 100, 100, 40)
    sans_hp = 30

    state = "menu"   # "menu" o "enemy"
    selected = 0     # 0 = FIGHT, 1 = MERCY

    attack_timer = 0
    attack_duration = 6500
    phase = 1

    speed = 5
    gravity = 0.7
    jump_power = -13
    y_vel = 0
    is_blue = False

    bones = []
    lasers = []

    running = True
    while running:
        dt = clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                # ---------------- MENU PLAYER ----------------
                if state == "menu":
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        selected = 1 - selected

                    if event.key == pygame.K_z:

                        # FIGHT
                        if selected == 0:
                            damage = random.randint(4, 8)
                            sans_hp -= damage

                        # MERCY
                        if selected == 1:
                            if sans_hp <= 5:
                                print("Hai risparmiato Sans!")
                                pygame.quit()
                                sys.exit()

                        # Passa al turno nemico
                        state = "enemy"
                        attack_timer = 0
                        phase = random.randint(1,3)
                        is_blue = (phase == 3)

        # ---------------- TURNO NEMICO ----------------
        if state == "enemy":
            attack_timer += dt
            keys = pygame.key.get_pressed()

            # Movimento
            if not is_blue:
                if keys[pygame.K_LEFT]: player_rect.x -= speed
                if keys[pygame.K_RIGHT]: player_rect.x += speed
                if keys[pygame.K_UP]: player_rect.y -= speed
                if keys[pygame.K_DOWN]: player_rect.y += speed
            else:
                if keys[pygame.K_LEFT]: player_rect.x -= speed
                if keys[pygame.K_RIGHT]: player_rect.x += speed
                if keys[pygame.K_SPACE] and player_rect.bottom >= arena.bottom:
                    y_vel = jump_power

                y_vel += gravity
                player_rect.y += y_vel

                if player_rect.bottom >= arena.bottom:
                    player_rect.bottom = arena.bottom
                    y_vel = 0

            player_rect.clamp_ip(arena)

            # -------- FASE 1: OSSA --------
            if phase == 1:
                if random.randint(1,20) == 1:
                    x = random.randint(arena.left, arena.right-20)
                    bones.append(pygame.Rect(x, arena.top-60, 20, 60))

            # -------- FASE 2: OSSA + LASER --------
            if phase == 2:
                if random.randint(1,25) == 1:
                    x = random.randint(arena.left, arena.right-20)
                    bones.append(pygame.Rect(x, arena.top-60, 20, 60))

                if random.randint(1,70) == 1:
                    lasers.append(pygame.Rect(arena.left, random.randint(arena.top, arena.bottom-10), arena.width, 10))

            # -------- FASE 3: SALTO BLU --------
            if phase == 3:
                if random.randint(1,25) == 1:
                    y = arena.bottom - 20
                    bones.append(pygame.Rect(arena.left-60, y, 60, 20))

            # Movimento ossa
            for bone in bones[:]:
                if phase in [1,2]:
                    bone.y += 8
                else:
                    bone.x += 10

                if bone.colliderect(player_rect):
                    player_hp -= 1
                    bones.remove(bone)

                if bone.top > arena.bottom or bone.left > arena.right:
                    bones.remove(bone)

            # Laser collision
            for laser in lasers:
                if laser.colliderect(player_rect):
                    player_hp -= 1

            # Fine turno nemico
            if attack_timer > attack_duration:
                state = "menu"
                bones.clear()
                lasers.clear()
                is_blue = False
                player_rect.center = arena.center

        # -------- GAME OVER --------
        if player_hp <= 0:
            print("Game Over")
            pygame.quit()
            sys.exit()

        if sans_hp <= 0:
            print("Hai sconfitto Sans!")
            pygame.quit()
            sys.exit()

        # ---------------- DISEGNO ----------------
        screen.fill((0,0,0))

        pygame.draw.rect(screen, (255,255,255), sans_rect)
        pygame.draw.rect(screen, (255,255,255), arena, 3)

        if is_blue:
            blue = player_img.copy()
            blue.fill((0,0,255), special_flags=pygame.BLEND_RGB_MULT)
            screen.blit(blue, player_rect)
        else:
            screen.blit(player_img, player_rect)

        for bone in bones:
            pygame.draw.rect(screen, (255,255,255), bone)

        for laser in lasers:
            pygame.draw.rect(screen, (0,255,255), laser)

        # UI HP
        screen.blit(font.render(f"HP: {player_hp}", True, (255,255,255)), (50, 650))
        screen.blit(font.render(f"SANS HP: {sans_hp}", True, (255,255,255)), (650, 650))

        # MENU
        if state == "menu":
            fight_color = (255,0,0) if selected == 0 else (150,0,0)
            mercy_color = (255,255,0) if selected == 1 else (150,150,0)

            screen.blit(font.render("FIGHT", True, fight_color), (350, 600))
            screen.blit(font.render("MERCY", True, mercy_color), (500, 600))

        pygame.display.flip()

    pygame.quit()

undertale_fight()