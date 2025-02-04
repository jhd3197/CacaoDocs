import React, { useEffect, useState, useCallback } from 'react';
import { Table, Spin, Tag, Card, Switch, Space, Input, Select, Typography, Tabs, Layout } from 'antd';
import { TableOutlined, AppstoreOutlined, SearchOutlined } from '@ant-design/icons';
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter';
import json from 'react-syntax-highlighter/dist/esm/languages/hljs/json';
import { atomOneDark } from 'react-syntax-highlighter/dist/esm/styles/hljs';
import { useLocation, useNavigate } from 'react-router-dom';
import type { AppData } from '../../global';
import ApiCard from '../Cards/ApiCard';

const { Title } = Typography;
const { Search } = Input;
const { TabPane } = Tabs;
const { Content } = Layout;

SyntaxHighlighter.registerLanguage('json', json);

interface ApiProps {
  data: AppData;
}

const Api: React.FC<ApiProps> = ({ data }) => {
  const [loading, setLoading] = useState(true);
  const [selectedEndpoint, setSelectedEndpoint] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'card' | 'table'>('card');
  const [searchText, setSearchText] = useState('');
  const [selectedMethods, setSelectedMethods] = useState<string[]>([]);
  const [selectedVersions, setSelectedVersions] = useState<string[]>([]);
  const [selectedResponseCodes, setSelectedResponseCodes] = useState<string[]>([]);
  const [selectedStatuses, setSelectedStatuses] = useState<string[]>([]);

  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    if (data && data.api) {
      setLoading(false);
    }
  }, [data]);

  const scrollToElement = useCallback((hash: string) => {
    const cleanHash = decodeURIComponent(hash.replace(/^#\/api#|^#\/api|^#/, ''));
    console.log('Attempting to scroll to:', cleanHash);

    const findAndScroll = (retries = 5) => {
      const element = document.getElementById(cleanHash);
      console.log('Found element:', element);
      
      if (element) {
        setTimeout(() => {
          element.scrollIntoView({ behavior: 'smooth', block: 'center' });
          element.style.backgroundColor = 'rgba(255, 140, 0, 0.1)';
          element.style.transition = 'background-color 1s ease';
          setTimeout(() => {
            element.style.backgroundColor = 'transparent';
          }, 2000);
        }, 150);
      } else if (retries > 0) {
        setTimeout(() => findAndScroll(retries - 1), 200);
      }
    };

    findAndScroll();
  }, []);

  useEffect(() => {
    if (!loading && data?.api) {
      const handleNavigation = (event?: CustomEvent) => {
        const hash = event?.detail?.hash || location.hash;
        if (hash) {
          scrollToElement(hash);
        }
      };

      window.addEventListener('navigationRequest' as any, handleNavigation);
      
      if (location.hash) {
        handleNavigation();
      }

      return () => {
        window.removeEventListener('navigationRequest' as any, handleNavigation);
      };
    }
  }, [loading, data, location.hash, scrollToElement]);

  const handleEndpointSelect = (endpoint: string) => {
    const hash = `/api/${endpoint}`;
    navigate(`#${hash}`, { replace: true });
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
      render: (status: string) => {
        const statusColors: Record<string, string> = {
          'Production': 'green',
          'In Review': 'orange',
          'Planned': 'purple'
        };
        return <Tag color={statusColors[status] || 'default'}>{status}</Tag>;
      },
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

  const uniqueMethods = Array.isArray(data.api)
    ? Array.from(new Set(data.api.map((item) => item.method)))
    : [];
  const uniqueVersions = Array.isArray(data.api)
    ? Array.from(new Set(data.api.map((item) => item.version)))
    : [];
  const uniqueResponseCodes = Array.isArray(data.api)
    ? Array.from(
        new Set(
          data.api.flatMap((item) => (item.responses ? Object.keys(item.responses) : []))
        )
      )
    : [];
  const uniqueStatuses = Array.isArray(data.api)
    ? Array.from(new Set(data.api.map((item) => item.status)))
    : [];

  const filterData = (items: typeof data.api) => {
    if (!Array.isArray(items)) return [];
    
    return items.filter((item) => {
      const searchLower = searchText.toLowerCase();
      const matchesSearch =
        !searchText ||
        item.endpoint.toLowerCase().includes(searchLower) ||
        item.description.toLowerCase().includes(searchLower) ||
        item.function_name.toLowerCase().includes(searchLower) ||
        item.method.toLowerCase().includes(searchLower);

      const matchesMethod =
        selectedMethods.length === 0 || selectedMethods.includes(item.method);

      const matchesVersion =
        selectedVersions.length === 0 || selectedVersions.includes(item.version);

      const matchesStatus =
        selectedStatuses.length === 0 || selectedStatuses.includes(item.status);

      const matchesResponse =
        selectedResponseCodes.length === 0 ||
        (item.responses &&
          Object.keys(item.responses).some((code) =>
            selectedResponseCodes.includes(code)
          ));

      return (
        matchesSearch &&
        matchesMethod &&
        matchesVersion &&
        matchesStatus &&
        matchesResponse
      );
    });
  };

  const filteredData = React.useMemo(() => {
    const baseData = selectedEndpoint
      ? data?.api?.filter((item) => item.endpoint === selectedEndpoint)
      : data?.api;
    return filterData(baseData || []);
  }, [data, selectedEndpoint, searchText, selectedMethods, selectedVersions, selectedStatuses, selectedResponseCodes]);

  const renderContent = () => {
    if (loading) return <Spin size="large" />;

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
            <Select
              mode="multiple"
              placeholder="Filter by Status"
              style={{ minWidth: 200 }}
              onChange={setSelectedStatuses}
              options={uniqueStatuses.map((status) => ({
                label: status,
                value: status,
              }))}
            />
          </div>
        </Space>

        {viewMode === 'card' ? (
          <div>
            {filteredData.map((endpoint) => {
              const elementId = `${endpoint.endpoint}-${endpoint.method}`;
              return (
                <div 
                  id={elementId}
                  key={elementId}
                  style={{ 
                    transition: 'background-color 1s ease',
                    scrollMarginTop: '80px',
                    marginBottom: '20px',
                    scrollBehavior: 'smooth'
                  }}
                >
                  <ApiCard endpoint={endpoint} types={data.types} config={data.config} />
                </div>
              );
            })}
          </div>
        ) : (
          <Table
            dataSource={filteredData}
            columns={columns}
            rowKey={(record) => `${record.endpoint}-${record.method}-${record.version}`}
            pagination={{ pageSize: 10 }}
          />
        )}
      </div>
    );
  };

  return (
    <Layout style={{ minHeight: '100vh', background: data.config?.theme.bg_color || '#fff' }}>
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
