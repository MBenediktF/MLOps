def evaluate_model(model, x_test, y_test):
    # Modell evaluieren
    test_loss, test_acc = model.evaluate(x_test, y_test, verbose=2)
    print('\nTest accuracy:', test_acc)
