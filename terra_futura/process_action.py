from .simple_types import Resource, GridPosition
from collections import Counter
from .interfaces import ProcessActionInterface, InterfaceCard, InterfaceGrid
from .card import Card

class ProcessAction():
    def activateCard(self, card: Card, grid: InterfaceGrid, 
                     inputs: list[tuple[Resource, GridPosition]], 
                     outputs: list[tuple[Resource, GridPosition]], 
                     pollution: list[GridPosition]) -> bool:
        """Checks whether the action is valid, and if so performs it."""

        if not card.is_active:
            return False

        #check pollution for each position
        counted_pollution = Counter(pollution)
        for position, count in counted_pollution.items():
            pollutionCard = grid.getCard(position)
            if not pollutionCard or not pollutionCard.can_place_pollution(count):
                return False

        #check inputs for each position
        inputs_grouped: dict[GridPosition, list[Resource]] = {}
        for resource, position in inputs:
            inputs_grouped.setdefault(position, []).append(resource)

        for position, resources in inputs_grouped.items():
            resourceCard = grid.getCard(position)
            if resourceCard is None or not resourceCard.canGetResources(resources):
                return False

        #check outputs for each position
        outputs_grouped: dict[GridPosition, list[Resource]] = {}
        for resource, position in outputs:
            outputs_grouped.setdefault(position, []).append(resource)
        if len(outputs_grouped) > 1:
            return False
        elif len(outputs_grouped) == 1:
            output_card_position = next(iter(outputs_grouped))
            outputs_resources = outputs_grouped[output_card_position]
            output_card: Card = grid.getCard(output_card_position)
            if output_card.state() != card.state() or not card.canPutResources(outputs_resources):
                return False

        inputs_resources: list[Resource] = [input[0] for input in inputs]
        outputs_resources: list[Resource] = [output[0] for output in outputs]

        if card.check(inputs_resources, outputs_resources, len(pollution)) or card.checkLower(inputs_resources, outputs_resources, len(pollution)):
            #perform action
            for position, count in counted_pollution.items():
                pollutionCard = grid.getCard(position)
                pollutionCard.place_pollution(count)
            for position, resources in inputs_grouped.items():
                resourceCard = grid.getCard(position)
                resourceCard.getResources(resources)
            for position, resources in outputs_grouped.items():
                resourceCard = grid.getCard(position)
                resourceCard.putResources(resources)
            return True

        return False
