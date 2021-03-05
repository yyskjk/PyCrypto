from tkinter import *
from tkinter import messagebox, Menu
import requests
import json
import sqlite3

pycrypto = Tk()
pycrypto.title("My Crypto Portfolio")
pycrypto.iconbitmap("favicon.ico")

con = sqlite3.connect('coin.db')
cursorObj = con.cursor()
cursorObj.execute("CREATE TABLE IF NOT EXISTS coin(id INTEGER PRIMARY KEY, symbol TEXT, amount INTEGER, price REAL)")
con.commit()


def reset():
    for cell in pycrypto.winfo_children():
        cell.destroy()
    app_nav()
    app_header()
    my_portfolio()


def app_nav():
    def clear_all():
        cursorObj.execute("DELETE FROM coin")
        con.commit()
        reset()
        messagebox.showinfo("Portfolio Notification", "Portfolio Cleared - Add new coins!")

    def close_app():
        pycrypto.destroy()

    menu = Menu(pycrypto)
    file_item = Menu(menu)
    file_item.add_command(label="Clear portfolio", command=clear_all)
    file_item.add_command(label="Close App", command=close_app)
    menu.add_cascade(label="File", menu=file_item)
    pycrypto.config(menu=menu)


def my_portfolio():
    api_request = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=10"
                               "&convert=USD&CMC_PRO_API_KEY=4ba63929-4189-42c8-aac9-e7999f97ef23")
    api = json.loads(api_request.content)

    cursorObj.execute("SELECT * FROM coin")
    coins = cursorObj.fetchall()

    def font_clr(x):
        if x > 0:
            return "green"
        elif x < 0:
            return "red"
        else:
            return "black"

    def insert_coin():
        cursorObj.execute("INSERT INTO coin(symbol, amount, price) VALUES(?, ?, ?)",
                          (symbol_txt.get(), amount_txt.get(), price_txt.get()))
        con.commit()
        reset()
        messagebox.showinfo("Portfolio Notification", "Coin added to portfolio successfully")

    def update_coin():
        cursorObj.execute("UPDATE coin SET symbol=?, amount=?, price=? WHERE id=?",
                          (symbol_upd.get(), amount_upd.get(), price_upd.get(), portid.get()))
        con.commit()
        reset()
        messagebox.showinfo("Portfolio Notification", "Coin updated in portfolio successfully")

    def del_coin():
        cursorObj.execute("DELETE FROM coin WHERE id=?", (portid_del.get(),))
        con.commit()
        reset()
        messagebox.showinfo("Portfolio Notification", "Coin deleted from portfolio successfully")

    tot = 0
    c_row = 1
    tot_cv = 0
    tot_amtpaid = 0
    for i in range(10):
        for coin in coins:
            if api["data"][i]["symbol"] == coin[1]:
                tot_amt_paid = coin[3] * coin[2]
                cur_val = api["data"][i]["quote"]["USD"]["price"] * coin[2]
                pl_per_coin = api["data"][i]["quote"]["USD"]["price"] - coin[3]
                tot_pl = pl_per_coin * coin[2]
                tot += tot_pl
                tot_cv += cur_val
                tot_amtpaid += tot_amt_paid

                portfolio_id = Label(pycrypto, text=coin[0], bg="#F3F4F6", fg="black", font="Lato 12",
                                     padx="2", pady="2", borderwidth=2, relief="groove")
                portfolio_id.grid(row=c_row, column=0, sticky=N + S + E + W)

                name = Label(pycrypto, text=api["data"][i]["symbol"], bg="#F3F4F6", fg="black", font="Lato 12",
                             padx="2", pady="2", borderwidth=2, relief="groove")
                name.grid(row=c_row, column=1, sticky=N + S + E + W)

                price = Label(pycrypto, text="${0:.2f}".format(api["data"][i]["quote"]["USD"]["price"]), bg="#F3F4F6",
                              fg="black", font="Lato 12", padx="2", pady="2", borderwidth=2, relief="groove")
                price.grid(row=c_row, column=2, sticky=N + S + E + W)

                no_coins = Label(pycrypto, text=coin[2], bg="#F3F4F6", fg="black", font="Lato 12",
                                 padx="2", pady="2", borderwidth=2, relief="groove")
                no_coins.grid(row=c_row, column=3, sticky=N + S + E + W)

                amount_paid = Label(pycrypto, text="${0:.2f}".format(tot_amt_paid), bg="#F3F4F6", fg="black",
                                    font="Lato 12", padx="2", pady="2", borderwidth=2, relief="groove")
                amount_paid.grid(row=c_row, column=4, sticky=N + S + E + W)

                current_val = Label(pycrypto, text="${0:.2f}".format(cur_val), bg="#F3F4F6", fg="black", font="Lato 12",
                                    padx="2", pady="2", borderwidth=2, relief="groove")
                current_val.grid(row=c_row, column=5, sticky=N + S + E + W)

                pl_coin = Label(pycrypto, text="${0:.2f}".format(pl_per_coin), bg="#F3F4F6", fg=font_clr(pl_per_coin),
                                font="Lato 12",
                                padx="2", pady="2", borderwidth=2, relief="groove")
                pl_coin.grid(row=c_row, column=6, sticky=N + S + E + W)

                total_pl = Label(pycrypto, text="${0:.2f}".format(tot_pl), bg="#F3F4F6", fg=font_clr(tot_pl),
                                 font="Lato 12",
                                 padx="2", pady="2", borderwidth=2, relief="groove")
                total_pl.grid(row=c_row, column=7, sticky=N + S + E + W)

                c_row += 1
    # ---------ADD COIN---------------
    symbol_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    symbol_txt.grid(row=c_row + 1, column=1)

    price_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    price_txt.grid(row=c_row + 1, column=2)

    amount_txt = Entry(pycrypto, borderwidth=2, relief="groove")
    amount_txt.grid(row=c_row + 1, column=3)

    add_coin = Button(pycrypto, text="ADD COIN", command=insert_coin, bg="grey", fg="black", font="Lato 12",
                      padx="2", pady="2", borderwidth=2, relief="groove")
    add_coin.grid(row=c_row + 1, column=4, sticky=N + S + E + W)
    # ----------UPDATE COIN----------------
    portid = Entry(pycrypto, borderwidth=2, relief="groove")
    portid.grid(row=c_row + 2, column=0)

    symbol_upd = Entry(pycrypto, borderwidth=2, relief="groove")
    symbol_upd.grid(row=c_row + 2, column=1)

    price_upd = Entry(pycrypto, borderwidth=2, relief="groove")
    price_upd.grid(row=c_row + 2, column=2)

    amount_upd = Entry(pycrypto, borderwidth=2, relief="groove")
    amount_upd.grid(row=c_row + 2, column=3)

    update_coin = Button(pycrypto, text="UPDATE COIN", command=update_coin, bg="grey", fg="black", font="Lato 12",
                         padx="2", pady="2", borderwidth=2, relief="groove")
    update_coin.grid(row=c_row + 2, column=4, sticky=N + S + E + W)
    # -------------DELETE COIN---------------
    portid_del = Entry(pycrypto, borderwidth=2, relief="groove")
    portid_del.grid(row=c_row + 3, column=0)

    del_coin = Button(pycrypto, text="DELETE COIN", command=del_coin, bg="grey", fg="black", font="Lato 12",
                      padx="2", pady="2", borderwidth=2, relief="groove")
    del_coin.grid(row=c_row + 3, column=4, sticky=N + S + E + W)
    # --------------------------------------
    tot_a_p = Label(pycrypto, text="${0:.2f}".format(tot_amtpaid), bg="#F3F4F6", fg="black", font="Lato 12",
                    padx="2", pady="2", borderwidth=2, relief="groove")
    tot_a_p.grid(row=c_row, column=4, sticky=N + S + E + W)

    tot_c_v = Label(pycrypto, text="${0:.2f}".format(tot_cv), bg="#F3F4F6", fg="black", font="Lato 12",
                    padx="2", pady="2", borderwidth=2, relief="groove")
    tot_c_v.grid(row=c_row, column=5, sticky=N + S + E + W)

    overall_pl = Label(pycrypto, text="${0:.2f}".format(tot), bg="#F3F4F6", fg=font_clr(tot), font="Lato 12",
                       padx="2", pady="2", borderwidth=2, relief="groove")
    overall_pl.grid(row=c_row, column=7, sticky=N + S + E + W)

    api = ""

    refresh = Button(pycrypto, text="REFRESH", command=reset, bg="grey", fg="black", font="Lato 12",
                     padx="2", pady="2", borderwidth=2, relief="groove")
    refresh.grid(row=c_row + 1, column=7, sticky=N + S + E + W)


