from login import Login_function

opt = input('please enter option')

match opt:
    case "1":
        Login_function()

    case _:
        print('invalid')
