#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Function to swap two elements
void swap(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

// Partition function - places pivot in correct position
// and arranges smaller elements to left, larger to right
int partition(int arr[], int low, int high) {
    int pivot = arr[high];  // Choose rightmost element as pivot
    int i = low - 1;        // Index of smaller element
    
    for (int j = low; j < high; j++) {
        // If current element is smaller than pivot
        if (arr[j] < pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return i + 1;
}

// Main Quick Sort function
void quickSort(int arr[], int low, int high) {
    if (low < high) {
        // Partition the array and get pivot index
        int pi = partition(arr, low, high);
        
        // Recursively sort elements before and after partition
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

// Function to generate random array
void generateRandomArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        arr[i] = rand() % 10000;
    }
}

// Function to verify if array is sorted
int isSorted(int arr[], int size) {
    for (int i = 0; i < size - 1; i++) {
        if (arr[i] > arr[i + 1]) {
            return 0;
        }
    }
    return 1;
}

// Function to print array (shows first 10 and last 10 elements)
void printArray(int arr[], int size) {
    if (size <= 20) {
        // If array is small, print all elements
        for (int i = 0; i < size; i++) {
            printf("%d ", arr[i]);
        }
        printf("\n");
    } else {
        // Print first 10 elements
        for (int i = 0; i < 10; i++) {
            printf("%d ", arr[i]);
        }
        printf("... ");
        
        // Print last 10 elements
        for (int i = size - 10; i < size; i++) {
            printf("%d ", arr[i]);
        }
        printf("(showing first 10 and last 10 of %d elements)\n", size);
    }
}

int main() {
    int size;
    
    // Get array size from user
    printf("Enter array size: ");
    if (scanf("%d", &size) != 1) {
        printf("Error: Invalid input!\n");
        return 1;
    }
    
    // Validate input
    if (size <= 0) {
        printf("Error: Array size must be positive!\n");
        return 1;
    }
    
    // Allocate memory for array
    int* arr = (int*)malloc(size * sizeof(int));
    
    if (arr == NULL) {
        printf("Error: Memory allocation failed!\n");
        return 1;
    }
    
    // Seed random number generator
    srand(time(NULL));
    
    // Generate random array
    generateRandomArray(arr, size);
    
    // Display header
    printf("\n===================\n");
    printf("Serial Quick Sort\n");
    printf("===================\n");
    
    // Display array size
    printf("Array Size: %d\n\n", size);
    
    // Display array before sorting
    printf("Before sorting: \n");
    printArray(arr, size);
    printf("\n");
    
    // Measure execution time
    clock_t start = clock();
    quickSort(arr, 0, size - 1);
    clock_t end = clock();
    
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;
    
    // Display array after sorting
    printf("After sorting: \n");
    printArray(arr, size);
    printf("\n");
    
    // Verify sorting
    printf("Verifying sorted array...\n");
    if (isSorted(arr, size)) {
        printf("✓ SUCCESS: Array is correctly sorted!\n\n");
    } else {
        printf("✗ FAILED: Array is NOT correctly sorted!\n\n");
    }
    
    // Display execution time
    printf("Execution Time: %.6f seconds\n", time_taken);
    printf("----------------------------------------\n");
    
    // Free allocated memory
    free(arr);
    
    return 0;
}