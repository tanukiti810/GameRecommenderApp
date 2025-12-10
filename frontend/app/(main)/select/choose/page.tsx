"use client";

import React, { useMemo, useState } from "react";
import SidebarSelect from "@/components/main/select-main/SidebarSelect";
import SelectedGames from "@/components/main/selected-games/SelectedGames";

type RawGame = {
  appid?: number;
  name?: string;
  price?: number | string;
  image?: string | null;
  description?: string | null;
};

type DisplayGame = {
  id: number;
  title: string;
  price: number;
  image: string;
  description: string;
};

export default function ChoosePage() {
  const [games, setGames] = useState<RawGame[]>([]);
  const uniqueDisplayGames = useMemo<DisplayGame[]>(() => {
    const displayGames = games
      .map((g) => {
        const id = g.appid;
        if (!id) return null;

        return {
          id,
          title: g.name ?? "",
          price: Number(g.price ?? 0),
          image:
            g.image ??
            `https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/${id}/header.jpg`,
          description: g.description ?? "",
        } as DisplayGame;
      })
      .filter(Boolean) as DisplayGame[];


    return Array.from(new Map(displayGames.map((g) => [g.id, g])).values());
  }, [games]);

  return (
    <div style={{ display: "flex", gap: 16 }}>
      {/* 左フィルタ */}
      <SidebarSelect onResults={setGames} />

      {/* 右の一覧 */}
      <div style={{ flex: 1 }}>
        <SelectedGames games={uniqueDisplayGames} />
      </div>
    </div>
  );
}
