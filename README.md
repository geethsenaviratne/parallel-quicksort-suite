# Parallel Quick Sort Suite 🚀

A comprehensive parallel computing project implementing **Quick Sort** across multiple parallel programming paradigms: **OpenMP**, **MPI**, and **CUDA**. This project demonstrates performance optimization, scalability analysis, and comparative evaluation of different parallel computing approaches.


## 🎯 Overview

This project implements **parallel Quick Sort** using three major parallel computing paradigms:

1. **OpenMP** - Shared-memory parallelism using task-based approach
2. **MPI** - Distributed-memory parallelism using master-worker pattern
3. **CUDA** - GPU parallelism using hybrid Quick Sort + bitonic merge

### Key Features

✅ **Multiple Implementations**: Serial, OpenMP, MPI, and CUDA versions  
✅ **Comprehensive Analysis**: Performance metrics, scalability studies, bottleneck identification  
✅ **Extensive Testing**: 10M element arrays with multiple configurations  
✅ **Detailed Documentation**: Complete report with graphs and analysis  
✅ **Visualization**: Python scripts for generating performance charts  
✅ **Production-Ready**: Optimized thresholds, error handling, and validation  

---

## 🏆 Performance Highlights

### Best Results (10M Elements)

| Implementation | Configuration | Time (s) | Speedup | Efficiency |
|----------------|--------------|----------|---------|------------|
| **Serial** | Baseline | 1.548s | 1.00x | 100% |
| **OpenMP** | 16 threads | **0.137s** | **11.03x** | **69%** |
| **OpenMP** | 8 threads | 0.203s | 7.46x | 93% |
| **MPI** | 8 processes | 0.199s | 7.62x | 95% |
| **CUDA** | 512 blocks (1M) | 0.047s | 1.55x | - |

### Key Achievements

🥇 **OpenMP Winner**: 11.03x speedup (0.137s) - 91% execution time reduction  
🥈 **MPI Strong**: 7.62x speedup, competitive with OpenMP  
🥉 **CUDA Limited**: 1.55x speedup due to Quick Sort's GPU incompatibility  

**⚡ 91% Time Reduction**: From 1.548s to 0.137s using OpenMP with 16 threads!

---

## 📁 Repository Structure

```
parallel-quicksort-suite/
├── Source_Codes/
│   ├── Serial/
│   │   ├── serial.c                    # Serial Quick Sort baseline
│   │   └── serial-output.png           # Execution screenshot
│   ├── OpenMP/
│   │   ├── quicksort_openmp.c          # OpenMP task-based implementation
│   │   ├── Makefile                    # Build configuration
│   │   └── Graphs/                     # OpenMP performance graphs
│   ├── MPI/
│   │   ├── quicksort_mpi.c             # MPI master-worker implementation
│   │   ├── Makefile                    # Build configuration
│   │   └── Graphs/                     # MPI performance graphs
│   └── CUDA/
│       ├── quicksort_cuda.cu           # CUDA hybrid implementation
│       ├── Makefile                    # Build configuration
│       └── Graphs/                     # CUDA performance graphs
├── Data Files/
│   ├── OpenMP-output_files/            # OpenMP CSV results
│   ├── MPI-output_files/               # MPI CSV results
│   └── CUDA-output_files/              # CUDA CSV results
├── Screenshots/
│   ├── OpenMp/                         # OpenMP execution screenshots
│   ├── MPI/                            # MPI execution screenshots
│   └── CUDA/                           # CUDA execution screenshots
├── Report - Quick_Sort.pdf             # Comprehensive analysis report
├── Graph - Graph.pdf                   # Comprehensive graphs
└── README.md                           # This file
```

---

## 🔧 Implementation Details

### 1. Serial Quick Sort (Baseline)

- **Algorithm**: Standard recursive Quick Sort with rightmost pivot
- **Complexity**: O(n log n) average, O(n²) worst case
- **Performance**: 1.548s for 10M elements (6.46 M/s throughput)
- **Purpose**: Baseline for speedup calculations

