import misc
print("Successfully imported stock-tracker")

if not misc.credentials_check():
    print("No API credentials found, add credentials.ini to project folder!")