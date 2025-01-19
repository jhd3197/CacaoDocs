import React, { ReactNode, useState, useMemo, CSSProperties } from 'react';
import { Menu, Tag, Typography, Input, ConfigProvider } from 'antd';
import { useLocation } from 'react-router-dom';
import { ApiOutlined, SearchOutlined, CodeOutlined, BookOutlined } from '@ant-design/icons';
import './SecondarySidebar.css';
import { Background } from 'reactflow';
import type { AppData, DocItem, ApiEndpoint, TypeItem  } from '../../global';

const { Text } = Typography;
const { SubMenu } = Menu;


interface SecondarySidebarProps {
    onEndpointSelect?: (endpoint: string) => void;
    data: AppData;
}

const methodColors: Record<string, string> = {
    GET: '#10B981',
    POST: '#331201',
    PUT: '#331201',
    DELETE: '#EF4444',
    PATCH: '#8B5CF6'
};

const EndpointItem: React.FC<{
    endpoint: ApiEndpoint;
    onClick: () => void;
}> = ({ endpoint, onClick }) => (
    <div
        onClick={() => {
            onClick();
            // Include method in the hash
            const hash = `/api#${endpoint.endpoint}-${endpoint.method}`;
            window.location.hash = hash;
        }}
        style={{
            borderRadius: '8px',
            padding: '8px 12px',
            margin: '8px 0',
            cursor: 'pointer',
            border: '1px solid #E2E8F0',
            transition: 'all 0.2s ease',
            boxShadow: '0 1px 2px rgba(0, 0, 0, 0.05)',
            background: '#FFFFFF',
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
                padding: '0px 4px',
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

const SearchInput: React.FC<{
    value: string;
    onChange: (value: string) => void;
}> = React.memo(({ value, onChange }) => (
    <Input
        prefix={<SearchOutlined style={{ color: '#654321' }} />}
        placeholder="Search..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        autoFocus
        className="search-input"
        style={{
            borderRadius: '6px',
            backgroundColor: '#FFFFFF',
            borderColor: 'rgba(255, 255, 255, 0.2)',
            color: '#654321'
        }}
    />
));

const MenuContainer: React.FC<{ 
    children: ReactNode; 
    searchText: string; 
    onSearchChange: (value: string) => void;
    openKeys: string[];
    styles: {
        container: React.CSSProperties;
        search: React.CSSProperties;
        base: React.CSSProperties;
    };
    themeVars: any;
}> = ({ children, searchText, onSearchChange, openKeys, styles, themeVars }) => (
    <div style={styles.container}>
        <div style={{
            ...styles.search,
            backgroundColor: themeVars?.secondary_sidebar_bg_color || 'rgb(42 36 32 / 30%)'
        }}>
            <SearchInput value={searchText} onChange={onSearchChange} />
        </div>
        <ConfigProvider
            theme={{
                token: {
                    colorBgBase: themeVars?.secondary_sidebar_bg_color || 'rgb(42 36 32 / 30%)',
                    colorTextBase: themeVars?.secondary_sidebar_text_color || '#fff',
                },
                components: {
                    Menu: {
                        colorItemText: themeVars?.secondary_sidebar_text_color || '#fff',
                        colorItemTextHover: themeVars?.secondary_sidebar_highlight_text_color || '#fff',
                        colorItemTextSelected: '#fff',
                        itemHoverBg: themeVars?.secondary_sidebar_highlight_bg_color || '#331201',
                        colorItemBgSelected: themeVars?.secondary_sidebar_highlight_bg_color || '#331201',
                        colorItemBg: themeVars?.secondary_sidebar_bg_color || 'rgb(42 36 32 / 30%)',
                        subMenuItemBg: themeVars?.secondary_sidebar_bg_color || 'rgb(42 36 32 / 30%)',
                        itemBg: themeVars?.secondary_sidebar_bg_color || 'rgb(42 36 32 / 30%)',
                    },
                },
            }}
        >
            <Menu 
                mode="inline" 
                openKeys={openKeys}
                style={{
                    backgroundColor: 'transparent',
                    color: themeVars?.secondary_sidebar_text_color || '#fff'
                }}
            >
                {children}
            </Menu>
        </ConfigProvider>
    </div>
);

const SecondarySidebar: React.FC<SecondarySidebarProps> = ({ onEndpointSelect, data }) => {
    const themeVars = data?.config?.theme || {
        secondary_sidebar_bg_color: 'rgb(42 36 32 / 30%)',
        secondary_sidebar_text_color: '#fff'
    };
    
    console.log('SecondarySidebar received data:', data); // Debug log
    
    // Add null checks and default arrays
    const safeData = {
        api: Array.isArray(data?.api) ? data.api : [],
        docs: Array.isArray(data?.docs) ? data.docs : [],
        types: Array.isArray(data?.types) ? data.types : []
    };

    const location = useLocation();
    const [searchText, setSearchText] = useState('');

    // Move MENU_STYLES inside the component
    const menuStyles = {
        base: {
            borderRight: 0,
            padding: '0 12px 24px',
            background: 'transparent'
        },
        container: {
            height: '100vh',
            overflowY: 'auto' as const,
            borderRight: `1px solid ${themeVars.secondary_sidebar_bg_color}`,
            maxHeight: '100%', // Ensure it doesn't overflow on mobile
            backgroundColor: themeVars.secondary_sidebar_bg_color
        },
        search: {
            padding: '12px',
            position: 'sticky' as const,
            top: 0,
            backgroundColor: themeVars.secondary_sidebar_bg_color,
            zIndex: 1
        },
        groupTitle: {
            fontSize: '14px',
            fontWeight: 600,
            textTransform: 'uppercase' as const,
            letterSpacing: '0.05em',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            color: themeVars.secondary_sidebar_text_color
        } as CSSProperties
    };

    const filterItems = <T extends { function_name?: string; endpoint?: string }>(items: T[]) => {
        return items.filter(item => 
            (item.function_name?.toLowerCase().includes(searchText.toLowerCase()) ||
            item.endpoint?.toLowerCase().includes(searchText.toLowerCase()))
        );
    };

    const isApiPage = location.pathname === '/api';
    const isTypesPage = location.pathname.includes('/types');
    const isDocsPage = location.pathname.includes('/docs');

    // Memoize tags to prevent infinite re-renders
    const allTags = useMemo(() => {
        const apiTags = Array.from(new Set(safeData.api.map(item => item.tag)));
        const docsTags = Array.from(new Set(safeData.docs.map(item => item.tag)));
        const typesTags = Array.from(new Set(safeData.types.map(item => item.tag)));
        return [...apiTags, ...docsTags, ...typesTags] as string[];
    }, [safeData]);

    const [openKeys, setOpenKeys] = useState<string[]>(allTags);

    const SECTION_ICONS = {
        api: <ApiOutlined style={{ color: '#fff' }} />,
        types: <CodeOutlined style={{ color: '#fff' }} />,
        docs: <BookOutlined style={{ color: '#fff' }} />
    };

    if (isTypesPage) {
        const typesByTag = Object.entries(
            filterItems(safeData.types).reduce((acc: Record<string, TypeItem[]>, type) => {
                if (!acc[type.tag]) {
                    acc[type.tag] = [];
                }
                acc[type.tag].push(type);
                return acc;
            }, {})
        );

        const scrollToType = (functionName: string) => {
            const element = document.getElementById(`type-${functionName}`);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        };

        return (
            <MenuContainer 
                searchText={searchText} 
                onSearchChange={setSearchText}
                openKeys={allTags}
                styles={menuStyles}
                themeVars={themeVars}
            >
                {typesByTag.map(([tag, types]) => (
                    <SubMenu 
                        key={tag} 
                        title={
                            <span style={menuStyles.groupTitle}>
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
                                {type.function_name} ( )
                            </Menu.Item>
                        ))}
                    </SubMenu>
                ))}
            </MenuContainer>
        );
    }

    if (isDocsPage) {
        const docsByTag = Object.entries(
            filterItems(safeData.docs).reduce((acc: Record<string, DocItem[]>, doc) => {
                if (!acc[doc.tag]) {
                    acc[doc.tag] = [];
                }
                acc[doc.tag].push(doc);
                return acc;
            }, {})
        );

        const scrollToDoc = (functionName: string) => {
            const element = document.getElementById(`doc-${functionName}`);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        };

        return (
            <MenuContainer 
                searchText={searchText} 
                onSearchChange={setSearchText}
                openKeys={allTags}
                styles={menuStyles}
                themeVars={themeVars}
            >
                {docsByTag.map(([tag, docs]) => (
                    <SubMenu 
                        key={tag} 
                        title={
                            <span style={menuStyles.groupTitle}>
                                {SECTION_ICONS.docs}
                                {tag.charAt(0).toUpperCase() + tag.slice(1)}
                            </span>
                        }
                    >
                        {docs.map(document => (
                            <Menu.Item 
                                key={document.function_name}
                                onClick={() => scrollToDoc(document.function_name)}
                            >
                                {document.function_name} ( ) 
                            </Menu.Item>
                        ))}
                    </SubMenu>
                ))}
            </MenuContainer>
        );
    }

    if (isApiPage) {
        const filteredEndpoints = filterItems(safeData.api);
        
        const scrollToEndpoint = (endpoint: ApiEndpoint) => {
            // Create element ID using both endpoint path and method
            const elementId = `${endpoint.endpoint}-${endpoint.method}`;
            
            const retryScroll = async (retries = 5, delay = 100) => {
                for (let i = 0; i < retries; i++) {
                    const element = document.getElementById(elementId);
                    if (element) {
                        element.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        // Update URL with the combined endpoint and method
                        window.location.hash = `/api#${elementId}`;
                        break;
                    }
                    await new Promise(resolve => setTimeout(resolve, delay * Math.pow(2, i)));
                }
            };

            retryScroll();
        };

        const groupedEndpoints = Object.entries(
            filteredEndpoints.reduce((acc: Record<string, ApiEndpoint[]>, endpoint) => {
                const tag = endpoint.tag;
                if (!acc[tag]) acc[tag] = [];
                acc[tag].push(endpoint);
                return acc;
            }, {})
        ).sort(([a], [b]) => a.localeCompare(b));

        console.log('Grouped API endpoints:', groupedEndpoints); // Debug log

        return (
            <MenuContainer 
                searchText={searchText} 
                onSearchChange={setSearchText}
                openKeys={allTags}
                styles={menuStyles}
                themeVars={themeVars}
            >
                {groupedEndpoints.map(([tag, endpoints]) => (
                    <Menu.SubMenu
                        key={tag}
                        style={{ 
                            background: themeVars.secondary_sidebar_bg_color
                        }}
                        title={
                            <span style={{ 
                                ...menuStyles.groupTitle,
                                color: themeVars.secondary_sidebar_text_color
                            }}>
                                {SECTION_ICONS.api}
                                {tag}
                            </span>
                        }
                    >
                        <div style={{ padding: '0 4px' }}>
                            {filterItems(endpoints).map((endpoint: ApiEndpoint) => (
                                <EndpointItem
                                    key={`${endpoint.endpoint}-${endpoint.method}`}
                                    endpoint={endpoint}
                                    onClick={() => {
                                        onEndpointSelect?.(endpoint.endpoint);
                                        scrollToEndpoint(endpoint);
                                    }}
                                />
                            ))}
                        </div>
                    </Menu.SubMenu>
                ))}
            </MenuContainer>
        );
    }

    return (
        <MenuContainer 
            searchText={searchText} 
            onSearchChange={setSearchText}
            openKeys={allTags}
            styles={menuStyles}
            themeVars={themeVars}
        >
            <Menu.Item key="1">Introduction</Menu.Item>
            <Menu.Item key="2">Quick Start</Menu.Item>
            <Menu.Item key="3">Installation</Menu.Item>
        </MenuContainer>
    );
};

export default SecondarySidebar;
