#! /usr/bin/python3


def read_number(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        decimal = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * decimal
            decimal /= 10
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def read_plus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def read_minus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def read_multi(line,index):
    token ={'type':'MULTI'}
    return token, index + 1

def read_divide(line, index):
    token ={'type':'DIVIDE'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = read_number(line, index)
        elif line[index] == '+':
            (token, index) = read_plus(line, index)
        elif line[index] == '-':
            (token, index) = read_minus(line, index)
        elif line[index] == '*':
            (token, index) = read_multi(line, index)
        elif line[index] == '/':
            (token, index) = read_divide(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


def evaluate(tokens):
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token 
    index = 0  
    new_tokens=[]
    
    # firstly, turn * and / with numbers into one number 
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER' or tokens[index]['type']== 'PLUS' or tokens[index]['type'] =='MINUS':
            new_tokens.append(tokens[index])   
        elif tokens[index]['type'] == 'MULTI':
            new_number = {'type': 'NUMBER', 'number': new_tokens[-1]['number']*tokens[index+1]['number']}
            new_tokens.pop()
            new_tokens.append(new_number)
            index += 1
        elif tokens[index]['type'] == 'DIVIDE':
            new_number = {'type': 'NUMBER', 'number': new_tokens[-1]['number']/tokens[index+1]['number']}
            new_tokens.pop()
            new_tokens.append(new_number)
            index += 1
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        index += 1
   
    # then calculate + and -
    index = 1
    while index < len(new_tokens):
        if new_tokens[index]['type'] == 'NUMBER':
            if new_tokens[index - 1]['type'] == 'PLUS':
                answer += new_tokens[index]['number']
            elif new_tokens[index - 1]['type'] == 'MINUS':
                answer -= new_tokens[index]['number']
            else:
                print('Invalid syntax')
        index += 1
    return answer



def test(line):
    tokens = tokenize(line)
    actual_answer = evaluate(tokens)
    expected_answer = eval(line)
    if abs(actual_answer - expected_answer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expected_answer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expected_answer, actual_answer))


# Add more tests to this function :)
def run_test():
    print("==== Test started! ====")
    test("1+2")
    test("1.0+2.1-3")
    #for * and /
    test("1.0+2.1*3.2/4.3/2.5-4")
    
    print("==== Test finished! ====\n")
    

run_test()

while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)