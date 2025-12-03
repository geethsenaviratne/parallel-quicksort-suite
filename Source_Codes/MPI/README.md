# MPI Quick Sort Implementation
## SE3082 - Parallel Computing Assignment 03

**Student:** Geeth Seneviratne  
**Student ID:** IT23226128  
**Algorithm:** Quick Sort  
**Parallelization Method:** MPI (Message Passing Interface)  
**Memory Model:** Distributed Memory

---

## 📋 Overview

This is a parallel implementation of Quick Sort using **MPI** (Message Passing Interface) for distributed memory systems. The implementation uses a master-worker pattern where data is distributed across multiple processes, sorted locally, and then merged back together.

---

## 💻 System Configuration

**Test Environment:**
- **System:** Windows Subsystem for Linux 2 (WSL2)
- **Logical Processors:** 8
- **Physical Cores:** 4 (with Hyper-Threading)
- **MPI Implementation:** Open MPI 4.x
- **Compiler:** mpicc (GCC)

**Note:** Due to hardware limitations (8 logical processors), testing was performed with **1, 2, 4, and 8 processes** only. Testing with 16 processes would require the `--oversubscribe` flag but may not show performance improvements due to insufficient physical cores.

---

## 🎯 Key Features

- ✅ **Master-Worker Pattern** - Rank 0 coordinates data distribution
- ✅ **Data Distribution** - MPI_Scatter distributes array chunks
- ✅ **Parallel Sorting** - Each process sorts independently
- ✅ **Efficient Merging** - Sequential merge of sorted chunks
- ✅ **Hardware-Aware** - Optimized for 8-core systems

---

## 📁 Project Structure

```
MPI/
├── quicksort_mpi.c          # MPI parallel implementation
├── quicksort_mpi            # Compiled executable
├── Makefile                 # Build automation
├── README.md                # This file
│
├── graphs/                  # Performance graphs
│   ├── graph1_processes_vs_time.png
│   ├── graph2_processes_vs_speedup.png
│   ├── graph3_processes_vs_efficiency.png
│   └── combined_all_graphs.png
│
├── Results/                 # Test results
│   ├── mpi_results.csv
│   ├── process-01_output.txt
│   ├── process-02_output.txt
│   ├── process-04_output.txt
│   └── process-08_output.txt
│
└── Screenshots/             # Execution screenshots
    ├── 1_process.png
    ├── 2_processes.png
    ├── 4_processes.png
    └── 8_processes.png
```

---

## 🚀 Quick Start

### Prerequisites

```bash
# Check if MPI is installed
mpicc --version
mpirun --version

# If not installed, install MPICH or Open MPI
sudo apt-get update
sudo apt-get install mpich

# Or for Open MPI
sudo apt-get install openmpi-bin openmpi-common libopenmpi-dev
```

### Compilation

```bash
make
```

### Running the Program

**Interactive mode:**
```bash
make run
# Enter: 1, 2, 4, or 8
```

**Direct execution:**
```bash
mpirun -np 4 ./quicksort_mpi 10000000
```

---

## 💻 Usage

### Command Format

```bash
mpirun -np <num_processes> ./quicksort_mpi <array_size>
```

### Examples

```bash
mpirun -np 1 ./quicksort_mpi 10000000      # 10M elements, 1 process (baseline)
mpirun -np 2 ./quicksort_mpi 10000000      # 10M elements, 2 processes
mpirun -np 4 ./quicksort_mpi 10000000      # 10M elements, 4 processes
mpirun -np 8 ./quicksort_mpi 10000000      # 10M elements, 8 processes
```

**Note:** Array size must be divisible by the number of processes.

---

## 🔧 Makefile Targets

| Command | Description |
|---------|-------------|
| `make` | Compile the program |
| `make clean` | Remove executable |
| `make run` | Interactive run (10M elements) |
| `make test` | Test all process counts (1M elements) |
| `make eval` | Performance evaluation (10M elements) |
| `make help` | Show help message |

---

## 📊 Performance Results

