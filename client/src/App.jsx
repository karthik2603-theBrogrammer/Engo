import { useState, useEffect } from 'react';
import axios from 'axios';
import { Toaster, toast } from 'sonner';
import { Button } from '@nextui-org/button';

import Flow from './components/Flow';
import CombineRulesComponent from './components/CombineRulesComponent';
import EvaluateRulesComponent from './components/EvaluateRulesComponent';
import CreateRuleComponent from './components/CreateRuleComponent';
import SelectRuleComponent from './components/SelectRuleComponent'; // Import new component
import IntroductionToEngoComponent from './components/IntroductionToEngoComponent';
import './App.css';

function App() {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const [rules, setRules] = useState(null);
  const [selectedSetting, setSelectedSetting] = useState(null); // Initially null
  const [selectedRuleAst, setSelectedRuleAst] = useState(null);
  const [combinedAst, setCombinedAst] = useState(null);
  const [evaluationResult, setEvaluationResult] = useState(null);

  const toggleDrawer = () => setIsDrawerOpen(!isDrawerOpen);

  // Fetch all rules from the backend API
  const fetchRules = async () => {
    try {
      const response = await axios.get('http://localhost:5555/all-rules');
      setRules(response.data.result);
      toast.success("ENGO Rule engine is a go!")
    } catch (error) {
      toast.error(`Error fetching rules:, ${JSON.stringify(error)}`);
    }
  };

  useEffect(() => {
    fetchRules();
  }, []);

  const handleSelectRule = (rule) => {
    setSelectedRuleAst(rule.ast_json);
    setCombinedAst(null);
    setEvaluationResult(null);
    setIsDrawerOpen(false); // Close drawer after selection
    toast.success(`Viewing the selected rule's AST!`)
  };

  const handleCombineRules = async (selectedRuleIds, useMostFreqOperatorHeuristic, customOperator) => {
    try {
      const body = {
        rule_ids: selectedRuleIds,
        use_most_freq_operator_heuristic: useMostFreqOperatorHeuristic ? 1 : 0,
        custom_operator: customOperator,
        store_combined_rule: false,
      };
      const response = await axios.post('http://localhost:5555/rules/combine', body);
      setCombinedAst(response.data.combined_ast);
      setSelectedRuleAst(null);
      setEvaluationResult(null);
      setIsDrawerOpen(false);

      toast.success(`Viewing the combined rule's AST!`)
    } catch (error) {
      toast.error(`Error: ${JSON.stringify(error?.response?.data?.error)}`);
    }
  };

  const onEvaluateCombinedRules = async (requestBody) => {
    try {
      const response = await axios.post('http://localhost:5555/evaluate-combined-rules', requestBody);
      setEvaluationResult(response.data.result);
      response.data.result
        ? toast.success('Evaluation Result: Valid')
        : toast.error('Evaluation Result: Invalid User');
    } catch (error) {
      toast.error(`Error: ${JSON.stringify(error?.response?.data?.error)}`);
    }
  };

  return (
    <>
      {/* <HeroModalComponent /> */}
      <div className="relative z-100 flex">
        <img
          src="/engo-3.png"
          alt="engo-url"
          className={`absolute z-100 top-12 ${selectedSetting === null ? 'md:top-0' : 'md:-top-2'} left-1/2 ${selectedRuleAst == null ? 'md:left-1/2' : "md:left-[200px]"} transform -translate-x-1/2 md:h-[250px] h-[150px] md:w-[400px] w-[270px] bg-transparent object-contain`}
          height={100}
          width={100}
        />
      </div>
      {/* engo-arrow-to-console */}
      <div className="md:flex hidden absolute z-100 top-[70px] right-0  ">
        <img
          src="/arrow.png"
          alt="engo-url"
          className={`engo-arrow-to-console z-100 md:h-[80px] h-[70px]  w-[270px] md:w-[200px] bg-transparent object-contain`}
          height={100}
          width={100}
        />
      </div>
      <div
        className={`absolute flex items-center justify-center top-[200px] md:top-[220px] z-[20] left-1/2 transform -translate-x-1/2 w-full ${(selectedRuleAst === null && combinedAst == null) ? 'flex' : 'hidden'
          }`}
        style={{ pointerEvents: 'auto' }}
      >
        <p className="w-[90%] md:w-[60%] text-center text-[15px]">
          Engo is a custom Rule Engine built by me, Karthik Namboori. I am a 4th Year Computer Science Engineering student at PES University, Bangalore.
          For more, check out my work on {" "}
          <a
            href="https://github.com/karthik2603-theBrogrammer"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:underline"
          >
            GitHub
          </a>
          {" "}and{" "}
          <a
            href="https://www.linkedin.com/in/karthik-namboori-145238216/"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-500 hover:underline"
          >
            LinkedIn
          </a>
          . To get started, click the <strong>Toggle Console</strong> button and do give a read to the introduction section.
        </p>
      </div>



      <div
        id="drawer-navigation"
        className={`fixed top-0 left-0 z-40 w-[100%] md:w-[80%] h-screen p-4 overflow-y-auto transition-transform ${isDrawerOpen ? 'translate-x-0' : '-translate-x-full'
          } bg-gray-400 bg-opacity-20 backdrop-blur-lg backdrop-filter rounded-lg`}
      >
        <h5 className="text-base font-semibold text-gray-500 uppercase">Engo</h5>
        <button
          type="button"
          onClick={toggleDrawer}
          className="absolute top-2.5 end-2.5 text-gray-400 hover:bg-gray-200 hover:text-gray-900 p-1.5 rounded-lg"
        >
          <svg
            className="w-5 h-5"
            xmlns="http://www.w3.org/2000/svg"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fillRule="evenodd"
              d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 011.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
              clipRule="evenodd"
            />
          </svg>
          <span className="sr-only">Close menu</span>
        </button>

        <div className="py-4 flex flex-col items-center justify-center gap-2 mt-3">
          <h1 className="font-bold text-5xl text-center">Rule Engine Console</h1>
          <p className="text-sm text-center">
            Use this console to fetch and select rules, render their ASTs, modify rules, and more!
          </p>
        </div>

        <div className="flex gap-4 my-4 items-center justify-center flex-wrap">
          {['Create Rule', 'Select Rule', 'Combine Rules', 'Evaluate Rules'].map((setting) => (
            <Button
              key={setting}
              className="px-4 py-2 rounded-lg"
              variant={selectedSetting === setting ? 'shadow' : 'flat'}
              color="primary"
              onClick={() => setSelectedSetting(setting)}
            >
              {setting}
            </Button>
          ))}
        </div>

        <div className="py-4">
          {
            selectedSetting === null && (
              <IntroductionToEngoComponent/>
            )
          }
          {selectedSetting === 'Select Rule' && (
            <SelectRuleComponent rules={rules} onSelectRule={handleSelectRule} />
          )}
          {selectedSetting === 'Create Rule' && <CreateRuleComponent fetchRules={fetchRules} />}
          {selectedSetting === 'Combine Rules' && (
            <CombineRulesComponent rules={rules} onCombineRules={handleCombineRules} />
          )}
          {selectedSetting === 'Evaluate Rules' && (
            <EvaluateRulesComponent
              rules={rules}
              onEvaluateCombinedRules={onEvaluateCombinedRules}
              evaluationResult={evaluationResult}
            />
          )}
        </div>
      </div>

      <button
        className="absolute top-4 right-4 z-40 text-white bg-blue-700 hover:bg-blue-800 focus:ring-1 font-medium rounded-lg text-sm px-5 py-2.5"
        onClick={toggleDrawer}
      >
        Toggle Console!
      </button>

      <Flow astJson={selectedRuleAst || combinedAst} />
      <Toaster richColors position="bottom-right" expand={true} />
    </>
  );
}

export default App;
