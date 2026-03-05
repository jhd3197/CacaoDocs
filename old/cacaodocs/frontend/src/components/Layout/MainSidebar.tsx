import React from 'react';
import { Menu, Image, Button } from 'antd';
import { Link, useLocation } from 'react-router-dom';
import {
    HomeOutlined,
    AppstoreOutlined,
    BlockOutlined,
    FunctionOutlined,
    FileTextOutlined,
    GithubOutlined,
    SearchOutlined
} from '@ant-design/icons';
import logo from '../../assets/img/logo.png';

import type { AppData } from '../../global';

interface MainSidebarProps {
    apiData: AppData;
}

const MainSidebar: React.FC<MainSidebarProps> = ({ apiData }) => {
    const location = useLocation();
    const logoSource = apiData.config.logo_url || logo;

    const triggerSearch = () => {
        // Simulate Ctrl+K keyboard event
        const event = new KeyboardEvent('keydown', {
            key: 'k',
            code: 'KeyK',
            ctrlKey: true,
            bubbles: true
        });
        document.dispatchEvent(event);
    };

    const hasModules = apiData.modules.length > 0;
    const hasClasses = apiData.classes.length > 0;
    const hasFunctions = apiData.functions.length > 0;
    const hasPages = apiData.pages.length > 0;

    return (
        <div style={{
            padding: '16px 0',
            height: '100%',
            display: 'flex',
            flexDirection: 'column'
        }}>
            <div style={{
                padding: '0 24px',
                marginBottom: '16px',
                display: 'flex',
                alignItems: 'center',
            }}>
                <Image
                    src={logoSource}
                    alt="Logo"
                    preview={false}
                    style={{
                        maxWidth: '100%',
                        objectFit: 'contain'
                    }}
                />
            </div>

            <Button
                style={{
                    margin: '0 24px 16px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between'
                }}
                onClick={triggerSearch}
                icon={<SearchOutlined />}
            >
                <span style={{ marginRight: 'auto', marginLeft: 8 }}>Search</span>
                <span style={{
                    opacity: 0.5,
                    fontSize: '12px',
                    marginLeft: 8
                }}>Ctrl+K</span>
            </Button>

            <Menu
                mode="inline"
                selectedKeys={[location.pathname]}
                style={{ borderRight: 0, flex: 1 }}
            >
                <Menu.Item key="/" icon={<HomeOutlined />}>
                    <Link to="/">Home</Link>
                </Menu.Item>
                {hasModules && (
                    <Menu.Item key="/modules" icon={<AppstoreOutlined />}>
                        <Link to="/modules">Modules</Link>
                    </Menu.Item>
                )}
                {hasClasses && (
                    <Menu.Item key="/classes" icon={<BlockOutlined />}>
                        <Link to="/classes">Classes</Link>
                    </Menu.Item>
                )}
                {hasFunctions && (
                    <Menu.Item key="/functions" icon={<FunctionOutlined />}>
                        <Link to="/functions">Functions</Link>
                    </Menu.Item>
                )}
                {hasPages && (
                    <Menu.Item key="/pages" icon={<FileTextOutlined />}>
                        <Link to="/pages">Guides</Link>
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
