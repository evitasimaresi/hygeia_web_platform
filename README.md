# hygeia: A web-bases application for managing health cases.

#### Video Demo: [Youtube](https://youtu.be/7oPtC_Hg6jw) 
https://youtu.be/7oPtC_Hg6jw


## Description:
This project is a web-based platform. The two user-types available are the `Patient` and the `Doctor`. It intends to offer the possibility to patients to log health issues they face and book an appointment with a doctor of their choice. Then they can keep track of upcoming appointments or even review their history of logged cases. On the other side doctors are able to review their daily schedule and get more information for each case.

## Planification:
### Technologies
#### Programming Languages
For the front-end HTML, CSS and Javascript were used. Python was used for the backend.

#### Web framework
Flask helped to host the web application and mak it dynamic. Also Django was used to manage content in a more dynamic way.

#### Databases
[SQLAlchemy](https://www.sqlalchemy.org/) was chosen to manage the database because of its simplicity while using Python language.

#### Libraries and dependencies
Major libraries used are:
* [Full calendar](https://fullcalendar.io/) is a JavaScript library which integrates event calendars. It was particularly useful for rendering the calendar so the patients can book appointments and also to visualize the upcoming appointments for both patients and doctors.
* [WTForms](https://wtforms.readthedocs.io/en/3.1.x/) is a Python library to render and validate forms. It was usefully on creating classes for each form and implement validators optimizing the time efficiency of the project.
* [email-validator](https://pypi.org/project/email-validator/) is a Python library which helps validate if strings have the e-mail format. It was useful for the registering form.
* Flask extensions such **Flask-Session**, **Flask-SQLAlchemy** and **WTForms-SQLAlchemy** where used.
* [Bootstrap](https://getbootstrap.com/) framework provided interface components that served as a base tool-kit for the front-end of the application.

Additionally the following APIs were used:
* [Memegen.link](https://memegen.link/) generates memes programmatically. The inspiration and source is the Problem Set 9. I kept the purpose of use and adopt it to the current platform's needs.
* Bard API give access to the Google's Bard LLM. The purpose of this use is to implement an AI assistant for the patient to get suggestions and for the doctor to process the patient input. Later technical issues rendered the implementation impossible.

> [!NOTE]
> The page "Chat" originally intended to visualize the implementation of Bard API which would give the impression to the user of chatting with the platform about his case. At the moment only the name left as a remembrance of the initial intension.

### UX/UI Design
Originally Figma helped to set a base about the desired design of the user's interface. Later on changes on the structure of the application led to different UI choices.

![ui-ux](/images/UI-UX.png)

### Directory Structure
The directory structure is shown on the below figure (1). The specific organization aimed to apply best practices tough during. Furthermore starting from top to bottom:
* `project` contains all the directories of the project and as well python configuration and initialization files, the list of dependencies and the README file.
* `app` directory contains all sub-directories including the static part of the platform and the flask's files aw well. 
* `Backup` and `test` directories contain files the helped during the development phase and do not offer any additional functionality on the final product.
* `instance` contains the database and data relative files.
* `venv` contain the configuration of the virtual environment created to isolate all the dependencies. This directory is excluded from version control.

![Diagram of directories.](/images/directories_diagramm.png)


### Component description
The following section is focused on providing a brief understanding of the core components consisting the project starting from the components that form the foundations of the platform's functionality and ultimately will be  presented components which don't have a foundational role.
* `__init__.py` initialize the Flask application, it configures the database with SQLAlchemy, set a server session using Flask-session, import the application's routes and finally a function initialize the database if it wasn't already initialized. The `commands.py` work complementary by providing basic logic functionality on the initialization stage of the database. It helps as it organize all relevant functionalities in one file leaving the maintain __init__ file cleaner, functions help to reuse the code and make it modular and basic error handling is giving a proper feedback about the process of initialization.
* `models.py` the database models are defined using SQLAlchemy, which serve as the core components of the database schema. The classes defined are **User** , **Patient**, **Doctor**, **Specialty**, **Case**, **Appointments** each represent a table in the database, the graphical representation of which is presented on the following figure (2). These classes define the field and relationship between them. Auxiliary class methods include registering new instances and committing them to the tables and serialization of the models converting them into JSON dictionaries. The structure followed gives efficiency in manipulating and retrieving data, improving the overall functionality of the application.

    ![Database schema](/images/database_schema.png)

* `forms.py` define the form classes using Flasf-WTF and WTF forms to handle submissions and validations. Three classes included are the **UserForm**, **Symptoms** and **Appointments** where fields and validators defined to control user’s input. **FlaskForms** are implemented and fields and validators from **wtforms** introduced on top. Form logic and view logic is separate and custom validation in complex validation needs indicate best practices.

* `routes.py` define the URL route and control the logic on requests to those URLs. Route functions control the user authentications like registering and login, booking appointment displacing appointments and logging new cases. Auxiliary functions can render views and session and request objects handle the incoming data. Best practices followed are the separation of the functionalities into different files, like the `helpers.py` and using decorators like **@login_required** to ensure proper security. Also, exceptions and errors are handled and helpful error messages provided to users ensuring a better user experience. Also, encrypting passwords using Werkzeug library ensures secure storage and authentication. Hashed password stored in the database instead of the plaintext password reduce the risk of unauthorized access in case of a data breach.

* **templates** directory contains all HTML templates. 
    - First and foremost, `layout.html` served as the base template which provided a layout for all other pages. It included all necessary elements for every HTML page, such as header and footer and also the navigation bar and any flask messages. Jinja2 used here offer a dynamic insert of content and specifically the  `{% block %}` tag ensures that page continent can inserted into **layout.html** keeping a consistent look and functionality across the platform while keeping any page separate.
    - `index.html` serves as the homepage of the application, it provides a welcome message, and information about upcoming appointments all customized for each user type, controlled by a conditional statement and session data.
    - The `authuser.html`, `userform.html`, `login.html`, `register.html` and `userform.html` work as a group and visualize the user authentication pages such as register and login. `authuser.html` provide the two bootstrap buttons to let user choose register or login. `login.html` and `register.html` control the action type and both call `userform.html` as the final element the render the final forms for both actions. This form elements used respectably by both actions such as the button to choose the user type, username and password field. Alternatively, when `register` is selected as action Jinja2 conditions render the extra fields required. A separate `<select>` field is available when `Doctor` is the chosen user type, but the appearance will be reviewed later on the section for `script.js`. The system created probably overcomplicated the functionality as `login.html` and `register.html` are probably unnecessary.
    - `chat.html` is a template available only for **Patients** and renders the form in which the user will insert information about a health issue. The form's structure is clear and simple for use and contain only the necessary information.
    - `appointments.html` is another template available only for **Patients** and contain two main elements. Firstly, a table, lists all cases that are not connected with an appointment giving all information provided by the user. For each case the patient can choose the specialty and eventually the available doctor that which to book the appointment. Next, a calendar will render and update to the available hours for each selected doctor. From this calendar the user can book an appointment by clicking in the desired date and time. Also, a message shown the select doctor is there to remind of the last selected doctor.
    - `history.html` is the last template available for patients. The main functionality is to render all the history of cases logged for each user. This is achieved with a table. Specifically, for each handled case a `more info` button will preview the date-time of the appointment and the doctor. If the case is not handled the `book appointment` button available will redirect the user back to `appointments.html`.
    - Lastly the `apology.html` template displays an apology message to the user and is part of the error handling user interface. The messages are customized and error code can be also customized. It improves the overall user experience (UX) by giving feedback on mistakes made and make the application more user-friendly.

* `script.js` contains JavaScript code that provide interactive actions to the application. The code is separated into functions to ensure better organization, modularity and reusability. Ajax requests are made to render new elements without the need for reloading all page while implementing XMLHttpRequests. Event listeners provide interactivity and feedback to user. Also, the FullCalendar library is configured, initialized and organized according to library's documentation and organized in functions.

* `style.css` define the style for HTML elements. Basic variables set to ensure consistency and styles organized by component. While bootstrap library a visually appealing result with excellent functionality it was critical to ensure a unique and custom design for the webpage. So the customization of all elements individually ensured this.

## Setup
1. Activate the virtual environment
```
cd venv/venv/bin/
source activate
```

2. Install dependencies:
```
cd ../../..
pip install -r requirements.txt
```

3. Run flask server

```
python3 run.py
```
4. Follow the address in web browser, the application is running in the following address.
```
http://127.0.0.1:5000
```

## Use case
The application support two user types. The `Patient` and the `Doctor`.
### Patient: Marina
In the first use case we will observe Marina. Marina lately is feeling a chest pain so she decided to use the new platform that her friend's suggested her.

1. First she should register as a new user. When she register successfully she will arrive to home page.

    ![register-p](/images/register-p.gif)

2. From the home page she can even navigate to chat tab or follow the welcome message to log her case. She fill the form as shown below and by saving the case she will be redirected in the appointments tab.

    ![log-case](/images/log-case.gif)

3. Now that her case is logged, she will choose doctor specialty and then choose between the available doctors. From the calendar previewed she will ultimately book an appointment. A message will reminder her the last doctor chosen.

    ![book-appointment](/images/appointment.gif)

4. Now she can navigate at any moment to home page to review upcoming appointments or to history tab to get a list of all cases logged with all related details.

    ![upcoming-history](/images/index-history.gif)

---
### Doctor: Chloe
In the second case we follow a Cardiologist, Chloe. 

1. Chloe wants to register. She has to follow the same method as Marina, but in Chloe's case she should choose `Doctor` and from the top-down menu select her specialty.

    ![register-d](/images/register-d.gif)

2. In the future Chloe can login whenever she wants and review her daily schedule. Inspect upcoming appointments with details about the case.

    ![upcoming](/images/login-uppcoming-d.gif)

---
### Error messages

1. Error messages during user authentication guide the user to fix wrong inputs.

    ![error-1](/images/error-1.gif)

1. Errors can happen also when the user log new case.

    ![error-2](/images/error-2.gif)


## Future improvements:
As there is always room for improvement, I would personally set a new milestone for future improvements.

> 1. Direct communication between doctor and patient. The doctor can make comments and suggestions before the appointment. Also, they will be given the possibility to log their prescription related to each handled case.
>
> 1. Implement an LLM model to assist doctor with managing and analyzing each case. And eventually reducing the administrating tasks for the doctor.
>
> 1. Additional functionality such us history case manipulation and user settings can be added. As well as an admin user type for administrative staff.

## Conclusion

Firstly, a brief `Description` of the web application was made. It was followed by the `Planification` section, which presented the chosen **technologies** and the structure and purpose of the project's **directory**. Also, a detailed description of each major **component** was analyzed. Last topic mentioned was a **setup guide**. Next `User Cases` section showcased the application from the user’s perspective. Last but not least `Future improvements` set new goals for new features.

Flask played a major role to elevate the capabilities of this project and possible serve a product that will equipped the users with a power fool tool. This project is the applied knowledge gathered throughout during the course of CS50. It is not considered finished, but is a good foundation for future projects as well as a proof of personal improvement.


**I hope this documentation serves as a valuable resource for understanding this project. Feedback and contribution is always welcome from the community.**
