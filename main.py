#!python
import pygame, sys, andechserBerg, os, signal

N_MIN_OBJEKTE = 7
F_BREITE, F_HOEHE = 1000, 500

pygame.init()

fenster = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
F_BREITE, F_HOEHE = pygame.display.get_surface().get_size()

sprites = pygame.sprite.LayeredUpdates()
strasse = andechserBerg.Strasse(sprites, F_BREITE, F_HOEHE)
strasse.rect.y = -strasse.rect.height+F_HOEHE
sprites.add(strasse)
wanderer = andechserBerg.Wanderer(F_BREITE, F_HOEHE)
sprites.add(wanderer)
uhr = pygame.time.Clock()

t_kollision_top = -100
t_kollision_flop= -100

i = 0

while True:
  i+=1
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      os._exit(0)

  
  n_neue_objekte = int (N_MIN_OBJEKTE - len(sprites) + i / 100)
  
  for j in range(n_neue_objekte):
    try:
      sprites.add(andechserBerg.ZufallsObjekt(F_BREITE, F_HOEHE, sprites))
    except:
      pass
      

  for sprite in sprites:
    if type(sprite) is andechserBerg.ZufallsObjekt and pygame.sprite.collide_rect(wanderer, sprite):
      if sprite.gut:
        wanderer.punkte +=1
        andechserBerg.fressen.play()
        if (wanderer.promille > 0):
          wanderer.promille -= 1
        t_kollision_top = pygame.time.get_ticks()
      else:
        wanderer.promille += 1
        andechserBerg.saufen.play()
        t_kollision_flop = pygame.time.get_ticks()
        if wanderer.promille > 15:
          fenster.fill((255,255,255))
          andechserBerg.kotzen.play()
          andechserBerg.text("Magen auspumpen erforderlich", fenster, (F_BREITE / 2, F_HOEHE / 2), 50)
          andechserBerg.text(str(wanderer.punkte) + " Menüs verzehrt", fenster, (F_BREITE / 2, F_HOEHE / 2 + 60), 30)
          pygame.display.flip()
          pygame.time.wait(3000)
          pygame.quit()
          os._exit(0)
      sprite.kill()

  if pygame.time.get_ticks() - t_kollision_flop < 100:
    fenster.fill((255, 0, 0))
  elif pygame.time.get_ticks() - t_kollision_top < 100:
    fenster.fill((0, 255, 0))
  else:
    fenster.fill((255, 255, 255))
        
  sprites.update()
  sprites.draw(fenster)

  andechserBerg.text("Menüs verzehrt: " + str(wanderer.punkte), fenster, (F_BREITE - 150, F_HOEHE - 50), 30)
  andechserBerg.text("Promille: {0:.1f}".format(wanderer.promille*0.1), fenster, (90, F_HOEHE - 50), 30)

  pygame.display.flip()
  uhr.tick(50)
  