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

interface MainSidebarProps {
    apiData: {
        api: any[];
        docs: any[];
        types: any[];
    };
}

const MainSidebar: React.FC<MainSidebarProps> = ({ apiData }) => {
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
                {apiData.api.length > 0 && (
                    <Menu.Item key="/api" icon={<ApiOutlined />}>
                        <Link to="/api">API</Link>
                    </Menu.Item>
                )}
                {apiData.types.length > 0 && (
                    <Menu.Item key="/types" icon={<BlockOutlined />}>
                        <Link to="/types">Types</Link>
                    </Menu.Item>
                )}
                {apiData.docs.length > 0 && (
                    <Menu.Item key="/docs" icon={<FileTextOutlined />}>
                        <Link to="/docs">Docs</Link>
                    </Menu.Item>
                )}
            </Menu>
        </div>
    );
};

export default MainSidebar;