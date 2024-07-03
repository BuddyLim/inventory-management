import React, { useEffect, useState } from "react";
import {
  Button,
  Flex,
  Form,
  FormProps,
  Input,
  List,
  Modal,
  Select,
  Space,
} from "antd";
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

interface StatsI {
  total_price: number;
  count: number;
  category: CategoryEnum;
}

const InventoryForm: React.FC = () => {
  const [form] = Form.useForm();
  const [currentStatsCategory, setCurrentStatsCategory] =
    useState<string>("All");
  const [inventoryList, setInventoryList] = useState<InventoryI[]>([]);
  const [statsModalOpen, setStatsModalOpen] = useState<boolean>(false);
  const [statsList, setStatsList] = useState<StatsI[]>([]);

  const [currentPage, setCurrentPage] = useState<number>(0);
  const [paginationList, setPaginationList] = useState<string[]>([]);

  const fetchPreviousInventoryList = (next_key?: string) => {
    axios
      .get(
        `${import.meta.env.VITE_API_BASE_URL}/inventories?next_key=${next_key ?? ""}`,
      )
      .then((res) => {
        const { items, next_key } = res.data;
        setCurrentPage((prevValue) => --prevValue);
        setInventoryList(items);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  const fetchNextInventoryList = (next_key?: string) => {
    axios
      .get(
        `${import.meta.env.VITE_API_BASE_URL}/inventories?next_key=${next_key ?? ""}`,
      )
      .then((res) => {
        const { items, next_key } = res.data;
        setCurrentPage((prevValue) => ++prevValue);
        setPaginationList((prevList) => [
          ...prevList,
          next_key?.["id"] ?? null,
        ]);
        setInventoryList(items);
      })
      .catch((error) => {
        console.log(error);
      });
  };

  useEffect(() => {
    axios
      .get(`${import.meta.env.VITE_API_BASE_URL}/inventories`)
      .then((res) => {
        const { items, next_key } = res.data;

        setPaginationList([items[0]["id"], next_key["id"]]);
        console.log(paginationList);
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

  const fetchStatsByCategory = (category: string) => {
    axios
      .post(`${import.meta.env.VITE_API_BASE_URL}/inventories/stats`, {
        category: category,
      })
      .then((res) => {
        console.log(res);

        setStatsList(res.data.items);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const handleModalOpen = () => {
    setStatsModalOpen((prevFlag) => !prevFlag);
    fetchStatsByCategory("all");
  };
  console.log(currentPage, paginationList);
  return (
    <div className={styles["inventory_container"]}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "baseline",
        }}
      >
        <h3 style={{ margin: "2% 0 5% 0" }}>Inventory Management</h3>
        <Button type="link" onClick={handleModalOpen}>
          stats
        </Button>
      </div>
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
      <Flex>
        {currentPage !== 0 ? (
          <Button
            block
            type="link"
            onClick={() => {
              fetchPreviousInventoryList(paginationList[currentPage - 1]);
            }}
          >
            back
          </Button>
        ) : (
          <div style={{ width: "100%" }} />
        )}
        {paginationList[currentPage + 1] !== null ? (
          <Button
            block
            onClick={() =>
              fetchNextInventoryList(paginationList[currentPage + 1])
            }
            type="link"
          >
            next
          </Button>
        ) : (
          <div style={{ width: "100%" }} />
        )}
      </Flex>
      <Modal
        title="Inventory Statistics"
        open={statsModalOpen}
        onCancel={handleModalOpen}
        closable
      >
        <Space direction="vertical">
          <Select
            value={currentStatsCategory}
            onSelect={(_, option) => {
              setCurrentStatsCategory(option.value!);

              fetchStatsByCategory(option.value!);
            }}
            style={{ width: "100%" }}
            options={[
              { value: "all", label: "All" },
              { value: "Clothing", label: "Clothing" },
              { value: "Stationary", label: "Stationary" },
              { value: "Books", label: "Books" },
            ]}
          />
          {statsList.map((statsObj, index) => {
            return (
              <div key={`stats-${index}`} className={styles["stast_list"]}>
                <span>{statsObj.category}</span>
                <span> x{statsObj.count}</span>
                <span> ${statsObj.total_price}</span>
              </div>
            );
          })}
        </Space>
      </Modal>
    </div>
  );
};

export default InventoryForm;
