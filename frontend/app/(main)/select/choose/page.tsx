"use client";

import React, { useState } from "react";
import SidebarSelect from "@/components/main/select-main/SidebarSelect";
import SelectedGames from "@/components/main/selected-games/SelectedGames";

export default function ChoosePage() {
  const [games, setGames] = useState<any[]>([]);

  return (
    <div style={{ display: "flex", gap: 16 }}>
      {/* 左フィルタ */}
      <SidebarSelect onResults={setGames} />

      {/* 右の一覧 */}
      <div style={{ flex: 1 }}>
        <div style={{ padding: 8 }}>
          <div>受け取った games の型: {Array.isArray(games) ? "array" : typeof games}</div>
          <div>games.length: {Array.isArray(games) ? games.length : "N/A"}</div>
          <pre style={{ whiteSpace: "pre-wrap", fontSize: 12 }}>
            {JSON.stringify(games?.slice?.(0, 2) ?? games, null, 2)}
          </pre>
        </div>

        <SelectedGames games={games} />
      </div>
    </div>
  );
}
