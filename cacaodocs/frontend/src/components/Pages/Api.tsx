import React, { useEffect, useState } from 'react';
import { Table, Spin, Tag, Card, Switch, Space, Input, Select, Typography, Tabs, Layout } from 'antd';
import { TableOutlined, AppstoreOutlined, SearchOutlined } from '@ant-design/icons';
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter';
import json from 'react-syntax-highlighter/dist/esm/languages/hljs/json';
import { atomOneDark } from 'react-syntax-highlighter/dist/esm/styles/hljs';
import localData from '../../data/localData.json';

const { Title } = Typography;
const { Search } = Input;
const { TabPane } = Tabs;
const { Content } = Layout;

interface ResponseDetail {
    code: string;
    description: string;
    example?: object; // Added example field
}

interface ApiEndpoint {
    endpoint: string;
    method: string;
    description: string;
    status: string;
    function_name: string;
    version: string;
    tag: string;
    responses?: ResponseDetail[]; // Made responses optional
}

SyntaxHighlighter.registerLanguage('json', json);

const Api: React.FC = () => {
    const [data, setData] = useState<ApiEndpoint[]>([]);
    const [loading, setLoading] = useState(true);
    const [selectedEndpoint, setSelectedEndpoint] = useState<string | null>(null);
    const [viewMode, setViewMode] = useState<'card' | 'table'>('card');
    const [searchText, setSearchText] = useState('');
    const [selectedMethods, setSelectedMethods] = useState<string[]>([]);
    const [selectedVersions, setSelectedVersions] = useState<string[]>([]);
    const [selectedResponseCodes, setSelectedResponseCodes] = useState<string[]>([]); // Added state for response codes

    useEffect(() => {
        setData(localData.api);
        setLoading(false);
    }, []);

    const handleEndpointSelect = (endpoint: string) => {
        const element = document.getElementById(`api-${endpoint}`);
        if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    };

    const methodColors: Record<string, string> = {
        GET: 'green',
        POST: '#331201',   // Changed from 'blue' to brown
        PUT: 'orange',
        DELETE: 'red',
        PATCH: 'purple'
    };

    const columns = [
        {
            title: 'Method',
            dataIndex: 'method',
            key: 'method',
            render: (method: string) => (
                <Tag color={methodColors[method]}>{method}</Tag>
            )
        },
        {
            title: 'Endpoint',
            dataIndex: 'endpoint',
            key: 'endpoint',
            render: (endpoint: string) => (
                <Typography.Text copyable>
                    {endpoint}
                </Typography.Text>
            )
        },
        {
            title: 'Description',
            dataIndex: 'description',
            key: 'description'
        },
        {
            title: 'Status',
            dataIndex: 'status',
            key: 'status',
            render: (status: string) => (
                <Tag color={status === 'Production' ? 'green' : 'orange'}>{status}</Tag>
            )
        },
        {
            title: 'Version',
            dataIndex: 'version',
            key: 'version'
        },
        {
            title: 'Tag',
            dataIndex: 'tag',
            key: 'tag',
            render: (tag: string) => <Tag>{tag}</Tag>
        }
    ];

    const uniqueMethods = Array.from(new Set(data.map(item => item.method)));
    const uniqueVersions = Array.from(new Set(data.map(item => item.version)));
    const uniqueResponseCodes = Array.from(new Set(data.flatMap(item => item.responses ? item.responses.map(response => response.code) : []))); // Extract unique response codes

    const filterData = (data: ApiEndpoint[]) => {
        return data.filter(item => {
            const searchLower = searchText.toLowerCase();
            const matchesSearch = searchText === '' || (
                (item.endpoint).toLowerCase().includes(searchLower) ||
                item.description.toLowerCase().includes(searchLower) ||
                item.function_name.toLowerCase().includes(searchLower) ||
                item.method.toLowerCase().includes(searchLower)
            );
            const matchesMethod = selectedMethods.length === 0 || 
                selectedMethods.includes(item.method);
            const matchesVersion = selectedVersions.length === 0 || 
                selectedVersions.includes(item.version);
            const matchesResponse = selectedResponseCodes.length === 0 || 
                (item.responses && item.responses.some(response => selectedResponseCodes.includes(response.code)));
            
            return matchesSearch && matchesMethod && matchesVersion && matchesResponse;
        });
    };

    const ApiCard: React.FC<{ endpoint: ApiEndpoint }> = ({ endpoint }) => (
        <Card 
            hoverable
            title={
                <Space direction="vertical" style={{ width: '100%' }}>
                    <Space>
                        <Tag color={methodColors[endpoint.method]} style={{ minWidth: '60px', textAlign: 'center' }}>
                            {endpoint.method}
                        </Tag>
                        <Title level={5} style={{ margin: 0 }}>{endpoint.endpoint}</Title>
                    </Space>
                </Space>
            }
            style={{ marginBottom: 25 }}
            bodyStyle={{ padding: '12x 24px 5px 24px' }} // Updated padding here
        >
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                <Typography.Paragraph>{endpoint.description}</Typography.Paragraph>
                <Space wrap>
                    <Tag color={endpoint.status === 'Production' ? 'green' : 'orange'}>
                        {endpoint.status}
                    </Tag>
                    <Tag color="blue">{endpoint.version}</Tag>
                    <Tag>{endpoint.tag}</Tag>
                </Space>
                {endpoint.responses && (
                    <Table
                        columns={[
                            { title: 'Code', dataIndex: 'code', key: 'code' },
                            { title: 'Description', dataIndex: 'description', key: 'description' }
                        ]}
                        dataSource={endpoint.responses}
                        pagination={false}
                        rowKey="code"
                    />
                )}
            </div>
        </Card>
    );

    const filteredData = filterData(selectedEndpoint ? data.filter(item => item.endpoint === selectedEndpoint) : data);

    const renderContent = () => {
        if (loading) return <Spin />;

        return (
            <div style={{ width: '100%' }}>
                <Space direction="vertical" style={{ width: '100%', marginBottom: 16 }}>
                    <div style={{ display: 'flex', gap: 16, flexWrap: 'wrap' }}>
                        <Search
                            placeholder="Search endpoints..."
                            allowClear
                            style={{ width: 300 }}
                            onChange={(e) => setSearchText(e.target.value)}
                        />
                        <Select
                            mode="multiple"
                            placeholder="Filter by Method"
                            style={{ minWidth: 200 }}
                            onChange={setSelectedMethods}
                            options={uniqueMethods.map(method => ({ label: method, value: method }))}
                        />
                        <Select
                            mode="multiple"
                            placeholder="Filter by Version"
                            style={{ minWidth: 200 }}
                            onChange={setSelectedVersions}
                            options={uniqueVersions.map(version => ({ label: version, value: version }))}
                        />
                        <Select
                            mode="multiple"
                            placeholder="Filter by Response Code"
                            style={{ minWidth: 200 }}
                            onChange={setSelectedResponseCodes}
                            options={uniqueResponseCodes.map(code => ({ label: code, value: code }))}
                        />
                    </div>
                </Space>

                {viewMode === 'card' ? (
                    <div>
                        {filteredData.map(endpoint => (
                            <div id={`api-${endpoint.endpoint}`} key={endpoint.endpoint}>
                                <ApiCard endpoint={endpoint} />
                            </div>
                        ))}
                    </div>
                ) : (
                    <Table 
                        dataSource={filteredData} 
                        columns={columns} 
                        rowKey="endpoint"
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

export default Api;