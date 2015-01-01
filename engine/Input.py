import sdl2
import sdl2.ext

class Input(object):
	
	registered = None
	mouse = None
	
	def __init__(self):
		self.registered = {}
		self.mouse = Mouse()
	
	def register(self, keyword, keycode):
		self.registered[keyword] = Key(keycode)
		
	def parseEvents(self, events):
		if self.mouse.clicked:
			self.mouse.clicked = False
			self.mouse.pressed = True
		for keyword, key in self.registered.items():
			if key.clicked:
				key.clicked = False
				key.pressed = True
		for event in events:
			if event.type in [sdl2.SDL_MOUSEBUTTONDOWN, sdl2.SDL_MOUSEBUTTONUP]:
				self.mouse.update(event)
				continue
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
	
	DOWN = None
	UP = None
	
	pressed = False
	clicked = False
	released = True
	
	def update(self, event):
		if event.type == self.DOWN:
			if self.pressed:
				self.clicked = False
			else:
				self.clicked = True
			self.pressed = True
			self.released = False
		elif event.type == self.UP:
			self.clicked = False
			self.pressed = False
			self.released = True
	
class Key(InputObject):

	keycode = None
	
	def __init__(self, keycode):
		self.keycode = keycode
		self.DOWN = sdl2.SDL_KEYDOWN
		self.UP = sdl2.SDL_KEYUP

class Mouse(InputObject):

	def __init__(self):
		self.DOWN = sdl2.SDL_MOUSEBUTTONDOWN
		self.UP = sdl2.SDL_MOUSEBUTTONUP