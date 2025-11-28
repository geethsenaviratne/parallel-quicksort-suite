# Serial QuickSort Implementation

## Student Information
- **Student ID**: IT23226128
- **Assignment**: SE3082 - Assignment 03
- **Implementation**: Serial QuickSort (Baseline)

## Files
- `serial_quicksort.c` - Source code
- `Makefile` - Build configuration
- `README.md` - This file

## Compilation

### Using Makefile (Recommended)
```bash
make
```

### Manual Compilation
```bash
gcc -o serial_quicksort serial_quicksort.c -O3 -Wall
```

## Execution

### Basic Usage
```bash
./serial_quicksort <array_size>
```

### Examples
```bash
# Sort 100,000 elements
./serial_quicksort 100000

# Sort 1 million elements
./serial_quicksort 1000000

# Sort 10 million elements
./serial_quicksort 10000000
```

### Using Makefile
```bash
# Run with default size (1M elements)
make run

# Run multiple tests
make test
```

## Algorithm Description

This is a standard implementation of the QuickSort algorithm using:
- **Divide and Conquer** approach
- **Last element** as pivot
- **In-place** sorting (no extra arrays)
- **Recursive** implementation

### Time Complexity
- Average Case: O(n log n)
- Worst Case: O(n²)
- Best Case: O(n log n)

### Space Complexity
- O(log n) - recursion stack

## Test Configuration
- Array Size: 1,000,000 elements
- Data Type: Random integers (0 - 99,999)
- Compiler: GCC with -O3 optimization

## Cleaning Up
```bash
make clean
```

## Sample Output
```
Serial Quick Sort
Array size: 1000000

Generating random array...
Sample elements: 56076 51167 48668 18769 40355 25835 26741 91520 54563 19076 ...

Sorting...
Sample elements: 0 9980 19979 29982 39985 50036 60017 70050 80028 89999 ...

Verifying sorted array...
✓ SUCCESS: Array is correctly sorted!

========================================
Performance Results
========================================
Array Size:      1000000 elements
Execution Time:  0.103644 seconds
========================================
```

## Troubleshooting

### Issue: Permission denied
```bash
chmod +x serial_quicksort
```

### Issue: Segmentation fault
- Try smaller array size
- Check available memory

### Issue: Compilation error
- Ensure GCC is installed
- Check file name matches