#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <cuda_runtime.h>

#define MAX_DEPTH 16
#define INSERTION_SORT_THRESHOLD 32

// CUDA error checking macro
#define CUDA_CHECK(call) \
    do { \
        cudaError_t err = call; \
        if (err != cudaSuccess) { \
            fprintf(stderr, "CUDA error in %s:%d: %s\n", __FILE__, __LINE__, \
                    cudaGetErrorString(err)); \
            exit(EXIT_FAILURE); \
        } \
    } while(0)

// Device function-swap two elements
__device__ void swap(int* a, int* b) {
    int temp = *a;
    *a = *b;
    *b = temp;
}

// Device function - insertion sort for small arrays
__device__ void insertionSort(int* arr, int left, int right) {
    for (int i = left + 1; i <= right; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= left && arr[j] > key) {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
    }
}

// Device function-partition
__device__ int partition(int* arr, int low, int high) {
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

// Device function - iterative quick sort
__device__ void quickSortDevice(int* arr, int low, int high) {
    int stack[MAX_DEPTH * 2];
    int top = -1;
    
    stack[++top] = low;
    stack[++top] = high;
    
    while (top >= 0) {
        high = stack[top--];
        low = stack[top--];
        
        if (high - low < INSERTION_SORT_THRESHOLD) {
            insertionSort(arr, low, high);
            continue;
        }
        
        if (low < high) {
            int pi = partition(arr, low, high);
            
            if (pi - 1 > low) {
                stack[++top] = low;
                stack[++top] = pi - 1;
            }
            
            if (pi + 1 < high) {
                stack[++top] = pi + 1;
                stack[++top] = high;
            }
        }
    }
}

// CUDA kernel - parallel quick sort on segments
__global__ void quickSortKernel(int* arr, int size, int num_threads) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (tid < num_threads) {
        int segment_size = size / num_threads;
        int start = tid * segment_size;
        int end = (tid == num_threads - 1) ? size - 1 : start + segment_size - 1;
        
        if (start < end) {
            quickSortDevice(arr, start, end);
        }
    }
}

// GPU bitonic merge kernel
__global__ void bitonicMergeKernel(int *arr, int size, int stride, int stage) {
    int tid = blockIdx.x * blockDim.x + threadIdx.x;
    
    if (tid < size) {
        int ixj = tid ^ stride;
        
        if (ixj > tid && ixj < size) {
            bool ascending = ((tid & stage) == 0);
            if ((arr[tid] > arr[ixj]) == ascending) {
                int temp = arr[tid];
                arr[tid] = arr[ixj];
                arr[ixj] = temp;
            }
        }
    }
}

// Generate random array
void generateRandomArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        arr[i] = rand() % 100000;
    }
}

// Verify if array is sorted
int isSorted(int arr[], int size) {
    for (int i = 0; i < size - 1; i++) {
        if (arr[i] > arr[i + 1]) {
            return 0;
        }
    }
    return 1;
}


void printSampleElements(int arr[], int size) {
    int step = size / 10;
    if (step == 0) step = 1;
    
    for (int i = 0; i < size && i < 10 * step; i += step) {
        printf("%d ", arr[i]);
    }
    printf("...\n");
}

// Find next power of 2
int nextPowerOf2(int n) {
    int power = 1;
    while (power < n) {
        power *= 2;
    }
    return power;
}

