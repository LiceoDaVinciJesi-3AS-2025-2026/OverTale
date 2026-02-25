import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("* Sans Battle")
clock = pygame.time.Clock()

font_big   = pygame.font.SysFont("arial", 32, bold=True)
font_med   = pygame.font.SysFont("arial", 24)
font_small = pygame.font.SysFont("arial", 18)

BLACK  = (0, 0, 0)
WHITE  = (255, 255, 255)
RED    = (220, 0, 0)
CYAN   = (0, 255, 255)
YELLOW = (255, 255, 0)
GRAY   = (80, 80, 80)
DKGRAY = (20, 20, 20)
BLUE   = (0, 80, 255)


def UnderTale_Fight():
    # ── Arena ──────────────────────────────────────────────────────────
    arena     = pygame.Rect(150, 200, 600, 300)
    sans_rect = pygame.Rect(WIDTH // 2 - 55, 50, 110, 45)

    # ── Player ────────────────────────────────────────────────────────
    player_img = pygame.image.load("Undertale.png")
    player_img = pygame.transform.scale(player_img, (30, 30))
    player_rect = player_img.get_rect(center=arena.center)

    player_hp_max = 100
    sans_hp_max   = 100

    PHASE_DURATION = 5_000   # ms

    speed      = 5
    gravity    = 0.7
    jump_power = -13

    BONE_INTERVAL  = 380
    LASER_INTERVAL = 1100
    PLAT_INTERVAL  = 1800

    # ── Velocità ossa: ridotte rispetto all'originale ─────────────────
    BONE_SPEED_V  = 7     # fase 1: era 10, ora 6
    BONE_SPEED_V2 = 7     # fase 2 seconda osso: era 13, ora 8
    BONE_SPEED_H  = 7
    LASER_LIFE    = 1000  # ms

    INV_TIME = 800

    # ── Stato interno ────────────────────────────────────────────────
    bones     = []
    lasers    = []
    platforms = []

    state = {
        "player_hp": player_hp_max,
        "sans_hp":   sans_hp_max,
        "phase":     1,
        "phase_timer": 0,
        "y_vel":     0.0,
        "on_ground": False,
        "inv_timer": 0,
        "bone_acc":  0,
        "laser_acc": 0,
        "plat_acc":  0,
        "gravity_active": False,
    }

    # ── Funzioni helper (dentro main) ─────────────────────────────────
    def reset_phase():
        bones.clear()
        lasers.clear()
        platforms.clear()
        player_rect.center = arena.center
        state["y_vel"]     = 0.0
        state["on_ground"] = False
        state["gravity_active"] = False
        if state["phase"] == 3:
            # Spawna subito alcune ossa orizzontali come piattaforme
            for y_offset in [-60, 0, 60]:
                y = arena.centery + y_offset
                dir = random.choice([-1, 1])
                x = arena.left - 75 if dir == 1 else arena.right
                bones.append({"rect": pygame.Rect(x, y, 75, 20),
                              "spd": BONE_SPEED_H, "horiz": True, "dir": dir})
            # Una sotto il giocatore per sicurezza
            bones.append({"rect": pygame.Rect(arena.centerx - 37, arena.centery + 30, 75, 20),
                          "spd": BONE_SPEED_H, "horiz": True, "dir": 1})

    def draw_hp_bar(x, y, w, h, current, maximum, color):
        pygame.draw.rect(screen, GRAY, (x, y, w, h))
        ratio = max(0.0, current / maximum)
        pygame.draw.rect(screen, color, (x, y, int(w * ratio), h))
        pygame.draw.rect(screen, WHITE, (x, y, w, h), 2)

    def draw_sans_hp_bar():
        bx, by, bw, bh = WIDTH - 48, 115, 24, 270
        pygame.draw.rect(screen, GRAY, (bx, by, bw, bh))
        ratio  = max(0.0, state["sans_hp"] / sans_hp_max)
        fill_h = int(bh * ratio)
        pygame.draw.rect(screen, WHITE, (bx, by + bh - fill_h, bw, fill_h))
        pygame.draw.rect(screen, WHITE, (bx, by, bw, bh), 2)
        lbl = font_small.render("SANS", True, WHITE)
        screen.blit(lbl, (bx - 2, by - 22))
        num = font_small.render(str(max(0, state["sans_hp"])), True, WHITE)
        screen.blit(num, (bx + 2, by + bh + 5))

    def draw_ui():
        phase_names = {1: "FASE 1 – OSSA", 2: "FASE 2 – OSSA + LASER", 3: "FASE 3 – SALTA!"}
        lbl = font_med.render(phase_names[state["phase"]], True, CYAN)
        screen.blit(lbl, (WIDTH // 2 - lbl.get_width() // 2, 8))

        remaining = max(0, (PHASE_DURATION - state["phase_timer"]) // 1000)
        tlbl = font_small.render(f"Tempo: {remaining}s", True, YELLOW)
        screen.blit(tlbl, (WIDTH // 2 - tlbl.get_width() // 2, 38))

        screen.blit(font_small.render("HP:", True, WHITE), (30, 160))
        draw_hp_bar(60, 160, 180, 16, state["player_hp"], player_hp_max, RED)
        screen.blit(font_small.render(f"{max(0, state['player_hp'])}/{player_hp_max}", True, WHITE), (248, 158))

        hint = "WASD / frecce per muoverti" if state["phase"] in (1, 2) else "A/D per muoverti  |  SPAZIO per saltare"
        ht = font_small.render(hint, True, GRAY)
        screen.blit(ht, (WIDTH // 2 - ht.get_width() // 2, HEIGHT - 26))

    def check_damage(rect_list, dmg):
        if state["inv_timer"] > 0:
            return
        for r in rect_list:
            if player_rect.colliderect(r):
                state["player_hp"] -= dmg
                state["inv_timer"]  = INV_TIME
                return

    def show_end_screen(title, color):
        screen.fill(BLACK)
        t1 = font_big.render(title, True, color)
        t2 = font_med.render("R = ricomincia    ESC = esci", True, WHITE)
        screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, HEIGHT // 2 - 40))
        screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, HEIGHT // 2 + 20))
        pygame.display.flip()
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
                if ev.type == pygame.KEYDOWN:
                    if ev.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()
                    if ev.key == pygame.K_r:
                        return

    # ── Init ─────────────────────────────────────────────────────────
    reset_phase()

    # ── Game loop ────────────────────────────────────────────────────
    while True:
        dt = clock.tick(60)
        phase = state["phase"]

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()
                if phase == 3 and ev.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    if state["on_ground"]:
                        state["y_vel"]     = jump_power
                        state["on_ground"] = False

        keys = pygame.key.get_pressed()

        # ── Movimento ─────────────────────────────────────────────────
        if phase in (1, 2):
            if keys[pygame.K_LEFT]  or keys[pygame.K_a]: player_rect.x -= speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: player_rect.x += speed
            if keys[pygame.K_UP]    or keys[pygame.K_w]: player_rect.y -= speed
            if keys[pygame.K_DOWN]  or keys[pygame.K_s]: player_rect.y += speed
            player_rect.clamp_ip(arena)
        else:
            moving = keys[pygame.K_LEFT] or keys[pygame.K_a] or keys[pygame.K_RIGHT] or keys[pygame.K_d]
            if moving:
                state["gravity_active"] = True

            if keys[pygame.K_LEFT]  or keys[pygame.K_a]: player_rect.x -= speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: player_rect.x += speed

            if state["gravity_active"]:
                state["y_vel"] += gravity
            else:
                state["y_vel"] = 0.0
            player_rect.y  += int(state["y_vel"])
            player_rect.x   = max(arena.left, min(player_rect.x, arena.right - player_rect.width))

            state["on_ground"] = False
            if player_rect.bottom >= arena.bottom:
                if phase == 3:
                    state["player_hp"] = 0
                else:
                    player_rect.bottom = arena.bottom
                    state["y_vel"]     = 0.0
                    state["on_ground"] = True
            if player_rect.top <= arena.top:
                player_rect.top    = arena.top
                state["y_vel"]     = 0.0

            if state["y_vel"] >= 0:
                for p in platforms:
                    pr = p["rect"]
                    if player_rect.colliderect(pr):
                        prev_bottom = player_rect.bottom - int(state["y_vel"])
                        if prev_bottom <= pr.top + 12:
                            player_rect.bottom = pr.top
                            state["y_vel"]     = 0.0
                            state["on_ground"] = True

                for b in bones:
                    if not b["horiz"]:  # salta le ossa verticali
                        continue
                    br = b["rect"]
                    if player_rect.colliderect(br):
                        prev_bottom = player_rect.bottom - int(state["y_vel"])
                        if prev_bottom <= br.top + 12:
                            player_rect.bottom = br.top
                            state["y_vel"]     = 0.0
                            state["on_ground"] = True

        # ── Timer fase ───────────────────────────────────────────────
        state["phase_timer"] += dt
        if state["phase_timer"] >= PHASE_DURATION:
            state["phase"]       += 1
            state["phase_timer"]  = 0
            state["bone_acc"] = state["laser_acc"] = state["plat_acc"] = 0
            state["sans_hp"] -= 33
            if state["phase"] > 3:
                show_end_screen("* SANS E' STATO SCONFITTO!", CYAN)
                UnderTale_Fight(); return
            reset_phase()
            continue

        state["inv_timer"] = max(0, state["inv_timer"] - dt)
        phase = state["phase"]  # aggiorna dopo eventuale cambio fase

        # ── Spawn ossa ───────────────────────────────────────────────
        state["bone_acc"] += dt
        if state["bone_acc"] >= BONE_INTERVAL:
            state["bone_acc"] = 0
            if phase in (1, 2):
                x = random.randint(arena.left, arena.right - 20)
                bones.append({"rect": pygame.Rect(x, arena.top - 75, 20, 75),
                              "spd": BONE_SPEED_V, "horiz": False, "dir": 1})
                if phase == 2:
                    x2 = random.randint(arena.left, arena.right - 20)
                    # Fase 2: seconda osso leggermente più veloce ma comunque ridotta
                    bones.append({"rect": pygame.Rect(x2, arena.top - 75, 20, 75),
                                  "spd": BONE_SPEED_V2, "horiz": False, "dir": 1})
            else:
                y   = random.randint(arena.top + 10, arena.bottom - 28)
                dir = random.choice([-1, 1])
                x   = arena.left - 75 if dir == 1 else arena.right
                bones.append({"rect": pygame.Rect(x, y, 75, 20),
                              "spd": BONE_SPEED_H, "horiz": True, "dir": dir})

        # ── Spawn laser ──────────────────────────────────────────────
        if phase >= 2:
            state["laser_acc"] += dt
            if state["laser_acc"] >= LASER_INTERVAL:
                state["laser_acc"] = 0
                if phase == 3:
                    x = random.randint(arena.left + 10, arena.right - 14)
                    lasers.append({"rect": pygame.Rect(x, arena.top, 10, arena.height),
                                   "life": LASER_LIFE})
                else:
                    y = random.randint(arena.top + 10, arena.bottom - 14)
                    lasers.append({"rect": pygame.Rect(arena.left, y, arena.width, 10),
                                   "life": LASER_LIFE})

        # ── Spawn piattaforme fase 3 ─────────────────────────────────
        if phase == 3:
            state["plat_acc"] += dt
            if state["plat_acc"] >= PLAT_INTERVAL:
                state["plat_acc"] = 0
                w   = random.randint(90, 170)
                y   = random.randint(arena.top + 50, arena.bottom - 60)
                dir = random.choice([-1, 1])
                x   = arena.left if dir == 1 else arena.right - w
                platforms.append({"rect": pygame.Rect(x, y, w, 14), "spd": 3, "dir": dir})

        # ── Aggiorna ossa ────────────────────────────────────────────
        for b in bones[:]:
            if b["horiz"]:
                b["rect"].x += b["spd"] * b["dir"]
                if b["rect"].left > arena.right + 20 or b["rect"].right < arena.left - 20:
                    bones.remove(b)
            else:
                b["rect"].y += b["spd"]
                if b["rect"].top > arena.bottom + 20:
                    bones.remove(b)

        # ── Aggiorna laser ───────────────────────────────────────────
        for l in lasers[:]:
            l["life"] -= dt
            if l["life"] <= 0:
                lasers.remove(l)

        # ── Aggiorna piattaforme ─────────────────────────────────────
        for p in platforms:
            p["rect"].x += p["spd"] * p["dir"]
            if p["rect"].right > arena.right - 2: p["dir"] = -1
            if p["rect"].left  < arena.left  + 2: p["dir"] =  1

        # ── Danni ────────────────────────────────────────────────────
        if phase != 3:
            check_damage([b["rect"] for b in bones],  dmg=5)
        check_damage([l["rect"] for l in lasers], dmg=10)

        if state["player_hp"] <= 0:
            show_end_screen("* GAME OVER", RED)
            UnderTale_Fight(); return

        # ── Disegno ──────────────────────────────────────────────────
        screen.fill(BLACK)

        pygame.draw.rect(screen, DKGRAY, arena)
        pygame.draw.rect(screen, WHITE,  arena, 3)

        pygame.draw.rect(screen, WHITE, sans_rect)
        slbl = font_small.render("SANS", True, BLACK)
        screen.blit(slbl, (sans_rect.centerx - slbl.get_width() // 2,
                            sans_rect.centery - slbl.get_height() // 2))

        for p in platforms:
            clipped = p["rect"].clip(arena)
            if clipped.width > 0:
                pygame.draw.rect(screen, WHITE, clipped)

        for b in bones:
            clipped = b["rect"].clip(arena)
            if clipped.width > 0 and clipped.height > 0:
                pygame.draw.rect(screen, WHITE, clipped)

        for l in lasers:
            clipped = l["rect"].clip(arena)
            if clipped.width > 0:
                if l["life"] > 700:
                    if (l["life"] // 80) % 2 == 0:
                        pygame.draw.rect(screen, YELLOW, clipped)
                else:
                    pygame.draw.rect(screen, CYAN, clipped)

        show_heart = state["inv_timer"] <= 0 or (state["inv_timer"] // 80) % 2 == 0
        if show_heart:
            if phase == 3:
                blue_img = player_img.copy()
                # Prima azzera il canale rosso
                blue_img.fill((0, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)
                # Poi aggiungi il blu elettrico
                blue_img.fill((0, 100, 255, 0), special_flags=pygame.BLEND_RGBA_ADD)
                screen.blit(blue_img, player_rect)
            else:
                screen.blit(player_img, player_rect)

        draw_sans_hp_bar()
        draw_ui()

        pygame.display.flip()


UnderTale_Fight()