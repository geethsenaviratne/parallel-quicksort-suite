#!/usr/bin/env python3
import matplotlib.pyplot as plt

# Updated Performance data using Serial baseline
processes = [1, 2, 4, 8]
execution_time = [0.696363, 0.337406, 0.209390, 0.198653]
throughput = [14.36, 29.64, 47.76, 50.34]
serial_time = 1.512392  # baseline serial execution time

# Calculate speedup and efficiency using Serial baseline
speedup = []
efficiency = []
for i in range(len(processes)):
    sp = serial_time / execution_time[i]
    speedup.append(sp)
    eff = (sp / processes[i]) * 100
    efficiency.append(eff)

# Ideal linear speedup for comparison
ideal_speedup = [1, 2, 4, 8]

print("Generating MPI performance graphs with colored labels using serial baseline...")

# =================================================================
# GRAPH 1: PROCESSES VS EXECUTION TIME
# =================================================================

fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(processes, execution_time, marker='o', linewidth=3, markersize=10, color='#2E86AB')
ax1.set_xlabel('Number of Processes', fontsize=14, fontweight='bold')
ax1.set_ylabel('Execution Time (seconds)', fontsize=14, fontweight='bold')
ax1.set_title('MPI QuickSort: Processes vs Execution Time\n(10 Million Elements)', 
              fontsize=16, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.set_xticks(processes)

# Add colored value labels
for p, time in zip(processes, execution_time):
    ax1.annotate(f'{time:.6f}s', (p, time), textcoords="offset points", 
                 xytext=(0,15), ha='center', fontsize=10, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFD700', 
                          edgecolor='black', linewidth=1.5))

plt.tight_layout()
plt.savefig('graph1_processes_vs_time.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Graph 1: graph1_processes_vs_time.png")

# =================================================================
# GRAPH 2: PROCESSES VS SPEEDUP
# =================================================================

fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(processes, speedup, marker='o', linewidth=3, markersize=10, color='#A23B72', 
         label='Actual Speedup', zorder=3)
ax2.plot(processes, ideal_speedup, linestyle='--', linewidth=3, color='#F18F01', 
         alpha=0.8, label='Ideal Linear', zorder=2)
ax2.set_xlabel('Number of Processes', fontsize=14, fontweight='bold')
ax2.set_ylabel('Speedup (times)', fontsize=14, fontweight='bold')
ax2.set_title('MPI QuickSort: Processes vs Speedup\n(10 Million Elements)', 
              fontsize=16, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.set_xticks(processes)
ax2.legend(fontsize=12)

# Add colored value labels
for p, sp in zip(processes, speedup):
    ax2.annotate(f'{sp:.2f}x', (p, sp), textcoords="offset points", 
                 xytext=(0,15), ha='center', fontsize=10, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#C0F0C0', 
                          edgecolor='black', linewidth=1.5))

plt.tight_layout()
plt.savefig('graph2_processes_vs_speedup.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Graph 2: graph2_processes_vs_speedup.png")

# =================================================================
# GRAPH 3: PROCESSES VS EFFICIENCY
# =================================================================

fig3, ax3 = plt.subplots(figsize=(10, 6))
bars = ax3.bar(processes, efficiency, color='#06A77D', alpha=0.8, edgecolor='black', linewidth=1.5)
ax3.set_xlabel('Number of Processes', fontsize=14, fontweight='bold')
ax3.set_ylabel('Efficiency (%)', fontsize=14, fontweight='bold')
ax3.set_title('MPI QuickSort: Processes vs Efficiency\n(10 Million Elements)', 
              fontsize=16, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')
ax3.set_xticks(processes)
ax3.set_ylim([0, 250])  # Increased to accommodate >100% values

# Add colored value labels on bars
for bar, eff in zip(bars, efficiency):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height, f'{eff:.2f}%',
            ha='center', va='bottom', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor='#E9CACF', 
                     edgecolor='black', linewidth=1.5))

plt.tight_layout()
plt.savefig('graph3_processes_vs_efficiency.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Graph 3: graph3_processes_vs_efficiency.png")

# =================================================================
# COMBINED GRAPH
# =================================================================

fig, axes = plt.subplots(1, 2, figsize=(20, 6))
fig.suptitle('MPI QuickSort Performance Analysis (10 Million Elements, 8-Core System)', 
             fontsize=18, fontweight='bold')

# Time
axes[0].plot(processes, execution_time, marker='o', linewidth=2.5, markersize=9, color='#2E86AB')
axes[0].set_xlabel('Processes', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Time (s)', fontsize=12, fontweight='bold')
axes[0].set_title('Execution Time', fontsize=13, fontweight='bold')
axes[0].grid(True, alpha=0.3)
axes[0].set_xticks(processes)
for p, time in zip(processes, execution_time):
    axes[0].annotate(f'{time:.3f}', (p, time), textcoords="offset points", 
                     xytext=(0,8), ha='center', fontsize=9)

# Speedup
axes[1].plot(processes, speedup, marker='o', linewidth=2.5, markersize=9, color='#A23B72', 
             label='Actual', zorder=3)
axes[1].plot(processes, ideal_speedup, linestyle='--', linewidth=2.5, color='#F18F01', 
             alpha=0.7, label='Ideal', zorder=2)
axes[1].set_xlabel('Processes', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Speedup', fontsize=12, fontweight='bold')
axes[1].set_title('Speedup', fontsize=13, fontweight='bold')
axes[1].grid(True, alpha=0.3)
axes[1].set_xticks(processes)
axes[1].legend(fontsize=9)
for p, sp in zip(processes, speedup):
    axes[1].annotate(f'{sp:.2f}', (p, sp), textcoords="offset points", 
                     xytext=(0,8), ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('combined_all_graphs.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Combined: combined_all_graphs.png")

# =================================================================
# SUMMARY
# =================================================================

print("\n" + "="*60)
print("PERFORMANCE SUMMARY")
print("="*60)
print(f"Array Size: 10,000,000 elements")
print(f"System: 8-core system (tested with 1, 2, 4, 8 processes)\n")
print(f"{'Processes':<10} {'Time (s)':<12} {'Speedup':<12} {'Efficiency':<12}")
print("-" * 60)
for p, time, sp, eff in zip(processes, execution_time, speedup, efficiency):
    print(f"{p:<10} {time:<12.6f} {sp:<12.2f} {eff:<12.2f}%")
print("="*60)
print(f"\nBest Speedup: {max(speedup):.2f}x with {processes[speedup.index(max(speedup))]} processes")
print(f"Best Efficiency: {max(efficiency):.2f}% with {processes[efficiency.index(max(efficiency))]} processes")
print(f"Peak Throughput: {max(throughput):.2f} million elements/second")
print(f"Time Reduction: {((execution_time[0] - execution_time[-1]) / execution_time[0] * 100):.1f}%")
print("="*60)

print("\n✅ All 4 graphs generated successfully!")
