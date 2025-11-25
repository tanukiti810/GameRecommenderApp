"use client";

import React from "react";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import Checkbox from "@mui/material/Checkbox";
import Collapse from "@mui/material/Collapse";
import ExpandLess from "@mui/icons-material/ExpandLess";
import ExpandMore from "@mui/icons-material/ExpandMore";

interface SubItem {
  id: string;
  label: string;
}

interface ParentItem {
  id: string;
  label: string;
  children: SubItem[];
}

const items: ParentItem[] = [
  {
    id: "Action",
    label: "アクション",
    children: [
      { id: "FPS", label: "FPS" },
      { id: "ActionGame", label: "アクションゲーム" },
      { id: "Fighting", label: "格闘ゲーム" },
    ],
  },
  {
    id: "Adventure",
    label: "アドベンチャー",
    children: [
      { id: "Novel", label: "ノベル" },
      { id: "Exploration", label: "探索ゲーム" },
    ],
  },
];

const SidebarSelect = () => {
  const [checked, setChecked] = React.useState<string[]>([]);
  const [open, setOpen] = React.useState<{ [key: string]: boolean }>({});

  // --- debounce 用 ref ---
  const debounceRef = React.useRef<NodeJS.Timeout | null>(null);

  const sendDataDebounced = (selected: string[]) => {
  if (debounceRef.current) clearTimeout(debounceRef.current);
  debounceRef.current = setTimeout(async () => {
    try {
      const response = await fetch("http://localhost:8000/api/choose", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ selected }),
      });
      const result = await response.json();
      console.log("サーバーからの返却:", result);
    } catch (err) {
      console.error("送信エラー:", err);
    }
  }, 300);
};

  // --- 子チェック ---
  const handleToggle = (value: string) => () => {
    const currentIndex = checked.indexOf(value);
    const newChecked = [...checked];

    if (currentIndex === -1) newChecked.push(value);
    else newChecked.splice(currentIndex, 1);

    setChecked(newChecked);
    sendDataDebounced(newChecked);
  };

  // --- 親チェック ---
  const handleParentToggle = (parent: ParentItem) => () => {
    const allChildrenChecked = parent.children.every((c) =>
      checked.includes(c.id)
    );
    let newChecked = [...checked];

    if (allChildrenChecked) {
      newChecked = newChecked.filter(
        (id) => !parent.children.some((c) => c.id === id)
      );
    } else {
      parent.children.forEach((c) => {
        if (!newChecked.includes(c.id)) newChecked.push(c.id);
      });
    }

    setChecked(newChecked);
    sendDataDebounced(newChecked);
  };

  // --- アコーディオン開閉 ---
  const handleOpen = (key: string) => () => {
    setOpen((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  // --- 親チェック状態 ---
  const isParentChecked = (parent: ParentItem) =>
    parent.children.every((c) => checked.includes(c.id));

  const isParentIndeterminate = (parent: ParentItem) => {
    const checkedCount = parent.children.filter((c) =>
      checked.includes(c.id)
    ).length;
    return checkedCount > 0 && checkedCount < parent.children.length;
  };

  return (
    <div className="side-bar">
      <List sx={{ width: "100%" }}>
        {items.map((parent) => (
          <React.Fragment key={parent.id}>
            {/* 親アイテム */}
            <ListItem disablePadding>
              <ListItemButton onClick={handleOpen(parent.id)}>
                <ListItemIcon>
                  <Checkbox
                    edge="start"
                    checked={isParentChecked(parent)}
                    indeterminate={isParentIndeterminate(parent)}
                    tabIndex={-1}
                    disableRipple
                    onClick={(e) => {
                      e.stopPropagation();
                      handleParentToggle(parent)();
                    }}
                  />
                </ListItemIcon>
                <ListItemText primary={parent.label} />
                {open[parent.id] ? <ExpandLess /> : <ExpandMore />}
              </ListItemButton>
            </ListItem>

            {/* サブアイテム */}
            <Collapse in={open[parent.id]} timeout="auto" unmountOnExit>
              <List component="div" disablePadding>
                {parent.children.map((child) => (
                  <ListItem sx={{ pl: 4 }} key={child.id} disablePadding>
                    <ListItemButton onClick={handleToggle(child.id)} dense>
                      <ListItemIcon>
                        <Checkbox checked={checked.includes(child.id)} />
                      </ListItemIcon>
                      <ListItemText primary={child.label} />
                    </ListItemButton>
                  </ListItem>
                ))}
              </List>
            </Collapse>
          </React.Fragment>
        ))}
      </List>
    </div>
  );
};

export default SidebarSelect;
