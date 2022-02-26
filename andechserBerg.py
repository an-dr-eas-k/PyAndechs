from typing import Sequence
import pygame
import random
import math
import threading
from pygame import mixer

class Toene:

  def __init__(self) -> None:

    mixer.init()
    mixer.music.set_volume(0.7)
    self.fressen = pygame.mixer.Sound("media/fressen2.ogg")
    self.saufen = pygame.mixer.Sound("media/saufen1.ogg")
    self.kotzen = pygame.mixer.Sound("media/kotzen1.ogg")
    self.ultiAktiviert = pygame.mixer.Sound("media/ulti1.ogg")
    self.looser = pygame.mixer.Sound("media/looser1.ogg")
    self.winner = pygame.mixer.Sound("media/alter1.ogg")
    self.mega = pygame.mixer.Sound("media/megageil1.ogg")


class Helfer:
  def text(text, fenster, position, groesse):
    font = pygame.font.SysFont('arial', groesse)
    text = font.render(text, False, (0, 0, 0))
    F_BREITE = text.get_rect().width
    fenster.blit(text, (position[0] - (F_BREITE / 2), position[1]))


  def aspect_scale(img, rect):
    """ Scales 'img' to fit into box bx/by.
    This method will retain the original image's aspect ratio """
    bx, by = rect
    ix, iy = img.get_size()
    if ix > iy:
      # fit to width
      scale_factor = bx/float(ix)
      sy = scale_factor * iy
      if sy > by:
        scale_factor = by/float(iy)
        sx = scale_factor * ix
        sy = by
      else:
        sx = bx
    else:
      # fit to height
      scale_factor = by/float(iy)
      sx = scale_factor * ix
      if sx > bx:
        scale_factor = bx/float(ix)
        sx = bx
        sy = scale_factor * iy
      else:
        sy = by

    return pygame.transform.scale(img, (math.floor(sx), math.floor(sy)))


class Wanderer(pygame.sprite.Sprite):

  def __init__(self, toene, F_BREITE, F_HOEHE):
    super().__init__()
    self.toene = toene
    self._layer = 10

    self.F_BREITE = F_BREITE
    self.F_HOEHE = F_HOEHE

    self.image = Helfer.aspect_scale(pygame.image.load(
      "media/mann-von-oben1.png"), (100, 100))

    self.rect = self.image.get_rect()
    self.punkte = 0
    self.promille = 0
    self.swap = True
    self.groessenFaktor = 1.0
    self.groessenAenderungErlaubt = True
    self.drawMann()
    self.rect.center = (self.F_BREITE / 2, self.F_HOEHE / 2)




  def drawMann(self):
    ausdehnung = (100, 100)
    ausdehnung = (
      int (ausdehnung[0]*self.groessenFaktor), 
      int (ausdehnung[1]*self.groessenFaktor))

    if (self.swap):
      self.image = Helfer.aspect_scale(pygame.image.load(
        "media/mann-von-oben1.png"), ausdehnung)
      self.swap = False
    else:
      self.image = Helfer.aspect_scale(pygame.image.load(
        "media/mann-von-oben2.png"), ausdehnung)
      self.swap = True

    self.rect.width = self.image.get_rect().width
    self.rect.height = self.image.get_rect().height
    threading.Timer(0.3, self.drawMann).start()



  def update(self):
    gedrueckt = pygame.key.get_pressed()
    seed = math.floor(math.sqrt(self.promille * 20))
    if gedrueckt[pygame.K_UP]:
      self.rect.x += random.randint(seed * -1, seed)
      self.rect.y -= 8 + random.randint(seed * -1, seed)
    if gedrueckt[pygame.K_DOWN]:
      self.rect.x += random.randint(seed * -1, seed)
      self.rect.y += 8+ random.randint(seed * -1, seed)
    if gedrueckt[pygame.K_LEFT]:
      self.rect.x -= 8 + random.randint(seed * -1, seed)
      self.rect.y += random.randint(seed * -1, seed)
    if gedrueckt[pygame.K_RIGHT]:
      self.rect.x += 8 + random.randint(seed * -1, seed)
      self.rect.y += random.randint(seed * -1, seed)
    if gedrueckt[pygame.K_SPACE]:
      if (self.groessenAenderungErlaubt):
        self.groessenFaktor = random.random()* 0.7 + 0.3
        self.reagiereAufGroessenFaktor()
        threading.Timer(10, self.ruecksetzenGroessenFaktor).start()
        self.groessenAenderungErlaubt = False
        threading.Timer(30, self.groessenAenderungWiederErlaubt).start()
        print("eine groessenaenderung wird gemacht mit faktor "+str(self.groessenFaktor ))
    self.rect.clamp_ip(pygame.Rect(0, 0, self.F_BREITE, self.F_HOEHE))

  def reagiereAufGroessenFaktor(self):
    if (self.groessenFaktor > 0.7):
      self.toene.looser.play()
      return
    if (self.groessenFaktor > 0.4):
      self.toene.winner.play()
      return
    self.toene.mega.play()
        

  def ruecksetzenGroessenFaktor(self):
    self.groessenFaktor = 1.0
  
  def groessenAenderungWiederErlaubt(self):
    self.toene.ultiAktiviert.play()
    self.groessenAenderungErlaubt = True
    print("jetzt ist groessenaenderung wieder erlaubt")

