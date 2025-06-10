// 文件上传预览和交互效果
document.addEventListener('DOMContentLoaded', function () {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const uploadForm = document.querySelector('.upload-form');
    const container = document.querySelector('.container');

    // 添加页面加载动画
    container.style.opacity = '0';
    setTimeout(() => {
        container.style.transition = 'opacity 0.5s ease';
        container.style.opacity = '1';
    }, 100);

    // 点击上传区域触发文件选择
    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    // 拖放功能
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');

        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            handleFile(file);
        } else {
            showMessage('请上传图片文件！', 'error');
        }
    });

    // 粘贴功能
    document.addEventListener('paste', (e) => {
        const items = e.clipboardData.items;
        for (let i = 0; i < items.length; i++) {
            if (items[i].type.startsWith('image/')) {
                const file = items[i].getAsFile();
                handleFile(file);
                break;
            }
        }
    });

    // 文件选择处理
    fileInput.addEventListener('change', function (e) {
        const file = e.target.files[0];
        if (file) {
            handleFile(file);
        }
    });

    // 文件处理函数
    function handleFile(file) {
        // 文件类型验证
        if (!file.type.startsWith('image/')) {
            showMessage('请上传图片文件！', 'error');
            return;
        }

        // 文件大小验证（限制为10MB）
        if (file.size > 10 * 1024 * 1024) {
            showMessage('图片大小不能超过10MB！', 'error');
            return;
        }

        // 创建预览
        const reader = new FileReader();
        reader.onload = (e) => {
            const preview = document.createElement('img');
            preview.src = e.target.result;
            preview.className = 'preview-image';

            // 清除之前的预览
            const oldPreview = uploadArea.querySelector('.preview-image');
            if (oldPreview) oldPreview.remove();

            uploadArea.appendChild(preview);
            uploadArea.classList.add('has-image');
        };
        reader.readAsDataURL(file);

        // 更新文件输入
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;
    }

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