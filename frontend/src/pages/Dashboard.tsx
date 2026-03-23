import React from 'react';
import { Card, Row, Col, Statistic } from 'antd';
import { useTranslation } from 'react-i18next';
import { Column } from '@ant-design/charts';

const Dashboard: React.FC = () => {
  const { t } = useTranslation();

  const data = [
    { type: '降糖药', sales: 38 },
    { type: '降压药', sales: 52 },
    { type: '抗生素', sales: 61 },
    { type: '心血管', sales: 145 },
    { type: '其他', sales: 48 },
  ];

  const config = {
    data,
    xField: 'type',
    yField: 'sales',
    label: {
      position: 'middle' as const,
      style: {
        fill: '#FFFFFF',
        opacity: 0.6,
      },
    },
    xAxis: {
      label: {
        autoHide: true,
        autoRotate: false,
      },
    },
    meta: {
      type: {
        alias: '类别',
      },
      sales: {
        alias: '销售额',
      },
    },
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{t('dashboard')}</h1>
      <Row gutter={16} className="mb-6">
        <Col span={6}>
          <Card>
            <Statistic title="总分析药品数" value={112} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="本月新增" value={15} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="预警提示" value={3} valueStyle={{ color: '#cf1322' }} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="系统状态" value="正常" valueStyle={{ color: '#3f8600' }} />
          </Card>
        </Col>
      </Row>
      <Card title="各分类成本概览">
        <div style={{ height: 400 }}>
          {/* Use standard antd charts format. Type might be slightly different in newer versions but this is a standard config */}
          <Column {...config} />
        </div>
      </Card>
    </div>
  );
};

export default Dashboard;
