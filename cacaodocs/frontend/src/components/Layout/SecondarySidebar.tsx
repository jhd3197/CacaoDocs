import React, { ReactNode, useState, CSSProperties } from 'react';
import { Menu, Tag, Typography, Input } from 'antd';
import { useLocation } from 'react-router-dom';
import { ApiOutlined, SearchOutlined, CodeOutlined, BookOutlined } from '@ant-design/icons';
import localData from '../../data/localData.json';
import './SecondarySidebar.css';

const { Text } = Typography;
const { SubMenu } = Menu;

interface SecondarySidebarProps {
    onEndpointSelect?: (endpoint: string) => void;
}

const methodColors: Record<string, string> = {
    GET: '#10B981',    // Green
    POST: '#331201',   // Brown
    PUT: '#331201',    // Brown
    DELETE: '#EF4444', // Red
    PATCH: '#8B5CF6'   // Purple
};

const MENU_STYLES = {
    base: {
        borderRight: 0,
        padding: '0 12px 24px',
        background: 'transparent'
    },
    container: {
        height: '100vh',
        overflowY: 'auto' as const,
        backgroundColor: '#2A2420',
        borderRight: '1px solid rgba(0, 0, 0, 0.2)',
        '& .ant-menu': {
            backgroundColor: 'transparent',
            color: '#FFFFFF'
        }
    },
    search: {
        padding: '12px',
        position: 'sticky' as const,
        top: 0,
        backgroundColor: '#2A2420',
        borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
        zIndex: 1
    },
    menuItem: {
        margin: '4px 0',
        padding: '8px 12px',
        borderRadius: '6px',
        color: 'rgba(255, 255, 255, 0.85)',
        '&:hover': {
            backgroundColor: 'rgba(255, 255, 255, 0.1)'
        }
    },
    subMenu: {
        fontWeight: 600,
        color: '#E6D5C9',  // Updated color
        fontSize: '14px',
        textTransform: 'uppercase' as const,
        letterSpacing: '0.05em',
        display: 'flex',
        alignItems: 'center',
        gap: '8px'
    },
    groupTitle: {
        fontSize: '14px',
        fontWeight: 600,
        color: '#E6D5C9',
        textTransform: 'uppercase' as const,
        letterSpacing: '0.05em',
        display: 'flex',
        alignItems: 'center',
        gap: '8px'
    } as CSSProperties
};

const EndpointItem: React.FC<{
    endpoint: any;
    onClick: () => void;
}> = ({ endpoint, onClick }) => (
    <div
        onClick={onClick}
        style={{
            background: '#FFFFFF',
            borderRadius: '8px',
            padding: '8px 12px',
            margin: '8px 0',
            cursor: 'pointer',
            border: '1px solid #E2E8F0',
            transition: 'all 0.2s ease',
            boxShadow: '0 1px 2px rgba(0, 0, 0, 0.05)'
        }}
        onMouseEnter={e => {
            e.currentTarget.style.background = '#F8FAFC';
            e.currentTarget.style.transform = 'translateY(-1px)';
            e.currentTarget.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.05)';
        }}
        onMouseLeave={e => {
            e.currentTarget.style.background = '#FFFFFF';
            e.currentTarget.style.transform = 'translateY(0)';
            e.currentTarget.style.boxShadow = '0 1px 2px rgba(0, 0, 0, 0.05)';
        }}
    >
        <Text style={{ 
            display: 'block',
            fontSize: '13px',
            color: '#475569',
            marginBottom: '4px',
            fontWeight: 500
        }}>
            {endpoint.endpoint}
        </Text>
        <Tag
            color={methodColors[endpoint.method]}
            style={{
                margin: 0,
                padding: '0px 4px',  // Modified padding
                borderRadius: '4px',
                fontSize: '11px',
                lineHeight: '18px',
                fontWeight: 600
            }}
        >
            {endpoint.method}
        </Tag>
    </div>
);

interface ReturnType {
    description: string;
    full_type: string;
    is_list: boolean;
    is_type_ref: boolean;
    type_name: string;
}

interface DocItem {
    args?: Record<string, any>;  // Made optional
    description?: string;        // Made optional
    function_name: string;
    method?: string;            // Made optional
    returns?: ReturnType;       // Made optional
    status?: string;            // Made optional
    tag: string;
    type: string;
    version?: string;           // Made optional
    function_source?: string;   // Added
    inputs?: string[];          // Added
    outputs?: string | null;    // Updated to accept null
}

