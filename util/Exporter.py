import pandas
from pandas import DataFrame

pandas.options.mode.chained_assignment = None


class Exporter:
    writer: pandas.ExcelWriter = None
    sheetDataFrame: DataFrame = {}
    sheetNameList: list = []
    sheetName: str = ''
    columns: dict = {}

    def __init__(self, filename, columns=[], sheetName='Sheet1', format={}):
        self.writer = pandas.ExcelWriter(filename + '.xlsx', engine='xlsxwriter')
        self.columns[sheetName] = columns
        self.sheetNameList.append(sheetName)
        self.sheetName = sheetName
        self.format = format

        dataFrame = pandas.DataFrame(columns=columns)
        dataFrame.set_index(self.columns[sheetName][0])
        self.sheetDataFrame[sheetName] = dataFrame


    def addSheet(self, sheetName='Sheet2', columns=[]):
        """
        新增sheet页
        :param sheetName:
        :param columns:
        :return:
        """
        if sheetName in self.sheetDataFrame:
            return True
        self.columns[sheetName] = columns
        self.sheetDataFrame[sheetName] = pandas.DataFrame(columns=columns)

    def changeSheet(self, sheetName='Sheet2'):
        """
        切换sheet
        :param sheetName:
        :return:
        """
        if sheetName in self.sheetDataFrame:
            self.sheetName = sheetName
            return True
        return False

    def append(self, data=[], sheetName='Sheet1', axis=0):
        row = {key: [] for key in self.columns}
        for idx, item in enumerate(data):
            for i, key in enumerate(self.columns):
                row[key].append(item[i])

        # 写入DataFrame
        if self.sheetDataFrame[sheetName].empty:
            self.sheetDataFrame[sheetName] = pandas.DataFrame(row, columns=self.columns[sheetName])
        else:
            self.sheetDataFrame[sheetName] = pandas.concat([pandas.DataFrame(row), self.sheetDataFrame[sheetName]],
                                                           axis=axis,
                                                           join='inner')

    def save(self, startrow=0):
        self.sheetDataFrame[self.sheetName].to_excel(
            self.writer,
            sheet_name=self.sheetName,
            index=False,
            startrow=startrow
        )
        return self.writer._save()