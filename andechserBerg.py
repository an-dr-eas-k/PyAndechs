import pygame
import random
import math


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

    def __init__(self, F_BREITE, F_HOEHE):
        super().__init__()
        self.F_BREITE = F_BREITE
        self.F_HOEHE = F_HOEHE

        self.image = aspect_scale(pygame.image.load(
            "mann-von-oben1.png"), (100, 100))

        self.rect = self.image.get_rect()
        self.rect.center = (self.F_BREITE / 2, self.F_HOEHE / 2)
        self.punkte = 0
        self.promille = 0

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
        self.rect.clamp_ip(pygame.Rect(0, 0, self.F_BREITE, self.F_HOEHE))


class ZufallsObjekt(pygame.sprite.Sprite):

    bilder_top = [aspect_scale(pygame.image.load("hendl.png"), (100, 100)),
                  aspect_scale(pygame.image.load("hendlhaxl.png"), (100, 100))]

    bilder_flop = [aspect_scale(pygame.image.load("bierflasche-edit1.png"), (100, 100)),
                   aspect_scale(pygame.image.load("cocktail-edit1.png"), (100, 100))]

    n = 0

    def __init__(self, F_BREITE, F_HOEHE, sprites):
        super().__init__()
        ZufallsObjekt.n+=1
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
        
        # self.font = pygame.font.SysFont("Arial", 12)
        # self.textSurf = self.font.render('{}{}'.format(self.gut, self.id), 1, (255,255,255))
        # self.image = pygame.Surface((self.rect.width, self.rect.height))
        # W = self.textSurf.get_width()
        # H = self.textSurf.get_height()
        # self.image.blit(self.textSurf, [self.rect.width/2 - W/2, self.rect.height/2 - H/2])
 

    def update(self):
        if self.rect.top > self.F_HOEHE:
            self.kill()
        else:
            self.rect.x += self.x_speed
            self.rect.y += self.y_speed
            if random.randint(0, 120) == 0:
                self.x_speed = 0  # random.randint(-2, 2)


def text(text, fenster, position, groesse):
    font = pygame.font.SysFont('arial', groesse)
    text = font.render(text, False, (0, 0, 0))
    F_BREITE = text.get_rect().width
    fenster.blit(text, (position[0] - (F_BREITE / 2), position[1]))
