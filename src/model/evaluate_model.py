def evaluate_model(model, test_x, test_y):
    test_loss, test_mae = model.evaluate(test_x, test_y, verbose=0)

    return test_loss, test_mae
