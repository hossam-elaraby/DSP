from dataclasses import dataclass, field
from typing import Callable, List, Optional, Any


@dataclass
class AlgorithmParam:
    name: str
    label: str
    param_type: str
    default_value: Any
    options: List[str] = field(default_factory=list)
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    step: Optional[float] = None


@dataclass
class DSPAlgorithm:
    name: str
    category: str
    run_func: Callable
    params: List[AlgorithmParam] = field(default_factory=list)
    description: str = ""
