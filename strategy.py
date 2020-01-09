from __future__ import annotations # отложенные аннотации типов (python 3.7+)
from abc import ABC, abstractmethod # абстракции для интерфейсов
from random import choice # Важнейшая вещь для нашей стратегии


class Context():
    """
    Интерфейс, для определения клиентов.
    """


    def __init__(self, strategy: Strategy) -> None:
        """
        Контекст будет принимать стратегию через конструктор.
        Измененять стратегию можно даже во время выполнения!
        Для этого напишем установщик свойства (сеттер).
        """

        self._strategy = strategy


    @property
    def strategy(self) -> Strategy:
        """
        Контекст хранит ссылку на объект Стратегии в свойстве.
        Изначально не зная конкретного класса стратегии, должен работать
        с любой Стратегией через ее интерфейс.
        """

        return self._strategy


    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        """
        Сеттер - дает возможность заменить объект Стратегии на другой
        в текущем Контексте.
        """

        self._strategy = strategy


    def _check_point(self, p):
        '''
        Внутренняя служебная функция.
        Будем проверять правильность координат
        '''
        l, n = p
        if l not in range(8): l = 0
        if n not in range(8): n = 0

        return (l, n)


    def do_move(self, p0: (int, int)) -> (int, int):
        """
        Реализация конкретной стратегии находится в объекте Стратегии.
        """
        letters = "ABCDEFGH"
        l, n = self._check_point(p0)

        print("Берем ферзя с {}{}".format(letters[l], n + 1), end=' ')
        l, n = self._strategy.apply(l, n)
        print(  "используя {} ставим на {}{}".format(
                self._strategy.name, letters[l], n + 1)
             )
        return (l, n)



class Strategy(ABC): # интерфейс стратегии
    """
    Интерфейс Стратегии объявляет общие операции, для всех поддерживаемых версий
    алгоритма. В Контексте этот интерфейс используется для вызова алгоритма,
    определённого Конкретными Стратегиями.
    """


    @abstractmethod
    def apply(self, l: int, n: int): # Создаем абстрактный метод алгоритма
        pass   # Тут можно ошибку поднимать если не реализовано



# Конкретные Стратегии.
# Реализуют алгоритмы по базовому интерфейсу Стратегии.
# Интерфейс Стратегий делает их взаимозаменяемыми в Контексте.
class SideStrategy(Strategy):

    name = "'ход к соседу'"
    moves = ((0, 1), (0, -1), (1, 0), (-1, 0))

    def apply(self, l: int, n: int) -> (int, int):
        possibles = []
        for dl, dn in self.moves:
            if (l + dl in range(8)) and (n + dn in range(8)):
                possibles.append( (l + dl, n + dn) )

        return choice(possibles) if possibles else (l, n)


class DiagStrategy(Strategy):

    name = "'ход вразрез'"
    moves = ((1, 1), (1,-1), (-1,-1), (-1, 1))

    def apply(self, l: int, n: int) -> (int, int):
        possibles = []
        for dl, dn in self.moves:
            if (l + dl in range(8)) and (n + dn in range(8)):
                possibles.append( (l + dl, n + dn) )

        return choice(possibles) if possibles else (l, n)


# Главная функция для демонстрации возможностей
def main():
    '''
    Клиентский код выбирает конкретную стратегию и передаёт её в контекст.
    Клиент должен знать о различиях между стратегиями, чтобы сделать
    правильный выбор. Но мы будем действовать смело - наугад!
    '''

    p = (0, 0) # Задаем стартовую точку
    # Припоминаем все знакомые стратегии
    strategies = [SideStrategy(), DiagStrategy()]
    context = Context(strategies[0]) # Создаем контекст

    for _ in range(10): # Рассчитываем на 10 ходов
        p = context.do_move(p)
        context.strategy = choice(strategies) # пытаемся сменить стратегию


if __name__ == "__main__": # На случай использования как модуля
    main()            # Запускаем функцию демонстрации
