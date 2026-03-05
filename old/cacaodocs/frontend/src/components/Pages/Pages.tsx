import React from 'react';
import { Typography, Layout, Card, List } from 'antd';
import { Link } from 'react-router-dom';
import { FileTextOutlined } from '@ant-design/icons';
import type { AppData } from '../../global';

const { Title, Text, Paragraph } = Typography;
const { Content } = Layout;

interface PagesProps {
  data: AppData;
}

const Pages: React.FC<PagesProps> = ({ data }) => {
  const { pages } = data;

  // Sort pages by order, then title
  const sortedPages = [...pages].sort((a, b) => {
    if (a.order !== b.order) return a.order - b.order;
    return a.title.localeCompare(b.title);
  });

  return (
    <Layout style={{ minHeight: '100vh', background: data.config.theme.bg_color }}>
      <Content style={{ padding: '32px' }}>
        <Title level={2}>
          <FileTextOutlined style={{ marginRight: '12px' }} />
          Guides
        </Title>
        <Paragraph type="secondary" style={{ marginBottom: '24px' }}>
          Documentation and guides for this project.
        </Paragraph>

        <List
          grid={{ gutter: 16, xs: 1, sm: 1, md: 2, lg: 2, xl: 3, xxl: 3 }}
          dataSource={sortedPages}
          renderItem={(page) => (
            <List.Item>
              <Link to={`/pages/${encodeURIComponent(page.slug)}`}>
                <Card
                  hoverable
                  style={{ borderRadius: '12px' }}
                >
                  <Card.Meta
                    avatar={
                      <FileTextOutlined
                        style={{
                          fontSize: '32px',
                          color: data.config.theme.primary_color
                        }}
                      />
                    }
                    title={<Text strong>{page.title}</Text>}
                    description={
                      <Text type="secondary" style={{ fontSize: '0.9rem' }}>
                        {page.file_path.split(/[/\\]/).pop()}
                      </Text>
                    }
                  />
                </Card>
              </Link>
            </List.Item>
          )}
        />

        {pages.length === 0 && (
          <Card style={{ textAlign: 'center', padding: '48px' }}>
            <FileTextOutlined style={{ fontSize: '48px', color: '#ccc', marginBottom: '16px' }} />
            <Title level={4} type="secondary">No guides found</Title>
            <Text type="secondary">
              No Markdown files were found in the scanned directory.
            </Text>
          </Card>
        )}
      </Content>
    </Layout>
  );
};

export default Pages;
