import React from 'react';
import { Typography, Layout, Card, List, Tag, Space } from 'antd';
import { Link } from 'react-router-dom';
import { FolderOutlined, CodeOutlined, FunctionOutlined } from '@ant-design/icons';
import type { AppData, ModuleDoc } from '../../global';

const { Title, Text, Paragraph } = Typography;
const { Content } = Layout;

interface ModulesProps {
  data: AppData;
}

const Modules: React.FC<ModulesProps> = ({ data }) => {
  const { modules } = data;

  // Group modules by top-level package
  const groupedModules = modules.reduce((acc, module) => {
    const parts = module.full_path.split('.');
    const topLevel = parts[0] || module.name;
    if (!acc[topLevel]) {
      acc[topLevel] = [];
    }
    acc[topLevel].push(module);
    return acc;
  }, {} as Record<string, ModuleDoc[]>);

  return (
    <Layout style={{ minHeight: '100vh', background: data.config.theme.bg_color }}>
      <Content style={{ padding: '32px' }}>
        <Title level={2}>
          <FolderOutlined style={{ marginRight: '12px' }} />
          Modules
        </Title>
        <Paragraph type="secondary" style={{ marginBottom: '24px' }}>
          Browse all {modules.length} modules in this project.
        </Paragraph>

        {Object.entries(groupedModules).map(([packageName, packageModules]) => (
          <Card
            key={packageName}
            title={<Text strong style={{ fontSize: '1.1rem' }}>{packageName}</Text>}
            style={{ marginBottom: '16px', borderRadius: '12px' }}
          >
            <List
              itemLayout="horizontal"
              dataSource={packageModules}
              renderItem={(module) => (
                <List.Item>
                  <List.Item.Meta
                    avatar={<FolderOutlined style={{ fontSize: '24px', color: data.config.theme.primary_color }} />}
                    title={
                      <Link to={`/modules/${encodeURIComponent(module.full_path)}`}>
                        <Text strong>{module.full_path}</Text>
                      </Link>
                    }
                    description={
                      <Space direction="vertical" size={4}>
                        {module.docstring && (
                          <Text type="secondary">
                            {module.docstring.split('\n')[0].substring(0, 150)}
                            {module.docstring.length > 150 ? '...' : ''}
                          </Text>
                        )}
                        <Space size={8}>
                          {module.classes.length > 0 && (
                            <Tag icon={<CodeOutlined />} color="blue">
                              {module.classes.length} class{module.classes.length !== 1 ? 'es' : ''}
                            </Tag>
                          )}
                          {module.functions.length > 0 && (
                            <Tag icon={<FunctionOutlined />} color="green">
                              {module.functions.length} function{module.functions.length !== 1 ? 's' : ''}
                            </Tag>
                          )}
                        </Space>
                      </Space>
                    }
                  />
                </List.Item>
              )}
            />
          </Card>
        ))}

        {modules.length === 0 && (
          <Card style={{ textAlign: 'center', padding: '48px' }}>
            <FolderOutlined style={{ fontSize: '48px', color: '#ccc', marginBottom: '16px' }} />
            <Title level={4} type="secondary">No modules found</Title>
            <Text type="secondary">
              No Python modules were found in the scanned directory.
            </Text>
          </Card>
        )}
      </Content>
    </Layout>
  );
};

export default Modules;
