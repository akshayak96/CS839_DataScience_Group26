
def comp_acc(testY, pred):
    t = 0
    for i in range(0, len(testY)):
        if testY[i] == 1:
            t += 1
    tp = 0
    count1 = 0
    for i in range(0, len(pred)):
        if pred[i] == 1:
            count1 += 1
            if testY[i] == 1:
                tp = tp + 1

    pres = tp / t
    print("Precision:")
    print(pres)

    recall = tp / count1
    print("Recall:")
    print(recall)

    f1 = 2*(pres*recall)/(pres+recall)
    print("F1:")
    print(f1)
