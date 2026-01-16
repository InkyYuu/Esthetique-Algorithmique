from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Optional, List


@dataclass
class Character:
    name: str
    age: Optional[int] = None
    description: Optional[str] = None
    photo: Optional[str] = None
    sprites: Optional[dict[str, str]] = None


TextType = Literal["dialogue", "thought", "testimony", "date"]


@dataclass
class Scene:
    background: Optional[str] = None
    character: Optional[Character] = None
    characterEmotion: Optional[str] = None
    extraElements: Optional[List[str]] = None
    characterText: Optional[str] = None
    textType: Optional[TextType] = None
    text: Optional[str] = None
    music: Optional[str] = None


NodeType = Literal["dialogue", "choice", "action", "testimony"]


@dataclass
class Option:
    text: str
    isCorrect: bool
    nextId: Optional[str] = None


@dataclass
class Node:
    id: str
    type: NodeType
    scene: Scene
    previousId: Optional[str] = None  # Only testimony nodes have this field
    nextId: Optional[str] = None
    options: Optional[List[Option]] = None
    specialAction: Optional[List[dict[str, tuple]]] = None


@dataclass
class Evidence:
    name: str
    description: str
    image: str

@dataclass
class CourtRecord:
    evidences: List[Evidence]
    profils: List[Character]
    
    
