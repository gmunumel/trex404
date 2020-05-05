import os, pygame
from pygame.locals import *

def load_image(name, sizeX = -1, sizeY = -1):

  fullName = os.path.join('sprites', name)
  image = pygame.image.load(fullName)
  image = image.convert()

  colorkey = image.get_at((0, 0))
  image.set_colorkey(colorkey, RLEACCEL)

  if sizeX != -1 or sizeY != -1:
    image = pygame.transform.scale(image, (sizeX, sizeY))

  return image, image.get_rect()


def load_sprite_sheet(name, x, y, scaleX = -1, scaleY = -1):
  
  sprites = []
  fullName = os.path.join('sprites', name)
  sheet = pygame.image.load(fullName)
  sheet = sheet.convert()

  sheetRect = sheet.get_rect()

  sizeX = sheetRect.width / x
  sizeY = sheetRect.height / y

  for i in range(0, y):
    for j in range(0, x):
      rect = pygame.Rect((j * sizeX, i * sizeY, sizeX, sizeY))
      image = pygame.Surface(rect.size)
      image = image.convert()
      image.blit(sheet, (0,0), rect)

      colorkey = image.get_at((0, 0))
      image.set_colorkey(colorkey, RLEACCEL)

      if scaleX != -1 or scaleY != -1:
        image = pygame.transform.scale(image, (scaleX, scaleY))

      sprites.append(image)


  spriteRect = sprites[0].get_rect()

  return sprites, spriteRect