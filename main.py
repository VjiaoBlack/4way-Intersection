#!/usr/bin/python
from sys import argv
import pygame
from pygame.locals import *
import math
import random

CAR_WIDTH=50.0
CAR_LENGTH=80.0
CAR_VEL = 5.0

COLORS = {}
COLORS["NONE"] = (0,0,0)
COLORS["CHECKING"] = (100,100,255)
COLORS["GOING"] = (100,255,100)
COLORS["WAITING"] = (255,100,100)

PHI_VEL_TURNS = {}
PHI_VEL_TURNS["STRAIGHT"] = 0.0
PHI_VEL_TURNS["LEFT"] = 0.027
PHI_VEL_TURNS["RIGHT"] = -0.06

TURN_AMT = {}
TURN_AMT["STRAIGHT"] = 0
TURN_AMT["LEFT"] = 58
TURN_AMT["RIGHT"] = 26

class Car:
  def __init__(self, x, y, phi):
    self.vel = CAR_VEL
    self.phi = float(phi)

    self.state = "NONE"
    self.turn = "STRAIGHT"
    self.x = float(x) # center
    self.y = float(y) # center
    self.turn_amt = 0

    self.num_waits = 0
    self.cur_wait_amt = 0
    self.next_wait_amt = 50

  def draw(self, screen):
    points = []
    front_x = CAR_LENGTH * math.sin(self.phi) / 2.0
    front_y = CAR_LENGTH * math.cos(self.phi) / 2.0

    side_x = CAR_WIDTH * math.cos(self.phi) / 2.0
    side_y = CAR_WIDTH * math.sin(self.phi) / 2.0

    # front cross side points out of screen

    points.append((self.x - front_x - side_x,\
             self.y - front_y + side_y))

    points.append((self.x - front_x + side_x ,\
             self.y - front_y - side_y))

    points.append((self.x + front_x + side_x,\
             self.y + front_y - side_y))

    points.append((self.x + front_x - side_x ,\
             self.y + front_y + side_y ))

    pygame.draw.polygon(screen, (194, 194, 194), points)
    pygame.draw.circle(screen, COLORS[self.state], (int(self.x + front_x), int(self.y + front_y)), 10)

  def update(self):
    self.x += self.vel * math.sin(self.phi)
    self.y += self.vel * math.cos(self.phi)
    if (self.turn_amt <= 0):
      self.turn = "STRAIGHT"
    else:
      self.turn_amt -= 1
    self.phi += PHI_VEL_TURNS[self.turn]

  def change_state(self, front, right, intersections):
    if (len(intersections) > 0):
      for car in intersections:
        if car.state == "GOING":
          self.state = "WAITING"
          self.cur_wait_amt = self.next_wait_amt
          self.num_waits += 1
          return

    if (front != None):
      if front.state != "WAITING":
        self.state = "WAITING"
        self.cur_wait_amt = self.next_wait_amt
        self.num_waits += 1
        return

    if (right != None):
      if right.state != "WAITING":
        self.state = "WAITING"
        self.cur_wait_amt = self.next_wait_amt
        self.num_waits += 1
        return

    self.state = "GOING"
    self.turn = random.choice(["RIGHT", "LEFT", "STRAIGHT"])
    self.turn_amt = TURN_AMT[self.turn]
    self.vel = CAR_VEL


