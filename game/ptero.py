from game.globals import *
from game.lib import load_sprite_sheet
import pygame, random

class Ptero(pygame.sprite.Sprite):
  def __init__(self, speed = 5, sizeX = -1, sizeY = -1):
    pygame.sprite.Sprite.__init__(self, self.containers)
    self.images, self.rect = load_sprite_sheet('ptera.png', 2, 1, sizeX, sizeY)
    self.ptero_heights = [WIN_HEIGHT * 0.82, WIN_HEIGHT * 0.55]
    self.rect.centery = self.ptero_heights[random.randrange(0,2)]
    self.rect.left = WIN_WIDTH + self.rect.width
    self.image = self.images[0]
    self.movement = [-1 * speed, 0]
    self.index = 0
    self.counter = 0

  def draw(self):
    screen.blit(self.image, self.rect)

  def update(self):
    if self.counter % 10 == 0:
      self.counter = 0
      self.index = (self.index + 1) % 2
    self.image = self.images[self.index]
    self.rect = self.rect.move(self.movement)
    self.counter += 1

    if self.rect.right < 0:
      self.kill()