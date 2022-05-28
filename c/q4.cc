#include <iostream>
#include <ctime>
#include //TODO include eigen

using namespace Eigen;

int main()
{
    const int SIZE = 1000;
    //TODO: Add the matrix and vector from q3 in eigen format

    clock_t begin = clock();
    for(int iter=0; iter<100; iter++){

        // TODO: Matrix-vector product using Eigen
        // Do not use auto to initialise the solution,
        // this will produce an abstract type instead of a vector
    }
    clock_t end = clock();
    std::cout << "Time taken using eigen: " << double(end - begin) / CLOCKS_PER_SEC / 100 << std::endl;
    // TODO: Comment on your results here
    // ...
    return 0;
}


