import React, { useState } from 'react';
import { Typography, Layout, Card, Collapse, Tag, Space, Empty, Tabs, Table } from 'antd';
import { useParams, Link } from 'react-router-dom';
import { BlockOutlined, FunctionOutlined, InfoCircleOutlined } from '@ant-design/icons';
import type { AppData, MethodDoc } from '../../global';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { docco } from 'react-syntax-highlighter/dist/esm/styles/hljs';

const { Title, Text, Paragraph } = Typography;
const { Content } = Layout;
const { Panel } = Collapse;

interface ClassDetailProps {
  data: AppData;
}

const MethodCard: React.FC<{ method: MethodDoc; theme: any }> = ({ method, theme }) => {
  const getMethodPrefix = () => {
    if (method.is_classmethod) return '@classmethod ';
    if (method.is_staticmethod) return '@staticmethod ';
    if (method.is_property) return '@property ';
    if (method.is_async) return 'async ';
    return '';
  };

  return (
    <Card
      id={`method-${method.name}`}
      size="small"
      style={{ marginBottom: '12px', borderRadius: '8px' }}
      title={
        <Space>
          <FunctionOutlined style={{ color: theme.primary_color }} />
          <Text code>
            {getMethodPrefix()}def {method.name}{method.signature}
          </Text>
        </Space>
      }
      extra={
        <Space>
          {method.is_property && <Tag color="cyan">property</Tag>}
          {method.is_classmethod && <Tag color="orange">classmethod</Tag>}
          {method.is_staticmethod && <Tag color="gold">staticmethod</Tag>}
          {method.is_async && <Tag color="blue">async</Tag>}
        </Space>
      }
    >
      {method.docstring.summary && (
        <Paragraph>{method.docstring.summary}</Paragraph>
      )}
      {method.docstring.description && (
        <Paragraph type="secondary">{method.docstring.description}</Paragraph>
      )}

      {method.docstring.args.length > 0 && (
        <>
          <Text strong>Parameters:</Text>
          <ul style={{ marginTop: '8px', paddingLeft: '20px' }}>
            {method.docstring.args.map(arg => (
              <li key={arg.name}>
                <Text code>{arg.name}</Text>
                {arg.type && <Text type="secondary"> ({arg.type})</Text>}
                {arg.description && <Text>: {arg.description}</Text>}
                {arg.default && <Text type="secondary"> (default: {arg.default})</Text>}
              </li>
            ))}
          </ul>
        </>
      )}

      {method.docstring.returns && (
        <>
          <Text strong>Returns:</Text>
          <Paragraph style={{ marginLeft: '16px' }}>
            {method.docstring.returns.type && <Text code>{method.docstring.returns.type}</Text>}
            {method.docstring.returns.description && <Text>: {method.docstring.returns.description}</Text>}
          </Paragraph>
        </>
      )}

      {method.docstring.raises.length > 0 && (
        <>
          <Text strong>Raises:</Text>
          <ul style={{ marginTop: '8px', paddingLeft: '20px' }}>
            {method.docstring.raises.map((r, i) => (
              <li key={i}>
                <Text code>{r.type}</Text>
                {r.description && <Text>: {r.description}</Text>}
              </li>
            ))}
          </ul>
        </>
      )}

      <Collapse ghost size="small">
        <Panel header="View Source" key="source">
          <SyntaxHighlighter language="python" style={docco}>
            {method.source}
          </SyntaxHighlighter>
        </Panel>
      </Collapse>
    </Card>
  );
};

