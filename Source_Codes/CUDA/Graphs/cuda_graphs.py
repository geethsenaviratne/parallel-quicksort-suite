

import matplotlib.pyplot as plt
import csv

# Performance data from actual CUDA tests (1M elements)
block_sizes = [64, 128, 256, 512]
execution_time = [0.292133, 0.172404, 0.086914, 0.046930]
throughput = [3.42, 5.80, 11.51, 21.31]  # Million elements/sec

# Calculate speedup (compared to serial: 0.727s for 10M, scaled to 1M)
# For 1M elements, serial would be approximately 0.0727s
serial_time_1M = 0.0727  # Estimated serial time for 1M elements
speedup = []
for time in execution_time:
    speedup.append(serial_time_1M / time)

print("Generating CUDA Quick Sort performance graphs...")
print(f"\nSerial baseline (1M): {serial_time_1M:.4f}s (estimated)")

# =================================================================
# GRAPH 1: BLOCK SIZE VS EXECUTION TIME
# =================================================================

fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(block_sizes, execution_time, marker='o', linewidth=3, markersize=10, 
         color='#FF6B35', label='Execution Time')
ax1.set_xlabel('Block Size (Threads per Block)', fontsize=14, fontweight='bold')
ax1.set_ylabel('Execution Time (seconds)', fontsize=14, fontweight='bold')
ax1.set_title('CUDA Quick Sort: Block Size vs Execution Time\n(1 Million Elements, RTX 4060)', 
              fontsize=16, fontweight='bold', pad=20)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_xticks(block_sizes)
ax1.legend(fontsize=12)

# Add colored value labels
for bs, time in zip(block_sizes, execution_time):
    ax1.annotate(f'{time:.6f}s', (bs, time), textcoords="offset points", 
                 xytext=(0,15), ha='center', fontsize=11, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFD700', 
                          edgecolor='black', linewidth=1.5))

plt.tight_layout()
plt.savefig('graph1_blocksize_vs_time.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Graph 1: graph1_blocksize_vs_time.png")

# =================================================================
# GRAPH 2: BLOCK SIZE VS SPEEDUP
# =================================================================

fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(block_sizes, speedup, marker='s', linewidth=3, markersize=10, 
         color='#4ECDC4', label='Actual Speedup')
ax2.set_xlabel('Block Size (Threads per Block)', fontsize=14, fontweight='bold')
ax2.set_ylabel('Speedup (times)', fontsize=14, fontweight='bold')
ax2.set_title('CUDA Quick Sort: Block Size vs Speedup\n(1 Million Elements, RTX 4060)', 
              fontsize=16, fontweight='bold', pad=20)
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.set_xticks(block_sizes)
ax2.legend(fontsize=12)

# Add colored value labels
for bs, sp in zip(block_sizes, speedup):
    ax2.annotate(f'{sp:.2f}x', (bs, sp), textcoords="offset points", 
                 xytext=(0,15), ha='center', fontsize=11, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#C0F0C0', 
                          edgecolor='black', linewidth=1.5))

plt.tight_layout()
plt.savefig('graph2_blocksize_vs_speedup.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Graph 2: graph2_blocksize_vs_speedup.png")

# =================================================================
# COMBINED GRAPH (2 graphs side by side)
# =================================================================

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('CUDA Quick Sort Performance Analysis (NVIDIA RTX 4060 Laptop, 1 Million Elements)', 
             fontsize=18, fontweight='bold', y=1.02)

# Left: Time
axes[0].plot(block_sizes, execution_time, marker='o', linewidth=3, 
             markersize=10, color='#FF6B35')
axes[0].set_xlabel('Block Size (Threads per Block)', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Execution Time (seconds)', fontsize=12, fontweight='bold')
axes[0].set_title('Block Size vs Execution Time', fontsize=13, fontweight='bold')
axes[0].grid(True, alpha=0.3, linestyle='--')
axes[0].set_xticks(block_sizes)
for bs, time in zip(block_sizes, execution_time):
    axes[0].annotate(f'{time:.3f}s', (bs, time), textcoords="offset points", 
                     xytext=(0,10), ha='center', fontsize=10, fontweight='bold')

# Right: Speedup
axes[1].plot(block_sizes, speedup, marker='s', linewidth=3, 
             markersize=10, color='#4ECDC4')
axes[1].set_xlabel('Block Size (Threads per Block)', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Speedup (times)', fontsize=12, fontweight='bold')
axes[1].set_title('Block Size vs Speedup', fontsize=13, fontweight='bold')
axes[1].grid(True, alpha=0.3, linestyle='--')
axes[1].set_xticks(block_sizes)
for bs, sp in zip(block_sizes, speedup):
    axes[1].annotate(f'{sp:.2f}x', (bs, sp), textcoords="offset points", 
                     xytext=(0,10), ha='center', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('combined_graphs.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Combined: combined_graphs.png")

# =================================================================
# SUMMARY
# =================================================================

print("\n" + "="*70)
print("CUDA QUICK SORT PERFORMANCE SUMMARY")
print("="*70)
print(f"GPU: NVIDIA GeForce RTX 4060 Laptop")
print(f"Algorithm: Quick Sort (segments) + Bitonic Merge (GPU)")
print(f"Array Size: 1,000,000 elements\n")
print(f"{'Block Size':<12} {'Time (s)':<14} {'Speedup':<12} {'Throughput':<15}")
print("-" * 70)
for bs, time, sp, tp in zip(block_sizes, execution_time, speedup, throughput):
    print(f"{bs:<12} {time:<14.6f} {sp:<12.2f} {tp:<15.2f} M/s")
print("="*70)

# Find best configuration
best_idx = execution_time.index(min(execution_time))
print(f"\n✅ Best Configuration: {block_sizes[best_idx]} threads/block")
print(f"   Best Time: {min(execution_time):.6f} seconds")
print(f"   Best Speedup: {max(speedup):.2f}x")
print(f"   Peak Throughput: {max(throughput):.2f} million elements/second")

# Performance improvement analysis
print(f"\n📊 Performance Improvement:")
print(f"   64 → 512: {execution_time[0]/execution_time[-1]:.2f}x faster")
print(f"   Time reduced by: {((execution_time[0] - execution_time[-1]) / execution_time[0] * 100):.1f}%")
print("="*70)

print("\n✅ All 3 graphs generated successfully!")
print("\nGenerated files:")
print("  1. graph1_blocksize_vs_time.png       (Individual)")
print("  2. graph2_blocksize_vs_speedup.png    (Individual)")
print("  3. combined_graphs.png                (Both together)")
print("="*70)



# Generate CSV file
csv_filename = "cuda_quicksort_results.csv"

with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    # Write header row
    writer.writerow(["Block Size", "Array Size", "Execution Time (s)", "Speedup"])
    
    # Write data rows
    for bs, time, sp, tp in zip(block_sizes, execution_time, speedup, throughput):
        writer.writerow([bs, 1000000, time, f"{sp:.2f}"])

print(f"\n✓ CSV file generated: {csv_filename}")
