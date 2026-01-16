import os
from typing import Optional, Union
import pygame
from PIL import Image, ImageSequence
from classes import Scene

ASSETS_DIR = "assets"


def asset_path(rel: Optional[str]) -> Optional[str]:
    if not rel:
        return None
    return os.path.join(ASSETS_DIR, rel)


class AnimatedGIF:
    """Petit player d'animation GIF (frames + durées)."""

    def __init__(self, frames: list[pygame.Surface], durations_ms: list[int]):
        self.frames = frames
        self.durations_ms = durations_ms
        self.i = 0
        self.acc = 0.0
        if not self.frames:
            self.frames = [pygame.Surface((1, 1), pygame.SRCALPHA)]
        if not self.durations_ms or len(self.durations_ms) != len(self.frames):
            self.durations_ms = [100] * len(self.frames)

    def update(self, dt_ms: float):
        if len(self.frames) <= 1:
            return
        self.acc += dt_ms
        # Certains GIF ont des durations à 0/10ms -> on clamp pour éviter de "spin"
        cur_dur = max(20, int(self.durations_ms[self.i]))
        while self.acc >= cur_dur:
            self.acc -= cur_dur
            self.i = (self.i + 1) % len(self.frames)
            cur_dur = max(20, int(self.durations_ms[self.i]))

    def get(self) -> pygame.Surface:
        return self.frames[self.i]


def load_gif_animated(path: str) -> AnimatedGIF:
    pil = Image.open(path)
    frames: list[pygame.Surface] = []
    durations: list[int] = []
    for frame in ImageSequence.Iterator(pil):
        fr = frame.convert("RGBA")
        surf = pygame.image.fromstring(fr.tobytes(), fr.size, fr.mode).convert_alpha()
        frames.append(surf)
        durations.append(int(frame.info.get("duration", 100)))
    if not frames:
        fr = pil.convert("RGBA")
        surf = pygame.image.fromstring(fr.tobytes(), fr.size, fr.mode).convert_alpha()
        frames = [surf]
        durations = [100]
    return AnimatedGIF(frames, durations)


def load_image_any(path: str) -> Union[pygame.Surface, AnimatedGIF]:
    """Charge une image. Si .gif => AnimatedGIF, sinon pygame.Surface."""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".gif":
        return load_gif_animated(path)
    return pygame.image.load(path).convert_alpha()


def draw_text_wrapped(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: pygame.Color,
    rect: pygame.Rect,
    line_spacing: int = 6,
):
    words = text.split(" ")
    lines = []
    current = ""
    for w in words:
        test = (current + " " + w).strip()
        if font.size(test)[0] <= rect.width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w
    if current:
        lines.append(current)

    y = rect.y
    for line in lines:
        img = font.render(line, True, color)
        surface.blit(img, (rect.x, y))
        y += img.get_height() + line_spacing
        if y > rect.bottom:
            break


class Typewriter:
    """Gère l'affichage progressif du texte + timing."""

    def __init__(self, chars_per_sec: float = 45.0):
        self.chars_per_sec = chars_per_sec
        self.full_text: str = ""
        self.visible_count: int = 0
        self._acc_ms: float = 0.0
        self.done: bool = True

    def start(self, text: str):
        self.full_text = text or ""
        self.visible_count = 0
        self._acc_ms = 0.0
        self.done = (len(self.full_text) == 0)

    def finish(self):
        self.visible_count = len(self.full_text)
        self.done = True

    def update(self, dt_ms: float) -> list[str]:
        """Retourne la liste des nouveaux caractères révélés."""
        if self.done:
            return []
        self._acc_ms += dt_ms
        ms_per_char = 1000.0 / max(1.0, self.chars_per_sec)
        revealed_chars: list[str] = []
        while self._acc_ms >= ms_per_char and not self.done:
            self._acc_ms -= ms_per_char
            if self.visible_count < len(self.full_text):
                ch = self.full_text[self.visible_count]
                self.visible_count += 1
                revealed_chars.append(ch)
            if self.visible_count >= len(self.full_text):
                self.done = True
        return revealed_chars

    def visible_text(self) -> str:
        return self.full_text[: self.visible_count]


