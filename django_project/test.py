a = "!cd book-crawler && .venv/bin/python -m scrapy crawl {0} && ./books.sh create {0} && ./books.sh convert {0}\n# !cd book-crawler && ./books.sh create {0} && ./books.sh convert {0}"
b = ['yy', 'mtc', 'vt', 'tct', 'tfull', 'tcv', 'ttv']
for i in b:
    print(a.format(i))
