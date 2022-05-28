#include <mpi.h>
#include <stdio.h>
#include "reduce.h"
#include "utils.h"
#include <math.h>
#include <stdlib.h>
#include <limits.h>

#define min(a,b) (((a) <= (b)) ? (a) : (b))
#define max(a,b) (((a) >= (b)) ? (a) : (b))

/* This is the implementation that we came up with in the exercises for
   MPI_SUM. */

int ring_allreduce(const int *sendbuf, int *recvbuf, int count, MPI_Op op,
                   MPI_Comm comm)
{
  int rank, size;
  int i, c;
  int ierr;
  int source;
  int dest;

  if (op != MPI_SUM) {
    fprintf(stderr, "Only coded for op == MPI_SUM\n");
    return MPI_Abort(comm, 1);
  }
  ierr = MPI_Comm_rank(comm, &rank);CHKERR(ierr);
  ierr = MPI_Comm_size(comm, &size);CHKERR(ierr);

  source = (rank + size - 1) % size;
  dest = (rank + 1) % size;
  for (c = 0; c < count; c++) {
    recvbuf[c] = sendbuf[c];
  }
  for (i = 0; i < size - 1; i++) {
    ierr = MPI_Sendrecv_replace(recvbuf, count, MPI_INT, dest, 0, source, 0, comm, MPI_STATUS_IGNORE);CHKERR(ierr);
    /* Only correct for op == MPI_SUM */
    for (c = 0; c < count; c++) {
      recvbuf[c] += sendbuf[c];
    }
  }
  return 0;
}

int tree_allreduce(const int *sendbuf, int *recvbuf, int count, MPI_Op op,
                   MPI_Comm comm)
{
  /* You should implement the tree reduction here, you should handle
     MPI_SUM, MPI_PROD, MPI_MIN, and MPI_MAX for the MPI_Op
     argument. */
  /*
IN sendbuf: starting address of send buffer (choice)
OUT recvbuf: starting address of receive buffer (choice)
IN count: number of elements in send buffer (non-negative integer)
IN op: operation (handle)
IN comm: communicator (handle)
*/

  int rank, size;
  int i, c;
  int terr;
 // int sourcet;
  //int destt;
  int receiver;
  int sender;
  int *tmpbuf;
  int *tmp_min;
  int *tmp_max;

  terr = MPI_Comm_rank(comm, &rank);CHKERR(terr);
  terr = MPI_Comm_size(comm, &size);CHKERR(terr);


  tmpbuf = malloc(count * sizeof(*tmpbuf));
  // copy elements from sendbuf to recvbuf
  for (c = 0; c < count; c++) {
    tmpbuf[c] = sendbuf[c];
    recvbuf[c] = sendbuf[c];
  }
  tmp_min = malloc(count * sizeof(*tmp_min));
  tmp_max = malloc(count * sizeof(*tmp_max));
  for (c = 0; c < count; c++) {
    tmp_min[c] = sendbuf[c];
    tmp_max[c] = sendbuf[c];
  }

  // Process the Reduce operation from all processes to the process 0 (the root)
  for (i = 2; i <= size; i *= 2) {
  	if (rank % i == 0) {
		//reciever = rank;
		sender = rank + ( i / 2); // devide by 2
          	terr = MPI_Recv(recvbuf, count, MPI_INT, sender, 2022, comm, MPI_STATUS_IGNORE);CHKERR(terr);
		if (op == MPI_SUM) {
			for (c = 0; c < count; c++) {
				recvbuf[c] += tmpbuf[c];
			}
			// tmp_max = local_max;
			for (c = 0; c < count; c++) {
				tmpbuf[c] = recvbuf[c];
			}
    }
    else if (op == MPI_PROD) {
			for (c = 0; c < count; c++) {
				recvbuf[c] *= tmpbuf[c];
			}
			for (c = 0; c < count; c++) {
				tmpbuf[c] = recvbuf[c];
			}
      }
    else if (op == MPI_MAX) {
      for (c = 0; c < count; c++) {
        recvbuf[c] = max(recvbuf[c], tmp_max[c]);
      }
      for (c = 0; c < count; c++) {
        tmp_max[c] = recvbuf[c];
      }
    }

    else if (op == MPI_MIN) {
      for (c = 0; c < count; c++) {
        recvbuf[c] = min(recvbuf[c], tmp_min[c]);
      }
      for (c = 0; c < count; c++) {
        tmp_min[c] = recvbuf[c];
      }
    }
	} 
  else {
		if ( rank % (i / 2) == 0) {
			receiver = rank - (i / 2);
			//sender = rank;
        		terr = MPI_Send(sendbuf, count, MPI_INT, receiver, 2022, comm);CHKERR(terr);
		}
	}
  }
  // Process the broadcast operation from the process 0 to all other processes
  MPI_Bcast(recvbuf, count, MPI_INT, 0, comm);

  return 0;
}
