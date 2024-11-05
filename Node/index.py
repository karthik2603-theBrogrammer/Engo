from constants import VALID_OPERATORS, FUNCTIONS, ATTRIBUTE_CATALOG, VALID_LOGICAL_OPERATORS

class Node:
    def __init__(self, node_type, value=None, left=None, right=None, args=None):
        """
        Represents a node in the AST.

        :param node_type: 'operator', 'condition', 'function', 'constant', or 'variable'
        :param value: For 'operator' nodes, it can be 'AND', 'OR', or 'NOT'.
                      For 'condition' nodes, it's a tuple (attribute/Node, operator, operand/Node).
                      For 'function' nodes, it's the function name.
                      For 'constant' nodes, it's a Boolean or numeric value.
                      For 'variable' nodes, it's the variable name.
        :param left: Left child node.
        :param right: Right child node (optional for 'NOT' operator).
        :param args: List of argument nodes for 'function' nodes.
        """
        self.node_type = node_type
        self.value = value
        self.left = left
        self.right = right
        self.args = args or []
        self.id = self.get_id()  # Unique identifier for the node
        self.VALID_OPERATORS = VALID_OPERATORS
        self.VALID_LOGICAL_OPERATORS = VALID_LOGICAL_OPERATORS
        self.ATTRIBUTE_CATALOG = ATTRIBUTE_CATALOG

    def get_id(self):
        """
        Generates a unique identifier for the node based on its content.
        """
        if self.node_type == 'condition':
            attr, op, val = self.value
            attr_id = attr.get_id() if isinstance(attr, Node) else self.sanitize(attr)
            op_id = self.sanitize(op)
            val_id = val.get_id() if isinstance(val, Node) else self.sanitize(val)
            return f"COND_{attr_id}_{op_id}_{val_id}"
        elif self.node_type == 'operator':
            left_id = self.left.get_id() if self.left else 'None'
            right_id = self.right.get_id() if self.right else 'None'
            return f"{left_id}-{self.value}-{right_id}"
        elif self.node_type == 'function':
            args_ids = '_'.join(arg.get_id() for arg in self.args)
            return f"FUNC_{self.value}_{args_ids}"
        elif self.node_type == 'constant':
            return f"CONST_{self.sanitize(self.value)}"
        elif self.node_type == 'variable':
            return f"VAR_{self.sanitize(self.value)}"
        else:
            return 'Unknown'
        
    def __repr__(self):
        if self.node_type == 'operator':
            return f"Node(node_type={self.node_type}, value={self.value})"
        elif self.node_type == 'condition':
            attr, op, val = self.value
            return f"Node(node_type={self.node_type}, value={self.value})"
        else:
            return str(self.value)

    @staticmethod
    def sanitize(value):
        if isinstance(value, str):
            return value.replace(' ', '_').replace('-', '_').replace('&', 'and')
        else:
            return str(value)

        
    def replace_node(self, target_id, new_node):
        """
        Replaces the node with the given target_id with new_node in the AST.
        """
        if self.id == target_id:
            self.node_type = new_node.node_type
            self.value = new_node.value
            self.left = new_node.left
            self.right = new_node.right
            return True
        else:
            replaced = False
            if self.left:
                replaced = self.left.replace_node(target_id, new_node)
            if not replaced and self.right:
                replaced = self.right.replace_node(target_id, new_node)
            return replaced
        

    def change_operator(self, target_id, new_operator):
        """
        Changes the operator of an operator node (AND, OR, etc) or condition node.

        :param target_id: The ID of the target node.
        :param new_operator: The new operator (must be in VALID_OPERATORS).
        :return: True if the operator was changed, False otherwise.
        """
        if self.id == target_id:
            if self.node_type == 'operator' or self.node_type == 'condition':
                # Validate new operator
                if new_operator not in self.VALID_OPERATORS and new_operator not in self.VALID_LOGICAL_OPERATORS:
                    raise ValueError(f"Operator '{new_operator}' is not in VALID_OPERATORS and VALID_LOGICAL_OPERATORS")
                new_operator = new_operator.upper()
                if self.node_type == 'operator':
                    self.value = new_operator
                elif self.node_type == 'condition':
                    attr, _, val = self.value
                    self.value = (attr, new_operator, val)
                self.id = self.get_id()
                return True
            else:
                raise ValueError(f"Node with ID '{target_id}' is not an operator or condition node")
        else:
            changed = False
            if self.left:
                changed = self.left.change_operator(target_id, new_operator)
            if not changed and self.right:
                changed = self.right.change_operator(target_id, new_operator)
            return changed

    def change_operand(self, target_id, new_left_operand=None, new_right_operand=None):
        """
        Changes the operands of a condition node.

        :param target_id: The ID of the target condition node.
        :param new_left_operand: The new left operand (attribute or Node).
        :param new_right_operand: The new right operand (value or Node).
        :return: True if the operand was changed, False otherwise.
        """
        if self.id == target_id and self.node_type == 'condition':
            attr, op, val = self.value

            # Update the left operand if provided
            if new_left_operand is not None:
                # Validate left operand
                if isinstance(new_left_operand, str):
                    if new_left_operand not in self.ATTRIBUTE_CATALOG:
                        raise ValueError(f"Attribute '{new_left_operand}' is not in ATTRIBUTE_CATALOG")
                    attr = new_left_operand
                elif isinstance(new_left_operand, Node):
                    attr = new_left_operand
                else:
                    raise ValueError(f"Invalid left operand type: {type(new_left_operand)}")

            # Update the right operand if provided
            if new_right_operand is not None:
                # Right operand can be a value or a Node
                if isinstance(new_right_operand, (int, float, str, Node)):
                    val = new_right_operand
                else:
                    raise ValueError(f"Invalid right operand type: {type(new_right_operand)}")

            self.value = (attr, op, val)
            self.id = self.get_id()
            return True
        else:
            changed = False
            if self.left:
                changed = self.left.change_operand(target_id, new_left_operand, new_right_operand)
            if not changed and self.right:
                changed = self.right.change_operand(target_id, new_left_operand, new_right_operand)
            return changed

        
    def add_sub_expression(self, parent_id, sub_expr_ast, position='left'):
        if self.id == parent_id and self.node_type == 'operator':
            if position == 'left':
                self.left = sub_expr_ast
            elif position == 'right':
                self.right = sub_expr_ast
            else:
                raise ValueError("Position must be 'left' or 'right'")
            self.id = self.get_id()
            return True
        else:
            added = False 
            if self.left:
                added = self.left.add_sub_expression(parent_id, sub_expr_ast, position)
            if not added and self.right:
                added = self.right.add_sub_expression(parent_id, sub_expr_ast, position)
            return added
        
    def remove_sub_expression(self, target_id):
        """
        Removes a sub-expression with the given target_id.
        Ensures that the AST remains logically correct after removal.
        """
        # If the left child is the target
        if self.left and self.left.id == target_id:
            # Replace the current node with the right child if it exists
            if self.right:
                self._promote_child('right')
            else:
                self.left = None
                self.id = self.get_id()
            return True

        # If the right child is the target
        elif self.right and self.right.id == target_id:
            # Replace the current node with the left child if it exists
            if self.left:
                self._promote_child('left')
            else:
                self.right = None
                self.id = self.get_id()
            return True

        # Recursively search in left and right children
        removed = False
        if self.left:
            removed = self.left.remove_sub_expression(target_id)
        if not removed and self.right:
            removed = self.right.remove_sub_expression(target_id)

        return removed

    def _promote_child(self, child_position):
        """
        Promote a child (either 'left' or 'right') to replace the current node.
        :Private Method for this class.
        """
        if child_position == 'left':
            child = self.left
        else:
            child = self.right

        # Copy the child node's properties into the current node
        self.node_type = child.node_type
        self.value = child.value
        self.left = child.left
        self.right = child.right
        self.id = self.get_id()


    
    def get_text(self):
        """
        Recursively converts the AST into a readable text representation of the rule.
        """
        if self.node_type == 'condition':
            attr, op, val = self.value
            left_text = attr.get_text() if isinstance(attr, Node) else str(attr)
            right_text = val.get_text() if isinstance(val, Node) else str(val)
            return f"({left_text} {op} {right_text})"

        elif self.node_type == 'operator':
            if self.value == 'NOT':
                left_text = self.left.get_text() if self.left else ""
                return f"(NOT {left_text})"
            else:
                left_text = self.left.get_text() if self.left else ""
                right_text = self.right.get_text() if self.right else ""
                return f"({left_text} {self.value} {right_text})"

        elif self.node_type == 'function':
            args_text = ", ".join(arg.get_text() for arg in self.args)
            return f"{self.value}({args_text})"

        elif self.node_type == 'constant':
            return str(self.value)

        elif self.node_type == 'variable':
            return self.value

        else:
            raise ValueError(f"Unknown node type: {self.node_type}")
        

# def get_id(self):
    #     """
    #     Generates a unique identifier for the node based on its content.
    #     """
    #     if self.node_type == 'condition':
    #         return f"COND_{hash(self.value)}"
    #     elif self.node_type == 'operator':
    #         left_id = self.left.get_id() if self.left else 'None'
    #         right_id = self.right.get_id() if self.right else 'None'
    #         return f"OP_{self.value}_{left_id}_{right_id}"
    #     elif self.node_type == 'constant':
    #         return f"CONST_{self.value}"
    #     else:
    #         return 'Unknown'
