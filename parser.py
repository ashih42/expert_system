from lark import Lark, Transformer, v_args
from lark.exceptions import LarkError
from colorama import Fore, Back, Style

from exceptions import ParserException
from file_to_string import file_to_string
import expert_system

class Parser:

	def __init__(self):
		grammar = file_to_string('grammars/parser.lark')
		self.__lark_parser = Lark(grammar, parser='lalr', transformer=Parser.MyTransformer())

	def parse(self, statement):
		try:
			statement = statement.split('#')[0]			# remove comments
			if statement != '':
				self.__lark_parser.parse(statement)
		except LarkError as e:
			raise ParserException(e)

	@v_args(inline=True)	# Affects the signatures of the methods
	class MyTransformer(Transformer):

		def __init__(self):
			pass

		# TOP LEVEL OPERATIONS ------------------------------------------------

		def add_rule(self, lhs, rhs):
			expert_system.ExpertSystem.instance.add_rule(lhs, rhs)

		def set_facts(self, *args):
			expert_system.ExpertSystem.instance.set_facts(args)

		def query_vars(self, *args):
			expert_system.ExpertSystem.instance.process_queries(args)

		def show_info(self):
			expert_system.ExpertSystem.instance.show_info()

		def del_rule(self, index):
			expert_system.ExpertSystem.instance.del_rule(index)

		def verbose_on(self):
			expert_system.ExpertSystem.instance.set_verbose(True)

		def verbose_off(self):
			expert_system.ExpertSystem.instance.set_verbose(False)

		def visualize(self):
			expert_system.ExpertSystem.instance.visualize()

		def reset(self):
			expert_system.ExpertSystem.instance.reset()

		def dance(self):
			expert_system.ExpertSystem.instance.dance()

		def doge(self):
			expert_system.ExpertSystem.instance.doge()

		# LHS ------------------------------------------------

		def xor_op(self, a, b):
			return a + ' ^ ' + b

		def or_op(self, a, b):
			return a + ' | ' + b

		def and_op(self, a, b):
			return a + ' + ' + b

		def not_op(self, a):
			return '!' + a

		def parentheses(self, a):
			return '(' + a + ')'
		
		# RHS ------------------------------------------------

		def rhs_var(self, var):
			return [ var ]

		def rhs_and_var(self, rhs, var):
			rhs.append(var)
			return rhs

		# PARSING TOKENS ------------------------------------------------

		def parse_var(self, token):
			return token.value

		def parse_index(self, token):
			return int(token.value)

