import React from 'react';
import { HashRouter as Router, Route, Switch } from 'react-router-dom';
import { ConfigProvider } from 'antd';
import CustomLayout from './components/Layout/Layout';
import Home from './components/Pages/Home';
import Api from './components/Pages/Api';
import Types from './components/Pages/Types';
import Docs from './components/Pages/Docs';

const App: React.FC = () => {
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
                        colorItemTextSelected: '#331201',
                    }
                }
            }}
        >
            <Router>
                <CustomLayout>
                    <Switch>
                        <Route path="/" exact component={Home} />
                        <Route path="/api" component={Api} />
                        <Route path="/types" component={Types} />
                        <Route path="/docs" component={Docs} />
                    </Switch>
                </CustomLayout>
            </Router>
        </ConfigProvider>
    );
};

export default App;