int main() {
    int size, blockSize;
    int *h_arr, *d_arr;
    float gpu_time_ms;
    cudaEvent_t start, stop;
    
    
    printf("Enter the block size: ");
    if (scanf("%d", &blockSize) != 1 || blockSize <= 0) {
        printf("Error: Invalid block size!\n");
        return 1;
    }
    
    if (blockSize > 1024 || (blockSize & (blockSize - 1)) != 0) {
        printf("Error: Block size must be a power of 2 and <= 1024!\n");
        return 1;
    }
    
    
    printf("Enter the array size: ");
    if (scanf("%d", &size) != 1 || size <= 0) {
        printf("Error: Invalid array size!\n");
        return 1;
    }
    
    printf("\n=================\n");
    printf("CUDA QUICK SORT\n");
    printf("=================\n\n");
    
    // Allocate host memory
    h_arr = (int*)malloc(size * sizeof(int));
    if (h_arr == NULL) {
        printf("Error: Memory allocation failed!\n");
        return 1;
    }
    
  
    srand(time(NULL));
    printf("Generating random array...\n");
    generateRandomArray(h_arr, size);
    
    printf("\nBefore Sorting (Sample elements): ");
    printSampleElements(h_arr, size);
    
    // Allocate device memory
    CUDA_CHECK(cudaMalloc(&d_arr, size * sizeof(int)));
    
    // Copy data to device
    CUDA_CHECK(cudaMemcpy(d_arr, h_arr, size * sizeof(int), cudaMemcpyHostToDevice));
    
    // Create events for timing
    CUDA_CHECK(cudaEventCreate(&start));
    CUDA_CHECK(cudaEventCreate(&stop));
    
    printf("Sorting with CUDA Quick Sort (Block size: %d)...\n", blockSize);
    
    // Start timing
    CUDA_CHECK(cudaEventRecord(start, 0));
    
    // Parallel QuickSort on segments
    int num_segments = blockSize;
    if (num_segments > size / 1000) num_segments = size / 1000;
    if (num_segments < 1) num_segments = 1;
    
    int numBlocks = (num_segments + blockSize - 1) / blockSize;
    quickSortKernel<<<numBlocks, blockSize>>>(d_arr, size, num_segments);
    CUDA_CHECK(cudaGetLastError());
    CUDA_CHECK(cudaDeviceSynchronize());
    
    // GPU Bitonic Merge (ALL ON GPU - NO CPU!)
    if (num_segments > 1) {
        int paddedSize = nextPowerOf2(size);
        int *d_padded = NULL;
        
        // Pad array if needed
        if (paddedSize > size) {
            CUDA_CHECK(cudaMalloc(&d_padded, paddedSize * sizeof(int)));
            CUDA_CHECK(cudaMemcpy(d_padded, d_arr, size * sizeof(int), cudaMemcpyDeviceToDevice));
            
            // Set padding to max value
            int *d_padding = d_padded + size;
            int paddingSize = paddedSize - size;
            int maxVal = 2147483647; // largest 32-bit integer
            
            int *h_padding = (int*)malloc(paddingSize * sizeof(int));
            for (int i = 0; i < paddingSize; i++) h_padding[i] = maxVal;
            CUDA_CHECK(cudaMemcpy(d_padding, h_padding, paddingSize * sizeof(int), cudaMemcpyHostToDevice));
            free(h_padding);
            
            CUDA_CHECK(cudaFree(d_arr));
            d_arr = d_padded;
        } else {
            paddedSize = size;
        }
        
        // Bitonic merge stages (ALL ON GPU)
        int threadsPerBlock = 256;
        int blocksPerGrid = (paddedSize + threadsPerBlock - 1) / threadsPerBlock;
        
        for (int stage = 2; stage <= paddedSize; stage *= 2) {
            for (int stride = stage / 2; stride > 0; stride /= 2) {
                bitonicMergeKernel<<<blocksPerGrid, threadsPerBlock>>>(d_arr, paddedSize, stride, stage);
                CUDA_CHECK(cudaGetLastError());
                CUDA_CHECK(cudaDeviceSynchronize());
            }
        }
    }
    
    // Copy back to host
    CUDA_CHECK(cudaMemcpy(h_arr, d_arr, size * sizeof(int), cudaMemcpyDeviceToHost));
    
    // Stop timing
    CUDA_CHECK(cudaEventRecord(stop, 0));
    CUDA_CHECK(cudaEventSynchronize(stop));
    CUDA_CHECK(cudaEventElapsedTime(&gpu_time_ms, start, stop));
    
    printf("After sorting (Sample elements): ");
    printSampleElements(h_arr, size);
    
    
    printf("\nVerifying sorted array...\n");
    if (isSorted(h_arr, size)) {
        printf("✓ SUCCESS: Array is correctly sorted!\n");
    } else {
        printf("✗ FAILED: Array is NOT correctly sorted!\n");
    }
    
    double time_seconds = gpu_time_ms / 1000.0;
    
    printf("\n======================\n");
    printf("Performance Results\n");
    printf("======================\n\n");
    printf("Array Size:  %d elements\n", size);
    printf("Block Size: %d\n", blockSize);
    printf("GPU: NVIDIA GeForce RTX 4060 Laptop\n");
    printf("\nExecution Time:  %.6f seconds\n", time_seconds);
    printf("Elements/second: %.2f million\n", (size / time_seconds) / 1000000.0);
    printf("-------------------------------------------------------\n");
    
    // Cleanup
    CUDA_CHECK(cudaEventDestroy(start));
    CUDA_CHECK(cudaEventDestroy(stop));
    CUDA_CHECK(cudaFree(d_arr));
    free(h_arr);
    
    return 0;
}
