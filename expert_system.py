from colorama import Fore, Back, Style
from os import system

from rule import Rule
from parser import Parser
from evaluator import Evaluator
from visualizer import Visualizer
from exceptions import ParserException, ExpertSystemException

class ExpertSystem:
	instance = None

	def __init__(self):
		if ExpertSystem.instance is None:
			ExpertSystem.instance = self
			self.__parser = Parser()
			self.__evaluator = Evaluator()
			self.__visualizer = Visualizer()
			self.__rules = []
			self.__facts = set()
			self.__inferred_facts = set()
			self.__is_verbose = False
		else:
			raise ExpertSystemException('ExpertSystem.instance already instantiated')

	def process_statement(self, statement):
		try:
			self.__parser.parse(statement)
		except RecursionError as e:
			print(Style.BRIGHT + Fore.RED + 'RecursionError: ' + Style.RESET_ALL + Fore.RESET + str(e))
		except ParserException as e:
			print(Style.BRIGHT + Fore.RED + 'ParserException: ' + Style.RESET_ALL + Fore.RESET + str(e))
		except ExpertSystemException as e:
			print(Style.BRIGHT + Fore.RED + 'ExpertSystemException: ' + Style.RESET_ALL + Fore.RESET + str(e))

	def process_queries(self, vars):
		self.__inferred_facts.clear()
		for var in vars:
			if self.__is_verbose:
				print('\nquerying ' + Fore.BLUE + var + Fore.RESET + ' = ?')
			value = self.resolve_var(var)
			print(Fore.BLUE + var + Fore.RESET + ' = ' + (Fore.GREEN if value else Fore.RED) + str(value) + Fore.RESET)

	def resolve_var(self, var):
		# Check the given knowledge base
		if var in self.__facts:
			return True

		# Check newly inferred facts so far
		if var in self.__inferred_facts:
			return True

		# Scan all rules, see if any infers this var
		for rule in self.__rules:
			if var in rule.rhs:
				if self.__is_verbose:
					print('Processing rule: ' + str(rule))
				if self.__evaluator.eval(rule.lhs):
					for rhs_var in rule.rhs:
						self.__add_inferred_fact(rhs_var)
					return True

		# Assume it's false ¯\_(ツ)_/¯
		return False

	def set_verbose(self, is_verbose):
		self.__is_verbose = is_verbose
		print(Style.BRIGHT + 'VERBOSE ' + Style.RESET_ALL + ('on' if self.__is_verbose else 'off'))

	def add_rule(self, lhs, rhs):
		rule = Rule(lhs, rhs)
		if self.__is_verbose:
			print('Added rule: ', rule)
		self.__rules.append(rule)
		self.__inferred_facts.clear()

	def del_rule(self, index):
		if not index in range(len(self.__rules)):
			raise ExpertSystemException('No rule at index %d' % index)
		print('Deleted rule: %s' % self.__rules[index])
		del self.__rules[index]
		self.__inferred_facts.clear()
	
	def set_facts(self, vars):
		self.__facts.clear()
		for var in vars:
			self.__facts.add(var)
		self.__inferred_facts.clear()

		if self.__is_verbose:
			print(Style.BRIGHT + '[FACTS]' + Style.RESET_ALL)
			for var in sorted(self.__facts):
				print(Fore.BLUE + var + Fore.RESET + ' = ' + Fore.GREEN + str(True) + Fore.RESET)
			print()
		
	def __add_inferred_fact(self, var):
		if var not in self.__facts and var not in self.__inferred_facts:
			self.__inferred_facts.add(var)
			if self.__is_verbose:
				print('Inferred new fact: ' + Fore.BLUE + var + Fore.RESET + ' = ' + Fore.GREEN + str(True) + Fore.RESET)

	def show_info(self):
		print(Style.BRIGHT + '[RULES]' + Style.RESET_ALL)
		for index, rule in enumerate(self.__rules):
			print('%d:\t %s' % (index, rule))
		print()

		print(Style.BRIGHT + '[FACTS]' + Style.RESET_ALL)
		for var in sorted(self.__facts):
			print(Fore.BLUE + var + Fore.RESET + ' = ' + Fore.GREEN + str(True) + Fore.RESET)
		print()

		print(Style.BRIGHT + '[INFERRED FACTS]' + Style.RESET_ALL)
		for var in sorted(self.__inferred_facts):
			print(Fore.BLUE + var + Fore.RESET + ' = ' + Fore.GREEN + str(True) + Fore.RESET)
		print()

	def visualize(self):
		self.__visualizer.visualize(self.__rules, self.__facts, self.__inferred_facts)

	def reset(self):
		self.__rules.clear()
		self.__facts.clear()
		self.__inferred_facts.clear()
		print(Fore.MAGENTA + 'Expert System has been reset' + Fore.RESET)

	def dance(self):
		dance_str = r'''(_＼ヽ
　 ＼＼ .Λ＿Λ.
　　 ＼(　ˇωˇ)　
　　　 >　⌒ヽ
　　　/ 　 へ＼
　　 /　　/　＼＼
　　 ﾚ　ノ　　 ヽ_つ
　　/　/
　 /　/|
　(　(ヽ
　|　|、＼
　| 丿 ＼ ⌒)
　| |　　) /
`ノ ) 　 Lﾉ
(_／'''
		print(dance_str)

	# Source: https://github.com/thiderman/doge
	def doge(self):
		system('doge')

