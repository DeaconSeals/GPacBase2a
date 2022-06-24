from typing import Tuple, Sequence

import gpac
from collections import deque
import heapq
import random


class shortestPathPillAgent():
	def __init__(self):
		self.pre_planned_actions = deque()

	def select_action(self, game):
		if len(self.pre_planned_actions) == 0:
			self.pre_planned_actions = path_to_pill_a_star('m', game)

		return self.pre_planned_actions.popleft()

class shortestPathFruitAgent(shortestPathPillAgent):
	def select_action(self, game):
		if game.fruit_location is not None and len(self.pre_planned_actions) == 0:
			self.pre_planned_actions = path_to_fruit_a_star('m', game)
		return super().select_action(game)

def path_to_pill(player, game):
	'''Search for the shortest path to the nearest pill using BFGS'''
	if len(game.pills) == 0:
		return ['hold']
	visited = set()
	frontier = deque()
	frontier.append((game.players[player], deque()))
	possible_actions = list(gpac.GHOST_ACTIONS.items())
	while frontier:
		base_loc, base_actions = frontier.popleft()
		for action, shift in random.sample(possible_actions, len(possible_actions)):
			actions = base_actions.copy()
			actions.append(action)
			x, y = base_loc[0]+shift[0], base_loc[1]+shift[1]
			if 0 <= x < len(game.map) and 0 <= y < len(game.map[x]) and game.map[x][y]==0 and (x,y) not in visited:
				if (x,y) in game.pills:
					return actions
				else:
					frontier.append(((x,y), actions))
					visited.add((x,y))
	return ['hold'] # failsafe case

def path_to_fruit(player, game):
	'''Search for the shortest path to the fruit using BFGS'''	
	if game.fruit_location == None:
		return ['hold']
	visited = set()
	frontier = deque()
	frontier.append((game.players[player], deque()))
	possible_actions = list(gpac.GHOST_ACTIONS.items())
	while frontier:
		base_loc, base_actions = frontier.popleft()
		for action, shift in random.sample(possible_actions, len(possible_actions)):
			actions = base_actions.copy()
			actions.append(action)
			x, y = base_loc[0]+shift[0], base_loc[1]+shift[1]
			if 0 <= x < len(game.map) and 0 <= y < len(game.map[x]) and game.map[x][y]==0 and (x,y) not in visited:
				if (x,y) == game.fruit_location:
					return actions
				else:
					frontier.append(((x,y), actions))
					visited.add((x,y))
	return ['hold'] # failsafe case


# Sean's code past here
class RandomGhostAgent:
	"""A ghost that acts randomly."""
	def __init__(self):
		pass

	def select_action(self, game: gpac.GPacGame, player: str) -> str:
		"""player: the string identifier for this agent in the GPac game."""
		return random.choice(game.get_actions(player))


class ChasingGhostAgent:
	"""A ghost that efficiently follows Pac-man, with minor randomness to prevent ghosts from bunching up too much.
	TODO: Does not work for multiple Pac-mans."""
	def __init__(self, path_staleness_ratio=5, random_wander_chance=0.25):
		"""path_staleness_ratio: With a path_staleness_ratio of 5, Pac-man can be distance 1 away from the path target
			for each 5 distance of remaining path before the path must be recalculated.
		random_wander_chance: Probability of the ghost making a random move when it has no path, to break up ghosts."""

		self.path_staleness_ratio = path_staleness_ratio
		self.random_wander_chance = random_wander_chance
		self.path_target = None
		self.pre_planned_actions = None

	def select_action(self, game: gpac.GPacGame, player: str) -> str:
		"""player: the string identifier for this agent in the GPac game."""
		if self.path_target is None or len(self.pre_planned_actions) == 0 or self.path_staleness_check(game):
			if random.random() < self.random_wander_chance:
				self.path_target = None
				self.pre_planned_actions = None
				return random.choice(game.get_actions(player))
			else:
				self.pre_planned_actions = path_to_pacman(player, game)
				self.path_target = game.players['m']

		return self.pre_planned_actions.popleft()

	def path_staleness_check(self, game: gpac.GPacGame) -> bool:
		"""Returns True if the path needs to be recalculated.

		Pac-man can stray from its target by a certain fraction of the remaining path distance
		before the path is considered stale and needs to be recalculated.
		When close to pac-man, paths will need to be recalculated every turn, but this will be cheaper."""

		target_inaccuracy = manhattan_distance(self.path_target, game.players['m'])
		path_length = len(self.pre_planned_actions)
		return target_inaccuracy * self.path_staleness_ratio >= path_length


