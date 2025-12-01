
#include <stdlib.h>
#include <stdio.h>
#include <hdf5.h>
#include <mpi.h>

#define FILE "testfile.h5"

int main(int argc, char* argv[]) {
  hid_t plist_id, file_id, mem_space, file_space, dset_id;
  hsize_t dims[1];
  dims[0] = 10;
  int data[10];
  int rank;

  MPI_Init(&argc, &argv);
  MPI_Comm_rank(MPI_COMM_WORLD, &rank);

  plist_id = H5Pcreate(H5P_FILE_ACCESS);
  H5Pset_fapl_mpio(plist_id, MPI_COMM_WORLD, MPI_INFO_NULL);
  file_id = H5Fcreate(FILE, H5F_ACC_TRUNC, H5P_DEFAULT, plist_id);
  H5Pclose(plist_id);

  file_space = H5Screate_simple(1, dims, NULL);
  dset_id = H5Dcreate(file_id, "test", H5T_NATIVE_INT, file_space, H5P_DEFAULT, H5P_DEFAULT, H5P_DEFAULT);
  plist_id = H5Pcreate(H5P_DATASET_XFER);
  H5Pset_dxpl_mpio(plist_id, H5FD_MPIO_COLLECTIVE);
  H5Dwrite(dset_id, H5T_NATIVE_INT, H5P_DEFAULT, file_space, plist_id, data);

  H5Pclose(plist_id);
  H5Dclose(dset_id);
  H5Sclose(file_space);
  H5Fclose(file_id);
  MPI_Finalize();

  remove(FILE);
  return EXIT_SUCCESS;
}

