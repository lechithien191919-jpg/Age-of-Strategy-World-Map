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
        }
        /* Màn hình chính (Trang chủ) */
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

        /* Màn hình chơi game / Bản đồ */
        .game-body { display: none; flex-direction: column; height: 100vh; position: relative; }
        .country-top-bar {
            position: absolute;
            top: 15px;
            left: 15px;
            background: rgba(0,0,0,0.8);
            padding: 6px 12px;
            border-radius: 20px;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
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
        .map-view-container {
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
            background: #1b263b;
            position: relative;
            overflow: hidden;
        }
        .world-map-canvas {
            font-size: 18px;
            color: #769fcd;
            text-align: center;
            padding: 20px;
            line-height: 1.6;
        }
        
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
            <p>Chưa có bản đồ nào!<br>Bấm nút <b>+</b> bên dưới để tạo map mới.</p>
        </div>
        <button class="add-btn" onclick="showMapModeModal()">+</button>
    </div>

    <div class="game-body" id="gameScreen">
        <div class="country-top-bar">
            <span>🇻🇳</span>
            <span><b>Vietnam</b> (Thanh Hóa)</span>
        </div>
        <div class="world-map-top-badge">
            🌍 A+ World Map
        </div>
        
        <div class="map-view-container" onclick="interactMap()">
            <div class="world-map-canvas">
                🗺️ [Bản đồ Thế Giới - 228 Quốc Gia]<br>
                <small style="color: #a0aec0;">Chạm vào vùng đất để chọn quốc gia & chiến tranh</small>
            </div>
        </div>

        <div class="bottom-toolbar">
            <button class="tool-btn" onclick="goHome()">❌</button>
            <button class="tool-btn">↩️</button>
            <button class="tool-btn">↪️</button>
            <button class="tool-btn active">🖱️</button>
            <button class="tool-btn">🔲</button>
            <button class="tool-btn" onclick="openWarMenu()">⚔️</button>
            <button class="tool-btn" onclick="saveMap()">💾</button>
        </div>
    </div>

    <div id="mapModeModal" class="modal">
        <div class="modal-content">
            <h3>Map Options</h3>
            <button class="modal-btn blue" onclick="showMapEditionModal()">🗺️ New Map</button>
            <button class="modal-btn blue" onclick="createMap('Sample Map')">📂 Sample Maps</button>
            <button class="modal-btn close-modal" onclick="closeModals()">Đóng</button>
        </div>
    </div>

    <div id="mapEditionModal" class="modal">
        <div class="modal-content">
            <h3>Map Edition</h3>
            <button class="modal-btn" onclick="createMap('Standard')"><b>Standard</b><br><small>For all phone models</small></button>
            <button class="modal-btn" onclick="createMap('Advanced')"><b>Advanced</b><br><small>For high end phone models</small></button>
            <button class="modal-btn" onclick="createMap('1945')"><b>1945</b><br><small>For all phone models</small></button>
            <button class="modal-btn" onclick="createMap('1914')"><b>1914</b><br><small>For all phone models</small></button>
            <button class="modal-btn" onclick="createMap('Empty Map')"><b>Empty Map</b><br><small>For all phone models</small></button>
            <button class="modal-btn close-modal" onclick="closeModals()">Đóng</button>
        </div>
    </div>

    <div id="warModal" class="modal">
        <div class="modal-content">
            <h3>Chế độ Chiến Tranh ⚔️</h3>
            <button class="modal-btn blue" onclick="alert('Đã bật chế độ tự chọn vùng đánh!'); closeModals();">🎯 Tự chọn vùng muốn chiếm</button>
            <button class="modal-btn blue" onclick="alert('Bot đang tự động triển khai chiến tranh, xe tăng và máy bay!'); closeModals();">🤖 Bot tự động chiếm đất</button>
            <button class="modal-btn close-modal" onclick="closeModals()">Đóng</button>
        </div>
    </div>

    <script>
        function showMapModeModal() {
            document.getElementById('mapModeModal').style.display = 'flex';
        }
        function showMapEditionModal() {
            document.getElementById('mapModeModal').style.display = 'none';
            document.getElementById('mapEditionModal').style.display = 'flex';
        }
        function closeModals() {
            document.getElementById('mapModeModal').style.display = 'none';
            document.getElementById('mapEditionModal').style.display = 'none';
            document.getElementById('warModal').style.display = 'none';
        }
        /* Bấm tạo map là nhảy thẳng vô game luôn không rườm rà */
        function createMap(type) {
            closeModals();
            document.getElementById('homeScreen').style.display = 'none';
            document.getElementById('gameScreen').style.display = 'flex';
        }
        function goHome() {
            if(confirm("Bạn có muốn thoát về màn hình chính không?")) {
                document.getElementById('gameScreen').style.display = 'none';
                document.getElementById('homeScreen').style.display = 'flex';
            }
        }
        function openWarMenu() {
            document.getElementById('warModal').style.display = 'flex';
        }
        function saveMap() {
            alert("Đã lưu bản đồ thành công! 💾");
        }
        function interactMap() {
            // Hiệu ứng chạm đất mở rộng lãnh thổ tương tác
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_CONTENT)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
