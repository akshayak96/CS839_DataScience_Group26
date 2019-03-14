
def comp_acc(testY, pred):

    pos = 0
    for i in range(0, len(testY)):
        if testY[i] == 1:
            pos += 1
    tp = 0
    fp = 0
    fn = 0
    count = 0
    for i in range(0, len(pred)):
        if pred[i] == 1:
            count += 1
            if testY[i] == 1:
                tp = tp + 1

    for j in range(0, len(pred)):
        if pred[i] == 1:
            if testY[i] == 0:
                fp = fp + 1

    for j in range(0, len(pred)):
        if pred[i] == 0:
            if testY[i] == 1:
                fn = fn + 1

    pres = tp / (fp + tp)
    print("Precision:")
    print(pres)

    recall = tp / count
    print("Recall:")
    print(recall)

    f1 = 2*(pres*recall)/(pres+recall)
    print("F1:")
    print(f1)
