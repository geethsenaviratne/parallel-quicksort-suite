# Serial Quick Sort Implementation
## SE3082 - Parallel Computing Assignment 03

---

## 📋 Overview

This is a serial (non-parallel) implementation of the Quick Sort algorithm in C. It serves as the baseline for comparing parallel implementations using OpenMP, MPI, and CUDA.

**Student:** Geeth Seneviratne 
**Student ID:** IT23226128  
**Algorithm:** Quick Sort  
**Problem Domain:** Sorting and Searching Algorithms

---

## 📁 Project Structure

```
serial/
├── serial.c          # Source code
├── Makefile          # Build automation
└── README.md         # This file
```

---

## 🚀 Quick Start

### Compilation

```bash
make
```

### Running the Program

```bash
./serial
```

Then enter the array size when prompted.

### One-Command Run

```bash
make run
```

### Clean Up

```bash
make clean
```

---

## 💻 Detailed Usage

### Compilation Methods

**Method 1: Using Makefile**
```bash
make
```

**Method 2: Direct GCC Compilation**
```bash
gcc -Wall -O2 -o serial serial.c
```

### Makefile Commands

| Command | Description |
|---------|-------------|
| `make` or `make all` | Compile the program |
| `make run` | Compile and run the program |
| `make clean` | Remove compiled files |
| `make help` | Show available commands |

---

## 📊 Example Output

```
Enter array size: 10000000

===================
Serial Quick Sort
===================
Array Size: 10000000

Before sorting: 
3892 2221 3673 2077 8140 2720 4823 7929 8672 6766 ... 9377 1714 6913 9939 3361 5469 8145 7156 1528 2038 (showing first 10 and last 10 of 10000000 elements)

After sorting: 
0 0 0 0 0 0 0 0 0 0 ... 9999 9999 9999 9999 9999 9999 9999 9999 9999 9999 (showing first 10 and last 10 of 10000000 elements)

Verifying sorted array...
✓ SUCCESS: Array is correctly sorted!

Execution Time: 1.505698 seconds
----------------------------------------
```

---

## 🧪 Testing

### Test Sizes

| Size | Description | Expected Time | Use Case |
|------|-------------|---------------|----------|
| 10,000 | Small | < 0.001s | Quick testing |
| 100,000 | Medium | ~0.01s | Standard testing |
| 1,000,000 | Large | ~0.1s | Performance testing |
| 10,000,000 | Extra Large | ~1-2s | Benchmark testing |

### Running Tests

```bash
# Test 1: Small array
./serial
# Enter: 10000

# Test 2: Medium array
./serial
# Enter: 100000

# Test 3: Large array
./serial
# Enter: 1000000

# Test 4: Extra large array
./serial
# Enter: 10000000
```


## 🔍 Algorithm Details

### Quick Sort Algorithm

**Type:** Divide and Conquer  
**Average Time Complexity:** O(n log n)  
**Worst Case Time Complexity:** O(n²)  
**Best Case Time Complexity:** O(n log n)  
**Space Complexity:** O(log n) - recursion stack

### How It Works

1. **Choose Pivot:** Select the rightmost element as pivot
2. **Partition:** Rearrange array so elements smaller than pivot are on left, larger on right
3. **Recursion:** Apply the same process to left and right sub-arrays
4. **Base Case:** When sub-array has 0 or 1 element, it's already sorted

### Why Quick Sort is Good for Parallelization

- **Independent Sub-problems:** Left and right sub-arrays can be sorted independently
- **Task Parallelism:** Recursive calls can be executed in parallel
- **Data Parallelism:** Partitioning can be parallelized
- **Scalable:** Benefits from multiple processors/cores

---

## 📝 Code Structure

### Main Functions

```c
void swap(int* a, int* b)
```
- Swaps two array elements
- Used during partitioning

```c
int partition(int arr[], int low, int high)
```
- Partitions array around pivot element
- Returns final position of pivot
- Core of the Quick Sort algorithm

```c
void quickSort(int arr[], int low, int high)
```
- Main recursive sorting function
- Divides array and sorts sub-arrays

```c
void generateRandomArray(int arr[], int size)
```
- Generates random integers (0-9999)
- Used for testing

```c
int isSorted(int arr[], int size)
```
- Verifies array is correctly sorted
- Returns 1 if sorted, 0 if not

```c
void printArray(int arr[], int size)
```
- Displays array contents
- Shows first 10 and last 10 elements for large arrays
- Shows all elements for arrays ≤ 20 elements

---

## 📈 Performance Benchmarks

### Test Environment
- **OS:** Ubuntu on WSL2
- **Compiler:** GCC with -O2 optimization
- **CPU:** (Your CPU details)

### Benchmark Results

| Array Size | Execution Time | Operations |
|-----------|----------------|------------|
| 10,000 | ~0.001s | ~133,000 |
| 100,000 | ~0.01s | ~1.66M |
| 1,000,000 | ~0.1s | ~19.9M |
| 10,000,000 | ~1.5s | ~232M |

**Note:** Actual times may vary based on hardware

---

## 🔧 Compilation Details

### Compiler Flags

- `-Wall`: Enable all compiler warnings
- `-O2`: Optimization level 2 (good balance of speed and compilation time)

### About the Warning

You may see this warning during compilation:
```
warning: ignoring return value of 'scanf' declared with attribute 'warn_unused_result'
```

**This is safe to ignore.** The program handles input correctly. The warning is just a compiler suggestion to check scanf's return value.

---

## 🎯 Features

- ✅ User-friendly input prompts
- ✅ Random array generation (values: 0-9999)
- ✅ Smart array display (shows first 10 and last 10 elements)
- ✅ Automatic sorting verification
- ✅ Precise execution time measurement
- ✅ Memory management (dynamic allocation)
- ✅ Error handling (invalid input, memory allocation failures)
- ✅ Clean, well-commented code

---

## 🐛 Troubleshooting

### Common Issues

**Problem:** `make: command not found`

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install build-essential

# Already have gcc? Just use direct compilation
gcc -Wall -O2 -o serial serial.c
```

---

**Problem:** `gcc: command not found`

**Solution:**
```bash
# Ubuntu/Debian
sudo apt-get install gcc

# Check if installed
gcc --version
```

---

**Problem:** Compilation warning about scanf

**Solution:**
This is just a warning, not an error. The program works correctly. You can safely ignore it or the code can be modified to explicitly check scanf's return value (which it already does).

---

**Problem:** Program runs but output seems incorrect

**Solution:**
- Verify you're using the latest version of serial.c
- Recompile with `make clean && make`
- Test with a small array size first (e.g., 100)

---


## 👨‍💻 Author

**Student:** Geeth Seneviratne 
**ID:** IT23226128  
**Course:** BSc (Hons) in Information Technology - Year 3  
**Module:** SE3082 - Parallel Computing  
**Assignment:** 03 - Algorithm Parallelization

---