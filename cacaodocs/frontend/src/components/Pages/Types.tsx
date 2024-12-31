import React, { useEffect, useState } from 'react';
import { Table, Spin, Tag, Layout, Switch, Space, Input, Select, Typography } from 'antd';
import { TableOutlined, AppstoreOutlined } from '@ant-design/icons';
import localData from '../../data/localData.json';
import TypeCard from './TypeCard';

const { Content } = Layout;
const { Title, Text } = Typography;
const { Search } = Input;

interface TypeArgument {
    bg_color: string;
    color: string;
    description: string;
    emoji: string;
    type: string;
}

interface TypeDefinition {
    args: Record<string, TypeArgument>;
    description: string;
    function_name: string;
    tag: string;
    type: string;
}

const Types: React.FC = () => {
    const [data, setData] = useState<TypeDefinition[]>([]);
    const [loading, setLoading] = useState(true);
    const [viewMode, setViewMode] = useState<'card' | 'table'>('card');
    const [searchText, setSearchText] = useState('');
    const [selectedTags, setSelectedTags] = useState<string[]>([]);

    useEffect(() => {
        try {
            // Transform the data to ensure it matches our interface
            const transformedData = localData.types.map(type => ({
                ...type,
                args: Object.fromEntries(
                    Object.entries(type.args).map(([key, value]) => [
                        key,
                        {
                            bg_color: value.bg_color || '#ffffff',
                            color: value.color || '#000000',
                            description: value.description || '',
                            emoji: value.emoji || '',
                            type: value.type || 'any'
                        }
                    ])
                )
            })) as TypeDefinition[];
            
            setData(transformedData);
        } catch (error) {
            console.error('Error transforming types data:', error);
            setData([]);
        }
        setLoading(false);
    }, []);

    const generateTypeDefinition = (type: TypeDefinition): string => {
        // Sort properties for consistent display
        const sortedProperties = Object.entries(type.args)
            .sort(([a], [b]) => a.localeCompare(b))
            .map(([key, value]) => {
                let typeStr = value.type;
                // Handle special types
                if (typeStr.startsWith('List[')) {
                    typeStr = `${typeStr.slice(5, -1)}[]`;
                }
                return `    ${key}: ${typeStr};`;
            })
            .join('\n');

        return `interface ${type.function_name} {\n${sortedProperties}\n}`;
    };

    const uniqueTags = Array.from(new Set(data.map(item => item.tag)));

    const filterData = (data: TypeDefinition[]) => {
        return data.filter(item => {
            const searchLower = searchText.toLowerCase();
            const matchesSearch = searchText === '' || (
                item.function_name.toLowerCase().includes(searchLower) ||
                item.description.toLowerCase().includes(searchLower)
            );
            const matchesTag = selectedTags.length === 0 || selectedTags.includes(item.tag);
            
            return matchesSearch && matchesTag;
        });
    };

    const columns = [
        {
            title: 'Function Name',
            dataIndex: 'function_name',
            key: 'function_name',
            sorter: (a: TypeDefinition, b: TypeDefinition) => 
                a.function_name.localeCompare(b.function_name)
        },
        {
            title: 'Description',
            dataIndex: 'description',
            key: 'description'
        },
        {
            title: 'Tag',
            dataIndex: 'tag',
            key: 'tag',
            render: (tag: string) => <Tag>{tag}</Tag>
        },
        {
            title: 'Properties',
            key: 'properties',
            render: (text: string, record: TypeDefinition) => 
                Object.keys(record.args).length
        }
    ];

    const filteredData = filterData(data);

    const renderContent = () => {
        if (loading) return <Spin />;

        return (
            <div style={{ width: '100%'  }}>
                <Space direction="vertical" style={{ width: '100%', marginBottom: 16 }}>
                    <div style={{ 
                        display: 'flex', 
                        gap: 16, 
                        flexWrap: 'wrap',
                        width: '100%'
                    }}>
                        <Search
                            placeholder="Search types..."
                            allowClear
                            style={{ width: '100%', maxWidth: 300 }}
                            onChange={(e) => setSearchText(e.target.value)}
                        />
                        <Select
                            mode="multiple"
                            placeholder="Filter by Tag"
                            style={{ minWidth: 200, flex: 1 }}
                            onChange={setSelectedTags}
                            options={uniqueTags.map(tag => ({ label: tag, value: tag }))}
                        />
                    </div>
                </Space>

                {viewMode === 'card' ? (
                    <div>
                        {filteredData.map(type => (
                            <div id={`type-${type.function_name}`} key={type.function_name}>
                                <TypeCard type={type} />
                            </div>
                        ))}
                    </div>
                ) : (
                    <Table 
                        dataSource={filteredData} 
                        columns={columns} 
                        rowKey="function_name"
                        pagination={{ pageSize: 10 }}
                    />
                )}
            </div>
        );
    };

    return (
        <Layout style={{ minHeight: '100vh' }}>
            <Content style={{ padding: '24px' }}>
                <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 16 }}>
                    <Space>
                        <AppstoreOutlined style={{ opacity: viewMode === 'card' ? 1 : 0.5 }} />
                        <Switch
                            checked={viewMode === 'table'}
                            onChange={(checked) => setViewMode(checked ? 'table' : 'card')}
                        />
                        <TableOutlined style={{ opacity: viewMode === 'table' ? 1 : 0.5 }} />
                    </Space>
                </div>
                {renderContent()}
            </Content>
        </Layout>
    );
};

export default Types;