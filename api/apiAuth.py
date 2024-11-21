
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
        #enroldata   = enrolAppUserInput()
        enrolmentappuserinput               = enrolmentAppUserInput(required=True)

    error       = graphene.Boolean()
    success_msg = graphene.Boolean()
    message     = graphene.String()

    @classmethod
    def mutate(cls, __, info, enrolmentappuserinput, **args):
    #def mutate(cls, __, info, email, password, password_confirm, dirphoneNumber, dirlastName, dirfirstname, registeredBusinessname, city, state, **args):
        email                   = enrolmentappuserinput.email
        password                = enrolmentappuserinput.password
        password_confirm        = enrolmentappuserinput.password_confirm 

        
        if not confirmEmail.isValid(email):
            return enrolAppUser(
                error   = True, 
                message = "{email} not a valid email! Kindly use a valid email address",
                success_msg = False
            )
                            
        if password != password_confirm:
            return enrolAppUser(
                error       = True,
                message     = "Password mismatch! Ensure same for password and password_confirm",
                success_msg = False
            )

        existing_users  = UserObject.get_query(info)
        thisUser        = existing_users.filter(UserModel.email==email).first()

        if thisUser:
            error       = True #f"User with this email address, {email} exists"
            message     = "App user with this email address, {email} exists. \n You might want to reset your password if you're unable to connect"
            success_msg = False

        fs_uniquifierbuild = generateUniqueString('uniquifier')
        fs_uniquifier       = fs_uniquifierbuild.generateString()
        new_user = User(
                        email                   = email,
                        password                = generate_password_hash(password, method="sha256"),
                        #password                = generate_password_hash(password, method="scrypt"),
                        fs_uniquifier           = fs_uniquifier
                    )

        try:
            db.session.add(new_user)
            db.session.commit()
            db.session.close()
            error       = False
            message     = f"Registration for {email}, successful! "
            success_msg = True

        except IntegrityError as e:
            return enrolAppUser(
                error       = True,
                message     = f"Registration failed! {e.orig}",
                success_msg = False
            )
        
        except:
            return enrolAppUser(
                error       = True,
                message     = f"Registration failed!",
                success_msg = False
            )
        
        return enrolAppUser(
                            error       = error,
                            message     = message,
                            success_msg = success_msg
                    )


class activateAppUser(graphene.Mutation):
    error       = graphene.Boolean()
    success_msg = graphene.Boolean()
    message     = graphene.String()

    class Arguments:
        email       = graphene.String(required=True)

    @classmethod
    def mutate(cls, __, info, email, **args):
        # Validate the email
        if not confirmEmail.isValid(email):
            return activateAppUser(
                error=True, 
                message=f"{email} is not a valid email! Kindly use a valid email address.",
                success_msg=False
            )

        # Query the user by email
        existing_users = UserObject.get_query(info)
        thisUser = existing_users.filter(UserModel.email == email).first()

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

