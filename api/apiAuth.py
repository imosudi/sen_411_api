
from helpers.uniquifier import generateUniqueString
from .apiQuery import *


# Authentication
class RefreshMutation(graphene.Mutation):
    class Arguments(object):
        refresh_token = graphene.String()

    new_token = graphene.String()

    @classmethod
    @mutation_jwt_refresh_token_required
    def mutate(self, _):
        current_user = get_jwt_identity()
        return RefreshMutation(
            new_token=create_access_token(identity=current_user),
        )
    
class authenticateAppUser(graphene.Mutation):
    error           = graphene.Boolean()
    message         = graphene.String()
    success_msg     = graphene.Boolean()
    accessToken     = graphene.String()
    refreshToken    = graphene.String()

    class Arguments:
        email       = graphene.String(required=True)
        password    = graphene.String(required=True)

    @classmethod
    def mutate(cls, __, info, email, password, **args):
        if not confirmEmail.isValid(email):
            return authenticateAppUser(
                error   = True, 
                message = "{email} not a valid email! Kindly use a valid email address",
                success_msg = False
            )
        
        existing_users  = UserObject.get_query(info)
        thisUser        = existing_users.filter(UserModel.email==email).first()
        #thisUser        =  User.query.filter_by(email=email).first()
        #print(thisUser)
        
        if not thisUser or thisUser.is_valid_client != True or not check_password_hash(thisUser.password, password):
        #if not thisUser  or not check_password_hash(thisUser.password, password):
            return authenticateAppUser(
                error           = True,
                success_msg     = False,
                message         = "Bad username or password! Kindly login with approved login details or request for user activation"                    
            )
        accessToken     = create_access_token(thisUser.email)#id)
        refreshToken    = create_refresh_token(thisUser.email)#id)
        
        return authenticateAppUser(
                error           = False,
                success_msg      = True,
                message         = "success",
                accessToken     = f"{accessToken}",
                refreshToken    = f"{refreshToken}"
            )


class enrolAppUser(graphene.Mutation):
    class Arguments:
        enrolmentappuserinput = enrolmentAppUserInput(required=True)

    error       = graphene.Boolean()
    success_msg = graphene.Boolean()
    message     = graphene.String()

    @classmethod
    def mutate(cls, __, info, enrolmentappuserinput, **args):
        email                   = enrolmentappuserinput.email
        password                = enrolmentappuserinput.password
        password_confirm        = enrolmentappuserinput.password_confirm

        # Validate email format
        if not confirmEmail.isValid(email):
            return enrolAppUser(
                error=True, 
                message=f"{email} is not a valid email! Kindly use a valid email address.",
                success_msg=False
            )
                            
        # Ensure passwords match
        if password != password_confirm:
            return enrolAppUser(
                error=True,
                message="Password mismatch! Ensure the same value for password and password_confirm.",
                success_msg=False
            )

        # Check if the user already exists
        existing_users  = UserObject.get_query(info)
        thisUser        = existing_users.filter(UserModel.email == email).first()

        if thisUser:
            return enrolAppUser(
                error=True,
                message=f"App user with this email address, {email}, exists. \nYou might want to reset your password if you're unable to connect.",
                success_msg=False
            )

        # Generate unique identifier
        fs_uniquifierbuild  = generateUniqueString('uniquifier')
        fs_uniquifier       = fs_uniquifierbuild.generateString()

        # Check if this is the first user
        is_first_user       = not existing_users.count()

        # Create the new user
        new_user = User(
            email=email,
            password=generate_password_hash(password, method="sha256"),
            fs_uniquifier=fs_uniquifier,
            active=is_first_user,  # Activate the first user by default
            is_valid_client=is_first_user,  # Validate the first user by default
            is_admin=is_first_user
        )

        # Add the new user to the database
        try:
            db.session.add(new_user)
            db.session.commit()
            message = f"Registration for {email} successful!"
            if is_first_user:
                message = f"Registration for {email} successful! This is the primary admin account"
            return enrolAppUser(
                error=False,
                message=message,
                success_msg=True
            )

        except IntegrityError as e:
            db.session.rollback()
            return enrolAppUser(
                error=True,
                message=f"Registration failed due to database error: {e.orig}",
                success_msg=False
            )

        except Exception as e:
            db.session.rollback()
            return enrolAppUser(
                error=True,
                message=f"Registration failed due to an error: {str(e)}",
                success_msg=False
            )


