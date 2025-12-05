# OpenMP Quick Sort Implementation
## SE3082 - Parallel Computing Assignment 03

**Algorithm:** Quick Sort  
**Parallelization Method:** OpenMP (Shared Memory)  
**Array Size:** 10,000,000 elements

---

## 📋 Overview

This is a parallel implementation of Quick Sort using **OpenMP** (Open Multi-Processing). The implementation uses task-based parallelism to sort array subarrays concurrently on shared-memory systems, achieving **5.06x speedup** with 16 threads.

---

## 📁 Project Structure

```
OpenMP/
├── quicksort_omp.c          # OpenMP parallel implementation
├── quicksort_omp            # Compiled executable
├── Makefile                 # Build automation
├── README.md                # This file
│
├── graphs/                  # Performance graphs
│   ├── graph1_threads_vs_time.png
│   ├── graph2_threads_vs_speedup.png
│   ├── graph3_threads_vs_efficiency.png
│   ├── combined_all_graphs.png
│   └── graphs.py            # Graph generator script
│
├── Results/                 # Test results
│   ├── openmp_results.csv
│   ├── thread-01_output.txt
│   ├── thread-02_output.txt
│   ├── thread-04_output.txt
│   ├── thread-08_output.txt
│   └── thread-16_output.txt
│
└── Screenshots/             # Execution screenshots
    ├── 1_threads.png
    ├── 2_threads.png
    ├── 4_threads.png
    ├── 8_threads.png
    └── 16_threads.png
```

---

## 🚀 Quick Start

### Compilation

```bash
make
```

### Running the Program

**Interactive mode:**
```bash
make run
# Enter: 1, 2, 4, 8, or 16
```

**Direct execution:**
```bash
./quicksort_omp 10000000 4
```

### Testing All Thread Counts

```bash
make test     # Test with 1M elements
make eval     # Test with 10M elements
```

---

## 💻 Usage

### Command Format

```bash
./quicksort_omp <array_size> <num_threads>
```

### Examples

```bash
./quicksort_omp 1000000 1      # 1M elements, 1 thread
./quicksort_omp 1000000 4      # 1M elements, 4 threads
./quicksort_omp 10000000 8     # 10M elements, 8 threads
./quicksort_omp 10000000 16    # 10M elements, 16 threads
```

---

## 📊 Performance Results

### Test Configuration
- **Array Size:** 10,000,000 elements
- **Random Range:** 0 - 99,999
- **Task Threshold:** 10,000 elements
- **System:** WSL2 (Windows Subsystem for Linux)
- **Compiler:** GCC with -O3 -fopenmp

### Performance Data

| Threads | Time (s) | Speedup | Efficiency | Throughput (M/s) |
|:-------:|:--------:|:-------:|:----------:|:----------------:|
| 1       | 0.694    | 1.00x   | 100.00%    | 14.42           |
| 2       | 0.626    | 1.11x   | 55.45%     | 15.98           |
| 4       | 0.364    | 1.91x   | 47.75%     | 27.50           |
| 8       | 0.203    | 3.42x   | 42.75%     | 49.31           |
| 16      | 0.137    | **5.06x** | 31.63%   | **72.93**       |

### Key Achievements

✅ **5.06x speedup** with 16 threads  
✅ **80.2% time reduction** from serial version  
✅ **72.93 million elements/second** peak throughput  
✅ **Consistent performance gains** across all thread counts

---

## 📈 Graphs

All performance graphs are available in the `graphs/` directory:

1. **graph1_threads_vs_time.png** - Execution time vs threads
2. **graph2_threads_vs_speedup.png** - Speedup vs threads (with ideal line)
3. **graph3_threads_vs_efficiency.png** - Efficiency vs threads
4. **combined_all_graphs.png** - All three graphs combined

### Generate Graphs

```bash
cd graphs
python3 graphs.py
```

---

## 🔧 Makefile Targets

| Command | Description |
|---------|-------------|
| `make` | Compile the program |
| `make clean` | Remove executable |
| `make run` | Interactive run (1M elements) |
| `make test` | Test all thread counts (1M elements) |
| `make eval` | Performance evaluation (10M elements) |
| `make help` | Show help message |

---

## 🎯 Key Features

### Parallelization Strategy

- **Task-based parallelism** using `#pragma omp task`
- **Adaptive thresholding** switches to serial for small subarrays
- **Dynamic load balancing** through OpenMP task scheduler
- **Recursive parallelism** for independent subarrays

### Code Highlights

