document.addEventListener('DOMContentLoaded', function () {
    const clearHistoryBtn = document.getElementById('clearHistoryBtn');
    const confirmModal = document.getElementById('confirmModal');
    const confirmBtn = document.getElementById('confirmBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const modalTitle = document.getElementById('modalTitle');
    const modalMessage = document.getElementById('modalMessage');
    const historyGrid = document.querySelector('.history-grid');
    const detailsModal = document.getElementById('detailsModal');
    const detailsClose = document.querySelector('.details-close');
    const detailsImage = document.getElementById('detailsImage');
    const detailsStats = document.getElementById('detailsStats');
    const detailsTable = document.getElementById('detailsTable');

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
        if (event.target === detailsModal) {
            detailsModal.style.display = 'none';
        }
    });

    // 关闭详细信息模态框
    if (detailsClose) {
        detailsClose.addEventListener('click', function () {
            detailsModal.style.display = 'none';
        });
    }

    // 点击历史记录项显示详细信息
    const historyItems = document.querySelectorAll('.history-item');
    historyItems.forEach(item => {
        item.addEventListener('click', async function () {
            const recordId = this.dataset.id;
            try {
                const response = await fetch(`/history/details/${recordId}`);
                if (!response.ok) {
                    throw new Error('Failed to fetch details');
                }
                const data = await response.json();

                // 更新图片
                detailsImage.src = `/static/${data.image_url}`;

                // 更新统计信息
                detailsStats.innerHTML = `
                    <div class="details-card">
                        <div class="num">${data.total_objects}</div>
                        <div class="label">Detected Objects</div>
                    </div>
                    <div class="details-card">
                        <div class="num">${data.avg_confidence.toFixed(2)}</div>
                        <div class="label">Average Confidence</div>
                    </div>
                    ${Object.entries(data.class_confidences).map(([cls, conf]) => `
                        <div class="details-card">
                            <div class="num">${conf.toFixed(2)}</div>
                            <div class="label">${cls} Confidence</div>
                        </div>
                    `).join('')}
                `;

                // 更新检测结果表格
                detailsTable.innerHTML = data.detections.map(det => `
                    <tr>
                        <td>${det.class_name}</td>
                        <td>${det.confidence.toFixed(2)}</td>
                        <td>
                            <span class="coord x1">${det.bbox[0].toFixed(1)}</span>,
                            <span class="coord y1">${det.bbox[1].toFixed(1)}</span>,
                            <span class="coord x2">${det.bbox[2].toFixed(1)}</span>,
                            <span class="coord y2">${det.bbox[3].toFixed(1)}</span>
                        </td>
                    </tr>
                `).join('');

                // 显示模态框
                detailsModal.style.display = 'block';
            } catch (error) {
                console.error('Error:', error);
                showMessage('Failed to load details', 'error');
            }
        });
    });
}); 