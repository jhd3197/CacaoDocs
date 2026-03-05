import React, { useState } from 'react';
import { Typography, Layout, Card, List, Tag, Space, Input } from 'antd';
import { Link } from 'react-router-dom';
import { BlockOutlined, SearchOutlined, FunctionOutlined } from '@ant-design/icons';
import type { AppData, ClassDoc } from '../../global';

const { Title, Text, Paragraph } = Typography;
const { Content } = Layout;

interface ClassesProps {
  data: AppData;
}

const Classes: React.FC<ClassesProps> = ({ data }) => {
  const [searchText, setSearchText] = useState('');
  const { classes } = data;

  const filteredClasses = classes.filter(cls =>
    cls.name.toLowerCase().includes(searchText.toLowerCase()) ||
    cls.full_path.toLowerCase().includes(searchText.toLowerCase()) ||
    cls.docstring.summary.toLowerCase().includes(searchText.toLowerCase())
  );

  // Group classes by module
  const groupedClasses = filteredClasses.reduce((acc, cls) => {
    const module = cls.module || 'Unknown';
    if (!acc[module]) {
      acc[module] = [];
    }
    acc[module].push(cls);
    return acc;
  }, {} as Record<string, ClassDoc[]>);

  return (
    <Layout style={{ minHeight: '100vh', background: data.config.theme.bg_color }}>
      <Content style={{ padding: '32px' }}>
        <Title level={2}>
          <BlockOutlined style={{ marginRight: '12px' }} />
          Classes
        </Title>
        <Paragraph type="secondary" style={{ marginBottom: '16px' }}>
          Browse all {classes.length} classes in this project.
        </Paragraph>

        <Input
          prefix={<SearchOutlined />}
          placeholder="Search classes..."
          value={searchText}
          onChange={e => setSearchText(e.target.value)}
          style={{ marginBottom: '24px', maxWidth: '400px' }}
          allowClear
        />

        {Object.entries(groupedClasses).map(([moduleName, moduleClasses]) => (
          <Card
            key={moduleName}
            title={
              <Space>
                <Text strong style={{ fontSize: '1.1rem' }}>{moduleName}</Text>
                <Tag>{moduleClasses.length}</Tag>
              </Space>
            }
            style={{ marginBottom: '16px', borderRadius: '12px' }}
          >
            <List
              itemLayout="horizontal"
              dataSource={moduleClasses}
              renderItem={(cls) => (
                <List.Item>
                  <List.Item.Meta
                    avatar={<BlockOutlined style={{ fontSize: '24px', color: data.config.theme.primary_color }} />}
                    title={
                      <Link to={`/classes/${encodeURIComponent(cls.full_path)}`}>
                        <Space>
                          <Text strong>class {cls.name}</Text>
                          {cls.bases.length > 0 && (
                            <Text type="secondary">({cls.bases.join(', ')})</Text>
                          )}
                        </Space>
                      </Link>
                    }
                    description={
                      <Space direction="vertical" size={4}>
                        {cls.docstring.summary && (
                          <Text type="secondary">
                            {cls.docstring.summary.substring(0, 150)}
                            {cls.docstring.summary.length > 150 ? '...' : ''}
                          </Text>
                        )}
                        <Space size={8}>
                          {cls.methods.length > 0 && (
                            <Tag icon={<FunctionOutlined />} color="blue">
                              {cls.methods.length} method{cls.methods.length !== 1 ? 's' : ''}
                            </Tag>
                          )}
                          {cls.decorators.map(d => (
                            <Tag key={d} color="purple">@{d}</Tag>
                          ))}
                        </Space>
                      </Space>
                    }
                  />
                </List.Item>
              )}
            />
          </Card>
        ))}

        {filteredClasses.length === 0 && (
          <Card style={{ textAlign: 'center', padding: '48px' }}>
            <BlockOutlined style={{ fontSize: '48px', color: '#ccc', marginBottom: '16px' }} />
            <Title level={4} type="secondary">
              {searchText ? 'No matching classes' : 'No classes found'}
            </Title>
            <Text type="secondary">
              {searchText
                ? 'Try adjusting your search terms.'
                : 'No Python classes were found in the scanned directory.'}
            </Text>
          </Card>
        )}
      </Content>
    </Layout>
  );
};

export default Classes;
