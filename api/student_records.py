import datetime
from .apiQuery import *

class addStudentData(graphene.Mutation):
    class Arguments:
        studentdatainput = studentDataInput(required=True)
        #adminemail  = graphene.String(required=True)
        token       = graphene.String(required=True)

    error = graphene.Boolean()
    success_msg = graphene.Boolean()
    message = graphene.String()

    @classmethod
    @mutation_jwt_required
    def mutate(cls, __, info, studentdatainput, **args):
        first_name      = studentdatainput.first_name
        middle_name     = studentdatainput.middle_name
        last_name       = studentdatainput.last_name
        date_of_birth   = studentdatainput.date_of_birth
        gender          = studentdatainput.gender
        matric_number   = studentdatainput.matric_number
        email           = studentdatainput.email
        phone_number    = studentdatainput.phone_number
        address         = studentdatainput.address
        department      = studentdatainput.department
        enrollment_year = studentdatainput.enrollment_year
        current_gpa     = studentdatainput.current_gpa


        # Validate email format
        if not confirmEmail.isValid(email):
            return addStudentData(
                error=True,
                message=f"{email} is not a valid email! Kindly use a valid email address.",
                success_msg=False,
            )

        # Check if the matric number or email already exists
        existing_student_by_email = (
            info.context.get("session").query(Student).filter_by(email=email).first()
        )
        existing_student_by_matric = (
            info.context.get("session")
            .query(Student)
            .filter_by(matric_number=matric_number)
            .first()
        )

        if existing_student_by_email or existing_student_by_matric:
            return addStudentData(
                error=True,
                message=f"A student with this email ({email}) or matric number ({matric_number}) already exists.",
                success_msg=False,
            )

        # Convert date_of_birth to the correct format
        try:
            date_of_birth = datetime.strptime(date_of_birth, "%Y-%m-%d")
        except ValueError:
            return addStudentData(
                error=True,
                message="Invalid date format for date_of_birth. Use 'YYYY-MM-DD'.",
                success_msg=False,
            )

        # Create  student new_data object
        new_data = Student(
            first_name      = first_name,
            middle_name     = middle_name,
            last_name       = last_name,
            date_of_birth   = date_of_birth,
            gender          = gender,
            matric_number   = matric_number,
            email           = email,
            phone_number    = phone_number,
            address         = address,
            department      = department,
            enrollment_year = enrollment_year,
            current_gpa     = current_gpa,
            is_active       = True,  # Activate student by default
        )

        # Add the new student to the database
        try:
            db.session.add(new_data)
            db.session.commit()
            return addStudentData(
                error=False,
                message=f"Student {new_data.first_name} {new_data.last_name} successfully registered.",
                success_msg=True,
            )

        except IntegrityError as e:
            db.session.rollback()
            return addStudentData(
                error=True,
                message=f"Failed to register the student. Database error: {e.orig}",
                success_msg=False,
            )

        except Exception as e:
            db.session.rollback()
            return addStudentData(
                error=True,
                message=f"An unexpected error occurred: {str(e)}",
                success_msg=False,
            )
