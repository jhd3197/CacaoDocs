// DocCard.tsx
import React from 'react';
import {
  Card,
  Tag,
  Space,
  Typography,
  Tabs,
  Tooltip,
  Button,
  message,
} from 'antd';
import { CopyOutlined } from '@ant-design/icons';
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter';
import { atomOneDark } from 'react-syntax-highlighter/dist/esm/styles/hljs';
import python from 'react-syntax-highlighter/dist/esm/languages/hljs/python'; 
import styled from 'styled-components';

import { DocItem, TypeDefinition } from '../../global';

SyntaxHighlighter.registerLanguage('python', python);

const { Title, Paragraph, Text } = Typography;
const { TabPane } = Tabs;

interface ReturnsObject {
  description: string;
  full_type: string;
  is_list: boolean;
  is_type_ref: boolean;
  type_name: string;
}

interface DocCardProps {
  doc: DocItem;
  types: TypeDefinition[]; 
}


// ------------------ Styled Components ------------------ //
const StyledCard = styled(Card)`
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
`;

const HeaderSection = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  
  h4 {
    margin: 0;
    flex-shrink: 0;
  }
  
  .copy-button {
    margin-right: auto;  // This will push the status tags to the right
  }
`;

const TagsContainer = styled.div`
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 8px;
`;

const DescriptionSection = styled.div`
  margin-bottom: 16px;
`;

const SyntaxContainer = styled.div`
  max-height: 300px;
  overflow: auto;
  border-radius: 8px;
`;

const TypeDefinitionCard = styled.div`
  background: rgb(245 240 235);
  border-radius: 8px;
  padding: 16px;
  border-left: 4px solid #8b5d3b;
  color: #8b5d3b;
`;

const TypeDetectedTag = styled(Tag)`
  background: rgb(58 47 42 / 8%);
  border: 1px solid #3a2f2a;
  color: #3a2f2a; // Light brown text
  margin-bottom: 12px;
  padding: 4px 8px;
  border-radius: 4px;
