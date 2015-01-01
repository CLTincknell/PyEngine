import sys
import sdl2
import sdl2.ext
import os

from engine import Input

class Game(object):

	game = None
	
	fullscreen = False
	
	width = 800
	height = 600
	
	quit = False

	#put this inside a Stage object
	window = None
	world = None
	
	input = None
	
	def __new__(cls, *p, **k):
		if not cls.game:
			cls.game = super(Game, cls).__new__(cls, *p, **k)
		return cls.game		

	def __init__(self):
		os.environ["PYSDL2_DLL_PATH"] = "/"
		
		sdl2.ext.init()
		
		self.window = sdl2.ext.Window("Game", size = (self.width, self.height))
		self.world = sdl2.ext.World()
		
		self.input = Input.Input()
		self.input.register("move_up", sdl2.SDLK_w)
		self.input.register("move_left", sdl2.SDLK_a)
		self.input.register("move_down", sdl2.SDLK_s)
		self.input.register("move_right", sdl2.SDLK_d)
		self.input.register("shoot_up", sdl2.SDLK_UP)
		self.input.register("shoot_left", sdl2.SDLK_LEFT)
		self.input.register("shoot_down", sdl2.SDLK_DOWN)
		self.input.register("shoot_right", sdl2.SDLK_RIGHT)
		self.input.register("exit", sdl2.SDLK_ESCAPE)
		self.input.register("jump", sdl2.SDLK_SPACE)
		self.input.register("fullscreen", sdl2.SDLK_f)

	def run(self):
		self.window.show()
		
		while not self.quit:
			self.parseEvents()
			self.printInputs()
			
			if self.input.clicked("exit"):
				self.quit = True
			
			if self.input.clicked("fullscreen"):
				if self.fullscreen:
					self.fullscreen = False
					sdl2.SDL_SetWindowFullscreen(self.window.window, 0)
				else:
					self.fullscreen = True
					sdl2.SDL_SetWindowFullscreen(self.window.window, sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP)
			
				
			
			sdl2.SDL_Delay(15)
			self.window.refresh()
			self.world.process()
			
	def parseEvents(self):
		events = sdl2.ext.get_events()
		input_events = []
		for event in events:
			if event.type == sdl2.SDL_QUIT:
				self.quit = True
				break
			elif event.type in [sdl2.SDL_KEYDOWN, sdl2.SDL_KEYUP, sdl2.SDL_MOUSEBUTTONDOWN, sdl2.SDL_MOUSEBUTTONUP]:
				input_events.append(event)
				break
		self.input.parseEvents(input_events)
		
	def printInputs(self):
		for code, key in self.input.registered.items():
			if key.clicked:
				print(code)
		if self.input.mouse.clicked:
			print("mouse")