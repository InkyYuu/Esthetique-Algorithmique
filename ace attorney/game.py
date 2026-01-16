from dataclasses import dataclass
from typing import Optional, Literal

import pygame

from classes import Node, CourtRecord
from ui import asset_path, AceUI


class MusicManager:
    def __init__(self, volume: float = 0.6):
        self.current: Optional[str] = None
        self.volume = volume

    def play(self, relpath: Optional[str], loop: bool = True, fade_ms: int = 600):
        if not relpath:
            return
        p = asset_path(relpath)
        if not p:
            return

        import os
        if not os.path.exists(p):
            print(f"[WARN] musique introuvable: {p}")
            return

        if self.current == p:
            return

        try:
            pygame.mixer.music.fadeout(fade_ms)
        except Exception:
            pass

        pygame.mixer.music.load(p)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1 if loop else 0, fade_ms=fade_ms)
        self.current = p

    def stop(self, fade_ms: int = 600):
        pygame.mixer.music.fadeout(fade_ms)
        self.current = None

    def set_volume(self, volume: float):
        self.volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.volume)


class Game:
    nodes: dict[str, Node]
    currentNodeId: str
    lifes: int
    courtRecord: CourtRecord
    courtRecordOpen: bool = False
    courtRecordState: Literal["evidence", "profil"] = "evidence"
    selectedEvidenceIndex: int = 0
    selectedProfilIndex: int = 0
    selectedChoiceIndex: int = 0

    def __init__(self, nodes: dict[str, Node], starting_node_id: str, courtRecord: CourtRecord, lifes: int = 5):
        self.nodes = nodes
        self.currentNodeId = starting_node_id
        self.lifes = lifes
        self.courtRecord = courtRecord
        self._last_node_id: Optional[str] = None

    def get_current_node(self) -> Node:
        return self.nodes[self.currentNodeId]
    
    def check_choice(self):
        node = self.get_current_node()
        if node.type == "choice" and node.options:
            selected_option = node.options[self.selectedChoiceIndex]
            if selected_option.nextId and selected_option.nextId in self.nodes:
                self.currentNodeId = selected_option.nextId

    def go_next(self):
        node = self.get_current_node()
        if node.nextId and node.nextId in self.nodes:
            self.currentNodeId = node.nextId

    def run(self):
        pygame.init()
        pygame.mixer.init()
        music = MusicManager(volume=0.6)

        screen = pygame.display.set_mode((1024, 768))
        pygame.display.set_caption("Ace Attorney - Prototype")
        clock = pygame.time.Clock()

        ui = AceUI(screen)

        running = True
        while running and self.lifes > 0:
            dt_ms = clock.tick(60)
            node = self.get_current_node()

            # Si music = "None" on réduit le volume progressivement jusqu'à 0
            if node.scene.music == "None":
                music.set_volume(music.volume - 0.01)
                if music.volume <= 0.01:
                    music.stop()
                    music.set_volume(0.7)

            if node.scene.music and node.scene.music != "None":
                music.play(node.scene.music)

            # Si on change de node, on relance le typewriter
            if self._last_node_id != self.currentNodeId:
                self._last_node_id = self.currentNodeId
                key = (self.currentNodeId, node.scene.textType, node.scene.text)
                ui.start_text_if_needed(node.scene, key)

            for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  running = False

              if event.type == pygame.KEYDOWN:
                  if event.key == pygame.K_ESCAPE:
                      running = False

                  # TAB : ouvrir / fermer le dossier
                  if event.key == pygame.K_TAB:
                      self.courtRecordOpen = not self.courtRecordOpen
                      if self.courtRecordOpen:
                          # Toujours ouvrir sur "preuves"
                          self.courtRecordState = "evidence"
                          self.selectedEvidenceIndex = 0
                          self.selectedProfilIndex = 0
                      continue

                  if event.key == pygame.K_z and node.type == "choice" and node.options and self.courtRecordOpen == False:
                    n = len(node.options) if node.options else 0
                    if n > 0 and self.selectedChoiceIndex > 0 and not self.courtRecordOpen:
                        self.selectedChoiceIndex = self.selectedChoiceIndex - 1
                        continue

                  if event.key == pygame.K_s and node.type == "choice" and node.options and self.courtRecordOpen == False:
                    n = len(node.options) if node.options else 0
                    if n > 0 and self.selectedChoiceIndex < n - 1 and not self.courtRecordOpen:
                        self.selectedChoiceIndex = self.selectedChoiceIndex + 1
                        continue
                    
                  if event.key == pygame.K_RETURN and node.type == "choice" and node.options and self.courtRecordOpen == False:
                      self.check_choice()
                      continue

                  # Si le dossier est ouvert : on gère uniquement la navigation dossier
                  if self.courtRecordOpen:
                      if event.key == pygame.K_r:
                          self.courtRecordState = "profil" if self.courtRecordState == "evidence" else "evidence"

                      elif event.key == pygame.K_q:
                          if self.courtRecordState == "evidence":
                              n = len(self.courtRecord.evidences)
                              if n > 0:
                                  self.selectedEvidenceIndex = (self.selectedEvidenceIndex - 1) % n
                          elif node.type != "choice":
                              n = len(self.courtRecord.profils)
                              if n > 0:
                                  self.selectedProfilIndex = (self.selectedProfilIndex - 1) % n

                      elif event.key == pygame.K_d:
                          if self.courtRecordState == "evidence":
                              n = len(self.courtRecord.evidences)
                              if n > 0:
                                  self.selectedEvidenceIndex = (self.selectedEvidenceIndex + 1) % n
                          elif node.type != "choice":
                              n = len(self.courtRecord.profils)
                              if n > 0:
                                  self.selectedProfilIndex = (self.selectedProfilIndex + 1) % n

                      # Quand le dossier est ouvert, on ne laisse pas SPACE/D avancer le dialogue
                      continue

                  # Contrôles normaux (dossier fermé)
                  if event.key in (pygame.K_SPACE, pygame.K_d):
                      if node.scene.textType != "date" and not ui.is_text_done():
                          ui.finish_text()
                      else:
                          self.go_next()

            # Révèle du texte (et joue le son)
            ui.update(dt_ms)

            # Dessine
            ui.render_scene(node.scene)

            if node.type == "choice" and node.options and ui.is_text_done():
              ui.render_choice_menu(node.options, self.selectedChoiceIndex)

            if self.courtRecordOpen:
              ui.render_court_record(
                  self.courtRecord,
                  self.courtRecordState,
                  self.selectedEvidenceIndex,
                  self.selectedProfilIndex
              )

            pygame.display.flip()

        pygame.quit()
