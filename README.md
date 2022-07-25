# Anmeldung
It is hard to get an appointment from Bürgerbüro Munich when you want to register your address. 
One glitch is that sometimes appointments are opened but one needs to be constantly checking the website in order to find an available spot quickly.  
Instead of constantly checking the website and wasting time, this project uses Selenium to check if there is an available spot. Depending on the date preferences
notifications are set through discord web hook if a spot is found.

## Usage
Open up the jupyter notebook, configure date preferences, chrome driver path and the discord webhook. Run the cell.

## Requirements
* Selenium 
* Jupyter Notebook
* Chromer Driver
* Discord Webhook

## Limitations
1. Chrome uses too much memory, and program stops after 3-4 hours due to memory usage.
2. The program is functional but not user friendly. Date preferences & webhook setup procedure can be improved.
3. Automatic registration can be implemented.
