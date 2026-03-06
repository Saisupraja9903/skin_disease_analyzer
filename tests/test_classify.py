import numpy as np
from PIL import Image

from ml.classify import ensemble_classify, classes


def test_ensemble_returns_eight():
    # create a dummy white image
    img = Image.new("RGB", (224, 224), color="white")
    preds = ensemble_classify(img)
    assert isinstance(preds, list)
    assert len(preds) == 8
    for name, score in preds:
        assert name in classes
        assert 0.0 <= score <= 1.0
