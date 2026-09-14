import random
import copy
import sys
from time import sleep
with open('Replay4K.txt','w') as file:
	file.write('')
pdfweight = [[65536,32768,16384,16],[8192,4096,2048,8],[1024,512,256,4],[128,64,32,2]]
for row in pdfweight:
	for col in row:
		col **= 2
snakeweight = [[65536,32768,16384,8192],[512,1024,2048,4096],[256,128,64,32],[2,4,8,16]]
def ismono(row):
	row2 = [x for x in row if x != 0]
	if row2 == sorted(row2) or row2[::-1] == sorted(row2):
		penalty = 0
	else:
		penalty = pdfweight[0][0] / 1000 * sum(row2)
	return penalty
def rotate(matrix):
	for idx in range(len(matrix)):
		for jdx in range(idx,len(matrix)):
			matrix[idx][jdx],matrix[jdx][idx] = matrix[jdx][idx],matrix[idx][jdx]
	for list in range(len(matrix)):
		matrix[list].reverse()
def flip(matrix):
	for idx in range(len(matrix)):
		matrix[idx].reverse()
class Game:
	def __init__(inst,gridx,gridy):
		inst.grid = []
		inst.temp = []
		inst.gridx = gridx
		inst.gridy = gridy
		inst.score = 0
		for i in range(inst.gridx):
			inst.temp.append(0)
		for i in range(inst.gridy):
			inst.grid.append(inst.temp.copy())
		inst.spawn()
		inst.spawn()
	def __str__(inst):
		x = ''
		for row in inst.grid:
			x += str(row)
			x += '\n'
		x += str(inst.score)
		return x
	def spawn(inst):
		completed = False
		while not completed:
			rx = random.randint(0,inst.gridx-1)
			ry = random.randint(0,inst.gridy-1)
			det = random.random()
			if det > 0.9:
				tile = 4
			else:
				tile = 2
			if inst.grid[rx][ry] == 0:
				inst.grid[rx][ry] = tile
				completed = True
	def test(inst,alg,trials=1):
		if alg == 'random':
			return random.choice(['left','right','up','down'])
		elif alg == 'scorert':
			testls = []
			movetestls = []
			for move in ['left','right','up','down']:
				for moveb in ['left','right','up','down']:
					a = inst.movetest(move)
					b = a.movetest(moveb)
					scoretotal = a.score + b.score
					testls.append(scoretotal)
					movetestls.append(move)
			helper = testls.index(max(testls))
			return movetestls[helper]
		elif alg == 'newrt':
			testls = []
			movetestls = []
			for move in ['left','right','up','down']:
				for moveb in ['left','right','up','down']:
					score = 0
					a = inst.movetest(move)
					b = a.movetest(moveb)
					for idx,row in enumerate(b.grid):
						#score += ismono(row)
						for jdx,col in enumerate(row):
							score += (col * pdfweight[idx][jdx])
					if a.grid != inst.grid:
						testls.append(score)
						movetestls.append(move)
			helper = testls.index(max(testls))
			return movetestls[helper]
	def movetest(inst,dir):
		test = copy.deepcopy(inst)
		test.score = 0
		if dir == 'up' or dir == 'down':
			rotate(test.grid)
		if dir == 'right' or dir == 'up':
			flip(test.grid)
		for idx,row in enumerate(test.grid):
			new = []
			for jdx,col in enumerate(row):
				if col != 0:
					new.append(col)
			for kdx,ele in enumerate(new):
				if kdx > 0:
					try:
						if new[kdx] == new[kdx-1]:
							new[kdx-1] += new[kdx]
							test.score += new[kdx-1]
							new.pop(kdx)
					except:
						pass
			while len(new) < inst.gridx:
				new.append(0)
			test.grid[idx] = new.copy()
		if dir == 'right' or dir == 'up':
			flip(test.grid)
		if dir == 'up' or dir == 'down':
			rotate(test.grid)
			rotate(test.grid)
			rotate(test.grid)
#		if test.grid != inst.grid:
#			test.spawn()
		return test
	def move(inst,dir):
		test = copy.deepcopy(inst.grid)
		if dir == 'up' or dir == 'down':
			rotate(inst.grid)
		if dir == 'right' or dir == 'up':
			flip(inst.grid)
		for idx,row in enumerate(inst.grid):
			new = []
			for jdx,col in enumerate(row):
				if col != 0:
					new.append(col)
			for kdx,ele in enumerate(new):
				if kdx > 0:
					try:
						if new[kdx] == new[kdx-1]:
							new[kdx-1] += new[kdx]
							inst.score += new[kdx-1]
							new.pop(kdx)
					except:
						pass
			while len(new) < 4:
				new.append(0)
			inst.grid[idx] = new.copy()
		if dir == 'right' or dir == 'up':
			flip(inst.grid)
		if dir == 'up' or dir == 'down':
			rotate(inst.grid)
			rotate(inst.grid)
			rotate(inst.grid)
		if test != inst.grid:
			inst.spawn()
	def interactive(inst):
		global end
		try:
			operation = inst.test('newrt')
		except:
			end = True
			with open('Replay4K.txt','a') as file:
				file.write('Gameover')
			print(inst)
			return
		if operation in ['left','right','up','down']:
			inst.move(operation)
		if operation == 'quit':
			sys.exit()
		with open('Replay4K.txt','a') as file:
			file.write(str(inst))
			file.write('\n')
			file.write(str(inst.score))
			file.write('\n')
end = False
a = Game(4,4)
with open('Replay4K.txt','a') as file:
	file.write(str(a.gridx))
	file.write('\n')
	file.write(str(a.gridy))
	file.write('\n')
print(a)
while True:
	a.interactive()
	if end:
		break