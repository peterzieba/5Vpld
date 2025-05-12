#!/usr/bin/env python3
"""
CUPL .PLD template generator GUI
Works on Linux and Windows (requires Python 3.x with Tkinter).
Generates a .pld file using the value in the **Name** entry as the filename.

This version quits automatically after successfully generating the file
(the button now reads “Generate .PLD and Quit”).
"""

import datetime
import tkinter as tk
from tkinter import messagebox

# Default field values
DEFAULTS = {
    "Name": "mydesign",
    "PartNo": "A1",
    "Revision": "01",
    "Designer": "Your Name",
    "Company": "My Company",
    "Assembly": "PCBA1",
    "Location": "U1",
}


class PLDGenerator(tk.Tk):
    """Main application window."""

    def __init__(self):
        super().__init__()
        self.title(".PLD Template Generator")
        self.resizable(False, False)
        self.entries = {}
        self._create_widgets()

    # ------------------------------------------------------------------ UI
    def _create_widgets(self):
        """Create labels, entry boxes, and the Generate button."""
        row = 0
        for field, default in DEFAULTS.items():
            tk.Label(self, text=f"{field}:").grid(row=row, column=0, padx=5, pady=4, sticky="e")
            var = tk.StringVar(value=default)
            entry = tk.Entry(self, textvariable=var, width=40)
            entry.grid(row=row, column=1, padx=5, pady=4, sticky="w")
            self.entries[field] = var
            row += 1

        tk.Button(
            self,
            text="Generate .PLD and Quit",
            command=self.generate_pld_and_quit,
        ).grid(row=row, column=0, columnspan=2, pady=12)

    # ---------------------------------------------------------------- logic
    def generate_pld_and_quit(self):
        """Collect values, write the .pld file, then exit."""
        data = {k: v.get().strip() for k, v in self.entries.items()}
        if not data["Name"]:
            messagebox.showerror("Missing Name", "The Name field cannot be empty.")
            self.destroy()
            return

        filename = f"{data['Name']}.pld"
        timestamp = datetime.datetime.now().strftime("%m-%d-%y")

        lines = [
            f"Name        {data['Name']};",
            f"PartNo      {data['PartNo']}; //Device specific: this is burned into the device as the UES / User Signature when supported by a device. Often 8 bytes for PLD parts, 2 Bytes for CPLD parts. See device datasheet.",
            f"Revision    {data['Revision']};",
            f"Designer    {data['Designer']};",
            f"Company     {data['Company']};",
            f"Assembly    {data['Assembly']};",
            f"Location    {data['Location']}; //Designator on the PCB silkscreen for the device",
            f"Date        {timestamp};",
            "",
            "//Specify target device here. Common values are: g16V8a, g22v10, f1502isptqfp44, f1508ispplcc84.",
            "//See 'Compiler Mode Selection' in the device's datasheet as well as the WinCUPL Device Library for possible choices.",
            "Device      ;   //",
            "",
            "/* Pin declarations */",
            "/* e.g. PIN 1 = IN1; */",
            "",
            "/* Logic equations */",
            "/* e.g. OUT1 = IN1 & IN2; */",
            "",
        ]

        try:
            with open(filename, "w", encoding="utf-8") as fp:
                fp.write("\n".join(lines))
        except OSError as err:
            messagebox.showerror("File Error", f"Could not write file:\n{err}")
            self.destroy()
            return

        messagebox.showinfo("Success", f"Template saved as {filename}")
        self.destroy()


if __name__ == "__main__":
    PLDGenerator().mainloop()
