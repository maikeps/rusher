# coding: utf-8

class Graph:
	def __init__(self, is_oriented):
		self.is_oriented = is_oriented
		self.nodes = {}

	def add_node(self, node):
		self.nodes.update({node.name : node})

	def remove_node(self, node_name):
		# del_node = self.nodes[node_name]
		del_node = self.get(node_name)
		del self.nodes[node_name]
		
		if not is_oriented:
			for node in self.nodes:
				node.remove_neighbour(del_node)

		return del_node

	def connect(self, node1_name, node2_name):
		node1 = self.get(node1_name)
		node2 = self.get(node2_name)
		# node1 = self.nodes[node1_name]
		# node2 = self.nodes[node2_name]

		node1.add_neighbour(node2)
		if not self.is_oriented: node2.add_neighbour(node1)

	def disconnect(self, node1_name, node2_name):
		node1 = self.get(node1_name)
		node2 = self.get(node2_name)
		# node1 = self.nodes[node1_name]
		# node2 = self.nodes[node2_name]

		node1.remove_neighbour(node2)
		if not self.is_oriented: node2.remove_neighbour(node1)

	def get(self, node_name):
		return self.nodes[node_name]

	def print_graph(self):
		for item in self.nodes:
			node = self.get(item)
			if not self.predecessors(node.name):
				print("("+ node.name + ") " + node.info[0])
			for next_node in self.predecessors(node.name):
				print("("+ node.name + ") " + node.info[0] + " -> " +  "("+next_node+") " + self.get(next_node).info[0])

	# Search methods

	# (node1) -> (node2)
	# node1 is predecessor to node2
	# predecessors(node2) returns [node1]
	def predecessors(self, node_name):
		node = self.get(node_name)
		predecessors = []

		for item in self.nodes:
			node_aux = self.get(item)
			if node.name in node_aux.neighbours:
				predecessors.append(node_aux.name)
	
		return predecessors

	def successors(self, node_name):
		node = self.get(node_name)
		successors = []
		
		for item in self.nodes:
			if item in node.neighbours:
				successors.append(item)

		return successors

	def path_to_end(self, initial_node):
		return self.path_to_end_rec(initial_node, [])

	def path_to_end_rec(self, node_name, path):
		node = self.get(node_name)
		for next_node in self.predecessors(node_name):
			path.append(next_node)
			path = self.path_to_end_rec(next_node, path)
		return path

class Node:
	def __init__(self, name, info):
		self.name = name
		self.info = info

		self.neighbours = {}

	def add_neighbour(self, node):
		self.neighbours.update({node.name : node})

	def remove_neighbour(self, node_name):
		del self.neighbours[node_name]