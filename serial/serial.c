#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Function to swap two elements
void swap(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

// Partition function
int partition(int arr[], int low, int high) {
    int pivot = arr[high];  // Choose rightmost element as pivot
    int i = (low - 1);      // Index of smaller element

    for (int j = low; j <= high - 1; j++) {
        // If current element is smaller than or equal to pivot
        if (arr[j] <= pivot) {
            i++; // increment index of smaller element
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return (i + 1);
}

// Main QuickSort function
void quickSort(int arr[], int low, int high) {
    if (low < high) {
        // pi is partitioning index, arr[pi] is now at right place
        int pi = partition(arr, low, high);

        // Separately sort elements before and after partition
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

// Function to print an array
void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++)
        printf("%d ", arr[i]);
    printf("\n");
}

// Function to generate random array
void generateRandomArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        arr[i] = rand() % 1000; // Random numbers between 0 and 999
    }
}

// Function to verify if array is sorted
int isSorted(int arr[], int size) {
    for (int i = 1; i < size; i++) {
        if (arr[i] < arr[i - 1]) {
            return 0; // Not sorted
        }
    }
    return 1; // Sorted
}

// Driver program
int main() {
    // Seed for random number generation
    srand(time(0));
    
    int size;
    printf("Enter array size: ");
    if (scanf("%d", &size) != 1 || size <= 0) {
        fprintf(stderr, "Invalid array size. Please enter a positive integer.\n");
        return 1;
    }

    int *arr = malloc(sizeof(int) * size);
    if (arr == NULL) {
        fprintf(stderr, "Memory allocation failed for size %d\n", size);
        return 1;
    }

    // Generate random array
    generateRandomArray(arr, size);

    printf("Original array: ");
    printArray(arr, size);

    // Perform QuickSort
    quickSort(arr, 0, size - 1);

    printf("Sorted array:   ");
    printArray(arr, size);

    // Verify the result
    if (isSorted(arr, size)) {
        printf("SUCCESS: Array is correctly sorted!\n");
    } else {
        printf("ERROR: Array is not sorted correctly!\n");
    }

    free(arr);
    return 0;
}