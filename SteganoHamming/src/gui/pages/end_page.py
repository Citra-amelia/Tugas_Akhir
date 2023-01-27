import tkinter as tk
import src.helper.gui as hg


class EndPage(tk.Frame):
    def __init__(self, parent, controller, title, stegano_type, file_dir, psnr, mse):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        heading = tk.Label(
            self,
            bg="white",
            fg="black",
            text=title,
            font='none 24 bold'
        )
        heading.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        if (stegano_type == "Image"):
            output_frame = hg.create_frame(self, 2)
            hg.create_label(output_frame, 'Output Image:', 0, 0)
            hg.create_label(output_frame, file_dir, 0, 1)
            
            pos_back = 4
            if (psnr is not None):
                psnr_frame = hg.create_frame(self, 3)
                hg.create_label(psnr_frame, 'PSNR = ' + str(psnr), 0, 0)
                pos_back += 1

                mse_frame = hg.create_frame(self,4)
                hg.create_label(mse_frame, 'MSE = ' + str(mse), 0, 0)
                pos_back += 1

            back_frame = hg.create_frame(self, pos_back)
            hg.create_button(back_frame, 'Back',
                            lambda: self.controller.show_frame("StartPage"), 0, 1)
        else:
            back_frame = hg.create_frame(self, 2)
            hg.create_button(back_frame, 'Back',
                            lambda: self.controller.show_frame("StartPage"), 0, 1)
