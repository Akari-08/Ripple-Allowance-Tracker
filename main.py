# Import necessary modules from KivyMD and Kivy for window management and app structure
from kivymd.app import MDApp
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager

# Import screen modules that manage various parts of the app (Firebase, Signup, etc.)
from firebase.firebasescreen import FirebaseScreen
from firebase.signupscreen import Signup
from firebase.emailsigninscreen import EmailLogin
from firebase.emailsignupscreen import EmailSignup
from firebase.welcomescreen import WelcomeScreen
from firebase.userdetailsscreen import UserDetails
from firebase.parentchildscreen import ParentChild
from dashboardParent.parentdashboard import ParentDashboard
from dashboardChild.childdashboard import ChildDashboard

# Set the window size for the app (optional, as it can auto scale)
Window.size = (360, 782)  # Or leave it for auto scaling

# Define the main application class that inherits from MDApp (Material Design App)
class MainApp(MDApp):
    # Define placeholders for user data and database connection
    user = []  # List to hold user data
    user_info = []  # List for storing additional user information
    db = None  # Placeholder for database connection (to be defined later)
    
    
# The run() method is used to start the app when it's executed, this is done below
if __name__ == "__main__":  # Check if this script is being run directly
    # Instantiate and run the MainApp class
    MainApp().run()