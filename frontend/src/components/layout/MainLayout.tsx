"use client";

import { LeftPanel } from "./LeftPanel";
import { CenterPanel } from "./CenterPanel";
import { RightPanel } from "./RightPanel";

export function MainLayout() {
  return (
    <div className="flex h-screen flex-col">
      {/* Header */}
      <header className="flex h-12 shrink-0 items-center border-b border-border bg-panel-bg px-4">
        <h1 className="text-lg font-semibold text-foreground">
          Stress-Strain Analyzer
        </h1>
      </header>

      {/* 3-pane layout */}
      <div className="grid flex-1 grid-cols-[280px_1fr_320px] overflow-hidden">
        <LeftPanel />
        <CenterPanel />
        <RightPanel />
      </div>
    </div>
  );
}
