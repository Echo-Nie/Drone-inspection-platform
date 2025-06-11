from datetime import datetime
from services.history_service import load_history

def get_statistics_data(data):
    start_date = datetime.strptime(data.get('startDate', ''), '%Y-%m-%d')
    end_date = datetime.strptime(data.get('endDate', ''), '%Y-%m-%d')
    selected_classes = data.get('classes', [])
    result_filter = data.get('result', 'all')

    history = load_history()
    
    filtered_history = [
        record for record in history
        if start_date <= datetime.strptime(record['date'], '%Y-%m-%d %H:%M:%S') <= end_date
    ]

    if selected_classes and 'all' not in selected_classes:
        filtered_history = [
            record for record in filtered_history
            if any(cls in selected_classes for cls in record.get('main_classes', []))
        ]

    if result_filter != 'all':
        filtered_history = [
            record for record in filtered_history
            if record.get('status', '') == result_filter
        ]

    dates = []
    counts = []
    distribution = {}
    confidence_data = {}
    records = []

    for record in filtered_history:
        date = record['date'].split()[0]
        if date not in dates:
            dates.append(date)
            counts.append(1)
        else:
            counts[dates.index(date)] += 1

        for cls in record.get('main_classes', []):
            distribution[cls] = distribution.get(cls, 0) + 1

        class_confidences = record.get('class_confidences', {})
        for cls, conf in class_confidences.items():
            if cls not in confidence_data:
                confidence_data[cls] = []
            confidence_data[cls].append(conf)

        records.append({
            'date': record['date'],
            'total_objects': record['total_objects'],
            'main_classes': record.get('main_classes', []),
            'avg_confidence': record.get('avg_confidence', 0),
            'status': record.get('status', 'success'),
            'status_text': '成功' if record.get('status', 'success') == 'success' else '失败'
        })

    confidence = {
        cls: sum(confs) / len(confs) if confs else 0
        for cls, confs in confidence_data.items()
    }

    response_data = {
        'dates': dates,
        'counts': counts,
        'distribution': [{'name': k, 'value': v} for k, v in distribution.items()],
        'classes': list(confidence.keys()),
        'confidence': [v * 100 for v in confidence.values()],
        'records': records
    }

    return response_data 