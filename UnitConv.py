# importing all widgets and modules from the tkinter library
from tkinter import *
import tkinter
from tkinter.ttk import *


# defining the reset function
def reset():
    # using the delete() method to delete entries in entry field
    input_field.delete(0, END)
    output_field.delete(0, END)
    # setting the value of the option menu to the
    # first index of the list using the set() method
    input_value.set(SELECTIONS[0])
    output_value.set(SELECTIONS[0])

    # setting the focus to input field using the focus_set() method
    input_field.focus_set()


# defining the convert function
def convert():
    global input_field
    # getting the string from entry field and converting it into float
    inputVal = float(input_field.get())
    # getting the values from selection menus
    input_unit = input_value.get()
    output_unit = output_value.get()

    # list of the required combination of the conversion factors
    conversion_factors = [input_unit in length_units and output_unit in length_units,
                          input_unit in weight_units and output_unit in weight_units,
                          input_unit in temperature_units and output_unit in temperature_units,
                          input_unit in area_units and output_unit in area_units,
                          input_unit in volume_units and output_unit in volume_units]

    if any(conversion_factors):  # If both the units are of same type, perform the conversion
        if input_unit == "celsius" and output_unit == "fahrenheit":
            output_field.delete(0, END)
            output_field.insert(0, (inputVal * 1.8) + 32)
        elif input_unit == "fahrenheit" and output_unit == "celsius":
            output_field.delete(0, END)
            output_field.insert(0, (inputVal - 32) * (5 / 9))
        else:
            output_field.delete(0, END)
            output_field.insert(0, round(inputVal * unitDict[input_unit] / unitDict[output_unit], 5))

    else:
        # displaying error if units are of different types
        output_field.delete(0, END)
        output_field.insert(0, "ERROR")


def run():
    global output_field, input_value, output_value, unitDict
    global length_units, weight_units, temperature_units, area_units, volume_units, SELECTIONS
    # dictionary of conversion factors
    unitDict = {
        "Millimeter": 0.001,
        "Centimeter": 0.01,
        "Meter": 1.0,
        "Kilometer": 1000.0,
        "Foot": 0.3048,
        "Mile": 1609.344,
        "Yard": 0.9144,
        "Inch": 0.0254,
        "Square meter": 1.0,
        "Square kilometer": 1000000.0,
        "Square centimeter": 0.0001,
        "Square millimeter": 0.000001,
        "Are": 100.0,
        "Hectare": 10000.0,
        "Acre": 4046.856,
        "Square mile": 2590000.0,
        "Square foot": 0.0929,
        "Cubic meter": 1000.0,
        "Cubic centimeter": 0.001,
        "Litre": 1.0,
        "Millilitre": 0.001,
        "Gallon": 3.785,
        "Gram": 1.0,
        "Kilogram": 1000.0,
        "Milligram": 0.001,
        "Quintal": 100000.0,
        "Ton": 1000000.0,
        "Pound": 453.592,
        "Ounce": 28.3495
    }

    # charts for units conversion
    length_units = [
        "Millimeter", "Centimeter", "Meter", "Kilometer", "Foot", "Mile", "Yard", "Inch"
    ]
    temperature_units = [
        "Celsius", "Fahrenheit"
    ]
    area_units = [
        "Square meter", "Square kilometer", "Square centimeter", "Square millimeter",
        "Are", "Hectare", "Acre", "Square mile", "Square foot"
    ]
    volume_units = [
        "Cubic meter", "Cubic centimeter", "Litre", "Millilitre", "Gallon"
    ]
    weight_units = [
        "Gram", "Kilogram", "Milligram", "Quintal", "Ton", "Pound", "Ounce"
    ]

    # creating the list of options for selection menu
    SELECTIONS = [
        "Select Unit",
        "Millimeter",
        "Centimeter",
        "Meter",
        "Kilometer",
        "Foot",
        "Mile",
        "Yard",
        "Inch",
        "Celsius",
        "Fahrenheit",
        "Square meter",
        "Square kilometer",
        "Square centimeter",
        "Square millimeter",
        "Are",
        "Hectare",
        "Acre",
        "Square mile",
        "Square foot"
        "Cubic meter",
        "Cubic centimeter",
        "Litre",
        "Millilitre",
        "Gallon"
        "Gram",
        "Kilogram",
        "Milligram",
        "Quintal",
        "Ton",
        "Pound",
        "Ounce"
    ]

    # creating the main window of the application
    # creating an object of the Tk() class
    guiWindow = Tk()


    # setting the title of the main window
    guiWindow.title("Unit Converter - Aura Notes (v1.0.5)")
    # setting the size and position of the main window
    guiWindow.geometry("500x500+500+250")
    # disabling the resizing option
    guiWindow.resizable(0, 0)
    # setting the background color to #16a085
    guiWindow.configure(bg="#16a085")

    # adding frames to the main window
    header_frame = Frame(guiWindow)
    body_frame = Frame(guiWindow)

    # setting the positions of the frames
    header_frame.pack(expand=True, fill="both")
    body_frame.pack(expand=True, fill="both")

    # adding the label to the header frame
    header_label = Label(
        header_frame,
        text="STANDARD UNIT CONVERTER",
    )

    # setting the position of the label
    header_label.pack(expand=True, side=TOP)

    # creating the objects of the StringVar() class
    input_value = StringVar()
    output_value = StringVar()
    # using the set() method to set the primary
    # value of the objects to index value 0
    # of the SELECTIONS list
    input_value.set(SELECTIONS[0])
    output_value.set(SELECTIONS[0])

    # creating the labels for the body of the main window
    input_label = Label(
        body_frame,
        text="From:",

    )
    output_label = Label(
        body_frame,
        text="To:",

    )

    # using the grid() method to set the position of the above labels
    input_label.grid(row=1, column=1, padx=50, pady=20, sticky=W)
    output_label.grid(row=2, column=1, padx=50, pady=20, sticky=W)

    # creating the entry fields for the body of the main window
    # input field to enter data
    input_field = Entry(
        body_frame,
    )
    # output field to display result
    output_field = Entry(
        body_frame,
    )

    # using the grid() method to set the position of the above entry fields
    input_field.grid(row=1, column=2)
    output_field.grid(row=2, column=2)

    # adding the option menus to the main window
    input_menu = OptionMenu(
        body_frame,
        input_value,
        *SELECTIONS
    )
    output_menu = OptionMenu(
        body_frame,
        output_value,
        *SELECTIONS
    )

    # using the grid() method to set the position of the above option menus
    input_menu.grid(row=1, column=3, padx=20)
    output_menu.grid(row=2, column=3, padx=20)

    # creating the buttons for the main window
    # CONVERT button
    convert_button = Button(
        body_frame,
        text="CONVERT",

        command=convert
    )
    # RESET button
    reset_button = Button(
        body_frame,
        text="RESET",
        command=reset
    )

    # using the grid() method to set the position of the above buttons
    convert_button.grid(row=3, column=2)
    reset_button.grid(row=3, column=3)

    # running the application
    guiWindow.mainloop()

run()