const ClassDetail: React.FC<ClassDetailProps> = ({ data }) => {
  const { id } = useParams<{ id: string }>();
  const classPath = decodeURIComponent(id || '');
  const [activeTab, setActiveTab] = useState('methods');

  const cls = data.classes.find(c => c.full_path === classPath);

  if (!cls) {
    return (
      <Layout style={{ minHeight: '100vh', background: data.config.theme.bg_color }}>
        <Content style={{ padding: '32px' }}>
          <Empty description={`Class "${classPath}" not found`} />
        </Content>
      </Layout>
    );
  }

  // Categorize methods
  const publicMethods = cls.methods.filter(m => !m.name.startsWith('_'));
  const privateMethods = cls.methods.filter(m => m.name.startsWith('_') && !m.name.startsWith('__'));
  const dunderMethods = cls.methods.filter(m => m.name.startsWith('__') && m.name.endsWith('__'));
  const properties = cls.methods.filter(m => m.is_property);

  const attributeColumns = [
    { title: 'Name', dataIndex: 'name', key: 'name', render: (t: string) => <Text code>{t}</Text> },
    { title: 'Type', dataIndex: 'type', key: 'type', render: (t: string) => <Text code>{t}</Text> },
    { title: 'Description', dataIndex: 'description', key: 'description' },
  ];

  return (
    <Layout style={{ minHeight: '100vh', background: data.config.theme.bg_color }}>
      <Content style={{ padding: '32px' }}>
        <Space direction="vertical" style={{ width: '100%' }} size="large">
          {/* Header */}
          <div>
            <Link to="/classes">
              <Text type="secondary">&larr; Back to Classes</Text>
            </Link>
            <Title level={2} style={{ marginTop: '8px' }}>
              <BlockOutlined style={{ marginRight: '12px' }} />
              class {cls.name}
              {cls.bases.length > 0 && (
                <Text type="secondary" style={{ fontSize: '0.7em', marginLeft: '12px' }}>
                  ({cls.bases.join(', ')})
                </Text>
              )}
            </Title>
            <Space>
              <Tag color="blue">{cls.module}</Tag>
              <Text type="secondary">Line {cls.line_number}</Text>
              {cls.decorators.map(d => (
                <Tag key={d} color="purple">@{d}</Tag>
              ))}
            </Space>
          </div>

          {/* Docstring */}
          {(cls.docstring.summary || cls.docstring.description) && (
            <Card style={{ borderRadius: '12px' }}>
              {cls.docstring.summary && (
                <Paragraph style={{ fontSize: '1.1rem' }}>{cls.docstring.summary}</Paragraph>
              )}
              {cls.docstring.description && (
                <Paragraph style={{ whiteSpace: 'pre-wrap' }}>{cls.docstring.description}</Paragraph>
              )}
            </Card>
          )}

          {/* Attributes */}
          {cls.docstring.attributes.length > 0 && (
            <Card
              title={
                <Space>
                  <InfoCircleOutlined />
                  <Text strong>Attributes</Text>
                </Space>
              }
              style={{ borderRadius: '12px' }}
            >
              <Table
                dataSource={cls.docstring.attributes}
                columns={attributeColumns}
                pagination={false}
                size="small"
                rowKey="name"
              />
            </Card>
          )}

          {/* Methods Tabs */}
          <Card style={{ borderRadius: '12px' }}>
            <Tabs
              activeKey={activeTab}
              onChange={setActiveTab}
              items={[
                {
                  key: 'methods',
                  label: `Public Methods (${publicMethods.length})`,
                  children: publicMethods.length > 0 ? (
                    publicMethods.map(method => (
                      <MethodCard key={method.name} method={method} theme={data.config.theme} />
                    ))
                  ) : (
                    <Empty description="No public methods" />
                  ),
                },
                {
                  key: 'properties',
                  label: `Properties (${properties.length})`,
                  children: properties.length > 0 ? (
                    properties.map(method => (
                      <MethodCard key={method.name} method={method} theme={data.config.theme} />
                    ))
                  ) : (
                    <Empty description="No properties" />
                  ),
                },
                {
                  key: 'private',
                  label: `Private (${privateMethods.length})`,
                  children: privateMethods.length > 0 ? (
                    privateMethods.map(method => (
                      <MethodCard key={method.name} method={method} theme={data.config.theme} />
                    ))
                  ) : (
                    <Empty description="No private methods" />
                  ),
                },
                {
                  key: 'dunder',
                  label: `Special (${dunderMethods.length})`,
                  children: dunderMethods.length > 0 ? (
                    dunderMethods.map(method => (
                      <MethodCard key={method.name} method={method} theme={data.config.theme} />
                    ))
                  ) : (
                    <Empty description="No special methods" />
                  ),
                },
              ]}
            />
          </Card>

          {/* Full Source */}
          <Card
            title="Source Code"
            style={{ borderRadius: '12px' }}
          >
            <SyntaxHighlighter language="python" style={docco}>
              {cls.source}
            </SyntaxHighlighter>
          </Card>
        </Space>
      </Content>
    </Layout>
  );
};

export default ClassDetail;
