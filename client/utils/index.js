export function titleCase(str) {
  return str
    .toLowerCase()
    .split(" ")
    .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
    .join(" ");
}

export function formatDateToIST(dateString) {
  const date = new Date(dateString);

  // Format the date to IST with day, date, time, and time zone
  return date.toLocaleString("en-GB", {
    timeZone: "Asia/Kolkata",
    weekday: "short", // Sat
    day: "2-digit", // 19
    month: "short", // Oct
    year: "numeric", // 2024
    hour: "2-digit", // 16
    minute: "2-digit", // 52
    second: "2-digit", // 09
    hour12: true, // 24-hour format
  });
}

export function getArgumentValuesFromJson(args) {
  if (!args || args.length === 0) {
    return "()"; // Return empty parentheses if no arguments
  }

  // Map over the args, extract their values, and join them correctly
  const argsString = args.map((arg) => arg.value).join(",");

  // Wrap in parentheses
  return `(${argsString})`;
}

export const supportedFunctions = [
  {
    name: "get_minimum_age()",
    parameters: [],
    description: "Returns the minimum required age value (18)",
    example: "get_minimum_age() >= age",
    returns: "number",
  },
  {
    name: "calculate_bonus(experience)",
    parameters: ["experience"],
    description:
      "Calculates bonus amount based on years of experience (experience * 1000)",
    example: "calculate_bonus(5) > 4000",
    returns: "number",
  },
  {
    name: "average_salary()",
    parameters: [],
    description: "Returns the benchmark average salary value (40000)",
    example: "salary > average_salary()",
    returns: "number",
  },
  {
    name: "salary_for_age_experience(age, experience)",
    parameters: ["age", "experience"],
    description:
      "Calculates expected salary based on age and experience ((age * experience * 1000) + 1000)",
    example: "salary > salary_for_age_experience(30, 5)",
    returns: "number",
  },
  {
    name: "max(x, y)",
    parameters: ["x", "y"],
    description: "Returns the larger of two numbers",
    example: "max(salary, 50000) > average_salary()",
    returns: "number",
  },
  {
    name: "min(x, y)",
    parameters: ["x", "y"],
    description: "Returns the smaller of two numbers",
    example: "min(age, experience) > 5",
    returns: "number",
  },
  {
    name: "abs(x)",
    parameters: ["x"],
    description: "Returns the absolute value of a number",
    example: "abs(salary_difference) > 5000",
    returns: "number",
  },
];

export const introductionComponents = [
  {
    title: "Custom Rule Engine",
    description:
      "Engo is a custom rule engine that parses rules defined in its specific language called Engolang. It is built to define rules and check the validity of users based on specific rules of consideration.",
  },
  {
    title: "AST and DAG Representation",
    description:
      "Rules are parsed and visualized into Abstract Syntax Trees (ASTs). ASTs are commonly used in compiler frontend stages to represent the syntax of parsed rules in a supported language. Engo optimizes ASTs into Directed Acyclic Graphs (DAGs), eliminating redundant calculations and reusing pre-computed results. The user interface represents these DAGs after optimization using React Flow.",
  },
  {
    title: "Feature Set",
    description:
      "Engo supports various features, including rule creation, rule combination, rule evaluation, and modification. You can modify rules by changing operands, changing operators, adding sub-expressions, or removing sub-expressions.",
  },
  {
    title: "Tokenization and Custom Functions",
    description:
      "Engolang uses regular expressions (similar to the Lex software) to tokenize rules. Additionally, Engo supports user-defined custom functions (proceed to 'Create Rule' to view them), which can be extended by anyone using Engo.",
    url: "https://github.com/karthik2603-theBrogrammer/Karthik-Namboori-Zeotap-SDE-Intern?tab=readme-ov-file#engos-tokenizer",
  },
  {
    title: "Tech Stack",
    description:
      "Engo is built using React and Flask for the frontend and backend, respectively. Postgres is used as the database, and Docker is used for end-to-end shipment and deployment.",
  },
  {
    title: "Accessing Engo",
    description:
      "The engine can be accessed via the Python shell or via APIs within the self-hosted using Docker solution. Engo supports both Linux/amd64 and Linux/arm64 architectures.",
    url: "https://github.com/karthik2603-theBrogrammer/Karthik-Namboori-Zeotap-SDE-Intern?tab=readme-ov-file#-how-to-run-and-use-engo-",
  },
];
