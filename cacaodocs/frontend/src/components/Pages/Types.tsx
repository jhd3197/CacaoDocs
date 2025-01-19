import React, { useEffect, useState } from 'react';
import { Table, Spin, Tag, Layout, Switch, Space, Input, Select, Button } from 'antd';
import { TableOutlined, AppstoreOutlined } from '@ant-design/icons';
import { useLocation } from 'react-router-dom';
import TypeCard from '../Cards/TypeCard';
import ERDiagramView from './ERDiagramView';
import type { AppData, TypeItem } from '../../global';

const { Content } = Layout;
const { Search } = Input;

interface TypesProps {
  data: AppData;
}

const Types: React.FC<TypesProps> = ({ data }) => {
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'card' | 'table' | 'er'>('card');
  const [searchText, setSearchText] = useState('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [typesData, setTypesData] = useState<TypeItem[]>([]);
  const location = useLocation();

  useEffect(() => {
    if (data && data.types) {
      setTypesData(data.types);
      setLoading(false);

      // Get hash and remove the initial "/types" part if present
      const hash = decodeURIComponent(location.hash)
        .replace('#/types#', '')
        .replace('#', '');

      if (hash) {
        // Wait for component to fully render
        const scrollToElement = () => {
          const element = document.getElementById(`type-${hash}`);
          if (element) {
            element.scrollIntoView({ behavior: 'smooth', block: 'start' });
            // Add a highlight effect
            element.style.backgroundColor = 'rgba(255, 140, 0, 0.1)'; // Light orange highlight
            setTimeout(() => {
              element.style.transition = 'background-color 0.5s ease';
              element.style.backgroundColor = 'transparent';
            }, 1000);
          }
        };

        // Try multiple times in case of dynamic content loading
        setTimeout(scrollToElement, 100);
        setTimeout(scrollToElement, 500);
        setTimeout(scrollToElement, 1000);
      }
    }
  }, [data, location.hash]);

  const handleTypeSelect = (typeName: string) => {
    const element = document.getElementById(`type-${typeName}`);
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' });
      // Removed URL update to prevent route change
      // window.history.replaceState(null, '', `#/types#${encodedTypeName}`);
    }
  };

  // Optional: If you need a type definition generator
  // or any additional transformations, you can do so below.
  // For example, generating a type interface string:
  const generateTypeDefinition = (type: TypeItem): string => {
    const sortedProperties = Object.entries(type.args)
      .sort(([a], [b]) => a.localeCompare(b))
      .map(([key, value]) => {
        let typeStr = value.type;
        // Convert List[...] to T[] notation
        if (typeStr.startsWith('List[')) {
          typeStr = `${typeStr.slice(5, -1)}[]`;
        }
        return `    ${key}: ${typeStr};`;
      })
      .join('\n');

    return `interface ${type.function_name} {\n${sortedProperties}\n}`;
  };

  // Gather all unique tags for filtering
  const uniqueTags = Array.from(new Set(typesData.map(item => item.tag)));

  // Filtering logic
  const filterData = (items: TypeItem[]) => {
    return items.filter(item => {
      const searchLower = searchText.toLowerCase();
      const matchesSearch =
        searchText === '' ||
        item.function_name.toLowerCase().includes(searchLower) ||
        item.description.toLowerCase().includes(searchLower);

      const matchesTag =
        selectedTags.length === 0 || selectedTags.includes(item.tag);

      return matchesSearch && matchesTag;
    });
  };

  // Table columns definition
  const columns = [
    {
      title: 'Function Name',
      dataIndex: 'function_name',
      key: 'function_name',
      sorter: (a: TypeItem, b: TypeItem) =>
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
      render: (text: string, record: TypeItem) =>
        Object.keys(record.args).length
    }
  ];

  const filteredData = filterData(typesData);

  // Render main content
  const renderContent = () => {
    if (loading) {
      return <Spin />;
    }
    if (viewMode === 'er') {
      return <ERDiagramView typesData={typesData} />;
    }

    return (
      <div style={{ width: '100%' }}>
        {/* Filter Section */}
        <Space direction="vertical" style={{ width: '100%', marginBottom: 16 }}>
          <div
            style={{
              display: 'flex',
              gap: 16,
              flexWrap: 'wrap',
              width: '100%'
            }}
          >
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

        {/* Content in card or table form */}
        {viewMode === 'card' ? (
          <div>
            {filteredData.map(type => (
              <div 
                id={`type-${type.function_name}`} 
                key={type.function_name}
                style={{ transition: 'background-color 0.5s ease' }}
              >
                <TypeCard 
                  type={type} 
                />
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
    <Layout style={{ minHeight: '100vh', background: data.config?.theme.bg_color || '#fff' }}>
      <Content style={{ padding: '24px' }}>
        {/* Toggle: Table or Card View */}
        <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: 16 }}>
          <Space>
            <AppstoreOutlined style={{ opacity: viewMode === 'card' ? 1 : 0.5 }} />
            <Switch
              checked={viewMode === 'table'}
              onChange={(checked) => setViewMode(checked ? 'table' : 'card')}
            />
            <TableOutlined style={{ opacity: viewMode === 'table' ? 1 : 0.5 }} />
            {/* Add a button or toggle for ER mode */}
            <Button onClick={() => setViewMode(viewMode === 'er' ? 'card' : 'er')}>
              Toggle ER Diagram
            </Button>
          </Space>
        </div>
        {renderContent()}
      </Content>
    </Layout>
  );
};

export default Types;
