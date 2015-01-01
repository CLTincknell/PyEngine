import sdl2

class Stage(object):

	window = None
	
	width = 800
	height = 600
	
	fullscreen = False
	
	children = []
	
	def __init__(self):
		self.window = sdl2.ext.Window("Game", size = (self.width, self.height))
		self.window.show()
		
	def render(self):
		sdl2.ext.fill(self.window.get_surface(), sdl2.ext.Color(0, 0, 0))
		
		for child in self.children:
			child.render()
		
		self.window.refresh()
		
	def toggleFullscreen(self):
		self.fullscreen = not self.fullscreen
		if not self.fullscreen:
			sdl2.SDL_SetWindowFullscreen(self.window.window, 0)
		else:
			sdl2.SDL_SetWindowFullscreen(self.window.window, sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP)
			
	def addChild(self, child):
		if self.children.count(child) == 1:
			self.children.append(child)
		
	def removeChild(self, child):
		if self.children.count(child) == 1:
			self.children.remove(child)
		
	def setChildIndex(self, child, index):
		if self.children.count(child) == 1:
			self.removeChild(child)
			self.children.insert(min(len(self.children), index), child)
	