class AvoidingPacmanAgent(shortestPathFruitAgent):
	"""A Pac-man agent that will avoid being within a certain radius of ghosts."""

	def __init__(self, avoidance_radius=3, maximum_path_age=10, fruit_factor=4):
		"""avoidance_radius: The distance where Pac-man will consider itself too close to a ghost.
		maximum_path_age: The maximum time a path can be followed before it's recalculated
		fruit_factor: The extra length that Pac-man will travel to collect fruit."""

		super().__init__()
		self.avoidance_radius = avoidance_radius
		self.maximum_path_age = maximum_path_age
		self.fruit_factor = fruit_factor
		self.path_timestamp = None

	def select_action(self, game: gpac.GPacGame) -> str:
		ghosts = [location for player, location in game.players.items() if 'm' not in player]
		path_age = self.path_timestamp - game.time if self.path_timestamp is not None else 0  # Time is counting down, not up
		if nearest_manhattan_distance(game.players['m'], ghosts) <= self.avoidance_radius:
			self.pre_planned_actions = deque()
		if path_age > self.maximum_path_age:
			self.pre_planned_actions = deque()
		if game.fruit_location is not None and len(self.pre_planned_actions) == 0:
			fruit_path = path_to_fruit_a_star('m', game, ghost_proximity_cost_function)
			pill_path = path_to_pill_a_star('m', game, ghost_proximity_cost_function)
			if fruit_path[0] == 'hold':
				self.pre_planned_actions = pill_path
			elif pill_path[0] == 'hold':
				self.pre_planned_actions = fruit_path
			elif len(fruit_path) < len(pill_path) * self.fruit_factor and 2 * len(fruit_path) + len(pill_path) < game.time:
				self.pre_planned_actions = fruit_path
			else:
				self.pre_planned_actions = pill_path
			self.path_timestamp = game.time
		elif len(self.pre_planned_actions) == 0:
			self.pre_planned_actions = path_to_pill_a_star('m', game, ghost_proximity_cost_function)
			self.path_timestamp = game.time
		return self.pre_planned_actions.popleft()


def manhattan_distance(start: Tuple[int, int], end: Tuple[int, int]) -> int:
	return abs(start[0] - end[0]) + abs(start[1] - end[1])


def nearest_manhattan_distance(start: Tuple[int, int], ends: Sequence[Tuple[int, int]]) -> int:
	"""Manhattan distance to the nearest point in ends"""
	if len(ends) == 1:
		end, = ends
		return manhattan_distance(start, end)
	else:
		shortest_distance = None
		for end in ends:
			distance = manhattan_distance(start, end)
			if shortest_distance is None or distance < shortest_distance:
				shortest_distance = distance
		return shortest_distance


IMPOSSIBLE_COST = 1000000  # Arbitrary cost higher than any normal distance, as a failure case.


def identity_cost_function(point: Tuple[int, int], game: gpac.GPacGame) -> int:
	"""A cost function always equal to one."""
	return 1


