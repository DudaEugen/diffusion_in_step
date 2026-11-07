from enum import Enum

class SubstanceName(Enum):
    ALUMINIUM = 'aluminium'
    COPPER = 'copper'

    def __str__(self) -> str:
        return self.value