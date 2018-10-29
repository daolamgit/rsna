# Load converted model
import sys
import glob
import os
import pandas as pd
import numpy as np
import pydicom
from scipy.ndimage.interpolation import zoom

DATA_DIR = "/home/radonc/Projects/kg/rsna/Data/input_png/"
ROOT_DIR = "/home/radonc/Projects/kg/rsna/Data/working/"

train_pngs_dir = os.path.join(DATA_DIR, "stage_1_train_images")
test_dicoms_dir = os.path.join(DATA_DIR, "stage_1_test_images/")

sys.path.append( 'keras-retinanet')  # To find local version of the library
from keras_retinanet.models import load_model


retinanet = load_model(os.path.join(ROOT_DIR, "converted_model_50_512_44.h5"),
                       backbone_name="resnet50")


# Preprocessing function
def preprocess_input(x):
    x = x.astype("float32")
    x[..., 0] -= 103.939
    x[..., 1] -= 116.779
    x[..., 2] -= 123.680
    return x


test_dicoms = glob.glob(os.path.join(test_dicoms_dir, "*.dcm"))
test_patient_ids = [_.split("/")[-1].split(".")[0] for _ in test_dicoms]
test_predictions = []
for i, dcm_file in enumerate(test_dicoms):
    sys.stdout.write("Predicting images: {}/{} ...\r".format(i + 1, len(test_dicoms)))
    sys.stdout.flush()
    # Load DICOM and extract pixel array
    dcm = pydicom.read_file(dcm_file)
    arr = dcm.pixel_array
    # Make 3-channel image
    img = np.zeros((arr.shape[0], arr.shape[1], 3))
    for channel in range(img.shape[-1]):
        img[..., channel] = arr
        # Resize
    # Change image size if necessary!
    scale_factor = 256. / img.shape[0]
    img = zoom(img, [scale_factor, scale_factor, 1], order=1, prefilter=False)
    # Preprocess with ImageNet mean subtraction
    img = preprocess_input(img)
    prediction = retinanet.predict_on_batch(np.expand_dims(img, axis=0))
    test_predictions.append(prediction)

# Extract predictions
test_pred_df = pd.DataFrame()
for i, pred in enumerate(test_predictions):
    # Take top 5
    # Should already be sorted in descending order by score
    bboxes = pred[0][0][:5]
    scores = pred[1][0][:5]
    # -1 will be predicted if nothing is detected
    detected = scores > -1
    if np.sum(detected) == 0:
        continue
    else:
        bboxes = bboxes[detected]
        bboxes = [box / scale_factor for box in bboxes]
        scores = scores[detected]
    individual_pred_df = pd.DataFrame()
    for j, each_box in enumerate(bboxes):
        # RetinaNet output is [x1, y1, x2, y2]
        tmp_df = pd.DataFrame({"patientId": [test_patient_ids[i]],
                               "x": [each_box[0]],
                               "y": [each_box[1]],
                               "w": [each_box[2] - each_box[0]],
                               "h": [each_box[3] - each_box[1]],
                               "score": [scores[j]]})
        individual_pred_df = individual_pred_df.append(tmp_df)
    test_pred_df = test_pred_df.append(individual_pred_df)

test_pred_df.head()

# Generate submission

# Set box threshold for inclusion
threshold = 0.35

list_of_pids = []
list_of_preds = []
for pid in np.unique(test_pred_df.patientId):
    tmp_df = test_pred_df[test_pred_df.patientId == pid]
    tmp_df = tmp_df[tmp_df.score >= threshold]
    # Skip if empty
    if len(tmp_df) == 0:
        continue
    predictionString = " ".join(
        ["{} {} {} {} {}".format(row.score, row.x, row.y, row.w, row.h) for rownum, row in tmp_df.iterrows()])
    list_of_preds.append(predictionString)
    list_of_pids.append(pid)

positives = pd.DataFrame({"patientId": list_of_pids,
                          "PredictionString": list_of_preds})

negatives = pd.DataFrame({"patientId": list(set(test_patient_ids) - set(list_of_pids)),
                          "PredictionString": [""] * (len(test_patient_ids) - len(list_of_pids))})

submission = positives.append(negatives)

submission.to_csv(os.path.join(ROOT_DIR, 'submission_ret50_512_44.csv'), columns=['patientId', 'PredictionString'], index=False)
