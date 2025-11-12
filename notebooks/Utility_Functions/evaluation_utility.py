from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report, roc_auc_score, accuracy_score, confusion_matrix, log_loss, make_scorer

# Define an evaluation function that takes a specified model and test data as inputs, 
# uses the model to predict Gallstone Status and outputs evaluation metrics of the model.
 
def evaluate_model(model, X_valid, y_valid, model_name="Model"):
    # Get Gallstone Status predictions (0 or 1)
    y_pred = model.predict(X_valid)

    # Get prediction probabilities for Gallstone Status = 1, 
    # used for AUC score (metric used to measure binary classification perfomance)
    y_prob = model.predict_proba(X_valid)[:, 1]

    # Decision Tree Model - Results Report
    # Base Metrics
    accuracy = accuracy_score(y_valid, y_pred)
    auc_score = roc_auc_score(y_valid, y_prob)

    # Additional Metrics
    # Log Loss requires the prediction probabilities for ALL classes, which predict_proba returns
    y_proba_all = model.predict_proba(X_valid)
    logloss = log_loss(y_valid, y_proba_all)

    # Confusion Matrix and Specificity (requires the raw matrix)
    cm = confusion_matrix(y_valid, y_pred)

    # The matrix elements:
    # cm[0, 0] = True Negatives (TN)
    # cm[0, 1] = False Positives (FP)
    # cm[1, 0] = False Negatives (FN)
    # cm[1, 1] = True Positives (TP)

    TN = cm[0, 0]
    FP = cm[0, 1]

    # Specificity (True Negative Rate) = TN / (TN + FP)
    # Measures how well the model identifies true negative cases (Status 0)
    specificity = TN / (TN + FP) if (TN + FP) > 0 else 0

    # Report
    # Print best Hyperparameters for the trained model
    print(f"\n{model_name} Hyperparameters")

    key_params_list = ['max_depth', 'min_samples_leaf', 'min_samples_split', 'criterion', 'max_features', 'n_estimators']

    all_params = model.get_params()

    for param in key_params_list:
        # Check if the parameter exists before printing
        if param in all_params:
            value = all_params[param]
            print(f"  {param}: {value}")


    # Print performance of the trained model
    print(f"\n{model_name} Performance")

    target_names = ['No Gallstone', 'Gallstone']

    # 1. Classification Report (Precision, Recall, F1-Score)
    print("Classification Report:\n", classification_report(y_valid, y_pred, target_names=target_names))

    # 2. Key Summary Metrics
    print(f"Accuracy: {100*accuracy:.2f}%")
    print(f"AUC Score: {100*auc_score:.2f}%")
    print(f"Log Loss (Calibration): {logloss:.4f}")
    print(f"Specificity (True Negative Rate): {100*specificity:.2f}%")

    # 3. Confusion Matrix (Raw Counts)
    print("\nConfusion Matrix (Raw Counts):")
    print(f"   Predicted 0  |  Predicted 1")
    print(f"Actual 0:  {cm[0, 0]:<4} |  {cm[0, 1]}")
    print(f"Actual 1:  {cm[1, 0]:<4} |  {cm[1, 1]}")
  