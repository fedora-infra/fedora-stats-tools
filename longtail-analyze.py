import json

comparator = lambda item: item[1]

with open('foo.json', 'r') as f:
    all_data = json.loads(f.read())

for timestamp, data in all_data.items():
    for username, value in data.items():
        all_data[timestamp][username] = float(value)

timestamp_getter = lambda item: item[0]

sorted_data = sorted(all_data.items(), key=timestamp_getter)

results = {}

for timestamp, data in sorted_data:
    head = max(data.items(), key=comparator)
    tail = min(data.items(), key=comparator)

    x1, y1 = 0, head[1]
    x2, y2 = len(data), tail[1]

    slope = (y2 - y1) / (x2 - x1)
    intercept = y1

    metric = 0

    data_tuples = sorted(data.items(), key=comparator, reverse=True)

    for index, item in enumerate(data_tuples):
        username, actual = item
        # line formula is y = slope * x + intercept
        ideal = slope * index + intercept
        diff = ideal - actual
        metric = metric + diff

    print "%s, %f" % (timestamp, metric / len(data))
    results[timestamp] = metric / len(data)


import pygal
chart = pygal.Line()
chart.title = 'lol'
chart.x_labels = [stamp for stamp, blob in sorted_data]
chart.add('Metric', [results[stamp] for stamp, blob in sorted_data])
chart.render_in_browser()
