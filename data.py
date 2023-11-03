import math


class Data:
    limit = 30
    currentPage = 10
    maxPage = 20
    count = 600

    def changeLimit(self, limit):
        self.limit = limit
        self.maxPage = math.ceil(self.count / self.limit)

    def loadData(self, start=0, limit=30):
        list = [
            [1, '123123132', '2022-11-22', '123123'],
            [1, '123123132', '2022-11-22', '123123'],
            [1, '123123132', '2022-11-22', '123123'],
            [1, '123123132', '2022-11-22', '123123'],
        ]
        count = 600
        if start <= 1:
            self.currentPage = start
            self.maxPage = math.ceil(count / limit)
        return {
            'list': list,
            'count': count
        }

    def prev(self):
        self.currentPage -= 1
        if self.currentPage < 1:
            self.currentPage = 1
        self.loadData(self.currentPage, self.limit)

    def next(self):
        self.currentPage += 1
        if self.currentPage > self.maxPage:
            self.currentPage = self.maxPage
        self.loadData(self.currentPage, self.limit)

    def page(self, page):
        self.currentPage = page
        self.loadData(self.currentPage, self.limit)

    def refresh(self):
        self.currentPage = 0
        self.limit = 20
        self.loadData(self.currentPage, self.limit)
