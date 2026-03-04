import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sans Battle")
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
    arena    = pygame.Rect(150, 200, 600, 300)
    sans_img = pygame.image.load("Sans.png")
    sans_img = pygame.transform.scale(sans_img, (120, 120))
    sans = sans_img.get_rect(centerx=WIDTH // 2, top=60)

    # ── Player ────────────────────────────────────────────────────────
    player_img  = pygame.image.load("Cuore.png")
    player_img  = pygame.transform.scale(player_img, (30, 30))
    player_rect = player_img.get_rect(center=arena.center)

    bone_src = pygame.image.load("Sans_osso.png").convert_alpha()

    def draw_bone(rect, clip_area):
        """Disegna l'immagine osso scalata sul rettangolo, rispettando il clipping dell'arena."""
        clipped = rect.clip(clip_area)
        if clipped.width <= 0 or clipped.height <= 0:
            return
        scaled   = pygame.transform.scale(bone_src, (rect.width, rect.height))
        offset_x = clipped.x - rect.x
        offset_y = clipped.y - rect.y
        sub      = scaled.subsurface(pygame.Rect(offset_x, offset_y, clipped.width, clipped.height))
        screen.blit(sub, (clipped.x, clipped.y))

    player_hp_max = 100
    sans_hp_max   = 100

    PHASE_DURATION = 10_000   # ms

    speed      = 5
    gravity    = 0.7
    jump_power = -13

    BONE_INTERVAL  = 380
    LASER_INTERVAL = 1100

    BONE_SPEED_V  = 7
    BONE_SPEED_V2 = 7
    LASER_LIFE    = 1000  # ms

    # ── Fase 3: tunnel di ossa ────────────────────────────────────────
    TUNNEL_INTERVAL = 1400   # ms tra un muro e il successivo
    TUNNEL_SPEED    = 10     # pixel/frame verso sinistra
    TUNNEL_GAP      = 110    # ampiezza del buco (pixel)
    BONE_THICKNESS  = 22     # larghezza di ogni osso del muro

    INV_TIME = 800

    # ── Stato interno ────────────────────────────────────────────────
    bones   = []
    lasers  = []
    tunnels = []

    state = {
        "player_hp":   player_hp_max,
        "sans_hp":     sans_hp_max,
        "phase":       1,
        "phase_timer": 0,
        "inv_timer":   0,
        "bone_acc":    0,
        "laser_acc":   0,
        "tunnel_acc":  0,
    }

    # ── Helper: spawn di un muro tunnel ──────────────────────────────
    def spawn_tunnel():
        """Crea un muro a coppia di ossa verticali con gap casuale, parte da destra."""
        gap_y = random.randint(arena.top + 10, arena.bottom - TUNNEL_GAP - 10)
        x     = arena.right + BONE_THICKNESS + 5
        top_h = gap_y - arena.top
        bot_y = gap_y + TUNNEL_GAP
        bot_h = arena.bottom - bot_y

        wall = {
            "x":   float(x),
            "top": pygame.Rect(x, arena.top, BONE_THICKNESS, top_h),
            "bot": pygame.Rect(x, bot_y,     BONE_THICKNESS, bot_h),
        }
        tunnels.append(wall)

    # ── Funzioni helper ───────────────────────────────────────────────
    def reset_phase():
        bones.clear()
        lasers.clear()
        tunnels.clear()
        player_rect.center = arena.center

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
        screen.blit(lbl, (bx - 9, by - 22))
        num = font_small.render(str(max(0, state["sans_hp"])), True, WHITE)
        screen.blit(num, (bx - 1, by + bh + 5))

    def draw_ui():
        screen.blit(font_small.render("HP:", True, WHITE), (30, 160))
        draw_hp_bar(60, 160, 180, 16, state["player_hp"], player_hp_max, RED)
        screen.blit(font_small.render(f"{max(0, state['player_hp'])}/{player_hp_max}", True, WHITE), (248, 158))

        if state["phase"] == 3:
            hint = "W/S  o  ↑ ↓  per muoverti nel tunnel"
        else:
            hint = "WASD / frecce per muoverti"
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
        dt    = clock.tick(60)
        phase = state["phase"]

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_ESCAPE:
                    pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()

        # ── Movimento ─────────────────────────────────────────────────
        if phase in (1, 2):
            if keys[pygame.K_LEFT]  or keys[pygame.K_a]: player_rect.x -= speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: player_rect.x += speed
            if keys[pygame.K_UP]    or keys[pygame.K_w]: player_rect.y -= speed
            if keys[pygame.K_DOWN]  or keys[pygame.K_s]: player_rect.y += speed
            player_rect.clamp_ip(arena)
        else:
            # Fase 3: solo movimento verticale
            if keys[pygame.K_UP]   or keys[pygame.K_w]: player_rect.y -= speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]: player_rect.y += speed
            player_rect.y      = max(arena.top, min(player_rect.y, arena.bottom - player_rect.height))
            player_rect.centerx = arena.centerx

        # ── Timer fase ───────────────────────────────────────────────
        state["phase_timer"] += dt
        if state["phase_timer"] >= PHASE_DURATION:
            state["phase"]       += 1
            state["phase_timer"]  = 0
            state["bone_acc"] = state["laser_acc"] = state["tunnel_acc"] = 0
            state["sans_hp"] -= 33
            if state["phase"] > 3:
                show_end_screen("SANS E' STATO SCONFITTO!", CYAN)
                UnderTale_Fight(); return
            reset_phase()
            continue

        state["inv_timer"] = max(0, state["inv_timer"] - dt)
        phase = state["phase"]

        # ── Spawn ossa (fase 1 e 2) ───────────────────────────────────
        if phase in (1, 2):
            state["bone_acc"] += dt
            if state["bone_acc"] >= BONE_INTERVAL:
                state["bone_acc"] = 0
                x = random.randint(arena.left, arena.right - 20)
                bones.append({"rect": pygame.Rect(x, arena.top - 75, 20, 75),
                               "spd": BONE_SPEED_V, "horiz": False, "dir": 1})
                if phase == 2:
                    x2 = random.randint(arena.left, arena.right - 20)
                    bones.append({"rect": pygame.Rect(x2, arena.top - 75, 20, 75),
                                  "spd": BONE_SPEED_V2, "horiz": False, "dir": 1})

        # ── Spawn laser (fase 2) ──────────────────────────────────────
        if phase == 2:
            state["laser_acc"] += dt
            if state["laser_acc"] >= LASER_INTERVAL:
                state["laser_acc"] = 0
                y = random.randint(arena.top + 10, arena.bottom - 14)
                lasers.append({"rect": pygame.Rect(arena.left, y, arena.width, 10),
                                "life": LASER_LIFE})

        # ── Spawn muri tunnel (fase 3) ────────────────────────────────
        if phase == 3:
            state["tunnel_acc"] += dt
            if state["tunnel_acc"] >= TUNNEL_INTERVAL:
                state["tunnel_acc"] = 0
                spawn_tunnel()

        # ── Aggiorna ossa ────────────────────────────────────────────
        for b in bones[:]:
            b["rect"].y += b["spd"]
            if b["rect"].top > arena.bottom + 20:
                bones.remove(b)

        # ── Aggiorna laser ───────────────────────────────────────────
        for l in lasers[:]:
            l["life"] -= dt
            if l["life"] <= 0:
                lasers.remove(l)

        # ── Aggiorna muri tunnel ──────────────────────────────────────
        for w in tunnels[:]:
            w["x"] -= TUNNEL_SPEED
            w["top"].x = int(w["x"])
            w["bot"].x = int(w["x"])
            if w["top"].right < arena.left - 10:
                tunnels.remove(w)

        # ── Danni ────────────────────────────────────────────────────
        check_damage([b["rect"] for b in bones],  dmg=10)
        check_damage([l["rect"] for l in lasers], dmg=20)

        if phase == 3:
            tunnel_rects = []
            for w in tunnels:
                tunnel_rects.append(w["top"])
                tunnel_rects.append(w["bot"])
            check_damage(tunnel_rects, dmg=10)

        if state["player_hp"] <= 0:
            show_end_screen("GAME OVER", RED)
            UnderTale_Fight(); return

        # ── Disegno ──────────────────────────────────────────────────
        screen.fill(BLACK)

        pygame.draw.rect(screen, DKGRAY, arena)
        pygame.draw.rect(screen, WHITE,  arena, 3)

        # Disegna Sans (immagine + label)
        screen.blit(sans_img, sans)

        # Disegna ossa
        for b in bones:
            draw_bone(b["rect"], arena)

        # Disegna laser
        for l in lasers:
            clipped = l["rect"].clip(arena)
            if clipped.width > 0:
                if l["life"] > 700:
                    if (l["life"] // 80) % 2 == 0:
                        pygame.draw.rect(screen, YELLOW, clipped)
                else:
                    pygame.draw.rect(screen, CYAN, clipped)

        # Disegna muri tunnel
        for w in tunnels:
            for bone_rect in (w["top"], w["bot"]):
                draw_bone(bone_rect, arena)

        # Disegna cuore
        show_heart = state["inv_timer"] <= 0 or (state["inv_timer"] // 80) % 2 == 0
        if show_heart:
            if phase == 3:
                blue_img = player_img.copy()
                blue_img.fill((0, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)
                blue_img.fill((0, 100, 255, 0), special_flags=pygame.BLEND_RGBA_ADD)
                screen.blit(blue_img, player_rect)
            else:
                screen.blit(player_img, player_rect)

        draw_sans_hp_bar()
        draw_ui()

        pygame.display.flip()


UnderTale_Fight()