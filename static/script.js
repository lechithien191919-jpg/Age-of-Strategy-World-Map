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
    const warModal = document.getElementById('warModal');
    if(warModal) warModal.style.display = 'none';
}
function createMap(editionType) {
    alert("Đã tạo map thành công với chế độ: " + editionType + "! Đang chuyển vào game...");
    window.location.href = '/game';
}
function openGame() {
    window.location.href = '/game';
}
function goHome() {
    window.location.href = '/';
}
function openWarMenu() {
    document.getElementById('warModal').style.display = 'flex';
}
function closeWarMenu() {
    document.getElementById('warModal').style.display = 'none';
}
function startWar(mode) {
    if(mode === 'manual') {
        alert("Đã bật chế độ tự chọn vùng đánh! Hãy bấm vào quốc gia muốn tấn công.");
    } else {
        alert("Bot đang tự động triển khai chiến tranh dựa trên lực lượng, xe tăng, máy bay!");
    }
    closeWarMenu();
}
function deleteMap() {
    if(confirm("Bạn có chắc muốn xóa map này không?")) {
        alert("Đã xóa map!");
        window.location.href = '/';
    }
}

