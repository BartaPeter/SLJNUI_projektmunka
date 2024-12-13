import torch
import torch.nn as nn
from data_loader import load_data
from preprocessing import preprocess_data
from model import NeuralNet

#még nem mukodik!
data = load_data("running_data.db")

X_train, X_test, y_train, y_test, scaler_X, scaler_y = preprocess_data(data)
X_train_tensor = torch.tensor(X_train, dtype=torch.float32)
y_train_tensor = torch.tensor(y_train, dtype=torch.float32)

input_size = X_train_tensor.shape[1]
hidden_size = 64
output_size = y_train_tensor.shape[1]
model = NeuralNet(input_size, hidden_size, output_size)

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
epochs = 100

for epoch in range(epochs):
    optimizer.zero_grad()
    outputs = model(X_train_tensor)
    loss = criterion(outputs, y_train_tensor)


    loss.backward()
    optimizer.step()

    if (epoch + 1) % 10 == 0:
        print(f"Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.4f}")
torch.save(model.state_dict(), "model.pth")
torch.save({"scaler_X": scaler_X, "scaler_y": scaler_y}, "scalers.pth")