class AceUI:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.w, self.h = screen.get_size()

        self.font_main = pygame.font.SysFont("timesnewroman", 38, bold=False)
        self.font_name = pygame.font.SysFont("timesnewroman", 28, bold=True)
        self.font_date = pygame.font.SysFont("timesnewroman", 35, bold=True)

        # cache d'assets: pygame.Surface ou AnimatedGIF
        self._cache: dict[str, Union[pygame.Surface, AnimatedGIF]] = {}

        self.textbox_h = int(self.h * 0.28)
        self.textbox_rect = pygame.Rect(0, self.h - self.textbox_h, self.w, self.textbox_h)
        self.nameplate_rect = pygame.Rect(40, self.h - self.textbox_h - 34, 240, 44)

        self.c_box = pygame.Color(15, 23, 40)
        self.c_box_border = pygame.Color(200, 200, 220)
        self.c_text = pygame.Color(245, 245, 245)

        self.typewriter = Typewriter(chars_per_sec=45.0)
        self._typing_mode: str = "dialog"  # "dialog" ou "date"
        self._last_text_key: Optional[tuple] = None  # pour détecter changement de scène/texte

        self.blip: Optional[pygame.mixer.Sound] = None
        self.type_sfx: Optional[pygame.mixer.Sound] = None
        self._sfx_toggle = False  # toggle commun (évite spam audio)

        blip_path = asset_path("effects/sfx-blipmale.wav")
        if blip_path and os.path.exists(blip_path):
            try:
                self.blip = pygame.mixer.Sound(blip_path)
                self.blip.set_volume(0.3)
            except Exception as e:
                print(f"[WARN] impossible de charger le blip: {e}")

        type_path = asset_path("effects/sfx-typwriter.wav")
        if type_path and os.path.exists(type_path):
            try:
                self.type_sfx = pygame.mixer.Sound(type_path)
                self.type_sfx.set_volume(0.50)
            except Exception as e:
                print(f"[WARN] impossible de charger le sfx typewriter: {e}")

    def get_img(self, relpath: Optional[str]) -> Optional[Union[pygame.Surface, AnimatedGIF]]:
        p = asset_path(relpath)
        if not p:
            return None
        if p in self._cache:
            return self._cache[p]
        if not os.path.exists(p):
            print(f"[WARN] asset introuvable: {p}")
            return None
        try:
            asset = load_image_any(p)
            self._cache[p] = asset
            return asset
        except Exception as e:
            print(f"[WARN] impossible de charger l'image {p}: {e}")
            return None

    def _resolve_sprite_path(self, sprite_path: str, text_done: bool) -> str:
        """Si sprite '-talking' et texte fini => version sans '-talking'."""
        if not sprite_path:
            return sprite_path
        base, ext = os.path.splitext(sprite_path)
        if text_done and base.endswith("-talking"):
            candidate = base[: -len("-talking")] + ext
            if os.path.exists(asset_path(candidate) or ""):
                return candidate
        return sprite_path

    def start_text_if_needed(self, scene: Scene, key: tuple):
        """Redémarre le typewriter si le texte/scene a changé."""
        if self._last_text_key != key:
            self._last_text_key = key

            if scene.textType == "date":
                # plus lent pour les dates
                self._typing_mode = "date"
                self.typewriter.chars_per_sec = 18.0
                self.typewriter.start(scene.text or "")
            else:
                self._typing_mode = "dialog"
                self.typewriter.chars_per_sec = 45.0
                self.typewriter.start(scene.text or "")

    def update(self, dt_ms: float):
        revealed_chars = self.typewriter.update(dt_ms)

        # SFX frappe (différent date/dialog)
        for ch in revealed_chars:
            if ch.isspace():
                continue
            self._sfx_toggle = not self._sfx_toggle
            if not self._sfx_toggle:
                continue

            if self._typing_mode == "date":
                if self.type_sfx:
                    self.type_sfx.play()
            else:
                if self.blip:
                    self.blip.play()

        # Update animations GIF (tous ceux déjà chargés en cache)
        for asset in self._cache.values():
            if isinstance(asset, AnimatedGIF):
                asset.update(dt_ms)

    def is_text_done(self) -> bool:
        return self.typewriter.done

    def finish_text(self):
        self.typewriter.finish()

    def _render_date_banner(self, full_bg_already_drawn: bool, text: str):
        """Bandeau AA semi-transparent + texte vert centré."""
        # Bandeau bas
        band_h = int(self.h * 0.22)
        band_y = self.h - band_h - 18
        band = pygame.Rect(0, band_y, self.w, band_h)

        # surface semi-transparente
        band_surf = pygame.Surface((band.w, band.h), pygame.SRCALPHA)
        band_surf.fill((18, 34, 58, 190))  # bleu sombre
        self.screen.blit(band_surf, (band.x, band.y))

        pygame.draw.line(self.screen, pygame.Color(200, 200, 220), (0, band.y), (self.w, band.y), 2)
        pygame.draw.line(self.screen, pygame.Color(200, 200, 220), (0, band.bottom - 1), (self.w, band.bottom - 1), 2)

        # texte vert multi-lignes
        visible = text
        lines = visible.split("\n")

        green = pygame.Color(60, 220, 90)
        # calc hauteur totale
        line_heights = [self.font_date.size(l)[1] for l in lines] if lines else [self.font_date.get_height()]
        total_h = sum(line_heights) + max(0, (len(lines) - 1)) * 10
        y = band.y + (band.h - total_h) // 2

        for l in lines:
            img = self.font_date.render(l, True, green)
            x = (self.w - img.get_width()) // 2
            self.screen.blit(img, (x, y))
            y += img.get_height() + 10

        # chevron quand terminé
        if self.is_text_done():
            chevron = self.font_main.render("»", True, pygame.Color(255, 220, 60))
            self.screen.blit(chevron, (self.w - 60, band.bottom - 55))

    def render_scene(self, scene: Scene):
        self.screen.fill((0, 0, 0))

        bg_asset = self.get_img(scene.background)
        bg = bg_asset.get() if isinstance(bg_asset, AnimatedGIF) else bg_asset
        if bg:
            bg_scaled = pygame.transform.smoothscale(bg, (self.w, self.h))
            self.screen.blit(bg_scaled, (0, 0))
        else:
            pygame.draw.rect(self.screen, pygame.Color(0, 0, 0), (0, 0, self.w, self.h))

        # Écran "date"
        if scene.textType == "date":
            txt = self.typewriter.visible_text()
            self._render_date_banner(full_bg_already_drawn=True, text=txt)
            pygame.display.flip()
            return

        # Sprite personnage
        sprite = None
        if scene.character and scene.characterEmotion and scene.character.sprites:
            sprite_path = scene.character.sprites.get(scene.characterEmotion)
            if sprite_path:
                sprite_path = self._resolve_sprite_path(sprite_path, self.is_text_done())
                sprite_asset = self.get_img(sprite_path)
                sprite = sprite_asset.get() if isinstance(sprite_asset, AnimatedGIF) else sprite_asset

        if sprite and (scene.background == "backgrounds/waiting-room.jpg" or scene.background == "backgrounds/defense-assistant-side.jpg" or not scene.background):
            max_h = self.h - self.textbox_h + 30
            scale = min(1.0, max_h / sprite.get_height())
            new_size = (int(sprite.get_width() * scale), int(sprite.get_height() * scale))
            sp = pygame.transform.smoothscale(sprite, new_size)
            x = (self.w - sp.get_width()) // 2
            y = (self.h - self.textbox_h) - sp.get_height() + 40
            self.screen.blit(sp, (x, y))

        if sprite and scene.background == "backgrounds/judge-side.jpg":
            max_h = self.h - self.textbox_h + 30
            scale = min(1.0, max_h / sprite.get_height()) * 1.2
            new_size = (int(sprite.get_width() * scale), int(sprite.get_height() * scale))
            sp = pygame.transform.smoothscale(sprite, new_size)
            x = (self.w - sp.get_width()) // 2
            y = (self.h - self.textbox_h) - sp.get_height() + 180
            self.screen.blit(sp, (x, y))
        
        if sprite and scene.background == "backgrounds/defense-side.jpg":
            max_h = self.h - self.textbox_h + 30
            scale = min(1.0, max_h / sprite.get_height()) * 1.1
            new_size = (int(sprite.get_width() * scale), int(sprite.get_height() * scale))
            sp = pygame.transform.smoothscale(sprite, new_size)
            x = (self.w - sp.get_width()) // 2 - 30
            y = (self.h - self.textbox_h) - sp.get_height() + 100
            self.screen.blit(sp, (x, y))
          
        if sprite and scene.background == "backgrounds/prosecutor-side.jpg":
            max_h = self.h - self.textbox_h + 30
            scale = min(1.0, max_h / sprite.get_height()) * 1.1
            new_size = (int(sprite.get_width() * scale), int(sprite.get_height() * scale))
            sp = pygame.transform.smoothscale(sprite, new_size)
            x = (self.w - sp.get_width()) // 2 - 40
            y = (self.h - self.textbox_h) - sp.get_height() + 120
            self.screen.blit(sp, (x, y))

        if sprite and scene.background == "backgrounds/witness-side.jpg":
            max_h = self.h - self.textbox_h + 30
            scale = min(1.0, max_h / sprite.get_height())
            new_size = (int(sprite.get_width() * scale), int(sprite.get_height() * scale))
            sp = pygame.transform.smoothscale(sprite, new_size)
            x = (self.w - sp.get_width()) // 2
            y = (self.h - self.textbox_h) - sp.get_height() + 100
            self.screen.blit(sp, (x, y))

        # Textbox
        pygame.draw.rect(self.screen, self.c_box, self.textbox_rect)
        pygame.draw.rect(self.screen, self.c_box_border, self.textbox_rect, 3)

        show_name = scene.characterText
        if show_name:
            pygame.draw.rect(self.screen, pygame.Color(30, 120, 180), self.nameplate_rect)
            pygame.draw.rect(self.screen, self.c_box_border, self.nameplate_rect, 2)
            name_img = self.font_name.render(show_name, True, pygame.Color(255, 255, 255))
            self.screen.blit(name_img, (self.nameplate_rect.x + 12, self.nameplate_rect.y + 8))

        # Texte (progressif)
        txt = self.typewriter.visible_text()
        self.c_text = pygame.Color(255, 255, 255)
        if scene.textType == "thought":
            self.c_text = pygame.Color(80, 160, 255)
        elif scene.textType == "testimony":
            self.c_text = pygame.Color(60, 200, 120)

        text_rect = pygame.Rect(140, self.textbox_rect.y + 35, self.w - 280, self.textbox_rect.height - 50)
        draw_text_wrapped(self.screen, txt, self.font_main, self.c_text, text_rect)

        # Chevron seulement quand le texte est fini (sinon ça spoil)
        if self.is_text_done():
            chevron = self.font_main.render("»", True, pygame.Color(255, 220, 60))
            self.screen.blit(chevron, (self.w - 60, self.h - 55))

        pygame.display.flip()


    def _draw_dotted_lines(self, rect: pygame.Rect, lines: int = 3):
      y = rect.y + 60
      for _ in range(lines):
          pygame.draw.line(self.screen, pygame.Color(160, 160, 160), (rect.x, y), (rect.right, y), 1)
          # pointillés
          for x in range(rect.x, rect.right, 10):
              pygame.draw.line(self.screen, pygame.Color(160, 160, 160), (x, y), (x + 5, y), 1)
          y += 52

    def _blit_scaled_center(self, img: pygame.Surface, box: pygame.Rect, pad: int = 10):
      avail = pygame.Rect(box.x + pad, box.y + pad, box.w - 2 * pad, box.h - 2 * pad)
      if avail.w <= 0 or avail.h <= 0:
          return
      scale = min(avail.w / img.get_width(), avail.h / img.get_height())
      w = max(1, int(img.get_width() * scale))
      h = max(1, int(img.get_height() * scale))
      s = pygame.transform.smoothscale(img, (w, h))
      x = avail.x + (avail.w - w) // 2
      y = avail.y + (avail.h - h) // 2
      self.screen.blit(s, (x, y))

    def render_court_record(self, courtRecord, state: str, ev_i: int, pr_i: int):
        """
        state: 'evidence' ou 'profil'
        ev_i: index evidence selectionné
        pr_i: index profil selectionné
        """
        # fond légèrement assombri
        overlay = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.screen.blit(overlay, (0, 0))

        # grand panneau
        panel = pygame.Rect(80, 90, self.w - 160, self.h - 220)
        pygame.draw.rect(self.screen, pygame.Color(215, 235, 250), panel, border_radius=6)
        pygame.draw.rect(self.screen, pygame.Color(30, 90, 150), panel, 6, border_radius=6)

        # bandeau "Preuves / Profils"
        header = pygame.Rect(panel.x, panel.y, 220, 50)
        pygame.draw.rect(self.screen, pygame.Color(40, 140, 200), header)
        title = "Preuves" if state == "evidence" else "Profils"
        timg = self.font_name.render(title, True, pygame.Color(255, 255, 255))
        self.screen.blit(timg, (header.x + 16, header.y + 10))

        # zone contenu
        content = pygame.Rect(panel.x + 24, panel.y + 70, panel.w - 48, panel.h - 160)
        pygame.draw.rect(self.screen, pygame.Color(250, 250, 250), content, border_radius=4)

        # zone image à gauche
        img_box = pygame.Rect(content.x + 24, content.y + 24, 230, 230)
        pygame.draw.rect(self.screen, pygame.Color(210, 210, 210), img_box)
        pygame.draw.rect(self.screen, pygame.Color(180, 180, 180), img_box, 2)

        # barre jaune + nom
        name_bar = pygame.Rect(img_box.right + 24, content.y + 24, content.w - (img_box.w + 72), 52)
        pygame.draw.rect(self.screen, pygame.Color(240, 190, 40), name_bar)

        # description (avec lignes pointillées)
        desc_rect = pygame.Rect(name_bar.x, name_bar.bottom + 10, name_bar.w, content.h - 110)
        self._draw_dotted_lines(desc_rect, lines=4)

        if state == "evidence":
            items = courtRecord.evidences
            if items:
                ev_i = max(0, min(ev_i, len(items) - 1))
                ev = items[ev_i]

                # image
                asset = self.get_img(ev.image)
                surf = asset.get() if isinstance(asset, AnimatedGIF) else asset
                if surf:
                    self._blit_scaled_center(surf, img_box, pad=18)

                # nom
                nimg = self.font_main.render(ev.name, True, pygame.Color(0, 0, 0))
                self.screen.blit(nimg, (name_bar.x + 12, name_bar.y + 8))

                # texte
                draw_text_wrapped(
                    self.screen,
                    ev.description,
                    self.font_main,
                    pygame.Color(0, 0, 0),
                    pygame.Rect(desc_rect.x, desc_rect.y + 12, desc_rect.w, desc_rect.h - 12),
                    line_spacing=14,
                )
            else:
                nimg = self.font_main.render("Aucune preuve.", True, pygame.Color(0, 0, 0))
                self.screen.blit(nimg, (name_bar.x + 12, name_bar.y + 8))

        else:
            items = courtRecord.profils
            if items:
                pr_i = max(0, min(pr_i, len(items) - 1))
                ch = items[pr_i]

                # photo
                asset = self.get_img(getattr(ch, "photo", None))
                surf = asset.get() if isinstance(asset, AnimatedGIF) else asset
                if surf:
                    self._blit_scaled_center(surf, img_box, pad=18)

                # nom + âge
                age = getattr(ch, "age", None)
                label = f"{ch.name}" + (f" ({age} ans)" if age is not None else "")
                nimg = self.font_main.render(label, True, pygame.Color(0, 0, 0))
                self.screen.blit(nimg, (name_bar.x + 12, name_bar.y + 8))

                # desc
                draw_text_wrapped(
                    self.screen,
                    getattr(ch, "description", "") or "",
                    self.font_main,
                    pygame.Color(0, 0, 0),
                    pygame.Rect(desc_rect.x, desc_rect.y + 12, desc_rect.w, desc_rect.h - 12),
                    line_spacing=14,
                )
            else:
                nimg = self.font_main.render("Aucun profil.", True, pygame.Color(0, 0, 0))
                self.screen.blit(nimg, (name_bar.x + 12, name_bar.y + 8))

        # Barre de vignettes en bas
        strip = pygame.Rect(panel.x + 24, panel.bottom - 86, panel.w - 48, 62)
        pygame.draw.rect(self.screen, pygame.Color(40, 140, 200), strip, border_radius=4)

        thumb_size = 56
        gap = 10
        x = strip.x + 10
        y = strip.y + (strip.h - thumb_size) // 2

        if state == "evidence":
            items = courtRecord.evidences
            sel = ev_i
            get_thumb_path = lambda it: it.image
        else:
            items = courtRecord.profils
            sel = pr_i
            get_thumb_path = lambda it: getattr(it, "photo", None)

        for idx, it in enumerate(items[:12]):  # limite simple
            box = pygame.Rect(x, y, thumb_size, thumb_size)
            pygame.draw.rect(self.screen, pygame.Color(20, 90, 140), box, border_radius=4)
            pygame.draw.rect(self.screen, pygame.Color(10, 40, 70), box, 2, border_radius=4)

            path = get_thumb_path(it)
            asset = self.get_img(path)
            surf = asset.get() if isinstance(asset, AnimatedGIF) else asset
            if surf:
                self._blit_scaled_center(surf, box, pad=6)

            if idx == sel:
                pygame.draw.rect(self.screen, pygame.Color(255, 220, 60), box, 4, border_radius=4)

            x += thumb_size + gap
            if x + thumb_size > strip.right:
                break

        # hints touches
        hint = self.font_name.render("TAB Retour   R Preuves/Profils   Q/D Sélection", True, pygame.Color(255, 255, 255))
        self.screen.blit(hint, (panel.x + panel.w - hint.get_width() - 18, panel.bottom - 28))

        pygame.display.flip()
