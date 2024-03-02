# Исходный список со словарями
data = [
    {
        "id": "7518b750-022a-4092-b902-3b0fb519ee78",
        "createdOn": "2024-01-09T04:09:21.091953",
        "name": "ИП Вязигин_52500-00.pdf",
        "documentName": None,
        "typeName": None,
        "size": 91779,
        "type": 14,
        "signatureId": "ed39a983-a72a-4657-aa8a-80872f194c68"
    },
    {
        "id": "54c41b96-5b86-44b4-993a-1601749f6c5a",
        "createdOn": "2024-01-09T04:09:21.091954",
        "name": "Тех.задание Нива Шевроле.docx",
        "documentName": None,
        "typeName": None,
        "size": 11247,
        "type": 4,
        "signatureId": "0a3bf612-c55b-4bc4-9e44-d00f3226f997"
    },
    {
        "id": "9afcd0da-8539-4173-8bab-937a8d8c08a8",
        "createdOn": "2024-01-09T04:09:21.650948",
        "name": "Информация по закупке №100211874124100002_44.html",
        "documentName": None,
        "typeName": None,
        "size": 0,
        "type": 2,
        "signatureId": "756622d5-cf53-4727-a2fd-394ebaf85fc9"
    },
    {
        "id": "8fbf90ca-f5fa-4670-9f3c-4468800f8e60",
        "createdOn": "2024-01-09T04:09:21.650949",
        "name": "TradeDto-8b08852e-b904-45c7-8eeb-c1170a2a0dfd.xml",
        "documentName": None,
        "typeName": None,
        "size": 3333,
        "type": 3,
        "signatureId": "4bce3e1d-8544-4245-93f0-50e1695c5dc7"
    }
]

# Фильтрация списка словарей по значению поля "type"
filtered_data = [item.get('id') for item in data if item.get('type') == 4]

# Вывод отфильтрованного списка
print(filtered_data)
