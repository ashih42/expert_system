from graphviz import Digraph
from lark import Lark, Transformer, v_args
from colorama import Fore, Back, Style
import os

from rule import Rule
from file_to_string import file_to_string

class Visualizer:
	__GRAPHS_DIR = 'graphs'

	def __init__(self):
		grammar = file_to_string('grammars/visualizer.lark')
		self.__lark_parser = Lark(grammar, parser='lalr', transformer=Visualizer.MyTransformer(self))
		self.__file_count = 0
		self.__delete_old_graphs()

	# Do not delete hidden ._* files, as they will be removed when the originals are removed
	def __delete_old_graphs(self):
		base_path = os.path.dirname(__file__)
		graphs_path = os.path.join(base_path, Visualizer.__GRAPHS_DIR)
		
		if os.path.exists(graphs_path) and os.path.isdir(graphs_path):
			for f in os.listdir(graphs_path):
				if not f.startswith('._'):
					f = os.path.join(graphs_path, f)
					os.remove(f)
		else:
			os.mkdir(graphs_path)

	def visualize(self, rules, facts, inferred_facts):
		self.dot = Digraph()
		self.node_count = 0		# for giving nodes unique identifiers while processing rules

		filename = 'graph_%05d.gv' % self.__file_count
		base_path = os.path.dirname(__file__)
		file_path = os.path.join(base_path, Visualizer.__GRAPHS_DIR, filename)
		self.__file_count += 1

		# process all rules
		for rule in rules:
			node_id = self.__lark_parser.parse(rule.lhs)
			for var in rule.rhs:
				self.dot.node(var, var, shape='box')
				self.dot.edge(node_id, var)

		# process all facts
		for var in sorted(facts):
			self.dot.node(var, var, shape='box', color='green')

		# process all inferred facts
		for var in sorted(inferred_facts):
			self.dot.node(var, var, shape='box', color='green')

		# save graphviz .gv file
		with open(file_path, 'w') as file:
			file.write(self.dot.source)

		# produce and open pdf
		self.dot.render(file_path, view=True)


	@v_args(inline=True)	# Affects the signatures of the methods
	class MyTransformer(Transformer):

		def __init__(self, visualizer):
			self.__visualizer = visualizer

		def xor_op(self, a, b):
			self.__visualizer.node_count += 1
			node_id = 'xor %05d' % self.__visualizer.node_count
			self.__visualizer.dot.node(node_id, 'xor')
			self.__visualizer.dot.edge(a, node_id, arrowhead='box')
			self.__visualizer.dot.edge(b, node_id, arrowhead='box')
			return node_id

		def or_op(self, a, b):
			self.__visualizer.node_count += 1
			node_id = 'or %05d' % self.__visualizer.node_count
			self.__visualizer.dot.node(node_id, 'or')
			self.__visualizer.dot.edge(a, node_id, arrowhead='box')
			self.__visualizer.dot.edge(b, node_id, arrowhead='box')
			return node_id

		def and_op(self, a, b):
			self.__visualizer.node_count += 1
			node_id = 'and %05d' % self.__visualizer.node_count
			self.__visualizer.dot.node(node_id, 'and')
			self.__visualizer.dot.edge(a, node_id, arrowhead='box')
			self.__visualizer.dot.edge(b, node_id, arrowhead='box')
			return node_id

		def not_op(self, a):
			self.__visualizer.node_count += 1
			node_id = 'not %05d' % self.__visualizer.node_count
			self.__visualizer.dot.node(node_id, 'not')
			self.__visualizer.dot.edge(a, node_id, arrowhead='box')
			return node_id

		def parse_var(self, token):
			var = token.value
			self.__visualizer.dot.node(var, var, shape='box')
			self.__visualizer.node_count += 1
			return var
