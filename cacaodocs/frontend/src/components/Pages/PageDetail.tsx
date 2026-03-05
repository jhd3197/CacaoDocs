import React from 'react';
import { Typography, Layout, Card, Empty } from 'antd';
import { useParams, Link } from 'react-router-dom';
import { FileTextOutlined } from '@ant-design/icons';
import type { AppData } from '../../global';

const { Title, Text } = Typography;
const { Content } = Layout;

interface PageDetailProps {
  data: AppData;
}

const PageDetail: React.FC<PageDetailProps> = ({ data }) => {
  const { slug } = useParams<{ slug: string }>();
  const pageSlug = decodeURIComponent(slug || '');

  const page = data.pages.find(p => p.slug === pageSlug);

  if (!page) {
    return (
      <Layout style={{ minHeight: '100vh', background: data.config.theme.bg_color }}>
        <Content style={{ padding: '32px' }}>
          <Empty description={`Page "${pageSlug}" not found`} />
        </Content>
      </Layout>
    );
  }

  return (
    <Layout style={{ minHeight: '100vh', background: data.config.theme.bg_color }}>
      <Content style={{ padding: '32px', maxWidth: '900px', margin: '0 auto' }}>
        <Link to="/pages">
          <Text type="secondary">&larr; Back to Guides</Text>
        </Link>

        <Title level={2} style={{ marginTop: '16px', marginBottom: '8px' }}>
          <FileTextOutlined style={{ marginRight: '12px' }} />
          {page.title}
        </Title>
        <Text type="secondary" style={{ display: 'block', marginBottom: '24px' }}>
          {page.file_path}
        </Text>

        <Card style={{ borderRadius: '12px' }}>
          <div
            className="markdown-content"
            dangerouslySetInnerHTML={{ __html: page.content }}
            style={{
              lineHeight: 1.8,
              fontSize: '1rem',
            }}
          />
        </Card>

        <style>{`
          .markdown-content h1,
          .markdown-content h2,
          .markdown-content h3,
          .markdown-content h4,
          .markdown-content h5,
          .markdown-content h6 {
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            color: ${data.config.theme.primary_color};
          }

          .markdown-content h1 { font-size: 1.75rem; }
          .markdown-content h2 { font-size: 1.5rem; }
          .markdown-content h3 { font-size: 1.25rem; }

          .markdown-content p {
            margin-bottom: 1em;
          }

          .markdown-content pre {
            background: ${data.config.theme.code_bg_color};
            padding: 16px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 1em 0;
          }

          .markdown-content code {
            background: ${data.config.theme.code_bg_color};
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Fira Code', 'Consolas', monospace;
          }

          .markdown-content pre code {
            background: none;
            padding: 0;
          }

          .markdown-content ul,
          .markdown-content ol {
            padding-left: 2em;
            margin-bottom: 1em;
          }

          .markdown-content li {
            margin-bottom: 0.5em;
          }

          .markdown-content blockquote {
            border-left: 4px solid ${data.config.theme.primary_color};
            padding-left: 1em;
            margin: 1em 0;
            color: #666;
            font-style: italic;
          }

          .markdown-content table {
            width: 100%;
            border-collapse: collapse;
            margin: 1em 0;
          }

          .markdown-content th,
          .markdown-content td {
            border: 1px solid #ddd;
            padding: 8px 12px;
            text-align: left;
          }

          .markdown-content th {
            background: ${data.config.theme.code_bg_color};
          }

          .markdown-content a {
            color: ${data.config.theme.primary_color};
          }

          .markdown-content img {
            max-width: 100%;
            height: auto;
          }
        `}</style>
      </Content>
    </Layout>
  );
};

export default PageDetail;
