#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/ptrace.h>
#include <sys/reg.h>
#include <sys/types.h>
#include <sys/types.h>
#include <sys/user.h>
#include <sys/wait.h>

int x=0;

void dumpRegs(int pid){
    printf("------------------------\n");
    printf("%d\n",x);
    struct user_regs_struct regs;
    ptrace(PTRACE_GETREGS,pid,NULL, &regs);
    printf("cs: %llx.\n",regs.cs);
    printf("ds: %llx.\n",regs.ds);
    printf("eflags: %llx.\n",regs.eflags);
    printf("es: %llx.\n",regs.es);
    printf("fs: %llx.\n",regs.fs);
    printf("fs_base: %llx.\n",regs.fs_base);
    printf("gs: %llx.\n",regs.gs);
    printf("gs_base: %llx.\n",regs.gs_base);
    printf("orig_rax: %llx.\n",regs.orig_rax);
    printf("r10: %llx.\n",regs.r10);
    printf("r11: %llx.\n",regs.r11);
    printf("r12: %llx.\n",regs.r12);
    printf("r13: %llx.\n",regs.r13);
    printf("r14: %llx.\n",regs.r14);
    printf("r15: %llx.\n",regs.r15);
    printf("r8: %llx.\n",regs.r8);
    printf("r9: %llx.\n",regs.r9);
    printf("rax: %llx.\n",regs.rax);
    printf("rbp: %llx.\n",regs.rbp);
    printf("rbx: %llx.\n", regs.rbx);
    printf("rbx: %llx.\n",regs.rbx);
    printf("rcx: %llx.\n",regs.rcx);
    printf("rdi: %llx.\n",regs.rdi);
    printf("rdx: %llx.\n",regs.rdx);
    printf("rip: %llx.\n",regs.rip);
    printf("rsi: %llx.\n",regs.rsi);
    printf("rsp: %llx.\n",regs.rsp);
    printf("ss: %llx.\n",regs.ss); 
}

int main(int argc, char **argv){
    printf("begin\n");
    int pid=atoi(argv[1]);//the pid of the process
    int status;
    printf("attach%d\n",ptrace(PTRACE_ATTACH,pid));//attach to process
    //waitpid(pid,&status,0);
    wait(&status);
        x++;
        //printf("%d",ptrace(PTRACE_SINGLESTEP,pid,NULL,NULL));
        
        printf("------------------------\n");
        printf("%d\n",x);
        struct user_regs_struct regs;
        
        printf("getreg%d\n",ptrace(PTRACE_GETREGS,pid,0, &regs));
        
        printf("cs: %llx.\n",regs.cs);
        printf("ds: %llx.\n",regs.ds);
        printf("eflags: %llx.\n",regs.eflags);
        printf("es: %llx.\n",regs.es);
        printf("fs: %llx.\n",regs.fs);
        printf("fs_base: %llx.\n",regs.fs_base);
        printf("gs: %llx.\n",regs.gs);
        printf("gs_base: %llx.\n",regs.gs_base);
        printf("orig_rax: %llx.\n",regs.orig_rax);
        printf("r10: %llx.\n",regs.r10);
        printf("r11: %llx.\n",regs.r11);
        printf("r12: %llx.\n",regs.r12);
        printf("r13: %llx.\n",regs.r13);
        printf("r14: %llx.\n",regs.r14);
        printf("r15: %llx.\n",regs.r15);
        printf("r8: %llx.\n",regs.r8);
        printf("r9: %llx.\n",regs.r9);
        printf("rax: %llx.\n",regs.rax);
        printf("rbp: %llx.\n",regs.rbp);
        printf("rbx: %llx.\n", regs.rbx);
        printf("rbx: %llx.\n",regs.rbx);
        printf("rcx: %llx.\n",regs.rcx);
        printf("rdi: %llx.\n",regs.rdi);
        printf("rdx: %llx.\n",regs.rdx);
        printf("rip: %llx.\n",regs.rip);
        printf("rsi: %llx.\n",regs.rsi);
        printf("rsp: %llx.\n",regs.rsp);
        printf("ss: %llx.\n",regs.ss);
        int register_select = atoi(argv[2]);
        int bit_flip = atoi(argv[3]);
        if (register_select==0)
        {
            regs.r8 = regs.r8 ^ (1<<bit_flip);
            printf("newr8: %llx.\n",regs.r8);
        }
        else if (register_select==1)
        {
            regs.r9 = regs.r9 ^ (1<<bit_flip);
            printf("newr9: %llx.\n",regs.r9);
        }
        else if (register_select==2)
        {
            regs.r10 = regs.r10 ^ (1<<bit_flip);
            printf("newr10: %llx.\n",regs.r10);
        }
        else if (register_select==3)
        {
            regs.r11 = regs.r11 ^ (1<<bit_flip);
            printf("newr11: %llx.\n",regs.r11);
        }
        else if (register_select==4)
        {
            regs.r12 = regs.r12 ^ (1<<bit_flip);
            printf("newr12: %llx.\n",regs.r12);
        }
        else if (register_select==5)
        {
            regs.r13 = regs.r13 ^ (1<<bit_flip);
            printf("newr13: %llx.\n",regs.r13);
        }
        else if (register_select==6)
        {
            regs.r14 = regs.r14 ^ (1<<bit_flip);
            printf("newr14: %llx.\n",regs.r14);
        }
        else
        {
            regs.r15 = regs.r15 ^ (1<<bit_flip);
            printf("newr15: %llx.\n",regs.r15);
        }
        regs.r15 = regs.r15 ^ (1<<7);
        
        printf("setreg%d",ptrace(PTRACE_SETREGS,pid,NULL, &regs));
        printf("xxxxxxxxxxxxx");
    
    

    printf("%d",ptrace(PTRACE_CONT,pid,NULL,NULL));
    ptrace(PTRACE_DETACH,pid);//attach to process
    printf("end\n");
    return 0;
}