class Game:

  def __init__(self, diff, dim, path):
    self.size = (800,600)
    self.screen = pygame.display.set_mode(self.size)

    pygame.display.set_caption('4-Way Intersection Demo')

    font = pygame.font.SysFont(pygame.font.get_default_font(), 55)
    text = font.render("Loading...", 1, (255,255,255))
    rect = text.get_rect()
    rect.center = self.size[0]/2, self.size[1]/2
    self.screen.blit(text, rect)
    pygame.display.update(rect)

    self.diff = diff
    self.dim = map(int, dim.split('x'))
    self.path = path

    self.left_cars = []
    self.top_cars = []
    self.right_cars = []
    self.bottom_cars = []

    self.turning_cars = []

  def start(self):
    self.draw_track()
    self.loop()


  def draw_track(self):
    self.screen.fill( (64, 64, 64) )

    pygame.draw.rect(self.screen, (255, 255, 255), (0, 200-5, 300, 10))
    pygame.draw.rect(self.screen, (255, 255, 255), (0, 400-5, 300, 10))

    pygame.draw.rect(self.screen, (255, 255, 255), (500, 200-5, 300, 10))
    pygame.draw.rect(self.screen, (255, 255, 255), (500, 400-5, 300, 10))


    pygame.draw.rect(self.screen, (255, 255, 255), (300-5, 0, 10, 200))
    pygame.draw.rect(self.screen, (255, 255, 255), (500-5, 0, 10, 200))

    pygame.draw.rect(self.screen, (255, 255, 255), (300-5, 400, 10, 200))
    pygame.draw.rect(self.screen, (255, 255, 255), (500-5, 400, 10, 200))

    pygame.draw.rect(self.screen, (255, 255, 0), (400-5, 0, 10, 200))
    pygame.draw.rect(self.screen, (255, 255, 0), (400-5, 400, 10, 200))
    pygame.draw.rect(self.screen, (255, 255, 0), (0, 300-5, 300, 10))
    pygame.draw.rect(self.screen, (255, 255, 0), (500, 300-5, 300, 10))

    pygame.draw.rect(self.screen, (255, 0, 0), (300-5, 300-5, 10, 100 + 10))
    pygame.draw.rect(self.screen, (255, 0, 0), (500-5, 200-5, 10, 100 + 10))
    pygame.draw.rect(self.screen, (255, 0, 0), (300-5, 200-5, 100 + 10, 10))
    pygame.draw.rect(self.screen, (255, 0, 0), (400-5, 400-5, 100 + 10, 10))


    pygame.display.update()

  def loop(self):
    self.clock = pygame.time.Clock()
    self.keep_going = 1

    while self.keep_going:
      self.clock.tick(30)
      for event in pygame.event.get():
        if event.type == QUIT:
          self.keep_going = 0
        elif event.type == KEYDOWN:
          if event.key == K_ESCAPE:
            self.keep_going = 0

          # the following four 
          if event.key == K_DOWN:
            c = Car(350, 0, 0)
            self.bottom_cars.append(c)

          if event.key == K_UP:
            c = Car(450, 600, -math.pi)
            self.top_cars.append(c)

          if event.key == K_LEFT:
            c = Car(800, 250, -0.5 * math.pi)
            self.left_cars.append(c)

          if event.key == K_RIGHT:
            c = Car(0, 350, 0.5 * math.pi)
            self.right_cars.append(c)

      keys = pygame.key.get_pressed()
      self.draw_track()
      self.update_cars()
      self.draw_cars()
      pygame.display.update()

  def update_cars(self):
    prev = -1

    top_car = self.top_cars[0] if self.top_cars else None
    bottom_car = self.bottom_cars[0] if self.bottom_cars else None
    right_car = self.right_cars[0] if self.right_cars else None
    left_car = self.left_cars[0] if self.left_cars else None

    if (top_car and top_car.state == "NONE"):
      top_car = None
    if (right_car and right_car.state == "NONE"):
      right_car = None
    if (left_car and left_car.state == "NONE"):
      left_car = None
    if (bottom_car and bottom_car.state == "NONE"):
      bottom_car = None


    for lcar in self.left_cars:
      if (prev == -1):
        # check if this car is at the stop sign
        if lcar.state == "CHECKING" or lcar.state == "WAITING":
          if lcar.cur_wait_amt > 0:
            lcar.cur_wait_amt -= 1
          else:
            # check other cars
            # lcar.state = "GOING"
            # lcar.turn = random.choice(["RIGHT", "LEFT", "STRAIGHT"])
            # lcar.turn_amt = TURN_AMT[lcar.turn]
            # lcar.vel = CAR_VEL
            lcar.change_state(right_car, bottom_car, self.turning_cars)
        elif lcar.state == "NONE" and lcar.x <= 500 + CAR_LENGTH / 2:
          lcar.vel = 0.0
          lcar.state = "CHECKING"
          lcar.cur_wait_amt = 30
        else:
          lcar.vel = CAR_VEL

      if (prev != -1):
        if math.fabs(lcar.x - prev) < CAR_LENGTH + 20 + lcar.vel:
          lcar.vel = 0.0
        else:
          lcar.vel = CAR_VEL
      lcar.update()
      prev = lcar.x
      if lcar.state == "GOING":
        self.left_cars.remove(lcar)
        self.turning_cars.append(lcar)

    prev = -1
    for rcar in self.right_cars:
      if (prev == -1):
        if rcar.state == "CHECKING" or rcar.state == "WAITING":
          if rcar.cur_wait_amt > 0:
            rcar.cur_wait_amt -= 1
          else:
            rcar.change_state(left_car, top_car, self.turning_cars)
        elif rcar.state == "NONE" and rcar.x >= 300 - CAR_LENGTH / 2:
          rcar.vel = 0.0
          rcar.state = "CHECKING"
          rcar.cur_wait_amt = 30
        else:
          rcar.vel = CAR_VEL

      if (prev != -1):
        if math.fabs(rcar.x - prev) < CAR_LENGTH + 20 + rcar.vel:
          rcar.vel = 0.0
        else:
          rcar.vel = CAR_VEL
      rcar.update()
      prev = rcar.x
      if rcar.state == "GOING":
        self.right_cars.remove(rcar)
        self.turning_cars.append(rcar)

    prev = -1
    for tcar in self.top_cars:
      if (prev == -1):
        if tcar.state == "CHECKING" or tcar.state == "WAITING":
          if tcar.cur_wait_amt > 0:
            tcar.cur_wait_amt -= 1
          else:
            tcar.change_state(bottom_car, left_car, self.turning_cars)
        elif tcar.state == "NONE" and tcar.y <= 400 + CAR_LENGTH / 2:
          tcar.vel = 0.0
          tcar.state = "CHECKING"
          tcar.cur_wait_amt = 30
        else:
          tcar.vel = CAR_VEL

      if (prev != -1):
        if math.fabs(tcar.y - prev) < CAR_LENGTH + 20 + tcar.vel:
          tcar.vel = 0.0
        else:
          tcar.vel = CAR_VEL
      tcar.update()
      prev = tcar.y
      if tcar.state == "GOING":
        self.top_cars.remove(tcar)
        self.turning_cars.append(tcar)

    prev = -1
    for bcar in self.bottom_cars:
      if (prev == -1):
        if bcar.state == "CHECKING" or bcar.state == "WAITING":
          if bcar.cur_wait_amt > 0:
            bcar.cur_wait_amt -= 1
          else:
            bcar.change_state(top_car, right_car, self.turning_cars)
        elif bcar.state == "NONE" and bcar.y >= 200 - CAR_LENGTH / 2:
          bcar.vel = 0.0
          bcar.state = "CHECKING"
          bcar.cur_wait_amt = 30
        else:
          bcar.vel = CAR_VEL

      if (prev != -1):
        if math.fabs(bcar.y - prev) < CAR_LENGTH + 20 + bcar.vel:
          bcar.vel = 0.0
        else:
          bcar.vel = CAR_VEL
      bcar.update()
      prev = bcar.y
      if bcar.state == "GOING":
        self.bottom_cars.remove(bcar)
        self.turning_cars.append(bcar)

    for car in self.turning_cars:
      car.update()
      if (car.x < 250 or car.x > 550 or car.y < 150 or car.y > 450):
        car.state = "NONE"

    return

  def draw_cars(self):
    for lcar in self.left_cars:
      lcar.draw(self.screen)

    for rcar in self.right_cars:
      rcar.draw(self.screen)

    for tcar in self.top_cars:
      tcar.draw(self.screen)

    for bcar in self.bottom_cars:
      bcar.draw(self.screen)

    for car in self.turning_cars:
      car.draw(self.screen)

    return

if __name__ == '__main__':
  pygame.init()
  args = argv[1:]
  diff = 0
  dim = '30x40'
  path = 1

  g = Game(diff, dim, path)
  g.start()
