import os
import geopandas as gpd
import pandas as pd
import streamlit as st
from typing import Dict

def prepare_input_data(file) -> gpd.GeoDataFrame:
    if "sheet" in file.type:
        df = pd.read_excel(file)
    elif "csv" in file.type:
        df = pd.read_csv(file)
    else:
        raise(BaseException("In correct file type"))

    # Removing undefined/na latlong
    df = df[df["Lat"].notna()]

    # @todo: Detect Outliers and remove them. Currently hardcoded
    # outliers_lat = pd.Series(data=[12.7093,12.82172,12.8223181])
    # df.drop(df[df["Lat"].isin(outliers_lat)].index, inplace=True)

    df = df[["Order Id","Lat","Long","Quantity"]]
    df.rename(columns = {'Lat':'lat'}, inplace = True)
    df.rename(columns = {'Long':'lon'}, inplace = True)

    st.dataframe(df)
    st.map(df)

# def prepare_geodat(df: pd.DataFrame):
#     crs_reference ={'init':"epsg:4326"}

#     inp_geometry = [Point(xy) for xy in zip(df['Long'], df['Lat'])]
#     demand_points_gdf = gpd.GeoDataFrame(df, geometry = inp_geometry, crs= crs_reference)

uploaded_file = st.file_uploader("Upload Files",type=['xlsx','csv'])

if uploaded_file:
    file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
    prepare_input_data(uploaded_file)