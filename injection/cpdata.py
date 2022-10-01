import os
import time

def main():
    for i in range(100):
        cmd = 'docker cp d71922ccb4f3:/home/autoware/base0126/baseline' + str(i) + '.zip .'
        os.system(cmd)
if __name__ == '__main__':
    main()