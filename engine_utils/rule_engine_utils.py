import re
import json

from Node import Node
from Parser import ParseError, Parser
from constants import VALID_OPERATORS, ATTRIBUTE_CATALOG, FUNCTIONS, VALID_LOGICAL_OPERATORS

def convert_double_to_single_quotes(rule_text):
    converted_text = re.sub(r'"([^"]*)"', r"'\1'", rule_text)
    return converted_text


def tokenize(rule_string):
    token_specification = [
        ('NUMBER', r'-?\d+(\.\d+)?'),   # Integer or decimal number, including negatives
        ('STRING',   r"'[^']*'"),             # String enclosed in single quotes
        ('AND',      r'\bAND\b'),             # Logical AND
        ('OR',       r'\bOR\b'),              # Logical OR
        ('NOT',      r'\bNOT\b'),             # Logical NOT
        ('FUNCTION', r'\b\w+\s*\('),          # Function names followed by '('
        ('COMMA',    r','),                   # Comma
        ('OP',       r'(<=|>=|<>|!=|=|<|>)'), # Comparison operators
        ('LPAREN',   r'\('),                  # Left parenthesis
        ('RPAREN',   r'\)'),                  # Right parenthesis
        ('IDENT',    r'\b\w+\b'),             # Identifiers
        ('SKIP',     r'[ \t]+'),              # Skip spaces and tabs
        ('MISMATCH', r'.'),                   # Any other character
    ]

    # Compile the regular expression with the IGNORECASE flag
    token_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    # print(token_regex)
    token_re = re.compile(token_regex, re.IGNORECASE)

    tokens = []
    pos = 0
    while pos < len(rule_string):
        mo = token_re.match(rule_string, pos)
        # print(mo)
        if not mo:
            raise ParseError(f"Unexpected character: '{rule_string[pos]}' at position {pos}", position=pos)
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == 'SKIP':
            pass
        elif kind == 'MISMATCH':
            raise ParseError(f"Unexpected token: '{value}' at position {pos}", position=pos, token=value)
        else:
            if kind in ('AND', 'OR', 'NOT'):
                value = value.upper()
            if kind == 'FUNCTION':
                value = value.strip().rstrip('(')
                tokens.append(('FUNCTION', value))
                tokens.append(('LPAREN', '('))
            else:
                tokens.append((kind, value))
        pos = mo.end()
    # print(tokens)
    return tokens

def is_blank(s):
    return s.strip() == ''

def create_rule(rule_string):
    """
    Parses a rule string and returns the root Node of the AST.
    """
    tokens = tokenize(rule_string)
    parser = Parser(tokens)
    ast = parser.parse()
    return ast

def print_ast(node, indent=0):
    """
    Utility function to print the AST for debugging.
    """
    prefix = ' ' * indent
    if node.node_type == 'operator':
        print(f"{prefix}{node.node_type}: {node.value}")
        if node.left:
            print_ast(node.left, indent + 2)
        if node.right:
            print_ast(node.right, indent + 2)
    elif node.node_type == 'condition':
        print(f"{prefix}{node.node_type}: {node.value}")
    else:
        print(f"{prefix}Unknown node type: {node.node_type}")


def evaluate_rule(ast, data):
    """
    Evaluates the AST against the provided data.
    """
    if ast.node_type == 'operator':
        if ast.value == 'AND':
            return evaluate_rule(ast.left, data) and evaluate_rule(ast.right, data)
        elif ast.value == 'OR':
            return evaluate_rule(ast.left, data) or evaluate_rule(ast.right, data)
        elif ast.value == 'NOT':
            return not evaluate_rule(ast.left, data)
        else:
            raise ValueError(f"Unknown operator: {ast.value}")
    elif ast.node_type == 'condition':
        attr, op, val = ast.value
        if isinstance(attr, Node):
            left_val = evaluate_node(attr, data)
        else:
            left_val = data.get(attr)
            if left_val is None:
                raise ValueError(f"Attribute '{attr}' not found in data")
        if isinstance(val, Node):
            right_val = evaluate_node(val, data)
        else:
            right_val = val
        return compare(left_val, op, right_val)
    elif ast.node_type == 'function':
        return evaluate_function(ast, data)
    elif ast.node_type == 'constant':
        return ast.value
    elif ast.node_type == 'variable':
        var_name = ast.value
        value = data.get(var_name)
        if value is None:
            raise ValueError(f"Variable '{var_name}' not found in data")
        return value
    else:
        raise ValueError(f"Unknown node type: {ast.node_type}")

