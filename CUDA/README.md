# CUDA Quick Sort Implementation
## SE3082 - Parallel Computing Assignment 03

**Student:** Geeth Seneviratne  
**Student ID:** IT23226128  
**Algorithm:** Hybrid Quick Sort (Quick Sort + Bitonic Merge)  
**Parallelization Method:** CUDA (GPU Computing)  
**Hardware:** NVIDIA GeForce RTX 4060 Laptop GPU

---

## 📋 Overview

This is a GPU-accelerated sorting implementation using **CUDA** on NVIDIA graphics cards. The implementation uses a **hybrid approach**: parallel Quick Sort for segmentation followed by GPU-based bitonic merge, maintaining Quick Sort algorithm consistency while leveraging GPU parallelism.

---

## 📁 Project Structure
```
CUDA/
├── Graphs/                              # Performance visualization
│   ├── combined_graphs.png             # Combined performance charts
│   ├── cuda_graphs.py                  # Graph generation script
│   ├── cuda_quicksort_results.csv      # Raw performance data
│   ├── graph1_blocksize_vs_time.png    # Block size vs execution time
│   └── graph2_blocksize_vs_speedup.png # Block size vs speedup chart
│
├── Results/                             # Output files from test runs
│   ├── Block-64_output.txt             # 64 block results
│   ├── Block-128_output.txt            # 128 block results
│   ├── Block-256_output.txt            # 256 block results
│   └── Block-512_output.txt            # 512 block results
│
├── Screenshots/                         # Visual documentation
│   ├── Blocks-64.png                   # 64 block screenshot
│   ├── Blocks-128.png                  # 128 block screenshot
│   ├── Blocks-256.png                  # 256 block screenshot
│   └── Blocks-512.png                  # 512 block screenshot
│
├── cuda_quicksort                       # Compiled executable
├── cuda_quicksort.cu                    # Main CUDA source code
├── Makefile                             # Build configuration
└── README.md                            # This file
```

### 📂 Directory Details

**`Graphs/`** - Performance analysis and visualization
- Python scripts for generating performance charts
- CSV data from benchmark runs
- PNG charts showing scaling behavior

**`Results/`** - Benchmark output files
- Text files containing execution time and verification results
- One file per block size configuration
- Includes sorting verification status

**`Screenshots/`** - Visual documentation
- Terminal screenshots of program execution
- One screenshot per block size configuration
- Shows real-time performance metrics

---

## 🎮 GPU Specifications

**Hardware:**
- **GPU:** NVIDIA GeForce RTX 4060 Laptop
- **CUDA Cores:** ~3072 cores
- **Memory:** 8 GB GDDR6
- **Compute Capability:** 8.9 (Ada Lovelace)
- **CUDA Version:** 12.7
- **Driver Version:** 566.14

---

## 📊 Performance Results (1M Elements)

| Block Size | Time (s) | Speedup | Throughput | Status |
|:----------:|:--------:|:-------:|:----------:|:------:|
| 64         | 0.292    | 0.25x   | 3.42 M/s   | Slow   |
| 128        | 0.172    | 0.42x   | 5.80 M/s   | Better |
| 256        | 0.087    | 0.84x   | 11.51 M/s  | Good   |
| **512**    | **0.047**| **1.55x**| **21.31 M/s**| **BEST** ⭐ |

**Key Achievements:**
- ✅ **Best Time:** 0.047 seconds (512 threads/block)
- ✅ **Peak Throughput:** 21.31 million elements/second
- ✅ **Scaling:** 6.2x faster (512 vs 64)
- ✅ **All Tests:** 100% verification passed

---

## 🚀 Quick Start

### Compilation
```bash
make
```

### Running
```bash
./cuda_quicksort
# Enter block size: 512
# Enter array size: 1000000
```

### Generating Graphs
```bash
cd Graphs
python3 cuda_graphs.py
```

---

## 🎯 Algorithm

**Phase 1:** Parallel Quick Sort on GPU segments  
**Phase 2:** GPU bitonic merge (no CPU bottleneck!)
```
Phase 1: GPU sorts N segments in parallel
Phase 2: GPU merges sorted segments
Result: 100% GPU processing! 🚀
```

---

## 💡 Key Features

✅ **Hybrid Algorithm** - Quick Sort + Bitonic Merge  
✅ **100% GPU** - No CPU bottleneck  
✅ **Excellent Scaling** - 6.2x improvement  
✅ **Optimal Config** - 512 threads/block  
✅ **Consistent** - Uses Quick Sort algorithm  

---

## 📈 Performance Highlights

- **512 threads/block:** Best performance
- **6.2x improvement:** 64 to 512 scaling
- **21.31 M/s:** Peak throughput
- **83.9% time reduction:** From 0.292s to 0.047s

---

## 🔧 Troubleshooting

**CUDA not found:** `export PATH=/usr/local/cuda/bin:$PATH`  
**GPU not detected:** Check `nvidia-smi`  
**Slow performance:** Use 512 threads/block  

---

## 👨‍💻 Author

**Student:** Geeth Seneviratne  
**Student ID:** IT23226128  
**Course:** BSc (Hons) in Computer Science - Year 3  
**Module:** SE3082 - Parallel Computing  
**Assignment:** 03 - CUDA Parallel Quick Sort  

**GPU-accelerated Quick Sort! 🚀**