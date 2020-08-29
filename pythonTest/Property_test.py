class score():
    def __init__(self, default=0):
        self._score = default

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError('Score must be interger')
        if not 0<= value <= 100:
            raise ValueError('Valid value must be in [1-100]')

        self._score = value

    def __get__(self, instance, owner):
        return self._score

    def __delete__(self, instance):
        del self._score

class student():
    math = score(0)
    chinese = score(0)
    english = score(0)

    def __init__(self, name, math, chinese, english):
        self.name = name
        self.math = math
        self.chinese = chinese
        self.english = english

    def __repr__(self):
        return "<Student: {}, math: {}, chinese: {}, english:{}>".format(
            self.name, self.math, self.chinese, self.english
        )

student_x = student('xiaoming', 10, 100, 80)
student_x # 输出__repr__函数中的返回的字符串内容
print(student_x) #显式打印__str__中返回的字符串内容

