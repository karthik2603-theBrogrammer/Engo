# Engo: A Custom Rule Engine.


<div align="center">
  <img src="https://github.com/user-attachments/assets/20927947-aefe-4ea7-9aa8-0f94bd40ac56" alt="Screenshot 2024-10-20 at 11 44 27 PM" width="900" height="370">
</div>





## What is Engo?

- Engo is a custom rule engine that parses rules defined in its specific language. It helps define rules and validate users against these rules. 
- Engo supports representations like `ASTs (Abstract Syntax Trees)` and `DAGs (Directed Acyclic Graphs)` to optimize rule processing.
- The UI, built using **React Flow**, allows interactive visualizations of these rule structures. 


<summary><h1>⚖️ AST vs DAG Comparison</h1></summary>

|  **AST (Abstract Syntax Tree)**         | **DAG (Directed Acyclic Graph)**       |
| ----------------------------------------- | ---------------------------------------- |
| <p align="center"><img width="468" alt="Screenshot 2024-10-21 at 12 34 57 AM" src="https://github.com/user-attachments/assets/3a4a4786-48a5-477a-85f8-82638ddb67ec"></p> | <p align="center"><img width="450" alt="Screenshot 2024-10-21 at 12 35 04 AM" src="https://github.com/user-attachments/assets/759bb37f-5bb6-4f99-8a3c-6e8066a8354c"></p> |
| Represents the syntax of a rule. It is commonly used in compilers for code analysis. Compiler first creates a parse tree (Concrete Syntax Tree) which is converted to an Syntax tree (Abstract Syntax). | Represents a compressed form of an AST. In large-scale applications with complex expressions, DAGs significantly reduce storage and eliminate redundant computations. |





<summary><h1>Engo's Tokenizer</h1></summary>

- A code-snippet from Engo's Tokenizer. Can parse numbers, attributes, functions (custom user-defined), left and right parantheses, comma andlogical operator in order of precedence (AND, OR, NOT).

```python
token_specification = [
    ('NUMBER', r'-?\d+(\.\d+)?'),   # Integer or decimal number, including negatives
    ('STRING',   r"'[^']*'"),       # String enclosed in single quotes
    ('AND',      r'\bAND\b'),       # Logical AND
    ('OR',       r'\bOR\b'),        # Logical OR
    ('NOT',      r'\bNOT\b'),       # Logical NOT
    ('FUNCTION', r'\b\w+\s*\('),    # Function names followed by '('
    ('COMMA',    r','),             # Comma
    ('OP',       r'(<=|>=|<>|!=|=|<|>)'), # Comparison operators
    ('LPAREN',   r'\('),            # Left parenthesis
    ('RPAREN',   r'\)'),            # Right parenthesis
    ('IDENT',    r'\b\w+\b'),       # Identifiers
    ('SKIP',     r'[ \t]+'),        # Skip spaces and tabs
    ('MISMATCH', r'.'),             # Any other character
]
```




<summary><h1>Engo's Structure</h1></summary>

Engo supports the following types of nodes:

1. **Operator Node**
   - Represents logical operators like `AND`, `OR`, and `NOT`.
   - **Example**:
     ```python
     Node(node_type='operator', value='AND', left=Node(...), right=Node(...))
     ```
     This represents an operator node that combines two sub-expressions using the `AND` operator.

2. **Condition Node**
   - Represents a condition to be evaluated. It contains an attribute, an operator, and an operand.
   - **Example**:
     ```python
     Node(node_type='condition', value=('age', '>', 30))
     ```
     This represents a condition node that checks if the attribute `age` is greater than `30`.

3. **Function Node**
   - Represents a function call with arguments. The function can be one of the custom functions defined in Engo.
   - **Example**:
     ```python
     Node(node_type='function', value='calculate_bonus', args=[Node(node_type='variable', value='experience')])
     ```
     This represents a function node for the `calculate_bonus` function, which takes `experience` as an argument.

4. **Constant Node**
   - Represents a constant value, either numeric or Boolean.
   - **Example**:
     ```python
     Node(node_type='constant', value=42)
     ```
     This represents a constant node with the value `42`.

5. **Variable Node**
   - Represents a variable that can be referenced within a condition or function.
   - **Example**:
     ```python
     Node(node_type='variable', value='salary')
     ```
     This represents a variable node with the value `salary`.





<summary><h1>🔗 Features of Engo</h1></summary>

