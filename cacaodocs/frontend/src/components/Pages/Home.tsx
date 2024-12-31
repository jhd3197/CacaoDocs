import React from 'react';
import { Typography, Layout, Row, Col, Card, Button, Space } from 'antd';
import { BookOutlined, RocketOutlined, TeamOutlined, FileSearchOutlined } from '@ant-design/icons';

const { Title, Paragraph } = Typography;
const { Content } = Layout;

const Home: React.FC = () => {
    return (
        <Layout>
            <Content style={{ padding: '50px 50px' }}>
                {/* Hero Section */}
                <Row justify="center" align="middle" style={{ minHeight: '60vh' }}>
                    <Col xs={24} md={16} style={{ textAlign: 'center' }}>
                        <Title>Welcome to CacaoDocs</Title>
                        <Paragraph style={{ fontSize: '18px' }}>
                            Your comprehensive documentation platform for better development
                        </Paragraph>
                        <Space size="large">
                            <Button type="primary" size="large" icon={<RocketOutlined />}>
                                Get Started
                            </Button>
                            <Button size="large" icon={<FileSearchOutlined />}>
                                Browse Docs
                            </Button>
                        </Space>
                    </Col>
                </Row>

                {/* Features Section */}
                <Row gutter={[32, 32]} style={{ marginTop: '64px' }}>
                    <Col xs={24} md={8}>
                        <Card hoverable>
                            <BookOutlined style={{ fontSize: '32px', color: '#1890ff' }} />
                            <Title level={3}>Clear Documentation</Title>
                            <Paragraph>
                                Write and organize your documentation with ease using our powerful tools
                            </Paragraph>
                        </Card>
                    </Col>
                    <Col xs={24} md={8}>
                        <Card hoverable>
                            <RocketOutlined style={{ fontSize: '32px', color: '#52c41a' }} />
                            <Title level={3}>Quick Setup</Title>
                            <Paragraph>
                                Get started in minutes with our intuitive setup process
                            </Paragraph>
                        </Card>
                    </Col>
                    <Col xs={24} md={8}>
                        <Card hoverable>
                            <TeamOutlined style={{ fontSize: '32px', color: '#722ed1' }} />
                            <Title level={3}>Team Collaboration</Title>
                            <Paragraph>
                                Work together seamlessly with your team members
                            </Paragraph>
                        </Card>
                    </Col>
                </Row>
            </Content>
        </Layout>
    );
};

export default Home;