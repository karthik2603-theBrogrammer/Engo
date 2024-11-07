#!/usr/bin/env python3

import time
import json
import io
import sys

from engine_utils import (
    create_rule,
    evaluate_rule,
    combine_rules,
    get_json_from_ast,
    get_ast_from_json,
)
from Node import Node
from constants import FUNCTIONS, ATTRIBUTE_CATALOG
from RichFont import console

# Add necessary functions to FUNCTIONS if not already present
FUNCTIONS['get_minimum_age'] = lambda: 18
FUNCTIONS['calculate_bonus'] = lambda experience: experience * 1000

# Helper function to remove 'id' fields from AST JSON for comparison
total_test_cases = 12
passing_test_cases = 0
start_time = None
end_time = None

def remove_ids(ast_json):
    if isinstance(ast_json, dict):
        ast_json.pop('id', None)
        for key, value in ast_json.items():
            remove_ids(value)
    elif isinstance(ast_json, list):
        for item in ast_json:
            remove_ids(item)

# Test runner function
def test_case(case_number, description, test_function, expected_output):
    global passing_test_cases
    console.print(f"[italic cyan]Running Test Case {case_number}: {description}")
    # Capture the output
    captured_output = io.StringIO()
    sys.stdout = captured_output
    try:
        test_function()
        sys.stdout = sys.__stdout__
        actual_output = captured_output.getvalue().strip()
        expected_output_str = expected_output.strip()
        # Compare actual output to expected output
        if actual_output == expected_output_str:
            console.print(f"Success ✅: {description}")
            passing_test_cases += 1
        else:
            print(f"Error ❌: {description}")
            print("Expected Output:")
            print(expected_output_str)
            print("Actual Output:")
            print(actual_output)
    except Exception as e:
        sys.stdout = sys.__stdout__
        print(f"Error ❌: {description}")
        print(f"Exception occurred: {e}")
    time.sleep(1)  # 1-second gap between test cases

# Feature 1: Parsing Individual Rules and Verifying ASTs

def test_simple_condition():
    rule = "age > 18"
    ast = create_rule(rule)
    ast_json = get_json_from_ast(ast)
    remove_ids(ast_json)
    print(json.dumps(ast_json, indent=2))

def test_condition_with_function():
    rule = "salary > calculate_bonus(experience)"
    ast = create_rule(rule)
    ast_json = get_json_from_ast(ast)
    remove_ids(ast_json)
    print(json.dumps(ast_json, indent=2))

expected_output_1 = '''{
  "node_type": "condition",
  "operator": ">",
  "left": {
    "node_type": "variable",
    "value": "age"
  },
  "right": {
    "node_type": "constant",
    "value": 18
  }
}'''

expected_output_2 = '''{
  "node_type": "condition",
  "operator": ">",
  "left": {
    "node_type": "variable",
    "value": "salary"
  },
  "right": {
    "node_type": "function",
    "value": "calculate_bonus",
    "args": [
      {
        "node_type": "variable",
        "value": "experience"
      }
    ]
  }
}'''

# Feature 2: Combining Rules and Verifying Combined ASTs

def test_combining_rules_or():
    rules = ["age > 18", "salary > 50000"]
    combined_ast = combine_rules(rules)
    ast_json = get_json_from_ast(combined_ast)
    remove_ids(ast_json)
    print(json.dumps(ast_json, indent=2))

def test_combining_rules_and():
    rules = ["age > 18", "salary > 50000"]
    combined_ast = combine_rules(rules, custom_operator='AND')
    ast_json = get_json_from_ast(combined_ast)
    remove_ids(ast_json)
    print(json.dumps(ast_json, indent=2))

expected_output_3 = '''{
  "node_type": "operator",
  "value": "OR",
  "left": {
    "node_type": "condition",
    "operator": ">",
    "left": {
      "node_type": "variable",
      "value": "age"
    },
    "right": {
      "node_type": "constant",
      "value": 18
    }
  },
  "right": {
    "node_type": "condition",
    "operator": ">",
    "left": {
      "node_type": "variable",
      "value": "salary"
    },
    "right": {
      "node_type": "constant",
      "value": 50000
    }
  }
}'''

expected_output_4 = '''{
  "node_type": "operator",
  "value": "AND",
  "left": {
    "node_type": "condition",
    "operator": ">",
    "left": {
      "node_type": "variable",
      "value": "age"
    },
    "right": {
      "node_type": "constant",
      "value": 18
    }
  },
  "right": {
    "node_type": "condition",
    "operator": ">",
    "left": {
      "node_type": "variable",
      "value": "salary"
    },
    "right": {
      "node_type": "constant",
      "value": 50000
    }
  }
}'''

# Feature 3: Evaluating Rules Against Sample Data

def test_evaluate_simple_condition():
    rule = "age > 18"
    data = {'age': 20}
    ast = create_rule(rule)
    result = evaluate_rule(ast, data)
    print(result)

def test_evaluate_combined_rules():
    rules = ["age > 18", "salary > 50000"]
    data = {'age': 25, 'salary': 60000}
    combined_ast = combine_rules(rules)
    result = evaluate_rule(combined_ast, data)
    print(result)

