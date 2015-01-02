import sys
import sdl2
import sdl2.ext
import os

from engine import Input, Graphics

class Game(object):

	initialized = False
	game = None
	
	def __new__(cls, *p, **k):
		if not cls.game:
			cls.game = super(Game, cls).__new__(cls, *p, **k)
		return cls.game		

	def __init__(self):
		if self.initialized:
			return
			
		os.environ["PYSDL2_DLL_PATH"] = "/"
		
		sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)
		sdl2.ext.init()
		
		sdl2.SDL_JoystickEventState(sdl2.SDL_ENABLE)
		sdl2.SDL_JoystickOpen(0)
		
		self.quit = False
		
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
		
		self.stage = Graphics.Stage()
		clip1 = Graphics.Movieclip("./resources/stretch.bmp")
		clip2 = Graphics.Movieclip("./resources/stretch.bmp")
		self.stage.addChild(clip1)
		clip1.addChild(clip2)
		clip1.sprite.x = 100
		clip1.sprite.y = 0
		clip2.sprite.x = 100
		clip2.sprite.y = 100
		
		self.initialized = True

	def run(self):
		while not self.quit:
			self.parseEvents()
			self.printInputs()
			
			if self.input.clicked("exit"):
				self.quit = True
			
			if self.input.clicked("fullscreen"):
				self.stage.toggleFullscreen()
			
			self.stage.update()
			self.stage.render()
			sdl2.SDL_Delay(15)
			
	def parseEvents(self):
		events = sdl2.ext.get_events()
		input_events = []
		for event in events:
			if event.type == sdl2.SDL_QUIT:
				self.quit = True
				break
			elif event.type in [sdl2.SDL_KEYDOWN, sdl2.SDL_KEYUP, sdl2.SDL_MOUSEBUTTONDOWN, sdl2.SDL_MOUSEBUTTONUP, sdl2.SDL_JOYBUTTONDOWN, sdl2.SDL_JOYBUTTONUP]:
				input_events.append(event)
				break
		self.input.parseEvents(input_events)
		
	def printInputs(self):
		for code, key in self.input.registered.items():
			if key.pressed:
				print(code)
		if self.input.mouse.pressed:
			print("mouse")