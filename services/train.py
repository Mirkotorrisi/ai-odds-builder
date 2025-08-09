import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, Flatten, Concatenate, Dense
from tensorflow.keras.optimizers import Adam
import joblib

# === CARICA E PREPARA IL DATASET ===
df = pd.read_csv("csv/passiveEvents.csv")

# Mappatura squadre in ID
all_teams = pd.concat([df["homeName"], df["awayName"]]).unique()
team_id_map = {name.strip(): idx for idx, name in enumerate(sorted(all_teams))}

df['homeId'] = df['homeName'].map(team_id_map)
df['awayId'] = df['awayName'].map(team_id_map)

num_teams = len(team_id_map)

# Funzione per creare e allenare un modello
def train_market_model(market_name, target_cols, save_prefix):
    print(f"\n=== Training modello: {market_name} ===")

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
    print(f"{market_name} - Test MAE: {mae:.4f}")

    model.save(f"assets/{save_prefix}_model.keras")
    joblib.dump(scaler, f"assets/{save_prefix}_scaler.joblib")

# === ALLENAMENTO DEI TRE MODELLI ===
train_market_model("1X2", ["outcome1", "outcomeX", "outcome2"], "market_1X2")
train_market_model("Over/Under", ["outcomeOver", "outcomeUnder"], "market_OU")
train_market_model("Goal/NoGoal", ["outcomeGG", "outcomeNG"], "market_BTTS")

# Salviamo anche la mappa squadre
joblib.dump(team_id_map, "assets/team_id_map.joblib")
