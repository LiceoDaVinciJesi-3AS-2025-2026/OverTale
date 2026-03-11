import pygame
import random
import sys

def UnderTale_Fight(screen, clock):
    # --- INIZIALIZZAZIONE RISORSE ---
    pygame.font.init()
    font_big   = pygame.font.SysFont("arial", 32, bold=True)
    font_med   = pygame.font.SysFont("arial", 24)
    font_small = pygame.font.SysFont("arial", 18)

    WIDTH, HEIGHT = 900, 700
    BLACK, WHITE = (0, 0, 0), (255, 255, 255)
    RED, CYAN, YELLOW = (220, 0, 0), (0, 255, 255), (255, 255, 0)
    GRAY, DKGRAY = (80, 80, 80), (20, 20, 20)

    arena = pygame.Rect(150, 200, 600, 300)
    
    try:
        sans_img = pygame.image.load("Sans.png")
        sans_img = pygame.transform.scale(sans_img, (120, 120))
        player_img = pygame.image.load("Cuore.png")
        player_img = pygame.transform.scale(player_img, (30, 30))
        bone_src = pygame.image.load("Sans_osso.png").convert_alpha()
    except:
        sans_img = pygame.Surface((120, 120)); sans_img.fill(WHITE)
        player_img = pygame.Surface((30, 30)); player_img.fill(RED)
        bone_src = pygame.Surface((20, 75)); bone_src.fill(WHITE)

    sans = sans_img.get_rect(centerx=WIDTH // 2, top=60)
    player_rect = player_img.get_rect(center=arena.center)

    # --- VARIABILI DI STATO ---
    player_hp_max, sans_hp_max = 100, 100
    PHASE_DURATION = 10000
    speed, gravity, jump_power = 5, 0.7, -13
    BONE_INTERVAL, LASER_INTERVAL, LASER_LIFE = 380, 1100, 1000
    TUNNEL_INTERVAL, TUNNEL_SPEED, TUNNEL_GAP, BONE_THICKNESS = 1400, 10, 110, 22
    INV_TIME = 800

    bones, lasers, tunnels = [], [], []
    state = {
        "player_hp": player_hp_max, "sans_hp": sans_hp_max, "phase": 1,
        "phase_timer": 0, "inv_timer": 0, "bone_acc": 0, "laser_acc": 0, "tunnel_acc": 0
    }

    # --- FUNZIONI HELPER ---
    def draw_bone(rect, clip_area):
        clipped = rect.clip(clip_area)
        if clipped.width <= 0 or clipped.height <= 0: return
        scaled = pygame.transform.scale(bone_src, (rect.width, rect.height))
        sub = scaled.subsurface(pygame.Rect(clipped.x - rect.x, clipped.y - rect.y, clipped.width, clipped.height))
        screen.blit(sub, (clipped.x, clipped.y))

    def reset_phase():
        bones.clear(); lasers.clear(); tunnels.clear()
        player_rect.center = arena.center

    def spawn_tunnel():
        gap_y = random.randint(arena.top + 10, arena.bottom - TUNNEL_GAP - 10)
        x = arena.right + BONE_THICKNESS + 5
        tunnels.append({
            "x": float(x),
            "top": pygame.Rect(x, arena.top, BONE_THICKNESS, gap_y - arena.top),
            "bot": pygame.Rect(x, gap_y + TUNNEL_GAP, BONE_THICKNESS, arena.bottom - (gap_y + TUNNEL_GAP))
        })

    def draw_hp_bar(x, y, w, h, current, maximum, color):
        pygame.draw.rect(screen, GRAY, (x, y, w, h))
        ratio = max(0.0, current / maximum)
        pygame.draw.rect(screen, color, (x, y, int(w * ratio), h))
        pygame.draw.rect(screen, WHITE, (x, y, w, h), 2)

    def draw_sans_hp_bar():
        bx, by, bw, bh = WIDTH - 48, 115, 24, 270
        pygame.draw.rect(screen, GRAY, (bx, by, bw, bh))
        ratio = max(0.0, state["sans_hp"] / sans_hp_max)
        fill_h = int(bh * ratio)
        pygame.draw.rect(screen, WHITE, (bx, by + bh - fill_h, bw, fill_h))
        pygame.draw.rect(screen, WHITE, (bx, by, bw, bh), 2)
        lbl = font_small.render("SANS", True, WHITE)
        screen.blit(lbl, (bx - 9, by - 22))
        num = font_small.render(str(max(0, state["sans_hp"])), True, WHITE)
        screen.blit(num, (bx - 1, by + bh + 5))

    def draw_ui():
        # Disegna la scritta HP e la barra
        screen.blit(font_small.render("HP:", True, WHITE), (30, 160))
        draw_hp_bar(60, 160, 180, 16, state["player_hp"], player_hp_max, RED)
        screen.blit(font_small.render(f"{max(0, state['player_hp'])}/{player_hp_max}", True, WHITE), (248, 158))
        

        # Calcoliamo i millisecondi rimanenti
        tempo_rimanente_ms = PHASE_DURATION - state["phase_timer"]
        # Convertiamo in secondi (es. 10.5)
        secondi_rimanenti = max(0, tempo_rimanente_ms / 1000)
        
        # Creiamo la scritta del timer
        testo_timer = font_med.render(f"PROSSIMA FASE TRA: {secondi_rimanenti:.1f}s", True, YELLOW)
        # Lo posizioniamo sopra l'arena (al centro)
        screen.blit(testo_timer, (WIDTH // 2 - testo_timer.get_width() // 2, 170))
        # -------------------------------------

        # Suggerimenti di movimento in basso
        hint = "W/S o ↑ ↓ per muoverti" if state["phase"] == 3 else "WASD / frecce per muoverti"
        ht = font_small.render(hint, True, GRAY)
        screen.blit(ht, (WIDTH // 2 - ht.get_width() // 2, HEIGHT - 26))

    def check_damage(rect_list, dmg):
        if state["inv_timer"] > 0: return
        for r in rect_list:
            if player_rect.colliderect(r):
                state["player_hp"] -= dmg
                state["inv_timer"] = INV_TIME
                return

    # --- GAME LOOP ---
    while True:
        dt = clock.tick(60)
        
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE: return "FUGA"

        keys = pygame.key.get_pressed()
        phase = state["phase"]

        # Movimento Cuore
        if phase in (1, 2):
            if keys[pygame.K_LEFT] or keys[pygame.K_a]: player_rect.x -= speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]: player_rect.x += speed
            if keys[pygame.K_UP] or keys[pygame.K_w]: player_rect.y -= speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]: player_rect.y += speed
            player_rect.clamp_ip(arena)
        else:
            if keys[pygame.K_UP] or keys[pygame.K_w]: player_rect.y -= speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]: player_rect.y += speed
            player_rect.y = max(arena.top, min(player_rect.y, arena.bottom - player_rect.height))
            player_rect.centerx = arena.centerx

        # Timer Fasi
        state["phase_timer"] += dt
        if state["phase_timer"] >= PHASE_DURATION:
            state["phase"] += 1; state["phase_timer"] = 0
            state["sans_hp"] -= 33
            if state["phase"] > 3: return "VITTORIA"
            reset_phase(); continue

        state["inv_timer"] = max(0, state["inv_timer"] - dt)

        # Spawn Ostacoli
        if state["phase"] in (1, 2):
            state["bone_acc"] += dt
            if state["bone_acc"] >= BONE_INTERVAL:
                state["bone_acc"] = 0
                x = random.randint(arena.left, arena.right - 20)
                bones.append({"rect": pygame.Rect(x, arena.top - 75, 20, 75), "spd": 7})
            
            if state["phase"] == 2:
                state["laser_acc"] += dt
                if state["laser_acc"] >= LASER_INTERVAL:
                    state["laser_acc"] = 0
                    y = random.randint(arena.top + 10, arena.bottom - 14)
                    lasers.append({"rect": pygame.Rect(arena.left, y, arena.width, 10), "life": LASER_LIFE})

        if state["phase"] == 3:
            state["tunnel_acc"] += dt
            if state["tunnel_acc"] >= TUNNEL_INTERVAL:
                state["tunnel_acc"] = 0; spawn_tunnel()

        # Update posizioni
        for b in bones[:]:
            b["rect"].y += b["spd"]
            if b["rect"].top > arena.bottom: bones.remove(b)
        for l in lasers[:]:
            l["life"] -= dt
            if l["life"] <= 0: lasers.remove(l)
        for w in tunnels[:]:
            w["x"] -= TUNNEL_SPEED
            w["top"].x = w["bot"].x = int(w["x"])
            if w["top"].right < arena.left: tunnels.remove(w)

        # Collisioni
        check_damage([b["rect"] for b in bones], 10)
        check_damage([l["rect"] for l in lasers if l["life"] <= 700], 20)
        if state["phase"] == 3:
            t_rects = []
            for w in tunnels: t_rects.extend([w["top"], w["bot"]])
            check_damage(t_rects, 10)

        if state["player_hp"] <= 0: return "MORTE"

        # Rendering
        screen.fill(BLACK)
        pygame.draw.rect(screen, DKGRAY, arena)
        pygame.draw.rect(screen, WHITE, arena, 3)
        screen.blit(sans_img, sans)
        
        for b in bones: draw_bone(b["rect"], arena)
        for l in lasers:
            clipped = l["rect"].clip(arena)
            if clipped.width > 0:
                color = YELLOW if l["life"] > 700 and (l["life"] // 80) % 2 == 0 else CYAN
                if l["life"] <= 700: pygame.draw.rect(screen, color, clipped)
                else: pygame.draw.rect(screen, color, clipped, 1)

        for w in tunnels:
            draw_bone(w["top"], arena); draw_bone(w["bot"], arena)

        if state["inv_timer"] <= 0 or (state["inv_timer"] // 80) % 2 == 0:
            if state["phase"] == 3:
                blue_img = player_img.copy()
                # Azzera il canale rosso, poi applica il blu
                blue_img.fill((0, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)  # azzera tutto preservando alpha
                blue_img.fill((0, 100, 255, 0), special_flags=pygame.BLEND_RGBA_ADD)  # aggiunge blu elettrico
                screen.blit(blue_img, player_rect)
            else:
                screen.blit(player_img, player_rect)

        draw_sans_hp_bar(); draw_ui()
        pygame.display.flip()