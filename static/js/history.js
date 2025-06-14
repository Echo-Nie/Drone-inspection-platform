document.addEventListener('DOMContentLoaded', function () {
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');
    const confirmModal = document.getElementById('confirmModal');
    const confirmBtn = document.getElementById('confirmBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const modalTitle = document.getElementById('modalTitle');
    const modalMessage = document.getElementById('modalMessage');
    const historyGrid = document.querySelector('.history-grid');

    // 显示消息函数
    function showMessage(message, type) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `msg center-popup-message ${type}`;
        msgDiv.innerHTML = message;
        document.body.appendChild(msgDiv);

        msgDiv.style.opacity = '0';
        msgDiv.style.transform = 'translate(-50%, -60px)';

        setTimeout(() => {
            msgDiv.style.transition = 'all 0.4s ease-out';
            msgDiv.style.opacity = '1';
            msgDiv.style.transform = 'translate(-50%, -50%)';
        }, 50);

        setTimeout(() => {
            msgDiv.style.opacity = '0';
            msgDiv.style.transform = 'translate(-50%, -40px)';
            setTimeout(() => msgDiv.remove(), 400);
        }, 2000);
    }

    // 清除所有历史记录按钮点击事件
    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener('click', function () {
            // 检查是否有历史记录
            if (!historyGrid || historyGrid.children.length === 0) {
                showMessage('No history to clear', 'info');
                return;
            }
            modalTitle.textContent = 'Confirm Clear';
            modalMessage.textContent = 'Are you sure you want to clear all history? This action is irreversible.';
            confirmModal.style.display = 'flex';
        });
    }

    // 确认按钮点击事件
    if (confirmBtn) {
        confirmBtn.addEventListener('click', function () {
            confirmModal.style.display = 'none';
            // 提交表单清除所有历史记录
            const form = document.createElement('form');
            form.method = 'POST';
            form.action = '/clear_history';
            document.body.appendChild(form);
            form.submit();
        });
    }

    // 取消按钮点击事件
    if (cancelBtn) {
        cancelBtn.addEventListener('click', function () {
            confirmModal.style.display = 'none';
        });
    }

    // 点击模态框外部关闭
    window.addEventListener('click', function (event) {
        if (event.target === confirmModal) {
            confirmModal.style.display = 'none';
        }
    });
}); 