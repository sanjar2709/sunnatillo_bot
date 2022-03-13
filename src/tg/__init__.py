class MediaType:
    TEXT = 1
    PHOTO = 2
    VIDEO = 3

    CHOICES = [
        (TEXT, "Text"),
        (PHOTO, "Photo"),
        (VIDEO, "Video"),
    ]

    @classmethod
    def getValue(self, index):
        result = '-'
        for i, name in self.CHOICES:
            if i == index:
                result = name
        return result

class MessagePlase:
    start = 1
    our = 2
    the_end = 3

    CHOICES = [
        (start, "Start Komandasida"),
        (our, "Biz haqimizda"),
        (the_end, "Test yakunlanganda"),
    ]

    @classmethod
    def getValue(self, index):
        result = '-'
        for i, name in self.CHOICES:
            if i == index:
                result = name
        return result

class UsersStatus:
    simple_user = 1
    answer_user = 2
    no_active = 3
    active = 4

    CHOICES = [
        (simple_user, "Botga start bosgan"),
        (answer_user, "Savollarga javob bergan"),
        (no_active, "Moderatsiyadan o'tmadi"),
        (active, "Moderatsiyadan o'tdi"),
    ]

    @classmethod
    def getValue(self, index):
        result = '-'
        for i, name in self.CHOICES:
            if i == index:
                result = name
        return result

class QuestionType:
    text = 1
    select = 2

    CHOICES = [
        (text, "Text"),
        (select, "Select"),
    ]

    @classmethod
    def getValue(self, index):
        result = '-'
        for i, name in self.CHOICES:
            if i == index:
                result = name
        return result