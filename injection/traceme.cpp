#include <stdio.h> 
#include <stdlib.h> 
#include <unistd.h> 
#include <sys/types.h> 
#include <sys/stat.h> 
#include <fcntl.h> 
#include <fstream>
#include <iostream>
using namespace std;
int function( char * a )
{
    char buffer[1024];
    int ic;
    int i;
    int m;
    
    printf("Entered %s\n", __FUNCTION__ );
    m = open( a, O_RDONLY );
    i = 0;

    while( read( m, buffer, sizeof(buffer) ) > 0 ) 
    {
          printf("%s", buffer );
    }
    printf("LEAVING %s\n", __FUNCTION__ );
    return 0; 
}
int main ( int argc, char ** argv ) 
{
    ofstream pidfile;
    ofstream xfile;
    pidfile.open("pid.txt", ios::out);
    pidfile << getpid() << endl;
    pidfile.close();
    printf("My pid..%d\n", getpid() );
    //printf("Press any key to continue...\n");
    //getchar();
    int i;
    int sum;
    sum = 0;
    double x = 0;
    for (i=0;i<1000000;i++)
    {
        x++;
        x--;
        x+=2;
        x-=2;
        x++;
        xfile.open(argv[1],ios::app);
        xfile << x << endl;
        xfile.close();
        printf("%f\n",x);
    }
    //printf("%f\n",x);
    return 0;
} 
