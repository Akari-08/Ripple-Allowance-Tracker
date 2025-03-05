# Ripple-Allowance-Tracker

[Project Under Development]

--------------------------------------------------------------

# Parent-Child Financial Management App

This is a Kivy-based application designed to help parents manage their children's finances, including allowances, spending limits, and transaction history. The app integrates with Firebase for authentication and data storage, providing a seamless experience for users.

## Features

- **User Authentication**: Secure login and signup using Firebase Authentication.
- **Parent and Child Roles**: Parents can create accounts and generate unique parent codes. Children can join using these codes.
- **Financial Management**:
  - Set and manage monthly allowances and spending limits for children.
  - View and edit children's balances.
  - Track transaction history for each child.
- **Dashboard**:
  - Parents can view all their children's financial details in one place.
  - Children can view their own balance and transaction history.
- **Notifications**: Snackbar notifications for important actions and errors.
- **Settings**: Options to log out or delete the account.

## Installation

The program itself should be runnable on a desktop/laptop, although the layout may be different on
mobile.
To run on an Android phone through Buildozer, download the product onto a Linux machine (A virtual
Ubuntu image can be downloaded on Virtualbox if necessary or a ubuntu WSL can be used).

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/parent-child-finance-app.git
   cd parent-child-finance-app
2. **Deploying the App**

Make sure your phone is in Developer mode by going to Settings and tapping 'Build Number' 7 times
quickly.
Go to Settings -- Developer Options and enable USB Debugging.
Connect your phone to your computer and make sure to Always Allow USB Debugging when your phone
connects.
Use the following commands in the terminal:
```Sudo apt install git
git clone https://github.com/kivy/buildozer.git
cd buildozer
sudo apt-get install python3.6
sudo apt-get install -y python3-setuptools
sudo python3 setup.py install
cd FridgeTracker
buildozer init
sudo apt update
sudo apt install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev
libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev
pip3 install --user --upgrade cython virtualenv
sudo apt-get install cython
buildozer android debug deploy run
```

## Dependancies
Kivy
KivyMD
Firebase
PyreBase
firebase_admin
email_validator
random
string
json
datetime

## License
This project is licensed under the MIT License. See the LICENSE file for details.