class ZufallsObjekt(pygame.sprite.Sprite):

  bilder_top = [Helfer.aspect_scale(pygame.image.load("media/hendl.png"), (100, 100)),
              Helfer.aspect_scale(pygame.image.load("media/hendlhaxl.png"), (100, 100))]

  bilder_flop = [Helfer.aspect_scale(pygame.image.load("media/bierflasche-edit1.png"), (100, 100)),
                  Helfer.aspect_scale(pygame.image.load("media/cocktail-edit1.png"), (100, 100))]

  n = 0

  def __init__(self, F_BREITE, F_HOEHE, sprites):
    super().__init__()
    ZufallsObjekt.n+=1
    self._layer = 5
    self.id = ZufallsObjekt.n
    self.F_BREITE = F_BREITE
    self.F_HOEHE = F_HOEHE

    self.gut = random.choices(population=[True, False], weights=[0.1,0.9])[0]

    if self.gut:
      self.image = random.choice(ZufallsObjekt.bilder_top)
    else:
      self.image = random.choice(ZufallsObjekt.bilder_flop)


    self.rect = self.image.get_rect()
    moeglichkeiten = list(range(math.floor(
      20+self.rect.width / 2), math.floor(self.F_BREITE-20-self.rect.width / 2)))
    y_pos = random.randint(-self.F_HOEHE, -self.rect.height)

    for sprite in sprites:
      if not isinstance(sprite, ZufallsObjekt):
        continue
      if not abs(sprite.rect.center[1] - y_pos) < sprite.rect.height:
        continue
        
      linkesEnde = sprite.rect.center[0] - (sprite.rect.width+self.rect.width) // 2
      rechtesEnde = sprite.rect.center[0] + (sprite.rect.width+self.rect.width) // 2
      moeglichkeiten=list(filter(lambda x:not(linkesEnde<=x<=rechtesEnde), moeglichkeiten))

    self.rect.center = (random.choice(moeglichkeiten), y_pos)

    self.x_speed = 0
    self.y_speed = 3
    

  def update(self):
    if self.rect.top > self.F_HOEHE:
      self.kill()
    else:
      self.rect.x += self.x_speed
      self.rect.y += self.y_speed

class Strasse(pygame.sprite.Sprite):

  def __init__(self, sprites, F_BREITE, F_HOEHE):
    super().__init__()
    self.sprites: Sequence = sprites
    self.F_BREITE = F_BREITE
    self.F_HOEHE = F_HOEHE
    self._layer = 0

    self.image = Helfer.aspect_scale(pygame.image.load(
        "media/weg.png"), (self.F_BREITE, self.F_HOEHE*5))

    self.rect = self.image.get_rect()
    self.rect.center = (self.F_BREITE / 2, -self.F_HOEHE)
    self.rect.y = -self.rect.height
    self.x_speed = 0
    self.y_speed = 3

  def update(self):
    if self.rect.top >= -1*self.y_speed and self.rect.top < 0:
      self.sprites.add(Strasse(self.sprites, self.F_BREITE, self.F_HOEHE))
    if self.rect.top > self.F_HOEHE:
      self.kill()    
    else:
      self.rect.x += self.x_speed
      self.rect.y += self.y_speed
