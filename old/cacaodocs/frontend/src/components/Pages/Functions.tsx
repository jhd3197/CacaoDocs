import React, { useState } from 'react';
import { Typography, Layout, Card, Collapse, Tag, Space, Input } from 'antd';
import { FunctionOutlined, SearchOutlined } from '@ant-design/icons';
import type { AppData, FunctionDoc } from '../../global';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { docco } from 'react-syntax-highlighter/dist/esm/styles/hljs';

const { Title, Text, Paragraph } = Typography;
const { Content } = Layout;
const { Panel } = Collapse;

interface FunctionsProps {
  data: AppData;
}

const FunctionCard: React.FC<{ func: FunctionDoc; theme: any }> = ({ func, theme }) => (
  <Card
    id={`function-${func.name}`}
    style={{ marginBottom: '16px', borderRadius: '12px' }}
    title={
      <Space>
        <FunctionOutlined style={{ color: theme.primary_color, fontSize: '20px' }} />
        <Text code style={{ fontSize: '1rem' }}>
          {func.is_async ? 'async ' : ''}def {func.name}{func.signature}
        </Text>
      </Space>
    }
    extra={
      <Space>
        <Tag color="blue">{func.module}</Tag>
        {func.is_async && <Tag color="purple">async</Tag>}
        {func.decorators.map(d => (
          <Tag key={d} color="orange">@{d}</Tag>
        ))}
      </Space>
    }
  >
    {func.docstring.summary && (
      <Paragraph style={{ fontSize: '1rem' }}>{func.docstring.summary}</Paragraph>
    )}
    {func.docstring.description && (
      <Paragraph type="secondary" style={{ whiteSpace: 'pre-wrap' }}>
        {func.docstring.description}
      </Paragraph>
    )}

    {func.docstring.args.length > 0 && (
      <div style={{ marginBottom: '16px' }}>
        <Text strong>Parameters:</Text>
        <ul style={{ marginTop: '8px', paddingLeft: '20px' }}>
          {func.docstring.args.map(arg => (
            <li key={arg.name} style={{ marginBottom: '4px' }}>
              <Text code>{arg.name}</Text>
              {arg.type && <Text type="secondary"> ({arg.type})</Text>}
              {arg.description && <Text>: {arg.description}</Text>}
              {arg.default && <Text type="secondary"> (default: {arg.default})</Text>}
            </li>
          ))}
        </ul>
      </div>
    )}

    {func.docstring.returns && (
      <div style={{ marginBottom: '16px' }}>
        <Text strong>Returns:</Text>
        <Paragraph style={{ marginLeft: '16px', marginTop: '4px' }}>
          {func.docstring.returns.type && <Text code>{func.docstring.returns.type}</Text>}
          {func.docstring.returns.description && <Text>: {func.docstring.returns.description}</Text>}
        </Paragraph>
      </div>
    )}

    {func.docstring.raises.length > 0 && (
      <div style={{ marginBottom: '16px' }}>
        <Text strong>Raises:</Text>
        <ul style={{ marginTop: '8px', paddingLeft: '20px' }}>
          {func.docstring.raises.map((r, i) => (
            <li key={i}>
              <Text code>{r.type}</Text>
              {r.description && <Text>: {r.description}</Text>}
            </li>
          ))}
        </ul>
      </div>
    )}

    {func.docstring.examples.length > 0 && (
      <div style={{ marginBottom: '16px' }}>
        <Text strong>Examples:</Text>
        {func.docstring.examples.map((ex, i) => (
          <SyntaxHighlighter key={i} language="python" style={docco}>
            {ex}
          </SyntaxHighlighter>
        ))}
      </div>
    )}

    <Collapse ghost size="small">
      <Panel header="View Source" key="source">
        <SyntaxHighlighter language="python" style={docco}>
          {func.source}
        </SyntaxHighlighter>
      </Panel>
    </Collapse>
  </Card>
);

const Functions: React.FC<FunctionsProps> = ({ data }) => {
  const [searchText, setSearchText] = useState('');
  const { functions } = data;

  const filteredFunctions = functions.filter(func =>
    func.name.toLowerCase().includes(searchText.toLowerCase()) ||
    func.full_path.toLowerCase().includes(searchText.toLowerCase()) ||
    func.docstring.summary.toLowerCase().includes(searchText.toLowerCase())
  );

  // Group by module
  const groupedFunctions = filteredFunctions.reduce((acc, func) => {
    const module = func.module || 'Unknown';
    if (!acc[module]) {
      acc[module] = [];
    }
    acc[module].push(func);
    return acc;
  }, {} as Record<string, FunctionDoc[]>);

  return (
    <Layout style={{ minHeight: '100vh', background: data.config.theme.bg_color }}>
      <Content style={{ padding: '32px' }}>
        <Title level={2}>
          <FunctionOutlined style={{ marginRight: '12px' }} />
          Functions
        </Title>
        <Paragraph type="secondary" style={{ marginBottom: '16px' }}>
          Browse all {functions.length} functions in this project.
        </Paragraph>

        <Input
          prefix={<SearchOutlined />}
          placeholder="Search functions..."
          value={searchText}
          onChange={e => setSearchText(e.target.value)}
          style={{ marginBottom: '24px', maxWidth: '400px' }}
          allowClear
        />

        {Object.entries(groupedFunctions).map(([moduleName, moduleFunctions]) => (
          <div key={moduleName} style={{ marginBottom: '32px' }}>
            <Title level={4} style={{ marginBottom: '16px' }}>
              <Tag color="blue">{moduleName}</Tag>
              <Text type="secondary" style={{ fontSize: '0.9rem', marginLeft: '8px' }}>
                {moduleFunctions.length} function{moduleFunctions.length !== 1 ? 's' : ''}
              </Text>
            </Title>
            {moduleFunctions.map(func => (
              <FunctionCard key={func.full_path} func={func} theme={data.config.theme} />
            ))}
          </div>
        ))}

        {filteredFunctions.length === 0 && (
          <Card style={{ textAlign: 'center', padding: '48px' }}>
            <FunctionOutlined style={{ fontSize: '48px', color: '#ccc', marginBottom: '16px' }} />
            <Title level={4} type="secondary">
              {searchText ? 'No matching functions' : 'No functions found'}
            </Title>
            <Text type="secondary">
              {searchText
                ? 'Try adjusting your search terms.'
                : 'No standalone functions were found in the scanned directory.'}
            </Text>
          </Card>
        )}
      </Content>
    </Layout>
  );
};

export default Functions;
