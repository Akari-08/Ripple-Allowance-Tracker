import kivy  # Import the Kivy library for building cross-platform graphical applications
from kivy.lang import Builder  # Import Builder module for defining user interfaces in KV language
from kivy.uix.screenmanager import Screen  # Import the Screen class for managing multiple screens in Kivy apps
from kivymd.uix.snackbar import MDSnackbar  # Import MDSnackbar from KivyMD for showing snackbars (temporary notifications)
from kivymd.uix.label import MDLabel  # Import MDLabel from KivyMD for displaying labeled text with Material Design style
# Import JsonStore for storing data in a JSON file for local storage
from kivy.storage.jsonstore import JsonStore  
from kivy.clock import Clock  # Import Clock for scheduling tasks

# multiple screens in Kivy apps
from firebase.welcomescreen import WelcomeScreen
from firebase.emailsignupscreen import EmailSignup
from firebase.emailsigninscreen import EmailLogin
from firebase.userdetailsscreen import UserDetails
from firebase.parentchildscreen import ParentChild
from dashboardParent.parentdashboard import ParentDashboard
from dashboardChild.childdashboard import ChildDashboard
from firebase.childparentcode import ChildCode

import firebase
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import email_validator
from zxcvbn import zxcvbn
# Module for generating random numbers and making random selections
import random  
# Module for working with string operations, such as generating random characters
import string  


# Configuration dictionary containing Firebase credentials and settings
config = {
    "apiKey": "***************************************",
    "authDomain": "************.firebaseapp.com",
    "databaseURL": "https://************-default-rtdb.firebaseio.com/",
    "storageBucket": "************.appspot.com",
    "serviceAccount": r'*************************************.json'
}

# Initialize the Firebase application using the provided config
firebase = pyrebase.initialize_app(config)

# Initialize Firebase authentication
auth = firebase.auth()

