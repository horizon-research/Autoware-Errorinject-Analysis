import os
import pdb

def main():
    for i in range(500):
        #cmd = './Traceme x'+str(i)+'.txt'
        cmd = './qsort prelist'+str(i)+'.txt postlist'+str(i)+'.txt'
        os.system(cmd)
    f = open('pid.txt','w')
    f.write('-1')
    f.close()
if __name__ == '__main__':
    main()

