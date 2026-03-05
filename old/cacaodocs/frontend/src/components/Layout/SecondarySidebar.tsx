import React, { ReactNode, useState, useMemo, CSSProperties } from 'react';
import { Menu, Input, ConfigProvider } from 'antd';
import { useLocation, Link } from 'react-router-dom';
import {
    SearchOutlined,
    AppstoreOutlined,
    BlockOutlined,
    FunctionOutlined,
    FileTextOutlined
} from '@ant-design/icons';
import './SecondarySidebar.css';
import type { AppData, ModuleDoc, ClassDoc, FunctionDoc } from '../../global';
const { SubMenu } = Menu;

interface SecondarySidebarProps {
    data: AppData;
}

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
                defaultOpenKeys={openKeys}
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

const SecondarySidebar: React.FC<SecondarySidebarProps> = ({ data }) => {
    const themeVars = data?.config?.theme || {
        secondary_sidebar_bg_color: 'rgb(42 36 32 / 30%)',
        secondary_sidebar_text_color: '#fff'
    };

    const location = useLocation();
    const [searchText, setSearchText] = useState('');

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
            maxHeight: '100%',
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

    const isModulesPage = location.pathname.startsWith('/modules');
    const isClassesPage = location.pathname.startsWith('/classes');
    const isFunctionsPage = location.pathname.startsWith('/functions');
    const isPagesPage = location.pathname.startsWith('/pages');

    const SECTION_ICONS = {
        modules: <AppstoreOutlined style={{ color: '#fff' }} />,
        classes: <BlockOutlined style={{ color: '#fff' }} />,
        functions: <FunctionOutlined style={{ color: '#fff' }} />,
        pages: <FileTextOutlined style={{ color: '#fff' }} />
    };

    // Group modules by top-level package
    const groupedModules = useMemo(() => {
        const filtered = data.modules.filter(m =>
            m.full_path.toLowerCase().includes(searchText.toLowerCase()) ||
            m.name.toLowerCase().includes(searchText.toLowerCase())
        );
        return filtered.reduce((acc, module) => {
            const parts = module.full_path.split('.');
            const topLevel = parts[0] || module.name;
            if (!acc[topLevel]) acc[topLevel] = [];
            acc[topLevel].push(module);
            return acc;
        }, {} as Record<string, ModuleDoc[]>);
    }, [data.modules, searchText]);

    // Group classes by module
    const groupedClasses = useMemo(() => {
        const filtered = data.classes.filter(c =>
            c.name.toLowerCase().includes(searchText.toLowerCase()) ||
            c.full_path.toLowerCase().includes(searchText.toLowerCase())
        );
        return filtered.reduce((acc, cls) => {
            const module = cls.module || 'Other';
            if (!acc[module]) acc[module] = [];
            acc[module].push(cls);
            return acc;
        }, {} as Record<string, ClassDoc[]>);
    }, [data.classes, searchText]);

    // Group functions by module
    const groupedFunctions = useMemo(() => {
        const filtered = data.functions.filter(f =>
            f.name.toLowerCase().includes(searchText.toLowerCase()) ||
            f.full_path.toLowerCase().includes(searchText.toLowerCase())
        );
        return filtered.reduce((acc, func) => {
            const module = func.module || 'Other';
            if (!acc[module]) acc[module] = [];
            acc[module].push(func);
            return acc;
        }, {} as Record<string, FunctionDoc[]>);
    }, [data.functions, searchText]);

    // Filter pages
    const filteredPages = useMemo(() => {
        return data.pages.filter(p =>
            p.title.toLowerCase().includes(searchText.toLowerCase()) ||
            p.slug.toLowerCase().includes(searchText.toLowerCase())
        );
    }, [data.pages, searchText]);

    const allKeys = useMemo(() => [
        ...Object.keys(groupedModules),
        ...Object.keys(groupedClasses),
        ...Object.keys(groupedFunctions),
    ], [groupedModules, groupedClasses, groupedFunctions]);

    if (isModulesPage) {
        return (
            <MenuContainer
                searchText={searchText}
                onSearchChange={setSearchText}
                openKeys={Object.keys(groupedModules)}
                styles={menuStyles}
                themeVars={themeVars}
            >
                {Object.entries(groupedModules).map(([pkg, modules]) => (
                    <SubMenu
                        key={pkg}
                        title={
                            <span style={menuStyles.groupTitle}>
                                {SECTION_ICONS.modules}
                                {pkg}
                            </span>
                        }
                    >
                        {modules.map(module => (
                            <Menu.Item key={module.full_path}>
                                <Link to={`/modules/${encodeURIComponent(module.full_path)}`}>
                                    {module.full_path}
                                </Link>
                            </Menu.Item>
                        ))}
                    </SubMenu>
                ))}
            </MenuContainer>
        );
    }

    if (isClassesPage) {
        return (
            <MenuContainer
                searchText={searchText}
                onSearchChange={setSearchText}
                openKeys={Object.keys(groupedClasses)}
                styles={menuStyles}
                themeVars={themeVars}
            >
                {Object.entries(groupedClasses).map(([module, classes]) => (
                    <SubMenu
                        key={module}
                        title={
                            <span style={menuStyles.groupTitle}>
                                {SECTION_ICONS.classes}
                                {module}
                            </span>
                        }
                    >
                        {classes.map(cls => (
                            <Menu.Item key={cls.full_path}>
                                <Link to={`/classes/${encodeURIComponent(cls.full_path)}`}>
                                    {cls.name}
                                </Link>
                            </Menu.Item>
                        ))}
                    </SubMenu>
                ))}
            </MenuContainer>
        );
    }

    if (isFunctionsPage) {
        return (
            <MenuContainer
                searchText={searchText}
                onSearchChange={setSearchText}
                openKeys={Object.keys(groupedFunctions)}
                styles={menuStyles}
                themeVars={themeVars}
            >
                {Object.entries(groupedFunctions).map(([module, functions]) => (
                    <SubMenu
                        key={module}
                        title={
                            <span style={menuStyles.groupTitle}>
                                {SECTION_ICONS.functions}
                                {module}
                            </span>
                        }
                    >
                        {functions.map(func => (
                            <Menu.Item key={func.full_path}>
                                <a
                                    href={`#function-${func.name}`}
                                    onClick={(e) => {
                                        e.preventDefault();
                                        const el = document.getElementById(`function-${func.name}`);
                                        if (el) el.scrollIntoView({ behavior: 'smooth' });
                                    }}
                                >
                                    {func.name}()
                                </a>
                            </Menu.Item>
                        ))}
                    </SubMenu>
                ))}
            </MenuContainer>
        );
    }

    if (isPagesPage) {
        return (
            <MenuContainer
                searchText={searchText}
                onSearchChange={setSearchText}
                openKeys={['pages']}
                styles={menuStyles}
                themeVars={themeVars}
            >
                <SubMenu
                    key="pages"
                    title={
                        <span style={menuStyles.groupTitle}>
                            {SECTION_ICONS.pages}
                            Guides
                        </span>
                    }
                >
                    {filteredPages.map(page => (
                        <Menu.Item key={page.slug}>
                            <Link to={`/pages/${encodeURIComponent(page.slug)}`}>
                                {page.title}
                            </Link>
                        </Menu.Item>
                    ))}
                </SubMenu>
            </MenuContainer>
        );
    }

    // Default: show overview
    return (
        <MenuContainer
            searchText={searchText}
            onSearchChange={setSearchText}
            openKeys={allKeys}
            styles={menuStyles}
            themeVars={themeVars}
        >
            <Menu.Item key="intro">
                <Link to="/">Overview</Link>
            </Menu.Item>
        </MenuContainer>
    );
};

export default SecondarySidebar;
