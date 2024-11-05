import { useState } from 'react';
import { Toaster, toast } from 'sonner';
import { Button } from '@nextui-org/button';
import { Input } from '@nextui-org/input';

import { titleCase, formatDateToIST } from '../../utils';

const ATTRIBUTE_CATALOG = ['age', 'department', 'salary', 'experience', 'income', 'spend'];
const INTEGER_ATTRIBUTE_CATALOG = ['age', 'salary', 'experience', 'income', 'spend'];

function EvaluateRulesComponent({ rules, onEvaluateCombinedRules, evaluationResult }) {
  const [selectedRuleIds, setSelectedRuleIds] = useState([]); // Support for multiple rules
  const [dataForEvaluation, setDataForEvaluation] = useState({});
  const [useHeuristic, setUseHeuristic] = useState(false); // Toggle heuristic usage
  const [customOperator, setCustomOperator] = useState('AND'); // Default operator

  // Helper function to ensure numbers are correctly parsed
  const parseValue = (attribute, value) => {
    if (INTEGER_ATTRIBUTE_CATALOG.includes(attribute)) {
      const parsedValue = parseFloat(value);
      return isNaN(parsedValue) ? '' : parsedValue; // Return empty string if not a valid number
    }
    return value; // Return as-is for non-numeric fields
  };

  const handleInputChange = (attribute, value) => {
    setDataForEvaluation((prevData) => ({
      ...prevData,
      [attribute]: parseValue(attribute, value),
    }));
  };

  const handleRuleSelect = (ruleId) => {
    setSelectedRuleIds((prev) =>
      prev.includes(ruleId)
        ? prev.filter((id) => id !== ruleId) // Remove if already selected
        : [...prev, ruleId] // Add if not selected
    );
  };

  const handleSubmit = () => {
    if (selectedRuleIds.length > 0) {
      onEvaluateCombinedRules({
        rule_ids: selectedRuleIds,
        data_for_evaluation: dataForEvaluation,
        use_most_freq_operator_heuristic: useHeuristic ? 1 : 0,
        custom_operator: customOperator,
        store_combined_rule: false,
      });
    } else {
      toast.warning('Please select at least one rule to evaluate.');
    }
  };

  // Sort rules based on `updated_at` (latest first)
  const sortedRules = [...(rules || [])].sort(
    (a, b) => new Date(b.updated_at) - new Date(a.updated_at)
  );

  return (
    <>
      <div className="flex flex-col items-center justify-center gap-2">
        <div className="flex flex-col items-center justify-center gap-2">
          <h1 className="text-2xl">Evaluate Rules</h1>
          <p className='text-center'>This feature allows you to evaluate users based on both, A single rule and a 
             combined set of rules. {"(If no operator choice is mentioned, the engine assumes a default of OR operator to combine the rules.)"}
        </p>
        <p className='text-center'>
          On evaluation, if the data satisfies the rule, you will be prompted with "Valid User!", else you will be prompted with "Invalid User!"
        </p>
        </div>

        <div className="flex flex-col gap-2">
          <div className="flex md:grid md:grid-cols-3 md:place-items-center items-start mt-4 gap-3 flex-col">
            {ATTRIBUTE_CATALOG.map((attribute, key) => (
              <Input
                key={key}
                type="text"
                label={titleCase(attribute)}
                value={dataForEvaluation[attribute] || ''}
                onChange={(e) => handleInputChange(attribute, e.target.value)}
              />
            ))}
          </div>

          <div className="flex gap-4 mt-4">
            <label className="flex items-center gap-2">
              <input
                type="checkbox"
                checked={useHeuristic}
                onChange={(e) => setUseHeuristic(e.target.checked)}
              />
              Use Most Frequent Operator Heuristic
            </label>

            <Input
              type="text"
              label="Custom Operator"
              value={customOperator}
              onChange={(e) => setCustomOperator(e.target.value)}
            />
          </div>

          <Button
            className="mt-4 px-4 py-2"
            onClick={handleSubmit}
            variant="light"
            color="primary"
          >
            Evaluate Combined Rules
          </Button>
        </div>

        <div className="w-full mt-4">
          {sortedRules && sortedRules.length ? (
            sortedRules.map((rule, key) => (
              <div
                key={rule.id}
                className={`flex items-center justify-between p-3 m-2 rounded cursor-pointer  transition-colors duration-200 ${
                  selectedRuleIds.includes(rule.id) ? 'bg-blue-300' : 'bg-gray-200'
                }`}
                onClick={() => handleRuleSelect(rule.id)}
              >
                <p className="font-bold">{key + 1}. {rule.rule_text}</p>
                <p className="text-sm text-center w-[250px]">
                  {formatDateToIST(rule?.updated_at)}
                </p>
              </div>
            ))
          ) : (
            <p>No rules available</p>
          )}
        </div>
      </div>
    </>
  );
}

export default EvaluateRulesComponent;