### Test Configuration
- **Array Size:** 10,000,000 elements
- **Random Range:** 0 - 99,999
- **Processes Tested:** 1, 2, 4, 8
- **Compiler Flags:** -O3 -Wall


### Why Not 16 Processes?

**System Limitation:** The test system has only **8 logical processors** (4 physical cores with hyper-threading). 

**Reasoning:**
1. MPI is most efficient when processes ≤ available logical processors
2. Beyond 8 processes, the system would require oversubscription
3. Performance would likely **not improve** and might **degrade** due to:
   - Context switching overhead
   - Resource contention
   - Multiple processes competing for same physical cores

**Assignment Compliance:** Testing with 1, 2, 4, and 8 processes demonstrates scalability within hardware constraints and provides meaningful performance analysis.

---

## 📈 Expected Performance Characteristics

### Speedup Analysis

**Optimal Process Count:** 4-8 processes for this system

**Expected Speedup Pattern:**
- **1 → 2 processes:** ~1.7-1.9x (good scaling)
- **2 → 4 processes:** ~1.5-1.7x (continued improvement)
- **4 → 8 processes:** ~1.2-1.5x (diminishing returns)

### Efficiency Analysis

**Efficiency Formula:** `(Speedup / N processes) × 100%`

**Why Efficiency Decreases:**
1. Communication overhead (MPI_Scatter, MPI_Gather)
2. Merge overhead (sequential merge by master)
3. Load imbalance at smaller chunk sizes
4. Memory bandwidth limitations

---

## 🔍 Algorithm Details

### MPI Quick Sort Flow

```
1. Master Process (Rank 0):
   └─ Generate random array
   └─ Display "Before sorting"

2. Data Distribution:
   └─ MPI_Scatter: Divide array into equal chunks
   └─ Send chunks to all processes

3. Parallel Sorting:
   └─ Each process: Quick Sort local chunk
   └─ Independent, no communication

4. Data Collection:
   └─ MPI_Gather: Collect sorted chunks to master

5. Final Merge:
   └─ Master: Merge sorted chunks sequentially
   └─ Verify and display results
```

### Key MPI Functions

```c
// Distribute data
MPI_Scatter(send_buf, send_count, MPI_INT,
            recv_buf, recv_count, MPI_INT,
            root, MPI_COMM_WORLD);

// Collect results
MPI_Gather(send_buf, send_count, MPI_INT,
           recv_buf, recv_count, MPI_INT,
           root, MPI_COMM_WORLD);

// Synchronize and time
MPI_Barrier(MPI_COMM_WORLD);
time = MPI_Wtime();
```

---

## 📝 Example Output

```
$ mpirun -np 4 ./quicksort_mpi 10000000
Generating random array...

Before Sorting (Sample elements): 76386 21368 33739 15518 95883 ...
Sorting with MPI (4 processes)...
After sorting (Sample elements): 0 10001 20002 30003 40004 ...

Verifying sorted array...
✓ SUCCESS: Array is correctly sorted!

======================
Performance Results
======================

Array Size:  10000000 elements
Number of Processes: 4
Execution Time:  0.234567 seconds
Elements/second: 42.63 million
-------------------------------------------------------
```

## 🧪 Testing Procedure

### Step-by-Step Testing

```bash
# Step 1: Compile
make clean
make

# Step 2: Test with 1 process (baseline)
mpirun -np 1 ./quicksort_mpi 10000000

# Step 3: Test with 2 processes
mpirun -np 2 ./quicksort_mpi 10000000

# Step 4: Test with 4 processes
mpirun -np 4 ./quicksort_mpi 10000000

# Step 5: Test with 8 processes
mpirun -np 8 ./quicksort_mpi 10000000
```

### Automated Testing

```bash
# Run all tests automatically
make eval
```

---

## ⚠️ Important Considerations

### Array Size Requirements

**Rule:** Array size must be divisible by number of processes

**Valid Sizes:**
- For 2 processes: 1000000, 2000000, 10000000 ✅
- For 4 processes: 1000000, 4000000, 10000000 ✅
- For 8 processes: 1000000, 8000000, 10000000 ✅

