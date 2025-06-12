# YOLO-Drone: Object Detection Platform Based on YOLOX

> **Project Name: YOLO-Drone**  
>
> **Full Name: Object Detection and Visualization System Based on YOLO Series**
>
> **Description:** *Developed and maintained by the YOLO-Drone team — Group of Course "New Technologies Topics (2)" instructed by Jin Xin*
>
> **Why we made it: Just for fun. 😄**
>
> *License: MIT*
>
> *GitHub Repository: [Echo-Nie/Drone-inspection-platform: Just for fun](https://github.com/Echo-Nie/Drone-inspection-platform)*
> 
> 🚀💻 Since I've already forgotten how to write Vue, I'm currently sticking to the basic front-end trio (HTML, CSS, JS). I plan to refactor and maintain the code using Vue after October! 

<p align="center">
  <img src="./assets/YOLO-Drone1.jpg" alt="YOLO-Drone" width="80%" />
</p>

<div align="center">
  
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-%23EE4C2C.svg?style=for-the-badge&logo=PyTorch&logoColor=white)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=for-the-badge&logo=opencv&logoColor=white)
![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)

</div>

<div align="center">
  
![GitHub repo size](https://img.shields.io/github/repo-size/Echo-Nie/YOLODrone-InspectionPlatform?style=flat-square&color=blueviolet)
![GitHub last commit](https://img.shields.io/github/last-commit/Echo-Nie/YOLODrone-InspectionPlatform?style=flat-square&color=teal)
![GitHub issues](https://img.shields.io/github/issues/Echo-Nie/YOLODrone-InspectionPlatform?style=flat-square&color=orange)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Echo-Nie/YOLODrone-InspectionPlatform?style=flat-square&color=green)
![License: MIT](https://img.shields.io/badge/License-MIT-yellowgreen.svg?style=flat-square)
![GitHub Commit Count](https://img.shields.io/badge/Commits-19-blue?style=flat-square)

</div>


## 🔍 Project Overview

This project is a lightweight object detection platform built upon **YOLO Series**, supporting image upload, model inference, result visualization, and historical record querying. The frontend is implemented using HTML + CSS + JavaScript for interactive user experience, while the backend is powered by Flask to provide robust web services. The overall architecture is simple and efficient, suitable for real-world applications such as drone aerial image analysis and intelligent surveillance.

We base our implementation on the [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) open-source framework, utilizing the pre-trained `yolo_x.pt` model. The complete detection pipeline is integrated into the Flask platform, enabling an end-to-end workflow from image upload to result display.



## 🛠️ Tech Stack

| Category                    | Technology / Tool                                   |
| --------------------------- | --------------------------------------------------- |
| **Deep Learning Framework** | PyTorch, Ultralytics YOLO                           |
| **Model Version**           | YOLOv_x                                             |
| **Backend Service**         | Flask                                               |
| **Frontend**                | HTML5 + CSS3 + JavaScript                           |
| **Image Processing**        | OpenCV                                              |
| **Data Storage**            | JSON Files (for storing detection history)          |
| **Deployment Dependencies** | Werkzeug (file upload), Jinja2 (template rendering) |



## 📦 Project Structure

```bash
YOLO-Drone/
├── assets/                   # Contains static resources used in the README (e.g., images, icons)
├── models/                   # Stores trained machine learning model files (e.g., uav.pt, yolov9c.pt)
├── routes/                   # Contains routing logic for defining API or page access paths
├── services/                 # Business logic modules: detection, history, data statistics, etc.
├── static/                   # Static resource directory (directly accessible by the frontend)
│   ├── css/                  
│   ├── js/                  
│   └── results/              # Stores output images from object detection
│       └── detect/           # Subdirectory for detection results; stores images generated during detection
├── templates/                # Frontend HTML templates used to render web content
├── uploads/                  # Directory for storing user-uploaded files
├── app.py                    # Starts the web server
├── config.py                 # Configuration file
├── requirements.txt          # List of Python dependencies required for the project
└── detection_history.json    # File that records detection history (e.g., timestamps, results)
```



## 🚀 Quick Start

**Install Dependencies**

```bash
pip install -r requirements.txt
```

**Launch the Server**

```bash
python app.py
```



## 👉 UI Display

Visit `http://localhost:5000` to access the object detection platform.

<p align="center">
  <img src="./assets/Index.png" alt="Index" width="100%" />
</p>

<p align="center">
  <img src="./assets/UI.jpg" alt="Index" width="100%" />
</p>

<p align="center">
  <img src="./assets/statics.png" alt="statics" width="100%" />
</p>

<p align="center">
  <img src="./assets/output.png" alt="output" width="100%" />
</p>

## 🖥️ Core Features

- ✅ Image Upload and Real-Time Detection  
- ✅ Detection Result Visualization (bounding boxes, class labels, confidence scores)  
- ✅ Detection Statistics Display (total objects, average confidence, per-class counts)  
- ✅ Detection History Management (automatically saves timestamp, image link, and detected objects)  
- ✅ Multi-Page Navigation (Home / History / About Us)



## 💡 Acknowledgments

Special thanks to the following open-source projects:

- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) — Efficient YOLO model implementation  
- [Flask](https://flask.palletsprojects.com/) — Lightweight web framework  
- [OpenCV](https://opencv.org/) — Core image processing library  
- [Werkzeug](https://palletsprojects.com/p/werkzeug/) — Flask dependency for file upload management  



## 🧩 Future Enhancements

- Support for real-time video stream detection (e.g., RTSP, webcam input)  
- Add user login and permission management system  
- Use SQLite or MongoDB for persistent detection history storage  
- Expose model as an API for integration with other systems  
- Deploy to cloud or server for public access
- 

## 🌠If you find this project helpful, please give it a ⭐
If you encounter any issues or have suggestions, feel free to:  
- Open an issue 🐛 on the [Issue Page](https://github.com/Echo-Nie/YOLODrone-InspectionPlatform/issues)  
- Submit a pull request 🚀 via [Pull Requests](https://github.com/Echo-Nie/YOLODrone-InspectionPlatform/pulls)
- Contact us via email ✉️ at [nyxchaoji123@163.com](nyxchaoji123@163.com)

Your support and contributions are greatly appreciated! 🌟
