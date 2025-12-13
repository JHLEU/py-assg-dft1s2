from login import Login_function
from signup import Signup




opt = input('please enter option: ')

match opt:
    case "1":
        Login_function(show_skip=False)  # call the class; no Skip button when called by others
    case _:
        print('invalid')

