# Background Removal API
This is a restful API which removes background of images using Trace-B7 segmentation model.

## Installation

* First of all clone the project:
```console
username@hostname:~$ git clone https://github.com/EngRobot33/Background-Removal-API
```
* Then, we need a virtual environment you can create like this:
```console
username@hostname:~/Background-Removal-API$ virtualenv venv
```
* Activate it with the command below:
```console
username@hostname:~/Background-Removal-API$ source venv/bin/activate
```
* After that, you must install all of the packages in `requirements.txt` file in project directory:
```console
username@hostname:~/Background-Removal-API$ pip install -r requirements.txt
```
* Move the images you want to remove their backgrounds in `images` directory.
* Change directory to `src`.
```console
username@hostname:~/Background-Removal-API$ cd src
```
* Download the Tracer-B7 model file from [here](https://huggingface.co/Carve/tracer_b7/resolve/d8a8fd9e7b3fa0d2f1506fe7242966b34381e9c5/tracer_b7.pth) to `src` folder alongside `manage.py` file.
* Create a `.env` file there, then add your created config:
```python
SECRET_KEY = 'Your secret key generated by https://djecrety.ir'
DEBUG = 'Project debug status'
```
* Enter the following command for migrations:
```console
username@hostname:~/Background-Removal-API/src$ python3 manage.py migrate
```
* Run the project via this command:
```console
username@hostname:~/Background-Removal-API/src$ python3 manage.py runserver
```
* In a new Termianl, change directory backwards and run the `main.py` file for starting processing:
```console
username@hostname:~/Background-Removal-API/src$ cd ..
username@hostname:~/Background-Removal-API$ python3 main.py
```
* Now the results are ready in `src/media` directory.
* Run the command below for tests:
```console
username@hostname:~/Background-Removal-API/src$ python3 manage.py test
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.


