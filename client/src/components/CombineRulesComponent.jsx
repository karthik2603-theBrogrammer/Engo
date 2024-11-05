import { useState } from 'react';
import { Button } from '@nextui-org/button';
import { Input } from '@nextui-org/input';
import { toast } from 'sonner';

import { formatDateToIST } from '../../utils'; // Utility function for date formatting

function CombineRulesComponent({ rules, onCombineRules }) {
    const [selectedRuleIds, setSelectedRuleIds] = useState([]); // Track selected rules
    const [useHeuristic, setUseHeuristic] = useState(false); // Toggle heuristic usage
    const [customOperator, setCustomOperator] = useState(''); // Store custom operator

    // Handle rule selection/deselection
    const handleRuleSelection = (ruleId) => {
        setSelectedRuleIds((prev) =>
            prev.includes(ruleId)
                ? prev.filter((id) => id !== ruleId) // Deselect rule
                : [...prev, ruleId] // Select rule
        );
    };

    const handleSubmit = () => {
        if (selectedRuleIds.length < 2) {
            toast.warning('Please select at least two rules to combine.');
            return;
        }

        onCombineRules(selectedRuleIds, useHeuristic, customOperator);
    };

    // Sort rules based on `updated_at` (latest first)
    const sortedRules = [...(rules || [])].sort(
        (a, b) => new Date(b.updated_at) - new Date(a.updated_at)
    );

    return (
        <div className="flex flex-col items-center justify-center gap-4">
            <h1 className="text-2xl">Combine Rules</h1>
            <p className="text-center">
                Select multiple rules to combine them using a custom operator or heuristic.
            </p>

            <div className="flex flex-col items-center justify-center ">
                <div className="flex flex-col md:flex-row gap-4 mt-4 w-full max-w-md">
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
                        placeholder="e.g., AND, OR"
                        value={customOperator}
                        onChange={(e) => setCustomOperator(e.target.value)}
                    />
                </div>

                <Button
                    className="mt-4 px-4 py-2 w-[100%]"
                    onClick={handleSubmit}
                    variant="light"
                    color="primary"
                >
                    Combine Selected Rules
                </Button>
            </div>

            <div className="w-full mt-4">
                {sortedRules.length ? (
                    sortedRules.map((rule) => (
                        <div
                            key={rule.id}
                            className={`flex items-center justify-between p-3 m-2 rounded cursor-pointer transition-colors duration-200 ${selectedRuleIds.includes(rule.id) ? 'bg-blue-300' : 'bg-gray-200'
                                }`}
                            onClick={() => handleRuleSelection(rule.id)}
                        >
                            <p className="font-bold">{rule.rule_text}</p>
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
    );
}

export default CombineRulesComponent;
