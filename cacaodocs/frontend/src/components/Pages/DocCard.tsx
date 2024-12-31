import React from 'react';
import { Card, Space, Typography, Tag, Tabs, Button, message } from 'antd';
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter';
import { atomOneDark } from 'react-syntax-highlighter/dist/esm/styles/hljs';
import python from 'react-syntax-highlighter/dist/esm/languages/hljs/python'; // Added import

const { Title, Text } = Typography;
const { TabPane } = Tabs;

SyntaxHighlighter.registerLanguage('python', python); // Added registration

interface Returns {
  description: string;
  full_type: string;
  is_list: boolean;
  is_type_ref: boolean;
  type_name: string;
}

interface DocItem {
  args?: Record<string, any>;
  description?: string;
  function_name: string;
  method?: string;
  returns?: Returns;
  status?: string;
  tag: string;
  type: string;
  version?: string;
  function_source?: string;
  inputs?: string[];
  outputs?: string | null;
}

const DocCard: React.FC<{ doc: DocItem }> = ({ doc }) => {
  const hasArgs = doc.args && Object.keys(doc.args).length > 0;
  const hasReturns = doc.returns && Object.keys(doc.returns).length > 0;
  const hasCode = doc.function_source && doc.function_source.trim().length > 0;

  const defaultTab = hasArgs ? "input" : hasReturns ? "output" : hasCode ? "code" : "";

  const handleCopyCode = () => {
    navigator.clipboard.writeText(doc.function_source || '')
      .then(() => {
        message.success('Code copied to clipboard!');
      })
      .catch(() => {
        message.error('Failed to copy code.');
      });
  };

  return (
    <Card
      hoverable
      title={
        <Space direction="vertical" style={{ width: '100%' }}>
          <Space align="center">
            <Title level={4} style={{ margin: 0 }}>
              {doc.function_name}()
            </Title>
            <Tag color={doc.status === 'Production' ? 'green' : 'orange'}>
              {doc.status}
            </Tag>
            <Tag color="blue">{doc.tag}</Tag>
          </Space>
          <Text type="secondary">{doc.description}</Text>
        </Space>
      }
      style={{ marginBottom: 24 }}
      bodyStyle={{ padding: '24px' }}
    >
      <Tabs defaultActiveKey={defaultTab}>
        {hasArgs && (
          <TabPane tab="Input" key="input">
            <div
              style={{
                borderRadius: '8px',
                overflow: 'hidden',
                backgroundColor: '#1E1E1E'
              }}
            >
            </div>

            {Object.entries(doc.args || {}).length > 0 && (
              <div
                style={{
                  marginTop: '16px',
                  display: 'grid',
                  gap: '12px',
                  gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))'
                }}
              >
                {Object.entries(doc.args || {}).map(([key, value]: [string, any]) => (
                  <Card size="small" key={key} style={{ borderRadius: '8px' }}>
                    <Space align="center">
                      <Text strong>{key}</Text>
                      <Tag>{value.type}</Tag>
                    </Space>
                    <Text
                      type="secondary"
                      style={{ display: 'block', marginTop: '4px' }}
                    >
                      {value.description}
                    </Text>
                  </Card>
                ))}
              </div>
            )}
          </TabPane>
        )}

        {hasReturns && (
          <TabPane tab="Output" key="output">
            <Card size="small" title="Returns" style={{ borderRadius: '8px' }}>
              <Space direction="vertical">
                <Tag color="blue">{doc.returns?.type_name}</Tag>
                <Text type="secondary">{doc.returns?.description}</Text>
              </Space>
            </Card>
          </TabPane>
        )}

        {hasCode && (
          <TabPane tab="Code" key="code">
          <SyntaxHighlighter language="python" style={atomOneDark}>
            {doc.function_source || ''}
          </SyntaxHighlighter>
            <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 16 }}>
              <Button type="primary" onClick={handleCopyCode}>
                Copy Code
              </Button>
            </div>
          </TabPane>
        )}
      </Tabs>
    </Card>
  );
};

export default DocCard;