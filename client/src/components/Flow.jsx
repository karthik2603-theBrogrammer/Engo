import React, { useState, useCallback, useMemo, useEffect } from 'react';
import {
  ReactFlow,
  Controls,
  Background,
  applyNodeChanges,
  applyEdgeChanges,
  addEdge,
  MarkerType,
} from '@xyflow/react'; // Adjust import based on your setup
import '@xyflow/react/dist/style.css';

import CustomNode from './CustomNode'; // Import the CustomNode component

// AST JSON input
const astJson = {
  "id": "COND_VAR_age_>_CONST_30-AND-COND_VAR_department_=_CONST_Marketing-AND-COND_VAR_salary_>_CONST_20000-OR-COND_VAR_experience_>_CONST_5",
  "left": {
    "id": "COND_VAR_age_>_CONST_30-AND-COND_VAR_department_=_CONST_Marketing",
    "left": {
      "id": "COND_VAR_age_>_CONST_30",
      "left": {
        "id": "VAR_age",
        "node_type": "variable",
        "value": "age"
      },
      "node_type": "condition",
      "operator": ">",
      "right": {
        "id": "CONST_30",
        "node_type": "constant",
        "value": 30
      }
    },
    "node_type": "operator",
    "right": {
      "id": "COND_VAR_department_=_CONST_Marketing",
      "left": {
        "id": "VAR_department",
        "node_type": "variable",
        "value": "department"
      },
      "node_type": "condition",
      "operator": "=",
      "right": {
        "id": "CONST_Marketing",
        "node_type": "constant",
        "value": "Marketing"
      }
    },
    "value": "AND"
  },
  "node_type": "operator",
  "right": {
    "id": "COND_VAR_salary_>_CONST_20000-OR-COND_VAR_experience_>_CONST_5",
    "left": {
      "id": "COND_VAR_salary_>_CONST_20000",
      "left": {
        "id": "VAR_salary",
        "node_type": "variable",
        "value": "salary"
      },
      "node_type": "condition",
      "operator": ">",
      "right": {
        "id": "CONST_20000",
        "node_type": "constant",
        "value": 20000
      }
    },
    "node_type": "operator",
    "right": {
      "id": "COND_VAR_experience_>_CONST_5",
      "left": {
        "id": "VAR_experience",
        "node_type": "variable",
        "value": "experience"
      },
      "node_type": "condition",
      "operator": ">",
      "right": {
        "id": "CONST_5",
        "node_type": "constant",
        "value": 5
      }
    },
    "value": "OR"
  },
  "value": "AND"
};

// Helper function to randomly adjust position
function adjustPosition(x, y, occupiedPositions) {
  const adjustmentRange = 80;
  let newX = x;
  let newY = y;

  while (occupiedPositions.has(`${newX}-${newY}`)) {
    newX = x + Math.floor(Math.random() * adjustmentRange) - adjustmentRange / 2;
    newY = y + Math.floor(Math.random() * adjustmentRange) - adjustmentRange / 2;
  }

  occupiedPositions.add(`${newX}-${newY}`);
  return { x: newX, y: newY };
}

// Function to calculate node positions and avoid overlap
function calculatePositions(ast, level = 0, xOffset = 0, spacingX = 200, spacingY = 150) {
  const nodes = [];
  const edges = [];
  const nodeMap = new Map(); // To reuse nodes by ID
  const occupiedPositions = new Set(); // Track used positions

  // Handle node changes from CustomNode
  const handleNodeChange = (updatedNodeData) => {
    setNodes((nds) =>
      nds.map((node) =>
        node.id === updatedNodeData.id
          ? { ...node, data: { ...node.data, node: updatedNodeData } }
          : node
      )
    );
  };
  function traverse(node, x = 0, y = 0, parentId = null) {
    // Adjust position if already occupied
    const { x: adjustedX, y: adjustedY } = adjustPosition(x, y, occupiedPositions);

    // Reuse or create node
    if (!nodeMap.has(node.id)) {
        const newNode = {
            id: node.id,
            type: 'customNode', // Use custom node type
            data: { node, onNodeChange: handleNodeChange }, // Pass node data and change handler
            position: { x: adjustedX, y: adjustedY },
        };
        nodes.push(newNode);
        nodeMap.set(node.id, newNode); // Store in map for reuse
    }

    // Create edge from parent to child
    if (parentId && !edges.some(edge => edge.source === parentId && edge.target === node.id)) {
        edges.push({
            id: `${parentId}-${node.id}`,
            source: parentId,
            target: node.id,
            markerEnd: {
                type: MarkerType.ArrowClosed, // Add arrow at the end
            },
        });
    }

    // Recursively traverse children
    if (node.left) {
        traverse(
            node.left,
            adjustedX - spacingX / (level + 1), // Shift left based on level
            adjustedY + spacingY, // Move down
            node.id
        );
    }
    if (node.right) {
        traverse(
            node.right,
            adjustedX + spacingX / (level + 1), // Shift right based on level
            adjustedY + spacingY, // Move down
            node.id
        );
    }
}


  traverse(ast, xOffset, 0); // Start from center
  return { nodes, edges };
}

function Flow({ astJson }) {
  const nodeTypes = useMemo(() => ({
    customNode: CustomNode, // Register custom node type
  }), []);

  const { nodes: initialNodes, edges: initialEdges } = useMemo(
    () => (astJson ? calculatePositions(astJson) : { nodes: [], edges: [] }),
    [astJson]
  );

  const [nodes, setNodes] = useState(initialNodes);
  const [edges, setEdges] = useState(initialEdges);

  useEffect(() => {
    if (astJson) {
      const { nodes: newNodes, edges: newEdges } = calculatePositions(astJson);
      setNodes(newNodes);
      setEdges(newEdges);
    }
  }, [astJson]);

  

  const onNodesChange = useCallback(
    (changes) => setNodes((nds) => applyNodeChanges(changes, nds)),
    []
  );

  const onEdgesChange = useCallback(
    (changes) => setEdges((eds) => applyEdgeChanges(changes, eds)),
    []
  );

  const onConnect = useCallback(
    (params) => setEdges((eds) => addEdge(params, eds)),
    []
  );

  return (
    <div style={{ height: '100vh' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
        fitView
        fitViewOptions={{ padding: 0.2 }}
      >
        <Background variant="dots" gap={16} size={1} />
        <Controls />
      </ReactFlow>
    </div>
  );
}

export default Flow;
