import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

file_path = "../output/latency_.csv"
output_dir = "../output/images/"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

data = pd.read_csv(file_path)

# 원하는 search_methods만 필터링
search_methods = ['exponential', 'mb_bbin', 'ex_mb_bbin', 'mb_slin', 'ex_mb_slin']
datasets = data['dataset'].unique()
fffsize = 10

num_datasets = len(datasets)
num_cols = 2  # Set 2 columns for a 2x2 grid
num_rows = 2  # Explicitly set to 2 rows for 2x2 grid
fig, axes = plt.subplots(num_rows, num_cols)  # Create the subplot grid
cs = plt.cm.tab20c.colors
plt.rcParams.update({'font.size': 16})

title_prefix = ["(a) ", "(b) ", "(c) ", "(d) "]

# 색상 및 마커 설정을 위한 딕셔너리
color_dict = {'mb_slin': cs[2], 'ex_mb_slin': cs[0], 'mb_bbin': cs[6], 'ex_mb_bbin': cs[4], 'exponential': cs[8]}
marker_dict = {'ex_mb_slin': 'o', 'mb_slin': 'o', 'ex_mb_bbin': '^', 'mb_bbin': '^', 'exponential': 's'}

# Initialize handles for the global legend
handles = []

for i, dataset in enumerate(datasets):
    row = i // num_cols
    col = i % num_cols
    ax = axes[row, col] if num_rows > 1 else axes[col]

    dataset_data = data[data['dataset'] == dataset]

    # 필터링된 search_methods에 대해서만 그래프 그리기
    for search_method in search_methods:
        if search_method in dataset_data['search_type'].unique():
            method_data = dataset_data[dataset_data['search_type'] == search_method]

            avg_data = method_data.groupby('density')['lookup_latency'].mean() / 1e6  # ns를 s로 변환하여 평균값 계산

            # scatter plot으로 그래프 그리기 (각 search_method 별로 다른 marker 및 색상 설정)
            line, = ax.plot(avg_data.index, avg_data, label=search_method, alpha=0.7, 
                            marker=marker_dict.get(search_method, 'o'),  # 기본값을 'o'로 설정
                            color=color_dict.get(search_method, 'black'))  # 기본값을 'black'으로 설정
            
            # Add handles for the global legend
            if i == 0:  # Only collect legend handles from the first subplot
                handles.append(line)

    # 그래프 제목 및 축 레이블 설정
    ax.set_title(f'{title_prefix[i] + dataset.split("_")[0]}', {'fontsize':fffsize, 'verticalalignment':'bottom'})
    ax.set_xlabel('index density', fontsize=fffsize, labelpad=0)
    ax.set_ylabel('lookup latency(s)', fontsize=fffsize, labelpad=0)

    # Set custom x-axis tick labels
    ax.set_xticks([0.2, 0.3, 0.4, 0.5, 0.6, 0.7])  # Set the positions for the ticks
    ax.set_xticklabels([0.2, 0.3, 0.4, 0.5, 0.6, 0.7], fontsize=fffsize)  # Set custom labels with fontsize

    # Set y-axis limit
    ax.set_ylim(0, 100)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

# 빈 서브플롯 제거
for i in range(len(datasets), num_cols * num_rows):
    row = i // num_cols
    col = i % num_cols
    ax = axes[row, col] if num_rows > 1 else axes[col]
    fig.delaxes(ax)

custom_labels = {
    'exponential': 'exponential',
    'mb_bbin': 'mb_bbin',
    'ex_mb_bbin': 'ex_bbin',  # Custom name
    'mb_slin': 'mb_slin',
    'ex_mb_slin': 'ex_slin'   # Custom name
}
legend_labels = [custom_labels[method] for method in search_methods]
# Create a global legend at the top with smaller font size
fig.legend(handles=handles, labels=search_methods, loc='upper center', ncol=3, fontsize=10)

# 전체 그림의 크기 조정
fig.set_size_inches(7, 5)  # Adjusted for 2x2 grid
plt.subplots_adjust(top=0.85, wspace=0.3, hspace=0.5)  # Adjusted top to make space for the legend

# PDF 파일로 저장
plt.savefig(output_dir + 'alex_lookup_latency.png', bbox_inches='tight')