### 2. OpenMP Implementation

**Approach**: Task-based parallelism with threshold-based switching

```c
#define TASK_THRESHOLD 10000

void quickSortParallel(int arr[], int low, int high) {
    if (low < high) {
        int pi = partition(arr, low, high);
        
        if ((pi - low) > TASK_THRESHOLD && (high - pi) > TASK_THRESHOLD) {
            #pragma omp task
            quickSortParallel(arr, low, pi - 1);
            #pragma omp task
            quickSortParallel(arr, pi + 1, high);
            #pragma omp taskwait
        } else {
            // Serial execution for small subarrays
        }
    }
}
```

**Key Features**:
- ✅ Task-based parallelism with dynamic work-stealing
- ✅ 10,000-element threshold (empirically determined)
- ✅ Automatic load balancing
- ✅ Zero communication overhead (shared memory)

**Performance**:
- **Best**: 11.03x speedup @ 16 threads (0.137s)
- **Optimal Efficiency**: 93% @ 8 threads (0.203s)
- **Super-Linear**: 218% efficiency @ 1 thread (cache effects)

### 3. MPI Implementation

**Approach**: Master-worker pattern with scatter/gather collectives

**Workflow**:
1. Master scatters array segments to all processes
2. Each process sorts its local segment using Quick Sort
3. Master gathers sorted segments
4. Master performs sequential merge of sorted segments

**Key Features**:
- ✅ MPI_Scatter/Gather for communication (deadlock-free)
- ✅ Equal segment distribution
- ✅ Sequential k-way merge (simple, reliable)
- ✅ Collective operations (optimized)

**Performance**:
- **Best**: 7.62x speedup @ 8 processes (0.199s)
- **Efficiency**: 90-95% through 8 processes
- **Communication**: 12% overhead on loopback
- **Scalability**: Limited by sequential merge beyond 8 processes

### 4. CUDA Implementation

**Approach**: Hybrid Quick Sort + bitonic merge on GPU

**Workflow**:
1. Divide array into 512 segments on CPU
2. Transfer segments to GPU
3. Each CUDA block sorts one segment using iterative Quick Sort
4. Perform bitonic merge to combine sorted segments
5. Transfer sorted array back to CPU

**Key Features**:
- ✅ Iterative Quick Sort (GPU recursion limits)
- ✅ Explicit stack management (MAX_DEPTH=16)
- ✅ Insertion sort for small subarrays (<32 elements)
- ✅ Bitonic merge for GPU efficiency
- ✅ 512 blocks optimal for RTX 4060

**Performance**:
- **Best**: 1.55x speedup @ 512 blocks (0.047s for 1M)
- **Configuration**: 6.2x variation (64 blocks → 512 blocks)
- **Limitation**: Quick Sort unsuited to GPU architecture
- **Overhead**: 50% from bitonic merge, 10% from transfers

---

## 📊 Results & Analysis

### Execution Time Comparison

