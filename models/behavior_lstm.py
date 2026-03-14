import torch
import torch.nn as nn
from utils.logger import get_logger

logger = get_logger()

class BehaviorLSTM(nn.Module):
    """
    Long Short-Term Memory model for long-term trajectory forecasting.
    Input: [batch, seq_len, 2] (Lat/Long or Pixel X/Y)
    Output: [batch, 2] (Next predicted position)
    """
    def __init__(self, input_size=2, hidden_size=64, num_layers=2):
        super(BehaviorLSTM, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 2)
        logger.info(f"BehaviorLSTM initialized (hidden={hidden_size}, layers={num_layers})")

    def forward(self, x):
        # x shape: (batch, seq, 2)
        h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size).to(x.device)
        
        out, _ = self.lstm(x, (h0, c0))
        # Take the last time step output
        out = self.fc(out[:, -1, :])
        return out

class TrajectoryForecaster:
    """
    Wrapper for LSTM trajectory forecasting.
    """
    def __init__(self, model_path=None):
        self.model = BehaviorLSTM()
        if model_path:
            try:
                self.model.load_state_dict(torch.load(model_path))
                logger.info(f"Loaded LSTM weights from {model_path}")
            except Exception as e:
                logger.error(f"Failed to load LSTM model: {e}")
        self.model.eval()

    def predict_multi_step(self, trajectory, steps=10):
        """
        Trajectory: List of tuples (x, y)
        steps: Number of future points to predict.
        """
        if len(trajectory) < 5:
            return []

        # Convert to tensor [1, seq, 2]
        input_data = torch.tensor(trajectory, dtype=torch.float32).unsqueeze(0)
        
        predictions = []
        current_input = input_data
        
        with torch.no_grad():
            for _ in range(steps):
                pred = self.model(current_input)
                predictions.append(pred.squeeze().tolist())
                # Update input by sliding window (replace last or append)
                # For simplicity in this mock-integration:
                current_input = torch.cat((current_input[:, 1:, :], pred.unsqueeze(1)), dim=1)
                
        return predictions
