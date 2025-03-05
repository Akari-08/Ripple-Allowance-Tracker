from kivy.lang import Builder  # Enables defining UI layouts using KV language
from kivy.uix.screenmanager import Screen  # Manages screen navigation
from dashboardChild.childbalance import Balance  # Custom module for balance management
from kivy.uix.label import Label  # Displays text labels in the app
from kivy.properties import StringProperty  # Allows dynamic property binding with string values
from kivy.properties import ObjectProperty  # Allows dynamic property binding with object values
from kivy.uix.boxlayout import BoxLayout  # Layout manager that arranges widgets horizontally or vertically
from kivy.uix.gridlayout import GridLayout  # Layout manager that arranges widgets in a grid
from datetime import datetime  # Provides date and time functionality
from kivy.uix.textinput import TextInput  # Widget for text input fields
from kivy.uix.spinner import Spinner  # Dropdown menu widget for selecting options
from kivymd.uix.button import MDFlatButton  # Flat button from KivyMD with Material Design style
from kivymd.uix.dialog import MDDialog  # Dialog popup from KivyMD for displaying messages
from kivymd.uix.snackbar import MDSnackbar  # Snackbar from KivyMD for showing temporary notifications
from kivymd.uix.label import MDLabel  # Label from KivyMD with Material Design style
from kivy.uix.scrollview import ScrollView  # Enables scrolling through content
import random  # Provides functionality for generating random numbers

Builder.load_file("dashboardChild/childbalance.kv")
Builder.load_file("dashboardChild/childdashboard.kv")

# Define global variables
user_info_temp = {}
db_temp = None
temp = True  # Define temp in the global scope
children_loaded = False

text_Color1 = 'ffffff'
text_Color2 = 'white'

# Load JSON file
import json

try:
    with open('user_data.json') as f:
        user_info = json.load(f)
except:
    print('No user data found')

class ButtonCard(BoxLayout):
    name = StringProperty('')  # Property to store the button's name
    func = ObjectProperty(None)  # Property to store the function associated with the button

    def __init__(self, name, func, **kwargs):
        """
        Initializes the ButtonCard instance.

        Args:
            name (str): The button's name.
            func (function): The function to be executed when the button is clicked.
            **kwargs: Additional keyword arguments for the parent class.
        """
        super().__init__(**kwargs)  # Initialize the parent BoxLayout
        self.name = name  # Assign the button name to the StringProperty
        self.func = func  # Assign the function to the ObjectProperty
        
class TransactionCard(BoxLayout):
    amount = StringProperty('')  # Property to store the transaction amount
    category = StringProperty('')  # Property to store the transaction category
    date = StringProperty('')  # Property to store the transaction date

    def __init__(self, amount, category, date, **kwargs):
        """
        Initializes the TransactionCard instance.

        Args:
            amount (str): The amount of the transaction.
            category (str): The category of the transaction.
            date (str): The date of the transaction.
            **kwargs: Additional keyword arguments for the parent class.
        """
        super().__init__(**kwargs)  # Initialize the parent BoxLayout
        self.amount = amount  # Assign the transaction amount to the StringProperty
        self.category = category  # Assign the transaction category to the StringProperty
        self.date = date  # Assign the transaction date to the StringProperty

