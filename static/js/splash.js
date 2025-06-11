document.addEventListener('DOMContentLoaded', () => {
    const splashContainer = document.querySelector('.splash-container');
    const duration = 3000; // 动画总时长，单位毫秒

    // 动画结束后跳转到主页
    setTimeout(() => {
        splashContainer.classList.add('splash-exit'); // 添加退出动画类

        // 等待退出动画完成，然后跳转
        splashContainer.addEventListener('animationend', (e) => {
            if (e.animationName === 'fadeOut') {
                // 重定向到主页的实际URL
                window.location.href = '/index';
            }
        });

    }, duration);
}); 