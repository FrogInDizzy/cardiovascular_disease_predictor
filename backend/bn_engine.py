import numpy as np
from collections import defaultdict

class Variable:
    def __init__(self, name, values):
        self.name = name
        self.values = values
        self.value_indices = {val: i for i, val in enumerate(values)}

class BayesianNetwork:
    def __init__(self):
        self.variables = {}
        self.var_names = []
        self.cpts = {}
        self.children = defaultdict(list)

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            lines = [line.split('#')[0].strip() for line in f if line.strip() and not line.strip().startswith('#')]
            num_vars = int(lines[0])
            line_idx = 1
            for _ in range(num_vars):
                parts = lines[line_idx].split()
                name, values = parts[0], parts[1:]
                self.variables[name] = Variable(name, values)
                self.var_names.append(name)
                line_idx += 1

            num_cpts = int(lines[line_idx])
            line_idx += 1
            for _ in range(num_cpts):
                parts = lines[line_idx].split()
                child, parents = parts[0], parts[1:]
                line_idx += 1
                for parent in parents:
                    self.children[parent].append(child)

                probs = []
                num_parent_configs = 1
                for parent in parents:
                    num_parent_configs *= len(self.variables[parent].values)
                    
                print(f"Reading CPT for {child}, expecting {num_parent_configs} lines starting at line {line_idx}")

                for _ in range(num_parent_configs):
                    probs.append([float(p) for p in lines[line_idx].split()])
                    line_idx += 1

                self.cpts[child] = (parents, probs)

    def exact_inference(self, query_var, evidence):
        hidden_vars = [var for var in self.var_names if var != query_var and var not in evidence]
        factors = []
        for var in self.var_names:
            parents, probs = self.cpts[var]
            factors.append(Factor(var, parents, probs, self))

        for factor in factors:
            factor.restrict(evidence)

        for hidden in hidden_vars:
            relevant = [f for f in factors if hidden in f.variables]
            if relevant:
                factors = [f for f in factors if hidden not in f.variables]
                product = relevant[0]
                for f in relevant[1:]:
                    product = product.multiply(f)
                summed = product.sum_out(hidden)
                factors.append(summed)

        result = factors[0]
        for f in factors[1:]:
            result = result.multiply(f)

        result.normalize()
        query_values = self.variables[query_var].values
        return [result.get_probability({query_var: val}) for val in query_values]

class Factor:
    def __init__(self, var=None, parents=None, probs=None, network=None):
        self.variables = [var] + parents if var else []
        self.network = network
        self.dimensions = [len(network.variables[v].values) for v in self.variables] if self.variables else []
        self.values = np.zeros(self.dimensions) if self.dimensions else np.array([1.0])

        if var:
            if not parents:
                for i, prob in enumerate(probs[0]):
                    self.values[i] = prob
            else:
                for idx, dist in enumerate(probs):
                    indices = self._flat_to_indices(idx, self.dimensions[1:])
                    for j, prob in enumerate(dist):
                        self.values[tuple([j] + indices)] = prob

    def _flat_to_indices(self, flat_idx, dimensions):
        indices = []
        for dim in reversed(dimensions):
            indices.insert(0, flat_idx % dim)
            flat_idx //= dim
        return indices

    def restrict(self, evidence):
        for var, val in evidence.items():
            if var in self.variables:
                idx = self.variables.index(var)
                val_idx = self.network.variables[var].value_indices[val]
                slicer = [slice(None)] * len(self.variables)
                slicer[idx] = val_idx
                self.values = self.values[tuple(slicer)]
                self.variables.pop(idx)
                self.dimensions.pop(idx)
                if not self.variables:
                    self.values = np.array([self.values.item()])

    def multiply(self, other):
        result = Factor(network=self.network)
        all_vars = list(set(self.variables + other.variables))
        result.variables = all_vars
        result.dimensions = [len(self.network.variables[v].values) for v in all_vars]
        result.values = np.ones(result.dimensions)
        idx_self = [all_vars.index(v) for v in self.variables]
        idx_other = [all_vars.index(v) for v in other.variables]
        for combo in np.ndindex(*result.dimensions):
            i1 = tuple(combo[i] for i in idx_self)
            i2 = tuple(combo[i] for i in idx_other)
            result.values[combo] = self.values[i1] * other.values[i2]
        return result

    def sum_out(self, var):
        if var not in self.variables:
            return self
        idx = self.variables.index(var)
        result = Factor(network=self.network)
        result.variables = self.variables[:idx] + self.variables[idx+1:]
        result.dimensions = self.dimensions[:idx] + self.dimensions[idx+1:]
        result.values = np.sum(self.values, axis=idx)
        return result

    def normalize(self):
        total = np.sum(self.values)
        if total > 0:
            self.values /= total

    def get_probability(self, evidence):
        indices = []
        for var in self.variables:
            val = evidence.get(var, self.network.variables[var].values[0])
            idx = self.network.variables[var].value_indices[val]
            indices.append(idx)
        return self.values[tuple(indices)]
