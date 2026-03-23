import { useEffect } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { ConfigProvider, theme as antdTheme } from 'antd';
import { useTranslation } from 'react-i18next';
import zhCN from 'antd/locale/zh_CN';
import enUS from 'antd/locale/en_US';
import { useAppStore } from './store';
import MainLayout from './layouts/MainLayout';
import Dashboard from './pages/Dashboard';
import DrugList from './pages/DrugList';
import Analysis from './pages/Analysis';
import Login from './pages/Login';
import './locales/i18n';

function App() {
  const { theme, locale } = useAppStore();
  const { i18n } = useTranslation();

  useEffect(() => {
    i18n.changeLanguage(locale);
    document.documentElement.className = theme;
  }, [locale, theme, i18n]);

  const antdLocale = locale === 'zh' ? zhCN : enUS;

  return (
    <ConfigProvider
      locale={antdLocale}
      theme={{
        algorithm: theme === 'dark' ? antdTheme.darkAlgorithm : antdTheme.defaultAlgorithm,
        token: {
          colorPrimary: '#1677ff',
        },
      }}
    >
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/" element={<MainLayout />}>
            <Route index element={<Navigate to="/dashboard" replace />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="drugs" element={<DrugList />} />
            <Route path="analysis" element={<Analysis />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </ConfigProvider>
  );
}

export default App;
