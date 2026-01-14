# iris_ml_processor.py
import pandas as pd
import psycopg2
import psycopg2.extras
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sqlalchemy import create_engine
import os


def process_iris_data(**kwargs):
    """
    Process Iris dataset from PostgreSQL, train a model, and save results.
    This function is designed to be used with Airflow's PythonOperator.
    """
    # Get connection parameters from environment variables
    pg_host = os.getenv('POSTGRES_ANALYTICS_HOST', 'postgres_analytics')
    pg_port = os.getenv('POSTGRES_PORT', '5432')
    pg_db = os.getenv('ANALYTICS_DB', 'analytics')
    pg_user = os.getenv('ETL_USER', 'etl_user')
    pg_password = os.getenv('ETL_PASSWORD', '123321s')
    execution_date = kwargs.get('ds')

    # Create SQLAlchemy engine
    conn_string = f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"
    engine = create_engine(conn_string)

    # Query the processed Iris data
    if execution_date:
        query = f"SELECT * FROM homework.iris_processed WHERE execution_date = '{execution_date}'"
    else:
        query = "SELECT * FROM homework.iris_processed"

    df = pd.read_sql(query, engine)
    print(f"Loaded data: {df.shape[0]} rows, {df.shape[1]} columns")

    # Drop unnecessary columns
    df.drop(
        [
            'species',
            'is_species__setosa',
            'is_species__versicolor',
            'is_species__virginica',
            'is_species__',
            'execution_date',
        ],
        axis=1, inplace=True, errors='ignore'
    )

    X = df.drop(columns=['species_label_encoded'])
    y = df['species_label_encoded']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    print(f"Training set: {X_train.shape[0]} samples, Test set: {X_test.shape[0]} samples")

    # Train the initial model
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Get initial model performance
    train_score = clf.score(X_train, y_train)
    test_score = clf.score(X_test, y_test)
    print(f"Initial model - Training accuracy: {train_score:.4f}, Test accuracy: {test_score:.4f}")

    # Get feature importances - ВИПРАВЛЕНО: назви колонок у нижньому регістрі
    importances = clf.feature_importances_
    feature_names = X_train.columns
    feature_importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importances
    })

    # Select the top 5 features - ВИПРАВЛЕНО: звернення до колонок у нижньому регістрі
    top_features = feature_importance_df.sort_values(
        by='importance',
        ascending=False
    ).head(5)['feature'].tolist()

    print(f"Top 5 features: {', '.join(top_features)}")

    # Filter for top 5 features
    X_train_top5 = X_train[top_features]
    X_test_top5 = X_test[top_features]

    # Train model with top 5
    clf_top5 = RandomForestClassifier(n_estimators=100, random_state=42)
    clf_top5.fit(X_train_top5, y_train)

    train_score_top5 = clf_top5.score(X_train_top5, y_train)
    test_score_top5 = clf_top5.score(X_test_top5, y_test)
    print(f"Top 5 features model - Training accuracy: {train_score_top5:.4f}, Test accuracy: {test_score_top5:.4f}")

    # Prepare results
    results_df = pd.DataFrame({
        'model_type': ['full_model', 'top5_features_model'],
        'train_accuracy': [train_score, train_score_top5],
        'test_accuracy': [test_score, test_score_top5],
        'features_count': [X_train.shape[1], 5],
        'run_timestamp': [pd.Timestamp.now(), pd.Timestamp.now()]
    })

    feature_importance_df['run_timestamp'] = pd.Timestamp.now()

    # Save results to PostgreSQL
    with engine.connect() as connection:
        # ВИПРАВЛЕНО: if_exists='replace' автоматично виправить структуру таблиць

        # Save model metrics
        results_df.to_sql('iris_model_metrics', connection, schema='homework',
                          if_exists='replace', index=False)

        # Save feature importance
        feature_importance_df.to_sql('iris_feature_importance', connection, schema='homework',
                                     if_exists='replace', index=False)

    return {
        'top_features': top_features,
        'full_model_accuracy': test_score,
        'top5_model_accuracy': test_score_top5
    }


if __name__ == "__main__":
    process_iris_data()