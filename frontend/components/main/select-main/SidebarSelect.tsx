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
import Box from "@mui/material/Box";
import { Divider, FormControlLabel, FormGroup } from "@mui/material";

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
  {
    id: "RPG",
    label: "RPG",
    children: [
      { id: "JRPG", label: "JRPG" },
      { id: "ARPG", label: "アクションRPG" },
      { id: "MMORPG", label: "MMORPG" },
    ],
  },
  {
    id: "Simulation",
    label: "シミュレーション",
    children: [
      { id: "LifeSim", label: "生活シミュレーション" },
      { id: "Strategy", label: "戦略シミュレーション" },
    ],
  },
  {
    id: "Sports",
    label: "スポーツ",
    children: [
      { id: "Racing", label: "レーシング" },
      { id: "Soccer", label: "サッカー" },
      { id: "Baseball", label: "野球" },
    ],
  },
];

const SidebarSelect = () => {
  const [checked, setChecked] = React.useState<string[]>([]);
  const [open, setOpen] = React.useState<{ [key: string]: boolean }>({});
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

  const handleToggle = (value: string) => (e: React.MouseEvent) => {
    e.stopPropagation();
    const currentIndex = checked.indexOf(value);
    const newChecked = [...checked];

    if (currentIndex === -1) newChecked.push(value);
    else newChecked.splice(currentIndex, 1);

    setChecked(newChecked);
    sendDataDebounced(newChecked);
  };

  const handleParentToggle = (parent: ParentItem) => (e: React.MouseEvent) => {
    e.stopPropagation();
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

  const handleOpen = (key: string) => (e: React.MouseEvent) => {
    e.stopPropagation();
    setOpen((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const isParentChecked = (parent: ParentItem) =>
    parent.children.every((c) => checked.includes(c.id));

  const isParentIndeterminate = (parent: ParentItem) => {
    const checkedCount = parent.children.filter((c) =>
      checked.includes(c.id)
    ).length;
    return checkedCount > 0 && checkedCount < parent.children.length;
  };

  return (
    <Box className="side-bar">
      <List sx={{ width: "100%", padding: 0 }}>
        <ListItem>
          <ListItemText primary="プラットフォーム" />
        </ListItem>

        <List disablePadding>
          <ListItem>
            <ListItemIcon>
              <Checkbox defaultChecked />
            </ListItemIcon>
            <ListItemText primary="Steam" />
          </ListItem>

          <Divider sx={{ mx: 2 }} />

          <ListItem>
            <ListItemIcon>
              <Checkbox defaultChecked />
            </ListItemIcon>
            <ListItemText primary="Switch" />
          </ListItem>
        </List>

        <Divider sx={{ mx: 1 }} />
        {items.map((parent) => (
          <React.Fragment key={parent.id}>
            <ListItem disablePadding>
              <ListItemButton onClick={handleOpen(parent.id)}>
                <ListItemIcon>
                  <Checkbox
                    edge="start"
                    checked={isParentChecked(parent)}
                    indeterminate={isParentIndeterminate(parent)}
                    tabIndex={-1}
                    disableRipple
                    onClick={handleParentToggle(parent)}
                  />
                </ListItemIcon>
                <ListItemText primary={parent.label} />
                {open[parent.id] ? <ExpandLess /> : <ExpandMore />}
              </ListItemButton>
            </ListItem>

            <Divider sx={{ mx: 1 }} />

            <Collapse in={open[parent.id]} timeout="auto" unmountOnExit>
              <List component="div" disablePadding>
                {parent.children.map((child) => (
                  <React.Fragment key={child.id}>
                    <ListItem sx={{ pl: 4 }} disablePadding>
                      <ListItemButton onClick={handleToggle(child.id)} dense>
                        <ListItemIcon>
                          <Checkbox
                            edge="start"
                            checked={checked.includes(child.id)}
                            tabIndex={-1}
                            disableRipple
                          />
                        </ListItemIcon>
                        <ListItemText primary={child.label} />
                      </ListItemButton>
                    </ListItem>
                    <Divider sx={{ mx: 2 }} />
                  </React.Fragment>
                ))}
              </List>
              <Divider />
            </Collapse>
          </React.Fragment>
        ))}
      </List>
    </Box>
  );
};

export default SidebarSelect;
