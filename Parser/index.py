from Node import Node

from constants import ATTRIBUTE_CATALOG, VALID_OPERATORS, FUNCTIONS

class ParseError(Exception):
    def __init__(self, message, position=None, token=None):
        super().__init__(message)
        self.position = position
        self.token = token

class Parser:
    def __init__(self, tokens, attribute_catalog=None):
        self.tokens = tokens
        self.pos = 0  # Current position in the token list
        self.current_token = self.tokens[self.pos] if self.tokens else None
        self.attribute_catalog = attribute_catalog or ATTRIBUTE_CATALOG

    def consume(self, expected_kinds=None):
        token = self.current_token
        if expected_kinds and token[0] not in expected_kinds:
            raise ParseError(f"Expected token kind {expected_kinds}, but got {token} at position {self.pos}", position=self.pos, token=token)
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            self.current_token = None
        return token

    def parse(self):
        node = self.parse_expression()
        if self.current_token is not None:
            raise ParseError(f"Unexpected token at position {self.pos}: {self.current_token}")
        return node

    def parse_expression(self):
        node = self.parse_term()
        while self.current_token and self.current_token[0] == 'OR':
            self.consume(['OR'])
            right = self.parse_term()
            node = Node('operator', value='OR', left=node, right=right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.current_token and self.current_token[0] == 'AND':
            self.consume(['AND'])
            right = self.parse_factor()
            node = Node('operator', value='AND', left=node, right=right)
        return node

    def parse_factor(self):
        if self.current_token and self.current_token[0] == 'NOT':
            self.consume(['NOT'])
            node = self.parse_factor()
            node = Node('operator', value='NOT', left=node)
            return node
        elif self.current_token and self.current_token[0] == 'LPAREN':
            self.consume(['LPAREN'])
            node = self.parse_expression()
            if self.current_token and self.current_token[0] == 'RPAREN':
                self.consume(['RPAREN'])
            else:
                raise ParseError(f"Expected closing parenthesis at position {self.pos}")
            return node
        else:
            node = self.parse_condition()
            return node

    def parse_condition(self):
        if self.current_token and self.current_token[0] in ('IDENT', 'FUNCTION'):
            left_operand = self.parse_value()
            if self.current_token and self.current_token[0] == 'OP':
                op_token = self.consume(['OP'])
                op = op_token[1]
                if op not in VALID_OPERATORS:
                    raise ParseError(f"Invalid operator '{op}' at position {self.pos - 1}", position=self.pos - 1, token=op_token)
                right_operand = self.parse_value()
                node = Node('condition', value=(left_operand, op, right_operand))
                return node
            else:
                raise ParseError(f"Expected an operator after operand at position {self.pos}")
        else:
            raise ParseError(f"Expected an operand at position {self.pos}")

    def parse_value(self):
        if self.current_token is None:
            raise ParseError(f"Expected a value at position {self.pos}", position=self.pos)
        token_type, token_value = self.current_token
        if token_type == 'NUMBER':
            self.consume(['NUMBER'])
            if '.' in token_value:
                return Node('constant', value=float(token_value))
            else:
                return Node('constant', value=int(token_value))
            
        elif token_type == 'STRING':
            self.consume(['STRING'])
            return Node('constant', value=token_value.strip("'"))
        elif token_type == 'IDENT':
            self.consume(['IDENT'])
            if token_value not in self.attribute_catalog:
                raise ParseError(f"Unknown attribute '{token_value}' at position {self.pos - 1}", position=self.pos - 1)
            return Node('variable', value=token_value)
        elif token_type == 'FUNCTION':
            return self.parse_function_call()
        elif token_type == 'LPAREN':
            self.consume(['LPAREN'])
            expr = self.parse_expression()
            if self.current_token and self.current_token[0] == 'RPAREN':
                self.consume(['RPAREN'])
                return expr
            else:
                raise ParseError(f"Expected closing parenthesis at position {self.pos}")
        else:
            raise ParseError(f"Unexpected token {self.current_token} at position {self.pos}", position=self.pos)

    def parse_function_call(self):
        func_token = self.consume(['FUNCTION'])
        func_name = func_token[1]
        if func_name not in FUNCTIONS:
            raise ParseError(f"Unknown function '{func_name}' at position {self.pos - 1}", position=self.pos - 1)
        self.consume(['LPAREN'])
        args = self.parse_arguments()
        if self.current_token and self.current_token[0] == 'RPAREN':
            self.consume(['RPAREN'])
        else:
            raise ParseError(f"Expected closing parenthesis for function call at position {self.pos}")
        return Node('function', value=func_name, args=args)

    def parse_arguments(self):
        args = []
        while self.current_token and self.current_token[0] != 'RPAREN':
            arg = self.parse_value()
            args.append(arg)
            if self.current_token and self.current_token[0] == 'COMMA':
                self.consume(['COMMA'])
            else:
                break
        return args





# class Parser:
#     def __init__(self, tokens):
#         self.tokens = tokens
#         self.pos = 0  # Current position in the token list
#         self.current_token = self.tokens[self.pos] if self.tokens else None

#     def consume(self, expected_kinds=None):
#         token = self.current_token
#         if expected_kinds and token[0] not in expected_kinds:
#             raise ValueError(f"Expected token kind {expected_kinds}, but got {token}")
#         self.pos += 1
#         if self.pos < len(self.tokens):
#             self.current_token = self.tokens[self.pos]
#         else:
#             self.current_token = None
#         return token

#     def parse(self):
#         node = self.parse_expression()
#         if self.current_token is not None:
#             raise ValueError(f"Unexpected token at the end: {self.current_token}")
#         return node

#     def parse_expression(self):
#         """
#         Parses expressions separated by OR.
#         """
#         node = self.parse_term()
#         while self.current_token and self.current_token[0] == 'OR':
#             self.consume(['OR'])
#             right = self.parse_term()
#             node = Node('operator', value='OR', left=node, right=right)
#         return node

#     def parse_term(self):
#         """
#         Parses terms separated by AND.
#         """
#         node = self.parse_factor()
#         while self.current_token and self.current_token[0] == 'AND':
#             self.consume(['AND'])
#             right = self.parse_factor()
#             node = Node('operator', value='AND', left=node, right=right)
#         return node

#     def parse_factor(self):
#         """
#         Parses factors, which could be conditions, parentheses, or NOT expressions.
#         """
#         if self.current_token and self.current_token[0] == 'NOT':
#             self.consume(['NOT'])
#             node = self.parse_factor()
#             node = Node('operator', value='NOT', left=node)
#             return node
#         elif self.current_token and self.current_token[0] == 'LPAREN':
#             self.consume(['LPAREN'])
#             node = self.parse_expression()
#             if self.current_token and self.current_token[0] == 'RPAREN':
#                 self.consume(['RPAREN'])
#             else:
#                 raise ValueError("Expected closing parenthesis")
#             return node
#         else:
#             node = self.parse_condition()
#             return node

#     def parse_condition(self):
#         """
#         Parses a condition in the form IDENT OP VALUE.
#         """
#         if self.current_token and self.current_token[0] == 'IDENT':
#             attr_token = self.consume(['IDENT'])
#             if self.current_token and self.current_token[0] == 'OP':
#                 op_token = self.consume(['OP'])
#                 if self.current_token:
#                     if self.current_token[0] in ('NUMBER', 'STRING', 'IDENT'):
#                         value_token = self.consume(['NUMBER', 'STRING', 'IDENT'])
#                         value = value_token[1]
#                         # Convert NUMBER tokens to float/int
#                         if value_token[0] == 'NUMBER':
#                             if '.' in value:
#                                 value = float(value)
#                             else:
#                                 value = int(value)
#                         elif value_token[0] == 'STRING':
#                             value = value.strip("'")
#                         else:
#                             # IDENT token, treat value as string (e.g., department = Sales)
#                             value = value_token[1]
#                         node = Node('condition', value=(attr_token[1], op_token[1], value))
#                         return node
#                     else:
#                         raise ValueError(f"Expected a value after operator at position {self.pos}, but got {self.current_token}")
#                 else:
#                     raise ValueError(f"Unexpected end of input after operator at position {self.pos}")
#             else:
#                 if self.current_token:
#                     raise ValueError(f"Expected an operator after identifier at position {self.pos}, but got {self.current_token}")
#                 else:
#                     raise ValueError(f"Unexpected end of input after identifier at position {self.pos}")
#         else:
#             if self.current_token:
#                 raise ValueError(f"Expected an identifier at the beginning of a condition at position {self.pos}, but got {self.current_token}")
#             else:
#                 raise ValueError(f"Unexpected end of input when expecting an identifier at position {self.pos}")


