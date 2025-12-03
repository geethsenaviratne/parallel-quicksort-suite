import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#results (from your run outputs)

def default_data_df():
    data = {
        'Implementation': [
            'Serial',
            'OpenMP (8 threads)',
            'MPI (8 processes)',
            'CUDA (256 blocks)'
        ],
        'ExecutionTimeSeconds': [
            1.589532,   # Serial
            0.208704,   # OpenMP (8 threads)
            0.220486,   # MPI (8 processes)
            1.228265    # CUDA (block size 256)
        ]
    }
    return pd.DataFrame(data)


# Color mapping 

COLORS = {
    'Serial': '#B0B0B0',               # gray baseline
    'OpenMP (8 threads)': '#1f77b4',   # blue
    'MPI (8 processes)': '#2ca02c',    # green     
    'CUDA (256 blocks)': '#d62728',    # red
}


# Data loaders & helpers

def load_data_from_csv(path):
    df = pd.read_csv(path)
    expected = ['Implementation', 'ExecutionTimeSeconds']
    if not all(col in df.columns for col in expected):
        raise ValueError(f"CSV must contain columns: {expected}")
    return df[['Implementation', 'ExecutionTimeSeconds']].copy()

def ensure_serial_first(df):
    if 'Serial' in df['Implementation'].values:
        serial_row = df[df['Implementation'] == 'Serial']
        others = df[df['Implementation'] != 'Serial']
        df = pd.concat([serial_row, others], ignore_index=True)
    return df

def compute_speedup(df):
    df = df.copy()
    df['ExecutionTimeSeconds'] = df['ExecutionTimeSeconds'].astype(float)
    serial_rows = df[df['Implementation'].str.lower() == 'serial']
    if not serial_rows.empty:
        baseline = float(serial_rows.iloc[0]['ExecutionTimeSeconds'])
    else:
        baseline = float(df.iloc[0]['ExecutionTimeSeconds'])
        print(f"Warning: 'Serial' not found; using '{df.iloc[0]['Implementation']}' as baseline ({baseline}s).")
    df['Speedup'] = df['ExecutionTimeSeconds'].apply(lambda t: baseline / t if t != 0 else float('inf'))
    return df, baseline

def _get_colors_for_impl(impl_list, enforce_serial_gray=True):
    colors = []
    for name in impl_list:
        if name in COLORS:
            c = COLORS[name]
        else:
            lname = name.lower()
            if 'serial' in lname:
                c = COLORS.get('Serial', '#B0B0B0')
            elif 'openmp' in lname:
                c = COLORS.get('OpenMP (8 threads)', '#1f77b4')
            elif 'mpi' in lname:
                c = COLORS.get('MPI (8 processes)', '#2ca02c')
            elif 'cuda' in lname:
                c = COLORS.get('CUDA', '#d62728')
            else:
                c = '#7f7f7f'
        colors.append(c)
    # Ensure serial bar is gray if it's the first and enforce_serial_gray True
    if enforce_serial_gray and len(impl_list) > 0 and 'serial' in impl_list[0].lower():
        colors[0] = COLORS.get('Serial', colors[0])
    return colors

# -------------------------
# Plot functions (style matching your example)
# -------------------------
def plot_execution_time(df, out_path, title='Comparative Execution Time'):
    impl = df['Implementation'].tolist()
    times = df['ExecutionTimeSeconds'].tolist()
    colors = _get_colors_for_impl(impl)

    fig, ax = plt.subplots(figsize=(10,5))
    bars = ax.bar(impl, times, color=colors, edgecolor='black', linewidth=1.0, alpha=0.95, zorder=3)

    ax.yaxis.grid(True, linestyle='-', linewidth=0.6, alpha=0.6, zorder=0)
    ax.set_axisbelow(True)

    ax.set_title(title, fontsize=16, weight='bold', pad=10)
    ax.set_ylabel('Execution Time (seconds)', fontsize=12)
    ax.set_xticklabels(impl, rotation=0, fontsize=11)

    # annotate bar tops with seconds suffix and bold text
    for rect in bars:
        h = rect.get_height()
        ax.annotate(f'{h:.4f}s',
                    xy=(rect.get_x() + rect.get_width()/2, h),
                    xytext=(0, 8),
                    textcoords='offset points',
                    ha='center', va='bottom', fontsize=10, weight='bold')

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor='white')
    plt.close()
    print(f"Saved execution time chart: {out_path}")

