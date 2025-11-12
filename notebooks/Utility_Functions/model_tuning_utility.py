import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV, StratifiedKFold, RepeatedStratifiedKFold
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score, confusion_matrix, log_loss, make_scorer

# Unified hyperparameter tuning function for both Decision Tree and Random Forest models

def optimize_tree_model(model_type, n_splits, X_train, y_train, n_repeats=1, n_iter_search=50, scoring='auc'):
    """
    Performs hyperparameter tuning for Decision Tree ('DT') or Random Forest ('RF') 
    using RandomizedSearchCV.

    Args:
        model_type (str): 'DT' or 'RF'.
        n_splits (int): Number of folds for cross-validation.
        X_train (np.array/pd.DataFrame): Training features.
        y_train (np.array/pd.Series): Training targets.
        n_repeats (int): Number of times to repeat the K-Fold.
        n_iter_search (int): Number of parameter settings sampled.
        scoring (str): The metric to optimize ('auc' or 'balanced_accuracy').

    Returns:
        sklearn model: The best estimator found by the search.
    """
    
    # Define Model and Parameter Grid
    if model_type.upper() == 'DT':
        # Initialize a baseline Decision Tree model for tunining using GridSeachCV
        estimator = DecisionTreeClassifier(random_state=42)
        model_name = "Decision Tree"
        search_class = GridSearchCV     # Define the search class 

        param_space = {
            'max_depth': [3, 4, 5, 7, 10, 15, None], 
            'min_samples_split': [2, 5, 10, 15, 20, 25],
            'min_samples_leaf': [1, 2, 5, 7, 10, 20, 50],
            'criterion': ['gini', 'entropy'],
            'max_features': [None, 'sqrt', 'log2'],
            'ccp_alpha': np.linspace(0, 0.02, 30)           # Post pruning parameter
        }
        
    elif model_type.upper() == 'RF':
        # Initialize a baseline Random Forest model for tunining using RandomizedSearchCV to reduce computational time 
        estimator = RandomForestClassifier(random_state=42)
        model_name = "Random Forest"
        search_class = RandomizedSearchCV
        
        param_space = {
            'n_estimators': [100, 200, 400, 600], 
            'max_depth': [None, 10, 20, 40],        
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'criterion': ['gini', 'entropy','log_loss' ],
            'max_features': ['sqrt', 'log2', 0.7],
            'bootstrap': [True, False]
        }
    else:
        # Output error message for an invalid model type
        raise ValueError("Invalid model_type. Use 'DT' or 'RF'.")

    # Define Scoring Metric
    if scoring.lower() == 'auc':
        scorer = 'roc_auc'
        score_name = "AUC Score"
    elif scoring.lower() == 'balanced_accuracy':
        scorer = 'balanced_accuracy'
        score_name = "Balanced Accuracy"
    else:
        raise ValueError("Invalid scoring metric. Use 'auc' or 'balanced_accuracy'.")


    # Define Cross-Validation Strategy
    if n_repeats > 1:
        cv_strategy = RepeatedStratifiedKFold(n_splits=n_splits, n_repeats=n_repeats, random_state=42)
        cv_type = f"Repeated Stratified KFold (K={n_splits}, R={n_repeats})"
    else:
        cv_strategy = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
        cv_type = f"Stratified KFold (K={n_splits})"

    # Dynamically assign param_grid or param_distributions based on the chosen search class
    search_params = {
        'estimator': estimator,
        'scoring': scorer,
        'cv': cv_strategy,
        'verbose': 1,
        'n_jobs': -1
    }

    if search_class == GridSearchCV:
        search_params['param_grid'] = param_space
        search_description = "Grid Search"
    else: # search_class == RandomizedSearchCV
        search_params['param_distributions'] = param_space
        # n_iter controls the number of different hyperparameter combinations the model will train and evaluate 
        search_params['n_iter'] = n_iter_search           
        search_description = f"Randomized Search (n_iter={n_iter_search})"
        # Include random_state only for RandomizedSearchCV
        search_params['random_state'] = 42
    
    # Dynamically initialize the search object (GridSearchCV or RandomizedSearchCV)
    # The '**' operator unpacks the key-value pairs from the 'search_params' dictionary
    # and passes them as keyword arguments to the class constructor.
    search_obj = search_class(**search_params)

    print(f"\nStarting Hyperparameter Search for {model_name} with {n_splits*n_repeats} evaluations...")
    print(f"Search Method: {search_description}")
    print(f"CV Strategy: {cv_type}")
    print(f"Optimizing for: {score_name}")
    
    search_obj.fit(X_train, y_train)
    print(f"Grid Search with {n_splits*n_repeats} evaluations complete.")

    # Report and return the optimized model
    print(f"\n{model_name} Results")
    print(f"Best {score_name} found: {search_obj.best_score_:.4f}")
    
    return search_obj.best_estimator_