from game.globals import *
from game.lib import load_sprite_sheet
import pygame, random

class Cactus(pygame.sprite.Sprite):
  def __init__(self, speed = 5, sizeX = -1, sizeY = -1):
    pygame.sprite.Sprite.__init__(self, self.containers)
    self.images, self.rect = load_sprite_sheet('cacti-small.png', 3, 1, sizeX, sizeY)
    self.rect.bottom = int(0.97 * HEIGHT)
    self.rect.left = WIDTH + self.rect.width
    self.image = self.images[random.randrange(0, 3)]
    self.movement = [-1 * speed, 0]

  def draw(self):
    screen.blit(self.image, self.rect)

  def update(self):
    self.rect = self.rect.move(self.movement)

    if self.rect.right < 0:
      self.kill()