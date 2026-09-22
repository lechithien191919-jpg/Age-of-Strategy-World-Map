from flask import Flask, render_template_string

app = Flask(__name__)

HTML_CONTENT = """
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Age of Strategy World Map Editor</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background-color: #0b192c;
            color: #fff;
            overflow: hidden;
            user-select: none;
        }
        .main-container {
            padding: 20px;
            max-width: 480px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            height: 100vh;
            box-sizing: border-box;
        }
        h2 { text-align: center; margin-bottom: 20px; }
        .search-box input {
            width: 100%;
            padding: 12px;
            border-radius: 8px;
            border: none;
            background: #fff;
            box-sizing: border-box;
            color: #000;
        }
        .empty-state {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            color: #8ab4f8;
            font-size: 16px;
            text-align: center;
        }
        .add-btn {
            position: fixed;
            bottom: 30px;
            right: 30px;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: #4e73df;
            color: white;
            font-size: 30px;
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 10px rgba(0,0,0,0.5);
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* Popup */
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.7);
            justify-content: center;
            align-items: center;
            z-index: 1000;
        }
        .modal-content {
            background: #fff;
            color: #000;
            padding: 20px;
            border-radius: 15px;
            width: 85%;
            max-width: 350px;
            text-align: center;
        }
        .modal-btn {
            width: 100%;
            padding: 12px;
            margin: 8px 0;
            border-radius: 10px;
            border: 1px solid #ccc;
            background: #f1f1f1;
            cursor: pointer;
            font-size: 16px;
            text-align: left;
            padding-left: 15px;
        }
        .modal-btn b { display: block; font-size: 17px; }
        .modal-btn small { color: #666; }
        .modal-btn.blue {
            background: #1e3d59;
            color: white;
            border: none;
            text-align: center;
        }
        .close-modal { background: #ff4d4d; color: white; border: none; text-align: center; }

        /* Màn hình game chứa hình bản đồ và ranh giới */
        .game-body { display: none; flex-direction: column; height: 100vh; position: relative; }
        .country-top-bar {
            position: absolute;
            top: 15px;
            left: 15px;
            background: rgba(0,0,0,0.8);
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 6px;
            border: 1px solid rgba(255,255,255,0.2);
            z-index: 10;
        }
        .world-map-top-badge {
            position: absolute;
            top: 15px;
            right: 15px;
            background: rgba(0,0,0,0.8);
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 13px;
            border: 1px solid rgba(255,255,255,0.2);
            z-index: 10;
        }
        
        /* Khung chứa hình bản đồ thế giới và lớp ranh giới */
        .map-container-wrapper {
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #0b192c;
            position: relative;
            padding-top: 50px;
            overflow: hidden;
        }
        .map-image-container {
            position: relative;
            max-width: 95%;
            max-height: 80vh;
        }
        .map-image-container img {
            width: 100%;
            height: auto;
            display: block;
            border-radius: 8px;
            border: 2px solid #334155;
            box-shadow: 0 8px 20px rgba(0,0,0,0.6);
        }
        
        /* Lớp ranh giới vẽ đè lên hình ảnh */
        .map-overlay-grid {
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            display: grid;
            grid-template-columns: repeat(10, 1fr);
            grid-template-rows: repeat(8, 1fr);
            gap: 2px;
            padding: 2px;
            box-sizing: border-box;
        }
        .border-cell {
            border: 1px dashed rgba(255, 255, 255, 0.4); /* Đường ranh giới mờ đè lên hình */
            background-color: rgba(0, 0, 0, 0.1);
            cursor: pointer;
            transition: background 0.1s;
            border-radius: 3px;
        }
        .border-cell:hover {
            background-color: rgba(230, 57, 70, 0.4);
            border: 1px solid #e63946;
        }

        /* Bảng chọn màu tô ranh giới */
        .color-palette {
            background: #1e293b;
            padding: 8px;
            display: flex;
            justify-content: center;
            gap: 10px;
            align-items: center;
            border-top: 1px solid #334155;
        }
        .color-option {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            cursor: pointer;
            border: 2px solid transparent;
        }
        .color-option.selected { border-color: #fff; transform: scale(1.1); }

        /* Thanh công cụ dưới đáy */
        .bottom-toolbar {
            display: flex;
            justify-content: space-around;
            background: #fff;
            padding: 10px 5px;
            box-sizing: border-box;
            z-index: 10;
        }
        .tool-btn {
            background: none;
            border: none;
            font-size: 20px;
            cursor: pointer;
            padding: 8px 12px;
            border-radius: 8px;
        }
        .tool-btn.active { background: #d0e1fd; }
    </style>
</head>
<body>

    <div class="main-container" id="homeScreen">
        <h2>My Maps</h2>
        <div class="search-box">
            <input type="text" placeholder="Search map...">
        </div>
        <div class="empty-state">
            <p>Chưa có bản đồ nào!<br>Bấm nút <b>+</b> bên dưới để tải bản đồ thế giới.</p>
        </div>
        <button class="add-btn" onclick="showMapModeModal()">+</button>
    </div>

    <div class="game-body" id="gameScreen">
        <div class="country-top-bar">
            <span>🇻🇳</span>
            <span><b>World Map Editor</b></span>
        </div>
        <div class="world-map-top-badge">
            🌍 Custom Borders
        </div>
        
        <div class="map-container-wrapper">
            <div class="map-image-container">
                <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTrTyhEwc3Z0pVy9IumMD7D6mv6PBo-87apR_sfoXkKAg&s=10" alt="World Map">
                
                <div class="map-overlay-grid" id="overlayGrid"></div>
            </div>
        </div>

        <div class="color-palette">
            <div class="color-option selected" style="background: rgba(0,0,0,0.2);" onclick="selectColor('rgba(0,0,0,0.2)', this)" title="Xóa màu"></div>
            <div class="color-option" style="background: rgba(230,57,70,0.6);" onclick="selectColor('rgba(230,57,70,0.6)', this)"></div>
            <div class="color-option"
            
