import sys
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as msg


class ExchangeGui:
    """
    Class creates GUI that allows to exchange currencies in easy way
    """
    def __init__(self, data):
        self.data = data
        self.gui()

    def gui(self):
        """
        main function maintaining GUI
        """
        if self.data.df is None:
            self.error_no_data()
        self.root = self.gui_main()
        self.gui_frame_top()
        self.gui_frame_middle()
        self.gui_frame_bottom()
        if not self.data.online:
            self.root.after_idle(self.info_show)
        self.root.mainloop()
        return None

    def gui_main(self):
        """
        function creates root
        :return: root
        """
        self.x_max = 500
        self.y_max = 305
        root = tk.Tk()
        root.title("Karkulator walut")
        root.geometry(f"{self.x_max}x{self.y_max}")
        root.resizable(False, False)
        return root

    def gui_frame_top(self):
        """
        function maintain top part of the GUI (left frame(from currency label, checkbox, label), middle frame(switch button),
        right frame(to currency label, checkbox, label))
        """
        currency_codes = [i for i in self.data.df.index]

        # Frame top left
        self.if_ftl_label = False  # just a creating helper :)

        self.ftl = tk.Frame(self.root, height=150, width=200)
        self.ftl.place(x=30, y=30)

        self.variable_from = tk.StringVar(self.ftl)
        self.variable_from.set("PLN")
        self.from_label_update()
        self.variable_from.trace_add("write", self.from_label_update)

        # Frame top right
        self.if_ftr_label = False  # just a creating helper :)

        self.ftr = tk.Frame(self.root, height=150, width=200)
        self.ftr.place(x=315, y=30)

        self.variable_to = tk.StringVar(self.ftr)
        self.variable_to.set("EUR")
        self.to_label_update()
        self.variable_to.trace_add("write", self.to_label_update)

        # Frame top middle
        self.ftm = tk.Frame(self.root, height=200, width=50)
        self.ftm.place(x=210, y=65)

        switch = tk.Button(self.ftm, text="<->", width=7, command=self.switch)
        switch.pack()

        # From currency
        from_currency_label_1 = tk.Label(self.ftl, text='Przelicz z: ')
        from_currency_label_1.config(font=("Courier", 14))
        from_currency_label_1.pack(side=tk.TOP)

        self.from_currency_box = ttk.Combobox(self.ftl, textvariable=self.variable_from, values=currency_codes, width=10,
                                              state="readonly", justify="center")
        self.from_currency_box.pack()

        # To currency
        to_currency_label = tk.Label(self.ftr, text='Przelicz na: ')
        to_currency_label.config(font=("Courier", 14))
        to_currency_label.pack(side=tk.TOP)

        to_currency_box = ttk.Combobox(self.ftr, textvariable=self.variable_to, values=currency_codes, width=10,
                                       state="readonly", justify="center")
        to_currency_box.pack()

        return None

    def gui_frame_middle(self):
        """
        function maintain middle part of the GUI (top frame(from currency label, entry, label),
        bottom frame(to currency button, label, label))
        """
        # frame middle top
        fmt = tk.Frame(self.root, height=75, width=250)
        fmt.place(x=105, y=130)

        self.variable_amount = tk.StringVar(fmt)

        label_type_amount = tk.Label(fmt, text="Wpisz kwotę:")
        label_type_amount.config(font=("Courier", 14))
        label_type_amount.pack(side=tk.TOP)

        entry_type_amount = tk.Entry(fmt, width=40, textvariable=self.variable_amount)
        entry_type_amount.pack(side=tk.LEFT)

        label_currency_from_code = tk.Label(fmt, textvariable=self.variable_from)
        label_currency_from_code.config(font=("Courier", 14))
        label_currency_from_code.pack(side=tk.RIGHT)

        # frame middle bottom
        self.fmb = tk.Frame(self.root, height=75, width=250)
        self.fmb.place(x=105, y=190)

        calculate_button = tk.Button(self.fmb, text="Przelicz!", width=40, command=self.button_calculate)
        calculate_button.pack()
        self.root.bind('<Return>', self.button_calculate)

        self.label_display_result = ttk.Label(self.fmb, text="0")
        self.label_display_result.config(font=("Courier", 14))
        self.label_display_result.pack(side=tk.LEFT)

        label_currency_to_code = tk.Label(self.fmb, textvariable=self.variable_to)
        label_currency_to_code.config(font=("Courier", 14))
        label_currency_to_code.pack(side=tk.RIGHT)

        return None

    def gui_frame_bottom(self):
        """
        function maintain bottom part of the GUI (button)
        """
        fb = tk.Frame(self.root, height=40, width=150)
        fb.place(x=220, y=260)

        button_exit = tk.Button(fb, text="Zakończ", width=7, command=self.program_end)
        button_exit.pack()
        self.root.bind('<Escape>', self.program_end)

        return None

    def from_label_update(self, *args):
        """
        function to update label describing from currency
        :param args: just to avoid errors
        """
        text = self.variable_from.get()
        if self.if_ftl_label:
            self.ftl_label.destroy()

        self.ftl_label = tk.Label(self.ftl, text=self.data.df.loc[text, 'Nazwa waluty'])
        self.ftl_label.config(font=("Courier", 14))
        self.ftl_label.pack(side=tk.BOTTOM)
        self.if_ftl_label = True
        return None

    def to_label_update(self, *args):
        """
        function to update label describing to currency
        :param args: just to avoid errors
        """
        text = self.variable_to.get()
        if self.if_ftr_label:
            self.ftr_label.destroy()

        self.ftr_label = tk.Label(self.ftr, text=self.data.df.loc[text, 'Nazwa waluty'])
        self.ftr_label.config(font=("Courier", 14))
        self.ftr_label.pack(side=tk.BOTTOM)
        self.if_ftr_label = True
        return None

    def switch(self, *args):
        """
        function is used as command by switch button from top middle frame to switch from and to currencies
        :param args: just to avoid errors
        """
        b1, b2 = self.variable_from.get(), self.variable_to.get()
        self.variable_from.set(b2)
        self.variable_to.set(b1)

    def button_calculate(self, *args):
        """
        function is used as command by calculate button from middle top frame to perform calculation
        :param args: just to avoid errors
        """
        if self.variable_amount.get() and self.isanum(self.variable_amount.get()):
            fc, tc, a = self.variable_from.get(), self.variable_to.get(), self.variable_amount.get()
            a = self.comma_to_dot_input(a)
            result = self.data.exchange(fc, tc, float(a))

            self.label_display_result.destroy()
            self.label_display_result = ttk.Label(self.fmb, text=str(result))
            self.label_display_result.config(font=("Courier", 14))
            self.label_display_result.pack(side=tk.LEFT)
        else:
            msg.showerror("Błąd", "Wprowadzona wartość nie jest poprawna")

        return None

    def comma_to_dot_input(self, string):
        """
        changes accidentally typed comma instead of dot into middle top entry
        :param string: input
        :return: string
        """
        return string.replace(",", ".")

    def isanum(self, string):
        """
        function checks if input is an acceptable argument (not negative number)
        :param string: input from middle top entry
        :return: bool
        """
        dot = True
        if not string[0].isnumeric():
            return False
        if string[0] == "0" and len(string) > 1:
            if string[1] not in [".", ","]:
                return False
        for i in string:
            if not i.isnumeric():
                if i in [".", ","]:
                    if dot:
                        dot = False
                    else:
                        return False
                else:
                    return False

        return True

    def program_end(self, *args):
        """
        used to end program and close GUI
        :param args: just to avoid errors
        """
        self.root.destroy()
        sys.exit(0)

    def error_no_data(self):
        """
        function called by self.data func when there is no connection and no saved data in directory so the currency
        rates are not available for the program
        """
        root = tk.Tk()
        root.title("Karkulator walut")
        root.geometry("500x150")
        root.resizable(False,False)
        t_box = tk.Text(root, width=500, height=150)
        t_box.pack()
        t_box.insert(tk.END, "Brak danych", ("h1"))
        t_box.insert(tk.END, "\n")
        t_box.insert(tk.END, "Nie można pobrać danych:\nsprawdź połączenie z internetem lub dostępność pliku\n'kursy.csv'")
        t_box.tag_add("h1", "1.0", "1.0")
        t_box.tag_config("h1", justify=tk.CENTER, font=("Times New Roman", 20))
        tk.mainloop()
        sys.exit(1)

    def info_show(self):
        """
        function informs that used currency rates may not be up to date
        """
        msg.showinfo("Dane", f"Użyto archiwalnych danych:\n {self.data.name}")
        return None
