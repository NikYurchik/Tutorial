result = None
operand = None
operator = None
wait_for_number = True

while True:
    print(f"operator = {operator}, result = {result}, wait_for_number = {wait_for_number}")
    if result == None:
        print("Start typing the expression")

    val = input()
    if val == '=':
        if not (operator == None):
            if not (result == None):
                print("Unfinished expression. Try again")
            continue
        break
        
    if wait_for_number:
        try:
            operand = float(val)
            if operator == None:
                result = operand
            elif operator == '+':
                result = result + operand
            elif operator == '-':
                result = result - operand
            elif operator =='*':
                result = result * operand
            elif operator == '/':
                result = result / operand
            operator = None
            wait_for_number = False
        except ValueError:
            print(f"'{val}' is not a number. Try again")
            continue
        except ZeroDivisionError:
            print("Division by Zero! Try again.")
            continue
    else:
        if val != '+' and val != '-' and val != '*' and val != '/':
            print(f"'{val}' is not '+' or '-' or '/' or '*'. Try again")
            continue
        operator = val
        wait_for_number = True


print(result)