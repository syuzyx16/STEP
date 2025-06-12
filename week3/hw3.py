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

def read_left(line, index):
    token ={'type':'LEFT'}
    return token, index + 1

def read_right(line, index):
    token ={'type':'RIGHT'}
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
        elif line[index] == '(':
            (token, index) = read_left(line, index)
        elif line[index] == ')':
            (token, index) = read_right(line, index)
        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


def four_op(tokens): # calculate inside of ()
    answer = 0
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token 
    index = 0  
    new_tokens=[]
    # firstly, turn * and / with numbers into one number 
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER' or tokens[index]['type'] == 'PLUS' or tokens[index]['type'] == 'MINUS':
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

def bracket_count(tokens):
    index = 0
    count =0
    while index < len (tokens):
        if tokens[index]['type'] == "LEFT":
            count += 1
        index +=1 
    return count 
         
 
def evaluate(tokens): #()の内部をevaluateで計算、numberへ転換
    
    count_bracket = bracket_count(tokens)
    new_tokens = tokens
    while count_bracket :
        new_tokens = []
        index = 0
        while index < len (tokens):   # (  ()  ()  )の場合、並列の括弧をまず処理 、次のwhile loopで、より大きな括弧を処理
            if tokens[index]['type'] == "LEFT":
                new_tokens.append(tokens[index]) 
                left_latest = len(new_tokens)-1  # new_tokensでの"("のindexを記録
                latest_is_left = True  # 最も新しい括弧が左
            elif tokens[index]['type'] == "RIGHT":
                if latest_is_left :
                    part_answer = four_op(new_tokens[left_latest+1:])  # 括弧の間にある式を計算
                    del new_tokens[left_latest:] #　"("とその後を消し、数値を入れ
                    new_number = {'type': 'NUMBER', 'number': part_answer}
                    new_tokens.append(new_number)
                    count_bracket -= 1   # 計算済みの括弧を総和から減らす
                else :
                    new_tokens.append(tokens[index]) 
                latest_is_left = False  # 最も新しいのは右
            else:
                new_tokens.append(tokens[index])   
            index += 1
        tokens = new_tokens
    return four_op(new_tokens)
    

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
    
    #for ()
    test("(2)")
    test("(2+1)")
    test("((2+1)*(2.1+1.1)+(1+2))*2")
    print("==== Test finished! ====\n")
    

run_test()


while True:
    print('> ', end="")
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)