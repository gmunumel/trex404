from game.globals import *
from game.lib import load_image

class Ground():
  def __init__(self, screen, speed = -5):
    self.image, self.rect = load_image('ground.png')
    self.image1, self.rect1 = load_image('ground.png')
    self.rect.bottom = WIN_HEIGHT
    self.rect1.bottom = WIN_HEIGHT
    self.rect1.left = self.rect.right
    self.speed = speed
    self.screen = screen

  def draw(self):
    self.screen.blit(self.image, self.rect)
    self.screen.blit(self.image1, self.rect1)

  def update(self):
    self.rect.left += self.speed
    self.rect1.left += self.speed

    if self.rect.right < 0:
      self.rect.left = self.rect1.right

    if self.rect1.right < 0:
      self.rect1.left = self.rect.right