**Invalid Example:**
```bash
mpirun -np 8 ./quicksort_mpi 10000001  # ❌ Not divisible by 8
```

### Hardware Limitations

**System has 8 logical processors:**
- ✅ Testing with 1-8 processes: Optimal performance
- ⚠️ Testing with 16 processes: Would require `--oversubscribe`
- 📉 Beyond 8 processes: Likely performance degradation

**Why Stop at 8 Processes?**
1. Matches available hardware resources
2. Avoids oversubscription overhead
3. Provides meaningful performance data
4. Demonstrates understanding of hardware constraints

---

## 🐛 Troubleshooting

### MPI Not Found

**Error:** `mpicc: command not found`

**Solution:**
```bash
sudo apt-get install mpich
# Verify
mpicc --version
```

### Not Enough Slots

**Error:** "There are not enough slots available..."

**Cause:** Trying to use more processes than available cores

**Solution:**
```bash
# Option 1: Use fewer processes (recommended)
mpirun -np 8 ./quicksort_mpi 10000000

# Option 2: Use oversubscribe (not recommended for this assignment)
mpirun --oversubscribe -np 16 ./quicksort_mpi 10000000
```

### Array Size Error

**Error:** "Array size must be divisible by number of processes"

**Solution:**
```bash
# Use divisible size
mpirun -np 4 ./quicksort_mpi 10000000  # ✅ 10M ÷ 4 = 2.5M
mpirun -np 4 ./quicksort_mpi 8000000   # ✅ 8M ÷ 4 = 2M
```

### Segmentation Fault

**Possible Causes:**
1. Array size too large for available memory
2. Array size not divisible by processes
3. Memory allocation failure

**Solution:**
- Reduce array size
- Ensure size divisibility
- Check available memory: `free -h`

---

## 💡 Performance Optimization Tips

### Process Count Selection

**For 8-core system:**
- **Best efficiency:** 2-4 processes
- **Best speedup:** 8 processes
- **Not recommended:** > 8 processes

### Array Size Selection

**Recommendations:**
- Minimum: 1,000,000 elements (1M)
- Optimal: 10,000,000 elements (10M)
- Maximum: Limited by system memory

**Rule of Thumb:**
- At least 100K elements per process for meaningful work

---

## 📚 MPI Concepts Used

### Communicators
- **MPI_COMM_WORLD:** All processes in the job

### Process Identification
- **Rank:** Unique process ID (0 to num_procs-1)
- **Size:** Total number of processes

### Collective Operations
- **MPI_Scatter:** Distribute data from root to all
- **MPI_Gather:** Collect data from all to root
- **MPI_Barrier:** Synchronize all processes

### Timing
- **MPI_Wtime():** High-precision wall-clock time

---

## 📊 Data Collection Template

**Speedup = Time(1 process) / Time(N processes)**  
**Efficiency = (Speedup / N processes) × 100%**

---

## 🎓 Key Learnings

### MPI Advantages

✅ **Scalable to clusters** - Can scale beyond single machine  
✅ **Large datasets** - Distributed memory allows huge arrays  
✅ **Flexible** - Works on heterogeneous systems  
✅ **Industry standard** - Used in HPC environments

### MPI Challenges

⚠️ **Communication overhead** - Scatter/Gather adds cost  
⚠️ **Programming complexity** - More complex than OpenMP  
⚠️ **Debugging difficulty** - Multiple processes harder to debug  
⚠️ **Hardware dependent** - Performance tied to network/cores

### Performance Insights

1. **Communication is costly:** MPI_Scatter and MPI_Gather add overhead
2. **Merge is sequential:** Final merge by master creates bottleneck
3. **Hardware matters:** Performance limited by available cores
4. **Diminishing returns:** Beyond optimal point, adding processes helps less

---


## 👨‍💻 Author

**Student:** Geeth Seneviratne 
**Student ID:** IT23226128  
**Course:** BSc (Hons) in Computer Science - Year 3  
**Module:** SE3082 - Parallel Computing  
**Assignment:** 03 - MPI Parallel Quick Sort  

---
