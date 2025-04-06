import re

def parse_bn_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # 变量块
    variable_blocks = re.findall(r'VARIABLE\s+(\w+)\s*{[^}]*?{([^}]*)}', content)
    variables = []
    states = []
    for var, vals in variable_blocks:
        val_list = vals.strip().replace(',', '').split()
        variables.append(var)
        states.append(val_list)

    # CPT 块（仅支持 1 个目标变量）
    match = re.search(r'PROBABILITY\s+\((\w+)\s*\|\s*([^)]+)\)\s*{(.*?)}', content, re.DOTALL)
    if not match:
        raise ValueError("无法找到 PROBABILITY 块")

    target = match[1]
    parents = match[2].split(',')
    parents = [p.strip() for p in parents]
    raw_cpt = match[3].strip()

    # 提取每一行的组合和概率
    entries = re.findall(r'\(([^)]+)\)\s*([0-9.,\s]+);', raw_cpt)
    cpt = []
    for combo_str, probs_str in entries:
        probs = list(map(float, probs_str.strip().split(',')))
        cpt.append(probs)

    return variables, states, target, parents, cpt

def write_table_cpt(output_path, variables, states, target, parents, cpt):
    with open(output_path, 'w') as f:
        f.write(f"{len(variables)}\n")
        for var, vals in zip(variables, states):
            f.write(f"{var} {' '.join(vals)}\n")
        f.write("1\n")
        f.write(f"{target} {' '.join(parents)}\n")
        for row in cpt:
            f.write(f"{row[0]:.5f} {row[1]:.5f}\n")
# 使用示例
bn_path = '/Users/edwingao/Desktop/Project/codepath/cardiovascular_disease_predictor/cardio_model.bn'  # 你提供的 CPT 表格文件路径
output_txt = '/Users/edwingao/Desktop/Project/codepath/cardiovascular_disease_predictor/cardio_model_new.bn'

variables, states, target, parents, cpt = parse_bn_file(bn_path)
write_table_cpt(output_txt, variables, states, target, parents, cpt)
