from math import ceil, floor
import pygame
from pygame.math import Vector2 as vector

from misc import *


# class for anything the player can interact with, will be packaged into a maze
# most attributes should be immutable, seve for anything in self.flags
class element:
  def __init__(self, pos, **flags):
    self.pos = pos
    self.flags = {"active":True}
    self.flags.update(flags)
  
  def __str__(self):
    return f"element@({self.x}, {self.y})"
  
  @property
  def x(self):
    return self.pos.x
  
  @property
  def y(self):
    return self.pos.y
  
  def draw(self, surface):
    pass


# class for walls, subclasses element
class Wall(element):
  def __init__(self, pos, **flags):
    super().__init__(pos, **flags)
    self.horiz = not self.pos.x%1
    self.verti = not self.pos.y%1
  
  def draw(self, surface, size):
    start = to_surface_pos(map(floor, self.pos), size)
    stop = to_surface_pos(map(ceil, self.pos), size)
    pygame.draw.line(surface, foreground, start, stop, 3)


# decorator for creating element subclasses
# element_dec returns the actual decerator function
def element_dec(cls):
  def decorator(subcls):
    subcls.action = {**cls.action, **subcls.action}
    return subcls
  return decorator


# class for tiles that activate when landed on, mixin, subclasses element
@element_dec
class Plate(element):
  action = {"if":"landed"}
  
  def __init__(self, pos, **flags):
    super().__init__(pos, **flags)


# class for finish tile, subclasses element
@Plate
class Finish(element):
  action = {"finish":None}
  
  def __init__(self, pos, **flags):
    super().__init__(pos, **flags)
