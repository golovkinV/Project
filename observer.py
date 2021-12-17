from abc import ABC, abstractmethod


# Наследник Engine
class ObservableEngine:
    def __init__(self):
        self.__subscribers = set()

    def subscribe(self, sub):
        self.__subscribers.add(sub)

    def unsubscribe(self, sub):
        self.__subscribers.remove(sub)

    def notify(self, value):
        for sub in self.__subscribers:
            sub.update(value)


class AbstractObserver(ABC):
    @abstractmethod
    def update(self, value):
        pass


class FullNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = list()

    def update(self, value):
        if value not in self.achievements:
            self.achievements.append(value)


class ShortNotificationPrinter(AbstractObserver):
    def __init__(self):
        self.achievements = set()

    def update(self, value):
        self.achievements.add(value["title"])