class activateAppUser(graphene.Mutation):
    error       = graphene.Boolean()
    success_msg = graphene.Boolean()
    message     = graphene.String()

    class Arguments:
        email       = graphene.String(required=True)
        adminemail  = graphene.String(required=True)
        token       = graphene.String(required=True)

    @classmethod
    @mutation_jwt_required
    def mutate(cls, __, info, email, adminemail, **args):
        # Validate the adminemail
        if not confirmEmail.isValid(adminemail):
            return activateAppUser(
                error=True, 
                message=f"{email} is not a valid admin email! Kindly use a valid email address.",
                success_msg=False
            )

        # Query the user by email
        existing_users  = UserObject.get_query(info)
        adminUser       = existing_users.filter(UserModel.email == adminemail).first()
        
        if not adminUser:
            return activateAppUser(
                error=True,
                message=f"This email {email} does not belong to the admin group. You're not allowed to activate another user.",
                success_msg=False
            )


        # Validate the email
        if not confirmEmail.isValid(email):
            return activateAppUser(
                error=True, 
                message=f"{email} is not a valid email! Kindly use a valid email address.",
                success_msg=False
            )

        # Query the user by email
        existing_users  = UserObject.get_query(info)
        thisUser        = existing_users.filter(UserModel.email == email).first()
        

        if not thisUser:
            return activateAppUser(
                error=True,
                message=f"No user found with email {email}. Please check the email or register first.",
                success_msg=False
            )

        if thisUser.active:
            return activateAppUser(
                error=False,
                message=f"The user with email {email} is already activated.",
                success_msg=True
            )

        # Activate the user
        try:
            thisUser.active = True
            db.session.commit()
            message = f"User with email {email} has been successfully activated!"
            return activateAppUser(
                error=False,
                message=message,
                success_msg=True
            )
        except Exception as e:
            db.session.rollback()
            return activateAppUser(
                error=True,
                message=f"Activation failed due to an error: {str(e)}",
                success_msg=False
            )

class deactivateAppUser(graphene.Mutation):
    error       = graphene.Boolean()
    success_msg = graphene.Boolean()
    message     = graphene.String()

    class Arguments:
        email       = graphene.String(required=True)
        adminemail  = graphene.String(required=True)
        token       = graphene.String(required=True)

    @classmethod
    @mutation_jwt_required
    def mutate(cls, __, info, email, adminemail, **args):
        # Validate the adminemail
        if not confirmEmail.isValid(adminemail):
            return deactivateAppUser(
                error=True, 
                message=f"{email} is not a valid admin email! Kindly use a valid email address.",
                success_msg=False
            )

        # Query the user by email
        existing_users  = UserObject.get_query(info)
        adminUser       = existing_users.filter(UserModel.email == adminemail).first()
        
        if not adminUser:
            return deactivateAppUser(
                error=True,
                message=f"This email {email} does not belong to the admin group. You're not allowed to deactivate another user.",
                success_msg=False
            )
        
        # Validate the email
        if not confirmEmail.isValid(email):
            return deactivateAppUser(
                error=True,
                message=f"{email} is not a valid email! Kindly use a valid email address.",
                success_msg=False
            )

        # Query the user by email
        existing_users = UserObject.get_query(info)
        thisUser = existing_users.filter(UserModel.email == email).first()

        if not thisUser:
            return deactivateAppUser(
                error=True,
                message=f"No user found with email {email}. Please check the email.",
                success_msg=False
            )

        if not thisUser.active:
            return deactivateAppUser(
                error=False,
                message=f"The user with email {email} is already deactivated.",
                success_msg=True
            )

        # Deactivate the user
        try:
            thisUser.active = False
            db.session.commit()
            message = f"User with email {email} has been successfully deactivated!"
            return deactivateAppUser(
                error=False,
                message=message,
                success_msg=True
            )
        except Exception as e:
            db.session.rollback()
            return deactivateAppUser(
                error=True,
                message=f"Deactivation failed due to an error: {str(e)}",
                success_msg=False
            )


class validateAppUser(graphene.Mutation):
    error       = graphene.Boolean()
    success_msg = graphene.Boolean()
    message     = graphene.String()

    class Arguments:
        email       = graphene.String(required=True)
        adminemail  = graphene.String(required=True)
        token       = graphene.String(required=True)

    @classmethod
    @mutation_jwt_required
    def mutate(cls, __, info, email, adminemail, **args):
        # Validate the adminemail
        if not confirmEmail.isValid(adminemail):
            return validateAppUser(
                error=True, 
                message=f"{email} is not a valid admin email! Kindly use a valid email address.",
                success_msg=False
            )

        # Query the user by email
        existing_users  = UserObject.get_query(info)
        adminUser       = existing_users.filter(UserModel.email == adminemail).first()
        
        if not adminUser:
            return validateAppUser(
                error=True,
                message=f"This email {email} does not belong to the admin group. You're not allowed to validate another user.",
                success_msg=False
            )
        
        # Validate the email
        if not confirmEmail.isValid(email):
            return validateAppUser(
                error=True, 
                message=f"{email} is not a valid email! Kindly use a valid email address.",
                success_msg=False
            )

        # Query the user by email
        existing_users = UserObject.get_query(info)
        thisUser = existing_users.filter(UserModel.email == email).first()

        if not thisUser:
            return validateAppUser(
                error=True,
                message=f"No user found with email {email}. Please check the email or register first.",
                success_msg=False
            )

        if thisUser.is_valid_client:
            return validateAppUser(
                error=False,
                message=f"The user with email {email} is already validated.",
                success_msg=True
            )

        # Activate the user
        try:
            thisUser.is_valid_client = True
            db.session.commit()
            message = f"User with email {email} has been successfully validated!"
            return activateAppUser(
                error=False,
                message=message,
                success_msg=True
            )
        except Exception as e:
            db.session.rollback()
            return validateAppUser(
                error=True,
                message=f"Activation failed due to an error: {str(e)}",
                success_msg=False
            )

