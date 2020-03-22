"""
Figuring out how binary numbers work in Python
one = 0b1
two = 0b10
three = 0b11
four = 0b100
five = 0b101
six = 0b110
seven = 0b111
eight = 0b1000
nine = 0b1001
ten = 0b1010
eleven = 0b1011
twelve = 0b1100
"""

import time

def main():
    
    start_time = time.time()
    a = 0b1
    a = a << 41
    
    b = 0b1
    b = b << 34
     
    a = a | b
    
    b = 0b1
    b = b << 27
     
    a = a | b
    
    b = 0b1
    b = b << 20
     
    a = a | b
    
    b = 0b1
    b = b << 13
     
    a = a | b
    
    b = 0b1
    b = b << 6
     
    a = a | b
    
    print(bin(a).count('1'))    
    print("{0:b}".format(a))

    print(time.time() - start_time)
    
if __name__ == '__main__':
    main()