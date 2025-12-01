
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <assert.h>
#include <stdlib.h>
#include <iostream>
#include "mpi.h"
#include "scr.h"
int checkpoint(int size_mb) {
  int rank;
  char tmp[256];
  char file[SCR_MAX_FILENAME];
  char dir[SCR_MAX_FILENAME];
  char dname;
  int rc;
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);
  SCR_Start_checkpoint();
  sprintf(tmp, "rank_%d", rank);
  std::cout << "In: " << tmp << "\n";
  SCR_Route_file(tmp, file);
  std::cout << "Out: " << file << "\n";
  SCR_Complete_checkpoint(1);
  return 0;
}
int main(int argc, char **argv) {
  int size_mb = 1;
  MPI_Init(NULL, NULL);
  SCR_Configf("SCR_CHECKPOINT_INTERVAL=%d", 1);
  SCR_Configf("SCR_USER_NAME=%s", "scons");
  SCR_Init();
  int flag = 0;
  SCR_Need_checkpoint(&flag);
  if (flag) {
    checkpoint(size_mb);
  }
  SCR_Finalize();
  MPI_Finalize();
  return 0;
}

