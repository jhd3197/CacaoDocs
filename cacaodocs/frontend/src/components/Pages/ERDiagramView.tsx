import React, { useCallback, useEffect } from 'react';
import ReactFlow, {
  ReactFlowProvider,
  useNodesState,
  useEdgesState,
  addEdge,
  Background,
  Controls,
  Handle,
  Node,
  Edge,
  Connection,
  ConnectionMode,
  Position,
  NodeTypes
} from 'reactflow';
import 'reactflow/dist/style.css';
import dagre from 'dagre';

export interface FieldDefinition {
  bg_color: string;
  color: string;
  description: string;
  emoji: string;
  type: string;
  note?: string;
}

export interface TypeDefinition {
  function_name: string;
  description?: string;
  args: Record<string, FieldDefinition>;
}

// Data shape for our ER Node
interface ERNodeData {
  label: string;
  description?: string;
  fields: Record<string, FieldDefinition>;
}

// --------------------------------------------------
// ERNode: The main node component for a type
// --------------------------------------------------
const ERNode = ({ data }: { data: ERNodeData }) => {
  return (
    <div
      style={{
        position: 'relative',
        background: '#fff',
        border: '1px solid #f0f0f0',
        borderRadius: 6,
        padding: 12,
        cursor: 'move',
        boxShadow: '0 2px 5px rgba(0,0,0,0.06)',
        minWidth: 180
      }}
    >
      {/* Node-level target handle */}
      <Handle
        type="target"
        position={Position.Left}
        id="tgt-node"
        style={{
          position: 'absolute',
          left: 0,
          top: 10,
          width: 10,
          height: 10,
          background: '#795548', // brown dot
        }}
      />

      {/* Title / function name */}
      <div style={{ fontWeight: 600, fontSize: 14, marginBottom: 4 }}>
        {data.label}
      </div>

      {/* Optional description under the title */}
      {data.description && (
        <div style={{ fontSize: 12, color: '#888', marginBottom: 8 }}>
          {data.description}
        </div>
      )}

      {/* Fields list */}
      {Object.entries(data.fields).map(([fieldName, fieldDef]) => (
        <div key={fieldName} style={{ position: 'relative', marginBottom: 8 }}>
          {/* A hidden field-level target handle if needed */}
          <Handle
            type="target"
            position={Position.Left}
            id={`tgt-${fieldName}`}
            style={{
              position: 'absolute',
              left: 0,
              top: '50%',
              transform: 'translateY(-50%)',
              visibility: 'hidden',
            }}
          />

          {/* Field label + description */}
          <div style={{ fontSize: 12, color: '#555', marginBottom: 3 }}>
            <strong>{fieldName}</strong>
            {fieldDef.description ? `: ${fieldDef.description}` : null}
          </div>

          {/* Tag with emoji + type */}
          <div
            style={{
              display: 'inline-block',
              background: fieldDef.bg_color || '#f0f2f5',
              color: fieldDef.color || '#000',
              padding: '3px 6px',
              borderRadius: 4,
              fontSize: 12,
            }}
          >
            {fieldDef.emoji} &nbsp;{fieldDef.type}
          </div>

          {/* Right-side handle to initiate a connection FROM this field */}
          <Handle
            type="source"
            position={Position.Right}
            id={`src-${fieldName}`}
            style={{
              position: 'absolute',
              right: 0,
              top: '50%',
              transform: 'translateY(-50%)',
            }}
          />
        </div>
      ))}
    </div>
  );
};

// --------------------------------------------------
// NoteNode: If a field has a "note"
// --------------------------------------------------
interface NoteNodeData {
  noteText: string;
}

const NoteNode = ({ data }: { data: NoteNodeData }) => {
  return (
    <div
      style={{
        position: 'relative',
        background: '#FEF3C7',
        border: '1px solid #FCD34D',
        borderRadius: 4,
        padding: 10,
        cursor: 'move',
        boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
      }}
    >
      <em>Note:</em> {data.noteText}
    </div>
  );
};

const nodeTypes: NodeTypes = {
  erNode: ERNode,
  noteNode: NoteNode,
};

interface ERDiagramViewProps {
  typesData: TypeDefinition[];
}