def evaluate_node(node, data):
    if isinstance(node, Node):
        if node.node_type == 'constant':
            return node.value
        elif node.node_type == 'function':
            return evaluate_function(node, data)
        elif node.node_type == 'variable':
            var_name = node.value
            value = data.get(var_name)
            if value is None:
                raise ValueError(f"Variable '{var_name}' not found in data")
            return value
        elif node.node_type == 'operator':
            return evaluate_rule(node, data)
        else:
            raise ValueError(f"Unsupported node type in evaluation: {node.node_type}")
    else:
        raise ValueError(f"Expected a Node, but got {type(node)}")


def evaluate_function(func_node, data):
    func_name = func_node.value
    func = FUNCTIONS.get(func_name)
    if func is None:
        raise ValueError(f"Function '{func_name}' is not defined")
    args = [evaluate_node(arg, data) for arg in func_node.args]
    try:
        result = func(*args)
    except Exception as e:
        raise ValueError(f"Error evaluating function '{func_name}': {e}")
    return result

def compare(user_val, operator, val):
    if user_val is None:
        return False
    if operator == '>':
        return user_val > val
    elif operator == '<':
        return user_val < val
    elif operator == '>=':
        return user_val >= val
    elif operator == '<=':
        return user_val <= val
    elif operator in ('=', '=='):
        return user_val == val
    elif operator in ('!=', '<>'):
        return user_val != val
    else:
        raise ValueError(f"Unsupported operator: {operator}")

def ast_to_json(node):
    """
    Converts the AST Node into a JSON-serializable dictionary.
    """
    if node is None:
        return None

    node_dict = {
        'id': node.id,
        'node_type': node.node_type,
    }

    if node.node_type == 'operator':
        node_dict['value'] = node.value
        node_dict['left'] = ast_to_json(node.left)
        if node.value != 'NOT' and node.right is not None:
            node_dict['right'] = ast_to_json(node.right)
    elif node.node_type == 'condition':
        op = node.value[1]
        node_dict['operator'] = op

        attr = node.value[0]
        if isinstance(attr, Node):
            node_dict['left'] = ast_to_json(attr)
        else:
            node_dict['attribute'] = attr

        val = node.value[2]
        if isinstance(val, Node):
            node_dict['right'] = ast_to_json(val)
        else:
            node_dict['operand'] = val
    elif node.node_type == 'function':
        node_dict['value'] = node.value  # Function name
        node_dict['args'] = [ast_to_json(arg) for arg in node.args]
    elif node.node_type == 'variable':
        node_dict['value'] = node.value  # Variable name
    elif node.node_type == 'constant':
        node_dict['value'] = node.value  # Constant value
    else:
        raise ValueError(f"Unknown node type: {node.node_type}")

    return node_dict

def json_to_ast(node_dict):
    """
    Reconstructs the AST Node from a JSON dictionary.

    :param node_dict: The dictionary representing the AST.
    :return: The root Node of the AST.
    """
    if node_dict is None:
        return None

    node_type = node_dict.get('node_type')

    if node_type == 'operator':
        value = node_dict.get('value')
        left_node = json_to_ast(node_dict.get('left'))
        if value != 'NOT':
            right_node = json_to_ast(node_dict.get('right'))
        else:
            right_node = None
        return Node(node_type='operator', value=value, left=left_node, right=right_node)
    elif node_type == 'condition':
        op = node_dict.get('operator')

        if 'left' in node_dict:
            attr = json_to_ast(node_dict.get('left'))
        else:
            attr = node_dict.get('attribute')

        if 'right' in node_dict:
            val = json_to_ast(node_dict.get('right'))
        else:
            val = node_dict.get('operand')

        return Node(node_type='condition', value=(attr, op, val))
    elif node_type == 'function':
        func_name = node_dict.get('value')
        args = [json_to_ast(arg) for arg in node_dict.get('args', [])]
        return Node(node_type='function', value=func_name, args=args)
    elif node_type == 'variable':
        var_name = node_dict.get('value')
        return Node(node_type='variable', value=var_name)
    elif node_type == 'constant':
        const_value = node_dict.get('value')
        return Node(node_type='constant', value=const_value)
    else:
        raise ValueError(f"Unknown node type: {node_type}")

