import customtkinter as ctk 
import cv2
from pyzbar.pyzbar import decode
from pydub import AudioSegment
from pydub.playback import play
import time

#list that stores barcode numbers
product_id = ["5012345678900", "6008454002636"]

#list that stores scanned products
scanned_l = []

line = ""
price = 0

#variables for payment
amount = 0

approve = 0

#pin for card variable
pin_num = "0"
card_num = ""

def scan():
    
    global line
    global price
    
  
    pay_btn.configure(state="enabled")
    
    beep = AudioSegment.from_wav("beep-02.wav")
    capture = cv2.VideoCapture(0)
    capture.set(3,640)
    capture.set(4,480)
    while True:
        success,frame = capture.read()
        frame = cv2.flip(frame,1)
        
        barcode_detect = decode(frame)
        if not barcode_detect:
            print("No barcode detected")
        else:
            for code in barcode_detect:
                if code.data != "":
                    #play(beep)
                    bar_data = code.data.decode('utf-8')
            break
        cv2.imshow('scanner', frame)
        cv2.waitKey(1) 
        
    
 
    
    
    if (bar_data == "5012345678900") and (bar_data in product_id):
        name = "white star(maize meal)" 
        scanned_l.append(bar_data) 
        prod_price = 100
        price += prod_price
        undef.configure(text="")
        
    elif bar_data == "6008454002636" and (bar_data in product_id):
        name = "Scholar (counter book A4 3Q.F & M)"
        scanned_l.append(bar_data)
        prod_price = 20
        price += prod_price
        undef.configure(text="")
        
    else:
        name = "Undefined product"
        prod_price = 0
        price += prod_price
        undef.configure(text="product not available in our database😒", text_color="red")
        
        
    if (len(name) < 40):
        space = 40 - len(name)
        line = line + (bar_data + (" "*2) + name + (" " * space) + "R" + str(float(prod_price))) + "\n"
    else:
        line = line + (bar_data + (" "*2) + name + " "+ "R" + str(float(prod_price))) + "\n"
    des.configure(text= line)
    
    
    total_lbl.configure(text="Total Price R" + str(float(price)))
    
    
def proceed():
    
    global amount
    global approve 
    
    passkey = pin_num.get()
    
    card_pay = card_num.get()
    
    print("card number: ", card_pay)
    
    if card_pay == "0720687560" and passkey == "1234":
        amount = 100
        print("card amount", amount)
    elif card_pay == "0661713535" and passkey == "2468":
        amount = 200
        print("card amount", amount)
    else:
        amount = 0
        
    if float(amount) >= float(price) and float(amount) != 0:
        suc_or_dec.configure(text="Approved")
        proceed_btn.configure(state="disabled")
        restart_btn.configure(state="enabled")
        amount = float(amount) - float(price)
        slip_generation()
        approve = 1
        database_filtering()
        print(amount)
    else:
        suc_or_dec.configure(text="Declined")
    
def payment():
    global card_num
    global suc_or_dec
    global pin_num
    global pin
    global entry
    global proceed_btn
    
    scan_btn.configure(state="disabled")
    pay_btn.configure(state="disabled")
    
    info = ctk.CTkLabel(parent, text="Enter your card number")
    info.pack()
    
    card_num = ctk.StringVar()
    pin_num = ctk.StringVar()
    
    entry = ctk.CTkEntry(parent, width=200, height=40, textvariable= card_num)
    entry.pack(padx=10, pady=10)
    
    pin_info = ctk.CTkLabel(parent, text="Enter pin")
    pin_info.pack()
    
    pin = ctk.CTkEntry(parent, width=200, height=40, textvariable= pin_num)
    pin.pack()
    
    proceed_btn = ctk.CTkButton(parent, text="Pay", command=proceed)
    proceed_btn.pack(padx=10,pady=10)
    restart_btn.pack(padx=10,pady=10)
    
    #success or decline msg 
    suc_or_dec = ctk.CTkLabel(parent, text="")
    suc_or_dec.pack()
    
def database_filtering():
    
    
    
    
    print("scanned products", scanned_l)
    
    for itms in scanned_l:
        if itms in product_id and approve == 1:
            product_id.remove(itms)
    print("products left in the database", product_id)
    
    #returning the values to null after purchase approval
    
    price = 0
    total_lbl.configure(text="Total Price R" + str(float(price)))
    line = ""
    des.configure(text=line)
    undef.configure(text="")
    suc_or_dec.configure(text="")
   
    
def slip_generation():
    
    price = 0
    name = ""
    
    print("\nhere is your slip","\n\n============================================")
    for items in scanned_l:
        if items == "5012345678900":
            name = "white star(maize meal)"
            prod_price = 100
            price += prod_price
        elif items == "6008454002636":
            name = "Scholar (counter book A4 3Q.F & M)"
            prod_price = 20
            price += prod_price
        if (len(name) < 40):
            space = 40 - len(name)
            print(name + (" " * space) + "R" + str(prod_price))
        else:
            print(name + " "+ "R" + str(prod_price))
    print("============================================","\nTotal Price" + (" "*(40 - len("Total Price"))) + "R" + str(price), "\n============================================")
    print("\nthank you for choosing us", "\n")
        

            
    
def restart():
    
    price = 0
    total_lbl.configure(text="Total Price R" + str(float(price)))
    line = ""
    des.configure(text=line)
    undef.configure(text="")
    suc_or_dec.configure(text="")
    #scanned_l.clear()
    
    print("scanned list",scanned_l)
    
    scan_btn.configure(state="enabled")
   
        
    
#system settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

#setting up the app
parent = ctk.CTk()
parent.geometry("500x700")
parent.title("digital_retail_store_scanner")

#welcome label
welcome = ctk.CTkLabel(parent, text="welcome")
welcome.pack()

#scanning button
scan_btn = ctk.CTkButton(parent, text="Scan", command= scan)
scan_btn.pack(padx = 10, pady = 10)

#scrollable frame 
my_s_frame = ctk.CTkScrollableFrame(parent, width=400)
my_s_frame.pack(pady=10)

#description label
des = ctk.CTkLabel(my_s_frame, text="")
des.pack()

#if the product is undefined
undef = ctk.CTkLabel(parent, text="")
undef.pack()

#total label
total_lbl = ctk.CTkLabel(parent, text="Total Price R" + str(float(price)))
total_lbl.pack(padx=10,pady=10)

#payment button


pay_btn = ctk.CTkButton(parent, text="Payment", command=payment, state="disabled")
pay_btn.pack(padx=10, pady=10)
 
 
  
#restart the whole process 

restart_btn = ctk.CTkButton(parent, text="Restart", command=restart) #state="disabled")




parent.mainloop()