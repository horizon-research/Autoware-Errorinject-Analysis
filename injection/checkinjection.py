import os
import pdb
import time

def main():
    for i in range(200):
        filename = 'x' + str(i) + '.txt'
        f = open(filename,'r')
        a = f.readlines()
        if len(a) != 1000000:
            print(filename+'length diff')
        for j in range(len(a)):
            if j+1 != float(a[j]):
                print(filename+'sdc @'+str(j))
                break

if __name__ == '__main__':
    main()
