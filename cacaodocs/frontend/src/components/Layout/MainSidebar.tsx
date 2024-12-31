import React from 'react';
import { Menu, Typography, Image } from 'antd';
import { Link, useLocation } from 'react-router-dom';
import { 
    HomeOutlined, 
    ApiOutlined, 
    BlockOutlined, 
    FileTextOutlined 
} from '@ant-design/icons';
import logo from '../../assets/img/logo.png';

const { Title } = Typography;

const MainSidebar: React.FC = () => {
    const location = useLocation();

    return (
        <div style={{ padding: '16px 0' }}>
            <div style={{ 
                padding: '0 24px', 
                marginBottom: '24px',
                display: 'flex',
                alignItems: 'center',
            }}>
                <Image
                    src={logo}
                    alt="CacaoDocs Logo"
                    preview={false}
                    style={{
                        width: '100%',
                        objectFit: 'contain'
                    }}
                />
            </div>
            <Menu
                mode="inline"
                selectedKeys={[location.pathname]}
                style={{ borderRight: 0 }}
            >
                <Menu.Item key="/" icon={<HomeOutlined />}>
                    <Link to="/">Home</Link>
                </Menu.Item>
                <Menu.Item key="/api" icon={<ApiOutlined />}>
                    <Link to="/api">API</Link>
                </Menu.Item>
                <Menu.Item key="/types" icon={<BlockOutlined />}>
                    <Link to="/types">Types</Link>
                </Menu.Item>
                <Menu.Item key="/docs" icon={<FileTextOutlined />}>
                    <Link to="/docs">Docs</Link>
                </Menu.Item>
            </Menu>
        </div>
    );
};

export default MainSidebar;