def plot_speedup(df, out_path, title='Comparative Speedup vs Serial'):
    impl = df['Implementation'].tolist()
    speedups = df['Speedup'].tolist()
    colors = _get_colors_for_impl(impl)

    fig, ax = plt.subplots(figsize=(10,5))
    bars = ax.bar(impl, speedups, color=colors, edgecolor='black', linewidth=1.0, alpha=0.95, zorder=3)

    # dashed baseline at 1x
    ax.axhline(1, color='#666666', linestyle='--', linewidth=1.0, zorder=1)

    ax.yaxis.grid(True, linestyle='-', linewidth=0.6, alpha=0.6, zorder=0)
    ax.set_axisbelow(True)

    ax.set_title(title, fontsize=16, weight='bold', pad=10)
    ax.set_ylabel('Speedup', fontsize=12)

    # annotate with 'x' suffix, bold, on top of bars
    for rect, s in zip(bars, speedups):
        ax.annotate(f'{s:.2f}x',
                    xy=(rect.get_x() + rect.get_width()/2, s),
                    xytext=(0, 8),
                    textcoords='offset points',
                    ha='center', va='bottom', fontsize=11, weight='bold')

    # add headroom above highest bar
    max_s = max(speedups) if len(speedups) > 0 else 1
    ax.set_ylim(0, max(max_s * 1.15, 1.5))

    ax.set_xticklabels(impl, rotation=0, fontsize=11)

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor='white')
    plt.close()
    print(f"Saved speedup chart: {out_path}")

def plot_combined(df, out_path):
    impl = df['Implementation'].tolist()
    times = df['ExecutionTimeSeconds'].tolist()
    speedups = df['Speedup'].tolist()
    colors = _get_colors_for_impl(impl)

    fig, axes = plt.subplots(1, 2, figsize=(14,5))

    # left: execution time
    ax = axes[0]
    bars1 = ax.bar(impl, times, color=colors, edgecolor='black', linewidth=1.0, alpha=0.95, zorder=3)
    ax.yaxis.grid(True, linestyle='-', linewidth=0.6, alpha=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.set_title('Comparative Execution Time', fontsize=14, weight='bold')
    ax.set_ylabel('Execution Time (seconds)', fontsize=11)
    ax.set_xticklabels(impl, rotation=0, fontsize=10)
    for rect in bars1:
        h = rect.get_height()
        ax.annotate(f'{h:.4f}s', xy=(rect.get_x()+rect.get_width()/2, h),
                    xytext=(0,6), textcoords='offset points', ha='center', va='bottom', fontsize=9, weight='bold')

    # right: speedup
    ax = axes[1]
    bars2 = ax.bar(impl, speedups, color=colors, edgecolor='black', linewidth=1.0, alpha=0.95, zorder=3)
    ax.axhline(1, color='#666666', linestyle='--', linewidth=1.0, zorder=1)
    ax.yaxis.grid(True, linestyle='-', linewidth=0.6, alpha=0.6, zorder=0)
    ax.set_axisbelow(True)
    ax.set_title('Comparative Speedup vs Serial', fontsize=14, weight='bold')
    ax.set_ylabel('Speedup', fontsize=11)
    ax.set_xticklabels(impl, rotation=0, fontsize=10)
    for rect, s in zip(bars2, speedups):
        ax.annotate(f'{s:.2f}x', xy=(rect.get_x()+rect.get_width()/2, s),
                    xytext=(0,6), textcoords='offset points', ha='center', va='bottom', fontsize=9, weight='bold')

    max_s = max(speedups) if len(speedups) > 0 else 1
    axes[1].set_ylim(0, max(max_s * 1.15, 1.5))

    plt.tight_layout()
    plt.savefig(out_path, dpi=300, facecolor='white')
    plt.close()
    print(f"Saved combined chart: {out_path}")

# -------------------------
# Main routine
# -------------------------
def main(argv):
    # optional CSV: Implementation,ExecutionTimeSeconds
    if len(argv) >= 2:
        csv_path = argv[1]
        if not os.path.exists(csv_path):
            print(f"CSV file not found: {csv_path}")
            return
        df = load_data_from_csv(csv_path)
    else:
        df = default_data_df()

    df = ensure_serial_first(df)
    df, baseline = compute_speedup(df)

    out_dir = 'charts'
    os.makedirs(out_dir, exist_ok=True)

    plot_execution_time(df, os.path.join(out_dir, 'execution_time.png'))
    plot_speedup(df, os.path.join(out_dir, 'speedup.png'))
    plot_combined(df, os.path.join(out_dir, 'combined.png'))

    # save CSV with speedup for records
    out_csv = os.path.join(out_dir, 'results_with_speedup.csv')
    df.to_csv(out_csv, index=False)
    print(f"Saved results CSV: {out_csv}")

if __name__ == '__main__':
    main(sys.argv)
