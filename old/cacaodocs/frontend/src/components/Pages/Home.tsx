import React from 'react';
import {
  Typography,
  Layout,
  Row,
  Col,
  Card,
  Statistic,
  Space,
  Button,
  theme
} from 'antd';
import {
  AppstoreOutlined,
  BlockOutlined,
  FunctionOutlined,
  FileTextOutlined,
  ArrowRightOutlined
} from '@ant-design/icons';
import { Link } from 'react-router-dom';
import type { AppData } from '../../global';
import { getStats } from '../../global';

const { Title, Text } = Typography;
const { Content } = Layout;
const { useToken } = theme;

interface HomeProps {
  data: AppData;
}

const Home: React.FC<HomeProps> = ({ data }) => {
  const { token } = useToken();
  const stats = getStats(data);

  const cards = [
    {
      title: 'Modules',
      count: stats.moduleCount,
      suffix: 'Modules',
      icon: <AppstoreOutlined style={{ fontSize: '40px', color: data.config.theme.home_page_card_text_color }} />,
      link: '/modules',
      linkText: 'Browse Modules',
      show: stats.moduleCount > 0,
    },
    {
      title: 'Classes',
      count: stats.classCount,
      suffix: 'Classes',
      icon: <BlockOutlined style={{ fontSize: '40px', color: data.config.theme.home_page_card_text_color }} />,
      link: '/classes',
      linkText: 'View Classes',
      show: stats.classCount > 0,
    },
    {
      title: 'Functions',
      count: stats.functionCount,
      suffix: 'Functions',
      icon: <FunctionOutlined style={{ fontSize: '40px', color: data.config.theme.home_page_card_text_color }} />,
      link: '/functions',
      linkText: 'Explore Functions',
      show: stats.functionCount > 0,
    },
    {
      title: 'Guides',
      count: stats.pageCount,
      suffix: 'Pages',
      icon: <FileTextOutlined style={{ fontSize: '40px', color: data.config.theme.home_page_card_text_color }} />,
      link: '/pages',
      linkText: 'Read Guides',
      show: stats.pageCount > 0,
    },
  ];

  const visibleCards = cards.filter(c => c.show);

  return (
    <Layout style={{
      minHeight: '100vh',
      background: data.config.theme.bg_color
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
              {data.config.version && (
                <Text style={{
                  color: data.config.theme.home_page_welcome_text_color,
                  fontSize: '0.9rem',
                  display: 'block',
                  marginTop: '8px',
                  opacity: 0.8
                }}>
                  Version {data.config.version}
                </Text>
              )}
            </Card>
          </Col>

          {/* Stats Cards */}
          {visibleCards.map(card => (
            <Col xs={24} md={Math.floor(24 / Math.min(visibleCards.length, 4))} key={card.title}>
              <Link to={card.link} style={{ display: 'block' }}>
                <Card
                  hoverable
                  style={{
                    height: '100%',
                    borderRadius: '16px',
                    transition: 'all 0.3s ease',
                    border: '1px solid #f0f0f0',
                    overflow: 'hidden'
                  }}
                  styles={{
                    body: {
                      padding: '32px 24px',
                      background: data.config.theme.home_page_card_bg_color
                    }
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
                        {card.icon}
                      </div>
                      <Title level={3} style={{ margin: '0 0 8px', fontSize: '1.5rem' }}>
                        {card.title}
                      </Title>
                      <Statistic
                        value={card.count}
                        suffix={card.suffix}
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
                      {card.linkText} <ArrowRightOutlined />
                    </Button>
                  </Space>
                </Card>
              </Link>
            </Col>
          ))}

          {/* Quick Stats Summary */}
          {stats.methodCount > 0 && (
            <Col span={24}>
              <Card
                style={{
                  borderRadius: '16px',
                  boxShadow: '0 4px 12px rgba(0, 0, 0, 0.05)',
                }}
              >
                <Row gutter={[32, 16]}>
                  <Col xs={12} md={6}>
                    <Statistic title="Total Modules" value={stats.moduleCount} />
                  </Col>
                  <Col xs={12} md={6}>
                    <Statistic title="Total Classes" value={stats.classCount} />
                  </Col>
                  <Col xs={12} md={6}>
                    <Statistic title="Total Functions" value={stats.functionCount} />
                  </Col>
                  <Col xs={12} md={6}>
                    <Statistic title="Total Methods" value={stats.methodCount} />
                  </Col>
                </Row>
              </Card>
            </Col>
          )}
        </Row>
      </Content>
    </Layout>
  );
};

export default Home;
