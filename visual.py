import pygame
import math
from queue import PriorityQueue
from queue import Queue
import random

WIDTH = 800
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))

pygame.display.set_caption("PathFinding Visualizer")

pygame.init()
clock = pygame.time.Clock()
clock.tick(60)

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,155,0)
GREY = (128,128,128)
TURQUOISE = (62,224,208)

class Spot:

	def __init__(self, row, col, width, total_rows):

		self.row = row
		self.col = col
		self.x = row*width
		self.y = col*width
		self.width = width
		self.color = WHITE
		self.neighbors = []
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == RED

	def is_open(self):
		return self.color==GREEN

	def is_barrier(self):
		return self.color ==BLACK

	def is_start(self):
		return self.color == YELLOW

	def is_end(self):
		return self.color == YELLOW

	def reset(self):
		self.color = WHITE

	def make_closed(self):
		self.color = RED

	def make_open(self):
		self.color = GREEN

	def make_barrier(self):
		self.color = BLACK

	def make_start(self):
		self.color = YELLOW

	def make_end(self):
		self.color = YELLOW

	def make_path(self):
		self.color = BLUE


	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))


	def update_neighbors(self, grid):
		
		self.neighbors = []

		#DOWN
		if(self.row < self.total_rows-1 and not grid[self.row+1][self.col].is_barrier()):
			self.neighbors.append(grid[self.row+1][self.col])
		#UP
		if(self.row > 0 and not grid[self.row-1][self.col].is_barrier()):
			self.neighbors.append(grid[self.row-1][self.col])
		#RIGHT
		if(self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_barrier()):
			self.neighbors.append(grid[self.row][self.col+1])
		#LEFT
		if(self.col > 0 and not grid[self.row][self.col-1].is_barrier()):
			self.neighbors.append(grid[self.row][self.col-1])

		# #TOP LEFT
		# if(self.row > 0 and self.col > 0 and not grid[self.row-1][self.col-1].is_barrier()):
		# 	self.neighbors.append(grid[self.row-1][self.col-1])

		# #TOP RIGHT
		# if(self.row > 0 and self.col < self.total_rows-1 and not grid[self.row-1][self.col+1].is_barrier()):
		# 	self.neighbors.append(grid[self.row-1][self.col+1])

		# #BOTTOM LEFT
		# if(self.row < self.total_rows-1 and self.col > 0 and not grid[self.row+1][self.col-1].is_barrier()):
		# 	self.neighbors.append(grid[self.row+1][self.col-1])

		# #BOTTOM RIGHT
		# if(self.row < self.total_rows-1 and self.col < self.total_rows-1 and not grid[self.row+1][self.col+1].is_barrier()):
		# 	self.neighbors.append(grid[self.row+1][self.col+1])



	#less than method for Spot class
	def __lt__(self, other):
		return False



#h function. we use manhattan distance
def h(p1, p2):

	x1,y1 = p1
	x2,y2 = p2

	#return abs(x1-x2)+abs(y1-y2)
	return math.sqrt((x1-x2)**2 + (y1-y2)**2)

def reconstruct_path(came_from, current, draw):

	while current in came_from:
		current = came_from[current] 
		current.make_path()
		draw()
		

