# Fantastic Matrix Language Interpreter

This is the project for Compilation Techniques course. FML is a programming language with built-in matrix type.

## Installation

No need to install. Just download it or clone the repository.  
Minimum version of Python required to run interpreter is 3.8 (because of the `:=` Assignment Expressions).

## Usage


```python
python fmli.py file/to/interpret
```

You can also add flag `-d` (or `--dump`) to dump text AST of the program.

## Example

Here is an example of how you may program factorial in FML.

```code
fun factorial(n) {
  if (n < 2)
    ret 1;
  else
    ret n * factorial(n-1);
}

print(factorial(10));
```

Dumped AST of the code above:

```console
Program
|-FunctionDefinition: factorial
| |-Identifier: n
| `-CompoundStatement
|   `-IfStatement
|     |-BinaryOperator: <
|     | |-Identifier: n
|     | `-Scalar: 2.0
|     |-ReturnStatement
|     | `-Scalar: 1.0
|     `-ReturnStatement
|       `-BinaryOperator: *
|         |-Identifier: n
|         `-FunctionCall: factorial
|           `-BinaryOperator: -
|             |-Identifier: n
|             `-Scalar: 1.0
`-FunctionCall: print
  `-FunctionCall: factorial
    `-Scalar: 10.0
```

You can find more examples in `examples` folder.

