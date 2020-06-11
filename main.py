from game.trex import TRex
from game.ptero import Ptero
from game.ground import Ground
from game.cloud import Cloud
from game.cactus import Cactus
from game.score import Score
from game.globals import *
from pygame.locals import *
import os, pygame, sys, random, neat

pygame.init()

srcSize = (WIN_WIDTH, WIN_HEIGHT) = (600, 150)
FPS = 60

screen = pygame.display.set_mode(srcSize)
clock = pygame.time.Clock()
pygame.display.set_caption("T-Rex 404")


def check_cactus_collide(cactus, trexs, genomes_track, nets):
  for cactu in cactus:
    for i, trex in enumerate(trexs):
      if pygame.sprite.collide_mask(trex, cactu):
        trex.set_is_dead()
        genomes_track[i].fitness -= 1
        trexs.pop(i)
        nets.pop(i)
        genomes_track.pop(i)

def check_pteros_collide(pteros, trexs, genomes_track, nets):
  for ptero in pteros:
    for i, trex in enumerate(trexs):
      if pygame.sprite.collide_mask(trex, ptero):
        trex.set_is_dead()
        genomes_track[i].fitness -= 1
        trexs.pop(i)
        nets.pop(i)
        genomes_track.pop(i)

def create_cactus(cactus, last_obstacle, gameSpeed):
  if len(cactus) < 2:
    if len(last_obstacle) == 0:
      last_obstacle.add(Cactus(gameSpeed, 40, 40))
    else:
      for l in last_obstacle:
        if l.rect.right < WIN_WIDTH * 0.5 and random.randrange(0, 40) == 10:
          last_obstacle.empty()
          last_obstacle.add(Cactus(gameSpeed, 40, 40))

def create_ptero(pteros, last_obstacle, gameSpeed):
  for l in last_obstacle:
    if l.rect.right < WIN_WIDTH * 0.75 and random.randrange(0,60) == 10:
      last_obstacle.empty()
      last_obstacle.add(Ptero(gameSpeed, 46, 40))

def create_clouds(clouds):
  if len(clouds) < 7 and random.randrange(0, 150) == 10:
      Cloud(WIN_WIDTH, random.randrange(WIN_HEIGHT / 5, WIN_HEIGHT / 2))

def update_fitness(trexs, cactus, pteros, genomes_track, nets):
  for genome_track in genomes_track:
    genome_track.fitness += 5

  for i, trex in enumerate(trexs):
    genomes_track[i].fitness += 0.1

    for cactu in cactus:
      distance_x = nets[i].activate((trex.rect.right, abs(trex.rect.right - cactu.rect.left)))

      if distance_x[0] > 0.5 and not trex.isJumping:
        trex.jump()

    for ptero in pteros:
      distance_x = nets[i].activate((trex.rect.right, abs(trex.rect.right - ptero.rect.left)))

      if distance_x[0] > 0.5:
        distance_y = nets[i].activate((trex.rect.top, abs(trex.rect.top - ptero.rect.bottom)))

        if distance_y[0] > 0.5 and not trex.isDucking:
          trex.duck()
        elif not trex.isJumping:
          trex.jump()

      else:
        distance_x = nets[i].activate((trex.rect.left, abs(trex.rect.left - ptero.rect.right)))
        
        if distance_x[0] > 0.1:
          trex.no_duck()


def main_game(genomes, config):
  gameSpeed = 4
  gameOver = False
  gameQuit = False

  ground = Ground(screen, -1 * gameSpeed)
  score = Score(screen)

  nets = []
  genomes_track = []
  trexs = []

  for _, genome in genomes:
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    nets.append(net)
    trexs.append(TRex(screen, 44, 47))
    genome.fitness = 0
    genomes_track.append(genome)


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
        quit() 
        
      if event.type == KEYDOWN:
        if event.key == K_SPACE or event.key == K_UP:
          for trex in trexs:
            trex.jump()
        if event.key == K_DOWN:
          for trex in trexs:
            trex.duck()

      if event.type == KEYUP:
        for trex in trexs:
          trex.no_duck()

    
    check_cactus_collide(cactus, trexs, genomes_track, nets)
    check_pteros_collide(pteros, trexs, genomes_track, nets)

    create_cactus(cactus, last_obstacle, gameSpeed)
    create_ptero(pteros, last_obstacle, gameSpeed)
    create_clouds(clouds)

    for trex in trexs:
      trex.update()
    
    update_fitness(trexs, cactus, pteros, genomes_track, nets)

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

      for trex in trexs:
        trex.draw()

      pygame.display.update()

    if (score.get_score() > 1000 and gameSpeed == 4) or \
      (score.get_score() > 2000 and gameSpeed == 4.5) or \
      (score.get_score() > 3000 and gameSpeed == 5) or \
      (score.get_score() > 4000 and gameSpeed == 5.5):
      gameSpeed += 0.5
      ground.set_speed(-1 * gameSpeed)
    
    if len(trexs) == 0:
      gameOver = True

    clock.tick(FPS)

  """
  while not gameQuit:
    for event in pygame.event.get():
      if event.type == QUIT:
        gameQuit = True

    if pygame.display.get_surface() != None:
      pygame.display.update()
    
    clock.tick(FPS)
  """

  #quit()


def run_neat(config_path):
  config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, 
    neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

  population = neat.Population(config)

  population.add_reporter(neat.StdOutReporter(True))
  stats = neat.StatisticsReporter()
  population.add_reporter(stats)

  winner = population.run(
    main_game, #fitness function
    50 # maximum number of iterations to run
  )

  print('\nBest genome:\n{!s}'.format(winner))


def config_neat():
  local_dir = os.path.dirname(__file__)
  config_path = os.path.join(local_dir, "neat/config-feedforward.txt")
  run_neat(config_path)

def quit():
  pygame.quit()
  sys.exit()

def main():
  config_neat()
  #main_game()

if __name__ == "__main__":
  main()
