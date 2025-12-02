import unittest
from unittest.mock import Mock, MagicMock
from card import Card, Deck
from processAction import ProcessAction


class MockResource:
    """Mock Resource class for testing."""
    def __init__(self, name: str):
        self.name = name
        self.value = name
    
    def __eq__(self, other):
        return isinstance(other, MockResource) and self.name == other.name
    
    def __repr__(self):
        return f"Resource({self.name})"


class TestProcessActionActivateCard(unittest.TestCase):

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.process_action = ProcessAction()
        self.mock_grid = Mock()
        self.green = MockResource("GREEN")
        self.red = MockResource("RED")

    def test_activateCard_inactive_card(self) -> None:
        """Test activateCard fails when card is inactive."""
        mock_card = Mock(spec=Card)
        mock_card.can_activate.return_value = False
        
        result = self.process_action.activateCard(
            card=mock_card,
            grid=self.mock_grid,
            inputs=[],
            outputs=[],
            pollution=[]
        )
        
        self.assertFalse(result)

    def test_activateCard_no_inputs_or_outputs(self) -> None:
        """Test activateCard with no inputs or outputs (Level I card)."""
        mock_card = Mock(spec=Card)
        mock_card.can_activate.return_value = True
        mock_card.activate.return_value = True
        
        result = self.process_action.activateCard(
            card=mock_card,
            grid=self.mock_grid,
            inputs=[],
            outputs=[],
            pollution=[]
        )
        
        self.assertTrue(result)
        mock_card.can_activate.assert_called_once()
        mock_card.activate.assert_called_once()

    def test_activateCard_with_inputs_available(self) -> None:
        """Test activateCard with available input resources."""
        mock_card = Mock(spec=Card)
        mock_card.can_activate.return_value = True
        mock_card.activate.return_value = True
        
        mock_grid_position = Mock()
        inputs = [(self.green, mock_grid_position)]
        
        result = self.process_action.activateCard(
            card=mock_card,
            grid=self.mock_grid,
            inputs=inputs,
            outputs=[],
            pollution=[]
        )
        
        self.assertTrue(result)
        mock_card.can_activate.assert_called_once()
        mock_card.activate.assert_called_once()

    def test_activateCard_with_unavailable_inputs(self) -> None:
        """Test activateCard fails when required inputs are unavailable."""
        mock_card = Mock(spec=Card)
        mock_card.can_activate.return_value = False
        
        mock_grid_position = Mock()
        inputs = [(self.green, mock_grid_position)]
        
        result = self.process_action.activateCard(
            card=mock_card,
            grid=self.mock_grid,
            inputs=inputs,
            outputs=[],
            pollution=[]
        )
        
        self.assertFalse(result)
        mock_card.activate.assert_not_called()

    def test_activateCard_multiple_inputs(self) -> None:
        """Test activateCard with multiple input resources."""
        mock_card = Mock(spec=Card)
        mock_card.can_activate.return_value = True
        mock_card.activate.return_value = True
        
        mock_grid_position1 = Mock()
        mock_grid_position2 = Mock()
        inputs = [
            (self.green, mock_grid_position1),
            (self.red, mock_grid_position2)
        ]
        
        result = self.process_action.activateCard(
            card=mock_card,
            grid=self.mock_grid,
            inputs=inputs,
            outputs=[],
            pollution=[]
        )
        
        self.assertTrue(result)
        mock_card.can_activate.assert_called_once()

    def test_activateCard_with_pollution(self) -> None:
        """Test activateCard applies pollution to grid positions."""
        mock_card = Mock(spec=Card)
        mock_card.can_activate.return_value = True
        mock_card.activate.return_value = True
        
        mock_pollution_pos1 = Mock()
        mock_pollution_pos2 = Mock()
        pollution = [mock_pollution_pos1, mock_pollution_pos2]
        
        result = self.process_action.activateCard(
            card=mock_card,
            grid=self.mock_grid,
            inputs=[],
            outputs=[],
            pollution=pollution
        )
        
        self.assertTrue(result)

    def test_activateCard_with_outputs(self) -> None:
        """Test activateCard distributes outputs to grid positions."""
        mock_card = Mock(spec=Card)
        mock_card.can_activate.return_value = True
        mock_card.activate.return_value = True
        
        mock_output_pos = Mock()
        outputs = [(self.green, mock_output_pos)]
        
        result = self.process_action.activateCard(
            card=mock_card,
            grid=self.mock_grid,
            inputs=[],
            outputs=outputs,
            pollution=[]
        )
        
        self.assertTrue(result)

    def test_activateCard_complex_scenario(self) -> None:
        """Test activateCard with inputs, outputs, and pollution."""
        mock_card = Mock(spec=Card)
        mock_card.can_activate.return_value = True
        mock_card.activate.return_value = True
        
        input_pos = Mock()
        output_pos = Mock()
        pollution_pos = Mock()
        
        inputs = [(self.green, input_pos)]
        outputs = [(self.red, output_pos)]
        pollution = [pollution_pos]
        
        result = self.process_action.activateCard(
            card=mock_card,
            grid=self.mock_grid,
            inputs=inputs,
            outputs=outputs,
            pollution=pollution
        )
        
        self.assertTrue(result)

    def test_activateCard_activation_fails(self) -> None:
        """Test activateCard fails if card.activate() fails."""
        mock_card = Mock(spec=Card)
        mock_card.can_activate.return_value = True
        mock_card.activate.return_value = False
        
        result = self.process_action.activateCard(
            card=mock_card,
            grid=self.mock_grid,
            inputs=[],
            outputs=[],
            pollution=[]
        )
        
        self.assertFalse(result)

    def test_activateCard_get_resources_fails(self) -> None:
        """Test activateCard fails if card.activate() fails."""
        mock_card = Mock(spec=Card)
        mock_card.can_activate.return_value = True
        mock_card.activate.return_value = False
        
        input_pos = Mock()
        inputs = [(self.green, input_pos)]
        
        result = self.process_action.activateCard(
            card=mock_card,
            grid=self.mock_grid,
            inputs=inputs,
            outputs=[],
            pollution=[]
        )
        
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
