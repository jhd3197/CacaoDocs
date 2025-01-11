import React from 'react';
import { Menu, Typography, Image } from 'antd';
import { Link, useLocation } from 'react-router-dom';
import { 
    HomeOutlined, 
    ApiOutlined, 
    BlockOutlined, 
    FileTextOutlined,
    GithubOutlined
} from '@ant-design/icons';
import logo from '../../assets/img/logo.png';

import type { AppData } from '../../global';

const { Title } = Typography;


interface MainSidebarProps {
    apiData: AppData;
}

const MainSidebar: React.FC<MainSidebarProps> = ({ apiData }) => {
    const location = useLocation();
    const logoSource = apiData.config.logo_url || logo;

    return (
        <div style={{ 
            padding: '16px 0',
            height: '100%',
            display: 'flex',
            flexDirection: 'column'
        }}>
            <div style={{ 
                padding: '0 24px', 
                marginBottom: '24px',
                display: 'flex',
                alignItems: 'center',
            }}>
                <Image
                    src={logoSource}
                    alt="Logo"
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
                style={{ borderRight: 0, flex: 1 }}
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
            
            <div style={{
                padding: '16px 24px',
                borderTop: '1px solid rgba(0, 0, 0, 0.06)',
                textAlign: 'center'
            }}>
                {apiData.config.github_url && (
                    <a 
                        href={apiData.config.github_url}
                        target="_blank" 
                        rel="noopener noreferrer"
                        style={{ fontSize: '24px', color: 'inherit' }}
                    >
                        <GithubOutlined />
                    </a>
                )}
                {apiData.config.footer_text && (
                    <div 
                        style={{ 
                            marginTop: '8px',
                            fontSize: '12px',
                            color: 'rgba(0, 0, 0, 0.45)'
                        }}
                        dangerouslySetInnerHTML={{ __html: apiData.config.footer_text }}
                    />
                )}
            </div>
        </div>
    );
};

export default MainSidebar;