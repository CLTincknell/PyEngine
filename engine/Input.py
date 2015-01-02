import sdl2
import sdl2.ext

class Input(object):
	
	initialized = False
	input = None
	
	def __new__(cls, *p, **k):
		if not cls.input:
			cls.input = super(Input, cls).__new__(cls, *p, **k)
		return cls.input		
		
	def __init__(self):
		if self.initialized:
			return
		self.registered = {}
		self.mouse = Mouse()
		self.initialized = True
	
	def register(self, keyword, keycode):
		self.registered[keyword] = Key(keycode)
		
	def parseEvents(self, events):
		self.mouse.clear()
		for keyword, key in self.registered.items():
			key.clear()
			
		for event in events:
			if event.type in [sdl2.SDL_MOUSEBUTTONDOWN, sdl2.SDL_MOUSEBUTTONUP]:
				self.mouse.update(event)
				continue
			elif event.type in [sdl2.SDL_JOYBUTTONDOWN, sdl2.SDL_JOYBUTTONUP]:
				print(event.type)
			else:
				for keyword, key in self.registered.items():
					if key.keycode == event.key.keysym.sym:
						key.update(event)
						continue
	
	def pressed(self, keyword):
		return False if keyword not in self.registered else self.registered[keyword].pressed
		
	def clicked(self, keyword):
		return False if keyword not in self.registered else self.registered[keyword].clicked
	
	def released(self, keyword):
		return False if keyword not in self.registered else self.registered[keyword].released
	
class InputObject(object):
	
	def __init__(self):
		self.DOWN = None
		self.UP = None
		self.pressed = False
		self.clicked = False
		self.released = True
		
	def update(self, event):
		if event.type == self.DOWN:
			if not self.pressed:
				self.clicked = True
			self.pressed = True
			self.released = False
		elif event.type == self.UP:
			self.clicked = False
			self.pressed = False
			self.released = True
	
	def clear(self):
		self.pressed = False
		self.released = True
	
class Key(InputObject):
	
	def __init__(self, keycode):
		super(Key, self).__init__()
		self.DOWN = sdl2.SDL_KEYDOWN
		self.UP = sdl2.SDL_KEYUP
		self.keycode = keycode

class Mouse(InputObject):

	def __init__(self):
		super(Mouse, self).__init__()
		self.DOWN = sdl2.SDL_MOUSEBUTTONDOWN
		self.UP = sdl2.SDL_MOUSEBUTTONUP