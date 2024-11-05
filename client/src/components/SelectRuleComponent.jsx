import { useState } from 'react';

import { titleCase, formatDateToIST } from '../../utils';


function SelectRuleComponent({ rules, onSelectRule }) {
  const [selectedRuleId, setSelectedRuleId] = useState(null); // Track selected rule

  const handleRuleSelection = (rule) => {
    setSelectedRuleId(rule.id); // Set selected rule ID
    onSelectRule(rule); // Pass selected rule to parent
  };
  const sortedRules = [...(rules || [])].sort(
    (a, b) => new Date(b.updated_at) - new Date(a.updated_at)
  );

  return (
    <div className="flex flex-col items-center justify-center ">
      <div className="flex flex-col items-center justify-center my-2">
      <h1 className="text-2xl mb-4">Select a Rule</h1>
      <p className="">Select a rule fo which you want to view the Abstract Syntax Tree.</p>
      </div>
      {sortedRules && sortedRules.length ? (
        sortedRules.map((rule, key) => (
          <div
            key={rule.id}
            className={`flex w-full justify-between p-3 m-1 rounded cursor-pointer transition-colors duration-200 ${
              selectedRuleId === rule.id ? 'bg-blue-300' : 'bg-gray-200'
            }`}
            onClick={() => handleRuleSelection(rule)}
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
  );
}

export default SelectRuleComponent;

