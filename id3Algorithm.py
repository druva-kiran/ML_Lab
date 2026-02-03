import math
import pandas as pd

def load_data(train_file, test_file):
    train_df = pd.read_csv(train_file)
    test_df = pd.read_csv(test_file)
    

    train_df = train_df.apply(lambda x: x.astype(str).str.strip().str.capitalize())
    test_df = test_df.apply(lambda x: x.astype(str).str.strip().str.capitalize())
    
    return train_df, test_df

class Node:
    def __init__(self, attribute):
        self.attribute = attribute
        self.children = []
        self.answer = ""

def entropy(target_col):
    values = target_col.value_counts(normalize=True)
    return -sum(values * values.apply(math.log2))

def info_gain(data, split_attribute, target_attribute):
    total_entropy = entropy(data[target_attribute])
    weighted_entropy = 0
    for val, subset in data.groupby(split_attribute):
        weighted_entropy += (len(subset) / len(data)) * entropy(subset[target_attribute])
    return total_entropy - weighted_entropy

def build_tree(data, attributes, target):

    if len(data[target].unique()) == 1:
        node = Node("")
        node.answer = data[target].iloc[0]
        return node
    

    if not attributes:
        node = Node("")
        node.answer = data[target].mode()[0]
        return node
    

    gains = {attr: info_gain(data, attr, target) for attr in attributes}
    best_attr = max(gains, key=gains.get)
    
    root = Node(best_attr)
    remaining_attrs = [a for a in attributes if a != best_attr]
    
    for val, subset in data.groupby(best_attr):
        child = build_tree(subset, remaining_attrs, target)
        root.children.append((val, child))
        
    return root

def print_tree(node, level=0):
    if node.answer != "":
        print("  " * level + node.answer)
        return
    print("  " * level + str(node.attribute))
    for value, child in node.children:
        print("  " * (level + 1) + str(value))
        print_tree(child, level + 2)

def classify(node, instance):
    if node.answer != "":
        return node.answer
    
    val = instance[node.attribute]
    for child_val, child_node in node.children:
        if val == child_val:
            return classify(child_node, instance)
    return "Unknown"

# --- Main Program ---
train_df, test_df = load_data('id3.csv', 'id3_test_1.csv')
features = list(train_df.columns[:-1])
target = train_df.columns[-1]

model_tree = build_tree(train_df, features, target)

print("The decision tree for the dataset using ID3 algorithm is")
print_tree(model_tree)

for _, row in test_df.iterrows():
    print(f"The test instance: {row.tolist()}")
    result = classify(model_tree, row)
    print(f"The label for test instance: {result}")