from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from random import shuffle
from typing import Iterable, List


# =========================
# 1) Creational pattern: Builder
# =========================

@dataclass
class TourProgram:
    transport: str | None = None
    accommodation: str | None = None
    meals: str | None = None
    museums: List[str] = field(default_factory=list)
    exhibitions: List[str] = field(default_factory=list)
    excursions: List[str] = field(default_factory=list)
    total_cost: float = 0.0

    def __str__(self) -> str:
        return (
            "TourProgram("
            f"transport={self.transport}, "
            f"accommodation={self.accommodation}, "
            f"meals={self.meals}, "
            f"museums={self.museums}, "
            f"exhibitions={self.exhibitions}, "
            f"excursions={self.excursions}, "
            f"total_cost={self.total_cost:.2f})"
        )


class TourBuilder:
    def __init__(self) -> None:
        self._tour = TourProgram()

    def set_transport(self, name: str, cost: float) -> "TourBuilder":
        self._tour.transport = name
        self._tour.total_cost += cost
        return self

    def set_accommodation(self, name: str, cost: float) -> "TourBuilder":
        self._tour.accommodation = name
        self._tour.total_cost += cost
        return self

    def set_meals(self, name: str, cost: float) -> "TourBuilder":
        self._tour.meals = name
        self._tour.total_cost += cost
        return self

    def add_museum(self, name: str, cost: float) -> "TourBuilder":
        self._tour.museums.append(name)
        self._tour.total_cost += cost
        return self

    def add_exhibition(self, name: str, cost: float) -> "TourBuilder":
        self._tour.exhibitions.append(name)
        self._tour.total_cost += cost
        return self

    def add_excursion(self, name: str, cost: float) -> "TourBuilder":
        self._tour.excursions.append(name)
        self._tour.total_cost += cost
        return self

    def build(self) -> TourProgram:
        result = self._tour
        self._tour = TourProgram()
        return result


# =========================
# 2) Structural pattern: Composite
# =========================


class FileSystemNode(ABC):
    def __init__(self, name: str, created_at: datetime | None = None) -> None:
        self.name = name
        self.created_at = created_at or datetime.now()

    @property
    @abstractmethod
    def size(self) -> int:
        ...

    @abstractmethod
    def attributes(self) -> dict:
        ...


class File(FileSystemNode):
    def __init__(
        self,
        name: str,
        extension: str,
        size: int,
        created_at: datetime | None = None,
    ) -> None:
        super().__init__(name=name, created_at=created_at)
        self.extension = extension
        self._size = size

    @property
    def size(self) -> int:
        return self._size

    def attributes(self) -> dict:
        return {
            "type": "file",
            "name": self.name,
            "extension": self.extension,
            "size": self.size,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class Directory(FileSystemNode):
    def __init__(self, name: str, created_at: datetime | None = None) -> None:
        super().__init__(name=name, created_at=created_at)
        self._children: List[FileSystemNode] = []

    def add(self, node: FileSystemNode) -> None:
        self._children.append(node)

    def remove(self, node: FileSystemNode) -> None:
        self._children.remove(node)

    def children(self) -> Iterable[FileSystemNode]:
        return tuple(self._children)

    @property
    def size(self) -> int:
        return sum(child.size for child in self._children)

    def attributes(self) -> dict:
        return {
            "type": "directory",
            "name": self.name,
            "size": self.size,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "children_count": len(self._children),
        }


# =========================
# 3) Behavioral pattern: Iterator
#    Random-order traversal for output
# =========================


class RandomFsIterator:
    def __init__(self, root: Directory) -> None:
        self._nodes = self._collect_nodes(root)
        shuffle(self._nodes)
        self._index = 0

    def _collect_nodes(self, node: FileSystemNode) -> List[FileSystemNode]:
        collected = [node]
        if isinstance(node, Directory):
            for child in node.children():
                collected.extend(self._collect_nodes(child))
        return collected

    def __iter__(self) -> "RandomFsIterator":
        return self

    def __next__(self) -> FileSystemNode:
        if self._index >= len(self._nodes):
            raise StopIteration
        node = self._nodes[self._index]
        self._index += 1
        return node


def print_random_fs(root: Directory) -> None:
    print("\n=== Random file system output ===")
    for node in RandomFsIterator(root):
        attrs = node.attributes()
        attrs_line = ", ".join(f"{k}={v}" for k, v in attrs.items())
        print(attrs_line)


# =========================
# Demo scenario
# =========================


def demo_tour() -> None:
    builder = TourBuilder()
    tour = (
        builder
        .set_transport("Plane", 450.0)
        .set_accommodation("Hotel 4*", 700.0)
        .set_meals("Breakfast + Dinner", 220.0)
        .add_museum("National Art Museum", 30.0)
        .add_exhibition("Modern Tech Expo", 25.0)
        .add_excursion("Old Town Walking Tour", 40.0)
        .build()
    )

    print("=== Tourist bureau order ===")
    print(tour)


def demo_fs() -> Directory:
    root = Directory("root")
    docs = Directory("docs")
    media = Directory("media")

    root.add(docs)
    root.add(media)

    docs.add(File("report", "pdf", 320_000))
    docs.add(File("notes", "txt", 8_000))

    photos = Directory("photos")
    media.add(photos)
    media.add(File("song", "mp3", 4_500_000))

    photos.add(File("vacation1", "jpg", 1_200_000))
    photos.add(File("vacation2", "jpg", 1_350_000))

    return root


def main() -> None:
    demo_tour()
    fs_root = demo_fs()
    print_random_fs(fs_root)


if __name__ == "__main__":
    main()