const ERDiagramView: React.FC<ERDiagramViewProps> = ({ typesData }) => {
  // Build a quick lookup by type name
  const typeMap: Record<string, TypeDefinition> = {};
  typesData.forEach((t) => {
    typeMap[t.function_name] = t;
  });

  // ------------------------------------------
  // Step 1: Build the initial Node array
  // ------------------------------------------
  const initialNodes: Node[] = typesData.map((type, index) => ({
    id: type.function_name,
    type: 'erNode',
    // place them in a rough grid; we'll auto-layout after mount
    position: { x: 300 * (index % 3), y: 200 * Math.floor(index / 3) },
    data: {
      label: type.function_name,
      description: type.description || '',
      fields: type.args,
    },
    draggable: true,
    selectable: true,
  }));

  // We'll store edges and noteNodes below
  const initialEdges: Edge[] = [];
  const noteNodes: Node[] = [];

  // Helper for unique edge IDs
  function edgeId(...parts: (string | number)[]) {
    return parts.join('-');
  }

  // ------------------------------------------
  // Step 2: Generate Edges (and NoteNodes)
  // ------------------------------------------
  typesData.forEach((sourceType) => {
    const sourceTypeName = sourceType.function_name;

    Object.entries(sourceType.args).forEach(([fieldName, fieldDef]) => {
      // Check if the field is something like List[Address]
      let actualFieldType = fieldDef.type;
      const bracketMatch = actualFieldType.match(/^List\[\s*(.*?)\s*\]$/);
      if (bracketMatch) {
        actualFieldType = bracketMatch[1];
      }

      // If that type is recognized, connect from this field to the node-level handle of the target
      if (typeMap[actualFieldType]) {
        initialEdges.push({
          id: edgeId('direct', sourceTypeName, fieldName, actualFieldType),
          source: sourceTypeName,
          sourceHandle: `src-${fieldName}`,
          target: actualFieldType,
          targetHandle: 'tgt-node',
          label: `${fieldName} → ${actualFieldType}`,
          type: 'smoothstep',
        });
      }

      // If there's a note, create a note node + edge
      if (fieldDef.note) {
        const noteNodeId = edgeId('noteNode', sourceTypeName, fieldName);

        noteNodes.push({
          id: noteNodeId,
          type: 'noteNode',
          position: { x: 0, y: 0 },
          data: { noteText: fieldDef.note },
          draggable: true,
          selectable: true,
        });

        initialEdges.push({
          id: edgeId('noteEdge', sourceTypeName, fieldName),
          source: sourceTypeName,
          sourceHandle: `src-${fieldName}`,
          target: noteNodeId,
          label: 'Note',
          type: 'smoothstep',
        });
      }
    });
  });

  // ------------------------------------------
  // Step 3: Place the note nodes near the source node (optional)
  // ------------------------------------------
  noteNodes.forEach((noteNode) => {
    const parts = noteNode.id.split('-');
    const sourceTypeName = parts[1];
    const sourceNode = initialNodes.find((n) => n.id === sourceTypeName);
    if (sourceNode) {
      noteNode.position.x = sourceNode.position.x + 220;
      noteNode.position.y = sourceNode.position.y + 60;
    }
  });

  // Combine the main type nodes + note nodes
  const allInitialNodes = [...initialNodes, ...noteNodes];
  const [nodes, setNodes, onNodesChange] = useNodesState(allInitialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  // If you want to allow user-created edges:
  const onConnect = useCallback(
    (params: Connection) =>
      setEdges((eds) => addEdge({ ...params, type: 'smoothstep' }, eds)),
    [setEdges]
  );

  // ---------------------------------------
  // Step 4: Use dagre to auto-layout nodes
  // ---------------------------------------
  const nodeWidth = 180;
  const nodeHeight = 70;

  const onAutoLayout = useCallback(() => {
    const g = new dagre.graphlib.Graph();
    g.setDefaultEdgeLabel(() => ({}));
    // rankdir: 'LR' = left-to-right, 'TB' = top-to-bottom, etc.
    // Increase spacing by raising ranksep and nodesep
    g.setGraph({ rankdir: 'LR', ranksep: 400, nodesep: 600 });

    nodes.forEach((node) => {
      g.setNode(node.id, { width: nodeWidth, height: nodeHeight });
    });
    edges.forEach((edge) => {
      g.setEdge(edge.source, edge.target);
    });

    dagre.layout(g);

    const newNodes = nodes.map((node) => {
      const nodeData = g.node(node.id);
      return {
        ...node,
        position: {
          x: nodeData.x - nodeWidth / 2,
          y: nodeData.y - nodeHeight / 2,
        },
      };
    });

    setNodes(newNodes);
  }, [nodes, edges, setNodes]);

  useEffect(() => {
    const timer = setTimeout(() => {
      onAutoLayout();
    }, 200);
  
    return () => clearTimeout(timer); // Cleanup in case the component unmounts before timeout finishes
  }, []); // Empty dependency array ensures it runs only on mount

  return (
    <ReactFlowProvider>
      <div style={{ width: '100%', height: '90vh', position: 'relative' }}>
        {/* "Auto Layout" button if user wants to rearrange at any point */}
        <button
          style={{
            position: 'absolute',
            zIndex: 10,
            top: 10,
            left: 10,
            padding: '6px 12px',
            cursor: 'pointer',
            border: '1px solid #ddd',
            background: '#fff',
            borderRadius: 4,
            boxShadow: '0 1px 3px rgba(0,0,0,0.2)',
          }}
          onClick={onAutoLayout}
        >
          Auto Layout
        </button>

        <ReactFlow
          nodeTypes={nodeTypes}
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onConnect={onConnect}
          connectionMode={ConnectionMode.Loose}
          defaultViewport={{ x: 0, y: 0, zoom: 1 }}
          elementsSelectable
          nodesDraggable
          fitView
        >
          <Background />
          <Controls />
        </ReactFlow>
      </div>
    </ReactFlowProvider>
  );
};

export default ERDiagramView;
