// 初始化图表
let trendChart = echarts.init(document.getElementById('trendChart'));
let distributionChart = echarts.init(document.getElementById('distributionChart'));
let accuracyChart = echarts.init(document.getElementById('accuracyChart'));

// 图表配置
const trendOption = {
    title: {
        text: '检测数量趋势',
        textStyle: {
            color: '#fff'
        }
    },
    tooltip: {
        trigger: 'axis'
    },
    xAxis: {
        type: 'category',
        data: [],
        axisLabel: {
            color: '#fff'
        }
    },
    yAxis: {
        type: 'value',
        axisLabel: {
            color: '#fff'
        }
    },
    series: [{
        data: [],
        type: 'line',
        smooth: true,
        lineStyle: {
            color: '#4a90e2'
        },
        areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                offset: 0,
                color: 'rgba(74, 144, 226, 0.5)'
            }, {
                offset: 1,
                color: 'rgba(74, 144, 226, 0.1)'
            }])
        }
    }]
};

const distributionOption = {
    title: {
        text: '目标类别分布',
        textStyle: {
            color: '#fff'
        }
    },
    tooltip: {
        trigger: 'item'
    },
    legend: {
        orient: 'vertical',
        right: 10,
        top: 'center',
        textStyle: {
            color: '#fff'
        }
    },
    series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
        },
        label: {
            show: false,
            position: 'center'
        },
        emphasis: {
            label: {
                show: true,
                fontSize: '20',
                fontWeight: 'bold',
                color: '#fff'
            }
        },
        labelLine: {
            show: false
        },
        data: []
    }]
};

const accuracyOption = {
    title: {
        text: '检测置信度统计',
        textStyle: {
            color: '#fff'
        }
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'shadow'
        }
    },
    xAxis: {
        type: 'category',
        data: [],
        axisLabel: {
            color: '#fff'
        }
    },
    yAxis: {
        type: 'value',
        axisLabel: {
            color: '#fff',
            formatter: '{value}%'
        }
    },
    series: [{
        data: [],
        type: 'bar',
        itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                offset: 0,
                color: '#4a90e2'
            }, {
                offset: 1,
                color: '#2c3e50'
            }])
        }
    }]
};

// 应用配置
trendChart.setOption(trendOption);
distributionChart.setOption(distributionOption);
accuracyChart.setOption(accuracyOption);

// 窗口大小改变时重绘图表
window.addEventListener('resize', function () {
    trendChart.resize();
    distributionChart.resize();
    accuracyChart.resize();
});

// 获取数据并更新图表
function updateCharts(data) {
    // 更新趋势图
    trendChart.setOption({
        xAxis: {
            data: data.dates
        },
        series: [{
            data: data.counts
        }]
    });

    // 更新分布图
    distributionChart.setOption({
        series: [{
            data: data.distribution
        }]
    });

    // 更新准确率图
    accuracyChart.setOption({
        xAxis: {
            data: data.classes
        },
        series: [{
            data: data.confidence
        }]
    });
}

// 处理筛选条件变化
document.getElementById('refreshBtn').addEventListener('click', function () {
    const startDate = document.getElementById('startDate').value;
    const endDate = document.getElementById('endDate').value;
    const selectedClasses = Array.from(document.getElementById('classFilter').selectedOptions).map(option => option.value);
    const resultFilter = document.getElementById('resultFilter').value;

    if (!startDate || !endDate) {
        showMessage('请选择时间范围', 'error');
        return;
    }

    // 发送请求获取筛选后的数据
    fetch('/api/statistics', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            startDate,
            endDate,
            classes: selectedClasses,
            result: resultFilter
        })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            if (!data || !data.dates || !data.counts) {
                throw new Error('Invalid data format');
            }
            updateCharts(data);
            updateTable(data.records);
        })
        .catch(error => {
            console.error('Error:', error);
            showMessage('获取数据失败，请重试', 'error');
        });
});

// 更新表格数据
function updateTable(records) {
    const tbody = document.querySelector('#dataTable tbody');
    tbody.innerHTML = '';

    records.forEach(record => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${record.date}</td>
            <td>${record.total_objects}</td>
            <td>${record.main_classes.join(', ')}</td>
            <td>${(record.avg_confidence * 100).toFixed(2)}%</td>
            <td>
                <span class="status-badge ${record.status}">
                    ${record.status_text}
                </span>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// 导出数据
document.getElementById('exportBtn').addEventListener('click', function () {
    const table = document.getElementById('dataTable');
    const rows = Array.from(table.querySelectorAll('tr'));

    // 准备CSV数据
    const csvContent = rows.map(row => {
        const cells = Array.from(row.querySelectorAll('th, td'));
        return cells.map(cell => {
            // 移除HTML标签并处理特殊字符
            const text = cell.textContent.replace(/<[^>]*>/g, '');
            return `"${text.replace(/"/g, '""')}"`;
        }).join(',');
    }).join('\n');

    // 创建下载链接
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `检测数据统计_${new Date().toLocaleDateString()}.csv`;
    link.click();
});

// 初始化日期选择器
function initDateInputs() {
    const today = new Date();
    const lastMonth = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());

    document.getElementById('startDate').value = lastMonth.toISOString().split('T')[0];
    document.getElementById('endDate').value = today.toISOString().split('T')[0];
}

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function () {
    initDateInputs();
    // 触发一次数据刷新
    document.getElementById('refreshBtn').click();
}); 