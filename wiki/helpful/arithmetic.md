# Arithmetic Operators

With the Arithmetic Operators it is possible to use simple mathematics in SQL Builder.

You can find more information about these operators here https://mariadb.com/kb/en/arithmetic-operators/

## Supported Operators

- Addition ``+``
- Subtraction ``-``
- Multiplication ``*``
- Division ``/``
- Modulo ``%``

## Usage

Initialise an Arithmetic class

The class accept follow types of variables in each step

- Arithmetic
- ArithmeticColumn
- Integer and Float

````python
from mariadb_sqlbuilder.helpful.arithmetic import Arithmetic

arithmetic = Arithmetic(100)
````

### Addition

````python
arithmetic.add(100)
````

### Subtraction

````python
arithmetic.sub(100)
````
### Multiplication

````python
arithmetic.mul(100)
````
### Division

````python
arithmetic.div(100)
````
### Modulo

````python
arithmetic.mod(50)
````

------
The class Arithmetic are repeatable

````python
arithmetic.sub(100).mul(2).add(200)
````

-----

## Calculations with brackets
Parenthesis calculation is possible, for this you can simply specify an arithmetic class 
with the parenthesis values for the variables, this is always repeatable.

### Example
````python
arithmetic.mul(Arithmetic(200).add(100))
````


# ArithmeticColumn
ArithmeticColumn is a class to specify a column for an arithmetic operation instead of a number.

This requires a Table and a Column

### Example

````python
ac = ArithmeticColumn(table, column)

# with custom parameters
ac = ArithmeticColumn("user", "money")
````


### Example usage

````python
arithmetic = Arithmetic(ArithmeticColumn("user", "money"))
arithmetic.mul(0.95)
````