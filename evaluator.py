from lark import Lark, Transformer, v_args
from colorama import Fore, Back, Style

from file_to_string import file_to_string
import expert_system

class Evaluator:

	def __init__(self):
		grammar = file_to_string('grammars/evaluator.lark')
		self.__lark_parser = Lark(grammar, parser='lalr', transformer=Evaluator.MyTransformer())

	def eval(self, statement):
		return self.__lark_parser.parse(statement)

	@v_args(inline=True)	# Affects the signatures of the methods
	class MyTransformer(Transformer):

		def __init__(self):
			pass

		def xor_op(self, a, b):
			return a ^ b

		def or_op(self, a, b):
			return a or b

		def and_op(self, a, b):
			return a and b

		def not_op(self, a):
			return not a

		def resolve_var(self, token):
			var = token.value
			return expert_system.ExpertSystem.instance.resolve_var(var)