| Feature | Function | Description |
| ------- | -------- | ----------- |
| **Rule Creation** | `create_rule(rule_string:string)` | Parses a rule string into an AST representation. |
| **Combining Rules** | `combine_rules(rules list, use_most_freq_operator_heuristic:bool, custom_operator:str)` | Combines multiple rules into a single AST. |
| **Rule Evaluation** | `evaluate_rule(ast:Node, data:JSON)` | Evaluates an AST against user-provided data to determine if the rule holds true. |
| **Add Sub-expression** | `add_sub_expression(parent_id:str, sub_expr_ast Node, position:string)` | Adds a sub-expression to an operator node. |
| **Remove Sub-expression** | `remove_sub_expression(target_id:string)` | Removes a sub-expression. **Note**: Does not work for the root node. |
| **Change Operator** | `change_operator(target_id:str, new_operator:str)` | Changes the operator of an operator or condition node. |
| **Change Operand** | `change_operand(target_id:str, new_left_operand:Node, new_right_operand:Node)` | Modifies the left or right operand of a condition node. |


<summary><h1>Custom Functions Supported</h1></summary>
  
| Function | Description |
| -------- | ----------- |
| **get_minimum_age()** | Returns `18` . |
| **calculate_bonus(experience)** | Returns `experience * 1000` . |
| **average_salary()** | Returns `40000`. |
| **salary_for_age_experience(age, experience)** | Calculates salary using age and experience with the formula salary = `(age * experience * 1000) + 1000` . |
| **max(x, y)** | Returns the maximum value between `x` and `y`. |
| **min(x, y)** | Returns the minimum value between `x` and `y`. |
| **abs(x)** | Returns the absolute value of `x`. |


<summary><h1>How to setup Engo</h1></summary>


### Manual Setup
1. **Clone the repository** and install necessary tools (`Node.js`, `npm`, `Python`, `Flask`, `Docker` etc.).
2. **Run the following commands in `/client`**:
 ```sh
 npm i && npm run dev
```
3. In the root directory, install dependencies and run the main file:
```sh
pip install -r requirements.txt
python main.py
```
4. Start the PostgreSQL database using Docker:
```sh
docker-compose -f docker-compose.yaml up
```

- To view the Postgres shell and execute commands, run the following command:
```sh
docker exec -it postgres_db psql -U postgres -d postgres
```


### 🐳 Docker Setup (supports both linux/amd64 and linux/arm64)
1. Clone the repository.
2. Run the command
```sh
docker-compose -f docker-compose-prod.yaml up
```
- And thats it! 🎉


<summary><h1>📝 How to run and use Engo ?</h1></summary>
  
### 1. Python Shell

- Example 1:
  
```python
>>> from engine_utils import *
>>> rule = "salary > salary_for_age_exp(age, experience)"
>>> ast = create_rule(rule)
>>> ast.get_text()
'(salary > salary_for_age_exp(age, experience))'

>>> evaluate_rule(ast, {"salary": 90000, "age": 21, "experience": 0})
True

>>> evaluate_rule(ast, {"salary": 90000, "age": 21, "experience": 5})
False
```

- Example 2:
  
```python
>>> from engine_utils import *
>>> rule = "age > 21 or experience > 4"
>>> ast = create_rule(rule)
>>> ast.get_text()
'((age > 21) OR (experience > 4))'
>>> ast
Node(node_type=operator, value=OR)

>>> print_ast_json(ast)
{
  "id": "COND_VAR_age_>_CONST_21-OR-COND_VAR_experience_>_CONST_4",
  "node_type": "operator",
  "value": "OR",
  "left": {
    "id": "COND_VAR_age_>_CONST_21",
    "node_type": "condition",
    "operator": ">",
    "left": {
      "id": "VAR_age",
      "node_type": "variable",
      "value": "age"
    },
    "right": {
      "id": "CONST_21",
      "node_type": "constant",
      "value": 21
    }
  },
  "right": {
    "id": "COND_VAR_experience_>_CONST_4",
    "node_type": "condition",
    "operator": ">",
    "left": {
      "id": "VAR_experience",
      "node_type": "variable",
      "value": "experience"
    },
    "right": {
      "id": "CONST_4",
      "node_type": "constant",
      "value": 4
    }
  }
}
```


## 🌐 HTTP API Using React and Flask
- After running the application, open the react application (Port 5173 for local and Port 3000 in case you are using docker) and perform any desired functions.


