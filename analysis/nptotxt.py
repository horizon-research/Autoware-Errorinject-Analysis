import os
import numpy as np 
import pdb
def main():
    data = np.load('xpavg.txt.npy')
    pdb.set_trace()
    np.savetxt('xpavg.txt',data)
    data = np.load('ypavg.txt.npy')
    np.savetxt('ypavg.txt',data)
    data = np.load('zpavg.txt.npy')
    np.savetxt('zpavg.txt',data)
    data = np.load('xoavg.txt.npy')
    np.savetxt('xoavg.txt',data)
    data = np.load('yoavg.txt.npy')
    np.savetxt('yoavg.txt',data)
    data = np.load('zoavg.txt.npy')
    np.savetxt('zoavg.txt',data)
    data = np.load('woavg.txt.npy')
    np.savetxt('woavg.txt',data)
if __name__ == '__main__':
    main()