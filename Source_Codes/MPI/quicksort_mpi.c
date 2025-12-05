#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <mpi.h>

// Function to swap two elements
void swap(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

// Partition function
int partition(int arr[], int low, int high) {
    int pivot = arr[high];
    int i = low - 1;
    
    for (int j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;
            swap(&arr[i], &arr[j]);
        }
    }
    swap(&arr[i + 1], &arr[high]);
    return i + 1;
}

// Serial Quick Sort
void quickSort(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

// Simple merge of two sorted arrays
void merge(int* result, int* left, int left_size, int* right, int right_size) {
    int i = 0, j = 0, k = 0;
    
    while (i < left_size && j < right_size) {
        if (left[i] <= right[j]) {
            result[k++] = left[i++];
        } else {
            result[k++] = right[j++];
        }
    }
    
    while (i < left_size) {
        result[k++] = left[i++];
    }
    
    while (j < right_size) {
        result[k++] = right[j++];
    }
}

// Function to generate random array
void generateRandomArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        arr[i] = rand() % 100000;
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

// Function to print sample elements
void printSampleElements(int arr[], int size) {
    int step = size / 10;
    if (step == 0) step = 1;
    
    for (int i = 0; i < size && i < 10 * step; i += step) {
        printf("%d ", arr[i]);
    }
    printf("...\n");
}

int main(int argc, char* argv[]) {
    int rank, num_procs;
    int size;
    int *arr = NULL;
    int *local_arr = NULL;
    int local_size;
    double start_time, end_time;
    
    // Initialize MPI
    MPI_Init(&argc, &argv);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &num_procs);
    
    // Check command line arguments
    if (argc != 2) {
        if (rank == 0) {
            printf("Usage: %s <array_size>\n", argv[0]);
            printf("Example: mpirun -np 4 %s 10000000\n", argv[0]);
        }
        MPI_Finalize();
        return 1;
    }
    
    size = atoi(argv[1]);
    
    // Validate input
    if (size <= 0 || size % num_procs != 0) {
        if (rank == 0) {
            printf("Error: Array size must be positive and divisible by number of processes!\n");
            printf("Array size: %d, Processes: %d\n", size, num_procs);
            printf("Suggestion: Use size that's divisible by %d\n", num_procs);
        }
        MPI_Finalize();
        return 1;
    }
    
    // Calculate local size for each process
    local_size = size / num_procs;
    
    // Master process generates array
    if (rank == 0) {
        arr = (int*)malloc(size * sizeof(int));
        if (arr == NULL) {
            printf("Error: Memory allocation failed!\n");
            MPI_Abort(MPI_COMM_WORLD, 1);
        }
        
        srand(time(NULL));
        printf("Generating random array...\n");
        generateRandomArray(arr, size);
        
        printf("\nBefore Sorting (Sample elements): ");
        printSampleElements(arr, size);
        printf("Sorting with MPI (%d processes)...\n", num_procs);
    }
    
    // Allocate local array for each process
    local_arr = (int*)malloc(local_size * sizeof(int));
    if (local_arr == NULL) {
        printf("Process %d: Memory allocation failed!\n", rank);
        MPI_Abort(MPI_COMM_WORLD, 1);
    }
    
    // Start timing
    MPI_Barrier(MPI_COMM_WORLD);
    start_time = MPI_Wtime();
    
    // Scatter data from master to all processes
    MPI_Scatter(arr, local_size, MPI_INT, 
                local_arr, local_size, MPI_INT, 
                0, MPI_COMM_WORLD);
    
    // Each process sorts its local array
    quickSort(local_arr, 0, local_size - 1);
    
    // Gather sorted arrays back to master
    MPI_Gather(local_arr, local_size, MPI_INT, 
               arr, local_size, MPI_INT, 
               0, MPI_COMM_WORLD);
    
    // Master merges all sorted chunks
    if (rank == 0) {
        // Simple iterative merge
        int *temp = (int*)malloc(size * sizeof(int));
        if (temp == NULL) {
            printf("Error: Temp array allocation failed!\n");
            MPI_Abort(MPI_COMM_WORLD, 1);
        }
        
        // Copy first chunk
        for (int i = 0; i < local_size; i++) {
            temp[i] = arr[i];
        }
        
        int current_size = local_size;
        
        // Merge remaining chunks one by one
        for (int proc = 1; proc < num_procs; proc++) {
            int *merged = (int*)malloc((current_size + local_size) * sizeof(int));
            if (merged == NULL) {
                printf("Error: Merged array allocation failed!\n");
                MPI_Abort(MPI_COMM_WORLD, 1);
            }
            
            // Merge temp with next chunk
            merge(merged, temp, current_size, 
                  arr + proc * local_size, local_size);
            
            // Update current result
            free(temp);
            temp = merged;
            current_size += local_size;
        }
        
        // Copy final result back to arr
        for (int i = 0; i < size; i++) {
            arr[i] = temp[i];
        }
        
        free(temp);
    }
    
    // End timing
    MPI_Barrier(MPI_COMM_WORLD);
    end_time = MPI_Wtime();
    
    
    if (rank == 0) {
        printf("After sorting (Sample elements): ");
        printSampleElements(arr, size);
        
        printf("\nVerifying sorted array...\n");
        if (isSorted(arr, size)) {
            printf("✓ SUCCESS: Array is correctly sorted!\n");
        } else {
            printf("✗ FAILED: Array is NOT correctly sorted!\n");
        }
        
        double time_taken = end_time - start_time;
        
        printf("\n======================\n");
        printf("Performance Results\n");
        printf("======================\n\n");
        printf("Array Size:  %d elements\n", size);
        printf("Number of Processes: %d\n", num_procs);
        printf("Execution Time:  %.6f seconds\n", time_taken);
        printf("Elements/second: %.2f million\n", (size / time_taken) / 1000000.0);
        printf("-------------------------------------------------------\n");
        
        free(arr);
    }
    
    free(local_arr);
    
    // Finalize MPI
    MPI_Finalize();
    return 0;
}