# Comp-Science-Project

## Installation
1. Clone this repository
2. Change directory to api/mask
    ```bash
    cd api/mask
    ```
3. Install dependencies for back-end. Ensure that [compatible versions](https://www.tensorflow.org/install/source#tested_build_configurations) of tensorflow-gpu, CUDA and CUDNN are installed. *(Tested working on tensorflow-gpu v1.12.0, CUDA v9.0, CUDNN v7.3.1, Keras v2.2.4)*
   ```bash
   pip3 install -r requirements.txt
   python3 setup.py install
   ```
4. Change directory to react root directory and install dependencies for front-end React
    ```bash
   cd ../../react-ui/cctv-dashboard
   npm install
   ```
   
## Running the program
1. Open 3 terminals.
2. In terminal 1, change directory to React root directory. Start the React front end.
    ```bash
    cd react-ui/cctv-dashboard
    npm start
    ```
3. In terminal 2, change directory to back-end root directory. Start the Django API.
    ```bash
   cd api
   python manage.py runserver
   ```
4. In terminal 3, change directory to back-end root directory. Start the Django queue.
    ```bash
   cd api
   python manage.py process_tasks
   ```
   
## Navigating the website
 The website contains 3 main sections. The Cameras page, the Statistics for each page, and the Analysis page that show the stats charts and tabular form the data displayed. On the camera page, enter the download URL of a video as input for one of the cameras.