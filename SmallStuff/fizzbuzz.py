x = 0

for i in range(100):
    x+=1 
    if x % 5 == 0 and x % 3 ==0:
        print("FizzBuzz")
    elif x % 3 == 0:
        print("Fizz")
    elif x % 5 == 0:
        print("Buzz")
    else:
        print(str(x))