#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ptrace.h>
#include <sys/reg.h>
#include <sys/types.h>
#include <sys/types.h>
#include <sys/user.h>
#include <sys/wait.h>

int main(int argc, char **argv){
    printf("begin\n");
    int pid=atoi(argv[1]);//the pid of the process
    int status;
    printf("attach%d\n",ptrace(PTRACE_ATTACH,pid));//attach to process
    //waitpid(pid,&status,0);
    wait(&status);
    int i;
        //printf("%d",ptrace(PTRACE_SINGLESTEP,pid,NULL,NULL));
        
        printf("------------------------\n");
        //printf("%d\n",x);
        struct user_fpregs_struct regs;
        printf("getreg%d\n",ptrace(PTRACE_GETFPREGS,pid,0, &regs));
        
        //printf("st0: %llx.\n",regs.st_space[0]);
        for (i=0;i<32;i++)
        {
            printf("xmm%d: %llx.\n",i,regs.xmm_space[i]);
        }
        int register_select = atoi(argv[2]);
        int bit_flip = atoi(argv[3]);
        for (i=0;i<32;i++)
        {
            if (i==register_select)
            {
                regs.xmm_space[i] = regs.xmm_space[i] ^ (1<<bit_flip);
                printf("new xmm%d: %llx.\n",i,regs.xmm_space[i]);
            }
        }
        printf("%d",ptrace(PTRACE_CONT,pid,NULL,NULL));
        ptrace(PTRACE_DETACH,pid);//attach to process
        printf("end\n");
        return 0;
}
