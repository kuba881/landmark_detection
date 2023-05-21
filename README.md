# landmark_detection
This project investigates facial asymmetry using Kinect v2 and a webcam for data collection. During balance system surgery, the facial nerve is severed and part of the face is paralyzed. The goal of this project is to create an application that would help doctors classify the degree of disability of a patient. The recording devices track specific points on the human face. Based on these points, the patient can be classified. 

The first part focuses on the graphical user interface created in Matlab environment. This GUI is used to control the whole recording process and to retrieve data. GUI is file getapp_02 and run script faceRecord. For getting information about records, reading app was created. This app is in file tabulkainfa and run script readapp. 

The second part of the work was to evaluate the obtained data using statistical methods. The aim of this part was to reduce the number of points used because many of them are not applicable. Firstly, script calculate_disstance_angles calculate distances and angles between two selected points based on specific table. All used tables are in folder Source of points. Next scripts Compare_all_same_records, Compare_every_point_againts_each_other and Compare_two_records were used for selecting the most useable pairs for classifiers.

The last part was classification using machine learning. Due to the low number of records, it is able to classify whether the patient is healthy or paralyzed. Methods used for classification are in file binary_classifier. Results of classification were validated using two methods. Leave one out validation (script validation_LOO) and k-fold validation (validation_k_fold). For better imagination, results were plotted in scripts visualization_kinect and visualization_openCV.

In the future I would like to get more data to evaluate and try to use fuzzy logic to classify into more than two groups.
