import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import bcrypt

from hospital_db import Department, Appointment, Reception, Practitioner, Patient, Base, hash_department, engine_urls  # Import your Appointment class and Base from your module

# Hardcoded user credentials
users = {
    "omar": {
        "username": "omar",
        "password": bcrypt.hashpw("password".encode('utf-8'), bcrypt.gensalt())
    },
    "tomine": {
        "username": "tomine",
        "password": bcrypt.hashpw("password".encode('utf-8'), bcrypt.gensalt())
    }
}


# Define a custom session state class
class SessionState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

# Create a session state object
session_state = SessionState(logged_in=False)

def login():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False

    if st.session_state.logged_in:
        return True
    
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in users and bcrypt.checkpw(password.encode('utf-8'), users[username]["password"]):
            st.session_state.logged_in = True
            st.success("Logged in as {}".format(username))
            return True
        else:
            st.error("Invalid credentials")
    return False

def home_page():
    st.title("Appointment Management System")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Appointments", "Patients", "Practitioners", "Departments"])
    
    with tab1:
        st.title('Appointments')
        subtab1, subtab2 = st.tabs(["New Appointments", "Appointment Information"])

        with subtab1:
            receptionist_id = st.number_input('Receptionist ID', min_value=1, step=1, key="Add Receptionist ID, appointments")
            patient_id = st.number_input('Patient ID', min_value=1, step=1, key="Add Patient ID, appointments")
            practitioner_id = st.number_input('Practitioner ID', min_value=1, step=1, key="Add Practitioner ID, appointments")
            department_id = st.number_input('Department ID', min_value=1, step=1, key="Add Department ID, appointments")
            appointment_date = st.date_input('Appointment Date', key="Add Appointment Date, appointments")
            appointment_time = st.time_input('Appointment Time', key="Add Appointment Time, appointments")
            notes = st.text_area('Notes', key="Add Notes, appointments")

            if st.button('Add Appointment'):
                db_num = hash_department(department_id)
                engine = create_engine(engine_urls[db_num])
                
                # create session class
                Session = sessionmaker(bind=engine)
                session = Session()  # session instance
                appt_dict = {
                    'ReceptionistID': receptionist_id,
                    'PatientID': patient_id,
                    'PractitionerID': practitioner_id,
                    'DepartmentID': department_id,
                    'AppointmentDate': appointment_date,
                    'AppointmentTime': appointment_time,
                    'Notes': notes
                }
                new_appointment = Appointment.add_appointment(session, appt_dict)
                st.success(f'Appointment added successfully. ID: {new_appointment.AppointmentID}')


        with subtab2:
            filter_options = {
            "AppointmentID": st.number_input("Appointment ID", value= None, step=1, key="Get Appointment ID, appointments"),
            "DepartmentID": st.number_input("Department ID", min_value=1, step=1, key="Get Department ID, appointments")
            }
            
            if st.button("Retrieve Appointment Information"):
                db_num = hash_department(filter_options["DepartmentID"])
                engine = create_engine(engine_urls[db_num])
                
                # create session class
                Session = sessionmaker(bind=engine)
                session = Session()  # session instance
                filtering_dict = {key: value for key, value in filter_options.items() if value}
                appointments = Appointment.get_appointment(session, filtering_dict)

                if appointments:
                    st.write("Appointment found:")
                    for appointment in appointments:
                        st.write(f"Appointment ID: {appointment.AppointmentID}")
                        st.write(f"Department ID: {appointment.DepartmentID}")
                        st.write(f"Receptionist ID: {appointment.ReceptionistID}")
                        st.write(f"Patient ID: {appointment.PatientID}")
                        st.write(f"Practitioner ID: {appointment.PractitionerID}")
                        st.write(f"Appointment Date: {appointment.AppointmentDate}")
                        st.write(f"Appointment Time: {appointment.AppointmentTime}")
                        st.write(f"Notes: {appointment.Notes}")
                        st.write("---")
                else:
                    st.write("No appointments found matching the filtering criteria.")
   
    with tab2:
        st.title('Patients')
        subtab1, subtab2 = st.tabs(["New Patients", "Patient Information"])

        with subtab1:
            filter_options = {
                "PatientID": st.number_input('Patient ID', min_value=1, key="Add Patient ID, patients"),
                "DepartmentID": st.number_input('Department ID', min_value=1, key="Add Department ID, patients"),
                "LastName": st.text_input('Last Name', key="Add Last Name, patients"),
                "FirstName": st.text_input('First Name', key="Add First Name, patients"),
                "DOB": st.date_input('Date of Birth', key='Add DOB, patients', ),
                "Gender": st.text_input('Gender', key='Add Gender, patients'),
                "Insurance": st.text_input('Insurance Status', key="Add Insurance, patients"),
                "PastProcedures": st.text_input('Past Procedures', key="Add Past Procedures, patients"),
                "Notes": st.text_area('Notes', key="Add Notes, patients")
            }
            if st.button('Add Patient'):
                db_num = hash_department(filter_options["DepartmentID"])
            
                # create session class
                engine = create_engine(engine_urls[db_num])
                Session = sessionmaker(bind=engine)
                session = Session()  # session instance
                
                filtering_dict = {key: value for key, value in filter_options.items() if value}

                new_patient = Patient.add_patient(session, filtering_dict)
                st.success(f'Patient added successfully. ID: {new_patient.PatientID}')
        
        with subtab2:
            filter_options = {
            "PatientID": (st.number_input("Patient ID", value= None, step=1, key="Get Patient ID, patients")),
            "DepartmentID": (st.number_input("Department ID", value=None, step=1, key="Get Department ID, patients"))
            }

            if st.button("Retrieve Patient Information"):
                db_num = hash_department(filter_options["DepartmentID"])
            
                # create session class
                engine1 = create_engine(engine_urls[db_num])
                Session1 = sessionmaker(bind=engine1)
                session1 = Session1()  # session instance
                
                if db_num == 1:
                    engine2 = create_engine(engine_urls[0])
                    Session2 = sessionmaker(bind=engine2)
                    session2 = Session2()  # session instance
                
                elif db_num == 0:
                    engine2 = create_engine(engine_urls[1])
                    Session2 = sessionmaker(bind=engine2)
                    session2 = Session2()  # session instance


                filtering_dict = {key: value for key, value in filter_options.items() if value}
                patients = Patient.get_patient(session1, session2, filtering_dict)

                if patients:
                    st.write("Patient(s) found:")
                    st.write(patients)
                    st.write(patients[0])
                    for patient in patients:
                        st.write(f"Patient ID: {patient.PatientID}")
                        st.write(f"Department ID: {patient.DepartmentID}")
                        st.write(f"Last Name: {patient.LastName}")
                        st.write(f"First Name: {patient.FirstName}")
                        st.write(f"Scheduling State: {patient.SchedulingState}")
                        st.write(f"Date of Birth: {patient.DOB}")
                        st.write(f"Gender: {patient.Gender}")
                        st.write(f"Insurance: {patient.Insurance}")
                        st.write(f"Past Procedures{patient.PastProcedures}")
                        st.write(f"Notes: {patient.Notes}")
                        st.write("---")
                else:
                    st.write("No patients found matching the filtering criteria.")

    with tab3:
        st.title('Practitioners')
        st.subheader("Practitioner Information")

        filter_options = {
            "DepartmentID": int(st.number_input("Department ID", min_value=1, step=1, key="Get Department ID, employees"))
            }

        if st.button("Retrieve Practitioner Information"):
            db_num = hash_department(filter_options["DepartmentID"])
            
            # create session class
            engine1 = create_engine(engine_urls[db_num])
            Session1 = sessionmaker(bind=engine1)
            session1 = Session1()  # session instance
            
            if db_num == 1:
                engine2 = create_engine(engine_urls[0])
                Session2 = sessionmaker(bind=engine2)
                session2 = Session2()  # session instance
            
            elif db_num == 0:
                engine2 = create_engine(engine_urls[1])
                Session2 = sessionmaker(bind=engine2)
                session2 = Session2()  # session instance

            practitioners, tot_count = Practitioner.get_practitioner(session1, session2, filter_options)
            st.write(practitioners)
            
            if practitioners:
                st.write([practitioners[0]])
                st.subheader("Employee(s) found:")
                
                st.write(f"Employee ID: {practitioners[0][0].EmployeeID}")
                st.write(f"Department ID: {practitioners[0][0].DepartmentID}")
                st.write(f"Last Name: {practitioners[0][0].LastName}")
                st.write(f"First Name: {practitioners[0][0].FirstName}")
                st.write(f"Title: {practitioners[0][0].Title}")
                st.write(f"License Number: {practitioners[0][0].LicenseNumber}")
                st.write(f"Specialty: {practitioners[0][0].Specialty}")
                st.write("---")
            else:
                st.write("No Practitioners found matching the filtering criteria.")

    with tab4:
        st.title('Departments')
        st.subheader("Department Information")

        filter_options = {
            "DepartmentID": int(st.number_input("Department ID", step=1, key="Get Department ID, departments"))
            }

        if st.button("Retrieve Department Information"):
            db_num = hash_department(filter_options["DepartmentID"])
            
            # create session class
            engine1 = create_engine(engine_urls[db_num])
            Session1 = sessionmaker(bind=engine1)
            session1 = Session1()  # session instance
            
            if db_num == 1:
                engine2 = create_engine(engine_urls[0])
                Session2 = sessionmaker(bind=engine2)
                session2 = Session2()  # session instance
            
            elif db_num == 0:
                engine2 = create_engine(engine_urls[1])
                Session2 = sessionmaker(bind=engine2)
                session2 = Session2()  # session instance


            departments = Department.get_department(session1, session2, filter_options)
            if departments:
                st.subheader("Department found:", )

                st.write(f"Department ID: {departments[0][0].DepartmentID}")
                st.write(f"Department Name: {departments[0][0].DepartmentName}")
                st.write(f"Total Employees: {departments[0][0].TotalEmployees}")
                st.write(f"Total Rooms: {departments[0][0].TotalRooms}")
                st.write("---")

            else:
                st.write("No Departments found matching the filtering criteria.")


if __name__ == "__main__":
    if login():
        home_page()