![Execution Time](https://github.com/geethsenaviratne/parallel-quicksort-suite/blob/main/Charts/execution_time.png?raw=true)

**Key Observations**:
- OpenMP and MPI dramatically outperform serial and CUDA
- OpenMP (8T): 0.203s vs Serial: 1.548s = **7.6x faster**
- MPI closely matches OpenMP at 8 workers
- CUDA slower due to algorithm mismatch

### Speedup Comparison

![Speedup Comparison](https://github.com/geethsenaviratne/parallel-quicksort-suite/blob/main/Charts/speedup.png?raw=true)

**Rankings**:
1. 🥇 **OpenMP 16T**: 11.03x speedup
2. 🥈 **MPI 8P**: 7.62x speedup
3. 🥈 **OpenMP 8T**: 7.46x speedup
4. 🥉 **CUDA 512B**: 1.55x speedup (1M elements)

### OpenMP Scaling

![OpenMP Performance](https://github.com/geethsenaviratne/parallel-quicksort-suite/blob/main/Source_Codes/OpenMP/graphs/combined_all_graphs.png?raw=true)

- **Strong Scaling**: Excellent through 8 threads (93% efficiency)
- **Moderate Scaling**: 8→16 threads (69% efficiency due to hyper-threading)
- **Super-Linear**: 1-2 threads show >100% efficiency from cache effects

### MPI Scaling

![MPI Performance](https://github.com/geethsenaviratne/parallel-quicksort-suite/blob/main/Source_Codes/MPI/Graphs/combined_all_graphs.png?raw=true)

- **Near-Linear**: Consistent scaling through 8 processes
- **High Efficiency**: 90-95% maintained
- **Bottleneck**: Sequential merge limits scalability beyond 8 processes

### CUDA Configuration

![CUDA Performance](https://github.com/geethsenaviratne/parallel-quicksort-suite/blob/main/Source_Codes/CUDA/Graphs/combined_graphs.png?raw=true)

- **Critical Configuration**: 512 blocks optimal (6.2x better than 64 blocks)
- **Occupancy**: 85% @ 512 blocks vs 15% @ 64 blocks
- **Algorithm Limit**: Bitonic merge O(n log² n) overhead dominates

---

## 🚀 Installation & Usage

### Prerequisites

```bash
# Compiler requirements
gcc --version          # GCC 9.0+ with OpenMP support
mpicc --version        # MPICH or OpenMPI
nvcc --version         # CUDA Toolkit 11.0+

# System requirements
- Multi-core CPU (8+ cores recommended)
- 4GB+ RAM
- NVIDIA GPU with CUDA support (for CUDA version)
```

### Quick Start

#### 1. Clone Repository

```bash
git clone https://github.com/geethsenaviratne/parallel-quicksort-suite.git
cd parallel-quicksort-suite
```

#### 2. Compile & Run Serial Version

```bash
cd Source_Codes/Serial
gcc -O3 -o serial serial.c
./serial
```

#### 3. Compile & Run OpenMP Version

```bash
cd Source_Codes/OpenMP
make
./quicksort_openmp <array_size> <num_threads>

# Example: 10M elements, 16 threads
./quicksort_openmp 10000000 16
```

#### 4. Compile & Run MPI Version

```bash
cd Source_Codes/MPI
make
mpirun -np <num_processes> ./quicksort_mpi <array_size>

# Example: 10M elements, 8 processes
mpirun -np 8 ./quicksort_mpi 10000000
```

#### 5. Compile & Run CUDA Version

```bash
cd Source_Codes/CUDA
make
./quicksort_cuda <array_size> <num_blocks>

# Example: 1M elements, 512 blocks
./quicksort_cuda 1000000 512
```

### Generate Performance Charts

```bash
cd Charts
python3 compare_graphs.py
```

---

## 💻 Hardware & Software

### Test Environment

**Hardware**:
- **CPU**: AMD Ryzen 7 (8 cores, 16 threads, 3.2-4.5 GHz)
- **RAM**: 16 GB DDR4 3200 MHz
- **GPU**: NVIDIA RTX 4060 Laptop (3072 CUDA cores, 8GB GDDR6)
- **Storage**: NVMe SSD

**Software**:
- **OS**: Ubuntu 22.04 LTS / Windows 11 with WSL2
- **Compilers**: 
  - GCC 11.3.0 with `-O3 -fopenmp`
  - MPICH 4.0.2 / OpenMPI 4.1.2
  - NVCC 12.7 with `-O3 -arch=sm_89`
- **Python**: 3.10+ (for visualization)
- **Libraries**: matplotlib, numpy, pandas

---

## 📖 Documentation

### Complete Report

📄 **[Report - Quick_Sort.pdf](Report%20-%20Quick_Sort.pdf)**

The comprehensive report includes:
- ✅ Parallelization strategies for all implementations
- ✅ Runtime configurations and optimization details
- ✅ Performance analysis with speedup/efficiency metrics
- ✅ Bottleneck identification and scalability limitations
- ✅ Critical reflection on challenges and lessons learned
- ✅ Comparative analysis with recommendations

### Key Findings

1. **OpenMP Best for Workstations**: 11.03x speedup with minimal complexity
2. **Configuration Critical**: 6.2x CUDA variation proves tuning importance
3. **Overhead Dominates**: OpenMP 43%, MPI 40%, CUDA 90% overhead
4. **Algorithm-Hardware Matching**: Quick Sort favors CPU over GPU
5. **Super-Linear Efficiency**: Cache effects, not parallel magic (218% @ 1T)

### Recommendations

**✅ Use OpenMP**: For single workstation Quick Sort (best performance, simplicity)  
**⚠️ Use MPI**: Only for mandatory distributed clusters (requires parallel merge)  
**❌ Avoid CUDA**: For Quick Sort specifically (algorithm mismatch)  

---


## 👤 Author

**Geeth Seneviratne**

- GitHub: [@geethsenaviratne](https://github.com/geethsenaviratne)
- Student ID: IT23226128
- Institution: SLIIT
- Course: SE3082 - Parallel Computing
- Semester: Year 3 Semester 2

---

## 🙏 Acknowledgments

- 13th Gen Intel(R) Core (TM) i7-13620H, 2400 Mhz, 10 Core(s)
- OpenMP, MPI, and CUDA documentation
- Academic advisors and course instructors
- Open-source community

---

## 📚 References

[1] W3Schools, "Quicksort Algorithm – DSA," W3Schools, Accessed: Dec. 3, 2025. [Online]. Available: https://www.w3schools.com/dsa/dsa_algo_quicksort.php

[2] S. Jain, "Parallel Quick Sort Algorithm," Medium, 2023. Accessed: Dec. 3, 2025. [Online]. Available: https://medium.com/@sj.jainsahil1005/parallel-quick-sort-algorithm-ff8b4cb09bad

[3] M. C. Beukman, "Parallel Quicksort using OpenMP," Medium, 2021. Accessed: Dec. 3, 2025. [Online]. Available: https://mcbeukman.medium.com/parallel-quicksort-using-openmp-9d18d7468cac

[4] GeeksforGeeks, "Implementation of Quick Sort using MPI, OMP and POSIX Thread," GeeksforGeeks, Accessed: Dec. 3, 2025. [Online]. Available: https://www.geeksforgeeks.org/dsa/implementation-of-quick-sort-using-mpi-omp-and-posix-thread/

[5] Antas243, "Parallel Quicksort Algorithm," Medium, 2020. Accessed: Dec. 3, 2025. [Online]. Available: https://243-antas.medium.com/parallel-quicksort-algorithm-991cbfc94adc

[6] R. Shankar, "Revisiting Quicksort with Julia and CUDA," Medium, 2019. Accessed: Dec. 3, 2025. [Online]. Available: https://medium.com/swlh/revisiting-quicksort-with-julia-and-cuda-2a997447939b

[7] Red Hat Developers, "Write a GPU algorithm for quicksort," Red Hat, 2024. Accessed: Dec. 3, 2025. [Online]. Available: https://developers.redhat.com/articles/2024/08/22/write-gpu-algorithm-quicksort#the_quicksort_algorithm

[8] OpenMP Architecture Review Board, "OpenMP Application Programming Interface Version 5.2," OpenMP, 2021. [Online]. Available: https://www.openmp.org/specifications/

[9] MPI Forum, "MPI: A Message-Passing Interface Standard Version 4.0," MPI Forum, 2021. [Online]. Available: https://www.mpi-forum.org/docs/

[10] NVIDIA Corporation, "CUDA C++ Programming Guide," NVIDIA Developer Documentation, 2024. [Online]. Available: https://docs.nvidia.com/cuda/cuda-c-programming-guide/

[11] T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein, *Introduction to Algorithms*, 3rd ed. Cambridge, MA: MIT Press, 2009.

---

## 🔗 Quick Links
- 📊 [Performance Charts](Charts/)
- 💻 [Source Codes](Source_Codes/)
- 📸 [Execution Screenshots](Screenshots/)
- 📁 [Raw Data Files](Data%20Files/)

---
