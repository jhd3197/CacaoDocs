import React, { useState } from 'react';
import {
  Card,
  Tag,
  Space,
  Typography,
  Tabs,
  Badge,
  Tooltip,
  Button,
  message,
  Table,
} from 'antd';
import {
  CodeOutlined,
  InfoCircleOutlined,
  CopyOutlined,
  CheckOutlined,
} from '@ant-design/icons';
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter';
import { atomOneDark } from 'react-syntax-highlighter/dist/esm/styles/hljs';
import styled from 'styled-components';
import { ApiEndpoint, TypeDefinition, AppData } from '../../global';

const { Title, Paragraph, Text } = Typography;
const { TabPane } = Tabs;

const StyledCard = styled(Card)`
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
`;

const HeaderSection = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const EndpointContainer = styled.div`
  display: flex;
  align-items: center;
  gap: 8px;
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

const ResponsesTabs = styled(Tabs)`
  .ant-tabs-nav {
    margin-bottom: 16px;
  }
`;

const SyntaxContainer = styled.div`
  max-height: 300px;
  overflow: auto;
  border-radius: 8px;
`;

// Show a custom background for the TypeDefinition block
const TypeDefinitionCard = styled.div<{ theme: AppData['config']['theme']}>`
  background: ${props => props.theme.type_bg_color_2 || 'rgb(245 240 235)'};
  border-radius: 8px;
  padding: 16px;
  border-left: 4px solid ${props => props.theme.type_bg_color_1 || '#8b5d3b'};
  color: ${props => props.theme.type_text_color || '#8b5d3b'};
`;

const TypeDetectedTag = styled(Tag)`
  background: ${props => props.theme?.type_bg_color_2 || 'rgb(245 240 235)'};
  border: 1px solid ${props => props.theme?.type_text_color || '#3a2f2a'};
  color: ${props => props.theme?.type_text_color || '#3a2f2a'}; // Light brown text
  margin-bottom: 12px;
  padding: 4px 8px;
  border-radius: 4px;
