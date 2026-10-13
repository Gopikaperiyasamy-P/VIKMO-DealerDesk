from django.http import HttpResponse

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VIKMO INTELLIGENCE — Dealer Operations & Inventory Command Center</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-base: #070a12;
      --bg-sidebar: #0b101d;
      --bg-surface: #111827;
      --bg-surface-elevated: #162032;
      --bg-card: rgba(17, 24, 39, 0.75);
      --border-subtle: rgba(255, 255, 255, 0.07);
      --border-hover: rgba(255, 255, 255, 0.15);
      --primary: #6366f1;
      --primary-glow: rgba(99, 102, 241, 0.25);
      --cyan: #06b6d4;
      --cyan-glow: rgba(6, 182, 212, 0.2);
      --violet: #8b5cf6;
      --violet-glow: rgba(139, 92, 246, 0.2);
      --emerald: #10b981;
      --emerald-glow: rgba(16, 185, 129, 0.2);
      --amber: #f59e0b;
      --amber-glow: rgba(245, 158, 11, 0.2);
      --rose: #f43f5e;
      --rose-glow: rgba(244, 63, 94, 0.2);
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --text-subtle: #64748b;
      --radius-sm: 6px;
      --radius-md: 10px;
      --radius-lg: 14px;
      --radius-xl: 18px;
      --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg-base);
      color: var(--text-main);
      font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      min-height: 100vh;
      display: flex;
      overflow-x: hidden;
      line-height: 1.5;
    }
    /* SIDEBAR */
    #sidebar {
      width: 260px;
      background: var(--bg-sidebar);
      border-right: 1px solid var(--border-subtle);
      display: flex;
      flex-direction: column;
      flex-shrink: 0;
      position: sticky;
      top: 0;
      height: 100vh;
      z-index: 40;
      transition: width 0.25s ease;
    }
    #sidebar.collapsed { width: 76px; }
    .brand-box {
      padding: 1.25rem 1.5rem;
      display: flex;
      align-items: center;
      gap: 0.85rem;
      border-bottom: 1px solid var(--border-subtle);
      background: rgba(11, 16, 29, 0.9);
    }
    .brand-icon {
      width: 36px;
      height: 36px;
      background: linear-gradient(135deg, var(--cyan), var(--primary));
      border-radius: var(--radius-md);
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 1.15rem;
      color: white;
      box-shadow: 0 0 16px var(--cyan-glow);
      flex-shrink: 0;
    }
    .brand-info { overflow: hidden; white-space: nowrap; }
    .brand-title {
      font-weight: 800;
      font-size: 1.05rem;
      letter-spacing: -0.02em;
      background: linear-gradient(135deg, #ffffff 40%, var(--cyan) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .brand-sub { font-size: 0.7rem; color: var(--text-muted); font-weight: 500; }
    .nav-menu {
      flex: 1;
      padding: 1rem 0.75rem;
      display: flex;
      flex-direction: column;
      gap: 0.35rem;
      overflow-y: auto;
    }
    .nav-item {
      display: flex;
      align-items: center;
      gap: 0.85rem;
      padding: 0.7rem 0.9rem;
      border-radius: var(--radius-md);
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.88rem;
      font-weight: 600;
      cursor: pointer;
      transition: var(--transition);
      border: 1px solid transparent;
      white-space: nowrap;
    }
    .nav-item:hover {
      color: var(--text-main);
      background: rgba(255, 255, 255, 0.04);
      border-color: var(--border-subtle);
    }
    .nav-item.active {
      color: #fff;
      background: linear-gradient(90deg, rgba(99, 102, 241, 0.18), rgba(6, 182, 212, 0.12));
      border-color: rgba(99, 102, 241, 0.35);
      box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);
    }
    .nav-icon { width: 20px; height: 20px; flex-shrink: 0; display: flex; align-items: center; justify-content: center; }
    .nav-badge {
      margin-left: auto;
      font-size: 0.7rem;
      font-weight: 700;
      padding: 0.15rem 0.45rem;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.08);
      color: var(--text-muted);
    }
    .nav-item.active .nav-badge { background: var(--primary); color: white; }
    .sidebar-footer {
      padding: 1rem 1.25rem;
      border-top: 1px solid var(--border-subtle);
      font-size: 0.75rem;
      color: var(--text-subtle);
    }

    /* MAIN CONTENT */
    #content-wrap {
      flex: 1;
      display: flex;
      flex-direction: column;
      min-width: 0;
      overflow-y: auto;
      height: 100vh;
    }

    /* TOP HEADER */
    header {
      background: rgba(11, 16, 29, 0.85);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--border-subtle);
      padding: 0.85rem 2rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      position: sticky;
      top: 0;
      z-index: 30;
      gap: 1rem;
    }
    .header-left { display: flex; align-items: center; gap: 1rem; }
    .toggle-sidebar-btn {
      background: transparent;
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      width: 34px;
      height: 34px;
      border-radius: var(--radius-sm);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      transition: var(--transition);
    }
    .toggle-sidebar-btn:hover { color: var(--text-main); border-color: var(--border-hover); }
    .header-title-box h1 {
      font-size: 1.15rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      display: flex;
      align-items: center;
      gap: 0.6rem;
    }
    .header-subtitle { font-size: 0.75rem; color: var(--text-muted); }
    .track-badge {
      background: linear-gradient(135deg, rgba(139, 92, 246, 0.25), rgba(99, 102, 241, 0.25));
      border: 1px solid rgba(139, 92, 246, 0.5);
      color: #c4b5fd;
      font-size: 0.7rem;
      font-weight: 700;
      padding: 0.2rem 0.6rem;
      border-radius: 9999px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .header-right { display: flex; align-items: center; gap: 1rem; }
    .connection-pill {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      font-size: 0.8rem;
      background: rgba(16, 185, 129, 0.08);
      color: var(--emerald);
      padding: 0.35rem 0.8rem;
      border-radius: 9999px;
      border: 1px solid rgba(16, 185, 129, 0.25);
      font-weight: 600;
    }
    .pulse-dot {
      width: 8px;
      height: 8px;
      background: var(--emerald);
      border-radius: 50%;
      box-shadow: 0 0 10px var(--emerald);
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
      70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
      100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    .last-refresh { font-size: 0.75rem; color: var(--text-subtle); }
    .btn-refresh {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      padding: 0.4rem 0.85rem;
      border-radius: var(--radius-sm);
      font-size: 0.8rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 0.4rem;
      cursor: pointer;
      transition: var(--transition);
    }
    .btn-refresh:hover { background: rgba(255, 255, 255, 0.12); border-color: var(--border-hover); }

    /* CONTENT BODY & VIEWS */
    main {
      padding: 2rem;
      display: flex;
      flex-direction: column;
      gap: 2rem;
      max-width: 1600px;
      margin: 0 auto;
      width: 100%;
    }
    .view-section { display: none; }
    .view-section.active-view { display: flex; flex-direction: column; gap: 2rem; animation: fadeIn 0.25s ease; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(4px); } to { opacity: 1; transform: translateY(0); } }

    /* CARDS & PANELS */
    .glass-card {
      background: var(--bg-card);
      backdrop-filter: blur(12px);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 1.5rem;
      box-shadow: 0 8px 24px -4px rgba(0, 0, 0, 0.4);
      position: relative;
    }
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 1.25rem;
      padding-bottom: 0.85rem;
      border-bottom: 1px solid var(--border-subtle);
    }
    .card-title {
      font-size: 1.05rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 0.6rem;
      letter-spacing: -0.01em;
    }
    .card-subtitle { font-size: 0.78rem; color: var(--text-muted); font-weight: 400; }

    /* LIVE INVENTORY OVERVIEW (PRIORITY A) */
    .kpi-grid {
      display: grid;
      grid-template-columns: 1.5fr repeat(5, 1fr);
      gap: 1.25rem;
    }
    @media (max-width: 1400px) {
      .kpi-grid { grid-template-columns: 1fr 1fr 1fr; }
    }
    @media (max-width: 768px) {
      .kpi-grid { grid-template-columns: 1fr; }
    }
    .kpi-hero-card {
      background: linear-gradient(135deg, rgba(6, 182, 212, 0.12) 0%, rgba(99, 102, 241, 0.1) 100%);
      border: 1px solid rgba(6, 182, 212, 0.35);
      border-radius: var(--radius-lg);
      padding: 1.6rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 12px 32px rgba(6, 182, 212, 0.15);
      position: relative;
      overflow: hidden;
    }
    .kpi-hero-card::after {
      content: '';
      position: absolute;
      top: -50px;
      right: -50px;
      width: 120px;
      height: 120px;
      background: var(--cyan);
      opacity: 0.15;
      filter: blur(40px);
      border-radius: 50%;
    }
    .kpi-hero-title {
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--cyan);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .kpi-hero-value {
      font-size: 2.75rem;
      font-weight: 800;
      line-height: 1.1;
      margin: 0.75rem 0 0.5rem;
      letter-spacing: -0.03em;
      background: linear-gradient(135deg, #ffffff 60%, var(--cyan) 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      font-family: 'JetBrains Mono', monospace;
    }
    .kpi-hero-desc {
      font-size: 0.78rem;
      color: var(--text-muted);
      line-height: 1.4;
    }
    .kpi-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-subtle);
      border-radius: var(--radius-lg);
      padding: 1.25rem 1.4rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: var(--transition);
    }
    .kpi-card:hover { border-color: var(--border-hover); transform: translateY(-2px); }
    .kpi-label {
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .kpi-value {
      font-size: 1.75rem;
      font-weight: 800;
      margin: 0.5rem 0 0.25rem;
      font-family: 'JetBrains Mono', monospace;
      letter-spacing: -0.02em;
    }
    .kpi-desc { font-size: 0.72rem; color: var(--text-subtle); }
    .color-in-stock { color: var(--emerald); }
    .color-low-stock { color: var(--amber); }
    .color-out-stock { color: var(--rose); }
    .color-value { color: var(--cyan); }
    .color-unique { color: var(--violet); }

    /* VISUAL ANALYTICS SECTION */
    .analytics-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.5rem;
    }
    @media (max-width: 1024px) {
      .analytics-grid { grid-template-columns: 1fr; }
    }
    .chart-container {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 2rem;
      padding: 1rem 0;
    }
    .chart-legend { display: flex; flex-direction: column; gap: 0.75rem; }
    .legend-item { display: flex; align-items: center; gap: 0.6rem; font-size: 0.85rem; }
    .legend-color { width: 12px; height: 12px; border-radius: 3px; flex-shrink: 0; }
    .mini-table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.85rem;
    }
    .mini-table th {
      text-align: left;
      padding: 0.6rem 0.75rem;
      font-size: 0.72rem;
      text-transform: uppercase;
      color: var(--text-muted);
      border-bottom: 1px solid var(--border-subtle);
    }
    .mini-table td {
      padding: 0.6rem 0.75rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.03);
    }
    .mini-table tr:hover td { background: rgba(255, 255, 255, 0.02); }

    /* INVENTORY EXPLORER (FULL-WIDTH) */
    .controls-row {
      display: flex;
      flex-wrap: wrap;
      gap: 0.85rem;
      align-items: center;
      margin-bottom: 1.25rem;
    }
    .search-input-wrap {
      flex: 1;
      min-width: 260px;
      position: relative;
    }
    .search-input-wrap input {
      width: 100%;
      padding-left: 2.4rem;
    }
    .search-icon {
      position: absolute;
      left: 0.85rem;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      pointer-events: none;
    }
    .filter-chips { display: flex; gap: 0.4rem; flex-wrap: wrap; }
    .chip {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-subtle);
      color: var(--text-muted);
      padding: 0.45rem 0.85rem;
      border-radius: var(--radius-sm);
      font-size: 0.8rem;
      font-weight: 600;
      cursor: pointer;
      transition: var(--transition);
    }
    .chip:hover { border-color: var(--border-hover); color: var(--text-main); }
    .chip.active-chip {
      background: rgba(99, 102, 241, 0.15);
      border-color: var(--primary);
      color: #fff;
    }
    input, select {
      font-family: inherit;
      border-radius: var(--radius-sm);
      border: 1px solid var(--border-subtle);
      padding: 0.55rem 0.85rem;
      background: var(--bg-surface);
      color: white;
      font-size: 0.85rem;
    }
    input:focus, select:focus {
      outline: none;
      border-color: var(--primary);
      box-shadow: 0 0 0 2px var(--primary-glow);
    }

    /* DATA TABLE */
    .table-responsive {
      overflow-x: auto;
      border-radius: var(--radius-md);
      border: 1px solid var(--border-subtle);
    }
    .data-table {
      width: 100%;
      border-collapse: collapse;
      text-align: left;
      font-size: 0.86rem;
    }
    .data-table th {
      background: var(--bg-surface-elevated);
      padding: 0.85rem 1rem;
      font-weight: 700;
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      color: var(--text-muted);
      border-bottom: 1px solid var(--border-subtle);
    }
    .data-table td {
      padding: 0.85rem 1rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.04);
      vertical-align: middle;
    }
    .data-table tr:hover td { background: rgba(255, 255, 255, 0.02); }
    .sku-code {
      font-family: 'JetBrains Mono', monospace;
      font-weight: 600;
      color: var(--cyan);
      background: rgba(6, 182, 212, 0.08);
      padding: 0.15rem 0.45rem;
      border-radius: 4px;
      font-size: 0.82rem;
      display: inline-block;
    }
    .badge-status {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      font-size: 0.72rem;
      font-weight: 700;
      padding: 0.2rem 0.55rem;
      border-radius: 999px;
      text-transform: uppercase;
      letter-spacing: 0.03em;
    }
    .badge-in-stock { background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.3); }
    .badge-low-stock { background: rgba(245, 158, 11, 0.15); color: #fbbf24; border: 1px solid rgba(245, 158, 11, 0.3); }
    .badge-out-stock { background: rgba(244, 63, 94, 0.15); color: #fb7185; border: 1px solid rgba(244, 63, 94, 0.3); }
    .stock-number {
      font-family: 'JetBrains Mono', monospace;
      font-weight: 700;
      font-size: 0.95rem;
    }
    .btn-action {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--border-subtle);
      color: var(--text-main);
      padding: 0.35rem 0.75rem;
      border-radius: var(--radius-sm);
      font-size: 0.78rem;
      font-weight: 600;
      cursor: pointer;
      transition: var(--transition);
    }
    .btn-action:hover {
      background: var(--primary);
      border-color: var(--primary);
      color: white;
    }
    .pagination-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 1.25rem;
      font-size: 0.82rem;
      color: var(--text-muted);
    }
    .pagination-btns { display: flex; gap: 0.5rem; align-items: center; }

    /* AI ASSISTANT PANEL */
    .assistant-layout {
      display: grid;
      grid-template-columns: 1fr 340px;
      gap: 1.5rem;
    }
    @media (max-width: 1024px) {
      .assistant-layout { grid-template-columns: 1fr; }
    }
    .chat-messages {
      height: 480px;
      overflow-y: auto;
      display: flex;
      flex-direction: column;
      gap: 1rem;
      padding-right: 0.5rem;
      margin-bottom: 1.25rem;
    }
    .msg-bubble {
      max-width: 82%;
      padding: 0.9rem 1.15rem;
      border-radius: var(--radius-lg);
      font-size: 0.9rem;
      line-height: 1.55;
    }
    .msg-bubble.user {
      align-self: flex-end;
      background: linear-gradient(135deg, var(--violet), var(--primary));
      color: white;
      border-bottom-right-radius: 3px;
      box-shadow: 0 4px 14px var(--primary-glow);
    }
    .msg-bubble.bot {
      align-self: flex-start;
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-subtle);
      border-bottom-left-radius: 3px;
    }
    .tool-execution-pill {
      display: inline-flex;
      align-items: center;
      gap: 0.35rem;
      background: rgba(99, 102, 241, 0.15);
      border: 1px solid rgba(99, 102, 241, 0.3);
      color: #a5b4fc;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.72rem;
      padding: 0.2rem 0.5rem;
      border-radius: 4px;
      margin-top: 0.5rem;
    }
    .cited-cards-row {
      display: flex;
      flex-wrap: wrap;
      gap: 0.5rem;
      margin-top: 0.65rem;
    }
    .cited-card {
      background: rgba(11, 16, 29, 0.7);
      border: 1px solid rgba(6, 182, 212, 0.3);
      border-radius: var(--radius-sm);
      padding: 0.4rem 0.65rem;
      font-size: 0.76rem;
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    .chat-prompts-bar {
      display: flex;
      flex-wrap: wrap;
      gap: 0.45rem;
      margin-bottom: 0.85rem;
    }
    .prompt-chip {
      background: rgba(139, 92, 246, 0.1);
      border: 1px solid rgba(139, 92, 246, 0.25);
      color: #ddd6fe;
      padding: 0.35rem 0.7rem;
      border-radius: 999px;
      font-size: 0.76rem;
      cursor: pointer;
      transition: var(--transition);
    }
    .prompt-chip:hover {
      background: rgba(139, 92, 246, 0.25);
      border-color: var(--violet);
      color: #fff;
    }
    .chat-input-bar {
      display: flex;
      gap: 0.75rem;
    }
    .chat-input-bar input { flex: 1; }
    .btn-send {
      background: linear-gradient(135deg, var(--violet), var(--primary));
      border: none;
      color: white;
      font-weight: 700;
      padding: 0.65rem 1.4rem;
      border-radius: var(--radius-sm);
      cursor: pointer;
      transition: var(--transition);
    }
    .btn-send:hover { opacity: 0.9; transform: translateY(-1px); }

    /* FORECASTING & REORDER VISUALS */
    .forecast-bar-chart {
      display: flex;
      align-items: flex-end;
      gap: 1.5rem;
      height: 200px;
      padding: 1rem 0 2rem;
      border-bottom: 1px solid var(--border-subtle);
    }
    .f-bar-group {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      height: 100%;
      justify-content: flex-end;
      gap: 0.5rem;
    }
    .f-bar-fill {
      width: 100%;
      max-width: 54px;
      background: linear-gradient(180deg, var(--cyan), var(--primary));
      border-radius: 4px 4px 0 0;
      transition: height 0.4s ease;
      position: relative;
    }
    .f-bar-val {
      font-size: 0.75rem;
      font-weight: 700;
      font-family: 'JetBrains Mono', monospace;
      color: #fff;
    }
    .f-bar-lbl {
      font-size: 0.72rem;
      color: var(--text-muted);
    }

    /* MODAL / DRAWER */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0, 0, 0, 0.7);
      backdrop-filter: blur(8px);
      z-index: 100;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 1.5rem;
    }
    .modal-overlay.active { display: flex; }
    .modal-card {
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-hover);
      border-radius: var(--radius-xl);
      max-width: 640px;
      width: 100%;
      max-height: 90vh;
      overflow-y: auto;
      padding: 2rem;
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
      position: relative;
    }
    .modal-close {
      position: absolute;
      top: 1.25rem;
      right: 1.25rem;
      background: transparent;
      border: none;
      color: var(--text-muted);
      font-size: 1.4rem;
      cursor: pointer;
    }
    .modal-close:hover { color: white; }

    /* LOADING & TOAST */
    .skeleton {
      background: linear-gradient(90deg, rgba(255,255,255,0.03) 25%, rgba(255,255,255,0.08) 50%, rgba(255,255,255,0.03) 75%);
      background-size: 200% 100%;
      animation: loading 1.5s infinite;
      border-radius: 4px;
    }
    @keyframes loading { 0% { background-position: 200% 0; } 100% { background-position: -200% 0; } }
  </style>
