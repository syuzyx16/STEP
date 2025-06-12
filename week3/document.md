## 1. Overview 

a simple calculator written by Python, for dealing with +, -, *, /, () and function abs, int and round, decimals can be read.


## 2. Structure
the calculator is composed of the following parts:

- **read** number/ operator/ function(string)

- **tokenizer**  make a list of dictionary which save the type of token and the value of it

- **four_op** can only calculate tokens including numbers and arithmetic operators, can not deal with '()' and functions

- **count_bracket** count the amount of '()'

- **evaluate** find the smallest '()'s within a loop, using four_op calculate the expression inside the '()' then turn expression and '()' into the result number of the expression, until all '()'s are cleaned, finally apply four_op to rested expression to get the final answer. 

- **test** apply eval function of python to get real answer and compare with the result got from **evaluate**


## 3. test case

test for ' + ' and ' - '

- 1+2
- 1.0+2.1-3
- 1.2+3

test for ' * ' and ' / '
- 1+2/3+2*3
- 1.0+2.1*3.2/4.3/2.5-4      continuous  ' * ' and ' / '

test for '()'
- (2)
- ((2))
- (2+1)
- ((2+1)*(2.1+1.1)+(1+2))*2
    
test for function
- 12+abs(int(round(-1.55)+abs(int(-2.3+4))))
- (int(abs(-1*(9-8/2))*(-1.5+3)+round(1.9)))*2 (cant pass this test, try to debug...)




