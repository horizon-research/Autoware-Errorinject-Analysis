import os
import time

def main():
    for i in range(100):
        cmd = 'rm baseline' + str(i) + '.zip .'
        os.system(cmd)
if __name__ == '__main__':
    main()