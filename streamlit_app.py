# app.py

import streamlit as st
import os

# User input
species_file = "species.txt"
treeheight_file = "treesizes.txt"
figs_dir = "./figs"

# Set page configuration
st.set_page_config(
    page_title="Tree Mortality Analysis",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load the data from text files
def load_data(file_path):
    with open(file_path) as f:
        return f.read().splitlines()

species_list = load_data(species_file)
treeheight_list = load_data(treeheight_file)

# Sidebar options
st.sidebar.title("Options")

# First selection: Select Species or Tree Height
subset_option = st.sidebar.selectbox("Select Species or Tree Height", ["Species", "Tree Height"])
if subset_option == "Species":
    subset = "species"
    subset_list = species_list
else:
    subset = "treeheight"
    subset_list = treeheight_list

# Second selection: Subset
group = st.sidebar.selectbox("Subset", subset_list)

# Third selection: Metric to display
metric_option = st.sidebar.selectbox(
    "Metric to display",
    [
        "Mortality (absolute)",
        "Mortality (relative to 2015)",
        "Change in Mortality since 2015 (absolute)",
        "Change in Mortality since 2015 (relative to 2015)",
    ]
)

# Set the variables based on metric_option
centered = False
normalized = False

if metric_option == "Mortality (absolute)":
    centered = False
    normalized = False
elif metric_option == "Mortality (relative to 2015)":
    centered = True
    normalized = False
elif metric_option == "Change in Mortality since 2015 (absolute)":
    centered = False
    normalized = True
elif metric_option == "Change in Mortality since 2015 (relative to 2015)":
    centered = True
    normalized = True

# Fourth selection: Map type
map_type_option = st.sidebar.selectbox("Map type", ["Greater Ecoregion", "Hexmap"])
if map_type_option == "Greater Ecoregion":
    map_type = "gre"
else:
    map_type = "hex"

# Construct the path to the plot image
plot_path = os.path.join(
    figs_dir,
    map_type,
    f"direct_bs-centered_{centered}_normalized-{normalized}-{group}.png"
)

# Overwrite if all groups are selected
if group == "All Species":
    if centered and normalized:
        plot_path = "./figs/all/species/fig-direct_bs-groups_of_most_observations-all_groups_100-bootstraps_centered_normalized.png"
    elif centered and not normalized:
        plot_path = "./figs/all/species/fig-direct_bs-groups_of_most_observations-all_groups_100-bootstraps_centered.png"
    elif not centered and normalized:
        plot_path = "./figs/all/species/fig-direct_bs-groups_of_most_observations-all_groups_100-bootstraps_normalized.png"
    elif not centered and not normalized:
        plot_path = "./figs/all/species/fig-direct_bs-groups_of_most_observations-all_groups_100-bootstraps.png"
    else:
        st.error("Plot not found")
elif subset_option == "All Tree Sizes":
    st.write("Tree size data has not been added yet.")

# Main part of the app
st.title("Tree Mortality Analysis")

# Check if the plot image exists
if os.path.exists(plot_path):
    st.image(plot_path, caption=f"{metric_option} for {group} in {map_type_option}", use_column_width=False)
else:
    st.write(f"This data has not been added yet: {plot_path}")
    # st.error(f"Plot image not found: {plot_path}")

# Show the plot path for debugging purposes
st.write(f"Plot path: {plot_path}")

# Custom CSS to widen the main content area and double the sidebar width
# st.markdown(
#     """
#     <style>
#     .css-18e3th9 {
#         flex: 1 1 70% !important;
#         max-width: 70% !important;
#     }
#     .css-1d391kg {
#         width: 400px !important;
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )
