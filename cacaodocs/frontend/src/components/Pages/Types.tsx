import React, { useEffect, useState } from 'react';
import { Table, Spin, Tag, Layout, Switch, Space, Input, Select } from 'antd';
import { TableOutlined, AppstoreOutlined } from '@ant-design/icons';
import TypeCard from './TypeCard';
import { TypeItem } from '../../global';

const { Content } = Layout;
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

interface TypesProps {
  data: TypeItem[];
}

const Types: React.FC<TypesProps> = ({ data }) => {
  const [loading, setLoading] = useState(true);
  const [viewMode, setViewMode] = useState<'card' | 'table'>('card');
  const [searchText, setSearchText] = useState('');
  const [selectedTags, setSelectedTags] = useState<string[]>([]);
  const [typesData, setTypesData] = useState<TypeDefinition[]>([]);

  /**
   * Instead of fetching from a server, we mimic the Docs.tsx approach:
   * directly take the "data" prop passed in and set it to local state.
   */
  useEffect(() => {
    // If your incoming `data` is already shaped as needed,
    // simply set it and stop loading.
    setTypesData(data as unknown as TypeDefinition[]);
    setLoading(false);
  }, [data]);

  // Optional: If you need a type definition generator
  // or any additional transformations, you can do so below.
  // For example, generating a type interface string:
  const generateTypeDefinition = (type: TypeDefinition): string => {
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
  const filterData = (items: TypeDefinition[]) => {
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

  const filteredData = filterData(typesData);

  // Render main content
  const renderContent = () => {
    if (loading) {
      return <Spin />;
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
        {/* Toggle: Table or Card View */}
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
