from tkinter import Tk
import tkinter as tk

from classifier.classifier import classify

import utilities.interpreter as setup
import utilities.util as util
from vectors_handling.vector_provider import provide_vectors

window_name = 'NLI GUI Interface'
default_color ='#a7aac4'
output_color = '#edeef3'
HEIGHT = 500
WIDTH = 300


class window(tk.Frame):
    def __init__(self, parent=None):
        canvas = tk.Canvas(parent, height=HEIGHT, width=WIDTH)
        canvas.pack()
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.pack()
        self.make_widgets(parent)


    def make_widgets(self, parent=None):

        main_frame = tk.Frame(parent, bg='white', height=HEIGHT, width=WIDTH)
        main_frame.place(relwidth=1, relheight=1)

        label = tk.Label(main_frame, text='NLI GUI Interface', bg='lightblue')
        label.place(relwidth=1, relheight=0.05, relx=0, rely=0)

        input_frame = tk.Frame(main_frame, bg=default_color, height=HEIGHT, width=WIDTH)
        input_frame.place(relwidth=1, relheight=0.65, rely=0.05)

        output_frame = tk.Frame(main_frame, bg=default_color, height=HEIGHT, width=WIDTH)
        output_frame.place(relwidth=1, relheight=0.3, rely=0.7)

        def callback(selection):
            check_functionwords(selection)
            return selection

        # Feature selection #
        default_feature = tk.StringVar()
        default_feature.set(setup.possible_inputs[0][0])

        feature_entry = tk.OptionMenu(input_frame, default_feature, *setup.possible_inputs[0], command=callback)
        tk.Label(input_frame, text='Feature', bg=default_color).place(relwidth=0.2, relheight=0.1, relx=0, rely=0.05)
        feature_entry.place(relwidth=0.8, relheight=0.1, relx=0.2, rely=0.05)
        # Feature selection #


        # Type selection #
        default_type = tk.StringVar()
        default_type.set(setup.possible_inputs[1][0])

        type_entry = tk.OptionMenu(input_frame, default_type, *setup.possible_inputs[1])
        tk.Label(input_frame, text='Type', bg=default_color).place(relwidth=0.2, relheight=0.1, relx=0, rely=0.15)
        type_entry.place(relwidth=0.8, relheight=0.1, relx=0.2, rely=0.15)

        # Type selection #


        # Domain selection #
        selected_domain = tk.IntVar()

        tk.Label(input_frame, text='Domain', bg=default_color).place(relwidth=0.2, relheight=0.1, relx=0, rely=0.25)
        tk.Radiobutton(input_frame, text=setup.possible_inputs[2][0], variable=selected_domain, value=1, indicatoron=False).place(relwidth=0.2, relheight=0.1, relx=0.2, rely=0.25)
        tk.Radiobutton(input_frame, text=setup.possible_inputs[2][1], variable=selected_domain, value=2, indicatoron=False).place(relwidth=0.2, relheight=0.1, relx=0.4, rely=0.25)
        # Domain selection #


        # Threads selection #
        default_threads = tk.IntVar(parent)
        default_threads.set(util.get_cpu_count())

        threads_entry = tk.Spinbox(input_frame, from_= 1, to=util.get_cpu_count(), textvariable=default_threads)

        tk.Label(input_frame, text='Threads', bg=default_color).place(relwidth=0.2, relheight=0.1, relx=0, rely=0.35)
        threads_entry.place(relwidth=0.2, relheight=0.1, relx=0.2, rely=0.35)
        # Threads selection #

        # Iterations selection #
        default_iterations = tk.IntVar(parent)
        default_iterations.set(20000)

        iterations_entry = tk.Spinbox(input_frame, from_=1, to=1000000, textvariable=default_iterations)

        tk.Label(input_frame, text='Iterations', bg=default_color).place(relwidth=0.2, relheight=0.1, relx=0, rely=0.45)
        iterations_entry.place(relwidth=0.2, relheight=0.1, relx=0.2, rely=0.45)
        # Iterations selection #

        # Synchronized functionwords #
        default_sync = tk.IntVar(parent)
        default_sync.set(400)

        sync_label = tk.Label(input_frame, text='Number of functionwords', bg=default_color)
        sync_entry = tk.Spinbox(input_frame, from_=1, to=400, textvariable=default_sync)

        def check_functionwords(selection):
            if selection == 'synchronized_functionwords':
                sync_label.place(relwidth=0.5, relheight=0.1, relx=0, rely=0.88)
                sync_entry.place(relwidth=0.2, relheight=0.1, relx=0.5, rely=0.88)
            else:
                sync_label.place_forget()
                sync_entry.place_forget()
        # Synchronized functionwords #


        def get_attributes():
            gui_feature = str(default_feature.get())
            gui_type = str(default_type.get())
            required_label = tk.Label(input_frame, text='REQUIRED', fg='red', font=30, bg=default_color)
            if selected_domain.get() == 1:
                gui_domain = 'in'
            elif selected_domain.get() == 2:
                gui_domain = 'out'
            else:
                required_label.place(relwidth=0.4, relheight=0.1, relx=0.6, rely=0.25)
                raise ValueError('Domain not specified')

            gui_threads = default_threads.get()
            gui_iterations = default_iterations.get()
            if gui_feature == 'synchronized_functionwords':
                gui_numOfFunctionwords = default_sync.get()
            else:
                gui_numOfFunctionwords = 0

            setup.set_params(gui_feature, gui_type, gui_domain, gui_threads, gui_iterations, gui_numOfFunctionwords)


        def update_log(_text):
            print(output_label.cget('text'))
            output_label.configure(text="{}\n[{}] {}".format(output_label.cget('text'), util.get_time(), _text))
            app.update()

        def submit_button():
            output_label.configure(text="")
            get_attributes()
            update_log('Processing vectors...')
            users, countries = provide_vectors()  # Generate vectors for the classification task

            #  For out-domain, require in domain vectors as well
            if setup.domain == 'out':
                setup.domain = 'in'
                update_log('Processing more vectors...')
                in_users, in_countries = provide_vectors()
                setup.domain = 'out'
                update_log('Classifing...')
                result = classify(users, countries, in_users, in_countries)

            else:
                update_log('Classifing...')
                result = classify(users, countries)

            update_log('Finished\n'
                       'score: ' + "%.3f" % round(result,3))
            util.write_scores(result)

        submit = tk.Button(input_frame, text ='Submit', bg='white', fg='blue', command=lambda: submit_button())
        submit.place(relwidth=0.25, relheight=0.1, relx = 0.73, rely = 0.88)

        output_text = tk.StringVar()

        output_label = tk.Label(output_frame, text=output_text.get(), anchor='n',justify='left', font=20, bg=output_color)
        output_label.place(relwidth=1, relheight=1, relx=0, rely=0)

class gui_interface():
    def __init__(self):
        root = Tk()
        root.title(window_name)
        global app
        app = window(root)
        app.mainloop()