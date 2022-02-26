import pygame, andechserBerg, os

pygame.init()


class Wanderung:

  N_MIN_OBJEKTE = 7

  def __init__(self):
    super().__init__()
    self.toene = andechserBerg.Toene()

    self.fenster = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    self.F_BREITE, self.F_HOEHE = pygame.display.get_surface().get_size()

    self.sprites = pygame.sprite.LayeredUpdates()
    self.strasse = andechserBerg.Strasse(self.sprites, self.F_BREITE, self.F_HOEHE)
    self.strasse.rect.y = -self.strasse.rect.height+self.F_HOEHE
    self.sprites.add(self.strasse)
    self.wanderer = andechserBerg.Wanderer(self.toene, self.F_BREITE, self.F_HOEHE)
    self.sprites.add(self.wanderer)
    self.uhr = pygame.time.Clock()

    self.t_kollision_top = -100
    self.t_kollision_flop= -100

  def wandere(self):
    i = 0

    while True:
      i+=1
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
          os._exit(0)

      
      n_neue_objekte = int (self.N_MIN_OBJEKTE - len(self.sprites) + i / 100)
      
      for j in range(n_neue_objekte):
        try:
          self.sprites.add(andechserBerg.ZufallsObjekt(self.F_BREITE, self.F_HOEHE, self.sprites))
        except:
          pass
          

      for sprite in self.sprites:
        if type(sprite) is andechserBerg.ZufallsObjekt and pygame.sprite.collide_rect(self.wanderer, sprite):
          if sprite.gut:
            self.wanderer.punkte +=1
            self.toene.fressen.play()
            if (self.wanderer.promille > 0):
              self.wanderer.promille -= 1
            self.t_kollision_top = pygame.time.get_ticks()
          else:
            self.wanderer.promille += 1
            self.toene.saufen.play()
            self.t_kollision_flop = pygame.time.get_ticks()
            if self.wanderer.promille > 15:
              self.fenster.fill((255,255,255))
              self.toene.kotzen.play()
              andechserBerg.Helfer.text("Magen auspumpen erforderlich", self.fenster, (self.F_BREITE / 2, self.F_HOEHE / 2), 50)
              andechserBerg.Helfer.text(str(self.wanderer.punkte) + " Menüs verzehrt", self.fenster, (self.F_BREITE / 2, self.F_HOEHE / 2 + 60), 30)
              pygame.display.flip()
              pygame.time.wait(3000)
              pygame.quit()
              os._exit(0)
          sprite.kill()

      if pygame.time.get_ticks() - self.t_kollision_flop < 100:
        self.fenster.fill((255, 0, 0))
      elif pygame.time.get_ticks() - self.t_kollision_top < 100:
        self.fenster.fill((0, 255, 0))
      else:
        self.fenster.fill((255, 255, 255))
            
      self.sprites.update()
      self.sprites.draw(self.fenster)

      andechserBerg.Helfer.text("Menüs verzehrt: " + str(self.wanderer.punkte), self.fenster, (self.F_BREITE - 150, self.F_HOEHE - 50), 30)
      andechserBerg.Helfer.text("Promille: {0:.1f}".format(self.wanderer.promille*0.1), self.fenster, (90, self.F_HOEHE - 50), 30)

      pygame.display.flip()
      self.uhr.tick(50)
      
w = Wanderung()
w.wandere()