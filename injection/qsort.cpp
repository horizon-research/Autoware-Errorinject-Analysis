#include <stdio.h> 
#include <stdlib.h> 
#include <unistd.h> 
#include <sys/types.h> 
#include <sys/stat.h> 
#include <fcntl.h> 
#include <fstream>
#include <iostream>
#include <time.h>
using namespace std;
int values[489100];
#define MAX 65530
int compare (const void * a, const void * b)
{
  return ( *(int*)a - *(int*)b );
}

int main (int argc, char **argv)
{
  int n;
  int i;
  ofstream pidfile;
  ofstream xfile;
  pidfile.open("pid.txt", ios::out);
  pidfile << getpid() << endl;
  pidfile.close();
  printf("My pid..%d\n", getpid() );
  srand((unsigned)time(NULL));
  for (i=0;i<489100;i++)
  {
    values[i] = rand() % MAX;
  }
  for (n=0; n<489100; n++)
  {
    xfile.open(argv[1],ios::app);
    xfile << values[n] << endl;
    xfile.close();
  }
  qsort (values, 489100, sizeof(int), compare);
  for (n=0; n<489100; n++)
  {
    xfile.open(argv[2],ios::app);
    xfile << values[n] << endl;
    xfile.close();
  }
  return 0;
}