def ghost_proximity_cost_function(point: Tuple[int, int], game: gpac.GPacGame, avoidance_radius=10) -> int:
	"""A cost function that increases as you get closer to ghosts."""
	ghosts = [location for player, location in game.players.items() if 'm' not in player]
	nearest_distance = nearest_manhattan_distance(point, ghosts)
	if nearest_distance == 0:
		return IMPOSSIBLE_COST  # A distance of 0 is a loss, so if this is the last option then just wait.
	elif nearest_distance == 1:
		return IMPOSSIBLE_COST // 10  # A distance of 1 is often a loss, but not always
	# Returning the square of the "closeness" to strongly discourage getting near ghosts if possible.
	return max(avoidance_radius - nearest_distance, 0) ** 2 + 1


def is_open(point: Tuple[int, int], game: gpac.GPacGame):
	"""Checks if a point is valid and open"""
	x, y = point
	return 0 <= x < len(game.map) and 0 <= y < len(game.map[x]) and game.map[x][y] == 0


class ExtremePathCostException(Exception):
	pass


def path_to_points(start: Tuple[int, int], ends: Sequence[Tuple[int, int]], game: gpac.GPacGame,
				   cost_function=identity_cost_function) -> deque:
	"""Calculates a path to the nearest end point of a set using A*.
	Tends to outperform BFS out to at least 30 endpoints."""
	possible_actions = list(gpac.GHOST_ACTIONS.items())
	frontier = [(nearest_manhattan_distance(start, ends), start)]  # Min-heap sorted by estimated distance to end (F in A*)
	path_distance = {start: 0}  # G in A*
	path_previous = dict()  # Previous node on path

	while len(frontier) > 0:
		estimated_cost, current = frontier[0]  # Smallest F
		if estimated_cost >= IMPOSSIBLE_COST:
			raise ExtremePathCostException("No safe path to target!")

		removed_current = False
		for action, direction in possible_actions:
			neighbor = current[0] + direction[0], current[1] + direction[1]
			if neighbor not in path_distance and is_open(neighbor, game):
				path_previous[neighbor] = current, action

				if neighbor in ends:  # Shortest path found!
					path = deque()  # List of directional actions
					path_traverse = neighbor
					while path_traverse != start:
						path_traverse, path_action = path_previous[path_traverse]
						path.appendleft(path_action)
					return path

				g = path_distance[current] + cost_function(neighbor, game)
				path_distance[neighbor] = g
				# Consistent heuristic, which simplifies A* as nodes will always be expanded in the right order
				f = g + nearest_manhattan_distance(neighbor, ends)
				if not removed_current:  # More efficient to remove current and replace in one step
					heapq.heapreplace(frontier, (f, neighbor))
					removed_current = True
				else:
					heapq.heappush(frontier, (f, neighbor))
		if not removed_current:
			heapq.heappop(frontier)


def path_to_point(start: Tuple[int, int], end: Tuple[int, int], game: gpac.GPacGame,
				  cost_function=identity_cost_function) -> deque:
	"""Calculates a path to a specific target using A*. Use BFS instead to find the nearest general object."""
	return path_to_points(start, (end,), game, cost_function)


def path_to_pill_a_star(player: str, game: gpac.GPacGame, cost_function=identity_cost_function) -> deque:
	"""Search for the shortest path to the nearest pill using A*."""
	if len(game.pills) > 30:
		return path_to_pill(player, game)  # Too many pills, might be better to use BFS

	try:
		return path_to_points(game.players[player], game.pills, game, cost_function)
	except ExtremePathCostException:
		return deque(('hold', ))


def path_to_fruit_a_star(player: str, game: gpac.GPacGame, cost_function=identity_cost_function) -> deque:
	"""Search for the shortest path to the fruit using A*"""
	if game.fruit_location is None:
		return deque(('hold', ))
	try:
		path = path_to_point(game.players[player], game.fruit_location, game, cost_function)
		return path
	except ExtremePathCostException:
		return deque(('hold', ))


def path_to_pacman(player: str, game: gpac.GPacGame) -> deque:
	"""Search for the shortest path to pac-man using A*. TODO: This needs to be updated for multiple pac-mans."""
	return path_to_point(game.players[player], game.players["m"], game)
