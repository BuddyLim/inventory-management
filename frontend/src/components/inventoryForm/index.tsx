import React, { useState } from 'react';
import { Button, Form, Input } from 'antd';
import axios from 'axios';

const InventoryForm: React.FC = () => {
  const [form] = Form.useForm();

  const handleFinish = (values) =>{
    console.log(values)
    axios.post("https://2uhvzh44vg.execute-api.us-east-1.amazonaws.com/Prod/inventories", {
      ...values
    })
    .then((res) =>{
      console.log(res)
    })
    .catch((error) => {
      console.log(error);
    });

  }

  return (
    <Form
      layout='vertical'
      form={form}
      onFinish={handleFinish}
      style={{ maxWidth: 600 }}
    >
      <Form.Item label="Name" name="name">
        <Input />
      </Form.Item>
      <Form.Item label="Price" name="price">
        <Input type='number' /> 
      </Form.Item>
      <Form.Item label="Category" name="category">
        <Input />
      </Form.Item>
      <Form.Item>
        <Button type="primary" htmlType="submit">Submit</Button>
      </Form.Item>
    </Form>
  );
};

export default InventoryForm;