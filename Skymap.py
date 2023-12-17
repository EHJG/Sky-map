from skyfield.api import Star, load, wgs84, N,S,E,W
from skyfield.data import hipparcos
from matplotlib import pyplot as plt
from skyfield.projections import build_stereographic_projection
from matplotlib.collections import LineCollection
import numpy as np
import leer_escribir_archivos as rw
import dsos

ts = load.timescale()
t = ts.utc(2023, 11, 11)
planets = load('de421.bsp')
tierra = planets['earth']
degrees = 0
field_of_view_degrees = 180.0
limiting_magnitude = 6.0
dso_limit_magnitude = 8.0

# Cargar DSO's de stellarium
with open(u'C:\\Carpeta de trabajo\\catalog.txt') as f:
    dsodata = dsos.load_dataframe(f)

# Cargar starnames (No he conseguido la forma de leer el Json correctamente para que lo muestre en pantalla junto al mapeado aun)
# with open('C:\Carpeta de trabajo\IAU-CSN.json') as f: 
# starnames = dsos.star_dataframe(f)

# Cargar Catalogo Hipparcos
with load.open(hipparcos.URL) as f: 
    df = hipparcos.load_dataframe(f)
bright_stars = Star.from_dataframe(df)

# Datos para imprimir direccion de estrellas especificas/disponibles
observer = tierra + wgs84.latlon(9.68 * N, 63.239980 *W, elevation_m=4)

#Funcion para filtrar estrellas segun su magnitud
def imprimir_filtrado(df, magnitud):
    df = df[df['magnitude'] <= magnitud]
    bright_stars = Star.from_dataframe(df)
    astro = observer.at(t).observe(bright_stars)
    print('Luego de filtrar en ese rango de magnitud, se encuentran {} estrellas'.format(len(df)))
    ra, dec, distance = astro.radec()
    print('Hay {} ascensiones'.format(len(ra.hours)))
    print('y {} declinaciones'.format(len(dec.degrees)))

#Funcion para imprimir direccion y distancia de estrellas especificas
def imprimir_direccion (df, magnitud, lok=0):
    if lok == 0:
        df = df[df['magnitude'] <= magnitud]
        bright_stars = Star.from_dataframe(df)
        punto = observer.at(t).observe(bright_stars)
        alt, az, distanc = punto.apparent().altaz()
        print(alt.dstr())
        print(az.dstr())
        print(distanc)
    else:
        bright_stars = Star.from_dataframe(df.loc[lok])
        punto = observer.at(t).observe(bright_stars)
        alt, az, distanc = punto.apparent().altaz()
        print(alt.dstr())
        print(az.dstr())
        print(distanc)

#Dibujando posiciones de las estrellas en el diagrama
def crear_mapeado (latitud, direccion_1, longitud, direccion_2, elevacion):

    # Constantes para mostrar estrellas
    site = wgs84.latlon(latitud * direccion_1, longitud *direccion_2, elevacion).at(t)
    ra, dec, distance = site.radec()
    center_object = Star(ra=ra, dec=dec)
    center = tierra.at(t).observe(center_object)
    projection = build_stereographic_projection(center)

    star_positions = tierra.at(t).observe(Star.from_dataframe(df))
    df['x'], df['y'] = projection(star_positions)

    dso_positions = tierra.at(t).observe(Star.from_dataframe(dsodata))
    dsodata['x'], dsodata['y'] = projection(dso_positions)
                    
    bright_stars2 = (df.magnitude <= limiting_magnitude)
    magnitude = df['magnitude'][bright_stars2]
    marker_size = 100 * 10 ** (magnitude / -2.5)

    bright_dsos = (dsodata.magnitude <= dso_limit_magnitude)
    dso_magnitude = dsodata['magnitude'][bright_dsos]
    dso_size = (0.9 + dso_limit_magnitude - dso_magnitude) ** 2.0

    fig, ax = plt.subplots(figsize=[10,10])

    horizon = []
    h0 = projection(site.from_altaz(alt_degrees=0, az_degrees=0.0))
    for i in range(1, 73):
        delta = 5.0
        current = i * delta
        h1 = projection(site.from_altaz(alt_degrees=0, az_degrees=current))
        horizon.append([h0, h1])
        h0 = h1

    ax.add_collection(LineCollection(horizon,
                            colors='#00f2', linewidths=1, linestyle='dashed', zorder=-1, alpha=0.5))

    #Coloco la vision de 180° desde una perspectiva de primera persona
    angle = np.pi - field_of_view_degrees / 360.0 * np.pi
    limit = np.sin(angle) / (1.0 - np.cos(angle))

    #Empiezo con el diagrama de dispersion
    ax.scatter(df['x'][bright_stars2], df['y'][bright_stars2],
    s=marker_size, color='black', marker='.', linewidths=0, 
    zorder=2)

    ax.scatter(dsodata['x'][bright_dsos], dsodata['y'][bright_dsos],
            s=dso_size, color='red', marker='.')

    #Cargar nombres de estrellas en el mapa (No he consegui aun un catalogo que funcione con los nombres de estrellas)
    '''
    for i, s in df[bright_stars2].iterrows():
        if -limit < s['x'] < limit and -limit < s['y'] < limit:
            print(i)
            if i in starnames:
                print(f"star {starnames[i]} mag {s['magnitude']}")
                ax.text(s['x'] + 0.004, s['y'] - 0.004, starnames[i], color='white',
                        ha='left', va='top', fontsize=9, weight='bold', zorder=1).set_alpha(0.5)
    '''
    for i, d in dsodata[bright_dsos].iterrows():
        if -limit < d['x'] < limit and -limit < d['y'] < limit:
            print(f"dso {d['label']} mag {d['magnitude']}")
            ax.text(d['x'] + 0.004, d['y'] - 0.004, d['label'], color='red',
                    ha='left', va='top', fontsize=9, weight='bold', zorder=1).set_alpha(0.5)

    #Marcamos los limites del grafico
    ax.set_xlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.xaxis.set_visible(True)
    ax.yaxis.set_visible(True)
    ax.set_aspect(1.0)
    ax.grid(True)
    ax.set(title='Estrellas visibles desde tu posicion')
    fig.savefig('bright_stars.png')

    plt.show()