`;
// -------------------------------------------------------- //

/**
 * List of built-in types to differentiate from custom types.
 */
const builtInTypes = ['str', 'int', 'dict', 'list', 'float', 'bool', 'object', 'array'];

/**
 * Utility function to extract base type name from composite types.
 * Handles "List[Type]", "Type[]", "Type?".
 */
const extractBaseType = (typeStr: string | undefined): string => {
  if (!typeStr) return '';

  // Handle List[Type]
  const listMatch = typeStr.match(/List\[(\w+)\]/);
  if (listMatch) return listMatch[1];

  // Handle Type[]
  const arrayMatch = typeStr.match(/(\w+)\[\]/);
  if (arrayMatch) return arrayMatch[1];

  // Handle optional types like Type?
  const optionalMatch = typeStr.match(/^(\w+)\?$/);
  if (optionalMatch) return optionalMatch[1];

  // Default to the original type string
  return typeStr;
};

/**
 * Detects if the returns field is a string with @type{TypeName} annotation.
 * Returns an object with isType and typeName.
 */
const detectTypeAnnotation = (
  returnsField: string | ReturnsObject | undefined
): { isType: boolean; typeName: string | null } => {
  if (typeof returnsField === 'string') {
    const typeMatch = returnsField.match(/@type{([^}]+)}/);
    return {
      isType: !!typeMatch,
      typeName: typeMatch ? typeMatch[1] : null,
    };
  }
  return { isType: false, typeName: null };
};

/**
 * SubTypeTooltip - a tooltip component that displays the definition of a nested type.
 */
const SubTypeTooltip: React.FC<{ definition: TypeDefinition; allTypes: TypeDefinition[] }> = ({
  definition,
  allTypes,
}) => {
  return (
    <div style={{ padding: '8px', maxWidth: '300px', backgroundColor: '#f0efee' }}>
      <Text strong style={{ color: '#3a2f2a', display: 'block', marginBottom: 4 }}>
        {definition.function_name} (Tag: {definition.tag})
      </Text>
      <Text style={{ color: '#3a2f2a', fontSize: '12px' }}>{definition.description}</Text>

      <div style={{ marginTop: 8 }}>
        {Object.entries(definition.args)
          .sort(([a], [b]) => a.localeCompare(b))
          .map(([argKey, argValue]) => {
            const baseType = extractBaseType(argValue.type);
            const nestedType = allTypes.find(t => t.function_name === baseType);
            return (
              <Paragraph key={argKey} style={{ marginBottom: 4, color: '#3a2f2a', fontSize: '12px' }}>
                <Tag color="#9d6243">{argKey}</Tag>
                :{' '}
                {nestedType ? (
                  // If there's a nested type, show it as a hoverable link with tooltip
                  <Tooltip
                    placement="right"
                    title={<SubTypeTooltip definition={nestedType} allTypes={allTypes} />}
                    overlayStyle={{ backgroundColor: '#f5f0eb' }} // Set tooltip background color
                    color='#f5f0eb'

                  >
                    <Text
                      style={{
                        color: '#3a2f2a',
                        textDecoration: 'underline',
                        cursor: 'pointer',
                      }}
                    >
                      {argValue.type}
                    </Text>
                  </Tooltip>
                ) : (
                  // Else just render the type name
                  <Text style={{ color: '#3a2f2a' }}>{argValue.type}</Text>
                )}{' '}
                —{' '}
                <Text type="secondary" style={{ color: '#3a2f2a' }}>
                  {argValue.description}
                </Text>
              </Paragraph>
            );
          })}
      </div>
    </div>
  );
};

/**
 * MiniTypePreview - displays a preview of a custom type's fields, including nested tooltips.
 */
const MiniTypePreview: React.FC<{ definition: TypeDefinition; allTypes: TypeDefinition[] }> = ({
  definition,
  allTypes,
}) => {
  return (
    <div style={{ background: '#f8f7f6', marginTop: '16px', padding: '16px', borderRadius: '8px' }}>
      <Text strong style={{ color: '#3a2f2a', display: 'block', marginBottom: 8 }}>
        {definition.function_name} (Tag: {definition.tag})
      </Text>
      <Text style={{ color: '#3a2f2a', fontSize: '14px' }}>{definition.description}</Text>

      <div style={{ marginTop: 12 }}>
        {Object.entries(definition.args)
          .sort(([a], [b]) => a.localeCompare(b))
          .map(([argKey, argValue]) => {
            const baseType = extractBaseType(argValue.type);
            const nestedType = allTypes.find(t => t.function_name === baseType);
            return (
              <div key={argKey} style={{ marginBottom: 8 }}>

              <Tag color="#9d6243">{argKey}</Tag>
                
                :{' '}
                {nestedType ? (
                  <Tooltip
                    title={<SubTypeTooltip definition={nestedType} allTypes={allTypes} />}
                    overlayStyle={{ backgroundColor: '#f5f0eb' }}
                    color='#f5f0eb'

                  >
                    <Text
                      style={{
                        textDecoration: 'underline',
                        cursor: 'pointer',
                        color: '#3a2f2a',
                      }}
                    >
                      {argValue.type}
                    </Text>
                  </Tooltip>
                ) : (
                  <Text style={{ color: '#3a2f2a' }}>{argValue.type}</Text>
                )}{' '}
                —{' '}
                <Text type="secondary" style={{ color: '#3a2f2a' }}>
                  {argValue.description}
                </Text>
              </div>
            );
          })}
      </div>
    </div>
  );
};

/**
 * DocCard Component
 */
const DocCard: React.FC<DocCardProps> = ({ doc, types }) => {
  const hasArgs = doc.args && Object.keys(doc.args).length > 0;
  const hasReturns = doc.returns !== undefined && doc.returns !== null;
  const hasCode = doc.function_source && doc.function_source.trim().length > 0;

  // Determine the default active tab
  const defaultTab = hasArgs
    ? "input"
    : hasReturns
      ? "output"
      : hasCode
        ? "code"
        : "";

  const handleCopyCode = () => {
    navigator.clipboard.writeText(doc.function_source || '')
      .then(() => {
        message.success('Code copied to clipboard!');
      })
      .catch(() => {
        message.error('Failed to copy code.');
      });
  };

  const handleCopyFunctionName = () => {
    navigator.clipboard.writeText(doc.function_name)
      .then(() => {
        message.success('Function name copied to clipboard!');
      })
      .catch(() => {
        message.error('Failed to copy function name.');
      });
  };

  /**
   * Render the Returns tab content.
   * Handles both string and object formats for `returns`.
   */
  const renderReturns = () => {
    if (!doc.returns) return null;

    let type_name = '';
    let description = '';
    let is_list = false;
    let is_type_ref = false;

    if (typeof doc.returns === 'string') {
      // Parse the string to extract type_name using @type{TypeName}
      const { isType, typeName } = detectTypeAnnotation(doc.returns);
      if (isType && typeName) {
        type_name = typeName;
        description = ''; // Description might not be available in string format
        is_list = false;
        is_type_ref = true; // Assuming type reference if @type is used
      } else {
        // If no type annotation found, treat the whole string as type_name
        type_name = doc.returns;
        description = '';
        is_list = false;
        is_type_ref = false;
      }
    } else if (typeof doc.returns === 'object') {
      type_name = doc.returns.type_name;
      description = doc.returns.description;
      is_list = doc.returns.is_list;
      is_type_ref = doc.returns.is_type_ref;
    }

    // Debugging: Log the extracted type information
    console.log(`renderReturns: type_name=${type_name}, is_type_ref=${is_type_ref}, is_list=${is_list}`);

    if (!type_name) return null;

    // Extract base type (handles List[Type], Type[], etc.)
    const baseType = extractBaseType(type_name);
    const foundType = baseType ? types.find(t => t.function_name === baseType) : undefined;

    // Debugging: Log whether the type was found
    console.log(`renderReturns: foundType for type_name=${type_name}:`, foundType);

    // Check if the type is a built-in type
    const isBuiltIn = builtInTypes.includes(baseType);

    if (isBuiltIn) {
      // Render a neutral tag without tooltip
      return (
        <div style={{ marginTop: 5 }}>
          <Tag style={{ cursor: 'default' }}>
            {type_name}
          </Tag>
          <Text type="secondary" style={{ display: 'block', marginTop: 4 }}>
            {description}
          </Text>
        </div>
      );
    }

    // Single Output with Custom Type
    if (!is_list && is_type_ref && foundType) {
      return (
        <div style={{ marginTop: 5 }}>
          <Text type="secondary" style={{ display: 'block', marginTop: 4 }}>
            {description}
          </Text>
          {/* Show MiniTypePreview */}
          <MiniTypePreview definition={foundType} allTypes={types} />
        </div>
      );
    }

    // If it's a type reference but not found, render a neutral tag without color
    if (!is_list && is_type_ref && !foundType) {
      return (
        <div style={{ marginTop: 5 }}>
          <Tag style={{ cursor: 'default' }}>
            {type_name}
          </Tag>
          <Text type="secondary" style={{ display: 'block', marginTop: 4 }}>
            {description}
          </Text>
        </div>
      );
    }

    // Multiple Outputs or non-custom type
    return (
      <Card size="small" title="Returns" style={{ borderRadius: '8px', marginTop: 5 }}>
        <Space direction="vertical">
          <Tag color="blue">{type_name}</Tag>
          <Text type="secondary">{description}</Text>
        </Space>
      </Card>
    );
  };

  /**
   * Render the Input tab content.
   * Handles both single and multiple inputs, with tooltips for custom types.
   */
  const renderInputTab = () => {
    if (!doc.args) return null;
    const numInputs = Object.keys(doc.args).length;

    // Single Input
    if (numInputs === 1) {
      const [inputName, inputValue] = Object.entries(doc.args)[0];
      const baseType = extractBaseType(inputValue.type);
      const foundType = baseType ? types.find(t => t.function_name === baseType) : undefined;

      // Debugging: Log whether the type was found
      console.log(`renderInputTab: Single Input - inputName=${inputName}, type=${inputValue.type}, foundType=`, foundType);

      // Check if the type is a built-in type
      const isBuiltIn = builtInTypes.includes(baseType);

      if (isBuiltIn) {
        // Render a neutral tag without tooltip
        return (
          <div style={{ marginTop: 5 }}>
            <Tag style={{ cursor: 'default' }}>
              {inputValue.type}
            </Tag>
            <Text type="secondary" style={{ display: 'block', marginTop: 4 }}>
              {inputValue.description}
            </Text>
          </div>
        );
      }

      if (foundType) {
        return (
          <div style={{ marginTop: 5 }}>
            <Text strong style={{ fontSize: '16px', marginBottom: 8, display: 'block' }}>
              Input: {inputName}
            </Text>
            <Tooltip
              title={<SubTypeTooltip definition={foundType} allTypes={types} />}
              overlayStyle={{ backgroundColor: '#f0efee' }}
            >
              <Tag color="blue" style={{ cursor: 'pointer', textDecoration: 'underline' }}>
                {inputValue.type}
              </Tag>
            </Tooltip>
            <Text type="secondary" style={{ display: 'block', marginTop: 4 }}>
              {inputValue.description}
            </Text>

            {/* Show MiniTypePreview */}
            <MiniTypePreview definition={foundType} allTypes={types} />
          </div>
        );
      }

      // If not a built-in type and not found in types, render a neutral tag without color
      return (
        <div style={{ marginTop: 5 }}>
          <Text strong style={{ fontSize: '16px', marginBottom: 8, display: 'block' }}>
            Input: {inputName}
          </Text>
          <Tag style={{ cursor: 'default' }}>
            {inputValue.type}
          </Tag>
          <Text type="secondary" style={{ display: 'block', marginTop: 4 }}>
            {inputValue.description}
          </Text>
        </div>
      );
    }

    // Multiple Inputs
    return (
      <div
        style={{
          marginTop: '16px',
          display: 'grid',
          gap: '12px',
          gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
        }}
      >
        {Object.entries(doc.args || {}).map(([key, value]: [string, any]) => {
          const baseType = extractBaseType(value.type);
          const foundType = baseType ? types.find(t => t.function_name === baseType) : undefined;

          // Debugging: Log for each input
          console.log(`renderInputTab: Multiple Input - key=${key}, type=${value.type}, foundType=`, foundType);

          // Check if the type is a built-in type
          const isBuiltIn = builtInTypes.includes(baseType);

          if (isBuiltIn) {
            // Render a neutral tag without tooltip
            return (
              <Card size="small" key={key} style={{ borderRadius: '8px' }}>
                <Space align="center">
                  <Text strong>{key}</Text>
                  <Tag style={{ cursor: 'default' }}>
                    {value.type}
                  </Tag>
                </Space>
                <Text
                  type="secondary"
                  style={{ display: 'block', marginTop: '4px', color: '#3a2f2a' }}
                >
                  {value.description}
                </Text>
              </Card>
            );
          }

          return (
            <Card size="small" key={key} style={{ borderRadius: '8px' }}>
              <Space align="center">
                <Text strong>{key}</Text>
                {foundType ? (
                  <Tooltip
                    title={<SubTypeTooltip definition={foundType} allTypes={types} />}
                    overlayStyle={{ backgroundColor: '#f0efee' }}
                  >
                    <Tag color="blue" style={{ cursor: 'pointer', textDecoration: 'underline' }}>
                      {value.type}
                    </Tag>
                  </Tooltip>
                ) : (
                  <Tag style={{ cursor: 'default' }}>
                    {value.type}
                  </Tag>
                )}
              </Space>
              <Text
                type="secondary"
                style={{ display: 'block', marginTop: '4px', color: '#3a2f2a' }}
              >
                {value.description}
              </Text>
            </Card>
          );
        })}
      </div>
    );
  };

  /**
   * Render the Code tab content.
   */
  const renderCodeTab = () => {
    if (!doc.function_source) return null;

    return (
      <>
        <SyntaxHighlighter language="python" style={atomOneDark}>
          {doc.function_source || ''}
        </SyntaxHighlighter>
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 5 }}>
          <Button type="primary" onClick={handleCopyCode}>
            Copy Code
          </Button>
        </div>
      </>
    );
  };

  return (
    <StyledCard
      hoverable
      title={
        <HeaderSection>
          <Title level={4}>
            {doc.function_name}()
          </Title>
          <Button
            className="copy-button"
            type="text"
            icon={<CopyOutlined />}
            onClick={handleCopyFunctionName}
            aria-label="Copy Function Name"
          />
          <Space>
            <Tag
              color={doc.status === 'Production' ? 'green' : 'orange'}
              style={{ minWidth: 60, textAlign: 'center' }}
            >
              {doc.status}
            </Tag>
            <Tag color="blue">{doc.tag}</Tag>
          </Space>
        </HeaderSection>
      }
      bodyStyle={{ padding: '24px' }}
      style={{ marginBottom: 24 }}
    >

      {doc.description && (
        <DescriptionSection style={{ marginBottom: 24 }}>
          <Paragraph>
            {doc.description}
          </Paragraph>
        </DescriptionSection>
      )}

      <Tabs defaultActiveKey={defaultTab}>
        {/* Input Tab */}
        {hasArgs && (
          <TabPane tab="Input" key="input">
            {renderInputTab()}
          </TabPane>
        )}

        {/* Output Tab */}
        {hasReturns && (
          <TabPane tab="Output" key="output">
            {renderReturns()}
          </TabPane>
        )}

        {/* Code Tab */}
        {hasCode && (
          <TabPane tab="Code" key="code">
            {renderCodeTab()}
          </TabPane>
        )}
      </Tabs>
    </StyledCard>
  );
};
// -------------------------------------------------------- //

export default DocCard;
