#include <iostream>

int main(){
    const int length = 8;
    int array[length] = {1,1,1,1,1,1,1,1};
    int* first_pointer = &array[0]; // Pointer to the first element of array
    int* last_pointer = first_pointer+length; // Pointer to the last element of array
    //Sum up array backwards
    int sum = 0;
    for(int i=0; i<length; i++) {
        sum += *last_pointer;
        last_pointer--;
    }
    std::cout << "Sum is " << sum << std::endl;
    std::cout << "Sum should be " << length << std::endl;
}