def print_ast_json(ast):
    ast_json = ast_to_json(ast)
    print(json.dumps(ast_json, indent=2))

def get_json_from_ast(ast):
    return ast_to_json(ast)

def get_ast_from_json(node_dict):
    return json_to_ast(node_dict)



def combine_rules(rules, use_most_freq_operator_heuristic=False, custom_operator=None):
    """
    Combines multiple rule strings into a single AST, minimizing redundant checks.

    :param rules: List of rule strings.
    :param use_most_freq_operator_heuristic: Boolean flag to use the heuristic (as mentioned in the instruction pdf givem).
    :param custom_operator: Operator to use for combining ('AND' or 'OR').
    :return: The root Node of the combined AST.

    preference given to 'use_most_freq_operator_heuristic' flag, if this is set, irrespective to 'custom_operator' 
    engine will make use of this.
    """
    if custom_operator not in VALID_LOGICAL_OPERATORS and custom_operator is not None:
        raise ValueError(f"Invalid custom_operator: {custom_operator}")
    asts = [create_rule(rule) for rule in rules]

    # Count operator frequencies across all ASTs
    operator_counts = {'AND': 0, 'OR': 0}

    def count_operators(node):
        if node.node_type == 'operator':
            operator_counts[node.value] += 1
            if node.left:
                count_operators(node.left)
            if node.right:
                count_operators(node.right)
        elif node.node_type == 'condition':
            pass

    for ast in asts:
        count_operators(ast)

    default_operator = "OR"
    operator = default_operator if custom_operator is None else custom_operator
    if use_most_freq_operator_heuristic:
        operator = max(operator_counts, key=operator_counts.get)

    node_cache = {}

    def deduplicate(node):
        """
        Recursively deduplicate nodes by merging identical subtrees.

        :param node: The current node to process.
        :return: The deduplicated node.
        """
        if node is None:
            return None

        node_id = node.id

        if node_id in node_cache:
            return node_cache[node_id]


        if node.node_type == 'operator':
            node.left = deduplicate(node.left)
            node.right = deduplicate(node.right)

        node_cache[node_id] = node
        return node


    dedup_asts = [deduplicate(ast) for ast in asts]

    if not dedup_asts:
        return None  

    from functools import reduce

    def combine_two_nodes(node1, node2):
        combined_node = Node(
            node_type='operator',
            value=operator,
            left=node1,
            right=node2
        )
        return deduplicate(combined_node)

    combined_ast = reduce(combine_two_nodes, dedup_asts)

    combined_ast = simplify_ast(combined_ast)

    return combined_ast


def simplify_ast(node):
    """
    Simplifies the AST by applying logical identities.

    :param node: The root node of the AST.
    :return: The simplified AST node.
    """
    if node is None:
        return None

    # Recursively simplify child nodes
    if node.node_type == 'operator':
        node.left = simplify_ast(node.left)
        node.right = simplify_ast(node.right) if node.value != 'NOT' else None

        # Apply simplification rules
        if node.value == 'AND':
            # Simplify: A AND A => A
            if node.left == node.right:
                return node.left
            # Simplify: A AND TRUE => A
            if is_true_node(node.left):
                return node.right
            if is_true_node(node.right):
                return node.left
            # Simplify: A AND FALSE => FALSE
            if is_false_node(node.left) or is_false_node(node.right):
                return false_node()
        elif node.value == 'OR':
            # Simplify: A OR A => A
            if node.left == node.right:
                return node.left
            # Simplify: A OR FALSE => A
            if is_false_node(node.left):
                return node.right
            if is_false_node(node.right):
                return node.left
            # Simplify: A OR TRUE => TRUE
            if is_true_node(node.left) or is_true_node(node.right):
                return true_node()
        elif node.value == 'NOT':
            # Simplify: NOT TRUE => FALSE
            if is_true_node(node.left):
                return false_node()
            # Simplify: NOT FALSE => TRUE
            if is_false_node(node.left):
                return true_node()
            # Simplify: NOT NOT A => A
            if node.left.node_type == 'operator' and node.left.value == 'NOT':
                return node.left.left

    return node

def is_true_node(node):
    # Define what constitutes a TRUE node
    return node.node_type == 'constant' and node.value == True

def is_false_node(node):
    # Define what constitutes a FALSE node
    return node.node_type == 'constant' and node.value == False

def true_node():
    return Node(node_type='constant', value=True)

def false_node():
    return Node(node_type='constant', value=False)
