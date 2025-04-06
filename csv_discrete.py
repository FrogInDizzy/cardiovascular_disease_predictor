import pandas as pd
import numpy as np
from collections import defaultdict
import itertools

# 读取CSV文件
df = pd.read_csv("/mnt/data/cardio_train.csv", sep=';')

# 选取变量并进行离散化
def categorize_age(age):
    years = age // 365
    if years < 40:
        return 'young'
    elif years < 60:
        return 'middle'
    else:
        return 'old'

def categorize_bmi(height, weight):
    bmi = weight / ((height / 100) ** 2)
    if bmi < 18.5:
        return 'underweight'
    elif bmi < 25:
        return 'normal'
    elif bmi < 30:
        return 'overweight'
    else:
        return 'obese'

def categorize_ap_hi(ap_hi):
    if ap_hi < 120:
        return 'normal'
    elif ap_hi < 140:
        return 'high'
    else:
        return 'very_high'

df['age_group'] = df['age'].apply(categorize_age)
df['bmi_group'] = df.apply(lambda row: categorize_bmi(row['height'], row['weight']), axis=1)
df['ap_hi_group'] = df['ap_hi'].apply(categorize_ap_hi)
df['cholesterol'] = df['cholesterol'].astype(str)
df['gluc'] = df['gluc'].astype(str)
df['smoke'] = df['smoke'].astype(str)
df['cardio'] = df['cardio'].astype(str)

# 保留有用的字段
fields = ['age_group', 'bmi_group', 'ap_hi_group', 'cholesterol', 'gluc', 'smoke', 'cardio']
df = df[fields]

# 构建CPT
def compute_cpt(df, target, parents):
    group = df.groupby(parents + [target]).size().unstack(fill_value=0)
    group = group.div(group.sum(axis=1), axis=0).fillna(0)
    return group

# 写入.bn文件格式
bn_lines = []
variables = {
    'age_group': ['young', 'middle', 'old'],
    'bmi_group': ['underweight', 'normal', 'overweight', 'obese'],
    'ap_hi_group': ['normal', 'high', 'very_high'],
    'cholesterol': ['1', '2', '3'],
    'gluc': ['1', '2', '3'],
    'smoke': ['0', '1'],
    'cardio': ['0', '1']
}

# 变量数和定义
bn_lines.append(str(len(variables)))
for var, vals in variables.items():
    bn_lines.append(f"{var} {' '.join(vals)}")

# CPTs
bn_lines.append(str(len(variables)))
for var in variables:
    parents = [p for p in variables if p != var]
    bn_lines.append(f"{var} {' '.join(parents)}")
    cpt = compute_cpt(df, var, parents)

    # 补全所有组合（确保生成的CPT是完整的）
    all_parent_vals = [variables[p] for p in parents]
    for combo in itertools.product(*all_parent_vals):
        row = cpt.loc[combo] if combo in cpt.index else [1/len(variables[var])] * len(variables[var])
        bn_lines.append(' '.join(f"{p:.4f}" for p in row))

# 保存为.bn文件
with open("/mnt/data/heart_disease.bn", "w") as f:
    f.write("\n".join(bn_lines))

"/mnt/data/heart_disease.bn 已生成 ✅"
