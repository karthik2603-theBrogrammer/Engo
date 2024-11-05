import React, { useState } from 'react';
import { Handle } from '@xyflow/react'; // Adjust import based on your setup
import { FaEdit, FaSave, FaTimes } from 'react-icons/fa'; // Using react-icons for icons

import { getArgumentValuesFromJson } from '../../utils';

function CustomNode({ data }) {
    const { node, onNodeChange } = data; // Destructure node data and change handler
    const [isEditing, setIsEditing] = useState(false);
    const [editData, setEditData] = useState({ ...node });

    // Toggle edit mode
    const handleEditClick = () => setIsEditing(true);

    // Handle input changes
    const handleInputChange = (field, value) => {
        setEditData((prev) => ({ ...prev, [field]: value }));
    };

    // Save changes and exit edit mode
    const handleSave = () => {
        setIsEditing(false);
        onNodeChange(editData);
    };

    // Cancel editing and revert changes
    const handleCancel = () => {
        setIsEditing(false);
        setEditData({ ...node });
    };

    return (
        <div className="relative">
            {/* Node Container */}
            <div className="bg-white border border-gray-200 rounded-lg p-4 shadow-lg min-w-48 w-fit">
                {isEditing ? (
                    <div className="flex flex-col gap-2">
                        {/* Editable Fields */}
                        <input
                            type="text"
                            className="border border-gray-300 rounded px-2 py-1"
                            placeholder="Node Type"
                            value={editData.node_type}
                            onChange={(e) => handleInputChange('node_type', e.target.value)}
                            required
                        />
                        {editData.operator !== undefined && (
                            <input
                                type="text"
                                className="border border-gray-300 rounded px-2 py-1"
                                placeholder="Operator"
                                value={editData.operator}
                                onChange={(e) => handleInputChange('operator', e.target.value)}
                                required
                            />
                        )}
                        {editData.value !== undefined && (
                            <input
                                type="text"
                                className="border border-gray-300 rounded px-2 py-1"
                                placeholder="Value"
                                value={editData.value}
                                onChange={(e) => handleInputChange('value', e.target.value)}
                                required
                            />
                        )}
                        {/* Save and Cancel Buttons */}
                        <div className="flex justify-end gap-2">
                            <button
                                onClick={handleSave}
                                className="flex items-center bg-green-500 text-white px-2 py-1 rounded hover:bg-green-600"
                            >
                                <FaSave className="mr-1" /> Save
                            </button>
                            <button
                                onClick={handleCancel}
                                className="flex items-center bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
                            >
                                <FaTimes className="mr-1" /> Cancel
                            </button>
                        </div>
                    </div>
                ) : (
                    <div className="flex flex-col items-center justify-center w-full gap-2">
                        {(node.node_type === "operator" || node.node_type === 'constant' || node.node_type === 'variable') && (
                            <p className="text-lg">{node.value}</p>
                        )}
                        {node.node_type === "condition" && (
                            <p className="text-lg">{node.operator}</p>
                        )}
                        {node.node_type === "function" && (
                            <div className='flex items-center justify-center'>
                                <p className="text-lg text-center text-wrap">{node.value}{getArgumentValuesFromJson(node?.args)}</p>
                            </div>
                        )}
                        <p className="text-md font-semibold">{"("}{node.node_type}{")"}</p>
                    </div>
                )}
            </div>

            {/* Handles for connecting edges (Parent to Child) */}
            <Handle
                type="target" // Represents incoming connection to this node (child)
                position="top"
                style={{ background: '#063895', width: 10 }}
                id="target-handle"
            />
            <Handle
                type="source" // Represents outgoing connection from this node (parent)
                position="bottom"
                style={{ background: '#063895', width: 10 }}
                id="source-handle"
            />
        </div>
    );
}

export default CustomNode;