</head>
<body>
  <!-- SIDEBAR NAVIGATION -->
  <aside id="sidebar">
    <div class="brand-box">
      <div class="brand-icon">V</div>
      <div class="brand-info">
        <div class="brand-title">VIKMO INTELLIGENCE</div>
        <div class="brand-sub">Inventory Command Center</div>
      </div>
    </div>

    <nav class="nav-menu">
      <div class="nav-item active" onclick="switchView('overview')">
        <span class="nav-icon">📊</span>
        <span>Overview</span>
      </div>
      <div class="nav-item" onclick="switchView('explorer')">
        <span class="nav-icon">📦</span>
        <span>Inventory Explorer</span>
        <span class="nav-badge" id="navProductCount">600</span>
      </div>
      <div class="nav-item" onclick="switchView('assistant')">
        <span class="nav-icon">🤖</span>
        <span>AI Assistant</span>
        <span class="nav-badge" style="background: rgba(139, 92, 246, 0.3); color: #c4b5fd;">Tool-Call</span>
      </div>
      <div class="nav-item" onclick="switchView('forecasting')">
        <span class="nav-icon">📈</span>
        <span>Demand Forecast</span>
        <span class="nav-badge">40 SKUs</span>
      </div>
      <div class="nav-item" onclick="switchView('reorder')">
        <span class="nav-icon">⚡</span>
        <span>Reorder Center</span>
        <span class="nav-badge" id="navReorderBadge" style="background: rgba(245, 158, 11, 0.2); color: #fbbf24;">Safety</span>
      </div>
      <div class="nav-item" onclick="switchView('orders')">
        <span class="nav-icon">📋</span>
        <span>Orders Ledger</span>
      </div>
      <div class="nav-item" onclick="switchView('devtools')">
        <span class="nav-icon">🛠️</span>
        <span>API Health & Tools</span>
      </div>
    </nav>

    <div class="sidebar-footer">
      <div>PostgreSQL • Django 5.2</div>
      <div style="color: var(--cyan); margin-top: 0.2rem;">Track: AI / ML Intern</div>
    </div>
  </aside>

  <!-- CONTENT WRAPPER -->
  <div id="content-wrap">
    <!-- TOP HEADER -->
    <header>
      <div class="header-left">
        <button class="toggle-sidebar-btn" onclick="toggleSidebar()" title="Toggle Sidebar">☰</button>
        <div class="header-title-box">
          <h1>
            <span>DealerDesk Command</span>
            <span class="track-badge">AI / ML Track</span>
          </h1>
          <div class="header-subtitle">Real-time PostgreSQL Relational Grounding & ML Reorder Intelligence</div>
        </div>
      </div>

      <div class="header-right">
        <div class="connection-pill" id="healthPill">
          <div class="pulse-dot"></div>
          <span id="healthStatusText">API Connected (2ms)</span>
        </div>
        <div class="last-refresh" id="lastRefreshText">Refreshed: Just now</div>
        <button class="btn-refresh" onclick="refreshAllData()">
          <span>🔄</span>
          <span>Refresh All</span>
        </button>
      </div>
    </header>

    <main>
      <!-- ========================================== -->
      <!-- VIEW 1: OVERVIEW & LIVE INVENTORY (PRIORITY A) -->
      <!-- ========================================== -->
      <section id="view-overview" class="view-section active-view">
        <!-- HERO & KPI METRICS (SECTION 2 IN PROMPT) -->
        <div class="kpi-grid">
          <!-- HERO CARD: TOTAL LIVE STOCK UNITS -->
          <div class="kpi-hero-card">
            <div>
              <div class="kpi-hero-title">
                <span>Total Live Stock Units</span>
                <span style="font-size: 0.72rem; opacity: 0.8;">PostgreSQL Aggregate</span>
              </div>
              <div class="kpi-hero-value" id="kpiTotalStock">—</div>
            </div>
            <div class="kpi-hero-desc">
              Sum of live available inventory across all unique catalogue products: <code>sum(stock for all unique SKUs)</code>. Excludes duplicates.
            </div>
          </div>

          <!-- KPI 1: UNIQUE PRODUCTS -->
          <div class="kpi-card">
            <div class="kpi-label">
              <span>Unique Products</span>
              <span class="color-unique">📦</span>
            </div>
            <div class="kpi-value color-unique" id="kpiUniqueProducts">—</div>
            <div class="kpi-desc">Total distinct SKUs in active catalogue</div>
          </div>

          <!-- KPI 2: IN-STOCK PRODUCTS -->
          <div class="kpi-card">
            <div class="kpi-label">
              <span>In-Stock Products</span>
              <span class="color-in-stock">✓</span>
            </div>
            <div class="kpi-value color-in-stock" id="kpiInStock">—</div>
            <div class="kpi-desc">Products with &gt; 10 units available</div>
          </div>

          <!-- KPI 3: LOW-STOCK PRODUCTS -->
          <div class="kpi-card">
            <div class="kpi-label">
              <span>Low-Stock Alerts</span>
              <span class="color-low-stock">⚠️</span>
            </div>
            <div class="kpi-value color-low-stock" id="kpiLowStock">—</div>
            <div class="kpi-desc">Products with 1 to 10 units remaining</div>
          </div>

          <!-- KPI 4: OUT-OF-STOCK -->
          <div class="kpi-card">
            <div class="kpi-label">
              <span>Out-of-Stock</span>
              <span class="color-out-stock">✕</span>
            </div>
            <div class="kpi-value color-out-stock" id="kpiOutStock">—</div>
            <div class="kpi-desc">Products with exactly 0 units in stock</div>
          </div>

          <!-- KPI 5: TOTAL INVENTORY VALUE -->
          <div class="kpi-card">
            <div class="kpi-label">
              <span>Inventory Value</span>
              <span class="color-value">₹</span>
            </div>
            <div class="kpi-value color-value" id="kpiInventoryValue" style="font-size: 1.45rem;">—</div>
            <div class="kpi-desc">Exact valuation: <code>sum(stock × price)</code></div>
          </div>
        </div>

        <!-- VISUAL ANALYTICS (SECTION 4 IN PROMPT) -->
        <div class="analytics-grid">
          <!-- STOCK DISTRIBUTION DONUT/BAR CHART -->
          <div class="glass-card">
            <div class="card-header">
              <div>
                <div class="card-title">📊 Catalogue Stock Health Distribution</div>
                <div class="card-subtitle">Real-time health breakdown calculated across entire catalogue</div>
              </div>
            </div>
            <div class="chart-container">
              <svg width="160" height="160" viewBox="0 0 160 160" id="distributionSvg">
                <!-- SVG donut dynamically populated -->
                <circle cx="80" cy="80" r="60" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="20"/>
              </svg>
              <div class="chart-legend" id="chartLegend">
                <div class="legend-item">
                  <div class="legend-color" style="background: var(--emerald);"></div>
                  <div>In Stock (&gt;10 units): <b id="legInStock">498</b> (<span id="legInPct">83.0%</span>)</div>
                </div>
                <div class="legend-item">
                  <div class="legend-color" style="background: var(--amber);"></div>
                  <div>Low Stock (1-10 units): <b id="legLowStock">59</b> (<span id="legLowPct">9.8%</span>)</div>
                </div>
                <div class="legend-item">
                  <div class="legend-color" style="background: var(--rose);"></div>
                  <div>Out of Stock (0 units): <b id="legOutStock">43</b> (<span id="legOutPct">7.2%</span>)</div>
                </div>
              </div>
            </div>
          </div>

          <!-- TOP LOW-STOCK TABLE -->
          <div class="glass-card">
            <div class="card-header">
              <div>
                <div class="card-title">⚠️ Top Critical Low-Stock Products</div>
                <div class="card-subtitle">Items requiring urgent warehouse attention (1–10 units)</div>
              </div>
              <button class="btn-action" onclick="switchView('explorer'); setExplorerFilter('low_stock');">View All</button>
            </div>
            <table class="mini-table" id="topLowStockTable">
              <thead>
                <tr>
                  <th>SKU</th>
                  <th>Product Name</th>
                  <th>Fitment</th>
                  <th>Price</th>
                  <th>Stock</th>
                </tr>
              </thead>
              <tbody id="topLowStockBody">
                <tr><td colspan="5" style="text-align:center;">Loading low stock records...</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- ========================================== -->
      <!-- VIEW 2: INVENTORY EXPLORER (SECTION 3 IN PROMPT) -->
      <!-- ========================================== -->
      <section id="view-explorer" class="view-section">
        <div class="glass-card">
          <div class="card-header">
            <div>
              <div class="card-title">📦 Live Inventory Explorer</div>
              <div class="card-subtitle">Full catalogue stock visibility with server-side search, filtering, and live adjustment</div>
            </div>
            <div style="font-size: 0.8rem; color: var(--text-muted);" id="explorerStatsText">
              Showing 0 of 600 products
            </div>
          </div>

          <!-- SEARCH & FILTER CONTROLS -->
          <div class="controls-row">
            <div class="search-input-wrap">
              <span class="search-icon">🔍</span>
              <input type="text" id="explorerSearch" placeholder="Search by SKU, product name, brand, or vehicle..." oninput="debounceExplorerSearch()">
            </div>

            <div class="filter-chips">
              <div class="chip active-chip" data-status="" onclick="setExplorerFilter('')">All</div>
              <div class="chip" data-status="in_stock" onclick="setExplorerFilter('in_stock')">In Stock (&gt;10)</div>
              <div class="chip" data-status="low_stock" onclick="setExplorerFilter('low_stock')">Low Stock (1–10)</div>
              <div class="chip" data-status="out_of_stock" onclick="setExplorerFilter('out_of_stock')">Out of Stock (0)</div>
            </div>

            <select id="explorerCategory" onchange="loadExplorerProducts(1)">
              <option value="">All Categories</option>
            </select>

            <select id="explorerSort" onchange="loadExplorerProducts(1)">
              <option value="stock">Stock: Low to High</option>
              <option value="-stock">Stock: High to Low</option>
              <option value="name">Name: A to Z</option>
              <option value="sku">SKU Code</option>
              <option value="-price">Price: High to Low</option>
              <option value="price">Price: Low to High</option>
            </select>
          </div>

          <!-- TABLE -->
          <div class="table-responsive">
            <table class="data-table">
              <thead>
                <tr>
                  <th>SKU</th>
                  <th>Product Name & Brand</th>
                  <th>Category</th>
                  <th>Compatible Vehicle</th>
                  <th>Current Stock</th>
                  <th>Unit Price</th>
                  <th>Line Valuation</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody id="explorerTableBody">
                <!-- Data populated dynamically -->
              </tbody>
            </table>
          </div>

          <!-- PAGINATION -->
          <div class="pagination-bar">
            <div>
              Page <b id="currentPageNum">1</b> of <b id="totalPageNum">1</b> (<span id="totalItemsCount">0</span> items total)
            </div>
            <div class="pagination-btns">
              <button class="btn-action" id="btnPrevPage" onclick="changePage(-1)">← Previous</button>
              <button class="btn-action" id="btnNextPage" onclick="changePage(1)">Next →</button>
              <select id="pageSizeSelect" onchange="changePageSize(this.value)" style="margin-left: 0.5rem; padding: 0.35rem 0.5rem;">
                <option value="15">15 / page</option>
                <option value="25" selected>25 / page</option>
                <option value="50">50 / page</option>
              </select>
            </div>
          </div>
        </div>
      </section>

      <!-- ========================================== -->
      <!-- VIEW 3: AI DEALER ASSISTANT (SECTION 5 IN PROMPT) -->
      <!-- ========================================== -->
      <section id="view-assistant" class="view-section">
        <div class="assistant-layout">
          <!-- MAIN CHAT PANEL -->
          <div class="glass-card" style="display: flex; flex-direction: column;">
            <div class="card-header">
              <div>
                <div class="card-title">🤖 DealerDesk AI Assistant</div>
                <div class="card-subtitle">Grounded in PostgreSQL live stock with real function tool calling</div>
              </div>
              <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: var(--violet);">
                POST /api/assistant/chat/
              </div>
            </div>

            <!-- PROMPTS CHIPS -->
            <div class="chat-prompts-bar">
              <span class="prompt-chip" onclick="sendQuickPrompt('What is the total live stock available?')">What is the total live stock available?</span>
              <span class="prompt-chip" onclick="sendQuickPrompt('Show all products with low stock.')">Show all products with low stock</span>
              <span class="prompt-chip" onclick="sendQuickPrompt('Check stock for BRK-1044.')">Check stock for BRK-1044</span>
              <span class="prompt-chip" onclick="sendQuickPrompt('Find brake pads compatible with Pulsar 150.')">Brake pads for Pulsar 150</span>
              <span class="prompt-chip" onclick="sendQuickPrompt('Which products need reordering?')">Which products need reordering?</span>
              <span class="prompt-chip" onclick="sendQuickPrompt('Forecast demand for FIL-1016.')">Forecast demand for FIL-1016</span>
            </div>

            <!-- CHAT BUBBLES -->
            <div class="chat-messages" id="chatMessages">
              <div class="msg-bubble bot">
                👋 Welcome to <b>VIKMO DealerDesk Intelligence</b>. I am your grounded AI parts assistant.<br><br>
                You can ask about live inventory aggregates, part fitment across vehicles, live stock and prices, 4-week demand forecasts, or tell me to generate DRAFT orders.
              </div>
            </div>

            <!-- INPUT BAR -->
            <div class="chat-input-bar">
              <input type="text" id="assistantInput" placeholder="Ask about live inventory, vehicle parts, stock, or draft orders..." onkeypress="if(event.key==='Enter') sendAssistantMessage()">
              <button class="btn-send" onclick="sendAssistantMessage()">Send</button>
            </div>
          </div>

          <!-- ASSISTANT CAPABILITY & CONTEXT PANEL -->
          <div class="glass-card" style="display: flex; flex-direction: column; gap: 1.25rem;">
            <div class="card-header" style="margin-bottom: 0;">
              <div class="card-title" style="font-size: 0.95rem;">⚡ Real Tool Calling</div>
            </div>

            <div style="font-size: 0.8rem; color: var(--text-muted); line-height: 1.5;">
              The LLM invokes functions against our backend server. Results are grounded directly in PostgreSQL database state.
            </div>

            <div style="display: flex; flex-direction: column; gap: 0.6rem; font-size: 0.78rem;">
              <div style="background: rgba(255,255,255,0.03); padding: 0.6rem; border-radius: var(--radius-sm); border: 1px solid var(--border-subtle);">
                <b style="color: var(--cyan);">search_parts</b>: Hybrid retrieval matching vehicle fitment, brand, name, and category.
              </div>
              <div style="background: rgba(255,255,255,0.03); padding: 0.6rem; border-radius: var(--radius-sm); border: 1px solid var(--border-subtle);">
                <b style="color: var(--emerald);">check_stock</b>: Real-time queries for stock quantities, prices, or catalogue aggregate.
              </div>
              <div style="background: rgba(255,255,255,0.03); padding: 0.6rem; border-radius: var(--radius-sm); border: 1px solid var(--border-subtle);">
                <b style="color: var(--violet);">create_draft_order</b>: Validates requested SKUs and creates a DRAFT order.
              </div>
            </div>

            <div style="margin-top: auto; padding: 0.85rem; background: rgba(99, 102, 241, 0.08); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: var(--radius-sm); font-size: 0.75rem; color: var(--text-muted);">
              🛡️ <b>Security Guardrail:</b> Catalogue text is treated as untrusted data. Prompt injection inside supplier descriptions cannot override assistant rules.
            </div>
          </div>
        </div>
      </section>

      <!-- ========================================== -->
      <!-- VIEW 4: DEMAND FORECASTING (SECTION 6 IN PROMPT) -->
      <!-- ========================================== -->
      <section id="view-forecasting" class="view-section">
        <div class="glass-card">
          <div class="card-header">
            <div>
              <div class="card-title">📈 4-Week ML Demand Forecasting</div>
              <div class="card-subtitle">Gradient Boosting model validated chronologically (MAE: 7.434 vs 9.074 baseline)</div>
            </div>
            <div style="display: flex; gap: 0.75rem; align-items: center;">
              <label style="font-size: 0.8rem; color: var(--text-muted);">Select Forecast SKU:</label>
              <select id="forecastSkuSelector" onchange="loadForecastData(this.value)">
                <!-- 40 SKUs populated dynamically -->
              </select>
            </div>
          </div>

          <div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 2rem;">
            <!-- CHART -->
            <div>
              <div style="font-size: 0.85rem; font-weight: 700; color: var(--text-muted); margin-bottom: 0.75rem;">
                Projected Weekly Units Sold (Horizon: Sep 28 – Oct 19, 2026)
              </div>
              <div class="forecast-bar-chart" id="forecastBars">
                <!-- Dynamically generated bars -->
              </div>
              <div style="margin-top: 1rem; display: flex; gap: 1.5rem; font-size: 0.8rem; color: var(--text-muted);">
                <div>Current Live Stock: <b id="fLiveStock" style="color: var(--cyan);">—</b> units</div>
                <div>Supplier Lead Time: <b id="fLeadTime" style="color: #fff;">—</b> weeks</div>
              </div>
            </div>

            <!-- TABLE -->
            <div>
              <div style="font-size: 0.85rem; font-weight: 700; color: var(--text-muted); margin-bottom: 0.75rem;">
                Forecast Breakdown by Week
              </div>
              <table class="mini-table">
                <thead>
                  <tr>
                    <th>Week Start (Monday)</th>
                    <th>Forecasted Units</th>
                    <th>Share of Lead Demand</th>
                  </tr>
                </thead>
                <tbody id="forecastTableBody">
                  <tr><td colspan="3">Select a SKU to view forecast</td></tr>
                </tbody>
              </table>
              <div style="margin-top: 1.25rem; font-size: 0.75rem; color: var(--text-subtle); line-height: 1.4;">
                Values sourced directly from <code>ml/forecast.csv</code> (160 rows). Features incorporate moving Diwali festival proximity and planned promotional spikes.
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- ========================================== -->
      <!-- VIEW 5: SMART REORDER CENTER (SECTION 7 IN PROMPT) -->
      <!-- ========================================== -->
      <section id="view-reorder" class="view-section">
        <div class="glass-card">
          <div class="card-header">
            <div>
              <div class="card-title">⚡ Smart Reorder Center</div>
              <div class="card-subtitle">Exact safety stock and reorder point calculations grounded in live PostgreSQL inventory</div>
            </div>
            <div style="display: flex; gap: 0.5rem;">
              <button class="chip active-chip" onclick="filterReorderTable('all', this)">All (40)</button>
              <button class="chip" onclick="filterReorderTable('needed', this)">Reorder Required</button>
              <button class="chip" onclick="filterReorderTable('sufficient', this)">Sufficient Stock</button>
            </div>
          </div>

          <div class="table-responsive">
            <table class="data-table">
              <thead>
                <tr>
                  <th>SKU</th>
                  <th>Current Live Stock</th>
                  <th>Lead Time (L)</th>
                  <th>Lead Demand</th>
                  <th>Safety Stock (σ)</th>
                  <th>Reorder Point</th>
                  <th>Suggested Reorder</th>
                  <th>Status</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody id="reorderTableBody">
                <tr><td colspan="9" style="text-align: center;">Loading reorder suggestions...</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- ========================================== -->
      <!-- VIEW 6: ORDERS LEDGER (SECTION 8 IN PROMPT) -->
      <!-- ========================================== -->
      <section id="view-orders" class="view-section">
        <div class="glass-card">
          <div class="card-header">
            <div>
              <div class="card-title">📋 Orders Management Ledger</div>
              <div class="card-subtitle">Historical and draft orders with exact 18% GST line calculations</div>
            </div>
            <button class="btn-action" onclick="openNewOrderModal()">+ New Draft Order</button>
          </div>

          <div class="table-responsive">
            <table class="data-table">
              <thead>
                <tr>
                  <th>Order Number</th>
                  <th>Dealer ID</th>
                  <th>Status</th>
                  <th>Items Count</th>
                  <th>Subtotal</th>
                  <th>GST (18%)</th>
                  <th>Grand Total</th>
                  <th>Created At</th>
                </tr>
              </thead>
              <tbody id="ordersTableBody">
                <tr><td colspan="8" style="text-align:center;">Loading orders ledger...</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <!-- ========================================== -->
      <!-- VIEW 7: DEVELOPER TOOLS & API HEALTH -->
      <!-- ========================================== -->
      <section id="view-devtools" class="view-section">
        <div class="glass-card">
          <div class="card-header">
            <div>
              <div class="card-title">🛠️ Developer Tools & System Health</div>
              <div class="card-subtitle">Direct access to backend endpoints and automated grading contracts</div>
            </div>
            <button class="btn-refresh" onclick="pingHealth()">Ping Health Check</button>
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
            <div style="display: flex; flex-direction: column; gap: 0.75rem;">
              <div style="font-weight: 700; font-size: 0.9rem; color: var(--cyan); margin-bottom: 0.25rem;">Live Contract Endpoints</div>

              <a class="endpoint-item" href="/api/health/" target="_blank" style="display: flex; justify-content: space-between; padding: 0.65rem 0.85rem; background: var(--bg-surface); border-radius: 6px; border: 1px solid var(--border-subtle); color: inherit; text-decoration: none;">
                <span><code>GET /api/health/</code></span>
                <span style="color: var(--emerald);">200 OK</span>
              </a>

              <a class="endpoint-item" href="/api/inventory/summary/" target="_blank" style="display: flex; justify-content: space-between; padding: 0.65rem 0.85rem; background: var(--bg-surface); border-radius: 6px; border: 1px solid var(--border-subtle); color: inherit; text-decoration: none;">
                <span><code>GET /api/inventory/summary/</code></span>
                <span style="color: var(--cyan);">Inventory Aggregate</span>
              </a>

              <a class="endpoint-item" href="/api/products/?page_size=5" target="_blank" style="display: flex; justify-content: space-between; padding: 0.65rem 0.85rem; background: var(--bg-surface); border-radius: 6px; border: 1px solid var(--border-subtle); color: inherit; text-decoration: none;">
                <span><code>GET /api/products/</code></span>
                <span>600 Catalogue Items</span>
              </a>

              <a class="endpoint-item" href="/api/dealers/?page_size=5" target="_blank" style="display: flex; justify-content: space-between; padding: 0.65rem 0.85rem; background: var(--bg-surface); border-radius: 6px; border: 1px solid var(--border-subtle); color: inherit; text-decoration: none;">
                <span><code>GET /api/dealers/</code></span>
                <span>25 Seeded Dealers</span>
              </a>

              <a class="endpoint-item" href="/api/reorder-suggestions/" target="_blank" style="display: flex; justify-content: space-between; padding: 0.65rem 0.85rem; background: var(--bg-surface); border-radius: 6px; border: 1px solid var(--border-subtle); color: inherit; text-decoration: none;">
                <span><code>GET /api/reorder-suggestions/</code></span>
                <span>40 Reorder Suggestions</span>
              </a>

              <a class="endpoint-item" href="/api/forecast/FIL-1016/" target="_blank" style="display: flex; justify-content: space-between; padding: 0.65rem 0.85rem; background: var(--bg-surface); border-radius: 6px; border: 1px solid var(--border-subtle); color: inherit; text-decoration: none;">
                <span><code>GET /api/forecast/FIL-1016/</code></span>
                <span>4-Week Demand Array</span>
              </a>
            </div>

            <div style="background: rgba(255,255,255,0.02); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 1.25rem;">
              <div style="font-weight: 700; font-size: 0.9rem; color: #fff; margin-bottom: 0.5rem;">Automated Verification Commands</div>
              <div style="font-size: 0.8rem; color: var(--text-muted); line-height: 1.6;">
                Run these in your terminal to verify contract correctness:
              </div>
              <pre style="background: rgba(0,0,0,0.5); padding: 0.75rem; border-radius: 6px; font-size: 0.78rem; font-family: 'JetBrains Mono', monospace; margin: 0.75rem 0; color: #a5b4fc; overflow-x: auto;">
