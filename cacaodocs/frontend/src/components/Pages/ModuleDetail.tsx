import React from 'react';
import { Typography, Layout, Card, Collapse, Tag, Space, Divider, Empty } from 'antd';
import { useParams, Link } from 'react-router-dom';
import { FolderOutlined, CodeOutlined, FunctionOutlined } from '@ant-design/icons';
import type { AppData, ClassDoc, FunctionDoc } from '../../global';
import SyntaxHighlighter from 'react-syntax-highlighter';
import { docco } from 'react-syntax-highlighter/dist/esm/styles/hljs';

const { Title, Text, Paragraph } = Typography;
const { Content } = Layout;
const { Panel } = Collapse;

interface ModuleDetailProps {
  data: AppData;
}

const FunctionCard: React.FC<{ func: FunctionDoc; theme: any }> = ({ func, theme }) => (
  <Card
    id={`function-${func.name}`}
    size="small"
    style={{ marginBottom: '12px', borderRadius: '8px' }}
    title={
      <Space>
        <FunctionOutlined style={{ color: theme.primary_color }} />
        <Text code>{func.is_async ? 'async ' : ''}{func.name}{func.signature}</Text>
      </Space>
    }
    extra={
      <Space>
        {func.decorators.map(d => (
          <Tag key={d} color="purple">@{d}</Tag>
        ))}
      </Space>
    }
  >
    {func.docstring.summary && (
      <Paragraph>{func.docstring.summary}</Paragraph>
    )}
    {func.docstring.description && (
      <Paragraph type="secondary">{func.docstring.description}</Paragraph>
    )}
    {func.docstring.args.length > 0 && (
      <>
        <Text strong>Parameters:</Text>
        <ul style={{ marginTop: '8px', paddingLeft: '20px' }}>
          {func.docstring.args.map(arg => (
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
    {func.docstring.returns && (
      <>
        <Text strong>Returns:</Text>
        <Paragraph style={{ marginLeft: '16px' }}>
          {func.docstring.returns.type && <Text code>{func.docstring.returns.type}</Text>}
          {func.docstring.returns.description && <Text>: {func.docstring.returns.description}</Text>}
        </Paragraph>
      </>
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

const ClassCard: React.FC<{ cls: ClassDoc; theme: any }> = ({ cls, theme }) => (
  <Card
    id={`class-${cls.name}`}
    style={{ marginBottom: '16px', borderRadius: '12px' }}
    title={
      <Space>
        <CodeOutlined style={{ color: theme.primary_color, fontSize: '20px' }} />
        <Text strong style={{ fontSize: '1.1rem' }}>class {cls.name}</Text>
        {cls.bases.length > 0 && (
          <Text type="secondary">({cls.bases.join(', ')})</Text>
        )}
      </Space>
    }
    extra={
      <Link to={`/classes/${encodeURIComponent(cls.full_path)}`}>
        <Tag color="blue">View Details</Tag>
      </Link>
    }
  >
    {cls.docstring.summary && (
      <Paragraph>{cls.docstring.summary}</Paragraph>
    )}
    {cls.docstring.description && (
      <Paragraph type="secondary">{cls.docstring.description}</Paragraph>
    )}
    {cls.methods.length > 0 && (
      <>
        <Divider orientation="left" plain>
          Methods ({cls.methods.length})
        </Divider>
        <Space wrap>
          {cls.methods
            .filter(m => !m.name.startsWith('_') || m.name === '__init__')
            .map(method => (
              <Tag key={method.name}>
                {method.is_property ? '@' : ''}{method.name}
                {!method.is_property && '()'}
              </Tag>
            ))}
        </Space>
      </>
    )}
  </Card>
);

const ModuleDetail: React.FC<ModuleDetailProps> = ({ data }) => {
  const { id } = useParams<{ id: string }>();
  const modulePath = decodeURIComponent(id || '');

  const module = data.modules.find(m => m.full_path === modulePath);

  if (!module) {
    return (
      <Layout style={{ minHeight: '100vh', background: data.config.theme.bg_color }}>
        <Content style={{ padding: '32px' }}>
          <Empty description={`Module "${modulePath}" not found`} />
        </Content>
      </Layout>
    );
  }

  return (
    <Layout style={{ minHeight: '100vh', background: data.config.theme.bg_color }}>
      <Content style={{ padding: '32px' }}>
        <Space direction="vertical" style={{ width: '100%' }} size="large">
          {/* Header */}
          <div>
            <Link to="/modules">
              <Text type="secondary">&larr; Back to Modules</Text>
            </Link>
            <Title level={2} style={{ marginTop: '8px' }}>
              <FolderOutlined style={{ marginRight: '12px' }} />
              {module.full_path}
            </Title>
            <Text type="secondary">{module.file_path}</Text>
          </div>

          {/* Module Docstring */}
          {module.docstring && (
            <Card style={{ borderRadius: '12px' }}>
              <Paragraph style={{ whiteSpace: 'pre-wrap', margin: 0 }}>
                {module.docstring}
              </Paragraph>
            </Card>
          )}

          {/* Classes */}
          {module.classes.length > 0 && (
            <div>
              <Title level={4}>
                <CodeOutlined style={{ marginRight: '8px' }} />
                Classes ({module.classes.length})
              </Title>
              {module.classes.map(cls => (
                <ClassCard key={cls.name} cls={cls} theme={data.config.theme} />
              ))}
            </div>
          )}

          {/* Functions */}
          {module.functions.length > 0 && (
            <div>
              <Title level={4}>
                <FunctionOutlined style={{ marginRight: '8px' }} />
                Functions ({module.functions.length})
              </Title>
              {module.functions.map(func => (
                <FunctionCard key={func.name} func={func} theme={data.config.theme} />
              ))}
            </div>
          )}

          {module.classes.length === 0 && module.functions.length === 0 && (
            <Card style={{ textAlign: 'center', padding: '32px' }}>
              <Text type="secondary">This module contains no public classes or functions.</Text>
            </Card>
          )}
        </Space>
      </Content>
    </Layout>
  );
};

export default ModuleDetail;
