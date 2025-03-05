# Import necessary Kivy and KivyMD modules
import kivy
from kivy.lang import Builder  # Import Builder from kivy.lang to load KV files
from kivy.uix.screenmanager import Screen  # Import Screen for creating screens
from dashboardParent.parentchildrenscreen import ParentChildren  # Import custom ParentChildren screen
from kivy.uix.scrollview import ScrollView  # Import ScrollView for scrollable content
from kivy.uix.gridlayout import GridLayout  # Import GridLayout for grid-based layouts
from kivy.uix.relativelayout import RelativeLayout  # Import RelativeLayout for relative positioning
from kivy.uix.boxlayout import BoxLayout  # Import BoxLayout for box-based layouts
from kivy.uix.label import Label  # Import Label for displaying text
from kivymd.uix.button import MDFloatingActionButton  # Import floating action button from KivyMD
from kivymd.uix.button import MDFlatButton  # Import flat button from KivyMD
from kivymd.uix.dialog import MDDialog  # Import dialog box from KivyMD
from kivy.uix.textinput import TextInput  # Import TextInput for user input
from kivy.uix.button import Button  # Import standard Button widget
from kivymd.uix.snackbar import MDSnackbar  # Import Snackbar for notifications
from kivymd.uix.label import MDLabel  # Import MDLabel for styled text labels

import json

import firebase
import pyrebase

# Load all the necessary kv files
Builder.load_file("dashboardParent/parentchildrenscreen.kv")
Builder.load_file("dashboardParent/parentdashboard.kv")

# Define global variables
user_info_temp = {}
db_temp = None
temp = True  # Define temp in the global scope
children_loaded = False

text_Color1 = 'ffffff'
text_Color2 = 'white'

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

from kivy.properties import StringProperty
from kivy.properties import NumericProperty

class NameCard(BoxLayout):
    first = StringProperty('')  # Define first as a StringProperty
    last = StringProperty('')   # Define last as a StringProperty
    balance = StringProperty('')  # Define balance as a NumericProperty

    def __init__(self, first, last, balance, **kwargs):
        """
        Initialize the class instance with user details.

        This method sets the first name, last name, and balance for the user.
        The balance is formatted as a string prefixed with a dollar sign.

        Args:
            first (str): The user's first name.
            last (str): The user's last name.
            balance (int or float): The user's balance.
            **kwargs: Additional keyword arguments passed to the parent class.
        """
        # Call the parent class's __init__ method
        super().__init__(**kwargs)

        # Set the first name
        self.first = first  # Store the first name in the instance
        # Set the last name
        self.last = last  # Store the last name in the instance
        # Format the balance as a string prefixed with a dollar sign
        balance = '$' + str(balance)
        # Set the formatted balance
        self.balance = balance  # Store the balance in the instance
        
class TransactionCard1(BoxLayout):
    amount = StringProperty('')  # Define first as a StringProperty
    category = StringProperty('')  # Define second as a StringProperty
    date = StringProperty('')  # Define second as a StringProperty

    def __init__(self, amount, category, date, **kwargs):
        """
        Initialize the class instance with transaction details.

        This method sets the amount, category, and date for a transaction.

        Args:
            amount (float or int): The amount of the transaction.
            category (str): The category of the transaction (e.g., "Food", "Transport").
            date (str): The date of the transaction.
            **kwargs: Additional keyword arguments passed to the parent class.
        """
        # Call the parent class's __init__ method
        super().__init__(**kwargs)

        # Set the transaction amount
        self.amount = amount  # Store the amount in the instance
        # Set the transaction category
        self.category = category  # Store the category in the instance
        # Set the transaction date
        self.date = date  # Store the date in the instance

