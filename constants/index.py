VALID_OPERATORS = {'<', '>', '<=', '>=', '=', '==', '!=', '<>'}
ATTRIBUTE_CATALOG = {'age', 'department', 'salary', 'experience', "income", "spend"}
VALID_LOGICAL_OPERATORS = {'AND', 'OR', 'NOT'}


FUNCTIONS = {
    'get_minimum_age':                              lambda: 18,
    'calculate_bonus':                              lambda experience: experience * 1000,
    'average_salary':                               lambda: 40000,
    'salary_for_age_experience':                    lambda age, experience:  (age * experience * 1000) + 1000,
    'max':                                          lambda x, y: max(x, y),
    'min':                                          lambda x, y: min(x, y),
    'abs':                                          lambda x: abs(x)
}