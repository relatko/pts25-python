from dataclasses import dataclass, field
from typing import List
from terra_futura.interfaces import Effect, Resource

# Assuming you already have:
# class Resource: ...
# class Effect(ABC):
#     @abstractmethod
#     def check(self, input: List[Resource], output: List[Resource], pollution: int) -> bool: ...
#     @abstractmethod
#     def hasAssistance(self) -> bool: ...
#     @abstractmethod
#     def state(self) -> str: ...


@dataclass
class EffectOr(Effect):
    """
    Composite effect: succeeds if ANY child effect would succeed for the same
    (input, output, pollution) triple.

    In other words:
        check(...) == True  iff  exists e in effects: e.check(...)

    This matches a card effect where you have multiple possible options and
    you are allowed to pick *one* of them.

    Example: 'Pay 1 wood → Gain 1 product' OR 'Pay 2 any → Gain 2 money'.
    """

    effects: List[Effect] = field(default_factory=list)

    def check(self, input: List[Resource], output: List[Resource], pollution: int) -> bool:
        """
        Returns True if at least one of the contained effects would accept
        this input/output/pollution combination.
        """
        # If there are no children, this OR can never succeed
        if not self.effects:
            return False

        return any(
            effect.check(input, output, pollution)
            for effect in self.effects
        )

    def hasAssistance(self) -> bool:
        """
        This OR has assistance if ANY of its children has assistance.
        """
        return any(effect.hasAssistance() for effect in self.effects)

    def state(self) -> str:
        """
        Human-readable description combining all children with ' OR '.
        """
        if not self.effects:
            return "(empty OR)"

        inner = " OR ".join(effect.state() for effect in self.effects)
        return f"({inner})"
