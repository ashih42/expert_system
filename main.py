from colorama import Fore, Back, Style
from os import getenv
from sys import argv
import readline

from expert_system import ExpertSystem

def terminate_with_usage():
	print(Style.BRIGHT + 'usage: ' + Style.RESET_ALL)
	print('python3 ' + Fore.BLUE + 'main.py ' + Fore.RESET + '-h \t\t\t (usage)')
	print('python3 ' + Fore.BLUE + 'main.py ' + Fore.RESET + '\t\t\t (start interactive session)')
	print('python3 ' + Fore.BLUE + 'main.py ' + Fore.RESET + '-f ' + Fore.CYAN + 'filename' + Fore.RESET +
		'\t\t (process input file)')
	print()

	print(Style.BRIGHT + '[CMMANDS]' + Style.RESET_ALL)
	print(Fore.BLUE + '@info' + Fore.RESET + "\t\t\t Display all rules and facts")
	print(Fore.BLUE + '@del index' + Fore.RESET + "\t\t Delete rule at index")
	print(Fore.BLUE + '@verbose on|off' + Fore.RESET + "\t\t Toggle verbose")
	print(Fore.BLUE + '@vis' + Fore.RESET + "\t\t\t Produce a complete graph pdf file")
	print(Fore.BLUE + '@reset' + Fore.RESET + "\t\t\t Reset the system")
	print(Fore.BLUE + '@dance' + Fore.RESET + '\t\t\t ¯\\_(ツ)_/¯')
	print(Fore.BLUE + '@doge' + Fore.RESET + '\t\t\t ¯\\_(ツ)_/¯')
	quit()

def interactive_loop(expert_system):
	prompt = getenv('ES_PROMPT')
	if prompt is None or prompt == '':
		prompt = '🍔 Enter statement: '
	while True:
		print()
		statement = input(prompt).strip()
		if statement.upper() == 'EXIT':
			break
		expert_system.process_statement(statement)

def process_file(expert_system, filename):
	with open(filename, 'r') as file:
		for line in file:
			statement = line.strip()
			if statement == '' or statement[0] == '#':
				print(Fore.MAGENTA + statement + Fore.RESET)
			else:
				expert_system.process_statement(statement)

def main():
	try:
		expert_system = ExpertSystem()

		# Interactive mode
		if len(argv) == 1:
			interactive_loop(expert_system)
		# Usage mode
		elif argv[1] == '-h':
			terminate_with_usage()
		# File-processing mode
		elif argv[1] == '-f':
			if len(argv) != 3:
				terminate_with_usage()
			filename = argv[2]
			process_file(expert_system, filename)
		# Nope mode
		else:
			terminate_with_usage()
	except IOError as e:
		print(Style.BRIGHT + Fore.RED + 'I/O Error: ' + Style.RESET_ALL + Fore.RESET + str(e))
	except EOFError as e:
		pass

if __name__ == '__main__':
	main()