expected_output_5 = 'True'
expected_output_6 = 'True'

# Feature 4: Testing User-Defined Functions

def test_function_no_args():
    rule = "age > get_minimum_age()"
    data = {'age': 20}
    ast = create_rule(rule)
    result = evaluate_rule(ast, data)
    print(result)

def test_function_with_args():
    rule = "salary > calculate_bonus(experience)"
    data = {'salary': 6000, 'experience': 5}
    ast = create_rule(rule)
    result = evaluate_rule(ast, data)
    print(result)

expected_output_7 = 'True'
expected_output_8 = 'True'

# Feature 5: Handling Negative Numbers

def test_negative_number_less_than():
    ATTRIBUTE_CATALOG.add('temperature')
    rule = "temperature < -5"
    data = {'temperature': -10}
    ast = create_rule(rule)
    result = evaluate_rule(ast, data)
    print(result)

def test_negative_number_greater_than():
    ATTRIBUTE_CATALOG.add('balance')
    rule = "balance > -1000"
    data = {'balance': -500}
    ast = create_rule(rule)
    result = evaluate_rule(ast, data)
    print(result)

expected_output_9 = 'True'
expected_output_10 = 'True'

# Feature 6: Testing JSON Serialization and Deserialization of ASTs

def test_ast_serialization_deserialization():
    rule = "age > 18 AND department = 'Sales'"
    ATTRIBUTE_CATALOG.add('department')
    ast = create_rule(rule)
    ast_json = get_json_from_ast(ast)
    remove_ids(ast_json)
    json_str = json.dumps(ast_json, indent=2)
    # Deserialize from JSON
    ast_reconstructed = get_ast_from_json(ast_json)
    # Evaluate with sample data
    data = {'age': 20, 'department': 'Sales'}
    result_original = evaluate_rule(ast, data)
    result_reconstructed = evaluate_rule(ast_reconstructed, data)
    print(f"Original: {result_original}, Reconstructed: {result_reconstructed}")

def test_ast_serialization_deserialization_complex():
    rule = "(age >= get_minimum_age()) AND (salary < 5000 OR department = 'HR')"
    ATTRIBUTE_CATALOG.update(['age', 'salary', 'department'])
    ast = create_rule(rule)
    ast_json = get_json_from_ast(ast)
    remove_ids(ast_json)
    json_str = json.dumps(ast_json, indent=2)
    ast_reconstructed = get_ast_from_json(ast_json)

    data = {'age': 18, 'salary': 6000, 'department': 'HR'}
    result_original = evaluate_rule(ast, data)
    result_reconstructed = evaluate_rule(ast_reconstructed, data)
    print(f"Original: {result_original}, Reconstructed: {result_reconstructed}")

expected_output_11 = 'Original: True, Reconstructed: True'
expected_output_12 = 'Original: True, Reconstructed: True'

def run_tests():
    global start_time, end_time
    start_time = time.time()
    # Feature 1 Tests
    test_case(1, "Parsing a rule with simple condition. [create_rule(rule:string)]", test_simple_condition, expected_output_1)
    test_case(2, "Parsing a rule with condition and function. [create_rule(rule:string)]", test_condition_with_function, expected_output_2)
    # Feature 2 Tests
    test_case(3, "Combining Rules with OR. [combine_rules([rules]:list<string>)]", test_combining_rules_or, expected_output_3)
    test_case(4, "Combining Rules with AND. [combine_rules([rules]:list<string>)]", test_combining_rules_and, expected_output_4)
    # Feature 3 Tests
    test_case(5, "Evaluating Simple Condition. [evaluate_rule(ast:Node, data:JSON)]", test_evaluate_simple_condition, expected_output_5)
    test_case(6, "Evaluating Combined Rules. [evaluate_rule(ast:Node, data:JSON)]", test_evaluate_combined_rules, expected_output_6)
    # Feature 4 Tests
    test_case(7, "Function Without Arguments", test_function_no_args, expected_output_7)
    test_case(8, "Function With Arguments", test_function_with_args, expected_output_8)
    # Feature 5 Tests
    test_case(9, "Negative Number Less Than", test_negative_number_less_than, expected_output_9)
    test_case(10, "Negative Number Greater Than", test_negative_number_greater_than, expected_output_10)
    # Feature 6 Tests
    test_case(11, "AST Serialization and Deserialization", test_ast_serialization_deserialization, expected_output_11)
    test_case(12, "AST Serialization and Deserialization Complex", test_ast_serialization_deserialization_complex, expected_output_12)
    # Continue with additional tests for other features...

    end_time = time.time()
if __name__ == "__main__":
    run_tests()
    console.print(f"[red]{total_test_cases - passing_test_cases}/ {total_test_cases} test cases have failed. ❌")
    console.print(f"[green]{passing_test_cases}/ {total_test_cases} test cases have passed. ✅ ")
    # console.print(f"[cyan]Completed all test cases in {round((end_time - start_time), 4)} seconds")