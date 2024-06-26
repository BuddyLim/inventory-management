import React, { useEffect, useState } from "react";
import { Button, Form, FormProps, Input, List, Select } from "antd";
import axios from "axios";
import { v4 as uuid } from "uuid";

import styles from "./index.module.css";

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

  const handleUpdateInventoryList = (
    values: InventoryI,
    id?: string,
    last_updated_dt?: string,
  ) => {
    setInventoryList((prevList) => {
      const inventoryIndex = prevList.findIndex(
        (inventory) => inventory.name === values.name,
      );
      if (inventoryIndex === -1) {
        const tempID = uuid();
        return [...prevList, { ...values, id: tempID, last_updated_dt: "" }];
      }

      const inventory = prevList[inventoryIndex];

      prevList[inventoryIndex] = {
        ...values,
        id: id ?? inventory.id,
        last_updated_dt: last_updated_dt ?? inventory.last_updated_dt,
      };

      return [...prevList];
    });
  };

  const handleFinish: FormProps<InventoryI>["onFinish"] = (values) => {
    handleUpdateInventoryList(values);

    axios
      .post(`${import.meta.env.VITE_API_BASE_URL}/inventories`, {
        ...values,
      })
      .then((res) => {
        const { id, last_updated_dt } = res.data;
        handleUpdateInventoryList(values, id, last_updated_dt);
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
    <div className={styles["inventory_container"]}>
      <h3 style={{ margin: "2% 0 5% 0" }}>Inventory Management</h3>
      <Form layout="vertical" form={form} onFinish={handleFinish}>
        <Form.Item label="Name" name="name">
          <Input />
        </Form.Item>
        <Form.Item label="Price" name="price">
          <Input type="number" />
        </Form.Item>
        <Form.Item label="Category" name="category">
          <Select>
            <Select.Option value="Clothing">Clothing</Select.Option>
            <Select.Option value="Stationary">Stationary</Select.Option>
            <Select.Option value="Books">Books</Select.Option>
          </Select>
        </Form.Item>
        <Form.Item style={{ width: "100%" }}>
          <Button type="primary" htmlType="submit" style={{ width: "100%" }}>
            Save Item
          </Button>
        </Form.Item>
      </Form>
      <List
        itemLayout="horizontal"
        dataSource={inventoryList}
        renderItem={(item, index) => (
          <List.Item
            actions={[
              <a
                key="list-delete"
                style={{ color: "red" }}
                onClick={() => handleDeleteInventory(item.id, index)}
              >
                delete
              </a>,
            ]}
          >
            <List.Item.Meta
              title={item.name}
              description={`$ ${item.price} - ${item.category}`}
            />
          </List.Item>
        )}
      />

      {/* <li style={{ color: "black" }} className={styles["inventory_list"]}> */}
      {/*     {inventoryList.map((inventory, index) => { */}
      {/*       return ( */}
      {/*         <ul key={inventory.id} className={styles["inventory_item"]}> */}
      {/*           <span className={styles["inventory_name"]}> */}
      {/*             {inventory.name} - ${inventory.price} */}
      {/*           </span> */}
      {/*           <Button */}
      {/*             danger */}
      {/*             type="primary" */}
      {/*             onClick={() => handleDeleteInventory(inventory.id, index)} */}
      {/*           > */}
      {/*             Delete */}
      {/*           </Button> */}
      {/*         </ul> */}
      {/*       ); */}
      {/*     })} */}
      {/*   </li> */}
    </div>
  );
};

export default InventoryForm;