class ChildDashboard(Screen):
    """
    A class representing the child dashboard screen. This screen allows the child to view their balance,
    add transactions, view transaction history, and manage account settings.
    """

    def __init__(self, **kwargs):
        """
        Initialize the ChildDashboard screen.
        """
        super(ChildDashboard, self).__init__(**kwargs)
        self.user = []  # Store user information
        self.user_info = []  # Store additional user info
        self.db = None  # Database reference
        self.localId = None  # User's unique ID
        self.balance = 0  # User's balance

    def on_enter(self, *args):
        """
        Called when the screen is entered. Initializes the screen, retrieves the balance,
        and updates the UI with balance, buttons, and transactions.
        """
        super(ChildDashboard, self).on_enter(*args)
        self.initialize()  # Ensure the screen is initialized
        self.find_balance()  # Retrieve the current balance
        self.print_balance()  # Display the balance
        self.print_buttons()  # Display action buttons
        self.print_transactions()  # Display transaction history

    def initialize(self):
        """
        Initialize user-related data and ensure required fields exist in the database.
        """
        global user_info
        try:
            self.user = self.parent.user  # Get user data from parent
            self.db = self.parent.db  # Get database reference from parent
            self.user_info = user_info  # Get additional user info
            self.localId = self.user_info['auth']['localId']  # Get user's unique ID
            doc_ref = self.db.collection('Users').document(self.localId)

            # Ensure required fields exist in the database
            if 'balance' not in doc_ref.get().to_dict():
                doc_ref.set({'balance': 0}, merge=True)
            if 'monthlyAllowance' not in doc_ref.get().to_dict():
                doc_ref.set({'monthlyAllowance': 0}, merge=True)
            if 'monthlyLimit' not in doc_ref.get().to_dict():
                doc_ref.set({'monthlyLimit': 0}, merge=True)
            if 'monthlyLimitSpent' not in doc_ref.get().to_dict():
                doc_ref.set({'monthlyLimitSpent': 0}, merge=True)

            # Retrieve user-specific data
            try:
                self.monthlyAllowance = doc_ref.get().to_dict()['monthlyAllowance']
                self.monthlyLimit = doc_ref.get().to_dict()['monthlyLimit']
                self.monthlyLimitSpent = doc_ref.get().to_dict()['monthlyLimitSpent']
            except:
                self.monthlyAllowance = 0
                self.monthlyLimit = 0
                self.monthlyLimitSpent = 0
        except Exception as e:
            print(f'Error occurred: {e}')

    def find_balance(self):
        """
        Retrieve the user's current balance from the database.
        """
        doc_ref = self.db.collection('Users').document(self.localId)
        doc = doc_ref.get()
        balance = doc.to_dict()
        try:
            self.balance = balance['balance']  # Set the balance
        except:
            self.balance = 0  # Default to 0 if balance is not found

    def print_balance(self):
        """
        Display the user's balance on the screen.
        """
        balance = self.balance  # Get the current balance
        if hasattr(self, 'balance_label1'):
            self.remove_widget(self.balance_label1)
            del self.balance_label1

        # Create or update labels to display the balance
        if not hasattr(self, 'balance_label'):
            self.balance_label1 = Label(text=f"{balance}", size_hint=(0.5, 0.1), pos_hint={"x": 0.25, "top": 0.85}, color=text_Color1, font_size=50)
            self.balance_label2 = Label(text="Balance", size_hint=(0.5, 0.1), pos_hint={"x": 0.25, "top": 0.81}, color=text_Color1, font_size=30)
            self.add_widget(self.balance_label1)  # Add the balance value label
            self.add_widget(self.balance_label2)  # Add the "Balance" text label
        else:
            self.balance_label1.text = f"{balance}"  # Update the balance value
            self.balance_label2.text = f"Balance"  # Update the "Balance" text

    def print_buttons(self):
        """
        Display action buttons on the screen (e.g., Add Transaction, View Details).
        """
        self.button_layout = BoxLayout(orientation='horizontal', size_hint_x=None, width=480, pos_hint={"x": -0.24})
        sub_button = ButtonCard(name="Add Transaction", func=self.add_transaction)
        add_button = ButtonCard(name="View Details", func=self.view_details)
        self.button_layout.add_widget(sub_button)
        self.button_layout.add_widget(add_button)
        self.add_widget(self.button_layout)

    def add_transaction(self):
        """
        Open a dialog to add a new transaction.
        """
        self.dialog = MDDialog(
            title=f"[color={text_Color1}]Add Transaction[/color]",  # Title with custom text color
            type="custom",
            md_bg_color=(0.1098, 0.1098, 0.1373, 1),  # Set dialog background color
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
                    on_release=lambda x: self.save_transaction(self.amount_input.text, self.category.text)  # Save the transaction
                )
            ]
        )

        # Add content to the dialog
        content = self.dialog.content_cls

        # Category selection spinner
        self.category = Spinner(
            text="Select Category",
            values=("Food", "Entertainment", "Transport", "Utilities", "Other")
        )

        # Layout for amount input
        add_transaction_layout = BoxLayout(
            orientation="horizontal",
            spacing=20,
            size_hint_y=None,
            height=50
        )

        # Amount input field
        self.amount_input = TextInput(
            hint_text='Amount',
            multiline=False,
            size_hint_x=0.6,
            input_type="number",
            foreground_color=(1, 1, 1, 1),  # White text
            background_color=(0.2, 0.2, 0.2, 1)  # Dark background
        )
        add_transaction_layout.add_widget(self.amount_input)
        content.add_widget(self.category)
        content.add_widget(add_transaction_layout)
        self.dialog.open()

    def save_transaction(self, amount, category):
        """
        Save a new transaction to the database after validating the input.

        Args:
            amount (str): The transaction amount.
            category (str): The transaction category.
        """
        try:
            float(amount)  # Validate that the amount is a number
        except:
            MDSnackbar(
                MDLabel(text="Amount must be a number", theme_text_color="Secondary"),
                auto_dismiss=True,
            ).open()
            return
        if float(amount) < 0:
            MDSnackbar(
                MDLabel(text="Amount must be positive", theme_text_color="Secondary"),
                auto_dismiss=True,
            ).open()
        if float(amount) > self.balance:
            MDSnackbar(
                MDLabel(text="Amount exceeds balance", theme_text_color="Secondary"),
                auto_dismiss=True,
            ).open()
            return
        if category == "Select Category":
            MDSnackbar(
                MDLabel(text="Please select a category", theme_text_color="Secondary"),
                auto_dismiss=True,
            ).open()
            return
        if self.monthlyLimitSpent + float(amount) > self.monthlyLimit:
            MDSnackbar(
                MDLabel(text="Amount exceeds monthly limit", theme_text_color="Secondary"),
                auto_dismiss=True,
            ).open()
            return

        # Update monthly limit spent
        self.monthlyLimitSpent += float(amount)
        doc_ref = self.db.collection('Users').document(self.localId)
        doc_ref.update({
            'monthlyLimitSpent': self.monthlyLimitSpent
        })

        # Record the transaction
        transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        doc_ref.update({
            'balance': self.balance - float(amount)
        })
        self.balance = self.balance - float(amount)
        self.print_balance()

        # Save transaction details
        rand = self.random_transaction_id()
        doc_ref.set({'transactions': 
                        {f'{rand}': {
                            'amount': float(amount),
                            'category': category,
                            'datetime': transaction_time
                            }
                        }
                    }, merge=True
                )
        self.print_transactions()
        self.dialog.dismiss()

    def print_transactions(self):
        """
        Display the user's transaction history on the screen.
        """
        if hasattr(self, 'scroll_view'):
            self.remove_widget(self.scroll_view)

        # Create a layout to hold transaction cards
        title_layout = BoxLayout(orientation='horizontal', size_hint_x=None, width=480, pos_hint={"x": 0.05, "y": 0.54})
        title = Label(text="Transactions", size_hint=(0.5, 0.1), color=text_Color1, font_size=30)
        title_layout.add_widget(title)
        layout = GridLayout(cols=1, size_hint_y=None, padding=[0, 0, 0, 0], spacing=0)
        layout.clear_widgets()
        layout.bind(minimum_height=layout.setter('height'))  # Make the layout scrollable

        # Add the layout to a ScrollView
        self.scroll_view = ScrollView(size_hint=(1.5, 0.8), pos_hint={'center_x': 0.52, 'center_y': 0.15})
        self.scroll_view.add_widget(layout)
        self.add_widget(self.scroll_view)
        self.add_widget(title_layout)

        # Retrieve and display transactions
        doc_ref = self.db.collection('Users').document(self.localId)
        transactions = doc_ref.get().to_dict()
        try:
            transactions = transactions['transactions']
        except:
            transactions = {}

        for transaction in transactions:
            amount = transactions[transaction]['amount']
            category = transactions[transaction]['category']
            date = transactions[transaction]['datetime'][:10]
            formatted_date = self.format_date(date)

            # Create and add a transaction card
            transaction_card = TransactionCard(amount=str(amount), category=category, date=formatted_date)
            layout.add_widget(transaction_card)

    def format_date(self, date_str):
        """
        Convert a date string in the format YYYY-MM-DD to a more readable format.

        Args:
            date_str (str): The date string in the format YYYY-MM-DD.

        Returns:
            str: The formatted date string (e.g., "April 2, 2025").
        """
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%B %d, %Y")
            return formatted_date
        except ValueError:
            return "Invalid date format. Please use YYYY-MM-DD."

    def view_details(self):
        """
        Display a dialog with the user's monthly allowance and limit details.
        """
        print(self.localId)
        doc_ref = self.db.collection('Users').document(self.localId)
        self.monthlyAllowance = doc_ref.get().to_dict()['monthlyAllowance']
        self.monthlyLimit = doc_ref.get().to_dict()['monthlyLimit']

        # Create and configure the dialog
        self.view_details_dialog = MDDialog(
            title=f"[color={text_Color1}]Parent Code[/color]",
            text=f"[color={text_Color1}]Monthly Allowance: ${self.monthlyAllowance}\nMonthly Limit: ${self.monthlyLimit}\nMonthly Limit Spent: ${self.monthlyLimitSpent}[/color]",
            md_bg_color=(0.1098, 0.1098, 0.1373, 1),
            buttons=[
                MDFlatButton(
                    text="OK",
                    theme_text_color="Custom",
                    text_color=f"{text_Color2}",
                    on_release=lambda x: self.view_details_dialog.dismiss(),
                )
            ]
        )
        self.view_details_dialog.open()

    def random_transaction_id(self):
        """
        Generate a random transaction ID.

        Returns:
            str: A unique transaction ID.
        """
        id = ''
        localid = self.localId
        id += localid[:4]
        id += str(random.randint(10000, 99999))
        id += localid[-4:]
        return id

    def settings(self):
        """
        Open a dialog for account settings (e.g., logout, delete account).
        """
        self.settings_dialog = MDDialog(
            title=f"[color={text_Color1}]Settings[/color]",
            md_bg_color=(0.1098, 0.1098, 0.1373, 1),
            buttons=[
                MDFlatButton(
                    text="Logout",
                    theme_text_color="Custom",
                    text_color="white",
                    on_release=lambda x: self.logout(),
                ),
                MDFlatButton(
                    text="Delete Account",
                    theme_text_color="Custom",
                    text_color="red",
                    on_release=lambda x: self.delete_account(),
                    line_color=(1, 0, 0, 1),
                    line_width=1
                )
            ]
        )
        self.settings_dialog.open()

    def delete_account(self):
        """
        Open a confirmation dialog for account deletion.
        """
        self.confirm_dialog = MDDialog(
            title="Confirm Deletion",
            text="Are you sure you want to delete your account?",
            buttons=[
                MDFlatButton(
                    text="Cancel",
                    on_release=lambda x: self.confirm_dialog.dismiss()
                ),
                MDFlatButton(
                    text="Delete",
                    on_release=lambda x: self.confirm_delete()
                )
            ]
        )
        self.confirm_dialog.open()

    def confirm_delete(self):
        """
        Confirm account deletion and navigate to the Firebase screen.
        """
        self.dialog.dismiss()
        self.confirm_dialog.dismiss()
        self.parent.current = 'firebase_screen'

    def logout(self):
        """
        Log out the user and navigate to the Firebase screen.
        """
        self.remove_widget(self.scroll_view)
        self.remove_widget(self.button_layout)
        with open('user_data.json', 'w') as file:
            json.dump({}, file)  # Clear user data
        self.settings_dialog.dismiss()
        self.parent.current = 'firebase_screen'
