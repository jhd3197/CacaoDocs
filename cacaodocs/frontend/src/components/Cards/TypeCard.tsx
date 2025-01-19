import React, { useState } from 'react';
import { Card, Tag, Space, Typography, List, Button } from 'antd';

const { Title, Text } = Typography;

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

interface TypeCardProps {
    type: TypeDefinition;
}

const TypeCard: React.FC<TypeCardProps> = ({ type }) => {
    const [expanded, setExpanded] = useState(false);
    const args = Object.entries(type.args);
    const hasMany = args.length > 6;

    // Get sorted arguments
    const sortedArgs = args.sort(([a], [b]) => a.localeCompare(b));
    const visibleArgs = expanded ? sortedArgs : sortedArgs.slice(0, 6);

    const handleShowMore = (e: React.MouseEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setExpanded(!expanded);
    };

    return (
        <Card 
            title={
                <Space direction="vertical" style={{ width: '100%' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Title level={4} style={{ margin: 0, marginTop:'10px' }}>{type.function_name}</Title>
                        <Tag color="blue">{type.tag}</Tag>
                    </div>
                    <Text type="secondary">{type.description}</Text>
                </Space>
            }
            style={{ margin: '0px 0px 25px 0px' }}
            bodyStyle={{ padding: '12px 24px 15px 24px' }}
            headStyle={{ padding: '0 24px 5px 24px' }}
        >
            <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
                <List
                    dataSource={visibleArgs}
                    renderItem={([key, value]) => (
                        <List.Item key={key}>
                            <List.Item.Meta
                                title={key}
                                description={value.description}
                            />
                            <Tag color={value.color} style={{ fontSize: '15px', padding: '5px 15px' }}>
                                <span>{value.emoji}</span>  {value.type}
                            </Tag>
                        </List.Item>
                    )}
                />

                {hasMany && (
                    <Button 
                        type="link" 
                        onClick={handleShowMore}
                        style={{ alignSelf: 'flex-start', padding: 0 }}
                    >
                        {expanded ? 'Show Less' : `Show More (${args.length - 6} more)`}
                    </Button>
                )}
            </div>
        </Card>
    );
};

export default TypeCard;
