import turtle
import math
import tkinter as tk

ekran = turtle.Screen()
ekran._root.attributes("-fullscreen", False)
ekran.bgcolor("skyblue")
ekran.title("3D Oyun ama sadece turtle ile")
ekran.tracer(0)
ekran.listen()

kalem = turtle.Turtle()
kalem.speed("fastest")
kalem.hideturtle()

kamera_x = 0
kamera_y = 0
kamera_z = -300
kamera_acisi_y = 0
kamera_acisi_x = 0

hareket_x = 0
hareket_z = 0
ziplama = False
y_hareketi = 0

mouse_kilitli = False
fare_son_x = 0
fare_son_y = 0

SEKILLER = {
    "KUP": {
        "NOKTALAR": [
            [-50, -50, -50], [50, -50, -50], [50, 50, -50], [-50, 50, -50],
            [-50, -50, 50], [50, -50, 50], [50, 50, 50], [-50, 50, 50]
        ],
        "AYRITLAR": [
            (0, 1), (1, 2), (2, 3), (3, 0),
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        ],
        "YUZLER": [
            (0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4),
            (2, 3, 7, 6), (0, 3, 7, 4), (1, 2, 6, 5)
        ]
    }
}

ISIK_YONU = (0.8, 0.8, 1)

def dondur_ve_goster(noktalar, d):
    projeksiyonlu_noktalar = []
    MIN_Z = 1 
    
    for x, y, z in noktalar:
        x -= kamera_x
        y -= kamera_y
        z -= kamera_z

        x_don = x * math.cos(kamera_acisi_y) - z * math.sin(kamera_acisi_y)
        z_don = x * math.sin(kamera_acisi_y) + z * math.cos(kamera_acisi_y)

        y_don = y * math.cos(kamera_acisi_x) - z_don * math.sin(kamera_acisi_x)
        z_don = y * math.sin(kamera_acisi_x) + z_don * math.cos(kamera_acisi_x)

        z_don = max(z_don, MIN_Z)

        x_cizim = (x_don * d) / z_don
        y_cizim = (y_don * d) / z_don

        projeksiyonlu_noktalar.append((x_cizim, y_cizim, z_don))

    return projeksiyonlu_noktalar


def zemin_kontrol():
    global kamera_y, ziplama, y_hareketi
    if kamera_y < -10:
        kamera_y = -10
        ziplama = False
        y_hareketi = 0

def hareket_et():
    global kamera_x, kamera_z

    ileri_x = math.sin(kamera_acisi_y) * hareket_z
    ileri_z = math.cos(kamera_acisi_y) * hareket_z

    yana_x = math.sin(kamera_acisi_y + math.pi / 2) * hareket_x
    yana_z = math.cos(kamera_acisi_y + math.pi / 2) * hareket_x

    yeni_x = kamera_x + ileri_x + yana_x
    yeni_z = kamera_z + ileri_z + yana_z

    KUP_MERKEZ_X, KUP_MERKEZ_Z = 0, 0
    KUP_BOYUTU = 50
    MIN_KMESAFE = 70

    dx = yeni_x - KUP_MERKEZ_X
    dz = yeni_z - KUP_MERKEZ_Z
    mesafe = math.sqrt(dx**2 + dz**2)

    if mesafe > MIN_KMESAFE:
        kamera_x = yeni_x
        kamera_z = yeni_z


def normal_vektor(yuz, noktalar):
    p1, p2, p3, _ = [noktalar[i] for i in yuz]
    u = (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])
    v = (p3[0] - p1[0], p3[1] - p1[1], p3[2] - p1[2])
    normal = (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0]
    )
    uzunluk = math.sqrt(normal[0]**2 + normal[1]**2 + normal[2]**2)
    return (normal[0] / uzunluk, normal[1] / uzunluk, normal[2] / uzunluk)

def yuz_parlaklik(yuz, noktalar):
    normal = normal_vektor(yuz, noktalar)
    return max(0, normal[0] * ISIK_YONU[0] + normal[1] * ISIK_YONU[1] + normal[2] * ISIK_YONU[2])

