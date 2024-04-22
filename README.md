Парсинг из сайта market.grsu.by:

Работает код только для одной ссылки, она меняется в main'е. Преобразовывает данные в csv, а после в json

Добавлена папка testcommerce.

На сайте можно:
- добавлять предмет
- обновлять предмет
- удалять предмет

Немного помучался со стилем.


Сортировка имени в возрастающем порядке: http://localhost:8000/items/?sort_by=name&order_by=asc
Сортировка имени в убывающем порядке: http://localhost:8000/items/?sort_by=name&order_by=desc
Сортировка цены в возрастающем порядке: http://localhost:8000/items/?sort_by=price&order_by=asc
Сортировка цены в убывающем порядке: http://localhost:8000/items/?sort_by=price&order_by=desc

