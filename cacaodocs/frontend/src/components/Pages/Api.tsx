import React, { useEffect, useState } from 'react';
import { Table, Spin, Tag, Card, Switch, Space, Input, Select, Typography, Tabs, Layout } from 'antd';
import { TableOutlined, AppstoreOutlined, SearchOutlined } from '@ant-design/icons';
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter';
import json from 'react-syntax-highlighter/dist/esm/languages/hljs/json';
import { atomOneDark } from 'react-syntax-highlighter/dist/esm/styles/hljs';
import { ApiEndpoint } from '../../global';
import ApiCard from '../Cards/ApiCard';

// ------------------ ADD THESE IMPORTS OR DEFINE YOUR OWN TypeDefinition INTERFACE ------------------ //
// For example, if your `TypeDefinition` interface is in the global file or somewhere else,
// adjust the import accordingly. It's the same shape used in Types.tsx
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

// ----------------------------------------------------------------------------------------------- //

const { Title } = Typography;
const { Search } = Input;
const { TabPane } = Tabs;
const { Content } = Layout;

SyntaxHighlighter.registerLanguage('json', json);

// ------------------ UPDATED PROPS TO ALSO RECEIVE `types` ------------------ //
interface ApiProps {
  data: ApiEndpoint[];
  types: TypeDefinition[];  // <--- New prop to pass type data
}

const Api: React.FC<ApiProps> = ({ data, types }) => {
  const [loading, setLoading] = useState(true);
  const [selectedEndpoint, setSelectedEndpoint] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'card' | 'table'>('card');
  const [searchText, setSearchText] = useState('');
  const [selectedMethods, setSelectedMethods] = useState<string[]>([]);
  const [selectedVersions, setSelectedVersions] = useState<string[]>([]);
  const [selectedResponseCodes, setSelectedResponseCodes] = useState<string[]>([]);

  useEffect(() => {
    console.log('Api component received data:', data);
    if (Array.isArray(data)) {
      setLoading(false);
    }
  }, [data]);

  const handleEndpointSelect = (endpoint: string) => {
    const element = document.getElementById(`api-${endpoint}`);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  const methodColors: Record<string, string> = {
    GET: 'green',
    POST: '#331201', // Changed from 'blue' to brown
    PUT: 'orange',
    DELETE: 'red',
    PATCH: 'purple',
  };

  const columns = [
    {
      title: 'Method',
      dataIndex: 'method',
      key: 'method',
      render: (method: string) => (
        <Tag color={methodColors[method]}>{method}</Tag>
      ),
    },
    {
      title: 'Endpoint',
      dataIndex: 'endpoint',
      key: 'endpoint',
      render: (endpoint: string) => (
        <Typography.Text copyable>{endpoint}</Typography.Text>
      ),
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: 'Status',
      dataIndex: 'status',
      key: 'status',
      render: (status: string) => (
        <Tag color={status === 'Production' ? 'green' : 'orange'}>{status}</Tag>
      ),
    },
    {
      title: 'Version',
      dataIndex: 'version',
      key: 'version',
    },
    {
      title: 'Tag',
      dataIndex: 'tag',
      key: 'tag',
      render: (tag: string) => <Tag>{tag}</Tag>,
    },
  ];

  // Ensure data is an array before extracting unique values
  const uniqueMethods = Array.isArray(data)
    ? Array.from(new Set(data.map((item) => item.method)))
    : [];
  const uniqueVersions = Array.isArray(data)
    ? Array.from(new Set(data.map((item) => item.version)))
    : [];
  const uniqueResponseCodes = Array.isArray(data)
    ? Array.from(
        new Set(
          data.flatMap((item) => (item.responses ? Object.keys(item.responses) : []))
        )
      )
    : [];

  const filterData = (items: ApiEndpoint[]) => {
    if (!Array.isArray(items)) return [];
    return items.filter((item) => {
      const searchLower = searchText.toLowerCase();
      const matchesSearch =
        searchText === '' ||
        item.endpoint.toLowerCase().includes(searchLower) ||
        item.description.toLowerCase().includes(searchLower) ||
        item.function_name.toLowerCase().includes(searchLower) ||
        item.method.toLowerCase().includes(searchLower);

      const matchesMethod =
        selectedMethods.length === 0 || selectedMethods.includes(item.method);

      const matchesVersion =
        selectedVersions.length === 0 || selectedVersions.includes(item.version);

      const matchesResponse =
        selectedResponseCodes.length === 0 ||
        (item.responses &&
          Object.keys(item.responses).some((code) =>
            selectedResponseCodes.includes(code)
          ));

      return matchesSearch && matchesMethod && matchesVersion && matchesResponse;
    });
  };

  const filteredData = filterData(
    selectedEndpoint
      ? Array.isArray(data)
        ? data.filter((item) => item.endpoint === selectedEndpoint)
        : []
      : Array.isArray(data)
      ? data
      : []
  );

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
              options={uniqueMethods.map((method) => ({
                label: method,
                value: method,
              }))}
            />
            <Select
              mode="multiple"
              placeholder="Filter by Version"
              style={{ minWidth: 200 }}
              onChange={setSelectedVersions}
              options={uniqueVersions.map((version) => ({
                label: version,
                value: version,
              }))}
            />
            <Select
              mode="multiple"
              placeholder="Filter by Response Code"
              style={{ minWidth: 200 }}
              onChange={setSelectedResponseCodes}
              options={uniqueResponseCodes.map((code) => ({
                label: code,
                value: code,
              }))}
            />
          </div>
        </Space>

        {viewMode === 'card' ? (
          <div>
            {filteredData.map((endpoint) => (
              <div id={`api-${endpoint.endpoint}`} key={endpoint.endpoint}>
                {/* ---------------- PASS TYPES DOWN HERE ---------------- */}
                <ApiCard endpoint={endpoint} types={types} />
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
