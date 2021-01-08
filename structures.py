from collections import deque
from typing import TypeVar, Generic, Optional
from heapq import heappush, heappop

T = TypeVar('T')


class colourPalette():
    PINK = (251, 182, 209)
    PASTEL_BLUE = (154, 206, 223)
    PASTEL_PURPLE = (221, 212, 232)
    PASTEL_GREEN = (181, 225, 174)
    TURQUOISE = (134, 207, 190)
    YELLOW = (225, 237, 81)
    PINK1 = (253, 222, 238)
    PINK2 = (251, 182, 209)
    PINK3 = (249, 140, 182)
    BLUE1 = (204, 236, 239)
    BLUE2 = (154, 206, 223)
    BLUE3 = (111, 183, 214)
    BLUE4 = (117, 137, 191)
    GREEN = (133, 202, 93)
    BLACK = (0, 0, 0)
    DARK_GREY = (49, 51, 53)


class Node(Generic[T]):
    def __init__(self, state: T, parent, cost: float = 0.0,
                 heuristic: float = 0.0) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


class Queue(Generic[T]):
    def __init__(self) -> None:
        self._container = deque()

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.popleft()

    def __repr__(self) -> str:
        return repr(self._container)


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container = []

    @property
    def empty(self) -> bool:
        return not self._container

    def push(self, item: T) -> None:
        heappush(self._container, item)

    def pop(self) -> T:
        return heappop(self._container)

    def __repr__(self) -> str:
        return repr(self._container)
