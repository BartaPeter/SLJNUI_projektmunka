import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

def preprocess_data(data):
    for col in data.columns:
        if data[col].dtype == 'object':
            data[col] = data[col].str.replace(',', '.')
            data[col] = pd.to_numeric(data[col], errors='coerce')
    data = data[(data['Distance'] > 0) & (data['Time'] > 0)]
    
    if data.empty:
        raise ValueError("A tisztítás után az adathalmaz üres. Ellenőrizd az adatokat!")
    if 'Gender' in data.columns:
        data['Gender'] = data['Gender'].map({'Male': 1, 'Female': 0})

    X = data.drop(columns=["Distance", "Time"])
    y = data[["Distance", "Time"]]

    scaler_X = MinMaxScaler()
    scaler_y = MinMaxScaler()

    X_scaled = scaler_X.fit_transform(X)
    y_scaled = scaler_y.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test, scaler_X, scaler_y