def astar(draw, grid, start, end):

	#to break ties when we have same F score
	count = 0

	open_set = PriorityQueue()
	#contains elements of the type [F-score, count, Node]
	open_set.put((0,count,start))

	#keep track of the path
	came_from = {}

	g_score = {spot : float("inf") for row in grid for spot in row}
	g_score[start] = 0

	f_score = {spot : float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	#this set is basically to keep track of the items in the prioq
	open_set_hash = {start}

	while not open_set.empty():

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		#[2] is the actual node
		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			start.make_start()
			end.make_end() 
			return True

		for neighbor in current.neighbors:

			temp_g_score = g_score[current]+1

			if(temp_g_score < g_score[neighbor]):

				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score

				f_score[neighbor] = temp_g_score+h(neighbor.get_pos(), end.get_pos())

				if(neighbor not in open_set_hash):
					count +=1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()
		draw()

		if current != start:
			current.make_closed()

	# font  = pygame.font.Font(None, 50)
	# text = font.render("NO PATH", True, RED)
	# text_rect = text.get_rect()
	# text_x = WINDOW.get_width() / 2 - text_rect.width / 2
	# text_y = WINDOW.get_height() / 2 - text_rect.height / 2
	# WINDOW.blit(text, [text_x, text_y])
	# pygame.display.flip()

	#return False 

#Code up the other algorithms

def djikstras(draw, grid, start, end):
	
	count = 0

	min_heap = PriorityQueue()
	#contains elements of the type [F-score, count, Node]
	min_heap.put((0,count,start))
	min_heap_set = {start}
	#visited = [[0 for i in range(len(grid))] for j in range(len(grid))]
	visited = {start}
	#keep track of the path
	came_from = {}

	distance = {spot : float("inf") for row in grid for spot in row}
	distance[start] = 0


	while(not min_heap.empty()):

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()


		current = min_heap.get()[2]
		min_heap_set.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw)
			start.make_start()
			end.make_end() 
			return True

		for neighbor in current.neighbors:

			temp_distance = distance[current]+1
			
			if(temp_distance < distance[neighbor]):

				came_from[neighbor] = current
				distance[neighbor] = temp_distance

				if(neighbor not in min_heap_set):
					count +=1
					min_heap.put((distance[neighbor],count, neighbor))
					min_heap_set.add(neighbor)
					neighbor.make_open()

		draw()

		if(current!= start):
			current.make_closed()


	return False



def breadthfirstsearch(draw, grid, start, end):
	
	count = 0

	q = Queue()
	qset = {start}

	q.put(start)

	came_from = {}

	while(not q.empty()):

		for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()

		n = q.qsize()

		for i in range(n):

			current = q.get()

			if(current == end):
				reconstruct_path(came_from, end, draw)
				start.make_start()
				end.make_end()
				return True

			for neighbor in current.neighbors:

				if(neighbor not in qset):
					q.put(neighbor)
					neighbor.make_open()
					qset.add(neighbor)
					came_from[neighbor] = current

			draw()

			if(current!=start):
				current.make_closed()

	return False


#Create Random Maze to test

def create_random_maze(grid, density):
	
	if(density=="low"):
		p=100
	elif(density == "medium"):
		p=500
	else:
		p=1000


	for i in range(p):

		r = random.randrange(len(grid))
		c = random.randrange(len(grid))

		grid[r][c].make_barrier()


def make_grid(rows, width):
	grid = []
	#gap is basically the width of each small cube 
	gap = width//rows

	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot =  Spot(i,j, gap, rows)
			grid[i].append(spot)

	return grid

#function to draw the grid lines between cubes
def draw_grid(win, rows, width):

	gap = width//rows

	for i in range(rows):

		pygame.draw.line(win, GREY, (0,i*gap),(width, i*gap))
		for j in range(rows):

			pygame.draw.line(win, GREY, (j*gap, 0),(j*gap, width))


def draw(win, grid, rows, width):

	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)

	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width//rows

	y,x = pos

	row = y//gap
	col = x//gap

	return row, col


def main(win, width):

	ROWS = 50

	grid = make_grid(ROWS, width)

	start = None
	end = None

	run = True
	started = False

	while run:
		#looping through all the events that have happened

		draw(win, grid, ROWS, width)
		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				run = False

				#left click
			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			#right click
			elif pygame.mouse.get_pressed()[2]:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]

				spot.reset()

				if spot == start:
					start = None
				elif spot == end:
					end = None

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_b and start and end:

					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					breadthfirstsearch(lambda : draw(win, grid, ROWS, width), grid, start, end) 

				if event.key == pygame.K_a and start and end:

					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					astar(lambda : draw(win, grid, ROWS, width), grid, start, end) 

				if event.key == pygame.K_d and start and end:

					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)

					djikstras(lambda : draw(win, grid, ROWS, width), grid, start, end)

				if event.key == pygame.K_r:

					# for row in grid:
					# 	for spot in row:
					# 		spot.update_neighbors(grid)

					create_random_maze(grid, "medium")

				if event.key == pygame.K_c:

					start = None
					end = None
					grid  =make_grid(ROWS, width)




	pygame.quit()



main(WINDOW, WIDTH)




