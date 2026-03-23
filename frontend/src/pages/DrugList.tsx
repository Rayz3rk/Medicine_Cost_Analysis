import React, { useState, useEffect } from 'react';
import { Table, Input, Button, Space, Tag, Modal, Form, message, Popconfirm } from 'antd';
import { useTranslation } from 'react-i18next';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { getDrugs, createDrug, updateDrug, deleteDrug } from '../services/api';

const DrugList: React.FC = () => {
  const { t } = useTranslation();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [drugs, setDrugs] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [form] = Form.useForm();

  const fetchDrugs = async () => {
    setLoading(true);
    try {
      const data = await getDrugs();
      setDrugs(data.map((d: any) => ({ ...d, key: d.id })));
    } catch (error) {
      message.error('获取药品列表失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDrugs();
  }, []);

  const columns = [
    {
      title: '药品名称',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: '规格',
      dataIndex: 'specifications',
      key: 'specifications',
    },
    {
      title: '适应症',
      dataIndex: 'indications',
      key: 'indications',
    },
    {
      title: '存储条件',
      dataIndex: 'storage_conditions',
      key: 'storage_conditions',
    },
    {
      title: '操作',
      key: 'action',
      render: (_: any, record: any) => (
        <Space size="middle">
          <Button type="link" icon={<EditOutlined />} onClick={() => handleEdit(record)}>编辑</Button>
          <Popconfirm title="确定删除吗?" onConfirm={() => handleDelete(record.id)}>
            <Button type="link" danger icon={<DeleteOutlined />}>删除</Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  const handleEdit = (record: any) => {
    setEditingId(record.id);
    form.setFieldsValue(record);
    setIsModalOpen(true);
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteDrug(id);
      message.success('删除成功');
      fetchDrugs();
    } catch (error) {
      message.error('删除失败');
    }
  };

  const handleAdd = () => {
    form.validateFields().then(async (values) => {
      try {
        if (editingId) {
          await updateDrug(editingId, values);
          message.success('更新成功');
        } else {
          await createDrug(values);
          message.success('创建成功');
        }
        setIsModalOpen(false);
        form.resetFields();
        setEditingId(null);
        fetchDrugs();
      } catch (error) {
        message.error('保存失败');
      }
    });
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">{t('drugs')}</h1>
        <Space>
          <Input.Search placeholder="搜索药品" allowClear />
          <Button type="primary" icon={<PlusOutlined />} onClick={() => {
            setEditingId(null);
            form.resetFields();
            setIsModalOpen(true);
          }}>
            新增药品
          </Button>
        </Space>
      </div>

      <Table dataSource={drugs} columns={columns} loading={loading} />

      <Modal
        title={editingId ? "编辑药品" : "新增药品"}
        open={isModalOpen}
        onOk={handleAdd}
        onCancel={() => {
          setIsModalOpen(false);
          setEditingId(null);
        }}
      >
        <Form form={form} layout="vertical">
          <Form.Item name="name" label="药品名称" rules={[{ required: true }]}>
            <Input />
          </Form.Item>
          <Form.Item name="specifications" label="规格">
            <Input />
          </Form.Item>
          <Form.Item name="indications" label="适应症">
            <Input />
          </Form.Item>
          <Form.Item name="storage_conditions" label="存储条件">
            <Input />
          </Form.Item>
        </Form>
      </Modal>
    </div>
  );
};

export default DrugList;
