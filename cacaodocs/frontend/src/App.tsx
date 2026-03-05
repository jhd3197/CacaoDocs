import React, { useEffect, useState } from 'react';
import { HashRouter as Router, Routes, Route } from 'react-router-dom';
import { ConfigProvider, Spin } from 'antd';
import CustomLayout from './components/Layout/Layout';
import Home from './components/Pages/Home';
import Modules from './components/Pages/Modules';
import ModuleDetail from './components/Pages/ModuleDetail';
import Classes from './components/Pages/Classes';
import ClassDetail from './components/Pages/ClassDetail';
import Functions from './components/Pages/Functions';
import Pages from './components/Pages/Pages';
import PageDetail from './components/Pages/PageDetail';
import GoogleAnalytics from './components/GoogleAnalytics';
import Clarity from './components/Clarity';
import GlobalSearch from './components/Search/GlobalSearch';

import type { AppData } from './global';

// Define a valid defaultConfig
const defaultConfig = {
  title: 'Documentation',
  description: 'API and module documentation',
  version: '1.0.0',
  logo_url: '',
  github_url: '',
  footer_text: '',
  google_analytics_id: '',
  clarity_id: '',
  theme: {
    primary_color: '#8B4513',
    secondary_color: '#D2691E',
    bg_color: '#faf8f5',
    text_color: '#1a202c',
    highlight_code_bg_color: '#fff8f0',
    highlight_code_border_color: '#8B4513',
    sidebar_bg_color: '#ffffff',
    sidebar_text_color: '#1a202c',
    sidebar_highlight_bg_color: '#8B4513',
    sidebar_highlight_text_color: '#ffffff',
    secondary_sidebar_bg_color: '#f5f0eb',
    secondary_sidebar_text_color: '#1a202c',
    secondary_sidebar_highlight_bg_color: '#8B4513',
    secondary_sidebar_highlight_text_color: '#ffffff',
    home_page_welcome_bg_1: '#8B4513',
    home_page_welcome_bg_2: '#D2691E',
    home_page_welcome_text_color: '#ffffff',
    home_page_card_bg_color: '#ffffff',
    home_page_card_text_color: '#1a202c',
    code_bg_color: '#f5f0eb',
  },
};

const App: React.FC = () => {
  const [apiData, setApiData] = useState<AppData>({
    modules: [],
    classes: [],
    functions: [],
    pages: [],
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
          const transformedData: AppData = {
            modules: Array.isArray(jsonData.modules) ? jsonData.modules : [],
            classes: Array.isArray(jsonData.classes) ? jsonData.classes : [],
            functions: Array.isArray(jsonData.functions) ? jsonData.functions : [],
            pages: Array.isArray(jsonData.pages) ? jsonData.pages : [],
            config: jsonData.config || jsonData.configs || defaultConfig
          };
          setApiData(transformedData);
        } catch (error) {
          console.error('Error fetching dev data:', error);
          setApiData({
            modules: [],
            classes: [],
            functions: [],
            pages: [],
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
        const transformedData: AppData = {
          modules: Array.isArray(globalData.modules) ? globalData.modules : [],
          classes: Array.isArray(globalData.classes) ? globalData.classes : [],
          functions: Array.isArray(globalData.functions) ? globalData.functions : [],
          pages: Array.isArray(globalData.pages) ? globalData.pages : [],
          config: globalData.config || globalData.configs || defaultConfig
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
          colorPrimary: apiData?.config?.theme?.primary_color || '#8B4513',
          colorTextHeading: apiData?.config?.theme?.primary_color || '#8B4513',
          colorLink: apiData?.config?.theme?.primary_color || '#8B4513',
        },
        components: {
          Typography: {
            titleMarginTop: 0,
            titleMarginBottom: 0,
            colorTextHeading: apiData?.config?.theme?.primary_color || '#8B4513',
          },
          Menu: {
            colorItemTextHover: apiData?.config?.theme?.sidebar_highlight_text_color || '#fff',
            colorItemTextSelected: '#fff',
            itemHoverBg: apiData?.config?.theme?.sidebar_highlight_bg_color || '#8B4513',
            colorItemBgSelected: apiData?.config?.theme?.sidebar_highlight_bg_color || '#8B4513',
          },
        },
      }}
    >
      {apiData.config.google_analytics_id && (
        <GoogleAnalytics measurementId={apiData.config.google_analytics_id} />
      )}
      {apiData.config.clarity_id && (
        <Clarity clarityId={apiData.config.clarity_id} />
      )}
      <Router>
        <CustomLayout apiData={apiData}>
          <GlobalSearch data={apiData} />
          <Routes>
            <Route path="/" element={<Home data={apiData} />} />
            <Route path="/modules" element={<Modules data={apiData} />} />
            <Route path="/modules/:id" element={<ModuleDetail data={apiData} />} />
            <Route path="/classes" element={<Classes data={apiData} />} />
            <Route path="/classes/:id" element={<ClassDetail data={apiData} />} />
            <Route path="/functions" element={<Functions data={apiData} />} />
            <Route path="/pages" element={<Pages data={apiData} />} />
            <Route path="/pages/:slug" element={<PageDetail data={apiData} />} />
          </Routes>
        </CustomLayout>
      </Router>
    </ConfigProvider>
  );
};

export default App;
