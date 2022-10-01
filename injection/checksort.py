import os
import pdb

def main():
    for i in range(300):
        print(i)
        prefilename = 'prelist' + str(i) + '.txt'
        postfilename = 'postlist' + str(i) + '.txt'
        fpre = open(prefilename,'r')
        a = fpre.readlines()
        fpost = open(postfilename,'r')
        b = fpost.readlines()
        pre = []
        post = []
        for j in range(len(a)):
            pre.append(int(a[j]))
        for j in range(len(b)):
            post.append(int(b[j]))
        if len(post) < len(pre):
            print(len(pre), len(post), prefilename+' crash')
            #break
        for j in range(0,len(b)-1):
            #if post[j] not in pre:
                #pdb.set_trace()
            #    print(prefilename+' sdc, not in prelist')
            #    break
            if post[j] > post[j+1]:
                print(prefilename+' sdc, @jth number')
                break
if __name__ == '__main__':
    main()
