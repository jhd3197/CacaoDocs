import React, { ReactNode, useState, useEffect } from 'react';
import { Layout as AntLayout, Button, Drawer } from 'antd';
import { MenuOutlined } from '@ant-design/icons';
import { useLocation } from 'react-router-dom';
import MainSidebar from './MainSidebar';
import { ConfigProvider } from 'antd';
import SecondarySidebar from './SecondarySidebar';
import type { AppData } from '../../global';

const { Content, Sider } = AntLayout;

// Constants for sidebar widths
const MAIN_SIDEBAR_WIDTH = 180;
const SECONDARY_SIDEBAR_WIDTH = 240;

interface LayoutProps {
    apiData: AppData;
    children: ReactNode;
}

const CustomLayout: React.FC<LayoutProps> = ({ children, apiData }) => {
    const location = useLocation();
    const isHomePage = location.pathname === '/';
    const needsSecondarySidebar = !isHomePage;
    const themeVars = apiData.config.theme;

    const [isMobile, setIsMobile] = useState(window.innerWidth <= 768);
    const [drawerVisible, setDrawerVisible] = useState(false);
    const [drawerView, setDrawerView] = useState<'main' | 'secondary'>(
        isHomePage ? 'main' : 'secondary'
    );

    useEffect(() => {
        const handleResize = () => {
            setIsMobile(window.innerWidth <= 768);
        };

        window.addEventListener('resize', handleResize);
        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);

    useEffect(() => {
        if (isMobile) {
            if (needsSecondarySidebar) {
                setDrawerView('secondary');
                setDrawerVisible(true);
            } else {
                setDrawerView('main');
                setDrawerVisible(false);
            }
        }
    }, [location.pathname, isMobile, needsSecondarySidebar]);

    return (
        <AntLayout style={{ minHeight: '100vh' }}>
            <ConfigProvider
                theme={{
                    // Global tokens (common for all components) 
                    token: {
                        // You can set “base” backgrounds or text here if desired
                        colorBgBase: themeVars.sidebar_bg_color || '#2A2420',
                        colorTextBase: themeVars.sidebar_text_color || '#fff',
                    },
                    // Component-specific token overrides
                    components: {
                        Menu: {
                            colorItemText: themeVars.sidebar_text_color || '#fff',
                            colorItemTextHover: themeVars.sidebar_highlight_text_color || '#fff',
                            colorItemTextSelected: '#fff',
                            itemHoverBg: themeVars.sidebar_highlight_bg_color || '#331201',
                            colorItemBgSelected: themeVars.sidebar_highlight_bg_color || '#331201',
                            colorItemBg: themeVars.sidebar_bg_color || '#2a2420',

                            subMenuItemBg: themeVars.sidebar_bg_color || '#2a2420',
                            itemBg: themeVars.sidebar_bg_color || '#2A2420',
                        },
                    },
                }}
            >
                {isMobile ? (
                    <>
                        <Button
                            type="primary"
                            icon={<MenuOutlined />}
                            onClick={() => {
                                setDrawerVisible(true);
                                setDrawerView(isHomePage ? 'main' : 'secondary');
                            }}
                            style={{ position: 'fixed', top: 16, left: 16, zIndex: 3 }}
                        />
                        <Drawer
                            title={
                                drawerView === 'main'
                                    ? 'Main Menu'
                                    : <>
                                        <Button
                                            type="link"
                                            onClick={() => setDrawerView('main')}
                                            style={{ padding: 0, marginRight: 8 }}
                                        >
                                            {'← Back'}
                                        </Button>
                                        {'Secondary Menu'}
                                    </>
                            }
                            placement="left"
                            closable={false}
                            maskClosable={true}
                            onClose={() => setDrawerVisible(false)}
                            visible={drawerVisible}
                            bodyStyle={{ padding: 0 }}
                            width={250} // Reduced width on mobile
                        >
                            {drawerView === 'main' ? (
                                <MainSidebar apiData={apiData} />
                            ) : (
                                <SecondarySidebar data={apiData} />
                            )}
                        </Drawer>
                    </>
                ) : (
                    <>
                        <Sider
                            width={MAIN_SIDEBAR_WIDTH}
                            style={{
                                background: themeVars.sidebar_bg_color,
                                borderRight: '1px solid ' + themeVars.sidebar_bg_color || '#fff',
                                height: '100vh',
                                position: 'fixed',
                                left: 0,
                                zIndex: 2
                            }}
                        >
                            <MainSidebar apiData={apiData} />
                        </Sider>
                        {needsSecondarySidebar && (
                            <Sider
                                width={SECONDARY_SIDEBAR_WIDTH}
                                style={{
                                    background: themeVars.secondary_sidebar_bg_color || '#2a2420',
                                    height: '100vh',
                                    position: 'fixed',
                                    left: MAIN_SIDEBAR_WIDTH,
                                    zIndex: 1
                                }}
                            >
                                <SecondarySidebar data={apiData} /> {/* Pass apiData to SecondarySidebar */}
                            </Sider>
                        )}
                    </>
                )}
            </ConfigProvider>
            <AntLayout
                style={{
                    marginLeft: isMobile ? 0 : needsSecondarySidebar
                        ? MAIN_SIDEBAR_WIDTH + SECONDARY_SIDEBAR_WIDTH
                        : MAIN_SIDEBAR_WIDTH
                }}
            >
                <Content
                    style={{
                        marginLeft: 0,
                        background: '#fff',
                        minHeight: '100vh',
                    }}
                >
                    {children}
                </Content>
            </AntLayout>
        </AntLayout>
    );
};

export default CustomLayout;