```c
// Main parallel region
#pragma omp parallel
{
    #pragma omp single
    {
        quickSortParallel(arr, 0, size - 1);
    }
}

// Task creation for parallel sorting
#pragma omp task shared(arr) firstprivate(low, pi)
{
    quickSortParallel(arr, low, pi - 1);
}
```

### Optimization Techniques

1. **Task Threshold (10,000 elements)**
   - Prevents overhead from excessive task creation
   - Small subarrays use serial sorting

2. **Firstprivate Clause**
   - Each task gets private copy of indices
   - Avoids race conditions

3. **Dynamic Scheduling**
   - OpenMP runtime handles load balancing
   - Efficient utilization of all threads

---

## 🔍 Algorithm Details

### Quick Sort Complexity

- **Average Time:** O(n log n)
- **Worst Case:** O(n²)
- **Space Complexity:** O(log n) - recursion stack

### Why Quick Sort for Parallelization?

✅ **Independent sub-problems** - Left and right subarrays can be sorted in parallel  
✅ **Recursive structure** - Natural fit for task-based parallelism  
✅ **Good cache locality** - In-place sorting with good memory access patterns  
✅ **Scalable** - Benefits from multiple processors/cores

---

## 📝 Example Output

```
Enter number of threads [1,2,4,8,16]: 8
Running with 8 threads...
Generating random array...

Before Sorting (Sample elements): 45177 52260 60792 54219 43514 ...
Sorting with OpenMP (8 threads)...
After sorting (Sample elements): 0 10011 20032 30032 40038 ...

Verifying sorted array...
✓ SUCCESS: Array is correctly sorted!

======================
Performance Results
======================

Array Size:  10000000 elements
Number of Threads: 8
Execution Time:  0.202783 seconds
Elements/second: 49.31 million
-------------------------------------------------------
```

---

## 🧪 Testing & Verification

### Automated Testing

```bash
# Quick test with 1M elements
make test

# Full evaluation with 10M elements
make eval
```

### Manual Testing

```bash
# Test individual thread counts
./quicksort_omp 10000000 1
./quicksort_omp 10000000 2
./quicksort_omp 10000000 4
./quicksort_omp 10000000 8
./quicksort_omp 10000000 16
```

### Verification

The program automatically verifies that the array is correctly sorted after each execution.

---

## 📊 Performance Analysis

### Speedup Analysis

**Strong Scaling (4-16 threads):**
- 4 threads: 1.91x speedup
- 8 threads: 3.42x speedup (79% improvement from 4 threads)
- 16 threads: 5.06x speedup (48% improvement from 8 threads)

**Speedup Formula:**
```
Speedup = T₁ / Tₙ
where T₁ = time with 1 thread, Tₙ = time with n threads
```

### Efficiency Analysis

**Efficiency decreases with thread count (expected behavior):**
- 2 threads: 55% efficiency
- 4 threads: 48% efficiency
- 8 threads: 43% efficiency
- 16 threads: 32% efficiency

**Efficiency Formula:**
```
Efficiency = (Speedup / Number of Threads) × 100%
```

### Bottlenecks

1. **Serial partitioning phase** (Amdahl's Law limitation)
2. **Task creation overhead** at higher thread counts
3. **Memory bandwidth** limitations
4. **Cache contention** with many threads

---

## 💡 Optimization Considerations

### Task Threshold Tuning

Current threshold: **10,000 elements**

**Recommendations:**
- **Small arrays (< 100K):** Increase to 20,000-50,000
- **Medium arrays (100K-1M):** Keep at 10,000
- **Large arrays (> 1M):** Can reduce to 5,000

### Thread Count Selection

| Use Case | Recommended Threads | Reason |
|----------|-------------------|---------|
| Efficiency-critical | 4-8 threads | Good balance (43-48% efficiency) |
| Maximum performance | All available threads | Best speedup (5.06x) |
| General purpose | 8 threads | Sweet spot (3.42x speedup) |

---


## 🐛 Troubleshooting

### Compilation Errors

**Error: `unsupported option '-fopenmp'`**

**Solution:**
```bash
# Install OpenMP support
sudo apt-get install libomp-dev

# Verify GCC version
gcc --version
```

## 👨‍💻 Author

**Student:** Geeth Seneviratne 
**Student ID:** IT23226128  
**Course:** BSc (Hons) in Computer Science - Year 3  
**Module:** SE3082 - Parallel Computing  
**Assignment:** 03 - OpenMP Parallel Quick Sort  

---
