import React from 'react';
import { Layout } from 'antd';

const { Sider } = Layout;

const Sidebar: React.FC = () => {
    return (
        <Sider width={180} theme="light" style={{ 
            borderRight: '1px solid #f0f0f0',
            position: 'fixed',
            left: 0,
            height: '100vh',
            zIndex: 2
        }}>
            {/* ...existing content... */}
        </Sider>
    );
};

export default Sidebar;
