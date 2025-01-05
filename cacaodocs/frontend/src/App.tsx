import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ConfigProvider, Spin } from 'antd';
import CustomLayout from './components/Layout/Layout';
import Home from './components/Pages/Home';
import Api from './components/Pages/Api';
import Types from './components/Pages/Types';
import Docs from './components/Pages/Docs';

import type { AppData } from './global';

const App: React.FC = () => {
  const [apiData, setApiData] = useState<AppData>({ api: [], docs: [], types: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDevData = async () => {
      try {
        const response = await fetch('http://localhost:5000/docs');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const jsonData = await response.json();
        console.log('Raw API response:', jsonData); // Debug log

        // Transform the data - check if arrays or objects
        const transformedData = {
          api: Array.isArray(jsonData.api) ? jsonData.api : (jsonData.api ? [jsonData.api] : []),
          docs: Array.isArray(jsonData.docs) ? jsonData.docs : (jsonData.docs ? [jsonData.docs] : []),
          types: Array.isArray(jsonData.types) ? jsonData.types : (jsonData.types ? [jsonData.types] : [])
        };

        console.log('Transformed data:', transformedData); // Debug log
        setApiData(transformedData);
      } catch (error) {
        console.error('Error fetching dev data:', error);
        setApiData({ api: [], docs: [], types: [] });
      } finally {
        setLoading(false);
      }
    };

    // If in development, attempt to fetch from localhost
    if (process.env.NODE_ENV === 'development') {
      fetchDevData();
    } else {
      // Production logic
      if (
        window.globalData?.api?.length ||
        window.globalData?.docs?.length ||
        window.globalData?.types?.length
      ) {
        setApiData(window.globalData);
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
          colorPrimary: '#331201',
          colorTextHeading: '#331201',
          colorLink: '#331201',
        },
        components: {
          Typography: {
            titleMarginTop: 0,
            titleMarginBottom: 0,
            colorTextHeading: '#331201',
          },
          Menu: {
            colorItemTextHover: '#331201',
            colorItemTextSelected: '#fff',
          },
        },
      }}
    >
      <Router>
        <CustomLayout apiData={apiData}>
          <Routes>
            <Route path="/" element={<Home data={apiData} />} />
            <Route path="/api" element={<Api data={apiData.api} types={apiData.types} />} />
            <Route path="/types" element={<Types data={apiData.types} />} />
            <Route path="/docs" element={<Docs data={apiData.docs} types={apiData.types} />} />
          </Routes>
        </CustomLayout>
      </Router>
    </ConfigProvider>
  );
};

export default App;
