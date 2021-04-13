import os
from typing import Dict
from typing import Tuple

import folium
import geopandas as gpd
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static


def prepare_map(map_center: Tuple, other_interest_points: dict, df: pd.DataFrame):
    route_map = folium.Map(location=map_center, zoom_start=11, width="80%", height="80%")
    for location, loc_coordinates in other_interest_points.items():
        folium.Marker(loc_coordinates, color="purple", tooltip=location, radius=3).add_to(route_map)

    grouped = df.groupby("Rider")
    for i, rider in enumerate(grouped):

        color = "blue"
        if rider[0].lower() == "unassigned":
            st.write(f"Number of orders {rider[0]}: {len(rider[1])}")
            color = "red"

        for i, dp in rider[1].iterrows():
            p = (dp["lat"], dp["lon"])
            tooltip = f"Order Id:{dp['Order Id']}, Rider: {rider[0]}"
            folium.RegularPolygonMarker(p, tooltip=tooltip, number_of_sides=i + 2, color=color, radius=3).add_to(
                route_map
            )

    folium_static(route_map)


def prepare_input_data(file) -> gpd.GeoDataFrame:
    if "sheet" in file.type:
        df = pd.read_excel(file)
    elif "csv" in file.type:
        df = pd.read_csv(file)
    else:
        raise (BaseException("In correct file type"))

    # Removing undefined/na latlong
    df = df[df["Lat"].notna()]

    # @todo: Detect Outliers and remove them. Currently hardcoded
    # outliers_lat = pd.Series(data=[12.7093,12.82172,12.8223181])
    # df.drop(df[df["Lat"].isin(outliers_lat)].index, inplace=True)

    df = df[["Order Id", "Lat", "Long", "Rider", "Quantity"]]
    df.rename(columns={"Lat": "lat"}, inplace=True)
    df.rename(columns={"Long": "lon"}, inplace=True)

    st.dataframe(df)
    return df
    # st.map(df)


# def prepare_geodat(df: pd.DataFrame):
#     crs_reference ={'init':"epsg:4326"}

#     inp_geometry = [Point(xy) for xy in zip(df['Long'], df['Lat'])]
#     demand_points_gdf = gpd.GeoDataFrame(df, geometry = inp_geometry, crs= crs_reference)

uploaded_file = st.file_uploader("Upload Files", type=["xlsx", "csv"])

if uploaded_file:
    file_details = {"FileName": uploaded_file.name, "FileType": uploaded_file.type, "FileSize": uploaded_file.size}
    prepared_data = prepare_input_data(uploaded_file)
    interest_points = {"kitchen": (12.9036093, 77.6313629)}
    prepare_map((12.97194, 77.59369), interest_points, prepared_data)
