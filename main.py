from game.trex import TRex
from game.ptero import Ptero
from game.ground import Ground
from game.cloud import Cloud
from game.cactus import Cactus
from game.score import Score
from game.globals import *
from pygame.locals import *
import os, pygame, sys, random

pygame.init()

srcSize = (WIDTH, HEIGHT) = (600, 150)
FPS = 60

screen = pygame.display.set_mode(srcSize)
clock = pygame.time.Clock()
pygame.display.set_caption("T-Rex 404")


def check_cactus_collide(cactus, trex):
  for cactu in cactus:
    if pygame.sprite.collide_mask(trex, cactu):
      trex.set_is_dead()

def check_pteros_collide(pteros, trex):
  for ptero in pteros:
    if pygame.sprite.collide_mask(trex, ptero):
      trex.set_is_dead()

def create_cactus(cactus, last_obstacle, gameSpeed):
  if len(cactus) < 2:
    if len(cactus) == 0:
      last_obstacle.empty()
      last_obstacle.add(Cactus(gameSpeed, 40, 40))
    else:
      for l in last_obstacle:
        if l.rect.right < WIDTH * 0.7 and random.randrange(0, 40) == 10:
          last_obstacle.empty()
          last_obstacle.add(Cactus(gameSpeed, 40, 40))

def create_ptero(last_obstacle, gameSpeed):
  for l in last_obstacle:
    if l.rect.right < WIDTH * 0.5 and random.randrange(0, 100) == 10:
      last_obstacle.empty()
      last_obstacle.add(Ptero(gameSpeed, 46, 40))

def create_clouds(clouds):
  if len(clouds) < 7 and random.randrange(0, 150) == 10:
      Cloud(WIDTH, random.randrange(HEIGHT / 5, HEIGHT / 2))


def main():
  gameSpeed = 4
  gameOver = False
  gameQuit = False
  
  score = Score(screen)
  ground = Ground(screen, -1 * gameSpeed)
  trex = TRex(screen, 44, 47)

  clouds = pygame.sprite.Group()
  cactus = pygame.sprite.Group()
  pteros = pygame.sprite.Group()
  last_obstacle = pygame.sprite.Group()

  Cloud.containers = clouds
  Cactus.containers = cactus
  Ptero.containers = pteros

  while not gameOver:
    for event in pygame.event.get():
      if event.type == QUIT:
        gameOver = True
        
      if event.type == KEYDOWN:
        if event.key == K_SPACE or event.key == K_UP:
          trex.jump()
        if event.key == K_DOWN:
          trex.duck()

      if event.type == KEYUP:
        trex.no_duck()

    
    check_cactus_collide(cactus, trex)
    check_pteros_collide(pteros, trex)

    create_cactus(cactus, last_obstacle, gameSpeed)
    create_ptero(last_obstacle, gameSpeed)
    create_clouds(clouds)

    trex.update()
    ground.update()
    clouds.update()
    cactus.update()
    pteros.update()
    score.update()

    if pygame.display.get_surface() != None:
      screen.fill(BG_COLOR)
      ground.draw()
      clouds.draw(screen)
      cactus.draw(screen)
      pteros.draw(screen)
      score.draw()
      trex.draw()

      pygame.display.update()
    
    clock.tick(FPS)

    if trex.isDead:
      gameOver = True
      #print('score: {}'.format(score))

  while not gameQuit:
    for event in pygame.event.get():
      if event.type == QUIT:
        gameQuit = True

    if pygame.display.get_surface() != None:
      pygame.display.update()
    
    clock.tick(FPS)

  pygame.quit()
  sys.exit()


if __name__ == "__main__":
    main()