import React, { useEffect, useState } from "react";
import { Button, Form, FormProps, Input } from "antd";
import axios from "axios";

enum CategoryEnum {
  STATIONARY = "Stationary",
  BOOKS = "BOOKS",
  CLOTHING = "CLOTHING",
}

interface InventoryI {
  id: string;
  name: string;
  price: number;
  category: CategoryEnum;
  last_updated_dt: string;
}

const InventoryForm: React.FC = () => {
  const [form] = Form.useForm();
  const [inventoryList, setInventoryList] = useState<InventoryI[]>([]);

  useEffect(() => {
    axios
      .get(`${import.meta.env.VITE_API_BASE_URL}/inventories`)
      .then((res) => {
        const { items } = res.data;

        setInventoryList(items);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  const handleFinish: FormProps<InventoryI>["onFinish"] = (values) => {
    axios
      .post(`${import.meta.env.VITE_API_BASE_URL}/inventories`, {
        ...values,
      })
      .then((res) => {
        const { id, last_updated_dt } = res.data;

        setInventoryList((prevList) => {
          const inventoryIndex = prevList.findIndex(
            (inventoryIndex) => inventoryIndex.id === id,
          );
          if (inventoryIndex === -1) {
            return [...prevList, { ...values, id, last_updated_dt }];
          }

          prevList[inventoryIndex] = { ...values, id, last_updated_dt };

          return [...prevList];
        });
      })
      .catch((error) => {
        console.log(error);
      });
  };
  const handleDeleteInventory = (id: string, index: number) => {
    const tempInventory = { ...inventoryList[index] };

    setInventoryList((prevList) => {
      const newList = [...prevList];
      newList.splice(index, 1);
      return [...newList];
    });

    axios
      .post(`${import.meta.env.VITE_API_BASE_URL}/inventories/delete`, {
        id: id,
      })
      .catch(() => {
        setInventoryList((prevList) => {
          const newList = [...prevList];
          newList.splice(index, 0, tempInventory);
          return [...newList];
        });
      });
  };

  return (
    <>
      <h3>Inventory Management</h3>
      <Form
        layout="vertical"
        form={form}
        onFinish={handleFinish}
        style={{ maxWidth: 600 }}
      >
        <Form.Item label="Name" name="name">
          <Input />
        </Form.Item>
        <Form.Item label="Price" name="price">
          <Input type="number" />
        </Form.Item>
        <Form.Item label="Category" name="category">
          <Input />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit">
            Save Item
          </Button>
        </Form.Item>
      </Form>
      <div style={{ color: "black" }}>
        {inventoryList.map((inventory, index) => {
          return (
            <div key={inventory.id}>
              {inventory.name} - ${inventory.price}
              <Button
                danger
                type="primary"
                onClick={() => handleDeleteInventory(inventory.id, index)}
              >
                Delete
              </Button>
            </div>
          );
        })}
      </div>
    </>
  );
};

export default InventoryForm;
