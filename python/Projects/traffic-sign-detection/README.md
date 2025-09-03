Traffic Sign Detection
This is the code for the paper

Evaluation of deep neural networks for traffic sign detection systems
Álvaro Arcos-García, Juan Antonio Álvarez-García, Luis M. Soria-Morillo

The paper addresses the problem of traffic sign detection analysing the state-of-the-art of several object-detection systems (Faster R-CNN, R-FCN, SSD, and YOLO V2) combined with various feature extractors (Resnet V1 50, Resnet V1 101, Inception V2, Inception Resnet V2, Mobilenet V1, and Darknet-19). We aim to explore the properties of these object-detection models which are modified and specifically adapted to the traffic sign detection problem domain by means of transfer learning. In particular, various publicly available object-detection models that were pre-trained on the Microsoft COCO dataset are fine-tuned on the German Traffic Sign Detection Benchmark dataset. The evaluation and comparison of these models include key metrics, such as the mean average precision (mAP), memory allocation, running time, number of floating point operations, number of parameters of the model, and the effect of traffic sign image sizes.

We provide:

Several pretrained models.
Experiment results.
Test code to run the model on new images.
Instructions for training your model.
Instructions for evaluating your model.
Scripts to create GTSDB TFRecords.