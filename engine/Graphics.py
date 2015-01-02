import sdl2
import sdl2.ext
import math

from engine import Input

class Renderable(object):
	
	def __init__(self):
		self.parent = None
		self.children = []
		
	def update(self):
		for child in self.children:
			child.update()
			
	def render(self):
		for child in self.children:
			child.render()
	
	def addChild(self, child):
		if child not in self.children:
			child.parent = self
			self.children.append(child)
		
	def removeChild(self, child):
		if child in self.children:
			child.parent = None
			self.children.remove(child)
		
	def setChildIndex(self, child, index):
		if child in self.children:
			self.removeChild(child)
			child.parent = self
			self.children.insert(min(len(self.children), index), child)
			
	def getPosition(self):
		return None
		
	def generation(self):
		if self.parent:
			return 1 + self.parent.generation()
		return 1
	
class Stage(Renderable):

	initialized = False
	stage = None
	
	def __new__(cls, *p, **k):
		if not cls.stage:
			cls.stage = super(Stage, cls).__new__(cls, *p, **k)
		return cls.stage		
		
	def __init__(self):
		if self.initialized:
			return
		super(Stage, self).__init__()
		self.width = 800
		self.height = 600
		self.window = sdl2.ext.Window("Game", size = (self.width, self.height))
		self.window.show()
		self.renderer = sdl2.ext.SoftwareSpriteRenderSystem(self.window)
		self.factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
		self.fullscreen = False
		self.initialized = True
		
	def render(self):
		sdl2.ext.fill(self.window.get_surface(), sdl2.ext.Color(0, 0, 0))
		super(Stage, self).render()		
		#self.window.refresh()
		
	def toggleFullscreen(self):
		self.fullscreen = not self.fullscreen
		if not self.fullscreen:
			sdl2.SDL_SetWindowFullscreen(self.window.window, 0)
		else:
			sdl2.SDL_SetWindowFullscreen(self.window.window, sdl2.SDL_WINDOW_FULLSCREEN)
	
class Movieclip(Renderable):
	
	def __init__(self, path):
		super(Movieclip, self).__init__()
		self.filepath = path
		self.sprite = Stage().factory.from_image(self.filepath)
		self.physics = Physics()
	
	def update(self):
		self.updateSelf()
		super(Movieclip, self).update()
	
	def updateSelf(self):
		left = Input.Input().pressed("move_left")
		right = Input.Input().pressed("move_right")
		up = Input.Input().pressed("move_up")
		down = Input.Input().pressed("move_down")
		if right and not left:
			self.physics.ax = 1
		elif left and not right:
			self.physics.ax = -1
		else:
			self.physics.ax = 0
			self.physics.vx = self.physics.vx / 2
			if self.physics.vx < 0:
				self.physics.vx = math.ceil(self.physics.vx)
			else:
				self.physics.vx = math.floor(self.physics.vx)
		if up and not down:
			self.physics.ay = -1
		elif down and not up:
			self.physics.ay = 1
		else:
			self.physics.ay = 0
			self.physics.vy = self.physics.vy / 2
			if self.physics.vy < 0:
				self.physics.vy = math.ceil(self.physics.vy)
			else:
				self.physics.vy = math.floor(self.physics.vy)
		self.physics.vx += self.physics.ax
		self.physics.vy += self.physics.ay
		self.sprite.x = math.floor(self.sprite.x + self.physics.vx)
		self.sprite.y = math.floor(self.sprite.y + self.physics.vy)
		return
		
	def render(self):
		position = self.getPosition()
		Stage().renderer.render(self.sprite, position[0], position[1])
		
		super(Movieclip, self).render()
		
	def getPosition(self):
		parent_position = self.parent.getPosition()
		if parent_position:
			return self.sprite.x + parent_position[0], self.sprite.y + parent_position[1]
		return self.sprite.x, self.sprite.y
		
class Physics(object):

	def __init__(self):
		self.vx = 0
		self.vy = 0
		self.ax = 0
		self.ay = 0