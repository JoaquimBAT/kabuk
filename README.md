# kabuk
KabuK Style test

Code setup:
- Create a virtual env with Python3.11 or higher
- On the terminal run : pip install -r requirements.txt
- With requirements installed run: python3 app.py

Issues faced:
- All OTAs show an estimative of the price, or later inside the room option you would see price of a plan for multiple people. So this was ignored due the limited that, so what you will see on the output file is going to the estimative. With more time could have studied on how to overcome this price issue.
- Jalan website for some hotels would ot present the room informations on standardized way, so this was ignored as well. On this case i could have simply added a "dummy" value for romm type and get the price estimative for the hotel.
- ikyu web site when i tried to start my work was giving 403 as response, so it is not present on my code. Maybe used a VPN or change my IP to see if the website would responde to me.

Code improvements:
What i could hava done with more time was:
- Create a function to add rooms information to the dataframe.
- Use wait instead of sleep.