const SecondarySidebar: React.FC<SecondarySidebarProps> = ({ onEndpointSelect }) => {
    const location = useLocation();
    const [searchText, setSearchText] = useState('');

    const filterItems = (items: any[]) => {
        return items.filter(item => 
            item.function_name?.toLowerCase().includes(searchText.toLowerCase()) ||
            item.endpoint?.toLowerCase().includes(searchText.toLowerCase())
        );
    };

    const isApiPage = location.pathname === '/api';
    const isTypesPage = location.pathname.includes('/types');
    const isDocsPage = location.pathname.includes('/docs');

    // Get all tags for each section
    const apiTags = Array.from(new Set(localData.api.map(item => item.tag)));
    const docsTags = Array.from(new Set(localData.docs.map(item => item.tag)));
    const typesTags = Array.from(new Set(localData.types.map(item => item.tag)));

    // Combine all possible tags
    const allTags = [...apiTags, ...docsTags, ...typesTags];

    const SECTION_ICONS = {
        api: <ApiOutlined style={{ color: '#fff' }} />,
        types: <CodeOutlined style={{ color: '#fff' }} />,
        docs: <BookOutlined style={{ color: '#fff' }} />
    };

    const MenuContainer: React.FC<{ children: ReactNode }> = ({ children }) => (
        <div style={MENU_STYLES.container}>
            <div style={MENU_STYLES.search}>
                <Input
                    prefix={<SearchOutlined style={{ color: 'rgba(255, 255, 255, 0.65)' }} />}
                    placeholder="Search..."
                    onChange={(e) => setSearchText(e.target.value)}
                    className="search-input" // Added className
                    style={{
                        borderRadius: '6px',
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                        borderColor: 'rgba(255, 255, 255, 0.2)',
                        color: '#FFFFFF'
                    }}
                />
            </div>
            <Menu 
                mode="inline" 
                style={MENU_STYLES.base}
                defaultOpenKeys={allTags}
                theme="dark"
                className="custom-dark-menu"
            >
                {children}
            </Menu>
        </div>
    );

    if (isTypesPage) {
        const typesByTag = localData.types.reduce((acc, type) => {
            if (!acc[type.tag]) {
                acc[type.tag] = [];
            }
            acc[type.tag].push(type);
            return acc;
        }, {} as Record<string, typeof localData.types>);

        // Get all tags for default open keys
        const allTags = Object.keys(typesByTag);

        const scrollToType = (functionName: string) => {
            const element = document.getElementById(`type-${functionName}`);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        };

        return (
            <MenuContainer>
                {Object.entries(typesByTag).map(([tag, types]) => (
                    <SubMenu 
                        key={tag} 
                        title={
                            <span style={MENU_STYLES.groupTitle}>
                                {SECTION_ICONS.types}
                                {tag.charAt(0).toUpperCase() + tag.slice(1)}
                            </span>
                        }
                    >
                        {types.map(type => (
                            <Menu.Item 
                                key={type.function_name}
                                onClick={() => scrollToType(type.function_name)}
                            >
                                {type.function_name}
                            </Menu.Item>
                        ))}
                    </SubMenu>
                ))}
            </MenuContainer>
        );
    }

    // Add docs page handling
    if (isDocsPage) {
        const docsByTag = localData.docs.reduce((acc, doc) => {
            if (!acc[doc.tag]) {
                acc[doc.tag] = [];
            }
            acc[doc.tag].push(doc);
            return acc;
        }, {} as Record<string, DocItem[]>); // Updated type assertion

        const allTags = Object.keys(docsByTag);

        const scrollToDoc = (functionName: string) => {
            const element = document.getElementById(`doc-${functionName}`);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        };

        return (
            <MenuContainer>
                {Object.entries(docsByTag).map(([tag, docs]) => (
                    <SubMenu 
                        key={tag} 
                        title={
                            <span style={MENU_STYLES.groupTitle}>
                                {SECTION_ICONS.docs}
                                {tag.charAt(0).toUpperCase() + tag.slice(1)}
                            </span>
                        }
                    >
                        {docs.map(doc => (
                            <Menu.Item 
                                key={doc.function_name}
                                onClick={() => scrollToDoc(doc.function_name)}
                            >
                                {doc.function_name} ( ) 
                            </Menu.Item>
                        ))}
                    </SubMenu>
                ))}
            </MenuContainer>
        );
    }

    if (isApiPage) {
        const groupedEndpoints = Object.entries(
            localData.api.reduce((acc, endpoint) => {
                const tag = endpoint.tag;
                if (!acc[tag]) acc[tag] = [];
                acc[tag].push(endpoint);
                return acc;
            }, {} as Record<string, any[]>)
        ).sort(([a], [b]) => a.localeCompare(b));

        return (
            <MenuContainer>
                {groupedEndpoints.map(([tag, endpoints]) => (
                    <Menu.SubMenu
                        key={tag}
                        style={{ background: 'transparent' }} // Changed from #fff to transparent
                        title={
                            <span style={{ 
                                fontSize: '14px',
                                fontWeight: 600,
                                color: '#fff', // Changed to white
                                textTransform: 'uppercase',
                                letterSpacing: '0.05em',
                                display: 'flex',
                                alignItems: 'center',
                                gap: '8px'
                            }}>
                                {SECTION_ICONS.api}
                                {tag}
                            </span>
                        }
                    >
                        <div style={{ padding: '0 4px' }}>
                            {filterItems(endpoints).map((endpoint) => (
                                <EndpointItem
                                    key={endpoint.endpoint}
                                    endpoint={endpoint}
                                    onClick={() => onEndpointSelect?.(endpoint.endpoint)}
                                />
                            ))}
                        </div>
                    </Menu.SubMenu>
                ))}
            </MenuContainer>
        );
    }

    // Default sidebar content for other pages
    return (
        <MenuContainer>
            <Menu.Item key="1">Introduction</Menu.Item>
            <Menu.Item key="2">Quick Start</Menu.Item>
            <Menu.Item key="3">Installation</Menu.Item>
        </MenuContainer>
    );
};

export default SecondarySidebar;