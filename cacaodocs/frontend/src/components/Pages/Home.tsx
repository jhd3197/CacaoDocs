import React from 'react';
import {
  Typography,
  Layout,
  Row,
  Col,
  Card,
  Statistic,
  List,
  Space,
  Button,
  theme
} from 'antd';
import {
  FileTextOutlined,
  ApiOutlined,
  CodeOutlined,
  ClockCircleOutlined,
  ArrowRightOutlined
} from '@ant-design/icons';
import { Link } from 'react-router-dom';
import type { AppData } from '../../global';

const { Title, Text } = Typography;
const { Content } = Layout;
const { useToken } = theme;


interface HomeProps {
  data: AppData;
}


const DashboardHome: React.FC<HomeProps> = ({ data }) => {
  const { token } = useToken();

  const getRelativeTime = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now.getTime() - date.getTime());
    const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
    
    if (diffDays === 0) return 'Today';
    if (diffDays === 1) return 'Yesterday';
    if (diffDays < 7) return `${diffDays} days ago`;
    if (diffDays < 30) return `${Math.floor(diffDays / 7)} weeks ago`;
    if (diffDays < 365) return `${Math.floor(diffDays / 30)} months ago`;
    return `${Math.floor(diffDays / 365)} years ago`;
  };

  const getActivityTitle = (item: any) => {
    switch (item.itemType) {
      case 'api':
        return `API Endpoint Updated ${item.method || ''} ${item.endpoint || item.function_name}`;
      case 'type':
        return `Type Definition Modified ${item.function_name}${item.args ? ` with ${Object.keys(item.args).length} parameters` : ''}`;
      case 'doc':
        return `Documentation Updated ${item.function_name}()`;
      default:
        return item.function_name || 'Untitled';
    }
  };

  const recentActivity = [
    ...data.api.map(item => ({ ...item, itemType: 'api' })),
    ...data.docs.map(item => ({ ...item, itemType: 'doc' })),
    ...data.types.map(item => ({ ...item, itemType: 'type' }))
  ]
  .filter(item => item.last_updated)
  .sort((a, b) => {
    return new Date(b.last_updated).getTime() - new Date(a.last_updated).getTime();
  })
  .slice(0, 3);

  const getIconForType = (type: string) => {
    switch (type) {
      case 'api':
        return <ApiOutlined style={{ color: token.colorPrimary }} />;
      case 'type':
        return <CodeOutlined style={{ color: token.colorPrimary }} />;
      case 'doc':
        return <FileTextOutlined style={{ color: token.colorPrimary }} />;
      default:
        return <ApiOutlined style={{ color: token.colorPrimary }} />;
    }
  };

  return (
    <Layout style={{ 
      minHeight: '100vh',
      background: `${data.config.theme.bg_color}`
    }}>
      <Content style={{ padding: '32px' }}>
        <Row gutter={[32, 32]}>
          {/* Welcome Section */}
          <Col span={24}>
            <Card
              style={{
                borderRadius: '16px',
                background: `linear-gradient(145deg, ${data.config.theme.home_page_welcome_bg_1} 0%, ${data.config.theme.home_page_welcome_bg_2} 100%)`,
                border: 'none',
                boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)'
              }}
            >
              <Title level={4} style={{ 
                margin: 0,
                color: data.config.theme.home_page_welcome_text_color,
                fontSize: '2rem',
                fontWeight: 600
              }}>
               {data.config.title}
              </Title>
              <Text style={{ 
                color: data.config.theme.home_page_welcome_text_color,
                fontSize: '1.1rem',
                display: 'block',
                marginTop: '8px'
              }}>
               {data.config.description}
              </Text>
            </Card>
          </Col>

          {/* Action Cards */}
          {data.api.length > 0 && (
            <Col xs={24} md={8}>
              <Link to="/api" style={{ display: 'block' }}>
                <Card
                  hoverable
                  style={{
                    height: '100%',
                    borderRadius: '16px',
                    transition: 'all 0.3s ease',
                    border: '1px solid #f0f0f0',
                    overflow: 'hidden'
                  }}
                  bodyStyle={{
                    padding: '32px 24px',
                    background: data.config.theme.home_page_card_bg_color
                  }}
                >
                  <Space direction="vertical" size="large" style={{ width: '100%' }}>
                    <div style={{ textAlign: 'center' }}>
                      <div style={{
                        background: `${token.colorPrimary}15`,
                        borderRadius: '50%',
                        width: '80px',
                        height: '80px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        margin: '0 auto 20px'
                      }}>
                        <ApiOutlined style={{ fontSize: '40px', color: data.config.theme.home_page_card_text_color}} />
                      </div>
                      <Title level={3} style={{ margin: '0 0 8px', fontSize: '1.5rem' }}>API Documentation</Title>
                      <Statistic
                        value={data.api.length}
                        suffix="Endpoints"
                        valueStyle={{ color: data.config.theme.home_page_card_text_color, fontSize: '2rem' }}
                      />
                    </div>
                    <Button 
                      type="text"
                      style={{
                        color: data.config.theme.home_page_card_text_color,
                        padding: 0,
                        height: 'auto',
                        fontSize: '1rem'
                      }}
                    >
                      Explore APIs <ArrowRightOutlined />
                    </Button>
                  </Space>
                </Card>
              </Link>
            </Col>
          )}

          {data.types.length > 0 && (
            <Col xs={24} md={8}>
              <Link to="/types" style={{ display: 'block' }}>
                <Card
                  hoverable
                  style={{
                    height: '100%',
                    borderRadius: '16px',
                    transition: 'all 0.3s ease',
                    border: '1px solid #f0f0f0',
                    overflow: 'hidden'
                  }}
                  bodyStyle={{
                    padding: '32px 24px',
                    background: data.config.theme.home_page_card_bg_color
                  }}
                >
                  <Space direction="vertical" size="large" style={{ width: '100%' }}>
                    <div style={{ textAlign: 'center' }}>
                      <div style={{
                        background: `${token.colorPrimary}15`,
                        borderRadius: '50%',
                        width: '80px',
                        height: '80px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        margin: '0 auto 20px'
                      }}>
                        <CodeOutlined style={{ fontSize: '40px', color: data.config.theme.home_page_card_text_color }} />
                      </div>
                      <Title level={3} style={{ margin: '0 0 8px', fontSize: '1.5rem' }}>Type Definitions</Title>
                      <Statistic
                        value={data.types.length}
                        suffix="Types"
                        valueStyle={{ color: data.config.theme.home_page_card_text_color, fontSize: '2rem' }}
                      />
                    </div>
                    <Button 
                      type="text"
                      style={{
                        color: data.config.theme.home_page_card_text_color,
                        padding: 0,
                        height: 'auto',
                        fontSize: '1rem'
                      }}
                    >
                      View Types <ArrowRightOutlined />
                    </Button>
                  </Space>
                </Card>
              </Link>
            </Col>
          )}

          {data.docs.length > 0 && (
            <Col xs={24} md={8}>
              <Link to="/docs" style={{ display: 'block' }}>
                <Card
                  hoverable
                  style={{
                    height: '100%',
                    borderRadius: '16px',
                    transition: 'all 0.3s ease',
                    border: '1px solid #f0f0f0',
                    overflow: 'hidden'
                  }}
                  bodyStyle={{
                    padding: '32px 24px',
                    background: data.config.theme.home_page_card_bg_color
                  }}
                >
                  <Space direction="vertical" size="large" style={{ width: '100%' }}>
                    <div style={{ textAlign: 'center' }}>
                      <div style={{
                        background: `${token.colorPrimary}15`,
                        borderRadius: '50%',
                        width: '80px',
                        height: '80px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        margin: '0 auto 20px'
                      }}>
                        <FileTextOutlined style={{ fontSize: '40px', color: data.config.theme.home_page_card_text_color }} />
                      </div>
                      <Title level={3} style={{ margin: '0 0 8px', fontSize: '1.5rem' }}>Documentation</Title>
                      <Statistic
                        value={data.docs.length}
                        suffix="Pages"
                        valueStyle={{ color: data.config.theme.home_page_card_text_color, fontSize: '2rem' }}
                      />
                    </div>
                    <Button 
                      type="text"
                      style={{
                        color: data.config.theme.home_page_card_text_color,
                        padding: 0,
                        height: 'auto',
                        fontSize: '1rem'
                      }}
                    >
                      Browse Docs <ArrowRightOutlined />
                    </Button>
                  </Space>
                </Card>
              </Link>
            </Col>
          )}

          {/* Recent Activity Section */}
          {recentActivity.length > 0 && (
            <Col span={24}>
              <Card
                style={{
                  borderRadius: '16px',
                  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.05)',
                  color: data.config.theme.home_page_card_text_color
                }}
                bodyStyle={{
                  padding: '0px 24px'
                }}
                title={
                  <Space size="middle">
                    <ClockCircleOutlined style={{ fontSize: '20px' }} />
                    <span style={{ fontSize: '1.1rem', fontWeight: 600 }}>Recent Activity</span>
                  </Space>
                }
              >
                <List
                  itemLayout="horizontal"
                  dataSource={recentActivity}
                  renderItem={item => (
                    <List.Item style={{ padding: '16px 0' }}>
                      <List.Item.Meta
                        avatar={
                          <div style={{
                            background: `${token.colorBgContainer}`,
                            borderRadius: '8px',
                            padding: '8px',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center'
                          }}>
                            {getIconForType(item.itemType)}
                          </div>
                        }
                        title={
                          <Text strong>
                            {getActivityTitle(item)}
                          </Text>
                        }
                        description={
                          <Space direction="vertical" size={0}>
                            <Text type="secondary">
                              {getRelativeTime(item.last_updated)}
                            </Text>
                          </Space>
                        }
                      />
                    </List.Item>
                  )}
                />
              </Card>
            </Col>
          )}
        </Row>
      </Content>
    </Layout>
  );
};

export default DashboardHome;