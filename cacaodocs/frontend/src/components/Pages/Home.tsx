import React from 'react';
import { Typography, Layout, Row, Col, Card, Button, Space, theme } from 'antd';
import { Link } from 'react-router-dom';
import { 
  RocketOutlined, 
  FileSearchOutlined, 
  ApiOutlined,
  CodeOutlined,
  RightOutlined
} from '@ant-design/icons';

const { Title, Paragraph } = Typography;
const { Content } = Layout;
const { useToken } = theme;

const Home: React.FC = () => {
  const { token } = useToken();

  // Custom colors for the gradient
  const greenColor = '#2E7D32'; // Forest green
  const brownColor = '#795548'; // Rich brown

  return (
    <Layout>
      <Content>
        {/* Hero Section */}
        <Row 
          justify="center" 
          align="middle" 
          style={{ 
            minHeight: '80vh',
            background: `linear-gradient(145deg, ${token.colorBgContainer} 0%, ${token.colorBgLayout} 100%)`,
            padding: '0 24px'
          }}
        >
          <Col xs={24} md={20} lg={16} style={{ textAlign: 'center' }}>
            <Space direction="vertical" size="large" style={{ width: '100%' }}>
              <Title style={{ 
                fontSize: '4rem', 
                marginBottom: 0,
                background: `linear-gradient(90deg, ${greenColor} 0%, ${brownColor} 100%)`,
                WebkitBackgroundClip: 'text',
                WebkitTextFillColor: 'transparent'
              }}>
                Welcome to CacaoDocs
              </Title>
              <Paragraph style={{ 
                fontSize: '1.5rem',
                color: token.colorTextSecondary,
                margin: '24px 0 40px'
              }}>
                Your comprehensive documentation platform for better development
              </Paragraph>
              <Space size="large" wrap style={{ justifyContent: 'center' }}>
                <Link to="/docs">
                  <Button 
                    type="primary" 
                    size="large" 
                    icon={<RocketOutlined />}
                    style={{ 
                      height: '48px',
                      padding: '0 32px',
                      fontSize: '16px'
                    }}
                  >
                    Get Started
                  </Button>
                </Link>
                <Link to="/docs">
                  <Button 
                    size="large" 
                    icon={<FileSearchOutlined />}
                    style={{ 
                      height: '48px',
                      padding: '0 32px',
                      fontSize: '16px'
                    }}
                  >
                    Browse Docs
                  </Button>
                </Link>
              </Space>
            </Space>
          </Col>
        </Row>

        {/* Features Section */}
        <Row 
          style={{ 
            padding: '64px 24px',
            background: token.colorBgContainer
          }}
        >
          <Col span={24} style={{ maxWidth: 1200, margin: '0 auto' }}>
            <Row gutter={[32, 32]}>
              {/* API Card */}
              <Col xs={24} md={8}>
                <Link to="/api" style={{ display: 'block', height: '100%' }}>
                  <Card
                    hoverable
                    style={{ height: '100%' }}
                    bodyStyle={{ height: '100%' }}
                  >
                    <Space direction="vertical" size="middle" style={{ width: '100%' }}>
                      <ApiOutlined style={{ fontSize: '32px', color: greenColor }} />
                      <Title level={3}>Explore API</Title>
                      <Paragraph style={{ fontSize: '16px', marginBottom: '24px' }}>
                        Dive into our endpoints and discover powerful integrations.
                      </Paragraph>
                      <Button 
                        type="link" 
                        style={{ padding: 0 }}
                      >
                        Go to API <RightOutlined />
                      </Button>
                    </Space>
                  </Card>
                </Link>
              </Col>

              {/* Types Card */}
              <Col xs={24} md={8}>
                <Link to="/types" style={{ display: 'block', height: '100%' }}>
                  <Card
                    hoverable
                    style={{ height: '100%' }}
                    bodyStyle={{ height: '100%' }}
                  >
                    <Space direction="vertical" size="middle" style={{ width: '100%' }}>
                      <CodeOutlined style={{ fontSize: '32px', color: greenColor }} />
                      <Title level={3}>Review Types</Title>
                      <Paragraph style={{ fontSize: '16px', marginBottom: '24px' }}>
                        Check out type definitions for stable, consistent development.
                      </Paragraph>
                      <Button 
                        type="link" 
                        style={{ padding: 0 }}
                      >
                        View Types <RightOutlined />
                      </Button>
                    </Space>
                  </Card>
                </Link>
              </Col>

              {/* Docs Card */}
              <Col xs={24} md={8}>
                <Link to="/docs" style={{ display: 'block', height: '100%' }}>
                  <Card
                    hoverable
                    style={{ height: '100%' }}
                    bodyStyle={{ height: '100%' }}
                  >
                    <Space direction="vertical" size="middle" style={{ width: '100%' }}>
                      <FileSearchOutlined style={{ fontSize: '32px', color: greenColor }} />
                      <Title level={3}>Read Docs</Title>
                      <Paragraph style={{ fontSize: '16px', marginBottom: '24px' }}>
                        Find guides, best practices, and in-depth examples.
                      </Paragraph>
                      <Button 
                        type="link" 
                        style={{ padding: 0 }}
                      >
                        Open Docs <RightOutlined />
                      </Button>
                    </Space>
                  </Card>
                </Link>
              </Col>
            </Row>
          </Col>
        </Row>
      </Content>
    </Layout>
  );
};

export default Home;