def app_header():
    portfolio_id = Label(pycrypto, text="Portfolio ID", bg="#142E54", fg="white", font="Lato 12 bold", padx="5",
                         pady="5",
                         borderwidth=2,
                         relief="groove")
    portfolio_id.grid(row=0, column=0, sticky=N + S + E + W)

    name = Label(pycrypto, text="Coin", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5",
                 borderwidth=2,
                 relief="groove")
    name.grid(row=0, column=1, sticky=N + S + E + W)

    price = Label(pycrypto, text="Price", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5",
                  borderwidth=2,
                  relief="groove")
    price.grid(row=0, column=2, sticky=N + S + E + W)

    no_coins = Label(pycrypto, text="Coins owned", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5",
                     borderwidth=2, relief="groove")
    no_coins.grid(row=0, column=3, sticky=N + S + E + W)

    amount_paid = Label(pycrypto, text="Amount Paid", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5",
                        borderwidth=2, relief="groove")
    amount_paid.grid(row=0, column=4, sticky=N + S + E + W)

    current_val = Label(pycrypto, text="Current Value", bg="#142E54", fg="white", font="Lato 12 bold", padx="5",
                        pady="5",
                        borderwidth=2, relief="groove")
    current_val.grid(row=0, column=5, sticky=N + S + E + W)

    pl_coin = Label(pycrypto, text="P/L per coin", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5",
                    borderwidth=2, relief="groove")
    pl_coin.grid(row=0, column=6, sticky=N + S + E + W)

    total_pl = Label(pycrypto, text="Total P/L", bg="#142E54", fg="white", font="Lato 12 bold", padx="5", pady="5",
                     borderwidth=2, relief="groove")
    total_pl.grid(row=0, column=7, sticky=N + S + E + W)


app_nav()
app_header()
my_portfolio()
pycrypto.mainloop()

cursorObj.close()
con.close()