# 1. Run official smoke test (AI/ML track)
python smoke_test.py --track aiml

# 2. Run Django unit test suite
python manage.py test

# 3. Model evaluation benchmark
python ml/train_and_evaluate.py
              </pre>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>

  <!-- PRODUCT DETAIL & LIVE STOCK ADJUSTMENT MODAL -->
  <div class="modal-overlay" id="productModal">
    <div class="modal-card">
      <button class="modal-close" onclick="closeProductModal()">✕</button>
      <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.5rem;">
        <span class="sku-code" id="modalSku">SKU</span>
        <span class="badge-status badge-in-stock" id="modalStatusBadge">IN STOCK</span>
      </div>
      <h2 id="modalName" style="font-size: 1.25rem; font-weight: 800; margin-bottom: 0.75rem;">Product Name</h2>
      <p id="modalDesc" style="font-size: 0.82rem; color: var(--text-muted); line-height: 1.5; margin-bottom: 1.5rem;">Description</p>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; margin-bottom: 1.5rem;">
        <div style="background: var(--bg-surface); padding: 0.85rem; border-radius: 8px; border: 1px solid var(--border-subtle);">
          <div style="font-size: 0.72rem; color: var(--text-subtle); text-transform: uppercase;">Category & Brand</div>
          <div style="font-weight: 600; font-size: 0.9rem;" id="modalCategoryBrand">—</div>
        </div>
        <div style="background: var(--bg-surface); padding: 0.85rem; border-radius: 8px; border: 1px solid var(--border-subtle);">
          <div style="font-size: 0.72rem; color: var(--text-subtle); text-transform: uppercase;">Vehicle Fitment</div>
          <div style="font-weight: 600; font-size: 0.9rem;" id="modalFitment">—</div>
        </div>
        <div style="background: var(--bg-surface); padding: 0.85rem; border-radius: 8px; border: 1px solid var(--border-subtle);">
          <div style="font-size: 0.72rem; color: var(--text-subtle); text-transform: uppercase;">Unit Price</div>
          <div style="font-weight: 700; font-size: 1.1rem; color: var(--cyan);" id="modalPrice">₹0.00</div>
        </div>
        <div style="background: var(--bg-surface); padding: 0.85rem; border-radius: 8px; border: 1px solid var(--border-subtle);">
          <div style="font-size: 0.72rem; color: var(--text-subtle); text-transform: uppercase;">Line Valuation</div>
          <div style="font-weight: 700; font-size: 1.1rem; color: var(--emerald);" id="modalValuation">₹0.00</div>
        </div>
      </div>

      <!-- LIVE ADJUST STOCK FORM -->
      <div style="background: rgba(99, 102, 241, 0.08); border: 1px solid rgba(99, 102, 241, 0.25); border-radius: var(--radius-md); padding: 1.25rem;">
        <div style="font-weight: 700; font-size: 0.9rem; margin-bottom: 0.5rem; color: #fff;">
          ⚡ Quick Live Stock Adjustment (PUT /api/inventory/{sku}/)
        </div>
        <div style="display: flex; gap: 0.75rem; align-items: center;">
          <input type="number" id="modalStockInput" min="0" placeholder="New quantity..." style="width: 140px;">
          <input type="text" id="modalStockReason" placeholder="Reason (e.g. physical count audit)" style="flex: 1;">
          <button class="btn-action" style="background: var(--primary); color: white; padding: 0.6rem 1rem;" onclick="submitStockAdjustment()">Save</button>
        </div>
      </div>
    </div>
  </div>

  <!-- JAVASCRIPT LOGIC -->
  <script>
    let currentView = 'overview';
    let explorerPage = 1;
    let explorerPageSize = 25;
    let explorerStatusFilter = '';
    let explorerSearchDebounce = null;
    let allReorderSuggestions = [];
    const sessionId = "session-" + Math.random().toString(36).substring(2, 9);

    document.addEventListener('DOMContentLoaded', () => {
      refreshAllData();
      pingHealth();
      setInterval(pingHealth, 30000);
    });

    function toggleSidebar() {
      document.getElementById('sidebar').classList.toggle('collapsed');
    }

    function switchView(viewName) {
      currentView = viewName;
      document.querySelectorAll('.view-section').forEach(el => el.classList.remove('active-view'));
      document.querySelectorAll('.nav-item').forEach(el => el.classList.remove('active'));

      const target = document.getElementById('view-' + viewName);
      if (target) target.classList.add('active-view');

      // Update sidebar nav highlighting
      const navItems = document.querySelectorAll('.nav-item');
      if (viewName === 'overview') navItems[0].classList.add('active');
      else if (viewName === 'explorer') navItems[1].classList.add('active');
      else if (viewName === 'assistant') navItems[2].classList.add('active');
      else if (viewName === 'forecasting') navItems[3].classList.add('active');
      else if (viewName === 'reorder') navItems[4].classList.add('active');
      else if (viewName === 'orders') navItems[5].classList.add('active');
      else if (viewName === 'devtools') navItems[6].classList.add('active');
    }

    async function refreshAllData() {
      document.getElementById('lastRefreshText').innerText = "Refreshed: " + new Date().toLocaleTimeString();
      await Promise.all([
        loadInventorySummary(),
        loadExplorerProducts(explorerPage),
        loadReorderSuggestions(),
        loadForecastPortfolio(),
        loadOrdersLedger()
      ]);
    }

    async function pingHealth() {
      const t0 = performance.now();
      try {
        const res = await fetch('/api/health/');
        const ms = Math.round(performance.now() - t0);
        if (res.ok) {
          document.getElementById('healthStatusText').innerText = `API Connected (${ms}ms)`;
          document.getElementById('healthPill').style.borderColor = 'rgba(16, 185, 129, 0.25)';
        } else {
          document.getElementById('healthStatusText').innerText = 'API Degraded';
          document.getElementById('healthPill').style.borderColor = 'rgba(244, 63, 94, 0.4)';
        }
      } catch (e) {
        document.getElementById('healthStatusText').innerText = 'API Disconnected';
        document.getElementById('healthPill').style.borderColor = 'rgba(244, 63, 94, 0.8)';
      }
    }

    /* 1. LIVE INVENTORY OVERVIEW (SECTION 2) */
    async function loadInventorySummary() {
      try {
        const res = await fetch('/api/inventory/summary/');
        const data = await res.json();

        const totalUnits = data.total_stock_units || 0;
        const uniqueProds = data.unique_products || 0;
        const inStock = data.in_stock_products || 0;
        const lowStock = data.low_stock_products || 0;
        const outStock = data.out_of_stock_products || 0;
        const invValue = parseFloat(data.inventory_value || 0);

        document.getElementById('kpiTotalStock').innerText = Number(totalUnits).toLocaleString();
        document.getElementById('kpiUniqueProducts').innerText = Number(uniqueProds).toLocaleString();
        document.getElementById('kpiInStock').innerText = Number(inStock).toLocaleString();
        document.getElementById('kpiLowStock').innerText = Number(lowStock).toLocaleString();
        document.getElementById('kpiOutStock').innerText = Number(outStock).toLocaleString();
        document.getElementById('kpiInventoryValue').innerText = "₹" + invValue.toLocaleString('en-IN', {minimumFractionDigits: 2, maximumFractionDigits: 2});
        document.getElementById('navProductCount').innerText = uniqueProds;

        // Render Donut Chart
        renderDonut(inStock, lowStock, outStock, uniqueProds);

        // Fetch Top 5 Low-Stock items for mini-table
        loadTopLowStock();
      } catch (err) {
        console.error("Error loading inventory summary:", err);
      }
    }

    function renderDonut(inStock, lowStock, outStock, total) {
      if (!total) return;
      const inPct = ((inStock / total) * 100).toFixed(1);
      const lowPct = ((lowStock / total) * 100).toFixed(1);
      const outPct = ((outStock / total) * 100).toFixed(1);

      document.getElementById('legInStock').innerText = inStock;
      document.getElementById('legInPct').innerText = inPct + '%';
      document.getElementById('legLowStock').innerText = lowStock;
      document.getElementById('legLowPct').innerText = lowPct + '%';
      document.getElementById('legOutStock').innerText = outStock;
      document.getElementById('legOutPct').innerText = outPct + '%';

      // SVG Donut circumference = 2 * PI * 60 = ~377
      const circ = 377;
      const strokeIn = (inStock / total) * circ;
      const strokeLow = (lowStock / total) * circ;
      const strokeOut = (outStock / total) * circ;

      const svg = document.getElementById('distributionSvg');
      svg.innerHTML = `
        <circle cx="80" cy="80" r="60" fill="none" stroke="rgba(255,255,255,0.06)" stroke-width="18"/>
        <circle cx="80" cy="80" r="60" fill="none" stroke="#10b981" stroke-width="18"
          stroke-dasharray="${strokeIn} ${circ - strokeIn}" stroke-dashoffset="0" transform="rotate(-90 80 80)"/>
        <circle cx="80" cy="80" r="60" fill="none" stroke="#f59e0b" stroke-width="18"
          stroke-dasharray="${strokeLow} ${circ - strokeLow}" stroke-dashoffset="${-strokeIn}" transform="rotate(-90 80 80)"/>
        <circle cx="80" cy="80" r="60" fill="none" stroke="#f43f5e" stroke-width="18"
          stroke-dasharray="${strokeOut} ${circ - strokeOut}" stroke-dashoffset="${-(strokeIn + strokeLow)}" transform="rotate(-90 80 80)"/>
        <text x="80" y="76" text-anchor="middle" font-size="16" font-weight="800" fill="#fff">${total}</text>
        <text x="80" y="94" text-anchor="middle" font-size="10" font-weight="600" fill="#94a3b8">PRODUCTS</text>
      `;
    }

    async function loadTopLowStock() {
      try {
        const res = await fetch('/api/products/?stock_status=low_stock&ordering=stock&page_size=6');
        const data = await res.json();
        const tbody = document.getElementById('topLowStockBody');
        tbody.innerHTML = '';
        data.results.forEach(p => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td><span class="sku-code">${p.sku}</span></td>
            <td style="font-weight: 600;">${p.name}</td>
            <td style="color: var(--text-muted);">${p.vehicle_fitment}</td>
            <td style="font-family: monospace;">₹${p.price}</td>
            <td><span class="badge-status badge-low-stock">${p.stock} units</span></td>
          `;
          tbody.appendChild(tr);
        });
      } catch (e) { console.error(e); }
    }

    /* 2. INVENTORY EXPLORER (SECTION 3) */
    function debounceExplorerSearch() {
      clearTimeout(explorerSearchDebounce);
      explorerSearchDebounce = setTimeout(() => {
        loadExplorerProducts(1);
      }, 300);
    }

    function setExplorerFilter(status) {
      explorerStatusFilter = status;
      document.querySelectorAll('.filter-chips .chip').forEach(c => {
        c.classList.toggle('active-chip', c.getAttribute('data-status') === status);
      });
      loadExplorerProducts(1);
    }

    async function loadExplorerProducts(page = 1) {
      explorerPage = page;
      const search = document.getElementById('explorerSearch').value.trim();
      const sort = document.getElementById('explorerSort').value;
      const category = document.getElementById('explorerCategory').value;

      let url = `/api/products/?page=${page}&page_size=${explorerPageSize}`;
      if (search) url += `&search=${encodeURIComponent(search)}`;
      if (explorerStatusFilter) url += `&stock_status=${explorerStatusFilter}`;
      if (sort) url += `&ordering=${sort}`;
      if (category) url += `&category=${encodeURIComponent(category)}`;

      const tbody = document.getElementById('explorerTableBody');
      tbody.innerHTML = '<tr><td colspan="9" style="text-align:center; padding: 2rem;">Loading products...</td></tr>';

      try {
        const res = await fetch(url);
        const data = await res.json();

        tbody.innerHTML = '';
        if (!data.results || data.results.length === 0) {
          tbody.innerHTML = '<tr><td colspan="9" style="text-align:center; padding: 2rem; color: var(--text-muted);">No products match your filters.</td></tr>';
          return;
        }

        data.results.forEach(p => {
          let badgeClass = 'badge-in-stock';
          let badgeText = 'IN STOCK';
          let stockColor = 'var(--emerald)';
          if (p.stock === 0) {
            badgeClass = 'badge-out-stock';
            badgeText = 'OUT OF STOCK';
            stockColor = 'var(--rose)';
          } else if (p.stock <= 10) {
            badgeClass = 'badge-low-stock';
            badgeText = 'LOW STOCK';
            stockColor = 'var(--amber)';
          }

          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td><span class="sku-code">${p.sku}</span></td>
            <td>
              <div style="font-weight: 700; color: #fff;">${p.name}</div>
              <div style="font-size: 0.72rem; color: var(--text-muted);">${p.brand || ''}</div>
            </td>
            <td><span style="font-size: 0.8rem; color: var(--text-muted);">${p.category}</span></td>
            <td><span style="font-size: 0.8rem;">${p.vehicle_fitment}</span></td>
            <td><span class="stock-number" style="color: ${stockColor};">${p.stock}</span></td>
            <td style="font-family: monospace;">₹${p.price}</td>
            <td style="font-family: monospace; color: var(--cyan); font-weight: 600;">₹${p.inventory_value || (p.price * p.stock).toFixed(2)}</td>
            <td><span class="badge-status ${badgeClass}">${badgeText}</span></td>
            <td>
              <button class="btn-action" onclick='openProductModal(${JSON.stringify(p).replace(/'/g, "&apos;")})'>View</button>
            </td>
          `;
          tbody.appendChild(tr);
        });

        // Update pagination stats
        const totalItems = data.count || 0;
        const totalPages = Math.ceil(totalItems / explorerPageSize) || 1;
        document.getElementById('currentPageNum').innerText = page;
        document.getElementById('totalPageNum').innerText = totalPages;
        document.getElementById('totalItemsCount').innerText = totalItems;
        document.getElementById('btnPrevPage').disabled = (page <= 1);
        document.getElementById('btnNextPage').disabled = (page >= totalPages);
        document.getElementById('explorerStatsText').innerText = `Showing ${data.results.length} of ${totalItems} products`;

        // Populate Categories Dropdown once
        populateCategoriesDropdown(data.results);
      } catch (err) {
        tbody.innerHTML = `<tr><td colspan="9" style="text-align:center; padding: 2rem; color: var(--rose);">Error loading inventory: ${err.message}</td></tr>`;
      }
    }

    function changePage(delta) {
      loadExplorerProducts(explorerPage + delta);
    }
    function changePageSize(newSize) {
      explorerPageSize = parseInt(newSize);
      loadExplorerProducts(1);
    }

    let categoriesPopulated = false;
    function populateCategoriesDropdown(products) {
      if (categoriesPopulated) return;
      const catSelect = document.getElementById('explorerCategory');
      const cats = new Set(["Brakes", "Drivetrain", "Filters", "Engine & Oils", "Lighting & Electrical", "Body & Styling", "Suspension", "Accessories", "Tires", "Exhaust"]);
      cats.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c;
        opt.innerText = c;
        catSelect.appendChild(opt);
      });
      categoriesPopulated = true;
    }

    /* PRODUCT DETAILS MODAL & LIVE STOCK ADJUSTMENT */
    let selectedModalSku = null;
    function openProductModal(p) {
      selectedModalSku = p.sku;
      document.getElementById('modalSku').innerText = p.sku;
      document.getElementById('modalName').innerText = p.name;
      document.getElementById('modalDesc').innerText = p.description || 'No description provided.';
      document.getElementById('modalCategoryBrand').innerText = `${p.category} • ${p.brand}`;
      document.getElementById('modalFitment').innerText = p.vehicle_fitment;
      document.getElementById('modalPrice').innerText = '₹' + p.price;
      const lineVal = p.inventory_value || (parseFloat(p.price) * p.stock).toFixed(2);
      document.getElementById('modalValuation').innerText = '₹' + lineVal;
      document.getElementById('modalStockInput').value = p.stock;

      const badge = document.getElementById('modalStatusBadge');
      if (p.stock === 0) {
        badge.className = 'badge-status badge-out-stock';
        badge.innerText = 'OUT OF STOCK';
      } else if (p.stock <= 10) {
        badge.className = 'badge-status badge-low-stock';
        badge.innerText = `LOW STOCK (${p.stock} units)`;
      } else {
        badge.className = 'badge-status badge-in-stock';
        badge.innerText = `IN STOCK (${p.stock} units)`;
      }

      document.getElementById('productModal').classList.add('active');
    }

    function closeProductModal() {
      document.getElementById('productModal').classList.remove('active');
    }

    async function submitStockAdjustment() {
      if (!selectedModalSku) return;
      const qty = parseInt(document.getElementById('modalStockInput').value);
      const reason = document.getElementById('modalStockReason').value.trim() || 'Inventory dashboard adjustment';

      if (isNaN(qty) || qty < 0) {
        alert("Quantity must be a positive integer.");
        return;
      }

      try {
        const res = await fetch(`/api/inventory/${selectedModalSku}/`, {
          method: 'PUT',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({quantity: qty, reason: reason})
        });

        if (res.ok) {
          alert(`Stock for ${selectedModalSku} successfully updated to ${qty}!`);
          closeProductModal();
          refreshAllData();
        } else {
          const err = await res.json();
          alert(`Failed to update stock: ${err.error ? err.error.message : 'Unknown error'}`);
        }
      } catch (e) {
        alert("Network error: " + e.message);
      }
    }

    /* 3. AI ASSISTANT (SECTION 5) */
    function sendQuickPrompt(promptText) {
      document.getElementById('assistantInput').value = promptText;
      sendAssistantMessage();
    }

    async function sendAssistantMessage() {
      const input = document.getElementById('assistantInput');
      const text = input.value.trim();
      if (!text) return;

      const chatBox = document.getElementById('chatMessages');

      // Add user message bubble
      const userDiv = document.createElement('div');
      userDiv.className = 'msg-bubble user';
      userDiv.innerText = text;
      chatBox.appendChild(userDiv);
      input.value = '';
      chatBox.scrollTop = chatBox.scrollHeight;

      // Add thinking placeholder
      const botDiv = document.createElement('div');
      botDiv.className = 'msg-bubble bot';
      botDiv.innerHTML = '<span style="color: var(--cyan);">Thinking and evaluating live PostgreSQL tools...</span>';
      chatBox.appendChild(botDiv);
      chatBox.scrollTop = chatBox.scrollHeight;

      try {
        const res = await fetch('/api/assistant/chat/', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            session_id: sessionId,
            dealer_id: 1,
            message: text
          })
        });

        const data = await res.json();
        let replyHtml = (data.reply || 'No response').replace(/\\n/g, '<br>');

        // Tool calls execution badge
        if (data.tool_calls && data.tool_calls.length > 0) {
          const tools = data.tool_calls.map(t => t.name).join(', ');
          replyHtml += `<br><div class="tool-execution-pill">🔧 Tool Invoked: ${tools}</div>`;
        }

        // Cited SKUs preview cards
        if (data.cited_skus && data.cited_skus.length > 0) {
          let cardsHtml = '<div class="cited-cards-row">';
          data.cited_skus.forEach(sku => {
            cardsHtml += `<div class="cited-card"><span class="sku-code">${sku}</span> <a href="javascript:void(0)" onclick="quickInspectSku('${sku}')" style="color: var(--cyan); text-decoration: none; font-weight: 600;">Inspect</a></div>`;
          });
          cardsHtml += '</div>';
          replyHtml += cardsHtml;
        }

        botDiv.innerHTML = replyHtml;
      } catch (err) {
        botDiv.innerHTML = `<span style="color: var(--rose);">Error communicating with assistant: ${err.message}</span>`;
      }
      chatBox.scrollTop = chatBox.scrollHeight;
    }

    async function quickInspectSku(sku) {
      try {
        const res = await fetch(`/api/products/${sku}/`);
        const p = await res.json();
        openProductModal(p);
      } catch (e) { console.error(e); }
    }

    /* 4. DEMAND FORECASTING (SECTION 6) */
    const forecastPortfolioSkus = ["FIL-1016", "BRK-1090", "BRK-1085", "FIL-1031", "BRK-1019", "CHN-1006", "BRK-1105", "BDY-1001", "BDY-1010", "BDY-1030"];
    async function loadForecastPortfolio() {
      const select = document.getElementById('forecastSkuSelector');
      select.innerHTML = '';
      try {
        const res = await fetch('/api/reorder-suggestions/');
        const data = await res.json();
        const skus = (data.results || []).map(r => r.sku);
        skus.forEach(s => {
          const opt = document.createElement('option');
          opt.value = s;
          opt.innerText = s;
          select.appendChild(opt);
        });
        if (skus.length > 0) loadForecastData(skus[0]);
      } catch (e) {
        console.error(e);
      }
    }

    async function loadForecastData(sku) {
      if (!sku) return;
      try {
        const [fRes, pRes] = await Promise.all([
          fetch(`/api/forecast/${sku}/`),
          fetch(`/api/products/${sku}/`)
        ]);
        const fData = await fRes.json();
        const pData = await pRes.json();

        document.getElementById('fLiveStock').innerText = pData.stock;

        const weeks = fData.forecast || [];
        const barsBox = document.getElementById('forecastBars');
        const tbody = document.getElementById('forecastTableBody');
        barsBox.innerHTML = '';
        tbody.innerHTML = '';

        const maxVal = Math.max(...weeks.map(w => w.forecast_units), 1);
        const totalDemand = weeks.reduce((acc, w) => acc + w.forecast_units, 0);

        weeks.forEach((w, idx) => {
          const heightPct = Math.min(100, Math.round((w.forecast_units / maxVal) * 85) + 15);
          const barDiv = document.createElement('div');
          barDiv.className = 'f-bar-group';
          barDiv.innerHTML = `
            <div class="f-bar-val">${w.forecast_units}</div>
            <div class="f-bar-fill" style="height: ${heightPct}%;"></div>
            <div class="f-bar-lbl">W${idx+1} (${w.week_start.slice(5)})</div>
          `;
          barsBox.appendChild(barDiv);

          const sharePct = totalDemand ? ((w.forecast_units / totalDemand) * 100).toFixed(1) : 0;
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td style="font-family: monospace;">${w.week_start}</td>
            <td style="font-weight: 700; color: var(--cyan);">${w.forecast_units} units</td>
            <td style="color: var(--text-muted);">${sharePct}%</td>
          `;
          tbody.appendChild(tr);
        });
      } catch (err) {
        console.error("Forecast fetch error:", err);
      }
    }

    /* 5. SMART REORDER CENTER (SECTION 7) */
    async function loadReorderSuggestions() {
      try {
        const res = await fetch('/api/reorder-suggestions/');
        const data = await res.json();
        allReorderSuggestions = data.results || [];

        renderReorderTable(allReorderSuggestions);
        const neededCount = allReorderSuggestions.filter(r => r.reorder_qty > 0).length;
        document.getElementById('navReorderBadge').innerText = `${neededCount} Action`;
      } catch (e) {
        console.error(e);
      }
    }

    function renderReorderTable(list) {
      const tbody = document.getElementById('reorderTableBody');
      tbody.innerHTML = '';
      if (!list || list.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" style="text-align: center;">No items match filter.</td></tr>';
        return;
      }

      list.forEach(item => {
        const needsOrder = item.reorder_qty > 0;
        const statusBadge = needsOrder
          ? `<span class="badge-status badge-out-stock">REORDER NEEDED (+${item.reorder_qty})</span>`
          : `<span class="badge-status badge-in-stock">SUFFICIENT STOCK</span>`;

        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td><span class="sku-code">${item.sku}</span></td>
          <td style="font-weight: 700; color: ${item.current_stock <= 10 ? 'var(--amber)' : '#fff'};">${item.current_stock}</td>
          <td>${item.lead_time_weeks} weeks</td>
          <td style="font-family: monospace;">${item.lead_time_demand}</td>
          <td style="font-family: monospace; color: var(--cyan);">${item.safety_stock}</td>
          <td style="font-family: monospace; font-weight: 700;">${item.reorder_point}</td>
          <td style="font-family: monospace; font-weight: 800; color: ${needsOrder ? 'var(--amber)' : 'var(--text-muted)'}; font-size: 1rem;">
            ${item.reorder_qty}
          </td>
          <td>${statusBadge}</td>
          <td>
            ${needsOrder ? `<button class="btn-action" style="background: rgba(245, 158, 11, 0.2); border-color: var(--amber); color: #fff;" onclick="quickDraftReorder('${item.sku}', ${item.reorder_qty})">Draft Order</button>` : `<span style="color: var(--text-subtle); font-size: 0.75rem;">Healthy</span>`}
          </td>
        `;
        tbody.appendChild(tr);
      });
    }

    function filterReorderTable(filterType, btn) {
      document.querySelectorAll('#view-reorder .chip').forEach(c => c.classList.remove('active-chip'));
      if (btn) btn.classList.add('active-chip');

      if (filterType === 'needed') {
        renderReorderTable(allReorderSuggestions.filter(r => r.reorder_qty > 0));
      } else if (filterType === 'sufficient') {
        renderReorderTable(allReorderSuggestions.filter(r => r.reorder_qty === 0));
      } else {
        renderReorderTable(allReorderSuggestions);
      }
    }

    async function quickDraftReorder(sku, qty) {
      try {
        const res = await fetch('/api/orders/', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            dealer_id: 1,
            items: [{sku: sku, quantity: qty}]
          })
        });
        if (res.ok) {
          const ord = await res.json();
          alert(`Draft order ${ord.order_number} created for ${qty} units of ${sku}! (Grand Total: ₹${ord.grand_total})`);
          switchView('orders');
          loadOrdersLedger();
        } else {
          const err = await res.json();
          alert(`Error creating draft order: ${err.error ? err.error.message : 'Unknown'}`);
        }
      } catch (e) {
        alert("Network error: " + e.message);
      }
    }

    /* 6. ORDERS LEDGER (SECTION 8) */
    async function loadOrdersLedger() {
      try {
        const res = await fetch('/api/orders/');
        const data = await res.json();
        const tbody = document.getElementById('ordersTableBody');
        tbody.innerHTML = '';

        if (!data.results || data.results.length === 0) {
          tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; color: var(--text-muted);">No orders created yet. Use the assistant or reorder center to create a draft order.</td></tr>';
          return;
        }

        data.results.forEach(ord => {
          const tr = document.createElement('tr');
          tr.innerHTML = `
            <td><span class="sku-code" style="color: var(--violet);">${ord.order_number}</span></td>
            <td>DLR-${ord.dealer_id}</td>
            <td><span class="badge-status ${ord.status === 'CONFIRMED' ? 'badge-in-stock' : ord.status === 'CANCELLED' ? 'badge-out-stock' : 'badge-low-stock'}">${ord.status}</span></td>
            <td>${ord.items ? ord.items.length : 1}</td>
            <td style="font-family: monospace;">₹${ord.subtotal}</td>
            <td style="font-family: monospace;">₹${ord.tax_total}</td>
            <td style="font-family: monospace; font-weight: 700; color: var(--cyan);">₹${ord.grand_total}</td>
            <td style="font-size: 0.75rem; color: var(--text-muted);">${ord.created_at ? ord.created_at.slice(0, 19).replace('T', ' ') : '—'}</td>
          `;
          tbody.appendChild(tr);
        });
      } catch (e) { console.error(e); }
    }

    function openNewOrderModal() {
      const sku = prompt("Enter SKU code (e.g. BRK-1044):", "BRK-1044");
      if (!sku) return;
      const qtyStr = prompt("Enter Quantity (integer >= 1):", "2");
      const qty = parseInt(qtyStr);
      if (isNaN(qty) || qty < 1) {
        alert("Invalid quantity.");
        return;
      }
      quickDraftReorder(sku.trim().toUpperCase(), qty);
    }
  </script>
</body>
</html>
"""

def portal_view(request):
    return HttpResponse(HTML_CONTENT, content_type="text/html")
