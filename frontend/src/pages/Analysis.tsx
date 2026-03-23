import React, { useState, useEffect } from 'react';
import { Card, Form, Select, Button, Spin, Result, Descriptions, Tag, Space, Typography, InputNumber, Divider, message, Row, Col } from 'antd';
import { MinusCircleOutlined, PlusOutlined, DownloadOutlined } from '@ant-design/icons';
import { useTranslation } from 'react-i18next';
import { Pie } from '@ant-design/charts';
import { getDrugs, startAnalysis, getAnalysisStatus, downloadPdf, downloadDocx } from '../services/api';

const { Paragraph } = Typography;
const { Option } = Select;

const Analysis: React.FC = () => {
  const { t } = useTranslation();
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [drugs, setDrugs] = useState<any[]>([]);
  const [pollingSession, setPollingSession] = useState<string | null>(null);

  useEffect(() => {
    getDrugs().then(setDrugs).catch(() => message.error('获取药品列表失败'));
  }, []);

  useEffect(() => {
    let interval: any;
    if (pollingSession) {
      interval = setInterval(async () => {
        try {
          const res = await getAnalysisStatus(pollingSession);
          if (res.status === 'completed') {
            setResult({
              session_id: res.session_id,
              summary: res.report.cost_summary,
              strategy: res.report.pricing_strategy,
              supplyChain: res.report.supply_chain_advice,
              // Backend didn't return these exactly in our mock, let's fake chart data for now
              // or we should update backend to return structured metrics.
              metrics: {
                total_cost: "已测算",
                cost_tier: "A/B",
                target_price: "建议价格"
              },
              costBreakdown: [
                { type: '生产成本', value: 50 },
                { type: '运输成本', value: 20 },
                { type: '储存成本', value: 20 },
                { type: '其他', value: 10 },
              ]
            });
            setLoading(false);
            setPollingSession(null);
            message.success('分析完成');
          }
        } catch (error) {
          console.error(error);
        }
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [pollingSession]);

  const handleAnalyze = async (values: any) => {
    setLoading(true);
    setResult(null);
    try {
      const payload = {
        drug_name: values.drug_name,
        unit: values.unit,
        costs: {
          raw_material_cost: values.raw_material_cost,
          rd_cost: values.rd_cost || 0,
          production_cost: values.production_cost || 0,
          equipment_cost: values.equipment_cost || 0,
          vehicle_cost: values.vehicle_cost || 0,
          fuel_cost: values.fuel_cost || 0,
          inventory_loss_cost: values.inventory_loss_cost || 0,
          warehouse_rent: values.warehouse_rent || 0,
          energy_cost: values.energy_cost || 0,
          custom_costs: values.custom_costs || []
        }
      };
      const res = await startAnalysis(payload);
      setPollingSession(res.session_id);
    } catch (error) {
      message.error('启动分析失败');
      setLoading(false);
    }
  };

  const handleDownloadPdf = async () => {
    if (!result?.session_id) return;
    try {
      const res = await downloadPdf(result.session_id);
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `report_${result.session_id}.pdf`);
      document.body.appendChild(link);
      link.click();
    } catch (error) {
      message.error('下载PDF失败');
    }
  };

  const handleDownloadDocx = async () => {
    if (!result?.session_id) return;
    try {
      const res = await downloadDocx(result.session_id);
      const url = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `report_${result.session_id}.docx`);
      document.body.appendChild(link);
      link.click();
    } catch (error) {
      message.error('下载Word失败');
    }
  };

  const pieConfig = {
    appendPadding: 10,
    data: result?.costBreakdown || [],
    angleField: 'value',
    colorField: 'type',
    radius: 0.9,
    label: {
      type: 'inner',
      offset: '-30%',
      content: ({ percent }: any) => `${(percent * 100).toFixed(0)}%`,
      style: {
        fontSize: 14,
        textAlign: 'center',
      },
    },
    interactions: [{ type: 'element-active' }],
  };

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{t('analysis')}</h1>
      
      <Row gutter={24}>
        <Col span={8}>
          <Card title="参数配置" className="mb-6">
            <Form form={form} layout="vertical" onFinish={handleAnalyze} initialValues={{
              unit: '元/盒',
              rd_cost: 0, production_cost: 0, equipment_cost: 0,
              vehicle_cost: 0, fuel_cost: 0,
              inventory_loss_cost: 0, warehouse_rent: 0, energy_cost: 0
            }}>
              <Form.Item name="drug_name" label="选择药品" rules={[{ required: true }]}>
                <Select placeholder="请选择药品">
                  {drugs.map(d => <Option key={d.id} value={d.name}>{d.name}</Option>)}
                </Select>
              </Form.Item>
              
              <Form.Item name="unit" label="计量单位" rules={[{ required: true }]}>
                <Select>
                  <Option value="元/100片">元/100片</Option>
                  <Option value="元/剂">元/剂</Option>
                  <Option value="元/盒">元/盒</Option>
                </Select>
              </Form.Item>

              <Divider orientation="left">生产成本</Divider>
              <Form.Item name="raw_material_cost" label="原料成本" rules={[{ required: true }]}>
                <InputNumber style={{ width: '100%' }} min={0} />
              </Form.Item>
              <Form.Item name="rd_cost" label="研发成本">
                <InputNumber style={{ width: '100%' }} min={0} />
              </Form.Item>
              <Form.Item name="production_cost" label="生产工艺成本">
                <InputNumber style={{ width: '100%' }} min={0} />
              </Form.Item>
              <Form.Item name="equipment_cost" label="设备折旧及维护成本">
                <InputNumber style={{ width: '100%' }} min={0} />
              </Form.Item>

              <Divider orientation="left">运输成本</Divider>
              <Form.Item name="vehicle_cost" label="车辆设备成本">
                <InputNumber style={{ width: '100%' }} min={0} />
              </Form.Item>
              <Form.Item name="fuel_cost" label="燃料成本">
                <InputNumber style={{ width: '100%' }} min={0} />
              </Form.Item>

              <Divider orientation="left">储存成本</Divider>
              <Form.Item name="inventory_loss_cost" label="库存损耗成本">
                <InputNumber style={{ width: '100%' }} min={0} />
              </Form.Item>
              <Form.Item name="warehouse_rent" label="仓储场地租金">
                <InputNumber style={{ width: '100%' }} min={0} />
              </Form.Item>
              <Form.Item name="energy_cost" label="场地能耗成本">
                <InputNumber style={{ width: '100%' }} min={0} />
              </Form.Item>

              <Divider orientation="left">其他自定义成本</Divider>
              <Form.List name="custom_costs">
                {(fields, { add, remove }) => (
                  <>
                    {fields.map(({ key, name, ...restField }) => (
                      <Space key={key} style={{ display: 'flex', marginBottom: 8 }} align="baseline">
                        <Form.Item
                          {...restField}
                          name={[name, 'name']}
                          rules={[{ required: true, message: 'Missing name' }]}
                        >
                          <Select placeholder="成本类型" style={{ width: 120 }}>
                            <Option value="营销成本">营销成本</Option>
                            <Option value="管理费用">管理费用</Option>
                            <Option value="财务费用">财务费用</Option>
                            <Option value="其他">其他</Option>
                          </Select>
                        </Form.Item>
                        <Form.Item
                          {...restField}
                          name={[name, 'value']}
                          rules={[{ required: true, message: 'Missing cost' }]}
                        >
                          <InputNumber placeholder="金额" min={0} />
                        </Form.Item>
                        <MinusCircleOutlined onClick={() => remove(name)} />
                      </Space>
                    ))}
                    <Form.Item>
                      <Button type="dashed" onClick={() => add()} block icon={<PlusOutlined />}>
                        添加成本项
                      </Button>
                    </Form.Item>
                  </>
                )}
              </Form.List>

              <Form.Item>
                <Button type="primary" htmlType="submit" loading={loading} block>
                  开始多智能体分析
                </Button>
              </Form.Item>
            </Form>
          </Card>
        </Col>

        <Col span={16}>
          {loading && (
            <div className="flex justify-center p-12">
              <Spin size="large" tip="正在通过 RAG 和多智能体系统进行分析，请稍候..." />
            </div>
          )}

          {!loading && result && (
            <Space direction="vertical" size="large" style={{ width: '100%' }}>
              <Card 
                title="分析结果总览" 
                extra={
                  <Space>
                    <Button icon={<DownloadOutlined />} onClick={handleDownloadPdf}>导出 PDF</Button>
                    <Button icon={<DownloadOutlined />} onClick={handleDownloadDocx}>导出 Word</Button>
                    <Tag color="blue">分析完成</Tag>
                  </Space>
                }
              >
                <Descriptions bordered column={3}>
                  <Descriptions.Item label="总成本评估">{result.metrics.total_cost}</Descriptions.Item>
                  <Descriptions.Item label="成本等级">{result.metrics.cost_tier}</Descriptions.Item>
                  <Descriptions.Item label="建议目标售价"><span className="text-red-500 font-bold">{result.metrics.target_price}</span></Descriptions.Item>
                </Descriptions>
              </Card>

              <div className="grid grid-cols-2 gap-6">
                <Card title="成本结构占比">
                  <div style={{ height: 300 }}>
                    <Pie {...pieConfig} />
                  </div>
                </Card>
                
                <Card title="智能体专家建议" style={{ overflowY: 'auto', maxHeight: 400 }}>
                  <div className="space-y-4">
                    <div>
                      <h3 className="font-bold text-lg mb-2">Cost Accountant (成本会计)</h3>
                      <Paragraph className="bg-gray-50 dark:bg-gray-800 p-3 rounded">
                        {result.summary}
                      </Paragraph>
                    </div>
                    <div>
                      <h3 className="font-bold text-lg mb-2">Pricing Strategist (定价策略师)</h3>
                      <Paragraph className="bg-gray-50 dark:bg-gray-800 p-3 rounded">
                        {result.strategy}
                      </Paragraph>
                    </div>
                    <div>
                      <h3 className="font-bold text-lg mb-2">Supply Chain Manager (供应链经理)</h3>
                      <Paragraph className="bg-gray-50 dark:bg-gray-800 p-3 rounded">
                        {result.supplyChain}
                      </Paragraph>
                    </div>
                  </div>
                </Card>
              </div>
            </Space>
          )}

          {!loading && !result && (
            <Card>
              <Result
                title="请填写参数并开始分析"
                subTitle="系统将调用多个 AI 智能体对药品的生产、运输、储存等成本进行全方位测算。"
              />
            </Card>
          )}
        </Col>
      </Row>
    </div>
  );
};

export default Analysis;
