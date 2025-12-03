#!/usr/bin/env python3
"""
OpenMP QuickSort Performance Graphs Generator
Student: Kavin (IT23226128)
Updated with new results and colored labels
"""

import matplotlib.pyplot as plt

# Updated Performance data using Serial baseline
threads = [1, 2, 4, 8, 16]
execution_time = [0.693676, 0.625962, 0.363606, 0.202783, 0.137115]
throughput = [14.42, 15.98, 27.50, 49.31, 72.93]
serial_time = 1.512392  # baseline serial execution time

# Calculate speedup and efficiency using Serial baseline
speedup = []
efficiency = []
for i in range(len(threads)):
    sp = serial_time / execution_time[i]
    speedup.append(sp)
    eff = (sp / threads[i]) * 100
    efficiency.append(eff)

ideal_speedup = [1, 2, 4, 8, 16]

print("Generating graphs with colored labels using serial baseline...")

# Graph 1: Execution Time
fig1, ax1 = plt.subplots(figsize=(10, 6))
ax1.plot(threads, execution_time, marker='o', linewidth=3, markersize=10, color='#2E86AB')
ax1.set_xlabel('Number of Threads', fontsize=14, fontweight='bold')
ax1.set_ylabel('Execution Time (seconds)', fontsize=14, fontweight='bold')
ax1.set_title('Threads vs Execution Time\n(10 Million Elements)', fontsize=16, fontweight='bold')
ax1.grid(True, alpha=0.3)
ax1.set_xticks(threads)

for t, time in zip(threads, execution_time):
    ax1.annotate(f'{time:.6f}s', (t, time), textcoords="offset points", 
                 xytext=(0,15), ha='center', fontsize=10, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFD700', 
                          edgecolor='black', linewidth=1.5))

plt.tight_layout()
plt.savefig('graph1_threads_vs_time.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Graph 1: graph1_threads_vs_time.png")

# Graph 2: Speedup
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.plot(threads, speedup, marker='o', linewidth=3, markersize=10, color='#A23B72', 
         label='Actual Speedup', zorder=3)
ax2.plot(threads, ideal_speedup, linestyle='--', linewidth=3, color='#F18F01', 
         alpha=0.8, label='Ideal Linear', zorder=2)
ax2.set_xlabel('Number of Threads', fontsize=14, fontweight='bold')
ax2.set_ylabel('Speedup (times)', fontsize=14, fontweight='bold')
ax2.set_title('Threads vs Speedup\n(10 Million Elements)', fontsize=16, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.set_xticks(threads)
ax2.legend(fontsize=12)

for t, sp in zip(threads, speedup):
    ax2.annotate(f'{sp:.2f}x', (t, sp), textcoords="offset points", 
                 xytext=(0,15), ha='center', fontsize=10, fontweight='bold',
                 bbox=dict(boxstyle='round,pad=0.5', facecolor="#C0F0C0", 
                          edgecolor='black', linewidth=1.5))

plt.tight_layout()
plt.savefig('graph2_threads_vs_speedup.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Graph 2: graph2_threads_vs_speedup.png")

# Graph 3: Efficiency
fig3, ax3 = plt.subplots(figsize=(10, 6))
bars = ax3.bar(threads, efficiency, color='#06A77D', alpha=0.8, edgecolor='black', linewidth=1.5)
ax3.set_xlabel('Number of Threads', fontsize=14, fontweight='bold')
ax3.set_ylabel('Efficiency (%)', fontsize=14, fontweight='bold')
ax3.set_title('Threads vs Efficiency\n(10 Million Elements)', fontsize=16, fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')
ax3.set_xticks(threads)
ax3.set_ylim([0, 250])

for bar, eff in zip(bars, efficiency):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height, f'{eff:.2f}%',
            ha='center', va='bottom', fontsize=10, fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.4', facecolor="#E9CACF", 
                     edgecolor='black', linewidth=1.5))

plt.tight_layout()
plt.savefig('graph3_threads_vs_efficiency.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Graph 3: graph3_threads_vs_efficiency.png")

# Combined Graph
fig, axes = plt.subplots(1, 2, figsize=(20, 6))
fig.suptitle('OpenMP QuickSort Performance Analysis (10 Million Elements)', 
             fontsize=18, fontweight='bold')

# Time
axes[0].plot(threads, execution_time, marker='o', linewidth=2.5, markersize=9, color='#2E86AB')
axes[0].set_xlabel('Threads', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Time (s)', fontsize=12, fontweight='bold')
axes[0].set_title('Execution Time', fontsize=13, fontweight='bold')
axes[0].grid(True, alpha=0.3)
axes[0].set_xticks(threads)
for t, time in zip(threads, execution_time):
    axes[0].annotate(f'{time:.3f}', (t, time), textcoords="offset points", 
                     xytext=(0,10), ha='center', fontsize=9, fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFD700', 
                              edgecolor='black', linewidth=1))

# Speedup
axes[1].plot(threads, speedup, marker='o', linewidth=2.5, markersize=9, color='#A23B72', 
             label='Actual', zorder=3)
axes[1].plot(threads, ideal_speedup, linestyle='--', linewidth=2.5, color='#F18F01', 
             alpha=0.7, label='Ideal', zorder=2)
axes[1].set_xlabel('Threads', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Speedup', fontsize=12, fontweight='bold')
axes[1].set_title('Speedup', fontsize=13, fontweight='bold')
axes[1].grid(True, alpha=0.3)
axes[1].set_xticks(threads)
axes[1].legend(fontsize=9)
for t, sp in zip(threads, speedup):
    axes[1].annotate(f'{sp:.2f}', (t, sp), textcoords="offset points", 
                     xytext=(0,10), ha='center', fontsize=9, fontweight='bold',
                     bbox=dict(boxstyle='round,pad=0.3', facecolor='#C0F0C0', 
                              edgecolor='black', linewidth=1))

plt.tight_layout()
plt.savefig('combined_all_graphs.png', dpi=300, bbox_inches='tight')
plt.close()
print("Combined: execution time and speedup.png")

print("\n" + "="*60)
print("PERFORMANCE SUMMARY")
print("="*60)
print(f"Array Size: 10,000,000 elements\n")
print(f"{'Threads':<10} {'Time (s)':<12} {'Speedup':<12} {'Efficiency':<12}")
print("-" * 60)
for t, time, sp, eff in zip(threads, execution_time, speedup, efficiency):
    print(f"{t:<10} {time:<12.6f} {sp:<12.2f} {eff:<12.2f}%")
print("="*60)
print(f"\nBest Speedup: {max(speedup):.2f}x with {threads[speedup.index(max(speedup))]} threads")
print(f"Best Efficiency: {max(efficiency):.2f}% with {threads[efficiency.index(max(efficiency))]} threads")
print(f"Peak Throughput: {max(throughput):.2f} million elements/second")
print(f"Time Reduction: {((execution_time[0] - execution_time[-1]) / execution_time[0] * 100):.1f}%")
print("="*60)
print("\nAll 4 graphs generated successfully!")