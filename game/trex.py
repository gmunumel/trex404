#import pygame
from game.globals import *
from game.lib import load_sprite_sheet

class TRex():
  def __init__(self, screen, sizeX = -1, sizeY = -1):
    self.images, self.rect = load_sprite_sheet('dino.png', 5, 1, sizeX, sizeY)
    self.images1, self.rect1 = load_sprite_sheet('dino_ducking.png', 2, 1, sizeX, sizeY)
    self.image = self.images[0]
    self.trex_height = int(0.97 * WIN_HEIGHT)
    self.rect.bottom = self.trex_height
    self.rect.left = WIN_WIDTH / 15
    self.index = 0
    self.counter = 0
    self.gravity = 0.6
    self.movement = [0, 0]
    self.jumpVelocity = 11.5
    self.isJumping = False
    self.isDucking = False
    self.isDead = False
    self.screen = screen

  def set_rect_bottom(self):
    if self.rect.bottom > self.trex_height:
      self.isJumping = False
      self.rect.bottom = self.trex_height

  def set_is_dead(self):
    self.isDead = True

  def draw(self):
    self.screen.blit(self.image, self.rect)

  def jump(self):
    if not self.isDucking:
      self.isJumping = True
      self.movement[1] = -1 * self.jumpVelocity
      self.index = 0
      self.counter = 0

  def duck(self):
    if not self.isJumping:
      self.isDucking = True
      self.index = 0
      self.counter = 0

  def no_duck(self):
    self.isDucking = False

  def update(self):
    if self.isDucking:
      if self.counter % 8 == 0:
        self.counter = 0
        self.index = (self.index + 1) % 2
    else:
      if self.counter % 5 == 0:
        self.counter = 0
        self.index += 1

        if self.index == 1:
          self.index += 1

        if self.index % 4 == 0:
          self.index = 0

    if self.isJumping:
      self.movement[1] += self.gravity

    if self.isDead:
      self.image = self.images[4]
    elif self.isDucking:
      self.image = self.images1[self.index]
    else:
      self.image = self.images[self.index]

    self.rect = self.rect.move(self.movement)
    self.set_rect_bottom()

    self.counter += 1