#SOURCE: https://www.kaggle.com/grfiv4/plot-a-confusion-matrix

import numpy as np
import matplotlib.pyplot as plt
import itertools

from numpy.core.fromnumeric import size


def plot_confusion_matrix(cm,
                          target_names,
                          title='Confusion matrix',
                          cmap=None,
                          normalize=True):
    """
    Sourced from
    http://scikit-learn.org/stable/auto_examples/model_selection/plot_confusion_matrix.html

    """

    accuracy = np.trace(cm) / float(np.sum(cm))
    misclass = 1 - accuracy

    if cmap is None:
        cmap = plt.get_cmap('Blues')

    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title, fontdict= {'size':'15'})
    plt.colorbar()

    if target_names is not None:
        tick_marks = np.arange(len(target_names))
        plt.xticks(tick_marks, target_names, rotation=45, size = 15)
        plt.yticks(tick_marks, target_names,size = 15)

    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]


    thresh = cm.max() / 1.5 if normalize else cm.max() / 2
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        if normalize:
            plt.text(j, i, "{:0.4f}".format(cm[i, j]),
                     horizontalalignment="center", fontsize=18,
                     color="white" if cm[i, j] > thresh else "black")
        else:
            plt.text(j, i, "{:,}".format(cm[i, j]),
                     horizontalalignment="center", fontsize=16,
                     color="white" if cm[i, j] > thresh else "black")


    plt.tight_layout()
    plt.ylabel('True label', fontdict= {'size':'16'} )
    plt.xlabel('Predicted label\naccuracy={:0.4f}; misclass={:0.4f}'.format(accuracy, misclass), fontdict= {'size':'16'})
    plt.show()


plot_confusion_matrix(cm = np.array([[16,  0,  0,  0,  0,  0],
 [ 0,15,  0,  0,  0,  0],
 [ 0,  0, 14,  1,  0,  0],
 [ 0,  0,  0, 16,  0,  0],
 [ 0,  0,  0,  0, 15,  0],
 [ 0,  0,  2,  0, 14,  0]]), normalize = False, target_names = ['Class 0', 'Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5'], title = "Confusion Matrix")

plot_confusion_matrix(cm = np.array([[16,  0,  0,  0,  0,  0],
 [ 2, 12,  1,  0,  0,  0],
 [ 0,  0, 15,  0,  0,  0],
 [ 0,  0,  1, 15,  0,  0],
 [ 0,  0,  2,  2, 11,  0],
 [ 0,  0,  4, 11,  1,  0]]), normalize = False, target_names = ['Class 0', 'Class 1', 'Class 2', 'Class 3', 'Class 4', 'Class 5'], title = "Confusion Matrix")



