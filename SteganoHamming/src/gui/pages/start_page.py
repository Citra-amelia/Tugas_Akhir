import tkinter as tk


class StartPage(tk.Frame):
    def donothing(self):
        filewin = tk.Toplevel(self.master)
        button = tk.Button(filewin, text="Do nothing button")
        button.pack()

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        heading = tk.Label(
            self,
            bg="white",
            fg="black",
            text='Kode Hamming Kedalam Steganografi BPCS',
            font='none 20 bold'
        )
        heading.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        text_elements = [
            "Hide mesage to picture",
            "Extract mesage from picture",
        ]

        command_elements = [
            lambda: controller.show_frame("ImageInsertionForm"),
            lambda: controller.show_frame("ImageExtractForm"),
        ]

        index = 0
        for text in text_elements:
            button = tk.Button(
                self,
                bg='white',
                fg='black',
                text=text,
                command=command_elements[index],
                width=50,
                height=2
            )
            button.place(relx=0.5, rely=0.1*(index+2), anchor=tk.CENTER)
            index += 1
