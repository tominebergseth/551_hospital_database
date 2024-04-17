# Hospital Appointment Manager: Distributed Database System

## Team: Tomine Bergseth & Omar Alkhadra 

## Project Description:
Distributed relational database system designed for a hospital to manage its appointments' data.
Tomine Bergseth has written the code in hospital_db.py for the database logic and command line
and Omar Alkhadra made the web based application.

## Requirements for running this project:
- To install the required packages run the following from the command line:
  - pip install -r requirements.txt
- In order to run this project, you need to have MySQL installed and have a MySQL username and password.
- Prior to running, please run the following code in MySQL to create the databases: 
  - CREATE DATABASE database1;
  - CREATE DATABASE database2;
- At the top of the code, there is an engine url dictionary. After creating the databases within MySQl,
  please updat ethe url string for each database with your password and username in the following format:
  - 'mysql+mysqlconnector://USERNAME:PASSWORD@localhost/database1'
  - Fill in the username and password as indicated above for each database url.
  - Alternatively, uncomment the login call at the top of main to login via the command line each time
  - you run the script.

## Instructions on how to call each function from the command line:
- In the command line, navigate to the folder where you have downloaded this directory: cd path/to/folder
- Note: the following examples use backslashes in the JSON objects 

## Adding data:
- General format: python hotpital_db.py add_operation json_object_with_data_to add
- Departments example: python hospital_db.py add_department 
  "{\"DepartmentID\": 1, \"DepartmentName\": \"Cardiology\", \"TotalRooms\": 100}"
- Receptionists example: python hospital_db.py add_receptionist 
  "{\"EmployeeID\": 211111, \"LastName\": \"Smith\", \"FirstName\": \"John\", \"DepartmentID\": 1}"
  - Note: EmployeeID must be 6 digits
- Practitioners example: python hospital_db.py add_practitioner 
  "{\"EmployeeID\": 111111, \"LastName\": \"Jones\", \"FirstName\": \"Amanda\",
  \"LicenseNumber\": 4567,  \"Title\": \"Doctor\", \"DepartmentID\": 1, \"Specialty\": \"General heart disease\"}"
  - Note: EmployeeID must be 6 digits
- Patients example: python hospital_db.py add_patient 
  "{\"PatientID\": 1000, \"LastName\": \"Brown\", \"FirstName\": \"Ollie\",  
  \"DOB\": \"1991-10-10\",  \"Gender\": \"Female\",  \"Insurance\": \"Aetna\", \"PastProcedures\":
  \"MR Scan\", \"Notes\":  \"Lung/breathing problems\",  \"DepartmentID\": 1}"
  - Note: PatientID must be 4 digits
- Appointments example: python hospital_db.py add_appointment "{\"ReceptionistID\": 211111,
 \"PatientID\": 1000, \"PractitionerID\": 111111, \"DepartmentID\": 1, \"AppointmentDate\": 
 \"2024-03-19\", \"AppointmentTime\": \"10:00\", \"Notes\": \"Follow-up appointment\"}

## Modifying data:
- General format:  python hospital_db.py modify_operation json_object_with_filter_requirements_for_rows_to_update 
  json_object_with_new_values_to_insert
  - Exception for departments: python hospital_db.py modify_department dept_id json_object_with_new_values
- Departments example: python hospital_db.py modify_department 1 "{\"DepartmentName\": \"Emergency\"}"
- Receptionists example: python hospital_db.py modify_receptionist "{\"EmployeeID\": 211111}" "{\"DepartmentID\": 3}"
- Practitioners example: python hospital_db.py modify_practitioner "{\"Title\": \"Doctor\"}" 
  "{\"Title\": \" Medical Doctor\"}"  
- Patients example: python hospital_db.py modify_patient "{\"PatientID\": 1000}"  "{\"Insurance\": \"Kasier\"}" 
- Appointments example: python hospital_db.py modify_appointment "{\"AppointmentTime\": \"10:00\"}"
  "{\"AppointmentTime\": \"10:30\"}"

## Deleting data:
- Note: if you are testing along with these examples, please test delete after retrieve in order to have data to retrieve.
- General format: python hospital_db.py delete_operation json_object_with_filter_requirements_for_rows_to_delete
  - Exception for departments: python hospital_db.py delete_department dept_id
- Departments example: python hospital_db.py delete_department 1
- Receptionists example: python hospital_db.py delete_receptionist  "{\"EmployeeID\": 211111}"
- Practitioner example: python hospital_db.py delete_practitioner "{\"LastName\": \"Jones\", \"FirstName\": \"Amanda\", 
  \"LicenseNumber\": 4567}"
- Patient example: python hospital_db.py delete_patient "{\"PatientID\": 1000}"
- Appointments example: python hospital_db.py delete_appointment  "{\"AppointmentID\": 1}"

## Retrieving data:
- General format: python hospital_db.py get_operation json_object_with_filter_requirements_for_rows_to_retrieve
  - Note: the json_object is an optional argument, if not provided it defaults to retrieving all rows for that table
    across both databases.
  - Exceptions: get_practitioner_for, get_patient_of
    - For these the format is: python hospital_db.py get_operation id_var optional_list_of_attribute_names_to_retrieve
    - Note: the id_var is the PractitionerID in get_patient_of that you want to see patients of and
      PatientID for get_practitioner_for that you want to see practitioners for.
- Departments example: python hospital_db.py get_department "{\"DepartmentID\": 1}"
- Receptionists example: python hospital_db.py get_receptionist "{\"DepartmentID\": 1}"
- Practitioners example: python hospital_db.py get_practitioner "{\"Title\": \"Medical Doctor\"}"
- Patients example: python hospital_db.py get_patient "{ \"LastName\":  \"Brown\"}"
- Appointments example: python hospital_db.py get_appointment "{ \"AppointmentDate\": \"2024-03-19\"}"

- Examples to retrieve all for departments, patients, practitioners, receptionists, and appointments tables:
  - python hospital_db.py get_department
  - python hospital_db.py get_receptionist
  - python hospital_db.py get_practitioner
  - python hospital_db.py get_patient
  - python hospital_db.py get_appointment
  
- Patient_Of examples:
  - get_patient_of: python hospital_db.py get_patients_of 111111
    - With optional list of attributes to return: python hospital_db.py get_patients_of 111111 "[FirstName, LastName]"
  - get_practitioners_for: python hospital_db.py get_practitioners_for 1000
    - With optional list of attributes to return: python hospital_db.py get_practitioners_for 1000 "[FirstName, LastName]"

