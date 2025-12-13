from login import Login_function
from signup import Signup




opt = input('please enter option: ')

match opt:
    case "1":
        Signup()
    case _:
        print('invalid')

