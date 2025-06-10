// 文件上传预览和交互效果
document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.querySelector('input[type="file"]');
    const uploadForm = document.querySelector('.upload-form');
    const container = document.querySelector('.container');

    // 添加页面加载动画
    container.style.opacity = '0';
    setTimeout(() => {
        container.style.transition = 'opacity 0.5s ease';
        container.style.opacity = '1';
    }, 100);

    // 文件上传预览
    fileInput.addEventListener('change', function (e) {
        const file = e.target.files[0];
        if (file) {
            // 文件类型验证
            if (!file.type.startsWith('image/')) {
                showMessage('请上传图片文件！', 'error');
                fileInput.value = '';
                return;
            }

            // 文件大小验证（限制为10MB）
            if (file.size > 10 * 1024 * 1024) {
                showMessage('图片大小不能超过10MB！', 'error');
                fileInput.value = '';
                return;
            }

            // 显示文件名
            const fileName = file.name;
            const fileLabel = document.createElement('div');
            fileLabel.className = 'file-label';
            fileLabel.innerHTML = `<i class="fas fa-file-image"></i> ${fileName}`;

            // 移除之前的文件名显示
            const oldLabel = uploadForm.querySelector('.file-label');
            if (oldLabel) oldLabel.remove();

            uploadForm.insertBefore(fileLabel, fileInput.nextSibling);

            // 添加文件选择动画
            fileInput.style.borderColor = '#4a90e2';
            setTimeout(() => {
                fileInput.style.borderColor = '';
            }, 1000);
        }
    });

    // 表单提交时的加载状态
    uploadForm.addEventListener('submit', function (e) {
        const submitBtn = this.querySelector('button[type="submit"]');
        const originalText = submitBtn.innerHTML;

        submitBtn.disabled = true;
        submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> 处理中...';

        // 添加提交动画
        this.style.transform = 'scale(0.98)';
        setTimeout(() => {
            this.style.transform = 'scale(1)';
        }, 200);
    });

    // 导航菜单交互
    const navLinks = document.querySelectorAll('.nav-link');
    navLinks.forEach(link => {
        link.addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-2px)';
        });

        link.addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0)';
        });
    });

    // 统计卡片动画
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach(card => {
        card.addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-5px)';
        });

        card.addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0)';
        });
    });

    // 历史记录项动画
    const historyItems = document.querySelectorAll('.history-item');
    historyItems.forEach(item => {
        item.addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-5px)';
        });

        item.addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0)';
        });
    });
});

// 显示消息提示
function showMessage(message, type = 'info') {
    const msgDiv = document.createElement('div');
    msgDiv.className = `msg ${type}`;
    msgDiv.innerHTML = message;

    // 移除旧的消息
    const oldMsg = document.querySelector('.msg');
    if (oldMsg) oldMsg.remove();

    document.querySelector('.container').insertBefore(msgDiv, document.querySelector('.upload-form'));

    // 添加动画效果
    msgDiv.style.opacity = '0';
    msgDiv.style.transform = 'translateY(-10px)';

    setTimeout(() => {
        msgDiv.style.transition = 'all 0.3s ease';
        msgDiv.style.opacity = '1';
        msgDiv.style.transform = 'translateY(0)';
    }, 100);

    // 3秒后自动消失
    setTimeout(() => {
        msgDiv.style.opacity = '0';
        msgDiv.style.transform = 'translateY(-10px)';
        setTimeout(() => msgDiv.remove(), 300);
    }, 3000);
} 