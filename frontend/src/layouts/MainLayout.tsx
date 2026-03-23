import React, { useState } from 'react';
import { Layout, Menu, Button, Dropdown, Switch } from 'antd';
import { Outlet, useNavigate, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
  DashboardOutlined,
  MedicineBoxOutlined,
  LineChartOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  UserOutlined,
  TranslationOutlined,
  BulbOutlined,
} from '@ant-design/icons';
import { useAppStore } from '../store';

const { Header, Sider, Content } = Layout;

const MainLayout: React.FC = () => {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const { t } = useTranslation();
  const { theme, setTheme, locale, setLocale } = useAppStore();

  const menuItems = [
    {
      key: '/dashboard',
      icon: <DashboardOutlined />,
      label: t('dashboard'),
    },
    {
      key: '/drugs',
      icon: <MedicineBoxOutlined />,
      label: t('drugs'),
    },
    {
      key: '/analysis',
      icon: <LineChartOutlined />,
      label: t('analysis'),
    },
  ];

  const toggleTheme = () => {
    setTheme(theme === 'light' ? 'dark' : 'light');
  };

  const toggleLocale = () => {
    setLocale(locale === 'zh' ? 'en' : 'zh');
  };

  return (
    <Layout className="min-h-screen">
      <Sider trigger={null} collapsible collapsed={collapsed} theme={theme === 'dark' ? 'dark' : 'light'}>
        <div className="h-16 flex items-center justify-center font-bold text-lg overflow-hidden">
          {collapsed ? 'DCA' : 'Drug Cost Analysis'}
        </div>
        <Menu
          theme={theme === 'dark' ? 'dark' : 'light'}
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={({ key }) => navigate(key)}
        />
      </Sider>
      <Layout>
        <Header className={`p-0 flex justify-between items-center pr-6 ${theme === 'dark' ? 'bg-[#141414]' : 'bg-white'}`}>
          <Button
            type="text"
            icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
            onClick={() => setCollapsed(!collapsed)}
            className="w-16 h-16"
          />
          <div className="flex items-center space-x-4">
            <Button icon={<TranslationOutlined />} onClick={toggleLocale} type="text">
              {locale === 'zh' ? 'EN' : '中文'}
            </Button>
            <Switch
              checkedChildren={<BulbOutlined />}
              unCheckedChildren={<BulbOutlined />}
              checked={theme === 'dark'}
              onChange={toggleTheme}
            />
            <Button type="text" icon={<UserOutlined />}>
              Admin
            </Button>
          </div>
        </Header>
        <Content className="m-6 p-6 min-h-[280px] bg-white dark:bg-[#141414] rounded-lg">
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  );
};

export default MainLayout;
