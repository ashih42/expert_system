# expert_system
A [backward-chaining](https://en.wikipedia.org/wiki/Backward_chaining) [expert system](https://en.wikipedia.org/wiki/Expert_system) in Python using [lark-parser](https://github.com/lark-parser/lark). (42 Silicon Valley)

<p float="left">
  <img src="https://github.com/ashih42/expert_system/blob/master/Screenshots/and_or.png" width="500" />
</p>

* **Variables** are single-letter upper-case alphabets.
* **Variables** not defined/inferred to be ***TRUE*** are assumed ***FALSE***.
* **Rules** are lazily evaluated when needed.

## Prerequisites

You have `python3` and `graphviz` installed.

## Installing

```
./setup/setup.sh
```

* **Note:** If you get the error `ImportError: cannot import name 'Lark' from 'lark'`, it's because you had also installed `lark` besides `lark-parser`.  To fix the problem, uninstall both and reinstall `lark-parser`.
```
pip3 uninstall lark lark-parser
pip3 install lark-parser
```

## Running

### Interactive Mode
```
python3 main.py
```

### File-processing Mode
```
python3 main.py -f file
```

### Basic Operations

* Define **facts** (variables given to be TRUE)
  * e.g. `=AB`
* Define a **rule**
   * e.g. `A + B => C`
* Query **variables**
  * e.g. `?ABC`

### Useful Commands

* `@info` Display all rules and facts.
* `@del n` Delete rule at index `n`.
* `@verbose on|off` Toggle verbose.
* `@vis`Produce a knowledge graph as PDF file.
* `@reset` Reset the system.
* `EXIT` Terminate the system.
