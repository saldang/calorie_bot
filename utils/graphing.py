import matplotlib.pyplot as plt
import io

def plot_calorie_summary(data):
    dates = [row[0] for row in data]
    calories = [row[1] for row in data]

    plt.figure(figsize=(8, 4))
    plt.plot(dates, calories, marker='o')
    plt.title("Consumo calorico ultimi 7 giorni")
    plt.xlabel("Data")
    plt.ylabel("Calorie")
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return buf