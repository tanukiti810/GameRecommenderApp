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
import { Divider } from "@mui/material";

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
      { id: "FPS", label: "FPS（一人称シューティング）" },
      { id: "ThirdPersonShooter", label: "TPS（三人称シューティング）" },
      { id: "HackAndSlash", label: "ハクスラ（斬りまくりアクション）" },
      { id: "Fighting", label: "格闘アクション" },
      { id: "Platformer", label: "ジャンプアクション" },
      { id: "BulletHell", label: "弾幕シューティング" },
      { id: "Metroidvania", label: "メトロイドヴァニア（探索型）" },
      { id: "SoulsLike", label: "ソウルライク（高難度戦闘）" },
      { id: "RogueLite", label: "ローグライト" },
      { id: "Roguelike", label: "ローグライク" },
    ],
  },

  {
    id: "Adventure",
    label: "アドベンチャー",
    children: [
      { id: "Exploration", label: "探索アドベンチャー" },
      { id: "WalkingSimulator", label: "ウォーキング型" },
      { id: "VisualNovel", label: "ビジュアルノベル" },
      { id: "ChoicesMatter", label: "選択で変化する物語" },
      { id: "Mystery", label: "ミステリー" },
      { id: "Horror", label: "ホラー" },
      { id: "SurvivalHorror", label: "サバイバルホラー" },
    ],
  },

  {
    id: "RPG",
    label: "RPG（ロールプレイング）",
    children: [
      { id: "JRPG", label: "JRPG（日本風RPG）" },
      { id: "ARPG", label: "アクションRPG" },
      { id: "CRPG", label: "CRPG（PC風RPG）" },
      { id: "MMORPG", label: "MMORPG（大規模オンラインRPG）" },
      { id: "TurnBased", label: "ターン制RPG" },
      { id: "DungeonCrawler", label: "ダンジョン探索RPG" },
      { id: "RoguelikeDeckbuilder", label: "ローグライクカード" },
    ],
  },

  {
    id: "Simulation",
    label: "シミュレーション",
    children: [
      { id: "LifeSim", label: "生活シミュレーション" },
      { id: "FarmingSim", label: "農業シミュレーション" },
      { id: "VehicleSim", label: "乗り物シミュレーター" },
      { id: "Flight", label: "フライトシミュレーション" },
      { id: "SpaceSim", label: "宇宙シミュレーション" },
      { id: "Builder", label: "建築・クラフト" },
      { id: "Management", label: "経営シミュレーション" },
    ],
  },

  {
    id: "Strategy",
    label: "ストラテジー（戦略）",
    children: [
      { id: "RTS", label: "RTS（リアルタイム戦略）" },
      { id: "TBS", label: "ターン制戦略" },
      { id: "4X", label: "4X（探検/拡張/開発/征服）" },
      { id: "GrandStrategy", label: "大規模戦略" },
      { id: "TowerDefense", label: "タワーディフェンス" },
      { id: "AutoBattler", label: "オートバトラー" },
      { id: "CardBattler", label: "カードバトル" },
    ],
  },

  {
    id: "Sports",
    label: "スポーツ",
    children: [
      { id: "Racing", label: "レーシング" },
      { id: "Soccer", label: "サッカー" },
      { id: "Baseball", label: "野球" },
      { id: "Basketball", label: "バスケ" },
      { id: "Golf", label: "ゴルフ" },
      { id: "Boxing", label: "ボクシング" },
      { id: "Fishing", label: "釣り" },
    ],
  },

  {
    id: "Casual",
    label: "カジュアル・パズル",
    children: [
      { id: "Puzzle", label: "パズル" },
      { id: "Match3", label: "マッチ3" },
      { id: "Clicker", label: "クリッカー" },
      { id: "Relaxing", label: "リラックス" },
      { id: "Cozy", label: "癒し系" },
    ],
  },

  {
    id: "Creative",
    label: "創作・クラフト",
    children: [
      { id: "Sandbox", label: "サンドボックス" },
      { id: "Crafting", label: "クラフト" },
      { id: "Building", label: "建築" },
      { id: "Moddable", label: "Mod対応" },
    ],
  },

  {
    id: "Story",
    label: "ストーリー重視",
    children: [
      { id: "StoryRich", label: "物語重視" },
      { id: "Drama", label: "ドラマ" },
      { id: "Emotional", label: "感動系" },
      { id: "LoreRich", label: "設定が深い" },
    ],
  },

  {
    id: "SciFiFantasy",
    label: "SF・ファンタジー世界",
    children: [
      { id: "SciFi", label: "SF" },
      { id: "Fantasy", label: "ファンタジー" },
      { id: "Cyberpunk", label: "サイバーパンク" },
      { id: "Mythology", label: "神話" },
      { id: "Supernatural", label: "超常現象" },
    ],
  },

  {
    id: "History",
    label: "歴史テーマ",
    children: [
      { id: "Medieval", label: "中世" },
      { id: "Ancient", label: "古代" },
      { id: "WorldWar", label: "戦争" },
      { id: "AlternateHistory", label: "架空歴史" },
    ],
  },

  {
    id: "Multiplayer",
    label: "マルチプレイ",
    children: [
      { id: "Coop", label: "協力プレイ" },
      { id: "OnlineCoop", label: "オンライン協力" },
      { id: "LocalCoop", label: "ローカル協力" },
      { id: "PvP", label: "対戦（PvP）" },
      { id: "PvE", label: "対NPC（PvE）" },
      { id: "MOBA", label: "MOBA" },
      { id: "BattleRoyale", label: "バトルロイヤル" },
    ],
  },

  {
    id: "ArtStyle",
    label: "見た目・アートスタイル",
    children: [
      { id: "PixelGraphics", label: "ドット絵" },
      { id: "HandDrawn", label: "手描き風" },
      { id: "Anime", label: "アニメ調" },
      { id: "LowPoly", label: "ローポリ" },
      { id: "Stylized", label: "スタイライズ" },
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
    <Box className="liquid-glass-card-side">
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
