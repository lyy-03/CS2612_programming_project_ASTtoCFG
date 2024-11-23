# CS2612 Course Project (Programming part)

## Introduction
The project aims to generate a control flow graph (cfg) from the AST of WhileDB language introduced in the lesson.  
The project is completed independently by Yiyang Li.  
The project uses Python, version 3.12.  

## Code Structure 
There are four code files in the project, in which  
- `my_ast.py` defines the AST type, especially classifying all possible statements in WhileDB and processing them respectively.
- `cfg.py` defines and processes the CFGNode and CFG type, helping to create and maintain the control flow graph based on the AST of WhileDB language.
- `visualize.py` introduces the Graphviz package to help display the generated cfg to user.
- `main.py` is the main python file where you can give an AST example and get the cfg result.
  
## Usage
1. Download the correct version of `Graphviz` from the website https://graphviz.org/download/  and install according to the instruction.  
2. Add the path of `Graphviz` to the environment path of your OS. In Windows, it is usually `C:\Program Files\Graphviz\bin`.
3. Ensure you have correctly installed python (version >= 3.10).
4. Open the terminal, cd to the project's folder.
5. run `pip install graphviz`.
6. run `python main.py`.
7. The cfg is shown in the pdf file `cfg.pdf`.

You can change the value of `ast` in `main.py` to test different ASTs.