| 📝 API Action                     | 📍 Endpoint                   | 📄 Description                                               | 🔑 Parameters                                                                                          |
|-------------------------------|-------------------------------|--------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|
| **CREATE RULE**               | `/rule` (POST)                | Create a rule from a string and return its ID.               | - `rule_text` (string, required): The rule to be created in Engolang.                                  |
| **RETRIEVE RULE**             | `/rule/<rule_id>` (GET)       | Retrieve a rule by ID.                                       | - `rule_id` (integer, path): The unique identifier of the rule to retrieve.                            |
| **COMBINE RULES**             | `/rules/combine` (POST)       | Combine multiple rules into one and return its AST.          | - `rule_ids` (list of integers, required): IDs of rules to combine. <br> - `use_most_freq_operator_heuristic` (integer, optional): Set to `1` to use heuristic. <br> - `custom_operator` (string, optional): Operator (`AND` or `OR`). <br> - `store_combined_rule` (boolean, optional): Store the combined rule. |
| **EVALUATE RULE**             | `/rule/evaluate` (POST)       | Evaluate a rule given user data and return the result.       | - `rule_id` (integer, required): ID of the rule to evaluate. <br> - `data_for_evaluation` (object, required): Data to evaluate the rule against. |
| **EVALUATE COMBINED RULES**   | `/evaluate-combined-rules` (POST) | Evaluate combined rules and return the result.             | - `rule_ids` (list of integers, required): IDs of rules to combine and evaluate. <br> - `data_for_evaluation` (object, required): Data to evaluate against. <br> - `use_most_freq_operator_heuristic` (integer, optional): Set to `1` to use heuristic. <br> - `custom_operator` (string, optional): Operator (`AND` or `OR`). <br> - `store_combined_rule` (boolean, optional): Store the combined rule. |
| **DELETE RULE**               | `/rule/<rule_id>` (DELETE)    | Delete a rule by ID.                                         | - `rule_id` (integer, path): The unique identifier of the rule to delete.                              |
| **RETRIEVE ALL RULES**        | `/all-rules` (GET)            | Retrieve all rules in the system.                            | None                                                                                                   |

<summary><h1>✨ Snapshots of the UI</h1></summary>
<table>
  <tr>
    <td><img width="700" alt="Screenshot 2024-10-20 at 8 43 24 PM" src="https://github.com/user-attachments/assets/f8d1aa72-d2d2-4387-8787-2e4814918fc4"></td>
    <td><img width="700" alt="Screenshot 2024-10-21 at 1 32 56 AM" src="https://github.com/user-attachments/assets/af3950dd-eff8-44bd-9a07-48f4e53ef6ad"></td>
  </tr>
  <tr>
    <td><img width="700" alt="Screenshot 2024-10-21 at 1 33 19 AM" src="https://github.com/user-attachments/assets/e7d2cf34-8892-4d4b-89a9-4b8ca4568a05"></td>
    <td><img width="700" alt="Screenshot 2024-10-21 at 1 34 01 AM" src="https://github.com/user-attachments/assets/d1d98b0d-4714-4aef-9a2b-3912b2d190b0"></td>
  </tr>
</table>

<summary><h1>🚀 Bonus</h1></summary>

- The below table represents all the bonus features requested by Zeotap. All features have been implemented!

| Sl.No | _Feature Requested_                                           | _Details of feature_                                                                                                                                                                                                                                                                                               | Implemented |
|-------|---------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|
| 1     | Error handling for invalid rule strings.                      | The Rule Engine accurately throws a custom `ParseError` in case of errors such as missing an operator after operand, <br>imperfect closing of parenthesis, unexpected occurance of a token, etc                                                                                                                    | ✅         |
| 2     | Implement validations for attributes to be part of a catalog. | While parsing the rule to an AST and modifying the AST, the engine checks if the attributes are part of<br>the `ATTRIBUTE_CATALOG`, in the absence of which, a custom exception is raised.                                                                                                                         | ✅         |
| 3     | Modification of existing rules.                               | Rules can be modified by change of operator using the `node.change_operator()` API, change of operand (left and right operand values) using the `node.change_operand()` API and adding and removal of sub-expressions within the AST using `node.add_sub_expression()` and `node.remove_sub_expression()` APIs..   | ✅         |
| 4     | User-defined functions within the rule language.              | Custom functions have been tested and implemented. For example: `calculate_bonus(experience)`: A function to calculate bonus using the experience, `get_minimum_age()`: Returns some fixed value. I have also added support for the functions: `min()`, `max()` and `abs()`.                                       | ✅         |




<summary><h1>Testcases</h1></summary>

- To view the tests in detail, navigate to `run-tests.py`.

| Sl.No | Test Case                                                              | Passing (✅) / Not Passing (❌) |
|-------|------------------------------------------------------------------------|----------------------|
| 1     | Parsing a rule with simple condition. `[create_rule(rule:string)]`      | ✅                    |
| 2     | Parsing a rule with condition and function. `[create_rule(rule:string)]` | ✅                    |
| 3     | Combining Rules with OR. `[combine_rules([rules]:list)]`               | ✅                    |
| 4     | Combining Rules with AND. `[combine_rules([rules]:list)]`                | ✅                    |
| 5     | Evaluating Simple Condition `[evaluate_rule(ast:RootNode, data:JSON)]`   | ✅                    |
| 6     | Evaluating Combined Rules. `[evaluate_rule(ast:RootNode, data:JSON)]`    | ✅                    |
| 7     | Function Without Arguments                                             | ✅                    |
| 8     | Function With Arguments                                                | ✅                    |
| 9     | Negative Number Less Than                                              | ✅                    |
| 10    | Negative Number Greater Than                                           | ✅                    |
| 11    | AST Serialization and Deserialization                                  | ✅                    |
| 12    | AST Serialization and Deserialization Complex                          | ✅                    |



*fin*
