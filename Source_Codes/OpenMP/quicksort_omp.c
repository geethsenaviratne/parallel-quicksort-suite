#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <omp.h>

// Minimum size for creating parallel tasks
// Below this threshold, use serial sort to avoid overhead
#define TASK_THRESHOLD 10000

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

// Serial Quick Sort (used for small subarrays)
void quickSortSerial(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSortSerial(arr, low, pi - 1);
        quickSortSerial(arr, pi + 1, high);
    }
}

// Parallel Quick Sort using OpenMP tasks
void quickSortParallel(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        
        // Calculate subarray sizes
        int left_size = pi - low;
        int right_size = high - pi;
        
        // If subarrays are large enough, create parallel tasks
        if (left_size > TASK_THRESHOLD && right_size > TASK_THRESHOLD) {
            #pragma omp task shared(arr) firstprivate(low, pi)
            {
                quickSortParallel(arr, low, pi - 1);
            }
            
            #pragma omp task shared(arr) firstprivate(pi, high)
            {
                quickSortParallel(arr, pi + 1, high);
            }
            
            #pragma omp taskwait
        }
        // If only left subarray is large, parallelize left only
        else if (left_size > TASK_THRESHOLD) {
            #pragma omp task shared(arr) firstprivate(low, pi)
            {
                quickSortParallel(arr, low, pi - 1);
            }
            quickSortSerial(arr, pi + 1, high);
            #pragma omp taskwait
        }
        // If only right subarray is large, parallelize right only
        else if (right_size > TASK_THRESHOLD) {
            quickSortSerial(arr, low, pi - 1);
            #pragma omp task shared(arr) firstprivate(pi, high)
            {
                quickSortParallel(arr, pi + 1, high);
            }
            #pragma omp taskwait
        }
        // Both subarrays are small, use serial sort
        else {
            quickSortSerial(arr, low, pi - 1);
            quickSortSerial(arr, pi + 1, high);
        }
    }
}

// Function to generate random array
void generateRandomArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        arr[i] = rand() % 100000;  // 0-99999 range for better distribution
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

// Function to print sample elements (every size/10 element)
void printSampleElements(int arr[], int size) {
    int step = size / 10;
    if (step == 0) step = 1;
    
    for (int i = 0; i < size && i < 10 * step; i += step) {
        printf("%d ", arr[i]);
    }
    printf("...\n");
}

int main(int argc, char* argv[]) {
    int size;
    int num_threads;
    
    // Check command line arguments
    if (argc != 3) {
        printf("Usage: %s <array_size> <num_threads>\n", argv[0]);
        printf("Example: %s 1000000 4\n", argv[0]);
        return 1;
    }
    
    // Get array size and thread count from arguments
    size = atoi(argv[1]);
    num_threads = atoi(argv[2]);
    
    // Validate input
    if (size <= 0) {
        printf("Error: Array size must be positive!\n");
        return 1;
    }
    
    if (num_threads <= 0) {
        printf("Error: Number of threads must be positive!\n");
        return 1;
    }
    
    // Set number of threads
    omp_set_num_threads(num_threads);
    
    // Allocate memory for array
    int* arr = (int*)malloc(size * sizeof(int));
    
    if (arr == NULL) {
        printf("Error: Memory allocation failed!\n");
        return 1;
    }
    
    // Seed random number generator
    srand(time(NULL));
    
    // Generate random array
    printf("Generating random array...\n");
    generateRandomArray(arr, size);
    
    // Display sample elements before sorting
    printf("\nBefore Sorting (Sample elements): ");
    printSampleElements(arr, size);
    
    // Sorting message
    printf("Sorting with OpenMP (%d threads)...\n", num_threads);
    
    // Measure execution time
    double start = omp_get_wtime();
    
    // Start parallel region and create initial task
    #pragma omp parallel
    {
        #pragma omp single
        {
            quickSortParallel(arr, 0, size - 1);
        }
    }
    
    double end = omp_get_wtime();
    double time_taken = end - start;
    
    // Display sample elements after sorting
    printf("After sorting (Sample elements): ");
    printSampleElements(arr, size);
    
    // Verify sorting
    printf("\nVerifying sorted array...\n");
    if (isSorted(arr, size)) {
        printf("✓ SUCCESS: Array is correctly sorted!\n");
    } else {
        printf("✗ FAILED: Array is NOT correctly sorted!\n");
        free(arr);
        return 1;
    }
    
    // Display performance results
    printf("\n======================\n");
    printf("Performance Results\n");
    printf("======================\n");
    printf("\nArray Size:  %d elements\n", size);
    printf("Number of Threads: %d\n", num_threads);
    printf("Execution Time:  %.6f seconds\n", time_taken);
    printf("Elements/second: %.2f million\n", (size / time_taken) / 1000000.0);
    printf("-------------------------------------------------------\n");
    
    // Free allocated memory
    free(arr);
    
    return 0;
}