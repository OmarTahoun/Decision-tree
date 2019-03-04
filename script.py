from __future__ import print_function

data = [
    ['Green', 3, 'Apple'],
    ['Yellow', 3, 'Apple'],
    ['Red', 1, 'Grape'],
    ['Red', 1, 'Grape'],
    ['Yellow', 3, 'Lemon'],
]

header = ["color", "diameter", "label"]


def unique_values(rows, col):
    return set([row[col] for row in rows])


def class_count(rows):
    counts = {}
    for row in rows:
        label = row[-1]
        if label not in counts:
            counts[label] = 0
        counts[label] += 1
    return counts


def is_numeric(value):
    return isinstance(value, int) or isinstance(value, float)


class Question(object):
    """docstring for Question"""

    def __init__(self, column, value):
        self.column = column
        self.value = value

    def match(self, example):
        val = example[self.column]
        if is_numeric(val):
            return val >= self.value
        else:
            return val == self.value

    def __repr__(self):
        condition = "=="
        if is_numeric(self.value):
            condition = ">="
        return "Is %s %s %s ?" % (header[self.column], condition, str(self.value))


def part(rows, question):
    true_rows, false_rows = [], []

    for row in rows:
        if question.match(row):
            true_rows.append(row)
        else:
            false_rows.append(row)

    return true_rows, false_rows


def gini(rows):
    counts = class_count(rows)
    impurity = 1
    for label in counts:
        prob_of_label = counts[label] / float(len(rows))
        impurity -= prob_of_label**2
    return impurity


def info_gain(left, right, current_uncertainty):
    p = float(len(left)) / (len(left) + len(right))
    return current_uncertainty - p * gini(left) - (1 - p) * gini(right)


def best_split(rows):
    best_gain = 0
    best_question = None
    current_uncertainty = gini(rows)
    num_features = len(rows[0]) - 1

    for col in range(num_features):

        values = set([row[col] for row in rows])

        for value in values:
            question = Question(col, value)
            true, false = part(rows, question)

            if len(true) == 0 or len(false) == 0:
                continue
            gain = info_gain(true, false, current_uncertainty)
            if gain >= best_gain:
                best_gain, best_question = gain, question

    return best_gain, best_question


class Leaf:

    def __init__(self, rows):
        self.predictions = class_count(rows)


class Decision_node:

    def __init__(self, question, true_branch, false_branch):
        self.question = question
        self.true_branch = true_branch
        self.false_branch = false_branch


def build_tree(rows):

    gain, question = best_split(rows)

    if gain == 0:
        return Leaf(rows)

    true, false = part(rows, question)

    true = build_tree(true)
    false = build_tree(false)

    return Decision_node(question, true, false)


def print_tree(node, spacing=""):
    if isinstance(node, Leaf):
        print(spacing + "Predict", node.predictions)
        return
    print(spacing + str(node.question))

    print(spacing + '=======> True: ')
    print_tree(node.true_branch, spacing + " ")

    print(spacing + '=======> False: ')
    print_tree(node.false_branch, spacing + " ")


def classify(row, node):
    if isinstance(node, Leaf):
        return node.predictions
    if node.question.match(row):
        return classify(row, node.true_branch)
    else:
        return classify(row, node.false_branch)


def print_leaf(counts):
    total = sum(counts.values()) * 1.0
    probs = {}

    for label in counts.keys():
        probs[label] = str(int(counts[label] / total * 100)) + "%"
    return probs

my_tree = build_tree(data)
print_tree(my_tree)

test = [
    ['Green', 3, 'Apple'],
    ['Yellow', 4, 'Apple'],
    ['Red', 2, 'Grape'],
    ['Red', 1, 'Grape'],
    ['Yellow', 3, 'Lemon'],
]
for row in test:
    print("Actual: %s. Predicted: %s" %
          (row[-1], print_leaf(classify(row, my_tree))))


# print(best_split(data))
