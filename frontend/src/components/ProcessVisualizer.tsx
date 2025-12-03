import React, { useMemo } from 'react';
import ReactFlow, { MiniMap, Controls, Background } from 'reactflow';
import 'reactflow/dist/style.css';

// Define the types for the process model data
interface NodeData {
    label: string;
    size: number;
}

interface ProcessNode {
    id: string;
    data: NodeData;
    position: { x: number; y: number }; // Position is required by React Flow
}

interface ProcessEdge {
    id: string;
    source: string;
    target: string;
    label: string; // To show the weight/frequency
}

interface ProcessModel {
    nodes: Array<{ id: string; label: string; size: number }>;
    edges: Array<{ source: string; target: string; weight: number }>;
}

interface ProcessVisualizerProps {
    model: ProcessModel | null;
}

// A simple layouting function (you might want a more sophisticated one)
const getLayoutedElements = (model: ProcessModel) => {
    const nodes: ProcessNode[] = [];
    const edges: ProcessEdge[] = [];
    let x = 0;
    let y = 0;

    model.nodes.forEach((node, i) => {
        nodes.push({
            id: node.id,
            data: { label: `${node.label} (${node.size})`, size: node.size },
            position: { x, y },
        });
        // Simple positioning logic
        x += 200;
        if (i % 4 === 0 && i > 0) {
            y += 150;
            x = 0;
        }
    });

    model.edges.forEach((edge, i) => {
        edges.push({
            id: `e-${edge.source}-${edge.target}`,
            source: edge.source,
            target: edge.target,
            label: `(${edge.weight})`,
        });
    });

    return { nodes, edges };
};

export const ProcessVisualizer: React.FC<ProcessVisualizerProps> = ({ model }) => {
    const { nodes, edges } = useMemo(() => {
        if (!model) return { nodes: [], edges: [] };
        return getLayoutedElements(model);
    }, [model]);

    if (!model) {
        return <div>Upload a file to see the process model.</div>;
    }

    return (
        <div style={{ height: '70vh', border: '1px solid #ccc' }}>
            <ReactFlow
                nodes={nodes}
                edges={edges}
                fitView
            >
                <Controls />
                <MiniMap />
                <Background />
            </ReactFlow>
        </div>
    );
};
