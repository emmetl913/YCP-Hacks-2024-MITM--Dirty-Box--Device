b = 'exec("print("Hello, world!"); print("This is an example of exec()"))"'

def convertToKeystroker(string):
    s  = ''
    for char in string:
        if char == '"':
            s += '\\"'
          
        elif char == '\n':
            s+= "\\\\n"
          
        else:
            s+= char
            
        print(s)
    return s
        
print(convertToKeystroker(b))
#exec()