`;

const methodColors: Record<string, string> = {
  GET: '#52c41a',
  POST: '#1890ff',
  PUT: '#fa8c16',
  DELETE: '#f5222d',
  PATCH: '#722ed1',
};

const statusColors: Record<string, string> = {
  Production: 'green',
  Staging: 'orange',
  Development: 'blue',
};

const cleanDescription = (description?: string) => {
  if (!description) return '';
  return description.replace(/^["'](.*)["']$/, '$1');
};

const parseAndPrettifyJSON = (jsonString: string | object) => {
  try {
    const parsed =
      typeof jsonString === 'string' ? JSON.parse(jsonString) : jsonString;
    return JSON.stringify(parsed, null, 2);
  } catch {
    return null;
  }
};

// Utility function to extract base type name from composite types
const extractBaseType = (typeStr: string): string => {
  // Handle List[Type] or Array<Type>
  const listMatch = typeStr.match(/List\[(\w+)\]/);
  if (listMatch) return listMatch[1];

  const arrayMatch = typeStr.match(/(\w+)\[\]/);
  if (arrayMatch) return arrayMatch[1];

  // Handle optional types like Type?
  const optionalMatch = typeStr.match(/^(\w+)\?$/);
  if (optionalMatch) return optionalMatch[1];

  // Default to the original type string
  return typeStr;
};

// Detect if the example is referencing a Type via @type{SomeTypeName}
const detectTypeAnnotation = (
  example: string | object
): { isType: boolean; typeName: string | null } => {
  if (typeof example !== 'string') return { isType: false, typeName: null };

  const typeMatch = example.match(/@type{([^}]+)}/);
  return {
    isType: !!typeMatch,
    typeName: typeMatch ? typeMatch[1] : null,
  };
};

// ---------------- Mini preview for *SUB-TYPES* when hovered ----------------
const SubTypeTooltip: React.FC<{ definition: TypeDefinition; allTypes: TypeDefinition[]; config: AppData['config']; }> = ({
  definition,
  allTypes,
  config,
}) => {
  return (
    <div style={{ padding: '8px', maxWidth: '300px', backgroundColor: '#f5f0eb' }}>
      <Text strong style={{ color: '#3a2f2a', display: 'block', marginBottom: 4 }}>
        {definition.function_name} (Tag: {definition.tag})
      </Text>
      <Text style={{ color: '#3a2f2a', fontSize: '12px' }}>{definition.description}</Text>

      <div style={{ marginTop: 8 }}>
        {Object.entries(definition.args)
          .sort(([a], [b]) => a.localeCompare(b))
          .map(([argKey, argValue]) => {
            // Extract base type
            const baseType = extractBaseType(argValue.type);
            const nestedType = allTypes.find((t) => t.function_name === baseType);

            return (
              <Paragraph key={argKey} style={{ marginBottom: 4, color:  config?.theme?.type_text_color, fontSize: '12px' }}>
                <Tag style={{ 
                  backgroundColor: config?.theme?.type_bg_color_2 || '#9d6243',
                  color: config?.theme?.type_text_color || '#3a2f2a'
                }}>
                  {argKey}
                </Tag>
                
                :{' '}
                {nestedType ? (
                  // If there's a nested type, show it as a hoverable link with tooltip
                  <Tooltip
                    placement="right"
                    title={<SubTypeTooltip definition={nestedType} allTypes={allTypes} config={config} />}
                    overlayStyle={{ backgroundColor: config?.theme?.type_bg_color_2 }}
                    color = {config?.theme?.type_text_color || '#3a2f2a'}
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
                <span style={{ color: '#000' }}> — </span>
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

// -------------- UPDATED MINI-PREVIEW COMPONENT FOR THE FOUND TYPE --------------
const MiniTypePreview: React.FC<{ definition: TypeDefinition; allTypes: TypeDefinition[]; config: AppData['config']; }> = ({
  definition,
  allTypes,
  config,
}) => {
  return (
    <div style={{ marginTop: '16px' }}>
      <Text strong style={{ color: '#3a2f2a', display: 'block', marginBottom: 8 }}>
        {definition.function_name} (Tag: {definition.tag})
      </Text>
      <Paragraph style={{ marginBottom: 16, color: '#3a2f2a' }}>{definition.description}</Paragraph>

      <Space direction="vertical" style={{ width: '100%' }}>
        {Object.entries(definition.args)
          .sort(([a], [b]) => a.localeCompare(b))
          .map(([argKey, argValue]) => {
            // Extract base type
            const baseType = extractBaseType(argValue.type);
            const nestedType = allTypes.find((t) => t.function_name === baseType);

            return (
              <Paragraph key={argKey} style={{ marginBottom: 8, color: '#e6d5c9' }}>
                <Tag style={{ 
                  backgroundColor: config?.theme?.type_bg_color_2 || '#9d6243',
                  color: config?.theme?.type_text_color || '#3a2f2a'
                }}>
                  {argKey}
                </Tag>
                :{' '}
                {nestedType ? (
                  // If there's a nested type, show it as a hoverable link with tooltip
                  <Tooltip
                    placement="right"
                    title={<SubTypeTooltip definition={nestedType} allTypes={allTypes} config={config} />}
                    overlayStyle={{ backgroundColor: config?.theme?.type_bg_color_2 }}
                    color = {config?.theme?.type_text_color || '#3a2f2a'}
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
                <span style={{ color: '#000' }}> — </span>
                <Text type="secondary" style={{ color: '#3a2f2a' }}>
                  {argValue.description}
                </Text>
              </Paragraph>
            );
          })}
      </Space>
    </div>
  );
};
// --------------------------------------------------------------------------

interface ApiCardProps {
  endpoint: ApiEndpoint;
  types: TypeDefinition[];
  config: AppData['config'];
}

const ApiCard: React.FC<ApiCardProps> = ({ endpoint, types, config }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard
      .writeText(endpoint.endpoint)
      .then(() => {
        setCopied(true);
        message.success('Endpoint copied to clipboard!');
        setTimeout(() => setCopied(false), 2000);
      })
      .catch(() => {
        message.error('Failed to copy endpoint.');
      });
  };

  // -------------- Renders the example or a special Type preview --------------
  const renderExample = (example: string | object) => {
    const typeInfo = detectTypeAnnotation(example);

    if (typeInfo.isType && typeInfo.typeName) {
      // Try to find the matching type by function_name
      const foundType = types.find(
        (t) => t.function_name === typeInfo.typeName
      );

      // If found, show your mini TypeDefinition preview
      if (foundType) {
        return (
          <TypeDefinitionCard theme={config?.theme || {}}>
            <TypeDetectedTag theme={config?.theme}>Type: {typeInfo.typeName}</TypeDetectedTag>
            {/* Optionally remove the annotation from the displayed example below */}
            <SyntaxHighlighter
              language="typescript"
              style={atomOneDark}
              customStyle={{
                background: '#3a2f2a',
                margin: 0,
                padding: 0,
                color: '#e6d5c9',
              }}
            >
              {typeof example === 'string'
                ? example.replace(/@type{[^}]+}/, '').trim()
                : JSON.stringify(example, null, 2)}
            </SyntaxHighlighter>

            {/* Render additional mini preview data about the found type */}
            <MiniTypePreview definition={foundType} allTypes={types} config={config} />
          </TypeDefinitionCard>
        );
      }
      // If not found, just show the code block without any Type preview
      return (
        <TypeDefinitionCard theme={config?.theme || {}}>
          <TypeDetectedTag theme={config?.theme} color="error" icon={<CodeOutlined />}>
            Type "{typeInfo.typeName}" not found!
          </TypeDetectedTag>
          <Paragraph style={{ whiteSpace: 'pre-wrap', color: '#fff' }}>
            {typeof example === 'string'
              ? example.replace(/@type{[^}]+}/, '').trim()
              : JSON.stringify(example, null, 2)}
          </Paragraph>
        </TypeDefinitionCard>
      );
    }

    // If there's no type annotation, just show JSON or raw text
    const parsedJSON = parseAndPrettifyJSON(example);
    return parsedJSON ? (
      <SyntaxContainer>
        <SyntaxHighlighter
          language="json"
          style={atomOneDark}
          customStyle={{
            background: config?.theme?.code_bg_color || '#3a2f2a',
            padding: '16px',
            borderRadius: '8px',
            margin: 0
          }}
        >
          {parsedJSON}
        </SyntaxHighlighter>
      </SyntaxContainer>
    ) : (
      <Paragraph style={{ whiteSpace: 'pre-wrap' }}>
        {typeof example === 'string'
          ? example
          : JSON.stringify(example, null, 2)}
      </Paragraph>
    );
  };
  // ------------------------------------------------------------------

  const tooltipStyle = { 
    backgroundColor: '#f5f0eb',
  };

  return (
    <StyledCard
      hoverable
      title={
        <HeaderSection>
          <EndpointContainer>
            <Title level={5} style={{ margin: 0 }}>
              {endpoint.endpoint}
            </Title>
            <Tooltip title="Copy Endpoint" overlayStyle={tooltipStyle}>
              <Button
                type="text"
                icon={copied ? <CheckOutlined /> : <CopyOutlined />}
                onClick={handleCopy}
                aria-label="Copy Endpoint"
              />
            </Tooltip>
          </EndpointContainer>
          <Tag
            color={methodColors[endpoint.method]}
            style={{ minWidth: 60, textAlign: 'center' }}
          >
            {endpoint.method}
          </Tag>
        </HeaderSection>
      }
      bodyStyle={{ padding: '8px 24px 24px 24px' }}
      style={{ marginBottom: 20 }}
    >
      <TagsContainer>
        {endpoint.status && (
          <Tooltip title="Environment Status" overlayStyle={tooltipStyle}>
            <Badge
              color={statusColors[endpoint.status] || 'default'}
              text={endpoint.status}
            />
          </Tooltip>
        )}
        
        {endpoint.version && (
          <Tooltip title="API Version" overlayStyle={tooltipStyle}>
            <Badge color="blue" text={`${endpoint.version}`} />
          </Tooltip>
        )}
        
        {endpoint.tag && (
          <Tooltip title="API Tag" overlayStyle={tooltipStyle}>
            <Badge color="purple" text={endpoint.tag} />
          </Tooltip>
        )}
      </TagsContainer>

      {endpoint.description && (
        <DescriptionSection style={{ marginBottom: 0 }}>
          <Paragraph style={{ padding: '10px 0px 0px 0px', marginBottom: 0 }}>
            {cleanDescription(endpoint.description)}
          </Paragraph>
        </DescriptionSection>
      )}

      {endpoint.responses && (
        <ResponsesTabs defaultActiveKey={endpoint.args ? 'args' : Object.keys(endpoint.responses)[0]}>
          {endpoint.args && (
            <TabPane
              tab={
                <span>
                  <InfoCircleOutlined /> Variables
                </span>
              }
              key="args"
            >
              {(() => {
                const columns = [
                  {
                    title: 'Name', // Renamed from 'Arg' to 'Name'
                    dataIndex: 'argName',
                    key: 'argName',
                    render: (_: any, record: any) => (
                      <Tag style={{ backgroundColor: record.bg_color, color: record.color }}>
                        {record.emoji} {record.argName}
                      </Tag>
                    ),
                  },
                  // Removed the 'Emoji' column
                  {
                    title: 'Type',
                    dataIndex: 'type',
                    key: 'type',
                  },
                  {
                    title: 'Description',
                    dataIndex: 'description',
                    key: 'description',
                  },
                ];

                const dataSource = Object.entries(endpoint.args).map(([argName, argValue]) => ({
                  key: argName,
                  argName,
                  emoji: argValue.emoji,
                  type: argValue.type,
                  description: argValue.description,
                  bg_color: argValue.bg_color, // Added bg_color for rendering the Tag
                  color: argValue.color,       // Added color for Tag text
                }));

                return (
                  <Table
                    columns={columns}
                    dataSource={dataSource}
                    pagination={false}
                    style={{ marginTop: 5 }}
                  />
                );
              })()}
            </TabPane>
          )}

          {Object.entries(endpoint.responses).map(([code, details]) => (
            <TabPane
              tab={
                <span>
                  <CodeOutlined /> {code}
                </span>
              }
              key={code}
            >
              <Space direction="vertical" style={{ width: '100%' }}>
                {details.description && (
                  <>
                    <Text strong>Description:</Text>
                    <Paragraph>{cleanDescription(details.description)}</Paragraph>
                  </>
                )}
                {details.example && (
                  <>
                    {details.description && <Text strong>Example:</Text>}
                    {renderExample(details.example)}
                  </>
                )}
              </Space>
            </TabPane>
          ))}
        </ResponsesTabs>
      )}
    </StyledCard>
  );
};

export default ApiCard;
