import React, { useEffect, useState } from 'react';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import { ConfigProvider, Spin } from 'antd';
import CustomLayout from './components/Layout/Layout';
import Home from './components/Pages/Home';
import Api from './components/Pages/Api';
import Types from './components/Pages/Types';
import Docs from './components/Pages/Docs';

import type { AppData } from './global';

// Define a valid defaultConfig
const defaultConfig = {
  description: '',
  exclude_inputs: [],
  logo_url: '',
  tag_mappings: {},
  theme: {
    primary_color: '#FF8C00',
    secondary_color: '#0D47A1',
    bg_color: '#f0f4f8',
    text_color: '#1a202c',
    highlight_code_bg_color: '#ffe0b2',
    highlight_code_border_color: '#ff8c00',
    sidebar_bg_color: '#ffffff',
    sidebar_text_color: '#1a202c',
    sidebar_highlight_bg_color: '#0D47A1',
    sidebar_highlight_text_color: '#ffffff',
    secondary_sidebar_bg_color: '#e0e7ff',
    secondary_sidebar_text_color: '#1a202c',
    secondary_sidebar_highlight_bg_color: '#0D47A1',
    secondary_sidebar_highlight_text_color: '#ffffff',
    home_page_welcome_bg_1: '#FF8C00',
    home_page_welcome_bg_2: '#FFD580',
    home_page_welcome_text_color: '#ffffff',
    home_page_card_bg_color: '#ffffff',
    home_page_card_text_color: '#1a202c',
    code_bg_color: '#f0f4f8',
    type_bg_color_1: '#f0f4f8',
    type_bg_color_2: '#e0e7ff',
    type_text_color: '#1a202c',
  },
  title: 'Default title',
  type_mappings: {},
  verbose: false,
  version: '0.0.0',
};

const App: React.FC = () => {
  const [apiData, setApiData] = useState<AppData>({ 
    api: [], 
    docs: [], 
    types: [], 
    config: defaultConfig
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (process.env.NODE_ENV === 'development') {
      const fetchDevData = async () => {
        try {
          const response = await fetch('http://localhost:5000/docs');
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          const jsonData = await response.json();
          const transformedData = {
            api: Array.isArray(jsonData.api) ? jsonData.api : (jsonData.api ? [jsonData.api] : []),
            docs: Array.isArray(jsonData.docs) ? jsonData.docs : (jsonData.docs ? [jsonData.docs] : []),
            types: Array.isArray(jsonData.types) ? jsonData.types : (jsonData.types ? [jsonData.types] : []),
            config: jsonData.configs || defaultConfig
          };
          setApiData(transformedData);
        } catch (error) {
          console.error('Error fetching dev data:', error);
          setApiData({
            api: [],
            docs: [],
            types: [],
            config: defaultConfig
          });
        } finally {
          setLoading(false);
        }
      };
      fetchDevData();
    } else {
      // Production mode
      const globalData = (window as any).globalData;
      if (globalData) {
        const transformedData = {
          api: Array.isArray(globalData.api) ? globalData.api : [],
          docs: Array.isArray(globalData.docs) ? globalData.docs : [],
          types: Array.isArray(globalData.types) ? globalData.types : [],
          config: globalData.configs || defaultConfig
        };
        setApiData(transformedData);
      }
      setLoading(false);
    }
  }, []);

  // While fetching data (development) or setting up state
  if (loading || !apiData) {
    return (
      <div style={{ textAlign: 'center', marginTop: 80 }}>
        <Spin tip="Loading data..." />
      </div>
    );
  }

  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: apiData?.config?.theme?.primary_color || '#331201',
          colorTextHeading: apiData?.config?.theme?.primary_color || '#331201',
          colorLink: apiData?.config?.theme?.primary_color || '#331201',
        },
        components: {
          Typography: {
            titleMarginTop: 0,
            titleMarginBottom: 0,
            colorTextHeading: apiData?.config?.theme?.primary_color || '#331201',
          },
          Menu: {
            colorItemTextHover: apiData?.config?.theme?.sidebar_highlight_text_color || '#fff',
            colorItemTextSelected: '#fff',
            itemHoverBg: apiData?.config?.theme?.sidebar_highlight_bg_color || '#331201',
            colorItemBgSelected: apiData?.config?.theme?.sidebar_highlight_bg_color || '#331201',
          },
        },
      }}
    >
      <Router>
        <CustomLayout apiData={apiData}>
          <Routes>
            <Route path="/" element={<Home data={apiData} />} />
            <Route path="/api" element={<Api data={apiData} />} />
            <Route path="/types" element={<Types data={apiData} />} />
            <Route path="/docs" element={<Docs data={apiData}/>} />
          </Routes>
        </CustomLayout>
      </Router>
    </ConfigProvider>
  );
};

export default App;