class ParentDashboard(Screen):
    def __init__(self, **kwargs):
        """
        Initialize the ParentDashboard class instance.

        This method sets up the initial state of the ParentDashboard class by initializing
        attributes such as user information, children data, and a reference to the database.

        Args:
            **kwargs: Additional keyword arguments passed to the parent class.
        """
        # Call the parent class's __init__ method
        super(ParentDashboard, self).__init__(**kwargs)

        # Initialize an empty list to store user information
        self.user = []  # List to hold user data
        # Initialize an empty list to store additional user information
        self.user_info = []  # List to hold additional user details
        # Initialize an empty list to store children IDs
        self.children_ids = []  # List to hold IDs of children associated with the user
        # Initialize a placeholder for the database reference
        self.db = None  # Will store a reference to the database
        # Initialize an empty dictionary to store children data
        self.children_data = {}  # Dictionary to hold data related to children
        
        
    def on_enter(self, *args):
        """
        Called when the screen is entered.
        """
        global children_loaded
        global imported_children

        super(ParentDashboard, self).on_enter(*args)
        self.initialize()  # Ensure the screen is initialized
        self.parent_variables()
        if not children_loaded:
            self.import_children()  # Load the children's names
            self.load_children()  # Display the children's names
            children_loaded = True

    def initialize(self):
        """
        Initialize the dashboard with user data and database connection.
        """
        global temp  # Declare temp as a global variable
        global user_info_temp  # Declare user_info_temp as a global variable
        global db_temp  # Declare db_temp as a global variable
        
        if self.parent:
            # Check if self.parent has the 'user_info' and 'db' attributes
            if hasattr(self.parent, 'user_info') and hasattr(self.parent, 'db'):
                # Access user info and database connection from the ScreenManager
                if temp:
                    try:
                        self.user_info = self.parent.user_info
                        self.db = self.parent.db
                        user_info_temp = self.user_info
                        db_temp = self.db
                        temp = False
                    except Exception as e:
                        print("Error accessing user info or database:", e)

            else:
                print("Error: 'user_info' or 'db' not found in ScreenManager.")
        else:
            print("Error: Parent not found in ParentDashboard.")
            
    def parent_variables(self):
        """
        Assign global variables to instance attributes.

        This method assigns the values of global variables `user_info_temp` and `db_temp`
        to the instance attributes `self.user_info` and `self.db`, respectively.
        This is typically used to share data across different parts of the application.
        """
        # Declare the use of global variables
        global user_info_temp  # Global variable holding temporary user information
        global db_temp  # Global variable holding a temporary database reference

        # Assign the global user information to the instance attribute
        self.user_info = user_info_temp  # Store user info in the instance
        # Assign the global database reference to the instance attribute
        self.db = db_temp  # Store the database reference in the instance

    def import_children(self):
        """
        Import and store children data associated with the current user.

        This method retrieves the list of children IDs from the user's information,
        fetches each child's data from Firestore, and stores it in the `children_data`
        dictionary for easy access.
        """
        # Iterate through the list of children IDs in the user's information
        for child in self.user_info['Children']:
            # Append each child ID to the `children_ids` list
            self.children_ids.append(child)

        # Iterate through the list of children IDs
        for child in self.children_ids:
            # Get a reference to the child's document in the Firestore 'Users' collection
            doc_ref = self.db.collection('Users').document(child)
            # Retrieve the document snapshot
            doc = doc_ref.get()
            # Convert the document to a dictionary and store it in `children_data` with the child ID as the key
            self.children_data[child] = doc.to_dict()
    
    def switch_to_parent_children(self):
        """
        Switch to the ParentChildren screen.

        This method changes the current screen of the screen manager to the
        'parent_children_screen', which is typically used to display and manage
        information related to the user's children.
        """
        # Change the current screen of the screen manager to 'parent_children_screen'
        self.manager.current = 'parent_children_screen'

    def load_children(self):
        """
        Loads and displays child account information using a scrollable layout.

        This function:
        - Prints debug information about stored child data.
        - Creates a floating action button for adding a new child.
        - Initializes a scrollable GridLayout to display NameCard widgets.
        - Dynamically adds NameCard widgets for each child in self.children_data.

        Components:
        - MDFloatingActionButton: A "+" button to add a new child.
        - ScrollView: Ensures the child list is scrollable.
        - GridLayout: Holds the dynamically created NameCard widgets.
        """

        # Remove existing scroll view and button layout if they exist
        if hasattr(self, 'scroll_view'):
            self.remove_widget(self.scroll_view)
        if hasattr(self, 'button_layout'):
            self.remove_widget(self.button_layout)

        # Create a layout for the floating action button
        button_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=100)
        # Create a floating action button with a "+" icon
        button = MDFloatingActionButton(
            icon="plus",  # Set the icon to a plus sign
            pos_hint={"center_x": 0.5, "center_y": 0.5},  # Center the button
            md_bg_color=(1, 0.4745098039215686, 0.4, 1),  # Set the button color
            on_release=self.add_child  # Bind the button to the add_child method
        )
        button_layout.add_widget(button)  # Add the button to the layout

        # Create a GridLayout to hold NameCard widgets
        layout = GridLayout(cols=1, size_hint_y=None)
        layout.clear_widgets()  # Clear any existing widgets
        # Make the layout scrollable by binding its height to its minimum height
        layout.bind(minimum_height=layout.setter('height'))

        # Create a ScrollView to contain the GridLayout
        self.scroll_view = ScrollView(size_hint=(1, 0.6), pos_hint={'center_x': 0.5, 'center_y': 0.60})
        self.scroll_view.add_widget(layout)  # Add the GridLayout to the ScrollView

        # Store the button layout and scroll view as instance attributes
        self.button_layout = button_layout
        # Add the ScrollView and button layout to the screen
        self.add_widget(self.scroll_view)
        self.add_widget(self.button_layout)

        # Iterate through the children data and create NameCard widgets
        for child_id, child in self.children_data.items():
            # Extract the first name, last name, and balance from the child data
            first = child['first']
            last = child['last']
            balance = child['balance']

            # Create a NameCard widget with the child's details
            name_card = NameCard(first=first, last=last, balance=balance)
            # Add the NameCard widget to the GridLayout
            layout.add_widget(name_card)

    def add_child(self, *args):
        """
        Displays a dialog containing the parent code associated with the user's account.
        
        This method retrieves the 'parent_code' from the user's information. If no code is found,
        it defaults to 'No Code Available'. A pop-up dialog is then created and displayed, showing
        the parent code with a dark background and an "OK" button to dismiss it.
        
        Parameters:
            *args: Additional arguments that may be passed (not used in this function).
        """

        # Retrieve the parent code from the user's stored information
        parent_code = self.user_info.get('parent_code', 'No Code Available')

        # Create and configure the dialog box
        self.dialog = MDDialog(
            title=f"[color={text_Color1}]Parent Code[/color]",  # Title with white text
            text=f"[color={text_Color1}]{parent_code}[/color]",  # Display the parent code in white
            md_bg_color=(0.1098, 0.1098, 0.1373, 1),  # Set the dialog background color           # Add a button to dismiss the dialog
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=f"{text_Color2}",  # Set button text color to white
                    on_release=lambda x: self.dialog.dismiss()  # Close dialog on button press
                )
            ]
        )

        # Open the dialog
        self.dialog.open()
        
    def child_popup(self, first, last):
        """
        Displays a dialog containing the child's first and last name.
        
        This method takes the first and last name of a child as arguments and creates a pop-up dialog
        displaying the child's name in white text on a dark background. The dialog includes an "OK"
        button to dismiss it.
        
        Parameters:
            first (str): The first name of the child.
            last (str): The last name of the child.
        """
        for user_id, user_data in self.children_data.items():
            if user_data.get('first') == first and user_data.get('last') == last:
                balance = user_data.get('balance')
                monthlyLimit = user_data.get('monthlyLimit')
                monthlyAllowance = user_data.get('monthlyAllowance')
                break  # Exit the loop once the user is found
        else:
            print("User not found")
            return
        # Create and configure the dialog box
        self.child_popup_dialog = MDDialog(
            title=f"[color={text_Color1}]{first} {last}[/color]",
            md_bg_color=(0.1098, 0.1098, 0.1373, 1),  # Dialog background color
            text=f"[color={text_Color1}]Balance: {balance}\nMonthly Limit: {monthlyLimit}\nMonthly Allowance: {monthlyAllowance}[/color]",
            buttons=[
                    MDFlatButton(
                        text="Edit Balance",
                        theme_text_color="Custom",
                        text_color=text_Color2,
                        on_release=lambda x: (self.edit_balance(first, last), self.child_popup_dialog.dismiss())
                    ),
                    MDFlatButton(
                        text="Edit Limit",
                        theme_text_color="Custom",
                        text_color=text_Color2,
                        on_release=lambda x: (self.edit_monthly_limit(first, last), self.child_popup_dialog.dismiss())
                    ),
                    MDFlatButton(
                        text="Edit Allowance",
                        theme_text_color="Custom",
                        text_color=text_Color2,
                        on_release=lambda x: (self.edit_monthly_allowance(first, last), self.child_popup_dialog.dismiss())
                    ),
                ]
        )

        self.child_popup_dialog.open()
        
    def edit_monthly_limit(self, first, last):
        """
        Open a dialog to edit the monthly limit for a specific child.

        This function:
        - Searches for the child in `self.children_data` using their first and last name.
        - Displays the current monthly limit in a dialog.
        - Allows the user to update the monthly limit using a TextInput and +/- buttons.
        - Provides "Cancel" and "Apply" buttons to dismiss the dialog or save changes.

        Args:
            first (str): The first name of the child.
            last (str): The last name of the child.
        """

        # Search for the child in `self.children_data`
        for user_id, user_data in self.children_data.items():
            if user_data.get('first') == first and user_data.get('last') == last:
                # Retrieve the current monthly limit for the child
                monthlyLimit = user_data.get('monthlyLimit')
                break  # Exit the loop once the child is found
        else:
            # If the child is not found, print a message
            print("User not found")

        # Create a custom MDDialog for editing the monthly limit
        self.dialog = MDDialog(
            title=f"[color={text_Color1}]Edit Monthly Limit[/color]",  # Title with custom text color
            type="custom",
            md_bg_color=(0.1098, 0.1098, 0.1373, 1),  # Set the dialog background color
            content_cls=BoxLayout(
                orientation="vertical",
                spacing=20,
                padding=20,
                size_hint_y=None,
                height=150
            ),
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    text_color=f"{text_Color2}",  # Set button text color
                    on_release=lambda x: self.dialog.dismiss()  # Close dialog on button press
                ),
                MDFlatButton(
                    text="Apply",
                    theme_text_color="Custom",
                    text_color=f"{text_Color2}",  # Set button text color
                    on_release=lambda x: self.apply_monthlyLimit_changes(self.monthlyLimit_input.text, first, last)  # Apply changes
                )
            ]
        )

        # Add content to the dialog
        content = self.dialog.content_cls

        # Display the child's name in the dialog
        name_label = Label(
            text=f"[color=ffffff]{first} {last}[/color]",  # White text with markup
            markup=True,
            size_hint_y=None,
            height=30
        )
        content.add_widget(name_label)

        # Create a layout for the monthly limit controls
        monthlyLimit_layout = BoxLayout(
            orientation="horizontal",
            spacing=20,
            size_hint_y=None,
            height=50
        )

        # Add a "-" button to decrease the monthly limit
        minus_button = Button(
            text="-",
            size_hint_x=None,
            width=50,
            on_release=lambda x: self.update_monthlyLimit(-1)  # Decrease limit by 1
        )
        monthlyLimit_layout.add_widget(minus_button)

        # Add a TextInput for the monthly limit
        self.monthlyLimit_input = TextInput(
            text=str(monthlyLimit),  # Display the current monthly limit
            multiline=False,
            size_hint_x=0.6,
            input_type="number",
            foreground_color=(1, 1, 1, 1),  # White text
            background_color=(0.2, 0.2, 0.2, 1)  # Dark background
        )
        monthlyLimit_layout.add_widget(self.monthlyLimit_input)

        # Add a "+" button to increase the monthly limit
        plus_button = Button(
            text="+",
            size_hint_x=None,
            width=50,
            on_release=lambda x: self.update_monthlyLimit(1)  # Increase limit by 1
        )
        monthlyLimit_layout.add_widget(plus_button)

        # Add the monthly limit controls to the dialog
        content.add_widget(monthlyLimit_layout)

        # Open the dialog
        self.dialog.open()

        # Dismiss any existing child popup dialog
        self.child_popup_dialog.dismiss()
        
    def edit_balance(self, first, last):
        """
        Open a dialog to edit the balance for a specific child.

        This function:
        - Searches for the child in `self.children_data` using their first and last name.
        - Displays the current balance in a dialog.
        - Allows the user to update the balance using a TextInput and +/- buttons.
        - Provides "Cancel" and "Apply" buttons to dismiss the dialog or save changes.

        Args:
            first (str): The first name of the child.
            last (str): The last name of the child.
        """
        # Initialize balance with a default value
        balance = 0.0

        # Search for the child in `self.children_data`
        for user_id, user_data in self.children_data.items():
            if user_data.get('first') == first and user_data.get('last') == last:
                # Retrieve the current balance for the child
                balance = user_data.get('balance')
                break  # Exit the loop once the child is found
        else:
            # If the child is not found, print a message
            print("User not found")

        # Create a custom MDDialog for editing the balance
        self.dialog = MDDialog(
            title=f"[color={text_Color1}]Edit Balance[/color]",  # Title with custom text color
            type="custom",
            md_bg_color=(0.1098, 0.1098, 0.1373, 1),  # Set the dialog background color
            content_cls=BoxLayout(
                orientation="vertical",
                spacing=20,
                padding=20,
                size_hint_y=None,
                height=150
            ),
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    text_color=f"{text_Color2}",  # Set button text color
                    on_release=lambda x: self.dialog.dismiss()  # Close dialog on button press
                ),
                MDFlatButton(
                    text="Apply",
                    theme_text_color="Custom",
                    text_color=f"{text_Color2}",  # Set button text color
                    on_release=lambda x: self.apply_balance_changes(balance, self.balance_input.text, first, last)  # Apply changes
                )
            ]
        )

        # Add content to the dialog
        content = self.dialog.content_cls

        # Display the child's name in the dialog
        name_label = Label(
            text=f"[color={text_Color1}]{first} {last}[/color]",  # Custom text color with markup
            markup=True,
            size_hint_y=None,
            height=30
        )
        content.add_widget(name_label)

        # Create a layout for the balance controls
        balance_layout = BoxLayout(
            orientation="horizontal",
            spacing=20,
            size_hint_y=None,
            height=50
        )

        # Add a "-" button to decrease the balance
        minus_button = Button(
            text="-",
            size_hint_x=None,
            width=50,
            on_release=lambda x: self.update_balance(-1)  # Decrease balance by 1
        )
        balance_layout.add_widget(minus_button)

        # Add a TextInput for the balance
        self.balance_input = TextInput(
            text=str(balance),  # Display the current balance
            multiline=False,
            size_hint_x=0.6,
            input_type="number",
            foreground_color=(1, 1, 1, 1),  # White text
            background_color=(0.2, 0.2, 0.2, 1)  # Dark background
        )
        balance_layout.add_widget(self.balance_input)

        # Add a "+" button to increase the balance
        plus_button = Button(
            text="+",
            size_hint_x=None,
            width=50,
            on_release=lambda x: self.update_balance(1)  # Increase balance by 1
        )
        balance_layout.add_widget(plus_button)

        # Add the balance controls to the dialog
        content.add_widget(balance_layout)

        # Open the dialog
        self.dialog.open()

        # Dismiss any existing child popup dialog
        self.child_popup_dialog.dismiss()

    def edit_monthly_allowance(self, first, last):
        """
        Open a dialog to edit the monthly allowance for a specific child.

        This function:
        - Searches for the child in `self.children_data` using their first and last name.
        - Displays the current monthly allowance in a dialog.
        - Allows the user to update the monthly allowance using a TextInput and +/- buttons.
        - Provides "Cancel" and "Apply" buttons to dismiss the dialog or save changes.

        Args:
            first (str): The first name of the child.
            last (str): The last name of the child.
        """
        # Search for the child in `self.children_data`
        for user_id, user_data in self.children_data.items():
            if user_data.get('first') == first and user_data.get('last') == last:
                # Retrieve the current monthly allowance for the child
                monthlyAllowance = user_data.get('monthlyAllowance')
                print(f"Monthly Limit for {first} {last}: {monthlyAllowance}")
                break  # Exit the loop once the child is found
        else:
            # If the child is not found, print a message
            print("User not found")

        # Create a custom MDDialog for editing the monthly allowance
        self.dialog = MDDialog(
            title=f"[color={text_Color1}]Edit monthlyAllowance[/color]",  # Title with custom text color
            type="custom",
            md_bg_color=(0.1098, 0.1098, 0.1373, 1),  # Set the dialog background color
            content_cls=BoxLayout(
                orientation="vertical",
                spacing=20,
                padding=20,
                size_hint_y=None,
                height=150
            ),
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    theme_text_color="Custom",
                    text_color=f"{text_Color2}",  # Set button text color
                    on_release=lambda x: self.dialog.dismiss()  # Close dialog on button press
                ),
                MDFlatButton(
                    text="Apply",
                    theme_text_color="Custom",
                    text_color=f"{text_Color2}",  # Set button text color
                    on_release=lambda x: self.apply_monthlyAllowance_changes(self.monthlyAllowance_input.text, first, last)  # Apply changes
                )
            ]
        )

        # Add content to the dialog
        content = self.dialog.content_cls

        # Display the child's name in the dialog
        name_label = Label(
            text=f"[color=ffffff]{first} {last}[/color]",  # White text with markup
            markup=True,
            size_hint_y=None,
            height=30
        )
        content.add_widget(name_label)

        # Create a layout for the monthly allowance controls
        monthlyAllowance_layout = BoxLayout(
            orientation="horizontal",
            spacing=20,
            size_hint_y=None,
            height=50
        )

        # Add a "-" button to decrease the monthly allowance
        minus_button = Button(
            text="-",
            size_hint_x=None,
            width=50,
            on_release=lambda x: self.update_monthlyAllowance(-1)  # Decrease allowance by 1
        )
        monthlyAllowance_layout.add_widget(minus_button)

        # Add a TextInput for the monthly allowance
        self.monthlyAllowance_input = TextInput(
            text=str(monthlyAllowance),  # Display the current monthly allowance
            multiline=False,
            size_hint_x=0.6,
            input_type="number",
            foreground_color=(1, 1, 1, 1),  # White text
            background_color=(0.2, 0.2, 0.2, 1)  # Dark background
        )
        monthlyAllowance_layout.add_widget(self.monthlyAllowance_input)

        # Add a "+" button to increase the monthly allowance
        plus_button = Button(
            text="+",
            size_hint_x=None,
            width=50,
            on_release=lambda x: self.update_monthlyAllowance(1)  # Increase allowance by 1
        )
        monthlyAllowance_layout.add_widget(plus_button)

        # Add the monthly allowance controls to the dialog
        content.add_widget(monthlyAllowance_layout)

        # Open the dialog
        self.dialog.open()

        # Dismiss any existing child popup dialog
        self.child_popup_dialog.dismiss()
        
    def update_balance(self, amount):
        """
        Update the balance in the input field.

        This method adjusts the balance displayed in the `balance_input` TextInput widget
        by adding the specified `amount`. The balance is constrained to a maximum value
        of 999,999,999.99. If the amount is outside the valid range (0.50 to 500.00),
        an error message is printed.

        Args:
            amount (float): The amount to add to the current balance. Must be between 0.50 and 500.00.
        """
        # Check if the amount is within the valid range
        print(amount)
        if (amount >= 0.50 and amount <= 500.00) or (amount <= -0.50 and amount >= -500.00):
            try:
                # Get the current balance from the input field and convert it to a float
                current_balance = float(self.balance_input.text)
                # Calculate the new balance by adding the specified amount
                new_balance = current_balance + amount
                # Ensure the new balance does not exceed the maximum allowed value
                if new_balance > 999999999.99:
                    new_balance = 999999999.99
                # Update the input field with the new balance
                self.balance_input.text = str(new_balance)
            except ValueError:
                # Handle the case where the input cannot be converted to a float
                pass
        else:
            # Print an error message if the amount is outside the valid range
            print("Invalid amount")
        
    def update_monthlyLimit(self, amount):
        """
        Update the monthly limit in the input field.

        This method adjusts the monthly limit displayed in the `monthlyLimit_input` TextInput widget
        by adding the specified `amount`. The monthly limit is constrained to a maximum value
        of 999,999,999.99. If the input cannot be converted to a float, the error is ignored.

        Args:
            amount (float): The amount to add to the current monthly limit.
        """
        try:
            # Get the current monthly limit from the input field and convert it to a float
            current_monthlyLimit = float(self.monthlyLimit_input.text)
            # Calculate the new monthly limit by adding the specified amount
            new_monthlyLimit = current_monthlyLimit + amount
            # Ensure the new monthly limit does not exceed the maximum allowed value
            if new_monthlyLimit > 999999999.99:
                new_monthlyLimit = 999999999.99
            # Update the input field with the new monthly limit
            self.monthlyLimit_input.text = str(new_monthlyLimit)
        except ValueError:
            # Handle the case where the input cannot be converted to a float (e.g., invalid input)
            pass

    def update_monthlyAllowance(self, amount):
        """
        Update the monthly allowance in the input field.

        This method adjusts the monthly allowance displayed in the `monthlyAllowance_input` TextInput widget
        by adding the specified `amount`. The monthly allowance is constrained to a maximum value
        of 999,999,999.99. If the input cannot be converted to a float, the error is ignored.

        Args:
            amount (float): The amount to add to the current monthly allowance.
        """
        try:
            # Get the current monthly allowance from the input field and convert it to a float
            current_monthlyAllowance = float(self.monthlyAllowance_input.text)
            # Calculate the new monthly allowance by adding the specified amount
            new_monthlyAllowance = current_monthlyAllowance + amount
            # Ensure the new monthly allowance does not exceed the maximum allowed value
            if new_monthlyAllowance > 999999999.99:
                new_monthlyAllowance = 999999999.99
            # Update the input field with the new monthly allowance
            self.monthlyAllowance_input.text = str(new_monthlyAllowance)
        except ValueError:
            # Handle the case where the input cannot be converted to a float (e.g., invalid input)
            pass

    def apply_balance_changes(self, old_balance, new_balance, first, last):
        """
        Apply the changes to the balance and close the dialog.

        This method validates the new balance and applies the changes if they meet the criteria:
        - The new balance must be a valid number.
        - The difference between the new and old balance must be within the allowed range:
            - Cannot add more than 500.00 at a time.
            - Cannot subtract more than 500.00 at a time.
            - Cannot add or subtract less than 0.50 at a time.
        If the changes are valid, the balance is updated in Firestore and the local `children_data`.

        Args:
            old_balance (str): The current balance before changes.
            new_balance (str): The new balance to apply.
            first (str): The first name of the child.
            last (str): The last name of the child.
        """
        # Validate that the new balance is a number
        try:
            float(new_balance)
        except ValueError:
            # Show an error message if the new balance is not a valid number
            MDSnackbar(
                MDLabel(text="Amount must be a number", theme_text_color="Secondary"),
                auto_dismiss=True,
            ).open()
            return

        # Validate that the old balance is a number
        try:
            float(old_balance)
        except ValueError:
            # Show an error message if the old balance is not a valid number
            MDSnackbar(
                MDLabel(text="Amount must be a number", theme_text_color="Secondary"),
                auto_dismiss=True,
            ).open()
            return

        # Calculate the difference between the new and old balance
        difference = float(new_balance) - float(old_balance)
        print(difference)
        # Validate the difference against allowed limits
        if difference > 500.00 and difference > 0:
            # Show an error message if adding more than 500.00
            MDSnackbar(
                MDLabel(text="You can't add more than 500 at a time", theme_text_color="Secondary"),
                auto_dismiss=True,
            ).open()
            return
        elif difference < -500.00 and difference < 0:
            # Show an error message if subtracting more than 500.00
            MDSnackbar(
                MDLabel(text="You can't subtract more than 500 at a time", theme_text_color="Secondary"),
                auto_dismiss=True,
            ).open()
            return
        elif difference > -0.50 and difference < 0:
            # Show an error message if subtracting less than 0.50
            MDSnackbar(
                MDLabel(text="You can't subtract less than 0.50 at a time", theme_text_color="Secondary"),
                auto_dismiss=True,
            ).open()
            return
        elif difference < 0.50 and difference > 0:
            # Show an error message if adding less than 0.50
            MDSnackbar(
                MDLabel(text="You can't add less than 0.50 at a time", theme_text_color="Secondary"),
                auto_dismiss=True,
            ).open()
            return

        # Find the child in `self.children_data` using their first and last name
        for user_id, user_data in self.children_data.items():
            if user_data.get('first') == first and user_data.get('last') == last:
                break  # Exit the loop once the child is found
        else:
            # If the child is not found, print a message and return
            print("User not found")
            return

        # Update the balance in Firestore
        doc_ref = db_temp.collection('Users').document(user_id)
        doc_ref.update({'balance': float(new_balance)})

        # Update the balance in the local `children_data`
        self.children_data[user_id]['balance'] = float(new_balance)

        # Dismiss the dialog
        self.dialog.dismiss()

        # Reload the children data to reflect the changes
        self.load_children()
        
    def apply_monthlyLimit_changes(self, new_monthlyLimit, first, last):
        """
        Apply the changes to the monthly limit and close the dialog.

        This method updates the monthly limit for the specified child in Firestore and the local `children_data`.
        After updating, it dismisses the dialog and refreshes the UI to reflect the changes.

        Args:
            new_monthlyLimit (str): The new monthly limit to apply.
            first (str): The first name of the child.
            last (str): The last name of the child.
        """
        # Search for the child in `self.children_data` using their first and last name
        for user_id, user_data in self.children_data.items():
            if user_data.get('first') == first and user_data.get('last') == last:
                print(user_id)  # Print the user ID for debugging
                break  # Exit the loop once the child is found
        else:
            # If the child is not found, print a message and return
            print("User not found")
            return

        # Update the monthly limit in Firestore
        doc_ref = db_temp.collection('Users').document(user_id)
        doc_ref.update({'monthlyLimit': float(new_monthlyLimit)})  # Update the 'monthlyLimit' field

        # Update the monthly limit in the local `children_data`
        self.children_data[user_id]['monthlyLimit'] = float(new_monthlyLimit)  # Update the 'monthlyLimit' field

        # Dismiss the dialog
        self.dialog.dismiss()

        # Reload the children data to reflect the changes
        self.load_children()
    
    def apply_monthlyAllowance_changes(self, new_monthlyAllowance, first, last):
        """
        Apply the changes to the monthly allowance and close the dialog.

        This method validates the new monthly allowance and applies the changes if they meet the criteria:
        - The new monthly allowance must be a valid number.
        - The new monthly allowance cannot exceed the monthly limit.
        - The new monthly allowance cannot be less than $5 (unless it is $0).
        - The new monthly allowance cannot be more than $100.
        If the changes are valid, the monthly allowance is updated in Firestore and the local `children_data`.

        Args:
            new_monthlyAllowance (str): The new monthly allowance to apply.
            first (str): The first name of the child.
            last (str): The last name of the child.
        """
        # Search for the child in `self.children_data` using their first and last name
        for user_id, user_data in self.children_data.items():
            if user_data.get('first') == first and user_data.get('last') == last:
                print(user_id)  # Print the user ID for debugging
                break  # Exit the loop once the child is found
        else:
            # If the child is not found, print a message and return
            print("User not found")
            return

        # Validate that the new monthly allowance is a number
        try:
            float(new_monthlyAllowance)
        except ValueError:
            # Show an error message if the new monthly allowance is not a valid number
            MDSnackbar(
                MDLabel(text="Amount exceeds monthly limit", theme_text_color="Secondary"),
                auto_dismiss=True,
            ).open()
            return

        # Check if the new monthly allowance exceeds the monthly limit
        if float(new_monthlyAllowance) > float(user_data['monthlyLimit']):
            # Show an error message if the allowance exceeds the monthly limit
            MDSnackbar(
                MDLabel(text="Amount exceeds monthly limit", theme_text_color="Secondary"),
                auto_dismiss=True,
            ).open()
            return

        # Check if the new monthly allowance is less than $5 (and not $0)
        if float(new_monthlyAllowance) < 5 and float(new_monthlyAllowance) != 0:
            # Show an error message if the allowance is less than $5
            MDSnackbar(
                MDLabel(text="Amount cannot be less than $5", theme_text_color="Secondary"),
                auto_dismiss=True,
            ).open()
            return

        # Check if the new monthly allowance is more than $100
        if float(new_monthlyAllowance) > 100:
            # Show an error message if the allowance is more than $100
            MDSnackbar(
                MDLabel(text="Amount cannot be more than $100", theme_text_color="Secondary"),
                auto_dismiss=True,
            ).open()

        # Update the monthly allowance in Firestore
        doc_ref = db_temp.collection('Users').document(user_id)
        doc_ref.update({'monthlyAllowance': float(new_monthlyAllowance)})  # Update the 'monthlyAllowance' field

        # Update the monthly allowance in the local `children_data`
        self.children_data[user_id]['monthlyAllowance'] = float(new_monthlyAllowance)  # Update the 'monthlyAllowance' field

        # Dismiss the dialog
        self.dialog.dismiss()

        # Reload the children data to reflect the changes
        self.load_children()
        
    def settings(self):
        """
        Open a settings dialog with options to logout or delete the account.

        This method creates and displays a dialog with two buttons:
        - "Logout": Logs the user out of the application.
        - "Delete Account": Deletes the user's account.

        The dialog has a custom title and background color, and the buttons have custom text colors.
        """
        # Create a settings dialog with a custom title and background color
        self.settings_dialog = MDDialog(
            title=f"[color={text_Color1}]Settings[/color]",  # Title with custom text color
            md_bg_color=(0.1098, 0.1098, 0.1373, 1),  # Set the dialog background color
            buttons=[
                # Add a "Logout" button
                MDFlatButton(
                    text="Logout",
                    theme_text_color="Custom",
                    text_color="white",  # Set button text color to white
                    on_release=lambda x: self.logout(),  # Bind to the logout method
                ),
                # Add a "Delete Account" button
                MDFlatButton(
                    text="Delete Account",
                    theme_text_color="Custom",
                    text_color="red",  # Set button text color to red
                    on_release=lambda x: self.delete_account(),  # Bind to the delete_account method
                    line_color=(1, 0, 0, 1),  # Add a red border to the button
                    line_width=1  # Set the border width
                )
            ]
        )

        # Open the settings dialog
        self.settings_dialog.open()
    
    def delete_account(self):
        """
        Open a confirmation dialog for account deletion.

        This method creates and displays a confirmation dialog with two buttons:
        - "Cancel": Dismisses the dialog without taking any action.
        - "Delete": Proceeds with the account deletion process by calling `self.confirm_delete()`.

        The dialog asks the user to confirm if they want to delete their account.
        """
        # Create a confirmation dialog for account deletion
        self.confirm_dialog = MDDialog(
            title="Confirm Deletion",  # Dialog title
            text="Are you sure you want to delete your account?",  # Dialog message
            buttons=[
                # Add a "Cancel" button
                MDFlatButton(
                    text="Cancel",
                    on_release=lambda x: self.confirm_dialog.dismiss()  # Dismiss the dialog
                ),
                # Add a "Delete" button
                MDFlatButton(
                    text="Delete",
                    on_release=lambda x: self.confirm_delete()  # Call the confirm_delete method
                )
            ]
        )

        # Open the confirmation dialog
        self.confirm_dialog.open()
    
    def confirm_delete(self):
        """
        Confirm and proceed with account deletion.

        This method:
        - Dismisses any open dialogs.
        - Navigates the user to the 'firebase_screen' to complete the account deletion process.
        """
        # Dismiss the current dialog
        self.dialog.dismiss()

        # Dismiss the confirmation dialog
        self.confirm_dialog.dismiss()

        # Navigate to the 'firebase_screen' to complete the account deletion process
        self.parent.current = 'firebase_screen'

    def history(self):
        """
        Display the transaction history for all children.

        This method:
        - Removes any existing scroll view if it exists.
        - Creates a new scrollable layout to display transaction cards.
        - Iterates over each child and their transactions, creating a `TransactionCard1` for each transaction.
        - Adds the transaction cards to the layout and displays them in a scrollable view.
        """
        # Remove the existing scroll_view if it exists
        if hasattr(self, 'scroll_view'):
            self.remove_widget(self.scroll_view)

        # Create a new GridLayout to hold the transaction cards
        layout = GridLayout(cols=1, size_hint_y=None, padding=[0, 0, 0, 0], spacing=10)
        layout.clear_widgets()  # Clear any existing widgets
        layout.bind(minimum_height=layout.setter('height'))  # Make the layout scrollable

        # Create a new ScrollView to contain the layout
        self.scroll_view = ScrollView(size_hint=(1.5, 0.8), pos_hint={'center_x': 0.37, 'center_y': 0.52})
        self.scroll_view.add_widget(layout)  # Add the layout to the ScrollView
        self.add_widget(self.scroll_view)  # Add the ScrollView to the screen

        # Iterate over each child and their transactions
        for child in self.children_data:
            # Check if the child has any transactions
            if 'transactions' in self.children_data[child]:
                # Iterate over each transaction for the child
                for transaction_id, transaction_data in self.children_data[child]['transactions'].items():
                    # Extract transaction details
                    amount = transaction_data['amount']
                    category = transaction_data['category']
                    date = transaction_data['date']

                    # Create a TransactionCard1 widget for the transaction
                    transaction_card = TransactionCard1(amount=str(amount), category=category, date=date)
                    print(f"Adding transaction {transaction_id} to layout...")
                    layout.add_widget(transaction_card)  # Add the transaction card to the layout
            else:
                # Print a message if the child has no transactions
                print(f"No transactions for {child}")
                
    def children_screen_loader(self):
        """
        Clear existing transaction cards and reload the children's data.

        This method:
        - Iterates over the current children widgets and removes any `TransactionCard1` instances.
        - Calls `self.load_children()` to reload and display the updated children's data.
        """
        # Iterate over a copy of the children list to avoid modifying the list while iterating
        for child in self.children[:]:
            # Check if the child is an instance of TransactionCard1
            if isinstance(child, TransactionCard1):
                # Remove the TransactionCard1 widget from the screen
                self.remove_widget(child)

        # Reload the children's data and update the UI
        self.load_children()
        
    def logout(self):
        """
        Log out the current user and reset the application state.

        This method:
        - Removes the scroll view and button layout widgets from the screen.
        - Clears the user data by writing an empty dictionary to 'user_data.json'.
        - Dismisses the settings dialog.
        - Navigates the user to the 'firebase_screen' (login/signup screen).
        """
        # Remove the scroll view widget if it exists
        if hasattr(self, 'scroll_view'):
            self.remove_widget(self.scroll_view)

        # Remove the button layout widget if it exists
        if hasattr(self, 'button_layout'):
            self.remove_widget(self.button_layout)

        # Clear the user data by writing an empty dictionary to 'user_data.json'
        with open('user_data.json', 'w') as file:
            json.dump({}, file)  # Use an empty dictionary to reset the file

        # Dismiss the settings dialog
        self.settings_dialog.dismiss()

        # Navigate to the 'firebase_screen' (login/signup screen)
        self.parent.current = 'firebase_screen'
