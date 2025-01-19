import React, { useEffect, useState } from 'react';
import {
  Table,
  Spin,
  Tag,
  Layout,
  Card,
  Switch,
  Space,
  Input,
  Select,
  Typography,
  Tabs
} from 'antd';
import {
  TableOutlined,
  AppstoreOutlined
} from '@ant-design/icons';
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter';
import json from 'react-syntax-highlighter/dist/esm/languages/hljs/json';
import { atomOneDark } from 'react-syntax-highlighter/dist/esm/styles/hljs';
import DocCard from '../Cards/DocCard';
import type { AppData, DocItem } from '../../global';

const { Content } = Layout;
const { Title, Text } = Typography;
const { Search } = Input;
const { TabPane } = Tabs;

SyntaxHighlighter.registerLanguage('json', json);

interface DocsProps {
  data: AppData;
}

const Docs: React.FC<DocsProps> = ({ data }) => {
  const [docsData, setDocsData] = useState<DocItem[]>([]);
  const [loading, setLoading] = useState(true);

  // View mode: card or table
  const [viewMode, setViewMode] = useState<'card' | 'table'>('card');

  // Filters
  const [searchText, setSearchText] = useState('');
  const [selectedMethods, setSelectedMethods] = useState<string[]>([]);
  const [selectedVersions, setSelectedVersions] = useState<string[]>([]);
  const [selectedStatuses, setSelectedStatuses] = useState<string[]>([]);
  const [selectedTags, setSelectedTags] = useState<string[]>([]);

  // Add new state for highlighted doc
  const [highlightedDoc, setHighlightedDoc] = useState<string | null>(null);

  useEffect(() => {
    setDocsData(data.docs);
    setLoading(false);

    // Handle initial URL hash
    const fullHash = window.location.hash;
    const functionHash = fullHash.split('#').pop(); // Get the last part after #
    
    if (functionHash && functionHash !== 'docs') {
      // Add a longer delay to ensure the content is fully rendered
      setTimeout(() => {
        handleSelectDoc(functionHash);
      }, 100);
    }

    // Listen for hash changes
    const handleHashChange = () => {
      const newHash = window.location.hash.split('#').pop();
      if (newHash && newHash !== 'docs') {
        handleSelectDoc(newHash);
      }
    };

    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, [data]);

  // Update scroll and highlight functionality
  const handleSelectDoc = (functionName: string) => {
    const cleanFunctionName = functionName.replace(/[()]/g, ''); // Remove parentheses if present
    const element = document.getElementById(`doc-${cleanFunctionName}`);
    
    if (element) {
      // Add offset for any fixed headers
      const offset = 80; // Adjust this value based on your header height
      const elementPosition = element.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - offset;

      window.scrollTo({
        top: offsetPosition,
        behavior: 'smooth'
      });
      
      setHighlightedDoc(cleanFunctionName);
      
      // Update URL hash without triggering a new scroll
      const newHash = `#/docs#${cleanFunctionName}`;
      if (window.location.hash !== newHash) {
        window.history.pushState(null, '', newHash);
      }

      // Remove highlight after animation
      setTimeout(() => {
        setHighlightedDoc(null);
      }, 2000);
    }
  };

  // Prepare unique filter options
  const uniqueMethods = Array.from(
    new Set(docsData.map(item => item.method).filter(Boolean))
  );
  const uniqueVersions = Array.from(
    new Set(docsData.map(item => item.version).filter(Boolean))
  );
  const uniqueStatuses = Array.from(
    new Set(docsData.map(item => item.status).filter(Boolean))
  );
  const uniqueTags = Array.from(
    new Set(docsData.map(item => item.tag).filter(Boolean))
  );

  // Filtering logic
  const filterData = (allDocs: DocItem[]) => {
    return allDocs.filter(doc => {
      const searchLower = searchText.toLowerCase();
      const matchesSearch =
        !searchText ||
        doc.function_name.toLowerCase().includes(searchLower) ||
        doc.description?.toLowerCase().includes(searchLower) ||
        doc.method?.toLowerCase().includes(searchLower);

      const matchesMethod =
        selectedMethods.length === 0 || (doc.method && selectedMethods.includes(doc.method));

      const matchesVersion =
        selectedVersions.length === 0 || (doc.version && selectedVersions.includes(doc.version));

      const matchesStatus =
        selectedStatuses.length === 0 || (doc.status && selectedStatuses.includes(doc.status));

      const matchesTag =
        selectedTags.length === 0 || selectedTags.includes(doc.tag);

      return (
        matchesSearch &&
        matchesMethod &&
        matchesVersion &&
        matchesStatus &&
        matchesTag
      );
    });
  };

  // Table columns
  const columns = [
    {
      title: 'FunctionName',
      dataIndex: 'function_name',
      key: 'function_name',
      render: (name: string) => <Text copyable>{name}</Text>,
      sorter: (a: DocItem, b: DocItem) =>
        a.function_name.localeCompare(b.function_name)
    },
    {
      title: 'Method',
      dataIndex: 'method',
      key: 'method'
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
        <Tag color={status === 'Production' ? 'green' : 'orange'}>
          {status}
        </Tag>
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
      render: (tag: string) => <Tag color="blue">{tag}</Tag>
    }
  ];

  // Filter the data
  const filteredData = filterData(docsData);

  // Render main content
  const renderContent = () => {
    if (loading) {
      return <Spin />;
    }
    return (
      <div style={{ width: '100%' }}>
        {/* Filters */}
        <Space direction="vertical" style={{ width: '100%', marginBottom: 16 }}>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 16 }}>
            <Search
              placeholder="Search docs..."
              allowClear
              style={{ width: 300 }}
              onChange={(e) => setSearchText(e.target.value)}
            />
            <Select
              mode="multiple"
              allowClear
              placeholder="Filter by Method"
              style={{ minWidth: 150 }}
              onChange={setSelectedMethods}
              options={uniqueMethods.map(m => ({ label: m, value: m }))}
            />
            <Select
              mode="multiple"
              allowClear
              placeholder="Filter by Version"
              style={{ minWidth: 150 }}
              onChange={setSelectedVersions}
              options={uniqueVersions.map(ver => ({ label: ver, value: ver }))}
            />
            <Select
              mode="multiple"
              allowClear
              placeholder="Filter by Status"
              style={{ minWidth: 150 }}
              onChange={setSelectedStatuses}
              options={uniqueStatuses.map(st => ({ label: st, value: st }))}
            />
            <Select
              mode="multiple"
              allowClear
              placeholder="Filter by Tag"
              style={{ minWidth: 150 }}
              onChange={setSelectedTags}
              options={uniqueTags.map(t => ({ label: t, value: t }))}
            />
          </div>
        </Space>

        {/* Docs Display */}
        {viewMode === 'card' ? (
          <div>
            {filteredData.map(doc => (
              <div 
                id={`doc-${doc.function_name}`} 
                key={doc.function_name}
                style={{
                  transition: 'background-color 0.3s ease',
                  backgroundColor: highlightedDoc === doc.function_name ? '#ffecc7' : 'transparent',
                  padding: '8px',
                  borderRadius: '8px',
                }}
              >
                <DocCard doc={doc} types={data.types} />
              </div>
            ))}
          </div>
        ) : (
          <Table
            dataSource={filteredData}
            columns={columns}
            rowKey="function_name"
            pagination={{ pageSize: 8 }}
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

export default Docs;
