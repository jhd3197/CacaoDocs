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

const TypeCard: React.FC<{ type: TypeDefinition }> = ({ type }) => {
    const [expanded, setExpanded] = useState(Object.keys(type.args).length <= 6);
    const hasMany = Object.keys(type.args).length > 6;

    return (
        <Card 
            hoverable
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
                    dataSource={Object.entries(type.args).sort(([a], [b]) => a.localeCompare(b))}
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
                        onClick={() => setExpanded(!expanded)}
                        style={{ alignSelf: 'flex-start' }}
                    ></Button>
                )}

                {!expanded && hasMany && (
                    <div style={{
                        position: 'relative',
                        height: '50px',
                        marginTop: '-50px',
                        background: 'linear-gradient(transparent, white)'
                    }}/>
                )}
            </div>
        </Card>
    );
};

export default TypeCard;
