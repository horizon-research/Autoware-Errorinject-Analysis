import os
import math
import pdb

def main():
    f = open('lidartime/lidar.txt')
    latency = 0
    a = f.readlines()
    for i in range(len(a)):
        #pdb.set_trace()
        print(i)
        if float(a[i]) < 0.1:
            latency += float(a[i])*10
        else:
            latency += float(a[i])
    latency = latency/len(a)
    print(latency)

if __name__ == '__main__':
    main()