def tonlanmis_kirmizi(oran):
    oran = max(0, min(1, oran))
    kirmizi = int(255 * oran)
    return f"#{kirmizi:02x}0000"

def sekil_ciz():
    kalem.clear()
    arkaplan_ciz()

    global kamera_y, ziplama, y_hareketi
    kalem.clear()
    hareket_et()

    if ziplama:
        kamera_y += y_hareketi
        y_hareketi -= 2
        if kamera_y <= 0:
            kamera_y = 0
            ziplama = False

    kalem.clear()
    noktalar = dondur_ve_goster(SEKILLER["KUP"]["NOKTALAR"], 300)
    yuzler = SEKILLER["KUP"]["YUZLER"]
    
    yuz_siralama = sorted(
        enumerate(yuzler), key=lambda y: sum(noktalar[i][2] for i in y[1]) / 4, reverse=True
    )

    for yuz_index, yuz in yuz_siralama:
        parlaklik = yuz_parlaklik(yuz, SEKILLER["KUP"]["NOKTALAR"])
        renk = tonlanmis_kirmizi(parlaklik)
        
        kalem.penup()
        kalem.goto(noktalar[yuz[0]][:2])
        kalem.pendown()
        kalem.fillcolor(renk)
        kalem.begin_fill()
        for nokta in yuz:
            kalem.goto(noktalar[nokta][:2])
        kalem.goto(noktalar[yuz[0]][:2])
        kalem.end_fill()

    ekran.update()
    ekran.ontimer(sekil_ciz, 10)

def ileri_bas(): global hareket_z; hareket_z = 5
def geri_bas(): global hareket_z; hareket_z = -5
def sola_bas(): global hareket_x; hareket_x = -5
def saga_bas(): global hareket_x; hareket_x = 5
def dur(): global hareket_x, hareket_z; hareket_x = 0; hareket_z = 0
def zipla():
    global ziplama, y_hareketi, kamera_y
    if not ziplama:
        ziplama = True
        y_hareketi = 15

def fare_hareket(event):
    global kamera_acisi_y, kamera_acisi_x, fare_son_x, fare_son_y

    if mouse_kilitli:
        dx = event.x - fare_son_x
        dy = event.y - fare_son_y

        kamera_acisi_y += math.radians(dx * 0.5)
        kamera_acisi_x -= math.radians(dy * 0.5) 

        max_acı = math.radians(89)
        kamera_acisi_x = max(-max_acı, min(max_acı, kamera_acisi_x))

        fare_son_x = event.x
        fare_son_y = event.y

def mouse_kilitle(event):
    global mouse_kilitli, fare_son_x, fare_son_y
    mouse_kilitli = True
    fare_son_x = event.x
    fare_son_y = event.y
    ekran.cv.config(cursor="none")
    ekran._root.attributes("-fullscreen", True) 

def mouse_serbest(event=None):
    global mouse_kilitli
    mouse_kilitli = False
    ekran.cv.config(cursor="arrow")
    ekran._root.attributes("-fullscreen", False) 


def arkaplan_ciz():
    kalem.penup()
    kalem.goto(-500, 500)
    kalem.pendown()
    kalem.fillcolor("skyblue")  
    kalem.begin_fill()
    
    for x, y in [(500, 500), (500, -500), (-500, -500)]:
        kalem.goto(x, y)
    
    kalem.goto(-500, 500)
    kalem.end_fill()

ekran.onkeypress(ileri_bas, "w")
ekran.onkeypress(geri_bas, "s")
ekran.onkeypress(sola_bas, "a")
ekran.onkeypress(saga_bas, "d")
ekran.onkeyrelease(dur, "w")
ekran.onkeyrelease(dur, "s")
ekran.onkeyrelease(dur, "a")
ekran.onkeyrelease(dur, "d")
ekran.onkeypress(zipla, "space")
ekran.onkeypress(lambda: mouse_serbest(), "Escape")

tk_root = ekran._root
tk_root.bind("<Motion>", fare_hareket)
tk_root.bind("<Button-1>", mouse_kilitle)
tk_root.bind("<Button-3>", mouse_serbest)

sekil_ciz()
ekran.mainloop()