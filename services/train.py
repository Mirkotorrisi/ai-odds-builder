import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Flatten, Concatenate, Dense
from tensorflow.keras.optimizers import Adam

df = pd.read_csv("csv/passiveEvents.csv")

target_cols = [
    "outcome1", "outcomeX", "outcome2",
    "outcomeOver", "outcomeUnder",
    "outcomeGG", "outcomeNG"
]

all_teams = pd.concat([df["homeName"], df["awayName"]]).unique()

team_id_map = {name.strip(): idx for idx, name in enumerate(sorted(all_teams))}


df['homeId'] = df['homeName'].map(team_id_map)
df['awayId'] = df['awayName'].map(team_id_map)

df.to_csv("csv/dataset_with_ids.csv", index=False)

num_teams = len(team_id_map)


X_home = df["homeId"].values
X_away = df["awayId"].values
y = df[target_cols].values

scaler = MinMaxScaler()
y_scaled = scaler.fit_transform(y)

X_home_train, X_home_test, X_away_train, X_away_test, y_train, y_test = train_test_split(
    X_home, X_away, y_scaled, test_size=0.2, random_state=42
)

embedding_dim = 16

home_input = Input(shape=(1,), name="home_input")
away_input = Input(shape=(1,), name="away_input")

home_emb = Embedding(input_dim=num_teams, output_dim=embedding_dim)(home_input)
away_emb = Embedding(input_dim=num_teams, output_dim=embedding_dim)(away_input)

home_vec = Flatten()(home_emb)
away_vec = Flatten()(away_emb)
x = Concatenate()([home_vec, away_vec])

x = Dense(64, activation="relu")(x)
x = Dense(64, activation="relu")(x)
output = Dense(len(target_cols), activation="linear")(x)

model = Model(inputs=[home_input, away_input], outputs=output)
model.compile(optimizer=Adam(0.001), loss="mse", metrics=["mae"])

model.fit(
    [X_home_train, X_away_train], y_train,
    validation_data=([X_home_test, X_away_test], y_test),
    epochs=20, batch_size=64
)

loss, mae = model.evaluate([X_home_test, X_away_test], y_test)
print(f"\nTest MAE: {mae:.4f}")

model.save("assets/odds_embed_model.keras")
import joblib
joblib.dump(scaler, "assets/odds_scaler.joblib")
joblib.dump(team_id_map, "assets/team_id_map.joblib")
