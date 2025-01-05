import React, { ReactNode } from 'react';
import { Layout as AntLayout } from 'antd';
import { useLocation } from 'react-router-dom';
import MainSidebar from './MainSidebar';
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

    return (
        <AntLayout style={{ minHeight: '100vh' }}>
            <Sider
                width={MAIN_SIDEBAR_WIDTH}
                style={{
                    background: '#fff',
                    borderRight: '1px solid #E2E8F0',
                    height: '100vh',
                    position: 'fixed',
                    left: 0,
                    zIndex: 2
                }}
            >
                <MainSidebar apiData={apiData} />
            </Sider>
            <AntLayout style={{ marginLeft: MAIN_SIDEBAR_WIDTH }}>
                {needsSecondarySidebar && (
                    <Sider
                        width={SECONDARY_SIDEBAR_WIDTH}
                        style={{
                            background: '#2A2420',
                            borderRight: '1px solid rgba(0, 0, 0, 0.2)',
                            height: '100vh',
                            position: 'fixed',
                            left: MAIN_SIDEBAR_WIDTH,
                            zIndex: 1
                        }}
                    >
                        <SecondarySidebar data={apiData} /> {/* Pass apiData to SecondarySidebar */}
                    </Sider>
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
