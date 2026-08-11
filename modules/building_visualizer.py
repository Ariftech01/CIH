"""3D Building Visualizer Module for Construction Intelligence Hub (CIH).

Futuristic Spatial Engineering Workspace & Parametric BIM Studio.
Provides high-performance 3D scene rendering via Three.js, WebGL, OrbitControls,
contextual floating panels, slim navigation rail, spatial inspector, asset browser,
BIM area/volume analytics, undo/redo engine, and spatial context menus.
"""

import streamlit as st
import streamlit.components.v1 as components
from utils.styles import render_page_header


def render() -> None:
    """Render the Futuristic Spatial Engineering Workspace module."""
    from backend.workflow.project_workflow import project_workflow
    active_proj = project_workflow.get_active_project()
    sub_title = f"Spatial Engineering Workspace • Active Project: {active_proj.project_name} ({active_proj.project_code})" if active_proj else "Spatial Engineering Workspace • Enterprise Parametric BIM Studio"

    render_page_header(
        "3D Building Visualizer",
        sub_title,
    )

    # 0. Inject page-scoped CSS to enforce full-viewport engineering workspace layout without scroll traps
    st.markdown(
        """
        <style>
        /* Suppress outer page scrollbar when 3D Visualizer workspace is active */
        html, body, .stApp {
            overflow: hidden !important;
        }

        .main .block-container {
            padding-top: 0.5rem !important;
            padding-bottom: 0.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            max-width: 100% !important;
            height: calc(100vh - 10px) !important;
            display: flex !important;
            flex-direction: column !important;
            overflow: hidden !important;
        }

        .cih-page-header {
            margin-bottom: 0.5rem !important;
            padding-bottom: 0.5rem !important;
            flex-shrink: 0 !important;
        }

        .cih-page-title {
            font-size: 1.5rem !important;
        }

        .cih-page-subtitle {
            font-size: 0.82rem !important;
        }

        /* Ensure Streamlit HTML component iframe dynamically fills available viewport height */
        div[data-testid="stCustomComponentV1"],
        div[data-testid="element-container"]:has(iframe) {
            flex: 1 1 auto !important;
            height: 100% !important;
            display: flex !important;
            flex-direction: column !important;
            overflow: hidden !important;
        }

        iframe[title="st.components.v1.html"],
        div[data-testid="stCustomComponentV1"] iframe {
            flex: 1 1 auto !important;
            height: calc(100vh - 120px) !important;
            min-height: 400px !important;
            width: 100% !important;
            border: none !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # 1. Disable Floating AI Assistant widget on this page to maximize spatial canvas
    components.html(
        """
        <script>
        (function() {
            const hostDoc = window.parent.document || document;
            const rootNode = hostDoc.getElementById("cih-assistant-root");
            if (rootNode) rootNode.remove();
            const markEl = hostDoc.getElementById("cih-assistant-script-loaded");
            if (markEl) markEl.remove();
            const styleEl = hostDoc.getElementById("cih-assistant-injected-styles");
            if (styleEl) styleEl.remove();
        })();
        </script>
        """,
        height=0,
        width=0,
    )

    # 2. Render Full-Screen Enterprise 3D CAD Studio WebGL Canvas Component
    visualizer_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CIH Spatial Engineering Workspace Engine</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
        
        <!-- Three.js & OrbitControls from CDN -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
        
        <style>
            :root {
                --bg-dark: #07090E;
                --panel-bg: rgba(13, 19, 33, 0.78);
                --panel-border: rgba(255, 255, 255, 0.08);
                --panel-border-glow: rgba(59, 130, 246, 0.35);
                --card-bg: rgba(22, 30, 49, 0.65);
                --accent-blue: #3B82F6;
                --accent-blue-hover: #2563EB;
                --accent-cyan: #06B6D4;
                --accent-green: #10B981;
                --accent-amber: #F59E0B;
                --accent-red: #EF4444;
                --accent-purple: #8B5CF6;
                --text-primary: #F8FAFC;
                --text-secondary: #94A3B8;
                --text-muted: #64748B;
                --input-bg: rgba(10, 15, 26, 0.85);
                --radius-lg: 16px;
                --radius-md: 10px;
                --radius-sm: 6px;
            }

            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                user-select: none;
            }

            body, html {
                width: 100%;
                height: 100%;
                overflow: hidden;
                font-family: 'Inter', system-ui, -apple-system, sans-serif;
                background-color: var(--bg-dark);
                color: var(--text-primary);
            }

            #app-container {
                display: flex;
                flex-direction: column;
                width: 100%;
                height: 100%;
                position: relative;
                overflow: hidden;
            }

            /* TOP COMMAND BAR */
            #top-command-bar {
                height: 44px;
                background: var(--panel-bg);
                backdrop-filter: blur(20px);
                border-bottom: 1px solid var(--panel-border);
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 0 0.85rem;
                z-index: 50;
            }

            .bar-group {
                display: flex;
                align-items: center;
                gap: 0.4rem;
            }

            .brand-pill {
                display: flex;
                align-items: center;
                gap: 0.5rem;
                font-weight: 800;
                font-size: 0.88rem;
                color: var(--text-primary);
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid var(--panel-border);
                padding: 0.25rem 0.65rem;
                border-radius: var(--radius-sm);
            }

            /* DROPDOWN MENUS */
            .dropdown {
                position: relative;
                display: inline-block;
            }

            .dropdown-btn {
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid var(--panel-border);
                color: var(--text-primary);
                padding: 0.35rem 0.65rem;
                border-radius: var(--radius-sm);
                font-size: 0.75rem;
                font-weight: 500;
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 0.3rem;
                transition: all 0.2s ease;
            }

            .dropdown-btn:hover {
                background: rgba(59, 130, 246, 0.18);
                border-color: var(--accent-blue);
            }

            .dropdown-content {
                display: none;
                position: absolute;
                top: 110%;
                left: 0;
                min-width: 190px;
                background: var(--panel-bg);
                backdrop-filter: blur(24px);
                border: 1px solid var(--panel-border);
                border-radius: var(--radius-md);
                box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6);
                padding: 0.4rem;
                z-index: 100;
            }

            .dropdown:hover .dropdown-content {
                display: block;
                animation: fadeIn 0.15s ease-out;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-4px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .dropdown-item {
                padding: 0.4rem 0.65rem;
                font-size: 0.76rem;
                color: var(--text-secondary);
                border-radius: var(--radius-sm);
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: space-between;
                transition: all 0.15s ease;
            }

            .dropdown-item:hover {
                background: rgba(59, 130, 246, 0.2);
                color: var(--text-primary);
            }

            .dropdown-divider {
                height: 1px;
                background: var(--panel-border);
                margin: 0.3rem 0;
            }

            .btn-icon {
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid var(--panel-border);
                color: var(--text-primary);
                width: 32px;
                height: 32px;
                border-radius: var(--radius-sm);
                font-size: 0.85rem;
                cursor: pointer;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                transition: all 0.2s ease;
            }

            .btn-icon:hover {
                background: rgba(59, 130, 246, 0.2);
                border-color: var(--accent-blue);
                color: #FFFFFF;
                transform: translateY(-1px);
            }

            .btn-icon.active {
                background: rgba(59, 130, 246, 0.3) !important;
                border-color: var(--accent-blue) !important;
                color: #FFFFFF !important;
            }

            /* MAIN SPATIAL CANVAS CONTAINER */
            #main-workspace {
                flex: 1;
                display: flex;
                position: relative;
                width: 100vw;
                overflow: hidden;
            }

            /* SLIM LEFT NAVIGATION RAIL */
            #nav-rail {
                width: 48px;
                background: var(--panel-bg);
                backdrop-filter: blur(20px);
                border-right: 1px solid var(--panel-border);
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 0.6rem 0;
                gap: 0.5rem;
                z-index: 40;
                overflow-y: auto;
            }

            .rail-btn {
                width: 36px;
                height: 36px;
                border-radius: var(--radius-sm);
                background: transparent;
                border: 1px solid transparent;
                color: var(--text-secondary);
                font-size: 1.1rem;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                position: relative;
                transition: all 0.2s ease;
            }

            .rail-btn:hover {
                background: rgba(255, 255, 255, 0.08);
                color: var(--text-primary);
                transform: scale(1.05);
            }

            .rail-btn.active {
                background: rgba(59, 130, 246, 0.25);
                border-color: var(--accent-blue);
                color: var(--accent-cyan);
            }

            .rail-tooltip {
                position: absolute;
                left: 54px;
                background: var(--panel-bg);
                backdrop-filter: blur(16px);
                border: 1px solid var(--panel-border);
                padding: 0.25rem 0.6rem;
                border-radius: var(--radius-sm);
                font-size: 0.72rem;
                font-weight: 600;
                color: var(--text-primary);
                white-space: nowrap;
                pointer-events: none;
                opacity: 0;
                transition: opacity 0.2s ease;
                z-index: 100;
                box-shadow: 0 4px 14px rgba(0,0,0,0.5);
            }

            .rail-btn:hover .rail-tooltip {
                opacity: 1;
            }

            /* HERO 3D VIEWPORT CANVAS */
            #viewport-container {
                flex: 1;
                position: relative;
                width: 100%;
                height: 100%;
                background: radial-gradient(circle at center, #111827 0%, #07090E 100%);
            }

            #webgl-canvas {
                width: 100%;
                height: 100%;
                display: block;
            }

            /* FLOATING CONTEXTUAL PANELS */
            .floating-panel {
                position: absolute;
                background: var(--panel-bg);
                backdrop-filter: blur(24px);
                border: 1px solid var(--panel-border);
                border-radius: var(--radius-lg);
                box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6);
                z-index: 30;
                display: flex;
                flex-direction: column;
                overflow: hidden;
                transition: opacity 0.25s ease, transform 0.25s ease;
            }

            .floating-panel.hidden {
                display: none !important;
            }

            .panel-drag-header {
                height: 38px;
                background: rgba(255, 255, 255, 0.03);
                border-bottom: 1px solid var(--panel-border);
                padding: 0 0.85rem;
                display: flex;
                align-items: center;
                justify-content: space-between;
                cursor: move;
                font-size: 0.78rem;
                font-weight: 700;
                letter-spacing: 0.02em;
                color: var(--accent-cyan);
            }

            .panel-close-btn {
                background: none;
                border: none;
                color: var(--text-muted);
                font-size: 1rem;
                cursor: pointer;
                padding: 0.2rem;
                border-radius: 50%;
                transition: color 0.2s ease;
            }

            .panel-close-btn:hover {
                color: var(--accent-red);
            }

            .panel-body {
                padding: 0.85rem;
                overflow-y: auto;
                max-height: 65vh;
            }

            /* FORM CONTROLS INSIDE FLOATING PANELS */
            .form-group {
                margin-bottom: 0.75rem;
            }

            .form-group label {
                display: block;
                font-size: 0.72rem;
                font-weight: 600;
                color: var(--text-secondary);
                margin-bottom: 0.3rem;
                text-transform: uppercase;
                letter-spacing: 0.04em;
            }

            .form-control, select, input {
                width: 100%;
                background: var(--input-bg);
                border: 1px solid var(--panel-border);
                border-radius: var(--radius-sm);
                padding: 0.4rem 0.6rem;
                color: var(--text-primary);
                font-size: 0.78rem;
                outline: none;
                transition: border-color 0.2s ease;
            }

            .form-control:focus, select:focus, input:focus {
                border-color: var(--accent-blue);
                box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.25);
            }

            .form-row {
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 0.5rem;
            }

            .btn-action {
                background: rgba(255, 255, 255, 0.06);
                border: 1px solid var(--panel-border);
                color: var(--text-primary);
                padding: 0.4rem 0.75rem;
                border-radius: var(--radius-sm);
                font-size: 0.76rem;
                font-weight: 600;
                cursor: pointer;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                gap: 0.35rem;
                transition: all 0.2s ease;
            }

            .btn-action:hover {
                background: rgba(59, 130, 246, 0.25);
                border-color: var(--accent-blue);
            }

            .btn-action-primary {
                background: linear-gradient(135deg, #3B82F6, #2563EB);
                border: none;
                color: #FFFFFF;
                box-shadow: 0 4px 14px rgba(59, 130, 246, 0.35);
            }

            .btn-action-primary:hover {
                background: linear-gradient(135deg, #2563EB, #1D4ED8);
            }

            .btn-action-danger {
                background: rgba(239, 68, 68, 0.15);
                border-color: rgba(239, 68, 68, 0.3);
                color: #EF4444;
            }

            .btn-action-danger:hover {
                background: rgba(239, 68, 68, 0.3);
                color: #FFFFFF;
            }

            /* SPATIAL CONTEXT MENU */
            #spatial-context-menu {
                position: absolute;
                display: none;
                background: var(--panel-bg);
                backdrop-filter: blur(24px);
                border: 1px solid var(--panel-border-glow);
                border-radius: var(--radius-md);
                padding: 0.35rem;
                box-shadow: 0 12px 36px rgba(0, 0, 0, 0.7);
                z-index: 200;
                min-width: 170px;
            }

            .context-item {
                padding: 0.4rem 0.65rem;
                font-size: 0.75rem;
                font-weight: 500;
                color: var(--text-primary);
                border-radius: var(--radius-sm);
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 0.4rem;
                transition: background 0.15s ease;
            }

            .context-item:hover {
                background: rgba(59, 130, 246, 0.25);
                color: var(--accent-cyan);
            }

            /* VIEWPORT OVERLAY CONTROLS */
            .viewport-overlay {
                position: absolute;
                top: 1rem;
                right: 1rem;
                display: flex;
                flex-direction: column;
                gap: 0.4rem;
                z-index: 10;
            }

            .view-preset-btn {
                width: 36px;
                height: 36px;
                border-radius: 50%;
                background: var(--panel-bg);
                backdrop-filter: blur(12px);
                border: 1px solid var(--panel-border);
                color: var(--text-primary);
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                font-size: 0.85rem;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
                transition: all 0.2s ease;
            }

            .view-preset-btn:hover {
                background: var(--accent-blue);
                color: #FFFFFF;
                transform: scale(1.1);
            }

            /* ROTATING PLATFORM BANNER */
            #platform-banner {
                position: absolute;
                top: 1rem;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(13, 19, 33, 0.8);
                backdrop-filter: blur(16px);
                border: 1px solid rgba(59, 130, 246, 0.35);
                padding: 0.35rem 1rem;
                border-radius: 999px;
                font-size: 0.72rem;
                font-weight: 600;
                color: var(--accent-cyan);
                display: flex;
                align-items: center;
                gap: 0.5rem;
                pointer-events: none;
                z-index: 10;
                transition: opacity 0.3s ease;
            }

            .spinner-dot {
                width: 7px;
                height: 7px;
                border-radius: 50%;
                background-color: var(--accent-cyan);
                animation: pulse 1.5s infinite;
            }

            @keyframes pulse {
                0%, 100% { transform: scale(0.8); opacity: 0.5; }
                50% { transform: scale(1.2); opacity: 1; }
            }

            /* BOTTOM SPATIAL STATUS BAR */
            #status-bar {
                height: 32px;
                background: var(--panel-bg);
                backdrop-filter: blur(20px);
                border-top: 1px solid var(--panel-border);
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 0 0.85rem;
                font-size: 0.72rem;
                color: var(--text-secondary);
                z-index: 50;
            }

            .status-metrics {
                display: flex;
                align-items: center;
                gap: 1.2rem;
            }

            .metric-pill {
                display: flex;
                align-items: center;
                gap: 0.3rem;
            }

            .metric-val {
                color: var(--text-primary);
                font-weight: 700;
            }

            /* ITEM LIST & HIERARCHY TREE */
            .item-list {
                display: flex;
                flex-direction: column;
                gap: 0.35rem;
                max-height: 200px;
                overflow-y: auto;
            }

            .item-card {
                background: rgba(255, 255, 255, 0.04);
                border: 1px solid rgba(255, 255, 255, 0.06);
                border-radius: var(--radius-sm);
                padding: 0.45rem 0.6rem;
                display: flex;
                align-items: center;
                justify-content: space-between;
                cursor: pointer;
                transition: all 0.2s ease;
                font-size: 0.76rem;
            }

            .item-card:hover {
                background: rgba(59, 130, 246, 0.15);
                border-color: rgba(59, 130, 246, 0.35);
            }

            .item-card.active {
                background: rgba(59, 130, 246, 0.25);
                border-color: var(--accent-blue);
                font-weight: 600;
            }

            .tree-node {
                margin-left: 0.5rem;
                font-size: 0.75rem;
            }

            .tree-header {
                padding: 0.3rem 0.5rem;
                border-radius: var(--radius-sm);
                cursor: pointer;
                display: flex;
                align-items: center;
                gap: 0.35rem;
                color: var(--text-secondary);
                transition: background 0.2s ease;
            }

            .tree-header:hover {
                background: rgba(255, 255, 255, 0.06);
                color: var(--text-primary);
            }

            .tree-header.selected {
                background: rgba(6, 182, 212, 0.2);
                color: var(--accent-cyan);
                font-weight: 600;
            }

            #ruler-tooltip {
                position: absolute;
                background: rgba(6, 182, 212, 0.95);
                color: #000;
                font-weight: 800;
                font-size: 0.75rem;
                padding: 0.25rem 0.55rem;
                border-radius: var(--radius-sm);
                pointer-events: none;
                display: none;
                z-index: 30;
                box-shadow: 0 4px 14px rgba(0,0,0,0.5);
            }
        </style>
    </head>
    <body>
        <div id="app-container">
            <!-- TOP COMMAND BAR -->
            <div id="top-command-bar">
                <div class="bar-group">
                    <div class="brand-pill">
                        <span style="color:var(--accent-cyan);">🏗️</span>
                        <span>Spatial Engine</span>
                    </div>

                    <!-- DROPDOWN: CREATE -->
                    <div class="dropdown">
                        <button class="dropdown-btn">➕ Create ▼</button>
                        <div class="dropdown-content">
                            <div class="dropdown-item" onclick="openPresetRoom('bedroom')">🛏️ Master Bedroom (5x4m)</div>
                            <div class="dropdown-item" onclick="openPresetRoom('kitchen')">🍳 Modular Kitchen (4x3.5m)</div>
                            <div class="dropdown-item" onclick="openPresetRoom('hall')">🛋️ Living Hall (8x6m)</div>
                            <div class="dropdown-item" onclick="openPresetRoom('office')">💼 Executive Office (6x5m)</div>
                            <div class="dropdown-item" onclick="openPresetRoom('conference')">👥 Conference Room (8x5m)</div>
                            <div class="dropdown-item" onclick="openPresetRoom('bathroom')">🚿 Luxury Bathroom (3x2.5m)</div>
                            <div class="dropdown-divider"></div>
                            <div class="dropdown-item" onclick="toggleFloatingPanel('panel-asset-browser')">📦 BIM Assets Library</div>
                        </div>
                    </div>

                    <!-- DROPDOWN: UTILITIES -->
                    <div class="dropdown">
                        <button class="dropdown-btn">📐 Utilities ▼</button>
                        <div class="dropdown-content">
                            <div class="dropdown-item" onclick="toggleRulerTool()">📏 Distance Ruler</div>
                            <div class="dropdown-item" onclick="toggleGridLines()">📐 Toggle Grid Lines</div>
                            <div class="dropdown-item" onclick="toggleCeilings()">🔳 Toggle Ceilings</div>
                            <div class="dropdown-item" onclick="toggleRoomLabels()">🏷️ Toggle 3D Labels</div>
                            <div class="dropdown-divider"></div>
                            <div class="dropdown-item" onclick="toggleSnapToGrid()">🧲 Toggle Snap to Grid</div>
                        </div>
                    </div>

                    <!-- DROPDOWN: VIEW -->
                    <div class="dropdown">
                        <button class="dropdown-btn">👁️ View ▼</button>
                        <div class="dropdown-content">
                            <div class="dropdown-item" onclick="setCamView('iso')">🔄 Isometric View</div>
                            <div class="dropdown-item" onclick="setCamView('top')">⬆️ Top Plan (2D)</div>
                            <div class="dropdown-item" onclick="setCamView('front')">➡️ Front Elevation</div>
                            <div class="dropdown-item" onclick="setCamView('side')">⬅️ Side Elevation</div>
                        </div>
                    </div>

                    <!-- DROPDOWN: MODES -->
                    <div class="dropdown">
                        <button class="dropdown-btn" id="active-mode-btn">🎯 Modeling Mode ▼</button>
                        <div class="dropdown-content">
                            <div class="dropdown-item" onclick="switchWorkspaceMode('Modeling')">🛠️ Modeling Mode</div>
                            <div class="dropdown-item" onclick="switchWorkspaceMode('Review')">🔍 BIM Review Mode</div>
                            <div class="dropdown-item" onclick="switchWorkspaceMode('Inspection')">🦺 Inspection Mode</div>
                            <div class="dropdown-item" onclick="switchWorkspaceMode('Presentation')">🖥️ Presentation Mode</div>
                        </div>
                    </div>
                </div>

                <!-- TOP RIGHT QUICK ACTIONS -->
                <div class="bar-group">
                    <button class="btn-icon" id="btn-undo" title="Undo Action (Ctrl+Z)">↩️</button>
                    <button class="btn-icon" id="btn-redo" title="Redo Action (Ctrl+Y)">↪️</button>
                    <div style="width: 1px; height: 18px; background: var(--panel-border);"></div>
                    <button class="btn-icon" id="btn-fullscreen" title="Fullscreen Viewport">🖥️</button>
                    <button class="btn-action btn-action-primary" id="btn-screenshot" title="Export Render Snapshot">📸 Export Render</button>
                </div>
            </div>

            <!-- MAIN SPATIAL WORKSPACE -->
            <div id="main-workspace">
                <!-- SLIM LEFT NAVIGATION RAIL -->
                <div id="nav-rail">
                    <button class="rail-btn" onclick="toggleFloatingPanel('panel-project-setup')" title="Project Setup">
                        🏢
                        <div class="rail-tooltip">Project Setup</div>
                    </button>
                    <button class="rail-btn" onclick="toggleFloatingPanel('panel-floor-manager')" title="Floor Manager">
                        📑
                        <div class="rail-tooltip">Floor Manager</div>
                    </button>
                    <button class="rail-btn" onclick="toggleFloatingPanel('panel-room-builder')" title="Room Builder">
                        🔲
                        <div class="rail-tooltip">Room Builder</div>
                    </button>
                    <button class="rail-btn" onclick="toggleFloatingPanel('panel-hierarchy')" title="Hierarchy Tree">
                        🌳
                        <div class="rail-tooltip">Hierarchy Tree</div>
                    </button>
                    <button class="rail-btn" onclick="toggleFloatingPanel('panel-asset-browser')" title="BIM Asset Library">
                        📦
                        <div class="rail-tooltip">BIM Assets</div>
                    </button>
                    <button class="rail-btn" onclick="toggleFloatingPanel('panel-bim-analytics')" title="BIM Analytics">
                        📊
                        <div class="rail-tooltip">BIM Analytics</div>
                    </button>
                </div>

                <!-- HERO 3D VIEWPORT CANVAS -->
                <div id="viewport-container">
                    <div id="platform-banner">
                        <div class="spinner-dot"></div>
                        <span id="platform-banner-text">Spatial Pedestal • Left-Click + Drag to Rotate Orbit</span>
                    </div>

                    <div class="viewport-overlay">
                        <button class="view-preset-btn" onclick="setCamView('iso')" title="Reset Isometric View">🔄</button>
                        <button class="view-preset-btn" onclick="setCamView('top')" title="Top Plan View">⬆️</button>
                        <button class="view-preset-btn" onclick="setCamView('front')" title="Front View">➡️</button>
                        <button class="view-preset-btn" onclick="setCamView('side')" title="Side View">⬅️</button>
                    </div>

                    <canvas id="webgl-canvas"></canvas>
                    <div id="ruler-tooltip">0.00 m</div>

                    <!-- SPATIAL CONTEXT MENU -->
                    <div id="spatial-context-menu">
                        <div class="context-item" onclick="contextAction('focus')">🔍 Focus Camera</div>
                        <div class="context-item" onclick="contextAction('duplicate')">📋 Duplicate Object</div>
                        <div class="context-item" onclick="contextAction('isolate')">👁️ Isolate View</div>
                        <div class="dropdown-divider"></div>
                        <div class="context-item" style="color:var(--accent-red);" onclick="contextAction('delete')">🗑️ Delete Object</div>
                    </div>

                    <!-- FLOATING PANEL 1: PROJECT SETUP -->
                    <div class="floating-panel hidden" id="panel-project-setup" style="top: 1rem; left: 4rem; width: 300px;">
                        <div class="panel-drag-header">
                            <span>🏢 Project Setup</span>
                            <button class="panel-close-btn" onclick="toggleFloatingPanel('panel-project-setup')">×</button>
                        </div>
                        <div class="panel-body">
                            <div class="form-group">
                                <label>Project Name</label>
                                <input type="text" id="proj-name" value="CIH Enterprise Tower">
                            </div>
                            <div class="form-row">
                                <div class="form-group">
                                    <label>Type</label>
                                    <select id="proj-type">
                                        <option value="Residential" selected>Residential</option>
                                        <option value="Commercial">Commercial</option>
                                        <option value="Industrial">Industrial</option>
                                        <option value="High-Rise">High-Rise</option>
                                    </select>
                                </div>
                                <div class="form-group">
                                    <label>Units</label>
                                    <select id="proj-units">
                                        <option value="meters" selected>Meters (m)</option>
                                        <option value="feet">Feet (ft)</option>
                                    </select>
                                </div>
                            </div>
                            <div class="form-row">
                                <div class="form-group">
                                    <label>Floor Height</label>
                                    <input type="number" id="proj-floor-height" value="3.2" step="0.1">
                                </div>
                                <div class="form-group">
                                    <label>Ground Lvl</label>
                                    <input type="number" id="proj-ground-lvl" value="0.0" step="0.1">
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- FLOATING PANEL 2: FLOOR MANAGER -->
                    <div class="floating-panel hidden" id="panel-floor-manager" style="top: 1rem; left: 4rem; width: 310px;">
                        <div class="panel-drag-header">
                            <span>📑 Floor Manager</span>
                            <button class="panel-close-btn" onclick="toggleFloatingPanel('panel-floor-manager')">×</button>
                        </div>
                        <div class="panel-body">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.6rem;">
                                <span style="font-size:0.75rem; color:var(--text-secondary);">Active Floors Log</span>
                                <button class="btn-action btn-action-primary" style="padding:0.25rem 0.55rem; font-size:0.7rem;" id="btn-add-floor">➕ Add Floor</button>
                            </div>
                            <div class="item-list" id="floor-list"></div>
                        </div>
                    </div>

                    <!-- FLOATING PANEL 3: ROOM BUILDER -->
                    <div class="floating-panel hidden" id="panel-room-builder" style="top: 1rem; left: 4rem; width: 320px;">
                        <div class="panel-drag-header">
                            <span>🔲 Room & Geometry Studio</span>
                            <button class="panel-close-btn" onclick="toggleFloatingPanel('panel-room-builder')">×</button>
                        </div>
                        <div class="panel-body">
                            <div class="form-group">
                                <label>Target Floor</label>
                                <select id="room-target-floor"></select>
                            </div>
                            <div class="form-group">
                                <label>Room Presets</label>
                                <select id="room-preset-select">
                                    <option value="custom">Custom Dimensions</option>
                                    <option value="bedroom" selected>Master Bedroom (5.0 × 4.0m)</option>
                                    <option value="kitchen">Modular Kitchen (4.0 × 3.5m)</option>
                                    <option value="hall">Living Hall (8.0 × 6.0m)</option>
                                    <option value="office">Executive Office (6.0 × 5.0m)</option>
                                    <option value="conference">Conference Room (8.0 × 5.0m)</option>
                                    <option value="bathroom">Luxury Bathroom (3.0 × 2.5m)</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label>Room Name</label>
                                <input type="text" id="room-name" value="Master Bedroom">
                            </div>
                            <div class="form-row">
                                <div class="form-group">
                                    <label>Length (X)</label>
                                    <input type="number" id="room-len" value="5.0" step="0.5">
                                </div>
                                <div class="form-group">
                                    <label>Width (Z)</label>
                                    <input type="number" id="room-wid" value="4.0" step="0.5">
                                </div>
                            </div>
                            <div class="form-row">
                                <div class="form-group">
                                    <label>Height (Y)</label>
                                    <input type="number" id="room-hgt" value="3.0" step="0.1">
                                </div>
                                <div class="form-group">
                                    <label>Wall Thickness</label>
                                    <input type="number" id="room-wall-th" value="0.2" step="0.05">
                                </div>
                            </div>
                            <div class="form-row">
                                <div class="form-group">
                                    <label>Offset X</label>
                                    <input type="number" id="room-pos-x" value="0.0" step="0.5">
                                </div>
                                <div class="form-group">
                                    <label>Offset Z</label>
                                    <input type="number" id="room-pos-z" value="0.0" step="0.5">
                                </div>
                            </div>
                            <div class="form-group">
                                <label>Material Texture</label>
                                <select id="room-mat">
                                    <option value="wood" selected>Warm Timber Hardwood</option>
                                    <option value="marble">White Italian Marble</option>
                                    <option value="tiles">Slate Ceramic Tiles</option>
                                    <option value="concrete">Polished Industrial Concrete</option>
                                    <option value="carpet">Navy Executive Carpet</option>
                                </select>
                            </div>
                            <button class="btn-action btn-action-primary" style="width:100%; margin-top:0.3rem;" id="btn-add-room">➕ Add Room to Scene</button>
                        </div>
                    </div>

                    <!-- FLOATING PANEL 4: HIERARCHY TREE -->
                    <div class="floating-panel hidden" id="panel-hierarchy" style="top: 1rem; right: 4rem; width: 300px;">
                        <div class="panel-drag-header">
                            <span>🌳 Hierarchy Tree</span>
                            <button class="panel-close-btn" onclick="toggleFloatingPanel('panel-hierarchy')">×</button>
                        </div>
                        <div class="panel-body">
                            <div class="item-list" id="tree-container" style="max-height:360px;"></div>
                        </div>
                    </div>

                    <!-- FLOATING PANEL 5: OBJECT INSPECTOR -->
                    <div class="floating-panel hidden" id="panel-object-inspector" style="top: 1rem; right: 4rem; width: 320px;">
                        <div class="panel-drag-header">
                            <span>⚙️ Spatial Inspector</span>
                            <button class="panel-close-btn" onclick="toggleFloatingPanel('panel-object-inspector')">×</button>
                        </div>
                        <div class="panel-body">
                            <div id="props-form">
                                <div class="form-group">
                                    <label>Selected Room ID / Name</label>
                                    <input type="text" id="prop-name">
                                </div>
                                <div class="form-row">
                                    <div class="form-group">
                                        <label>Length (m)</label>
                                        <input type="number" id="prop-len" step="0.1">
                                    </div>
                                    <div class="form-group">
                                        <label>Width (m)</label>
                                        <input type="number" id="prop-wid" step="0.1">
                                    </div>
                                </div>
                                <div class="form-row">
                                    <div class="form-group">
                                        <label>Height (m)</label>
                                        <input type="number" id="prop-hgt" step="0.1">
                                    </div>
                                    <div class="form-group">
                                        <label>Wall Thickness</label>
                                        <input type="number" id="prop-wall-th" step="0.05">
                                    </div>
                                </div>
                                <div class="form-row">
                                    <div class="form-group">
                                        <label>Pos X</label>
                                        <input type="number" id="prop-x" step="0.5">
                                    </div>
                                    <div class="form-group">
                                        <label>Pos Z</label>
                                        <input type="number" id="prop-z" step="0.5">
                                    </div>
                                </div>
                                <div style="background: rgba(255,255,255,0.03); border: 1px solid var(--panel-border); padding: 0.6rem; border-radius: var(--radius-sm); margin-bottom: 0.75rem;">
                                    <div style="font-size: 0.72rem; color: var(--text-secondary); margin-bottom: 0.2rem;">Live Spatial Calculations</div>
                                    <div style="font-size: 0.78rem; font-weight: 700; color: var(--accent-cyan);" id="prop-calc-area">Area: 0.00 m²</div>
                                    <div style="font-size: 0.78rem; font-weight: 700; color: var(--accent-green);" id="prop-calc-vol">Volume: 0.00 m³</div>
                                </div>
                                <div class="form-row">
                                    <button class="btn-action" id="prop-btn-duplicate">📋 Duplicate</button>
                                    <button class="btn-action btn-action-danger" id="prop-btn-delete">🗑️ Delete</button>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- FLOATING PANEL 6: BIM ASSET BROWSER -->
                    <div class="floating-panel hidden" id="panel-asset-browser" style="top: 1rem; left: 4rem; width: 340px;">
                        <div class="panel-drag-header">
                            <span>📦 BIM Assets Library</span>
                            <button class="panel-close-btn" onclick="toggleFloatingPanel('panel-asset-browser')">×</button>
                        </div>
                        <div class="panel-body">
                            <div style="font-size:0.72rem; color:var(--text-secondary); margin-bottom:0.6rem;">Click asset preset to spawn into scene:</div>
                            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:0.5rem;">
                                <div class="item-card" onclick="spawnAsset('Structural Column', 1.0, 1.0, 3.5, 'concrete')">🏛️ Concrete Column</div>
                                <div class="item-card" onclick="spawnAsset('Structural Beam', 6.0, 0.8, 0.8, 'concrete')">🏗️ Concrete Beam</div>
                                <div class="item-card" onclick="spawnAsset('Glass Partition', 4.0, 0.1, 3.0, 'marble')">🪟 Glass Partition</div>
                                <div class="item-card" onclick="spawnAsset('Safety Barrier', 3.0, 0.2, 1.2, 'wood')">🦺 Safety Barrier</div>
                                <div class="item-card" onclick="spawnAsset('Storage Shed', 6.0, 5.0, 3.0, 'concrete')">🏬 Storage Shed</div>
                                <div class="item-card" onclick="spawnAsset('Elevator Core', 3.0, 3.0, 12.0, 'concrete')">🛗 Elevator Shaft</div>
                            </div>
                        </div>
                    </div>

                    <!-- FLOATING PANEL 7: BIM ANALYTICS -->
                    <div class="floating-panel hidden" id="panel-bim-analytics" style="top: 1rem; right: 4rem; width: 320px;">
                        <div class="panel-drag-header">
                            <span>📊 BIM Analytics Breakdown</span>
                            <button class="panel-close-btn" onclick="toggleFloatingPanel('panel-bim-analytics')">×</button>
                        </div>
                        <div class="panel-body">
                            <div style="display:flex; flex-direction:column; gap:0.6rem;">
                                <div style="background:rgba(255,255,255,0.03); padding:0.6rem; border-radius:var(--radius-sm); border:1px solid var(--panel-border);">
                                    <div style="font-size:0.72rem; color:var(--text-muted);">Total Built-up Area</div>
                                    <div style="font-size:1.1rem; font-weight:800; color:var(--accent-cyan);" id="modal-builtup">0.0 m²</div>
                                </div>
                                <div style="background:rgba(255,255,255,0.03); padding:0.6rem; border-radius:var(--radius-sm); border:1px solid var(--panel-border);">
                                    <div style="font-size:0.72rem; color:var(--text-muted);">Net Carpet Area</div>
                                    <div style="font-size:1.1rem; font-weight:800; color:var(--accent-green);" id="modal-carpet">0.0 m²</div>
                                </div>
                                <div style="background:rgba(255,255,255,0.03); padding:0.6rem; border-radius:var(--radius-sm); border:1px solid var(--panel-border);">
                                    <div style="font-size:0.72rem; color:var(--text-muted);">Perimeter Wall Surface</div>
                                    <div style="font-size:1.1rem; font-weight:800; color:var(--accent-amber);" id="modal-wall">0.0 m²</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- BOTTOM SPATIAL STATUS BAR -->
            <div id="status-bar">
                <div class="status-metrics">
                    <div class="metric-pill">📐 Built-up: <span class="metric-val" id="stat-builtup">0.00 m²</span></div>
                    <div class="metric-pill">🛋️ Carpet: <span class="metric-val" id="stat-carpet">0.00 m²</span></div>
                    <div class="metric-pill">🧱 Walls: <span class="metric-val" id="stat-wall">0.00 m²</span></div>
                    <div class="metric-pill">📦 Volume: <span class="metric-val" id="stat-vol">0.00 m³</span></div>
                </div>
                <div class="status-metrics">
                    <div class="metric-pill">🏢 Floors: <span class="metric-val" id="stat-floors-cnt">1</span></div>
                    <div class="metric-pill">🚪 Rooms: <span class="metric-val" id="stat-rooms-cnt">0</span></div>
                    <div class="metric-pill">⚡ Engine: <span class="metric-val" style="color:var(--accent-green);" id="stat-fps">60 FPS</span></div>
                </div>
            </div>
        </div>

        <!-- 3D GRAPHICS ENGINE & CONTROLLER SCRIPT -->
        <script>
        (function() {
            // ─────────────────────────────────────────────────────────────
            // GLOBAL APP STATE STORE
            // ─────────────────────────────────────────────────────────────
            const state = {
                project: {
                    name: "CIH Enterprise Tower",
                    type: "Residential",
                    units: "meters",
                    defaultFloorHeight: 3.2,
                    groundLevel: 0.0
                },
                floors: [
                    {
                        id: "floor_0",
                        name: "Ground Floor",
                        elevation: 0.0,
                        height: 3.2,
                        visible: true,
                        rooms: []
                    }
                ],
                activeFloorId: "floor_0",
                selectedRoomId: null,
                activeMode: "Modeling",
                settings: {
                    snapToGrid: true,
                    gridSize: 0.5,
                    showGrid: true,
                    showCeilings: false,
                    showLabels: true,
                    rulerMode: false
                },
                history: [],
                redoStack: []
            };

            const MATERIALS = {
                wood: { color: 0xB45309, roughness: 0.4 },
                marble: { color: 0xE2E8F0, roughness: 0.1 },
                tiles: { color: 0x475569, roughness: 0.3 },
                concrete: { color: 0x64748B, roughness: 0.7 },
                carpet: { color: 0x1E40AF, roughness: 0.9 }
            };

            // ─────────────────────────────────────────────────────────────
            // THREE.JS SCENE SETUP
            // ─────────────────────────────────────────────────────────────
            const container = document.getElementById('viewport-container');
            const canvas = document.getElementById('webgl-canvas');

            const scene = new THREE.Scene();
            scene.background = new THREE.Color(0x07090E);
            scene.fog = new THREE.FogExp2(0x07090E, 0.008);

            const camera = new THREE.PerspectiveCamera(45, container.clientWidth / container.clientHeight, 0.1, 1000);
            camera.position.set(18, 16, 22);

            const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true, preserveDrawingBuffer: true });
            renderer.setSize(container.clientWidth, container.clientHeight);
            renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
            renderer.shadowMap.enabled = true;
            renderer.shadowMap.type = THREE.PCFSoftShadowMap;

            const controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.target.set(0, 2, 0);

            // Lighting Setup
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.45);
            scene.add(ambientLight);

            const hemiLight = new THREE.HemisphereLight(0x38BDF8, 0x111827, 0.6);
            hemiLight.position.set(0, 50, 0);
            scene.add(hemiLight);

            const sunLight = new THREE.DirectionalLight(0xffffff, 0.85);
            sunLight.position.set(25, 45, 20);
            sunLight.castShadow = true;
            sunLight.shadow.mapSize.width = 2048;
            sunLight.shadow.mapSize.height = 2048;
            sunLight.shadow.camera.near = 0.5;
            sunLight.shadow.camera.far = 150;
            const d = 30;
            sunLight.shadow.camera.left = -d;
            sunLight.shadow.camera.right = d;
            sunLight.shadow.camera.top = d;
            sunLight.shadow.camera.bottom = -d;
            scene.add(sunLight);

            // Ground Grid Setup
            const gridGroup = new THREE.Group();
            const gridHelper = new THREE.GridHelper(60, 60, 0x3B82F6, 0x1E293B);
            gridHelper.position.y = -0.01;
            gridGroup.add(gridHelper);

            const axesHelper = new THREE.AxesHelper(3);
            axesHelper.position.set(-25, 0.1, -25);
            gridGroup.add(axesHelper);
            scene.add(gridGroup);

            // ROTATING CONSTRUCTION PLATFORM
            const platformGroup = new THREE.Group();
            const platGeo = new THREE.BoxGeometry(26, 0.4, 26);
            const platMat = new THREE.MeshStandardMaterial({
                color: 0x1E293B,
                metalness: 0.6,
                roughness: 0.2
            });
            const platformMesh = new THREE.Mesh(platGeo, platMat);
            platformMesh.position.y = -0.25;
            platformMesh.receiveShadow = true;
            platformGroup.add(platformMesh);

            const edgesGeo = new THREE.EdgesGeometry(platGeo);
            const edgesMat = new THREE.LineBasicMaterial({ color: 0x06B6D4, linewidth: 2 });
            const edgeLine = new THREE.LineSegments(edgesGeo, edgesMat);
            edgeLine.position.y = -0.25;
            platformGroup.add(edgeLine);
            scene.add(platformGroup);

            // Building Root Mesh Group
            const buildingGroup = new THREE.Group();
            scene.add(buildingGroup);

            let selectionOutline = null;
            let rulerPoints = [];
            let rulerLineMesh = null;
            let isUserInteracting = false;

            controls.addEventListener('start', () => { isUserInteracting = true; });

            // ─────────────────────────────────────────────────────────────
            // 3D TEXT SPRITE
            // ─────────────────────────────────────────────────────────────
            function createTextSprite(text, subtext) {
                const canvas = document.createElement('canvas');
                canvas.width = 256;
                canvas.height = 128;
                const ctx = canvas.getContext('2d');

                ctx.fillStyle = 'rgba(13, 19, 33, 0.88)';
                ctx.strokeStyle = '#06B6D4';
                ctx.lineWidth = 4;
                ctx.beginPath();
                ctx.roundRect(8, 8, 240, 112, 12);
                ctx.fill();
                ctx.stroke();

                ctx.fillStyle = '#F8FAFC';
                ctx.font = 'bold 22px Inter, sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText(text, 128, 50);

                ctx.fillStyle = '#38BDF8';
                ctx.font = '16px Inter, sans-serif';
                ctx.fillText(subtext, 128, 85);

                const texture = new THREE.CanvasTexture(canvas);
                const spriteMat = new THREE.SpriteMaterial({ map: texture, transparent: true });
                const sprite = new THREE.Sprite(spriteMat);
                sprite.scale.set(4, 2, 1);
                return sprite;
            }

            // ─────────────────────────────────────────────────────────────
            // REAL-TIME 3D SCENE REGENERATOR
            // ─────────────────────────────────────────────────────────────
            function rebuild3DScene() {
                saveHistoryState();

                while (buildingGroup.children.length > 0) {
                    const child = buildingGroup.children[0];
                    buildingGroup.remove(child);
                }

                if (selectionOutline) {
                    scene.remove(selectionOutline);
                    selectionOutline = null;
                }

                state.floors.forEach((floor) => {
                    if (!floor.visible) return;

                    const floorElev = floor.elevation;

                    floor.rooms.forEach(room => {
                        const roomGroup = new THREE.Group();
                        roomGroup.userData = { roomId: room.id, floorId: floor.id, roomData: room };

                        const L = parseFloat(room.length);
                        const W = parseFloat(room.width);
                        const H = parseFloat(room.height);
                        const T = parseFloat(room.wallThickness);
                        const matKey = room.material || 'wood';
                        const matDef = MATERIALS[matKey] || MATERIALS.wood;

                        // 1. FLOOR SLAB
                        const slabGeo = new THREE.BoxGeometry(L, 0.15, W);
                        const slabMat = new THREE.MeshStandardMaterial({
                            color: matDef.color,
                            roughness: matDef.roughness,
                            metalness: 0.1
                        });
                        const slabMesh = new THREE.Mesh(slabGeo, slabMat);
                        slabMesh.position.set(room.x + L / 2, floorElev + 0.075, room.z + W / 2);
                        slabMesh.receiveShadow = true;
                        slabMesh.castShadow = true;
                        roomGroup.add(slabMesh);

                        // 2. WALLS
                        const wallMat = new THREE.MeshStandardMaterial({
                            color: 0xE2E8F0,
                            roughness: 0.5,
                            metalness: 0.05
                        });

                        const nGeo = new THREE.BoxGeometry(L, H, T);
                        const nMesh = new THREE.Mesh(nGeo, wallMat);
                        nMesh.position.set(room.x + L / 2, floorElev + 0.15 + H / 2, room.z + W - T / 2);
                        nMesh.castShadow = true;
                        nMesh.receiveShadow = true;
                        roomGroup.add(nMesh);

                        const sGeo = new THREE.BoxGeometry(L, H, T);
                        const sMesh = new THREE.Mesh(sGeo, wallMat);
                        sMesh.position.set(room.x + L / 2, floorElev + 0.15 + H / 2, room.z + T / 2);
                        sMesh.castShadow = true;
                        sMesh.receiveShadow = true;
                        roomGroup.add(sMesh);

                        const eGeo = new THREE.BoxGeometry(T, H, W - 2 * T);
                        const eMesh = new THREE.Mesh(eGeo, wallMat);
                        eMesh.position.set(room.x + L - T / 2, floorElev + 0.15 + H / 2, room.z + W / 2);
                        eMesh.castShadow = true;
                        eMesh.receiveShadow = true;
                        roomGroup.add(eMesh);

                        const wGeo = new THREE.BoxGeometry(T, H, W - 2 * T);
                        const wMesh = new THREE.Mesh(wGeo, wallMat);
                        wMesh.position.set(room.x + T / 2, floorElev + 0.15 + H / 2, room.z + W / 2);
                        wMesh.castShadow = true;
                        wMesh.receiveShadow = true;
                        roomGroup.add(wMesh);

                        // 3. CORNER COLUMNS
                        const colMat = new THREE.MeshStandardMaterial({ color: 0x64748B, roughness: 0.3 });
                        const colGeo = new THREE.BoxGeometry(T * 1.4, H, T * 1.4);
                        [[0, 0], [L, 0], [0, W], [L, W]].forEach(([cx, cz]) => {
                            const cMesh = new THREE.Mesh(colGeo, colMat);
                            cMesh.position.set(room.x + cx, floorElev + 0.15 + H / 2, room.z + cz);
                            cMesh.castShadow = true;
                            roomGroup.add(cMesh);
                        });

                        // 4. CEILING SLAB
                        if (state.settings.showCeilings) {
                            const ceilGeo = new THREE.BoxGeometry(L, 0.1, W);
                            const ceilMat = new THREE.MeshStandardMaterial({ color: 0xF1F5F9, transparent: true, opacity: 0.85 });
                            const ceilMesh = new THREE.Mesh(ceilGeo, ceilMat);
                            ceilMesh.position.set(room.x + L / 2, floorElev + 0.15 + H + 0.05, room.z + W / 2);
                            ceilMesh.castShadow = true;
                            roomGroup.add(ceilMesh);
                        }

                        // 5. 3D ROOM SPRITE LABEL
                        if (state.settings.showLabels) {
                            const areaVal = (L * W).toFixed(1);
                            const unitText = state.project.units === 'meters' ? 'm²' : 'sq.ft';
                            const sprite = createTextSprite(room.name, `${areaVal} ${unitText}`);
                            sprite.position.set(room.x + L / 2, floorElev + H + 1.2, room.z + W / 2);
                            roomGroup.add(sprite);
                        }

                        buildingGroup.add(roomGroup);

                        if (state.selectedRoomId === room.id) {
                            highlightSelectedRoom(roomGroup);
                        }
                    });
                });

                updateUI();
            }

            function highlightSelectedRoom(roomGroup) {
                if (selectionOutline) scene.remove(selectionOutline);
                selectionOutline = new THREE.BoxHelper(roomGroup, 0x06B6D4);
                selectionOutline.material.linewidth = 3;
                scene.add(selectionOutline);
            }

            // ─────────────────────────────────────────────────────────────
            // RAYCAST SELECTION & SPATIAL CONTEXT MENU
            // ─────────────────────────────────────────────────────────────
            const raycaster = new THREE.Raycaster();
            const mouse = new THREE.Vector2();
            const contextMenu = document.getElementById('spatial-context-menu');

            window.addEventListener('click', (e) => {
                contextMenu.style.display = 'none';

                const rect = renderer.domElement.getBoundingClientRect();
                if (e.clientX < rect.left || e.clientX > rect.right || e.clientY < rect.top || e.clientY > rect.bottom) {
                    return;
                }

                mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
                mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

                if (state.settings.rulerMode) {
                    handleRulerClick(mouse);
                    return;
                }

                raycaster.setFromCamera(mouse, camera);
                const intersects = raycaster.intersectObjects(buildingGroup.children, true);

                if (intersects.length > 0) {
                    let curr = intersects[0].object;
                    while (curr && !curr.userData.roomId && curr.parent) {
                        curr = curr.parent;
                    }
                    if (curr && curr.userData.roomId) {
                        state.selectedRoomId = curr.userData.roomId;
                        highlightSelectedRoom(curr);
                        updatePropsPanel(curr.userData.roomData);
                        toggleFloatingPanel('panel-object-inspector', true);
                        renderHierarchyTree();
                    }
                } else {
                    state.selectedRoomId = null;
                    if (selectionOutline) {
                        scene.remove(selectionOutline);
                        selectionOutline = null;
                    }
                    toggleFloatingPanel('panel-object-inspector', false);
                    renderHierarchyTree();
                }
            });

            // Context Menu Trigger on Right Click
            window.addEventListener('contextmenu', (e) => {
                const rect = renderer.domElement.getBoundingClientRect();
                if (e.clientX >= rect.left && e.clientX <= rect.right && e.clientY >= rect.top && e.clientY <= rect.bottom) {
                    e.preventDefault();
                    mouse.x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
                    mouse.y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

                    raycaster.setFromCamera(mouse, camera);
                    const intersects = raycaster.intersectObjects(buildingGroup.children, true);

                    if (intersects.length > 0) {
                        let curr = intersects[0].object;
                        while (curr && !curr.userData.roomId && curr.parent) {
                            curr = curr.parent;
                        }
                        if (curr && curr.userData.roomId) {
                            state.selectedRoomId = curr.userData.roomId;
                            highlightSelectedRoom(curr);
                            updatePropsPanel(curr.userData.roomData);
                            toggleFloatingPanel('panel-object-inspector', true);
                        }
                    }

                    contextMenu.style.left = `${e.clientX}px`;
                    contextMenu.style.top = `${e.clientY}px`;
                    contextMenu.style.display = 'block';
                }
            });

            window.contextAction = function(action) {
                contextMenu.style.display = 'none';
                if (!state.selectedRoomId) return;

                if (action === 'focus') {
                    for (const floor of state.floors) {
                        const room = floor.rooms.find(r => r.id === state.selectedRoomId);
                        if (room) {
                            animateCamera(
                                new THREE.Vector3(room.x + room.length / 2 + 6, floor.elevation + room.height + 6, room.z + room.width / 2 + 6),
                                new THREE.Vector3(room.x + room.length / 2, floor.elevation, room.z + room.width / 2)
                            );
                            break;
                        }
                    }
                } else if (action === 'duplicate') {
                    document.getElementById('prop-btn-duplicate').click();
                } else if (action === 'delete') {
                    document.getElementById('prop-btn-delete').click();
                } else if (action === 'isolate') {
                    state.floors.forEach(f => {
                        f.rooms.forEach(r => {
                            if (r.id !== state.selectedRoomId) r.material = 'concrete';
                        });
                    });
                    rebuild3DScene();
                }
            };

            // ─────────────────────────────────────────────────────────────
            // DISTANCE RULER TOOL
            // ─────────────────────────────────────────────────────────────
            function handleRulerClick(m) {
                raycaster.setFromCamera(m, camera);
                const intersects = raycaster.intersectObjects([platformMesh, ...buildingGroup.children], true);
                if (intersects.length > 0) {
                    const pt = intersects[0].point;
                    rulerPoints.push(pt);

                    if (rulerPoints.length === 2) {
                        const dist = rulerPoints[0].distanceTo(rulerPoints[1]);
                        drawRulerLine(rulerPoints[0], rulerPoints[1], dist);
                        rulerPoints = [];
                        state.settings.rulerMode = false;
                    }
                }
            }

            function drawRulerLine(p1, p2, dist) {
                if (rulerLineMesh) scene.remove(rulerLineMesh);
                const points = [p1, p2];
                const geometry = new THREE.BufferGeometry().setFromPoints(points);
                const material = new THREE.LineBasicMaterial({ color: 0x06B6D4, linewidth: 4 });
                rulerLineMesh = new THREE.Line(geometry, material);
                scene.add(rulerLineMesh);

                const tooltip = document.getElementById('ruler-tooltip');
                tooltip.style.display = 'block';
                const unitStr = state.project.units === 'meters' ? 'm' : 'ft';
                const val = state.project.units === 'meters' ? dist : dist * 3.28084;
                tooltip.innerText = `📏 Distance: ${val.toFixed(2)} ${unitStr}`;

                setTimeout(() => {
                    tooltip.style.display = 'none';
                    if (rulerLineMesh) scene.remove(rulerLineMesh);
                }, 5000);
            }

            window.toggleRulerTool = function() {
                state.settings.rulerMode = !state.settings.rulerMode;
                rulerPoints = [];
            };

            // ─────────────────────────────────────────────────────────────
            // UI FLOATING PANELS & HIERARCHY TREE RENDERERS
            // ─────────────────────────────────────────────────────────────
            window.toggleFloatingPanel = function(panelId, forceState) {
                const panel = document.getElementById(panelId);
                if (!panel) return;

                if (forceState !== undefined) {
                    if (forceState) panel.classList.remove('hidden');
                    else panel.classList.add('hidden');
                } else {
                    panel.classList.toggle('hidden');
                }
            };

            window.switchWorkspaceMode = function(modeName) {
                state.activeMode = modeName;
                document.getElementById('active-mode-btn').innerText = `🎯 Mode: ${modeName} ▼`;

                if (modeName === 'Presentation') {
                    // Hide all floating panels for 100% clean cinematic viewport
                    document.querySelectorAll('.floating-panel').forEach(p => p.classList.add('hidden'));
                    state.settings.showLabels = false;
                    rebuild3DScene();
                } else if (modeName === 'Inspection') {
                    state.settings.showLabels = true;
                    toggleFloatingPanel('panel-bim-analytics', true);
                    rebuild3DScene();
                } else {
                    state.settings.showLabels = true;
                    rebuild3DScene();
                }
            };

            function updateUI() {
                renderFloorList();
                renderHierarchyTree();
                calculateBIMAnalytics();
                updateBannerState();
            }

            function updateBannerState() {
                const totalRooms = state.floors.reduce((acc, f) => acc + f.rooms.length, 0);
                const banner = document.getElementById('platform-banner');
                if (totalRooms > 0 || isUserInteracting) {
                    banner.style.opacity = '0';
                } else {
                    banner.style.opacity = '1';
                }
            }

            function renderFloorList() {
                const listEl = document.getElementById('floor-list');
                const targetSel = document.getElementById('room-target-floor');
                if (!listEl || !targetSel) return;

                listEl.innerHTML = '';
                targetSel.innerHTML = '';

                state.floors.forEach((floor) => {
                    const card = document.createElement('div');
                    card.className = `item-card ${floor.id === state.activeFloorId ? 'active' : ''}`;
                    card.innerHTML = `
                        <span>🏢 ${floor.name} (${floor.elevation.toFixed(1)}m)</span>
                        <div style="display:flex; gap:0.25rem;">
                            <button class="btn-action" style="padding:0.15rem 0.35rem; font-size:0.65rem;" onclick="toggleFloorVis('${floor.id}', event)">${floor.visible ? '👁️' : '🙈'}</button>
                            ${state.floors.length > 1 ? `<button class="btn-action btn-action-danger" style="padding:0.15rem 0.35rem; font-size:0.65rem;" onclick="deleteFloor('${floor.id}', event)">🗑️</button>` : ''}
                        </div>
                    `;
                    card.onclick = () => {
                        state.activeFloorId = floor.id;
                        renderFloorList();
                    };
                    listEl.appendChild(card);

                    const opt = document.createElement('option');
                    opt.value = floor.id;
                    opt.innerText = `${floor.name} (${floor.rooms.length} rooms)`;
                    if (floor.id === state.activeFloorId) opt.selected = true;
                    targetSel.appendChild(opt);
                });
            }

            window.toggleFloorVis = function(fId, e) {
                e.stopPropagation();
                const floor = state.floors.find(f => f.id === fId);
                if (floor) {
                    floor.visible = !floor.visible;
                    rebuild3DScene();
                }
            };

            window.deleteFloor = function(fId, e) {
                e.stopPropagation();
                if (state.floors.length <= 1) return;
                state.floors = state.floors.filter(f => f.id !== fId);
                state.activeFloorId = state.floors[0].id;
                rebuild3DScene();
            };

            function renderHierarchyTree() {
                const container = document.getElementById('tree-container');
                if (!container) return;

                container.innerHTML = '';

                const projNode = document.createElement('div');
                projNode.className = 'tree-header selected';
                projNode.innerHTML = `<span>🏢 ${state.project.name} (${state.project.type})</span>`;
                container.appendChild(projNode);

                state.floors.forEach(floor => {
                    const fNode = document.createElement('div');
                    fNode.className = 'tree-node';
                    fNode.innerHTML = `
                        <div class="tree-header">
                            <span>📑 ${floor.name} [Elev: ${floor.elevation}m]</span>
                        </div>
                    `;
                    const rList = document.createElement('div');
                    rList.className = 'tree-node';

                    floor.rooms.forEach(room => {
                        const rHeader = document.createElement('div');
                        rHeader.className = `tree-header ${room.id === state.selectedRoomId ? 'selected' : ''}`;
                        rHeader.innerHTML = `<span>🔲 ${room.name} (${room.length}×${room.width}m)</span>`;
                        rHeader.onclick = () => {
                            state.selectedRoomId = room.id;
                            rebuild3DScene();
                            updatePropsPanel(room);
                            toggleFloatingPanel('panel-object-inspector', true);
                        };
                        rList.appendChild(rHeader);
                    });

                    fNode.appendChild(rList);
                    container.appendChild(fNode);
                });
            }

            function updatePropsPanel(room) {
                const propForm = document.getElementById('props-form');
                if (!propForm) return;

                document.getElementById('prop-name').value = room.name;
                document.getElementById('prop-len').value = room.length;
                document.getElementById('prop-wid').value = room.width;
                document.getElementById('prop-hgt').value = room.height;
                document.getElementById('prop-wall-th').value = room.wallThickness;
                document.getElementById('prop-x').value = room.x;
                document.getElementById('prop-z').value = room.z;

                const area = (parseFloat(room.length) * parseFloat(room.width)).toFixed(2);
                const vol = (area * parseFloat(room.height)).toFixed(2);
                const uStr = state.project.units === 'meters' ? 'm' : 'ft';
                document.getElementById('prop-calc-area').innerText = `Area: ${area} ${uStr}²`;
                document.getElementById('prop-calc-vol').innerText = `Volume: ${vol} ${uStr}³`;
            }

            function calculateBIMAnalytics() {
                let totalBuiltup = 0;
                let totalCarpet = 0;
                let totalWall = 0;
                let totalVol = 0;
                let totalRooms = 0;

                state.floors.forEach(floor => {
                    floor.rooms.forEach(room => {
                        totalRooms++;
                        const L = parseFloat(room.length);
                        const W = parseFloat(room.width);
                        const H = parseFloat(room.height);
                        const T = parseFloat(room.wallThickness);

                        const roomBuiltup = L * W;
                        const roomCarpet = (L - 2 * T) * (W - 2 * T);
                        const roomWall = 2 * (L + W) * H;
                        const roomVol = roomBuiltup * H;

                        totalBuiltup += roomBuiltup;
                        totalCarpet += Math.max(0, roomCarpet);
                        totalWall += roomWall;
                        totalVol += roomVol;
                    });
                });

                const isMeters = state.project.units === 'meters';
                const areaFactor = isMeters ? 1.0 : 10.7639;
                const volFactor = isMeters ? 1.0 : 35.3147;
                const uAreaStr = isMeters ? 'm²' : 'sq.ft';
                const uVolStr = isMeters ? 'm³' : 'cu.ft';

                document.getElementById('stat-builtup').innerText = `${(totalBuiltup * areaFactor).toFixed(1)} ${uAreaStr}`;
                document.getElementById('stat-carpet').innerText = `${(totalCarpet * areaFactor).toFixed(1)} ${uAreaStr}`;
                document.getElementById('stat-wall').innerText = `${(totalWall * areaFactor).toFixed(1)} ${uAreaStr}`;
                document.getElementById('stat-vol').innerText = `${(totalVol * volFactor).toFixed(1)} ${uVolStr}`;
                document.getElementById('stat-floors-cnt').innerText = state.floors.length;
                document.getElementById('stat-rooms-cnt').innerText = totalRooms;

                const mBuilt = document.getElementById('modal-builtup');
                if (mBuilt) mBuilt.innerText = `${(totalBuiltup * areaFactor).toFixed(1)} ${uAreaStr}`;
                const mCarp = document.getElementById('modal-carpet');
                if (mCarp) mCarp.innerText = `${(totalCarpet * areaFactor).toFixed(1)} ${uAreaStr}`;
                const mWall = document.getElementById('modal-wall');
                if (mWall) mWall.innerText = `${(totalWall * areaFactor).toFixed(1)} ${uAreaStr}`;
            }

            // ─────────────────────────────────────────────────────────────
            // EVENT LISTENERS & UI CONTROLS
            // ─────────────────────────────────────────────────────────────
            document.getElementById('btn-add-floor').addEventListener('click', () => {
                const count = state.floors.length;
                const prevElev = state.floors[count - 1].elevation;
                const prevHgt = state.floors[count - 1].height;
                const newFloor = {
                    id: `floor_${Date.now()}`,
                    name: count === 1 ? '1st Floor' : count === 2 ? '2nd Floor' : `${count}th Floor`,
                    elevation: prevElev + prevHgt,
                    height: state.project.defaultFloorHeight,
                    visible: true,
                    rooms: []
                };
                state.floors.push(newFloor);
                state.activeFloorId = newFloor.id;
                rebuild3DScene();
            });

            window.openPresetRoom = function(presetKey) {
                toggleFloatingPanel('panel-room-builder', true);
                const sel = document.getElementById('room-preset-select');
                if (sel) {
                    sel.value = presetKey;
                    sel.dispatchEvent(new Event('change'));
                }
            };

            document.getElementById('room-preset-select').addEventListener('change', (e) => {
                const val = e.target.value;
                const presets = {
                    bedroom: { name: 'Master Bedroom', len: 5.0, wid: 4.0, hgt: 3.0, mat: 'wood' },
                    kitchen: { name: 'Modular Kitchen', len: 4.0, wid: 3.5, hgt: 3.0, mat: 'tiles' },
                    hall: { name: 'Living Hall', len: 8.0, wid: 6.0, hgt: 3.2, mat: 'marble' },
                    office: { name: 'Executive Office', len: 6.0, wid: 5.0, hgt: 3.0, mat: 'carpet' },
                    conference: { name: 'Conference Room', len: 8.0, wid: 5.0, hgt: 3.2, mat: 'carpet' },
                    bathroom: { name: 'Luxury Bathroom', len: 3.0, wid: 2.5, hgt: 2.8, mat: 'tiles' }
                };
                if (presets[val]) {
                    const p = presets[val];
                    document.getElementById('room-name').value = p.name;
                    document.getElementById('room-len').value = p.len;
                    document.getElementById('room-wid').value = p.wid;
                    document.getElementById('room-hgt').value = p.hgt;
                    document.getElementById('room-mat').value = p.mat;
                }
            });

            document.getElementById('btn-add-room').addEventListener('click', () => {
                const targetFloorId = document.getElementById('room-target-floor').value;
                const targetFloor = state.floors.find(f => f.id === targetFloorId);
                if (!targetFloor) return;

                const name = document.getElementById('room-name').value.trim() || 'New Room';
                let len = Math.max(0.5, parseFloat(document.getElementById('room-len').value) || 4.0);
                let wid = Math.max(0.5, parseFloat(document.getElementById('room-wid').value) || 4.0);
                let hgt = Math.max(1.0, parseFloat(document.getElementById('room-hgt').value) || 3.0);
                let wallTh = Math.max(0.05, parseFloat(document.getElementById('room-wall-th').value) || 0.2);
                let posX = parseFloat(document.getElementById('room-pos-x').value) || 0.0;
                let posZ = parseFloat(document.getElementById('room-pos-z').value) || 0.0;
                const mat = document.getElementById('room-mat').value;

                if (state.settings.snapToGrid) {
                    posX = Math.round(posX / state.settings.gridSize) * state.settings.gridSize;
                    posZ = Math.round(posZ / state.settings.gridSize) * state.settings.gridSize;
                }

                const newRoom = {
                    id: `room_${Date.now()}`,
                    name: name,
                    length: len,
                    width: wid,
                    height: hgt,
                    wallThickness: wallTh,
                    x: posX,
                    z: posZ,
                    material: mat
                };

                targetFloor.rooms.push(newRoom);
                state.selectedRoomId = newRoom.id;
                rebuild3DScene();
            });

            window.spawnAsset = function(name, len, wid, hgt, mat) {
                const activeFloor = state.floors.find(f => f.id === state.activeFloorId) || state.floors[0];
                const count = activeFloor.rooms.length;
                const newAsset = {
                    id: `asset_${Date.now()}`,
                    name: `${name} ${count + 1}`,
                    length: len,
                    width: wid,
                    height: hgt,
                    wallThickness: 0.15,
                    x: (count % 4) * (len + 1.5) - 4.0,
                    z: Math.floor(count / 4) * (wid + 1.5) - 3.0,
                    material: mat
                };
                activeFloor.rooms.push(newAsset);
                state.selectedRoomId = newAsset.id;
                rebuild3DScene();
            };

            ['prop-name', 'prop-len', 'prop-wid', 'prop-hgt', 'prop-wall-th', 'prop-x', 'prop-z'].forEach(id => {
                document.getElementById(id).addEventListener('input', () => {
                    if (!state.selectedRoomId) return;
                    for (const floor of state.floors) {
                        const room = floor.rooms.find(r => r.id === state.selectedRoomId);
                        if (room) {
                            room.name = document.getElementById('prop-name').value;
                            room.length = Math.max(0.5, parseFloat(document.getElementById('prop-len').value) || 1.0);
                            room.width = Math.max(0.5, parseFloat(document.getElementById('prop-wid').value) || 1.0);
                            room.height = Math.max(1.0, parseFloat(document.getElementById('prop-hgt').value) || 1.0);
                            room.wallThickness = Math.max(0.05, parseFloat(document.getElementById('prop-wall-th').value) || 0.1);
                            room.x = parseFloat(document.getElementById('prop-x').value) || 0.0;
                            room.z = parseFloat(document.getElementById('prop-z').value) || 0.0;
                            rebuild3DScene();
                            updatePropsPanel(room);
                            break;
                        }
                    }
                });
            });

            document.getElementById('prop-btn-delete').addEventListener('click', () => {
                if (!state.selectedRoomId) return;
                state.floors.forEach(f => {
                    f.rooms = f.rooms.filter(r => r.id !== state.selectedRoomId);
                });
                state.selectedRoomId = null;
                toggleFloatingPanel('panel-object-inspector', false);
                rebuild3DScene();
            });

            document.getElementById('prop-btn-duplicate').addEventListener('click', () => {
                if (!state.selectedRoomId) return;
                for (const floor of state.floors) {
                    const room = floor.rooms.find(r => r.id === state.selectedRoomId);
                    if (room) {
                        const dup = { ...room, id: `room_${Date.now()}`, name: `${room.name} (Copy)`, x: room.x + 2.0, z: room.z + 2.0 };
                        floor.rooms.push(dup);
                        state.selectedRoomId = dup.id;
                        rebuild3DScene();
                        break;
                    }
                }
            });

            window.setCamView = function(preset) {
                if (preset === 'iso') animateCamera(new THREE.Vector3(18, 16, 22), new THREE.Vector3(0, 2, 0));
                else if (preset === 'top') animateCamera(new THREE.Vector3(0, 40, 0.001), new THREE.Vector3(0, 0, 0));
                else if (preset === 'front') animateCamera(new THREE.Vector3(0, 4, 35), new THREE.Vector3(0, 4, 0));
                else if (preset === 'side') animateCamera(new THREE.Vector3(35, 4, 0), new THREE.Vector3(0, 4, 0));
            };

            function animateCamera(targetPos, targetLookAt) {
                const startPos = camera.position.clone();
                const startLook = controls.target.clone();
                let duration = 600;
                let startTime = performance.now();

                function step(now) {
                    let elapsed = now - startTime;
                    let progress = Math.min(1, elapsed / duration);
                    let ease = 0.5 - Math.cos(progress * Math.PI) / 2;

                    camera.position.lerpVectors(startPos, targetPos, ease);
                    controls.target.lerpVectors(startLook, targetLookAt, ease);
                    controls.update();

                    if (progress < 1) requestAnimationFrame(step);
                }
                requestAnimationFrame(step);
            }

            window.toggleSnapToGrid = function() {
                state.settings.snapToGrid = !state.settings.snapToGrid;
            };

            window.toggleGridLines = function() {
                state.settings.showGrid = !state.settings.showGrid;
                gridGroup.visible = state.settings.showGrid;
            };

            window.toggleCeilings = function() {
                state.settings.showCeilings = !state.settings.showCeilings;
                rebuild3DScene();
            };

            window.toggleRoomLabels = function() {
                state.settings.showLabels = !state.settings.showLabels;
                rebuild3DScene();
            };

            document.getElementById('btn-screenshot').addEventListener('click', () => {
                renderer.render(scene, camera);
                const dataURL = renderer.domElement.toDataURL('image/png');
                const link = document.createElement('a');
                link.download = `${state.project.name.replace(/\\s+/g, '_')}_Spatial_Render.png`;
                link.href = dataURL;
                link.click();
            });

            function saveHistoryState() {
                if (state.history.length > 25) state.history.shift();
                state.history.push(JSON.stringify(state.floors));
            }

            document.getElementById('btn-undo').addEventListener('click', () => {
                if (state.history.length > 1) {
                    state.redoStack.push(state.history.pop());
                    const lastState = state.history[state.history.length - 1];
                    state.floors = JSON.parse(lastState);
                    rebuild3DScene();
                }
            });

            document.getElementById('btn-redo').addEventListener('click', () => {
                if (state.redoStack.length > 0) {
                    const nextState = state.redoStack.pop();
                    state.history.push(nextState);
                    state.floors = JSON.parse(nextState);
                    rebuild3DScene();
                }
            });

            document.getElementById('proj-units').addEventListener('change', (e) => {
                state.project.units = e.target.value;
                calculateBIMAnalytics();
                rebuild3DScene();
            });

            // ─────────────────────────────────────────────────────────────
            // DRAGGABLE FLOATING PANELS ENGINE
            // ─────────────────────────────────────────────────────────────
            function makePanelsDraggable() {
                const panels = document.querySelectorAll('.floating-panel');
                panels.forEach(panel => {
                    const header = panel.querySelector('.panel-drag-header');
                    if (!header) return;

                    let isDragging = false;
                    let offsetX = 0;
                    let offsetY = 0;

                    header.addEventListener('mousedown', (e) => {
                        isDragging = true;
                        offsetX = e.clientX - panel.offsetLeft;
                        offsetY = e.clientY - panel.offsetTop;
                        panel.style.zIndex = 100;
                    });

                    window.addEventListener('mousemove', (e) => {
                        if (!isDragging) return;
                        panel.style.left = `${e.clientX - offsetX}px`;
                        panel.style.top = `${e.clientY - offsetY}px`;
                    });

                    window.addEventListener('mouseup', () => {
                        if (isDragging) {
                            isDragging = false;
                            panel.style.zIndex = 30;
                        }
                    });
                });
            }

            // ─────────────────────────────────────────────────────────────
            // INITIAL DEFAULT DEMO SCENE LOAD
            // ─────────────────────────────────────────────────────────────
            function loadDefaultDemoBuilding() {
                state.floors[0].rooms = [
                    { id: "r1", name: "Living Hall", length: 8.0, width: 6.0, height: 3.2, wallThickness: 0.2, x: -4.0, z: -3.0, material: "marble" },
                    { id: "r2", name: "Modular Kitchen", length: 4.5, width: 4.0, height: 3.2, wallThickness: 0.2, x: 4.0, z: -3.0, material: "tiles" }
                ];
                rebuild3DScene();
                makePanelsDraggable();
            }

            // ─────────────────────────────────────────────────────────────
            // ANIMATION LOOP & RESIZE HANDLER
            // ─────────────────────────────────────────────────────────────
            let lastTime = performance.now();
            let frameCount = 0;

            function animate() {
                requestAnimationFrame(animate);

                const totalRooms = state.floors.reduce((acc, f) => acc + f.rooms.length, 0);
                if (totalRooms === 0 && !isUserInteracting) {
                    platformGroup.rotation.y += 0.005;
                }

                controls.update();
                renderer.render(scene, camera);

                frameCount++;
                const now = performance.now();
                if (now - lastTime >= 1000) {
                    document.getElementById('stat-fps').innerText = `${frameCount} FPS`;
                    frameCount = 0;
                    lastTime = now;
                }
            }

            const updateViewportDimensions = () => {
                const w = container.clientWidth;
                const h = container.clientHeight;
                if (w > 0 && h > 0) {
                    camera.aspect = w / h;
                    camera.updateProjectionMatrix();
                    renderer.setSize(w, h);
                }
            };

            window.addEventListener('resize', updateViewportDimensions);

            if (window.ResizeObserver && container) {
                const ro = new ResizeObserver(() => {
                    updateViewportDimensions();
                });
                ro.observe(container);
            }

            // Initialize Spatial App
            loadDefaultDemoBuilding();
            animate();
        })();
        </script>
    </body>
    </html>
    """

    components.html(visualizer_html, height=820, scrolling=False)
