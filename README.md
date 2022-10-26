
<a name="readme-top"></a>


<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a>
    <img src="media/logo.png" alt="Logo" width="80" height="80">
  </a>

<br />
<h1 align="center">Image Retrieval System for Police</h1>

  
  

  <p align="center">
    The objective of this project is to design a face recognition system for security
control. Our system helps the police to detect events that might otherwise be
overlooked or take a long time to detect manually
    <br />
    <br/>
    <a href="https://github.com/bqwerr/Criminal-Record-Management-System">Repository</a>
    <!-- · <a href="https://bqwerr.github.io">Explore the docs</a> -->
  </p>
</div>

<br />

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#usage">Usage</a></li>
      </ul>
    </li>
    <li><a href="#features">Features</a></li>
    <li><a href="#contributors">Contributors</a></li>
    <!-- <li><a href="#license">License</a></li> -->
    <li><a href="#contact">Contact</a></li>
    <li><a href="#references">References</a></li>
  </ol>
</details>


<br />

<!-- ABOUT THE PROJECT -->
## About The Project
<br />

Criminal Record Management System detects criminals using Artificial Intelligence in real time videos, images and alerts the human supervisor i.e. the police to take the
necessary action. Video frames are converted into image frames using OpenCV and these frames are sent to the system where it uses Facial recognition over those frames to identify probable persons in the frame that could match with the trained model. The facial detection is done using KNN algorithm and dlib library.Additional features of the system is that the citizen can register complaints, apply for NOCs (No Objection Certificate) and request an appointment with the higher officials in the police department whereas police can view those complaints, appointment requests and NOC requests.

<br />

### Flow Diagram 
![Flow Diagram](/media/flow.png)

<br />

### Steps Involved in Extracting Facial features.

* Get Byte Stream from Image 
* Resize Image with OpenCV
* Frontal Face detection using pre-trained model
* Get 64 Landmarks using pre-trained model
* Convert NumPy arrays into encoded string
* Store the record in the database
    * id - criminal Id
    * img - original image of the criminal
    * key_points - key points (64 facial landmarks of criminal) in the form of encoded string

### Steps for Training a Model based on criminal records from the database
* Fetch Label & Key Points for each record.
* Train the model using KNN classifier.
```python
encoded_labels = LabelEncoder().fit_transform(labels)
classifier = KNeighborsClassifier(n_neighbors=len(labels),
                                        algorithm='ball_tree',
                                        weights='distance')
classifier.fit(key_pts, encoded_labels)
```

### Class Diagram
![Class Diagram](/media/class.png)

### Use Case Diagram
![Use Case Diagram](/media/usecase.png)

### Sequence Diagram
![Sequence Diagram](/media/sequence.png)

<br />


<details>

<summary> Screenshots of the application </summary>

<br />

#### Sign Up Page
![Sign Up](/media/signup.png)

#### Login Page
![Login](/media/login.png)

#### Compliant Registration
![Compliant Registration](/media/compliant.png)

#### Dashboard
![Dashboard](/media/dashboard.png)

#### Add Criminal Record
![Add Criminal Record](/media/upload-record.png)

#### Match Image with Database
![Match Image](/media/search-image.png)

#### Result of Prediction
![Result](/media/result.png)

</details>
<br />

### Built With

[![My Skills](https://skillicons.dev/icons?i=django,python,jquery,js,html,bootstrap&perline=3)](https://skillicons.dev)


<br />

<!-- GETTING STARTED -->
## Getting Started

To get a local copy of this application up and running follow these example steps.

### Prerequisites

* Python & dlib have to be installed in your local machine.
* For dlib Installation, I have followed this <a href="https://medium.com/@royce236/how-to-install-dlib-for-python-with-visual-studio-2017-on-windows-10-2018-226e49eaba65">article</a>.

### Installation

1. Clone the repository
   ```sh
   git clone https://github.com/bqwerr/Criminal-Record-Management-System.git
   ```
2. In the root project directory, open a terminal and create a virtual environment to install python libraries.

    ```
    pip install virtualenv
    virtualenv env
    env\Scripts\activate
    ```

3. Now install python libraries

    ```
    pip install -r requirements.txt
    ```

4. Run the application, using below commands in sequence

    ``` 
    python manage.py makemigrations
    python manage.py migrate
    python manage.py runserver
    ```

- Now the application will be running at http://localhost:8000.

<br />

### Usage

Below are the API endpoints consumed at the frontend.

* Fetch all criminal records
```
api/records/
```
* Post URL to add a criminal record to the database
```
api/add-record/
```
* Delete a criminal record from the database
```
api/delete-record/<str:pk>/
```
* To train a KNN Classifier with the criminal records in the database
```
api/train/ 
```
* Post URL to match an image with the trained model. An image should be included in the request to this endpoint.
```
api/match/
```


<!-- ROADMAP -->
## Features

- Dashboard for Police to get criminal records of suspects.
- KNN Algorithm is used to match the suspect image to the actual criminal record over a database.
- An endpoint is built to accept image frame(s) and provides inputs to the trained model
- Citizen can raise Compliants, NOC Requests and Appointment Requests in the portal.
- Police can view latest requests in the dashboard and contact the users.

<br />

<!-- See the [open issues](https://github.com/github_username/repo_name/issues) for a full list of proposed features (and known issues). -->




<!-- CONTRIBUTING -->
<!-- ## Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.
If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request
<br /> -->


<!-- CONTACT -->

## Contributors

[Srujan Tumma][linkedin] \
[Sai Kiran Kammari][SaiLinkedin]




<!-- ACKNOWLEDGMENTS -->
## References
* [Django Rest Framework](https://www.django-rest-framework.org/#example)
* [Installing Dlib](https://medium.com/@royce236/how-to-install-dlib-for-python-with-visual-studio-2017-on-windows-10-2018-226e49eaba65)
* https://github.com/gaganmanku96/Finding-missing-person-using-AI
* [Face Recognition examples with Dlib](https://sefiks.com/2020/07/11/face-recognition-with-dlib-in-python/)


[website]: https://bqwerr.github.io
[linkedin]: https://linkedin.com/in/srujan-tumma
[gmail]: mailto:tummasrujan@gmail.com
[github]: https://github.com/bqwerr
[SaiLinkedin]: https://www.linkedin.com/in/saikirankammari/

