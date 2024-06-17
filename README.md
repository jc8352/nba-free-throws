## NBA Free Throws

### Overview
This project aims to predict player free throw attempts based on the types of shots they attempt. Using these predictions, the project determines which players and teams take the most free throws above expected.

### Project Structure
```plain
nba-free-throws/
│
├── data/
│   └── result/
│       ├── fta_reg1/
│       │   ├── fta_pred_players.csv
│       │   └── fta_pred_teams.csv  
│       ├── fta_reg2/
│       │   ├── fta_pred_players.csv
│       │   └── fta_pred_teams.csv
│       ├── fta_reg/
│       │   ├── fta_pred_teams.csv
│       │   ├── ftr_pred_players.csv
│       │   └── ftr_pred_teams.csv
│       ├── 2022_players_complete.csv
│       ├── 2023_players_complete.csv
│       └── 2023_players_shooting.csv
│
├── graphics/
│   └── <charts and images>
|
├── json_to_csv/
│   ├── json_to_csv.py
│   ├── json_to_csv_22.py
│   └── <json files containing statistics>
│
├── src/
│   └── shots_fts_reg.py
```

### Files and Directories

- **data/result/fta_*/**
  - `fta_pred_players.csv`: CSV file containing the predicted free throw attempts for players.
  - `fta_pred_teams.csv`: CSV file containing the predicted free throw attempts for teams.

- **data/result/ftr_reg/**
  - `ftr_pred_players.csv`: CSV file containing the predicted free throw rates for players.
  - `ftr_pred_teams.csv`: CSV file containing the predicted free throw rates for teams.
  - `fta_pred_teams.csv`: CSV file containing the predicted free throw attempts for teams.

- **data/result/**
  - `2022_players_complete.csv`: Complete player data for the 2022 season (output from `json_to_csv_22.py`).
  - `2023_players_complete.csv`: Complete player data for the 2023 season (output from `json_to_csv.py`).

- **json_to_csv/**
  - `json_to_csv.py`: Script to convert JSON files to CSV format.
  - `json_to_csv_22.py`: Script to convert 2022 JSON files to CSV format.
  - `<other json files>`: JSON files used by the conversion scripts.

- **src/**
  - `shots_fts_reg.py`: Script for predicting free throw attempts based on shot types. This script:
    - Loads and preprocesses the shot data.
    - Implements three models:
      1. **Attempts from Inside 5 feet, Attempts from 20-24 feet, 3 Point Attempts, and Catch-and-Shoot Attempts vs Free Throw Rates**: Predicts free throw rates based on attempts from inside 5 feet, attempts from 20-24 feet, 3 point attempts, and catch-and-shoot attempts using a linear regression model. Outputs predictions to `data/result/fta_reg/ftr_pred_players.csv`, `data/result/fta_reg/fta_pred_teams.csv`, and `data/result/fta_reg/ftr_pred_teams.csv`.
      2. **Attempts from Inside 5 feet, Attempts From Drives, and Field Goal Attempts vs Free Throw Attempts**: Predicts free throw attempts based on attempts from inside 5 feet, attempts from drives, and field goal attempts using a linear regression model. Outputs predictions to `data/result/fta_reg1/fta_pred_players.csv` and `data/result/fta_reg1/fta_pred_teams.csv`.
      3. **Attempts from Inside 5 feet and Non-Catch-and-Shoot Attempts vs Free Throw Attempts**: Predicts free throw attempts based on non-catch-and-shoot attempts and attempts from inside 5 feet using a linear regression model. Outputs predictions to `data/result/fta_reg2/fta_pred_players.csv` and `data/result/fta_reg2/fta_pred_teams.csv`.

- **graphics/**
  - Contains charts and images generated during the analysis.

### Usage

1. **Data Conversion**:
   - Convert JSON files to CSV using the scripts in the `json_to_csv` directory.
   - Example:
     ```bash
     cd json_to_csv
     python3 json_to_csv.py
     python3 json_to_csv_22.py
     ```

2. **Free Throw Attempts Prediction**:
   - Run the prediction script to analyze and predict free throw attempts based on shot types.
   - Example:
     ```bash
     cd src
     python3 shots_fts_reg.py
     ```

3. **Analyze Results**:
   - The predicted results can be found in the directories in `data/result`.
   - Visualizations and charts are stored in the `graphics` directory for further analysis.
