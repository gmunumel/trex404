from game.lib import load_image
import pygame

class Cloud(pygame.sprite.Sprite):
  def __init__(self, x, y):
    pygame.sprite.Sprite.__init__(self, self.containers)
    self.image, self.rect = load_image('cloud.png', int(90*30/42), 30)
    self.rect.left = x
    self.rect.top = y
    self.speed = 1
    self.movement = [-1 * self.speed, 0]

  def draw(self):
    screen.blit(self.image, self.rect)

  def update(self):
    self.rect = self.rect.move(self.movement)

    if self.rect.right < 0:
      self.kill()