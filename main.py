import torch
from data_loader import load_data
from sklearn.preprocessing import MinMaxScaler
from model import NeuralNet

#még nem mukodik

user_data = load_data("users.db")
user_data['Gender'] = user_data['Gender'].map({'Male': 1, 'Female': 0})

scalers = torch.load("scalers.pth")
scaler_X = scalers['scaler_X']
scaler_y = scalers['scaler_y']

X_user = scaler_X.transform(user_data)
X_user_tensor = torch.tensor(X_user, dtype=torch.float32)
input_size = X_user_tensor.shape[1]

hidden_size = 64
output_size = 2
model = NeuralNet(input_size, hidden_size, output_size)
model.load_state_dict(torch.load("model.pth"))
model.eval()

with torch.no_grad():
    prediction = model(X_user_tensor).numpy()
    prediction_original = scaler_y.inverse_transform(prediction)

distance, time_in_seconds = prediction_original[0]
time_in_minutes = time_in_seconds / 60
print(f"Becsült távolság: {distance:.2f} km")
print(f"Becsült idő: {time_in_minutes:.2f} perc")
