import os, pygame, sys, random
from pygame.locals import *

pygame.init()

srcSize = (width, height) = (600, 150)
FPS = 60

screen = pygame.display.set_mode(srcSize)
clock = pygame.time.Clock()
pygame.display.set_caption("T-Rex 404")

BLACK = (0,0,0)
WHITE = (255,255,255)
BG_COLOR = (235,235,235)


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


class TRex():
  def __init__(self, sizeX = -1, sizeY = -1):
    self.images, self.rect = load_sprite_sheet('dino.png', 5, 1, sizeX, sizeY)
    self.images1, self.rect1 = load_sprite_sheet('dino_ducking.png', 2, 1, sizeX, sizeY)
    self.image = self.images[0]
    self.trex_height = int(0.97 * height)
    self.rect.bottom = self.trex_height
    self.rect.left = width / 15
    self.index = 0
    self.counter = 0
    self.gravity = 0.6
    self.movement = [0, 0]
    self.jumpVelocity = 11.5
    self.isJumping = False
    self.isDucking = False
    self.isDead = False

  def set_rect_bottom(self):
    if self.rect.bottom > self.trex_height:
      self.isJumping = False
      self.rect.bottom = self.trex_height

  def set_is_dead(self):
    self.isDead = True

  def draw(self):
    screen.blit(self.image, self.rect)

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


class Cactus(pygame.sprite.Sprite):
  def __init__(self, speed = 5, sizeX = -1, sizeY = -1):
    pygame.sprite.Sprite.__init__(self, self.containers)
    self.images, self.rect = load_sprite_sheet('cacti-small.png', 3, 1, sizeX, sizeY)
    self.rect.bottom = int(0.97 * height)
    self.rect.left = width + self.rect.width
    self.image = self.images[random.randrange(0, 3)]
    self.movement = [-1 * speed, 0]

  def draw(self):
    screen.blit(self.image, self.rect)

  def update(self):
    self.rect = self.rect.move(self.movement)

    if self.rect.right < 0:
      self.kill()


class Ptero(pygame.sprite.Sprite):
  def __init__(self, speed = 5, sizeX = -1, sizeY = -1):
    pygame.sprite.Sprite.__init__(self, self.containers)
    self.images, self.rect = load_sprite_sheet('ptera.png', 2, 1, sizeX, sizeY)
    self.ptero_height = [height * 0.82, height * 0.75, height * 0.60]
    self.rect.centery = self.ptero_height[random.randrange(0,3)]
    self.rect.left = width + self.rect.width
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


class Ground():
  def __init__(self, speed = -5):
    self.image, self.rect = load_image('ground.png')
    self.image1, self.rect1 = load_image('ground.png')
    self.rect.bottom = height
    self.rect1.bottom = height
    self.rect1.left = self.rect.right
    self.speed = speed

  def draw(self):
    screen.blit(self.image, self.rect)
    screen.blit(self.image1, self.rect1)

  def update(self):
    self.rect.left += self.speed
    self.rect1.left += self.speed

    if self.rect.right < 0:
      self.rect.left = self.rect1.right

    if self.rect1.right < 0:
      self.rect1.left = self.rect.right


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
        if l.rect.right < width * 0.7 and random.randrange(0, 40) == 10:
          last_obstacle.empty()
          last_obstacle.add(Cactus(gameSpeed, 40, 40))

def create_ptero(last_obstacle, gameSpeed):
  for l in last_obstacle:
    if l.rect.right < width * 0.5 and random.randrange(0, 100) == 10:
      last_obstacle.empty()
      last_obstacle.add(Ptero(gameSpeed, 46, 40))

def create_clouds(clouds):
  if len(clouds) < 7 and random.randrange(0, 150) == 10:
      Cloud(width, random.randrange(height / 5, height / 2))


def main():
  gameSpeed = 4
  gameOver = False
  gameQuit = False
  
  ground = Ground(-1 * gameSpeed)
  trex = TRex(44, 47)

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

    if pygame.display.get_surface() != None:
      screen.fill(BG_COLOR)
      ground.draw()
      clouds.draw(screen)
      cactus.draw(screen)
      pteros.draw(screen)
      trex.draw()

      pygame.display.update()
    
    clock.tick(FPS)

    if trex.isDead:
      gameOver = True

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