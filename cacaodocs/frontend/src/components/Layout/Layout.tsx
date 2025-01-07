import React, { ReactNode } from 'react';
import { Layout as AntLayout } from 'antd';
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
            <Sider
                width={MAIN_SIDEBAR_WIDTH}
                style={{
                    background: themeVars.sidebar_bg_color,
                    borderRight: '1px solid '+themeVars.sidebar_bg_color || '#fff',
                    height: '100vh',
                    position: 'fixed',
                    left: 0,
                    zIndex: 2
                }}
            >
                <MainSidebar apiData={apiData} />
            </Sider></ConfigProvider>
            <AntLayout style={{ marginLeft: MAIN_SIDEBAR_WIDTH }}>
                {needsSecondarySidebar && (
                    <ConfigProvider
                      theme={{
                        // Global tokens (common for all components) 
                        token: {
                          // You can set “base” backgrounds or text here if desired
                          colorBgBase: themeVars.secondary_sidebar_bg_color || '#2A2420',
                          colorTextBase: themeVars.secondary_sidebar_text_color || '#fff',
                        },
                        // Component-specific token overrides
                        components: {
                          Menu: {
                            colorItemText: themeVars.secondary_sidebar_text_color || '#fff',
                            colorItemTextHover: themeVars.secondary_sidebar_highlight_text_color || '#fff',
                            colorItemTextSelected: '#fff',
                            itemHoverBg: themeVars.secondary_sidebar_highlight_bg_color || '#331201',
                            colorItemBgSelected: themeVars.secondary_sidebar_highlight_bg_color || '#331201',
                            colorItemBg: themeVars.secondary_sidebar_bg_color || '#2a2420',

                            subMenuItemBg: themeVars.secondary_sidebar_bg_color || '#2a2420',
                            itemBg: themeVars.secondary_sidebar_bg_color || '#2A2420',
                          },
                        },
                      }}
                    >
                    <Sider
                        width={SECONDARY_SIDEBAR_WIDTH}
                        style={{
                            background:themeVars.secondary_sidebar_bg_color || '#2a2420',
                            height: '100vh',
                            position: 'fixed',
                            left: MAIN_SIDEBAR_WIDTH,
                            zIndex: 1
                        }}
                    >
                        <SecondarySidebar data={apiData} /> {/* Pass apiData to SecondarySidebar */}
                    </Sider>

                        </ConfigProvider>
                )}
                <Content style={{ 
                    marginLeft: needsSecondarySidebar ? SECONDARY_SIDEBAR_WIDTH : 0,
                    background: '#fff',
                    minHeight: '100vh',
                }}>
                    {children}
                </Content>
            </AntLayout>
        </AntLayout>
    );
};

export default CustomLayout;
