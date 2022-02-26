from multiprocessing.dummy import Event
import pygame, andechserBerg, os

pygame.init()
GESTORBEN = pygame.USEREVENT+1
STARTE_WANDERUNG = pygame.USEREVENT+2

class Lobby:
  def __init__(self, fenster:pygame.Surface, toene) -> None:
      pass

  def anzeigen(self) -> pygame.event.Event: pass

class Wanderung:

  N_MIN_OBJEKTE = 7
  MAX_PROMILLE = 15

  def __init__(self, fenster:pygame.Surface, toene):
    super().__init__()
    self.fenster = fenster
    self.toene = toene

    self.sprites = pygame.sprite.LayeredUpdates()
    self.strasse = andechserBerg.Strasse(self.sprites, self.fenster.get_size())
    self.strasse.rect.y = -self.strasse.rect.height+self.fenster.get_height()
    self.sprites.add(self.strasse)
    self.wanderer = andechserBerg.Wanderer(self.toene, self.fenster.get_size())
    self.sprites.add(self.wanderer)
    self.uhr = pygame.time.Clock()

    self.t_kollision_top = -100
    self.t_kollision_flop= -100

  def wandere(self) -> pygame.event.Event:
    i = 0

    while True:
      i+=1
      for event in pygame.event.get():
        if (False
          or event.type == GESTORBEN
          or event.type == pygame.QUIT):
          print ("ende")
          return event

      
      n_neue_objekte = int (self.N_MIN_OBJEKTE - len(self.sprites) + i / 100)
      
      for j in range(n_neue_objekte):
        try:
          self.sprites.add(andechserBerg.ZufallsObjekt(self.fenster.get_size(), self.sprites))
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
            if self.wanderer.promille > self.MAX_PROMILLE:
              self.sterbe()
          sprite.kill()

      if pygame.time.get_ticks() - self.t_kollision_flop < 100:
        self.fenster.fill((255, 0, 0))
      elif pygame.time.get_ticks() - self.t_kollision_top < 100:
        self.fenster.fill((0, 255, 0))
      else:
        self.fenster.fill((255, 255, 255))
            
      self.sprites.update()
      self.sprites.draw(self.fenster)

      andechserBerg.Helfer.text("Menüs verzehrt: " + str(self.wanderer.punkte), self.fenster, (self.fenster.get_width() - 150, self.fenster.get_height() - 50), 30)
      andechserBerg.Helfer.text("Promille: {0:.1f}".format(self.wanderer.promille*0.1), self.fenster, (90, self.fenster.get_height() - 50), 30)

      pygame.display.flip()
      self.uhr.tick(50)

  def sterbe(self):
    self.fenster.fill((255,255,255))
    self.toene.kotzen.play()
    andechserBerg.Helfer.text("Magen auspumpen erforderlich", self.fenster, (self.fenster.get_width() / 2, self.fenster.get_height() / 2), 50)
    andechserBerg.Helfer.text(str(self.wanderer.punkte) + " Menüs verzehrt", self.fenster, (self.fenster.get_width() / 2, self.fenster.get_height() / 2 + 60), 30)
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.event.post(pygame.event.Event(GESTORBEN))

class Game:
  def __init__(self) -> None:
    self.toene = andechserBerg.Toene()

    self.fenster = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    self.Lobby = Lobby(self.fenster, self.toene)



  def spiele(self): 
    while True:
#      lobbyEvent = self.Lobby.anzeigen()

#      if (lobbyEvent.type == STARTE_WANDERUNG):
        self.Wanderung = Wanderung(self.fenster, self.toene)
        wanderungsEvent = self.Wanderung.wandere()
        if (wanderungsEvent.type == pygame.QUIT):
          pygame.quit()
          os._exit(0)
#      else:
 #       pygame.quit()
  #      os._exit(0)
      


w = Game()
w.spiele()