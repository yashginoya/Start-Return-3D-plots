import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
import os

def make3DGraph(filePath, graphTitle):
    # filePath = 'D:\\yash\\Akash Strategy\\Pyramid Neutral Strategy\\Scripts\\HSL_TSL_Optimization\\Output\\NIFTY\\1\\1DT_TSL_Summary.csv'
    df = pd.read_csv(filePath)

    call_tsl = np.arange(50, 201, 10)  # Call Option SL values
    put_tsl = np.arange(50, 201, 10)    # Put Option SL values
    n_call = len(call_tsl)
    n_put = len(put_tsl) 
    put_tsl_grid, call_tsl_grid = np.meshgrid(put_tsl, call_tsl)

    new_df = df[["Call TSL","Put TSL","Total Return"]]
    new_df = new_df.sort_values(by= ["Call TSL","Put TSL","Total Return"]).reset_index(drop = True)

    returns2D = new_df["Total Return"].to_numpy().reshape((n_call,n_put))

    surface = go.Surface(
        z=returns2D, 
        x=call_tsl, 
        y=put_tsl,
        colorscale='Viridis',
        opacity= 0.8,
        hovertemplate="Call TSL: %{x}<br>Put TSL: %{y}<br>Returns: %{z}<extra></extra>"  # Custom hover text
    )

    layout = go.Layout(
        title=graphTitle,
        scene=dict(
            xaxis_title='Call Option SL',
            yaxis_title='Put Option SL',
            zaxis_title='Returns'
        ),
    )

    fig = go.Figure(data=[surface],layout=layout)

    def update_surface(trace, points, selector):
        if points.point_inds:
            # Get the hovered point
            ind = points.point_inds[0]
            z_val = returns2D.flatten()[ind]

            # Create a horizontal plane at the hovered point's Z value
            x_plane, y_plane = np.meshgrid(call_tsl[:, 0], put_tsl[0, :])  # Create grid for the plane
            z_plane = np.full_like(x_plane, z_val)  # Set all Z-values to the hovered Z-value

            # Create the horizontal plane
            plane = go.Surface(z=z_plane, x=x_plane, y=y_plane, opacity=0.2, colorscale='Blues')

            # Update the figure with the plane
            fig.add_trace(plane)
            fig.show()
        
    # fig.data[0].on_hover(update_surface)

    return fig

def main():

    SYMBOL_LIST = []
    version_folder_list = []

    for dirpath,dirnames,filenames in os.walk("HSL_TSL_Optimization/Output"):
        for dirc in dirnames:
            SYMBOL_LIST.append(dirc)

    SYMBOL = st.selectbox("Select a Symbol ", SYMBOL_LIST, index=0)

    for dirpath,dirnames,filenames in os.walk("HSL_TSL_Optimization/Output/" + SYMBOL):
        for dirc in dirnames:
            version_folder_list.append(dirc)

    

    InnerFolderName = st.selectbox("Select a Version ", version_folder_list , index=0)
    
    folder_path = "HSL_TSL_Optimization/Output/" + SYMBOL + "/" + InnerFolderName
    all_files = []

    for dirpath, dirnames, filenames in os.walk(folder_path):
        for file in filenames:
            all_files.append(file)

    # all_files = sorted(all_files)
    all_files = np.array(all_files)
    all_files.sort()

    st.markdown("# Graphs for Version: " + InnerFolderName)

    for curr_file_name in all_files:
        if "lock" in curr_file_name:
            continue
        if "TSL" in curr_file_name:
            file_path =  folder_path + '/' + curr_file_name
            graph_title = curr_file_name
            curr_3d_graph = make3DGraph(file_path,graph_title)
            st.plotly_chart(curr_3d_graph)

if __name__ == "__main__":
    main()
    