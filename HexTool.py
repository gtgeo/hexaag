import numpy as np
import geopandas as gpd
import time
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
import shapely.ops
from shapely.ops import polygonize
from shapely.geometry import Point
from geopandas import GeoDataFrame
from shapely.ops import nearest_points




start_time = time.time()

# A distance transformation towards the Centroid of the centroids of the input geography is considered
#fact = 2
#By changing HexSize the size of the hexagons will change
HexSize = 50000
#If you select HexOrientation = 2 the hexagons will be rotated by 90 degrees
HexOrientation = 1
#Here you choose the format of the output. It supports a wide variety of formats like shapefiles (shp), geojson(geojson), geopackages(gpkg) etc.
GeographyType = "gpkg"

'''import any file supported by fiona
 as geodataframe'''

InputGeography = gpd.read_file(r"C:\Users\gt\Desktop\Hexagonal_Maps\Lower Tier Local Authority to Upper Tier Local Authority (December 2017) Lookup in England and Wales\Upper_Tier_Local_Authorities_December_2011_Boundaries.shp")


HexMapOutput = r"C:\Users\gt\Desktop\out\final."

def hexmaps(InputGeography, HexMapOutput, HexSize, HexOrientation, GeographyType):

    InputGeography.plot()
    CRS = InputGeography.crs

    InputGeography = GeoDataFrame(InputGeography, geometry=InputGeography.centroid, crs=CRS)
    featmultipoint = shapely.geometry.MultiPoint(InputGeography.geometry)
    centr =  featmultipoint.centroid
    centdf = gpd.GeoSeries(centr, crs=CRS)


    distances_from_centroid = []

    for feature in featmultipoint:
        geom = shapely.geometry.point.Point(feature)
        distance_between_pts = centr.distance(geom)
        distances_from_centroid.append(distance_between_pts)

    InputGeography['distance'] = distances_from_centroid
    distances = np.array(distances_from_centroid)

    #'''recalibrating the areas 
    #to have the median as origin 0,0'''
    #xo = []
    #for i  in InputGeography.geometry.x:
    #    new = i - centdf.geometry.x
    #    xo.append(new)

    #yo = []
    #for i in InputGeography.geometry.y:
    #    new = i - centdf.geometry.y
    #    yo.append(new)


    #x, y = np.array(xo) , np.array(yo)


    ###### A distance transformation towards the Centroid of the centroids of the input geography is considered######

    '''calulating distances of points/areas
     from the median and transforming those distances'''

    #gonia = np.degrees(np.arctan(x/y))
    #xi = np.where(x < 0, 180, 0)
    #yi = np.where(y < 0, 360, 0)

    #angle = abs(xi - yi) + gonia

    #f = abs(1 - distances/(fact*(distances.max())))
    #tr = f*distances

    #FeatClass['trans_distance'] = tr
    #x1 = np.cos(np.radians(angle))[:, 0]*np.array(tr)
    #y1 = np.sin(np.radians(angle))[:, 0]*np.array(tr)

    '''
    adding back median coordinates
    '''

    #X = x1 + np.array(centdf.geometry.x)
    #Y = y1 + np.array(centdf.geometry.y)

    #geometry1 = [Point(xy) for xy in zip(X, Y)]
    #FeatClass = GeoDataFrame(FeatClass, crs=CRS, geometry=geometry1)



    InputGeography = InputGeography.sort_values('distance', ascending=1)
    InputGeography = InputGeography.reset_index(drop=True)


    minX = InputGeography.geometry.x.min()
    minY = InputGeography.geometry.y.min()
    maxX = InputGeography.geometry.x.max()
    maxY = InputGeography.geometry.y.max()


    '''creating a mesh of points '''


    if HexOrientation == 1:
        x1 = np.arange(minX - 4 * HexSize, maxX + 4 * HexSize, HexSize)
        y1 = np.arange(minY - 2 * ((3 * HexSize) / np.sqrt(3)), maxY + 2 * ((3 * HexSize) / np.sqrt(3)), (3 * HexSize) / np.sqrt(3))
    # create the mesh based on these arrays
        X1, Y1 = np.meshgrid(x1, y1)
        X1 = X1.reshape((np.prod(X1.shape),))
        Y1 = Y1.reshape((np.prod(Y1.shape),))
    # create one-dimensional arrays x2 and y2
        x2 = np.arange((minX + float(HexSize) / 2) - 4 * HexSize, (maxX + HexSize / 2) + 4 * HexSize, HexSize)
        y2 = np.arange((minY + 3 * HexSize / (2 * np.sqrt(3))) - 2 * ((3 * HexSize) / np.sqrt(3)), (maxY + 3 * HexSize / (2 * np.sqrt(3))) + 2 * ((3 * HexSize) / np.sqrt(3)), (3 * HexSize) / np.sqrt(3))
    # create the mesh based on these arrays
        X2, Y2 = np.meshgrid(x2, y2)
        X2 = X2.reshape((np.prod(X2.shape),))
        Y2 = Y2.reshape((np.prod(Y2.shape),))
    elif HexOrientation ==2:
        y1 = np.arange(minY - 3 * HexSize, maxY + 3 * HexSize, HexSize)
        x1 = np.arange(minX - 2 * ((3 * HexSize) / np.sqrt(3)), maxX + 2 * ((3 * HexSize) / np.sqrt(3)), (3 * HexSize) / np.sqrt(3))
        X1, Y1 = np.meshgrid(x1, y1)
        X1 = X1.reshape((np.prod(X1.shape),))
        Y1 = Y1.reshape((np.prod(Y1.shape),))
        y2 = np.arange((minY + float(HexSize) / 2) - 3 * HexSize, (maxY + HexSize / 2) + 3 * HexSize, HexSize)
        x2 = np.arange((minX + 3 * HexSize / (2 * np.sqrt(3))) - 2 * ((3 * HexSize) / np.sqrt(3)), (maxX + 3 * HexSize / (2 * np.sqrt(3))) + 2 * ((3 * HexSize) / np.sqrt(3)), (3 * HexSize) / np.sqrt(3))
        X2, Y2 = np.meshgrid(x2, y2)
        X2 = X2.reshape((np.prod(X2.shape),))
        Y2 = Y2.reshape((np.prod(Y2.shape),))

    Xg = np.append(X1, X2)
    Yg = np.append(Y1, Y2)

    geometry2 = [Point(xy) for xy in zip(Xg, Yg)]

    #the grid points in shapely Multipoint object

    grid = shapely.geometry.MultiPoint(geometry2)

    '''applying Voronoi on the mesh of points
     to create a hexgrid'''

    vor = Voronoi(grid)

    lines= [
        shapely.geometry.LineString(vor.vertices[line])
        for line in vor.ridge_vertices
        if -1 not in line
    ]

    hexes = list(polygonize(lines))



    snap = []

    for i in InputGeography.geometry:
        grid = shapely.geometry.MultiPoint(geometry2)
        k = nearest_points(i, grid)
        t1, t2 = k
        snap.append(t2)
        geometry2.remove(t2)

    snaped = shapely.geometry.MultiPoint(snap)

    final = []

    for i in snaped:
        for h in hexes:
            con = h.contains(i)
            if con == True:
                final.append(h)

    hexagons = gpd.GeoSeries(final)

    hexagons.plot()
    InputGeography.plot()


    Final = GeoDataFrame(InputGeography, geometry=hexagons.geometry, crs=CRS)
    Final.plot(column='distance', scheme='QUANTILES', k=5, cmap='OrRd', legend=True)
    Final.to_file(HexMapOutput+GeographyType)#, driver='ESRI Shapefile')
    Final['coords'] = Final['geometry'].apply(lambda x: x.representative_point().coords[:])
    Final['coords'] = [coords[0] for coords in Final['coords']]
    Final.plot()
    #for idx, row in Final.iterrows():
    #    plt.annotate(s=row['utla11nm'], xy=row['coords'],horizontalalignment='center')
