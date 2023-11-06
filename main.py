import pygame, sys
from time import time
from pygame.locals import *
from config import *
from board import Board
from components import Renderer, Update, Input


pygame.init()

# Variables
fpsClock = pygame.time.Clock()
WINDOW = pygame.display.set_mode((SCREEN_SIZE[0], SCREEN_SIZE[1]), RESIZABLE)
pygame.display.set_caption('Chess!')

# Initialise board
board = Board()

Renderer.objects_to_render.sort()

# Main runtime loop
def main () :
   looping = True

   prev_time = time()
  
   while looping :
    current_time = time()
    dt = current_time - prev_time
    prev_time = current_time

    handle_input()
    handle_update(dt)
    handle_rendering()
    fpsClock.tick(FPS)

 

def handle_input():
    for event in pygame.event.get() :
      # WHY ESCAPE ISNT WORKING HERE??
      if event.type == QUIT or event.type == K_ESCAPE:
        pygame.quit()
        sys.exit()

      # TODO: add a callback so that when this changes, everything can recalculate its position relative to the screen
      if event.type == WINDOWRESIZED:
         SCREEN_SIZE = WINDOW.get_size()

      for input_object in Input.objects_receive_input:
         input_object.handle_input(event, pygame.mouse.get_pos())
       


def handle_update(dt: float):
    for obj in Update.objects_to_update:
       obj.update(dt)
  

def handle_rendering():
    WINDOW.fill(BACKGROUND_COLOR)

    for obj in Renderer.objects_to_render:
       obj.draw(WINDOW)
   
    pygame.display.update()

  
main()


# https://code.visualstudio.com/docs/introvideos/versioncontrol
# https://www.pygame.org/wiki/GettingStartedpython3 -m pip install -U pygame --user
# http://pygametutorials.wikidot.com/tutorials-basic
# https://www.youtube.com/watch?v=n3tA3Ku65_8&ab_channel=freeCodeCamp.org