# Initialize Firebase Admin SDK with the service account credentials
cred = credentials.Certificate(r'*************************************.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore client for database interaction
db = firestore.client()

# Create a JSON storage object to save and retrieve user data
store = JsonStore('user_data.json')  

# Load all the necessary kv files
Builder.load_file("firebase/welcomescreen.kv")
Builder.load_file("firebase/emailsignupscreen.kv")
Builder.load_file("firebase/emailsigninscreen.kv")
Builder.load_file("firebase/signupscreen.kv")
Builder.load_file("firebase/firebasescreen.kv")
Builder.load_file("firebase/userdetailsscreen.kv")
Builder.load_file("firebase/parentchildscreen.kv")
Builder.load_file("firebase/childparentcode.kv")

class FirebaseScreen(Screen):
    def __init__(self, **kwargs):
        """
        Initialize the FirebaseScreen class.

        This method sets up the screen by calling the parent class's constructor and 
        initializing user-related attributes. If user data exists in local storage, 
        it retrieves and loads the data. Otherwise, it initializes default values.

        Args:
            **kwargs: Additional keyword arguments passed to the parent class.
        """
        # Call the parent class's constructor to initialize the screen
        super(FirebaseScreen, self).__init__(**kwargs)
        
        # Check if user data exists in local storage
        if store.exists('user'):
            # Retrieve stored user data
            user_data = store.get('user')
            
            # Load user details from storage
            self.localId = user_data['localId']  # Unique Firebase user ID
            self.email = user_data['email']  # User's email address
            self.role = user_data.get('role', '')  # User's role (parent/child)
            self.loggedIn = user_data.get('loggedIn', False)  # Login status
            self.user = user_data.get('user', {})  # User data from Firebase
            self.parent_code = user_data.get('parent_code', '')  # Parent code for parent users
            
            # Schedule a delayed call to continue to the dashboard after 0.1 seconds
            Clock.schedule_once(self.delayed_continue_to_dashboard_JSON, 0.1)
        else:
            # Initialize user-related attributes with default values
            self.localId = ''  # Default Firebase user ID
            self.email = ''  # Default email address
            self.role = ''  # Default role
            self.parent_code = ''  # Default parent code
            self.loggedIn = False  # User is not logged in by default

    def delayed_continue_to_dashboard_JSON(self, dt):
        """
        Delayed call to continue_to_dashboard_JSON to ensure the ScreenManager is fully initialized.
        This function is typically used in scenarios where you need to delay a screen transition
        or other UI action until the screen has been fully loaded or initialized, preventing
        errors caused by accessing uninitialized elements.
        """
        self.continue_to_dashboard_JSON()

    
    def on_kv_post(self, base_widget):
        """
        Called after the widget has been added to the widget tree.

        This method ensures that the widget is fully initialized and accessible in the tree.
        It retrieves user data from Firestore and updates the parent widget with the retrieved data.

        Args:
            base_widget: The base widget to which this widget has been added.
        """
        # Now that the widget is in the tree, you can safely access self.parent
        if self.parent and self.localId:
            # Get a reference to the user's document in Firestore
            doc_ref = db.collection('Users').document(self.localId)

            # Retrieve user data from Firestore and convert it to a dictionary
            doc = doc_ref.get().to_dict()
            self.parent.user_info = doc  # Update parent's user_info with Firestore data
            self.parent.db = db  # Pass the Firestore database reference to the parent
            self.parent.user = self.user  # Update parent's user attribute
        
    
    def print_password(self, password):
        """
        Evaluate and update the password strength based on the provided password.

        This method checks the strength of the password using `check_password_strength`
        and updates the password strength bar accordingly.

        Args:
            password (str): The password to evaluate.
        """
        # print(password)  # This line is commented out and does nothing
        strength = self.check_password_strength(password)  # Check the password strength
        # print(strength)  # This line is commented out and does nothing
        
        # Update the password strength bar based on the strength value
        if strength == 0:
            self.update_password_strength_bar(0)  # Empty password
        elif strength == 1 or strength == 2:
            self.update_password_strength_bar(1)  # Weak password
        elif strength == 3:
            self.update_password_strength_bar(2)  # Medium password
        elif strength == 4:
            self.update_password_strength_bar(3)  # Strong password
        elif strength == 5:
            self.update_password_strength_bar(4)  # Very Strong password
        
    def check_password_strength(self, password):
        """
        Evaluate the strength of a password using the zxcvbn library.

        This method checks the strength of the provided password. If the password is empty,
        it returns 0. Otherwise, it uses the zxcvbn library to calculate the password's
        strength score and returns the score incremented by 1. If an error occurs during
        the process, it prints the error and returns 0.

        Args:
            password (str): The password to evaluate.

        Returns:
            int: The password strength score (0 for empty, 1-5 for weak to very strong).
        """
        # Check if the password is empty
        if not password:
            return 0  # Return 0 for an empty password
        
        try:
            # Import the zxcvbn library for password strength analysis
            from zxcvbn import zxcvbn
            # Calculate the password strength score and return it incremented by 1
            return zxcvbn(password)['score'] + 1
        except Exception as e:
            # Handle any exceptions that occur during the process
            print(f"Error analyzing password: {e}")  # Print the error message
            return 0  # Return 0 in case of an error

    # def update_password_strength_bar(self, strength_level):

        # Access the canvas Color instructions by iterating through children
        print(self.ids)
        canvas = self.ids.password_strength_bar.canvas
        
        # Default colors for each strength level (weak, medium, strong, very strong)
        color_map = {
            1: (1, 0.3058823529411765, 0.38823529411764707, 1),  # Weak (red)
            2: (1, 0.7490196078431373, 0.0, 1),  # Medium (yellow)
            3: (0.17254901960784313, 0.8666666666666667, 0.9137254901960784, 1),  # Strong (green)
            4: (0.17254901960784313, 0.36470588235294116, 0.8627450980392157, 1),  # Very Strong (blue)
            0: (0.20784313725490197, 0.20784313725490197, 0.25882352941176473, 1)  # Grey for empty password
        }
        
        # Update the color for the appropriate bar
        bar_colors = list(canvas.children)

        # Only interact with 'Color' instructions, ignoring other instructions like 'BindTexture'
        bar_colors = [child for child in email_signup_instance.ids.password_strength_bar.canvas.children if isinstance(child, kivy.graphics.Color)]

        # Apply grey color to all bars if the password is empty
        if strength_level == 0:
            for bar_color in bar_colors:
                bar_color.rgba = color_map[0]
        elif strength_level == 1:
            bar_colors[0].rgba = color_map[1]  # Set color for weak
            bar_colors[1].rgba = (0.20784313725490197, 0.20784313725490197, 0.25882352941176473, 1)  # Grey for the other bars
            bar_colors[2].rgba = (0.20784313725490197, 0.20784313725490197, 0.25882352941176473, 1)
            bar_colors[3].rgba = (0.20784313725490197, 0.20784313725490197, 0.25882352941176473, 1)
        elif strength_level == 2:
            bar_colors[0].rgba = color_map[2]  # Set color for medium
            bar_colors[1].rgba = color_map[2]  # Show medium bar
            bar_colors[2].rgba = (0.20784313725490197, 0.20784313725490197, 0.25882352941176473, 1)  # Grey for the next bars
            bar_colors[3].rgba = (0.20784313725490197, 0.20784313725490197, 0.25882352941176473, 1)
        elif strength_level == 3:
            bar_colors[0].rgba = color_map[3]  # Set color for strong
            bar_colors[1].rgba = color_map[3]  # Show medium bar
            bar_colors[2].rgba = color_map[3]  # Show strong bar
            bar_colors[3].rgba = (0.20784313725490197, 0.20784313725490197, 0.25882352941176473, 1) # Grey for the last bar
        elif strength_level == 4:
            bar_colors[0].rgba = color_map[4]  # Set color for very strong
            bar_colors[1].rgba = color_map[4]  # Show medium bar
            bar_colors[2].rgba = color_map[4]  # Show strong bar
            bar_colors[3].rgba = color_map[4]  # Show very strong bar
            
        self.ids.password_strength_bar.canvas.ask_update()

    def update_password_strength_bar(self, strength_level):
        pass

    def generate_random_code(self, length):
        """Generate a random alphanumeric code of the specified length."""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    def fetch_parent_codes(self):
        """
        Retrieves all parent codes from the Firestore database.

        This function:
        1. Connects to the Firestore collection 'Users'.
        2. Extracts the 'parent_code' field from each document.
        3. Returns a list of all valid parent codes.
        4. Handles exceptions and logs errors if Firestore retrieval fails.

        Returns:
            list: A list containing all parent codes found in the Firestore database.
        """
        try:
            # Fetch all documents from your Firestore collection
            docs = db.collection('Users').stream()  
            # Create an empty list to store parent codes
            PCodes = []
            
            # Iterate through the documents and extract parent codes
            for doc in docs:
                parent_code = doc.to_dict().get('parent_code')
                if parent_code:
                    PCodes.append(parent_code)
            # Display the list of parent codes in the label
            return PCodes
        except Exception as e:
            print(f"Error fetching parent codes: {e}")        

    def signup_user(self, email, password):
        """
        Handles user signup by validating email, checking password strength, 
        creating a new user, and sending an email verification.

        This function ensures that:
        1. The email is in a valid format.
        2. The password meets the required strength criteria.
        3. The user is successfully created in Firebase Authentication.
        4. A verification email is sent after account creation.
        5. The user is redirected to the 'user_details' screen on success.

        Parameters:
            email (str): The email address entered by the user.
            password (str): The password entered by the user.
        """
        try:
            # Validate email format
            email_validator.validate_email(email)
        except Exception as e:
            # If email is invalid, show a Snackbar with an error message
            MDSnackbar(
                MDLabel(text="Invalid email"),  # Message indicating invalid email
                auto_dismiss=True,
            ).open()
            return

        try:
            # Check password strength, if too weak, show a Snackbar
            if self.check_password_strength(password) < 2:
                MDSnackbar(
                    MDLabel(text="Password is too weak"),  # Message indicating weak password
                    auto_dismiss=True,
                ).open()
                return
        except Exception as e:
            # Show any exception that occurs during password strength check
            MDSnackbar(
                MDLabel(text=str(e)),  # Show the error message
                auto_dismiss=True,
            ).open()

        try:
            # Attempt to create a new user with the given email and password
            user = auth.create_user_with_email_and_password(email, password)
            # Send an email verification to the newly created user
            test = auth.send_email_verification(user['idToken'])
            # If successful, call the signup success function
            self.signup_success(user)
            # Switch to the user details screen after successful signup
            self.ids.screen_manager.current = 'user_details'
        except Exception as e:
            # Handle any errors that occur during user creation or email verification
            MDSnackbar(
                MDLabel(text=f"{e}"),  # Display the error message in the Snackbar
                snackbar_x="10dp",
                snackbar_y="10dp",
                auto_dismiss=True,
            ).open()  
            
    def login_user(self, email, password):
        """
        Handles user login by validating email format and authenticating 
        the user with Firebase Authentication.

        This function ensures that:
        1. The email format is valid.
        2. The user is authenticated using Firebase Authentication.
        3. If login is successful, it calls the login_success function.
        4. If login fails, an error message is displayed.

        Parameters:
            email (str): The email address entered by the user.
            password (str): The password entered by the user.
        """
        try:
            # Validate email format
            email_validator.validate_email(email)
        except Exception as e:
            # If email is invalid, show an error message in a snackbar
            MDSnackbar(
                MDLabel(text="Invalid email"),  # Display error message
                auto_dismiss=True,  # Dismiss snackbar automatically
            ).open()
        try:
            # Attempt to sign in the user with provided email and password
            user = auth.sign_in_with_email_and_password(email, password)

            self.login_success(user)  # Proceed to login success function
        except Exception as e:
            # Handle any errors (e.g., email doesn't exist, wrong password)
            MDSnackbar(
                MDLabel(text=f"{e}"),  # Display error message in the snackbar
                auto_dismiss=True,  # Dismiss snackbar automatically
            ).open()
            
    def parent_role(self):
        """
        Assigns the 'parent' role to the currently logged-in user and generates a unique parent code.  
        If the user document exists in Firestore, it updates the role and assigns a unique parent code.  
        If the document does not exist, it creates a new document with the required details.  

        Steps:
        1. Check if the user is logged in and has a valid localId.
        2. Fetch all existing parent codes to ensure uniqueness.
        3. If the user's document exists, update it with the role and a unique parent code.
        4. If the document does not exist, create a new one with the same details.
        5. Handle various exceptions related to Firestore operations.
        
        Raises:
            firebase_admin.exceptions.NotFound: If the user document is not found.
            firebase_admin.exceptions.PermissionDenied: If access is denied due to permission issues.
            Exception: Catches and handles any other unexpected errors.
        """
        if self.localId and self.loggedIn:
            try:
                # Set the user's role as 'parent'
                self.role = 'parent'
                # Get reference to the user's document in Firestore
                doc_ref = db.collection('Users').document(self.localId)
                doc_snapshot = doc_ref.get()

                if doc_snapshot.exists:
                    # If the document exists, check for a unique parent code
                    
                    # Fetch existing parent codes to ensure uniqueness
                    PCodes = self.fetch_parent_codes()
                    
                    # Keep generating a new code if the current code already exists
                    while parent_code in PCodes:
                        parent_code = self.generate_random_code(6)
                    
                    # Update the document with the role and unique parent code
                    doc_ref.update({'role': 'parent', 'parent_code': parent_code})
                    self.parent_code = parent_code
                    self.save_user_data(self.user)
                    # Proceed to the dashboard
                    self.continue_to_dashboard()
                else:

                    # Fetch existing parent codes to ensure uniqueness
                    PCodes = self.fetch_parent_codes()
                    
                    # Keep generating a new code if the current code already exists
                    while parent_code in PCodes:
                        parent_code = self.generate_random_code(6)

                    # Create the document and set the role and parent code
                    doc_ref.set({'role': 'parent', 'parent_code': parent_code})
                    # Proceed to the dashboard
                    self.parent_code = parent_code
                    self.save_user_data(self.user)
                    self.continue_to_dashboard()
            except Exception as e:
                # Handle any other unexpected exceptions
                MDSnackbar(
                    MDLabel(text="An unexpected error occurred."),
                    auto_dismiss=True,
                ).open()
                return
        else:
            print("Please enter a User ID.")

    def child_role(self):
        """
        Assign the 'child' role to the current user and update their role in Firestore.

        This method ensures the user is logged in and has a valid `localId`. If so, it assigns
        the 'child' role to the user, updates or creates their document in Firestore, and
        navigates to the appropriate dashboard. If an error occurs, it displays a snackbar
        notification. If no user ID is provided, it prompts the user to enter one.
        """
        # Ensure the user is logged in and has a valid localId
        if self.localId and self.loggedIn:
            try:
                # Assign the role as 'child' for the user
                self.role = 'child'
                # Reference the user's document in the Firestore 'Users' collection
                doc_ref = db.collection('Users').document(self.localId)
                doc_snapshot = doc_ref.get()  # Retrieve the document snapshot
                if doc_snapshot.exists:
                    # If the document already exists, update the user's role to 'child'
                    doc_ref.update({'role': 'child'})
                else:
                    # If the document does not exist, create a new one with the role 'child'
                    doc_ref.set({'role': 'child'})
                self.save_user_data(self.user)  # Save updated user data
                # Proceed to the appropriate dashboard after updating/creating the role
                self.ids.screen_manager.current = 'child_code'  # Navigate to the 'child_code' screen
            except Exception as e:
                # Catch any unexpected errors
                MDSnackbar(
                    MDLabel(text="An unexpected error occurred."),  # Display error message
                    auto_dismiss=True,
                ).open()
                return
        else:
            # If no user ID is provided, prompt the user
            print("Please enter a User ID.")  # Debugging statement
    
    def login_success(self, user):
        """
        Handle actions after a successful user login.

        This method stores user information in instance variables, retrieves additional
        user data from Firestore, and navigates to the appropriate dashboard based on
        the user's role. It also saves the user data to local storage.

        Args:
            user (dict): A dictionary containing user information from Firebase.
        """
        # Store user information in the instance variables
        self.user = user
        self.localId = user['localId']  # Unique ID assigned by Firebase
        self.email = user['email']  # Store the user's email
        self.loggedIn = True  # Mark the user as logged in
        
        # Get a reference to the user's document in Firestore
        doc_ref = db.collection('Users').document(self.localId)
        
        # Retrieve user data from Firestore and convert it to a dictionary
        doc = doc_ref.get().to_dict()
        
        # Store a reference to the Firestore database in the parent instance
        self.parent.db = db

        # Store the user information in the parent instance for easy access
        self.parent.user_info = doc
        # Extract the user's role (parent/child) from Firestore data
        self.role = doc['role']
        self.parent_code = doc.get('parent_code', '')  # Extract the parent code if it exists
        self.save_user_data(user)  # Save user data to JsonStore
        
        # Proceed to the appropriate dashboard based on the user's role
        self.continue_to_dashboard()
    
    def signup_success(self, user):
        """
        Handle actions after a successful user signup.

        This method stores user information in instance variables, saves the user data to
        local storage, and updates or creates the user's document in Firestore. If the user
        is successfully processed, it navigates to the 'user_details' screen. If any errors
        occur, appropriate error messages are displayed.

        Args:
            user (dict): A dictionary containing user information from Firebase.
        """
        # Store user information in instance variables
        self.user = user
        self.localId = user['localId']  # Unique ID assigned by Firebase
        self.email = user['email']  # Store the user's email
        self.loggedIn = True  # Mark the user as logged in
        self.save_user_data(user)  # Save user data to JsonStore

        # Check if the user ID is valid and the user is logged in
        if self.localId and self.loggedIn:
            try:
                # Get reference to the user's document in Firestore
                doc_ref = db.collection('Users').document(self.localId)
                doc_snapshot = doc_ref.get()  # Retrieve the document snapshot
                
                # Update or create the user's document in Firestore
                if doc_snapshot.exists:
                    # If the document exists, update the email and set balance to 0
                    doc_ref.update({'email': self.email, 'balance': 0})
                else:
                    # If the document does not exist, create it with email and balance
                    doc_ref.set({'email': self.email, 'balance': 0})
            except firebase_admin.exceptions.NotFound as e:
                # Handle the case where the user is not found in Firestore
                MDSnackbar(
                    MDLabel(text="User not found."),  # Display error message
                    auto_dismiss=True,
                ).open()
                return
            except firebase_admin.exceptions.PermissionDenied as e:
                # Handle the case where permission is denied to access Firestore
                MDSnackbar(
                    MDLabel(text="Permission denied."),  # Display error message
                    auto_dismiss=True,
                ).open()
                return
            except Exception as e:
                # Handle any other unexpected errors
                MDSnackbar(
                    MDLabel(text="An unexpected error occurred."),  # Display error message
                    auto_dismiss=True,
                ).open()
                return
        else:
            # If no user ID is provided, prompt the user
            print("Please enter a User ID.")  # Debugging statement

        # Navigate to the 'user_details' screen
        self.ids.screen_manager.current = 'user_details'
        
    def update_names(self, first, last):
        """
        Update the user's first and last name in Firestore.

        This method updates or sets the user's first and last name in Firestore if the user
        is logged in and has a valid `localId`. If the operation is successful, it navigates
        to the 'parent_child' screen. If any errors occur, appropriate error messages are
        displayed.

        Args:
            first (str): The user's first name.
            last (str): The user's last name.
        """
        # Check if the user is logged in and has a valid localId
        if self.localId and self.loggedIn:
            try:
                # Get reference to the user's document in Firestore
                doc_ref = db.collection('Users').document(self.localId)
                doc_snapshot = doc_ref.get()  # Retrieve the document snapshot
                self.first = first  # Store the first name in the instance
                self.last = last  # Store the last name in the instance

                # Check if the document exists in Firestore
                if doc_snapshot.exists:
                    # If the document exists, update the first and last name
                    doc_ref.update({'first': first, 'last': last})
                    self.ids.screen_manager.current = 'parent_child'  # Navigate to 'parent_child' screen
                else:
                    # If the document does not exist, create it with the first and last name
                    doc_ref.set({'first': first, 'last': last})
                    self.ids.screen_manager.current = 'parent_child'  # Navigate to 'parent_child' screen
            except firebase_admin.exceptions.NotFound as e:
                # Handle the case where the user is not found in Firestore
                MDSnackbar(
                    MDLabel(text="User not found."),  # Display error message
                    auto_dismiss=True,
                ).open()
                return
            except firebase_admin.exceptions.PermissionDenied as e:
                # Handle the case where permission is denied to access Firestore
                MDSnackbar(
                    MDLabel(text="Permission denied."),  # Display error message
                    auto_dismiss=True,
                ).open()
                return
            except Exception as e:
                # Handle any other unexpected errors
                MDSnackbar(
                    MDLabel(text="An unexpected error occurred."),  # Display error message
                    auto_dismiss=True,
                ).open()
                return
        else:
            # If no user ID is provided, prompt the user
            print("Please enter a User ID.")  # Debugging statement
            
    def continue_to_dashboard(self):
        """
        Proceed to the appropriate dashboard based on the user's role.
        """
        if self.loggedIn and self.localId:
            self.parent.user = self.user
            if self.role == 'parent':
                self.parent.current = 'dashboard_parent'  # Switch to Dashboard screen
            elif self.role == 'child':
                self.parent.current = 'dashboard_child'  # Switch to Dashboard screen
                
    def continue_to_dashboard_JSON(self):
        """
        Proceed to the appropriate dashboard based on the user's role.
        """
        if self.loggedIn and self.localId:
            if self.role == 'parent':
                # Check if the 'dashboard_parent' screen exists
                if 'dashboard_parent' in self.parent.screen_names:
                    self.parent.current = 'dashboard_parent'  # Switch to Dashboard screen
                else:
                    print("Error: 'dashboard_parent' screen not found in ScreenManager.")
            elif self.role == 'child':
                # Check if the 'dashboard_child' screen exists
                if 'dashboard_child' in self.parent.screen_names:
                    self.parent.current = 'dashboard_child'  # Switch to Dashboard screen
                else:
                    print("Error: 'dashboard_child' screen not found in ScreenManager.")

            store.put('auth', localId=self.localId)  # Saves user ID
        

    def save_user_data(self, user):
        """Save user details to a JSON file."""
        store.put(
            'user',  # Store data under the key 'user'
            user=user,  # Store the complete user dictionary
            localId=user.get('localId', ''),  # Save the user’s unique ID (default to empty if not found)
            email=user.get('email', ''),  # Save the user’s email (default to empty if not found)
            role=self.role,  # Store the user’s role (e.g., parent/child)
            parent_code=self.parent_code,  # Store the parent code if applicable
            loggedIn=True  # Mark the user as logged in
        )
        
    def enter_parent_code(self, code):
        """
        Validate and process a parent code entered by the user.

        This method checks if the provided parent code is valid (6 characters long) and
        exists in Firestore. If the code is valid, it updates the user's role to 'child',
        saves the parent code, and navigates to the appropriate dashboard. If the code is
        invalid or an error occurs, an error message is displayed.

        Args:
            code (str): The parent code entered by the user.
        """
        # Check if the parent code is exactly 6 characters long
        if len(code) != 6:
            # If the code is invalid, display an error message
            MDSnackbar(
                MDLabel(text="Invalid parent code"),  # Display error message
                auto_dismiss=True,  # Dismiss snackbar automatically
            ).open()
            return

        try:
            # Fetch all parent codes from Firestore
            PCodes = self.fetch_parent_codes()
            # Check if the entered code exists in the list of valid parent codes
            if code in PCodes:
                # If the code is valid, update the user's role to 'child'
                self.role = 'child'
                self.parent_code = code  # Save the parent code
                self.save_user_data(self.user)  # Save updated user data
                # search through all firebase users to find the parent code to find local id
                docs = db.collection('Users').stream()
                for doc in docs:
                    if doc.to_dict().get('parent_code') == code:
                        doc_ref = db.collection('Users').document(doc.id)
                        children_update = []
                        current_children = doc.to_dict().get('Children', []) # Get existing children, or [] if none
                        children_update.append(current_children)
                        current_children.append(self.localId)             # Append new child
                        doc_ref.update({'Children': current_children})    # Update the whole field
                        
                self.continue_to_dashboard()  # Navigate to the appropriate dashboard
            else:
                # If the code is invalid, display an error message
                MDSnackbar(
                    MDLabel(text="Invalid parent code"),  # Display error message
                    auto_dismiss=True,  # Dismiss snackbar automatically
                ).open()
        except Exception as e:
            # Handle any unexpected errors
            print(e)  # Print the error for debugging






