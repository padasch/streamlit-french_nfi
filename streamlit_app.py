import streamlit as st
import pandas as pd
import os

# User input
species_file = "data/species.txt"
treeheight_file = "data/heights.txt"
gre_file = "data/greco.txt"
reg_file = "data/regions.txt"
figs_dir = "./figs"

# Set page configuration
st.set_page_config(
    page_title="Tree Mortality Analysis",
    layout="wide",
    initial_sidebar_state="expanded",
)


# Load the data from text files
def load_data(file_path):
    with open(file_path) as f:
        return f.read().splitlines()

# Display figures in one line
def display_fig(mypath, mycaption, column_wide):
    if os.path.exists(mypath):
        st.image(
            mypath,
            caption=mycaption,
            use_column_width=column_wide,
        )
    else:
        st.write(f"This data has not been added yet: {mypath}")


species_list = load_data(species_file)
treeheight_list = load_data(treeheight_file)
greco_list = load_data(gre_file)
region_list = load_data(reg_file)

# Initialize session state for page and selections
if "page" not in st.session_state:
    st.session_state.page = "Homepage"

# Sidebar navigation
st.sidebar.title("Navigation")
if st.sidebar.button("Homepage"):
    st.session_state.page = "Homepage"
    
if st.sidebar.button("Visualizations"):
    st.session_state.page = "Visualizations"
    
if st.sidebar.button("Dataset"):
    st.session_state.page = "Dataset"


# Sidebar options
col1, col2, col3 = st.columns([0.1, 0.8, 0.1])
with col2:
    # Title
    st.title("Tree Mortality Trends in France 🌲📊🇫🇷")
    
    # Homepage content -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    if st.session_state.page == "Homepage":
    
        st.warning("👈 Start exploring the data by clicking 'Visualizations' in the sidebar!")
        st.header("Description")
        st.write(
            """
        This app displays trends of tree mortality across different regions and species in France. All figures are based on the publicly available data from the French National Forest Inventory (IFN) [1]. The dataset contains various tree- and stand-level information collected during the annual campaigns of the IFN, whereby each tree is revisited after five years. Note that only the 20 most common species in terms of tree counts are shown here.
        
        The presented mortality rates were calculated as follows. After downloading the original NFI dataset [1], only sites were kept that were first visited in 2010 (due to changing data collection methods before that), that were marked as censusable (indicated by the variable 'peupnr'), and that had no missing coordinates. At the tree-level, only trees were kept that had clear declaration of their state at first and second visit, and trees that were targeted by the sampling scheme (indicated by the variable 'cible'). The mortality rate for each group and year (e.g. all Quercus robur in 2017) was calculated following a 100x bootstrapping approach. Here, all trees falling within the category were sampled with replacement 100 times, and the mortality rate was calculated for each sample as the percentage of trees that have died between the two sampling campaigns. The mean and standard deviation of these 100 mortality rates were then calculated and visualised. All line plots show the mean as solid line and standard deviation as error band. The spatial representations include a hexagonal grid overlaying France, the administrative departments and regions of France, as well as the [Greater Ecoregions and Sylvoecoregions](https://inventaire-forestier.ign.fr/spip.php?article773) of France. These maps are presented in the form of heatmaps, with each hexagon or region colored according to the selected mean mortality rate. Where the bootstrapped standard deviation was larger than 50% of the mean, the hexagon or region was stippled with grey dots to indicate high uncertainty. 
        
        **Explanation of Metrics:**
        
        - Mortality (absolute): Absolute mortality rate of trees in the selected group.
        - Mortality (relative to 2015): Change in mortality rate of trees in the selected group when subtracting the value from 2015.
        - Change in Mortality since 2015 (absolute): Absolute change in mortality rate of trees in the selected group since 2015.
        - Change in Mortality since 2015 (relative to 2015): Relative change in mortality rate of trees in the selected group since 2015.
        
        """
        )
        
        st.image(
            "figs/maps/region_map.png",
            caption="Map of France with regions",
            use_column_width=True,
        )

        st.header("Disclaimer")
        st.write(
            """
        All data shown here was derived from the freely available data provided by the French National Forest Inventory (IFN) [1]. This work is not affiliated with the IFN and is intended for educational and informational purposes only. The accuracy and reliability of the data are subject to the limitations of the IFN dataset. In Alignment with the IFN's Open Licence Etalab Version 2.0, the work displayed here is licensed under a [Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License](https://creativecommons.org/licenses/by-nc-nd/4.0/).

        [1] IGN - Inventaire forestier national français, Données brutes, Campagne annuelles 2005 et suivantes, https://inventaire-forestier.ign.fr/dataIFN/, site consulté le 20/02/2024.
        """
        )
    
    # Dataset content -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    elif st.session_state.page == "Dataset":
        st.warning("👈 Start exploring the data by clicking 'Visualizations' in the sidebar!")
        st.header("Dataset")
        # st.info("Loading the data...")
        # st.success("Data loaded successfully!")
        my_bar = st.progress(0, text="Loading the data...")
        st.write(pd.read_csv("data/nfi_data_for_webapp.csv"))
        with open("data/nfi_data_for_webapp.csv") as f:
            st.download_button('Download CSV', f, "french_nfi_data.csv")
        my_bar.progress(100, text="Loading the data...")
        my_bar.empty()
        st.header("Description")
        st.write(
            '''
            | Field                      | Description                                                   |
            |----------------------------|---------------------------------------------------------------|
            | idp                        | Unique identifier of the plot (can be used to match with the original NFI data) |
            | tree_id                    | Unique identifier of the tree (combined from idp and tree number) |
            | tree_state_1               | Tree state of tree at first visit                             |
            | tree_state_2               | Tree state of tree at second visit (five years later)         |
            | tree_state_change          | Merged variable from first and second tree state              |
            | ba_1                       | Basal area of tree at first visit [m^2]                             |
            | ba_2                       | Basal area of tree at second visit [m^2]                            |
            | v                          | Volume of tree at first visit [m^3]                                 |
            | genus_lat                  | Genus of tree                                                 |
            | species_lat                | Species of tree                                               |
            | species_lat_short          | Shortened species name                                        |
            | tree_height_class          | Height class of tree                                          |
            | tree_circumference_class   | Tree circumference class (following the French NFI)           |
            | ser                        | Sylvoecoregion code                                           |
            | gre                        | Greater Ecoregion code                                        |
            | reg                        | Administrative region code                                    |
            | dep                        | Administrative department code                                |

            '''
                )
   
    # Visualizations content -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    elif st.session_state.page == "Visualizations":
        # First selection: Select Species or Tree Height
        subset_option = st.sidebar.selectbox(
            "Group",
            ["[Select]", "Species", "Tree Height", "Greater Ecoregion", "Administrative Region"],
            index=["[Select]", "Species", "Tree Height", "Greater Ecoregion", "Administrative Region"].index(
                "[Select]"
            ),
        )
        
        if subset_option == "[Select]":
            st.warning("👈 Select a group in the sidebar to start exploring the data.")
            st.info("💬 If you have any questions or feedback, please reach out to the authors via [GitHub](https://github.com/padasch/streamlit-french_nfi), [email](mailto:pascal.schneider@wsl.ch), or [X](https://x.com/padasch_).")
            st.stop()
        

        # Options --------------------------------------------------------------------------------------------
        if subset_option == "Species":
            subset = "species_lat"
            subset_list = species_list
        elif subset_option == "Tree Height":
            subset = "tree_height_class"
            subset_list = treeheight_list
        elif subset_option == "Greater Ecoregion":
            subset = "gre"
            subset_list = greco_list
        elif subset_option == "Administrative Region":
            subset = "reg"
            subset_list = region_list

        # Second selection: Subset
        group = st.sidebar.selectbox("Subset", subset_list)

        # Third selection: Metric to display
        metric_option = st.sidebar.selectbox(
            "Metric",
            [
                "Absolute mortality rate",
                "Change in absolute mortality rate (compared to 2015)",
                "Relative mortality rate (compared to 2015)",
                "Change in relative mortality rate (compared to 2015)",
            ],
        )

        # Set the variables based on metric_option
        if metric_option == "Absolute mortality rate":
            centered = False
            normalized = False
        elif metric_option == "Change in absolute mortality rate (compared to 2015)":
            centered = True
            normalized = False
        elif metric_option == "Relative mortality rate (compared to 2015)":
            centered = False
            normalized = True
        elif metric_option == "Change in relative mortality rate (compared to 2015)":
            centered = True
            normalized = True

        # Species / Tree content -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # Fourth selection: Map type
        map_type_option = st.sidebar.selectbox(
            "Map",
            [
                "Hexagon",
                "Greater Ecoregion",
                "Sylvoecoregion",
                "Administrative Region",
                "Administrative Departments",
            ],
        )
        
        if map_type_option == "Greater Ecoregion":
            map_type = "gre"
        elif map_type_option == "Sylvoecoregion":
            map_type = "ser"
        elif map_type_option == "Administrative Region":
            map_type = "reg"
        elif map_type_option == "Administrative Departments":
            map_type = "dep"
        elif map_type_option == "Hexagon":
            map_type = "hex"
        else:
            st.write("Invalid choice for map type")

        # Species content -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        # Structure (for species, vice versa for height):
        # All Species:
        # - Single Plot
        #   - Line plot showing mortality rate across all tree heights for given species
        # - Spatial Trends 
        #   - Map across all or that given species
        # - Species by x 
        #   - Line plots per region (only for gre and reg)
        #   - Line facet per height
        
        # Get paths
        midpath = "mean-std-band/facet"
        
        if "All" in group:
            st.header(f"General trends across 20 most common species")
            st.subheader("Trend per Species")
            fig_1 = f"./figs/facet/species_lat/{midpath}/fig-direct_bs-groups_of_most_observations-all_groups_100-bootstraps-centered_{centered}-normalized_{normalized}.png"
            display_fig(fig_1, f"{metric_option} Trends for the 20 most common species, separated by species", True)
            
            st.subheader("Trend per Tree Height Class")
            fig_2 = f"./figs/facet/tree_height_class/{midpath}/fig-direct_bs-groups_of_most_observations-all_groups_100-bootstraps-centered_{centered}-normalized_{normalized}.png"
            display_fig(fig_2, f"{metric_option} Trends for the 20 most common species, separated by tree height class", True)
            
            st.subheader("Trend per Region")
            region_map = f"./figs/maps/{map_type}/direct_bs-centered_{centered}_normalized-{normalized}-All Species.png"
            display_fig(region_map, f"Spatial distribution of {metric_option} for the 20 most common species", True)
            
            if map_type in ["reg", "gre"]:
                region_facet = f"./figs/facet/{map_type}/{midpath}/fig-direct_bs-groups_of_most_observations-all_groups_100-bootstraps-centered_{centered}-normalized_{normalized}.png"
                display_fig(region_facet, f"Spatial distribution of {metric_option} for {map_type_option} for the 20 most common species", True)

        else:
            # Single plot
            plot_single = f"./figs/facet/{subset}/{midpath}/{group}-centered_{centered}-normalized-{normalized}.png"
            
            # Pick facet to show for each grouping
            if subset == "species_lat":
                title_1 = "Trend per Tree Height Class"
                plot_1 = f"./figs/facet/species_lat&tree_height_class/{midpath}/fig-{group}-direct_bs-_100-bootstraps-centered_{centered}-normalized_{normalized}.png"
                label_1 = f"{metric_option} for {group} per Tree Height Class"
                
                title_2 = "Trend per Region"
                plot_2 = f"./figs/maps/{map_type}/direct_bs-centered_{centered}_normalized-{normalized}-{group}.png"
                label_2 = f"{metric_option} for {group} per {map_type_option}"
                
            elif subset == "tree_height_class":
                title_1 = "Trend per Species"
                plot_1 = f"./figs/facet/species_lat&tree_height_class/{midpath}/fig-{group}-direct_bs-_100-bootstraps-centered_{centered}-normalized_{normalized}.png"
                label_1 = f"{metric_option} for {group} Height Class per Species"
                
                title_2 = "Trend per Region"
                plot_2 = f"./figs/maps/{map_type}/direct_bs-centered_{centered}_normalized-{normalized}-{group}.png"
                label_2 = f"{metric_option} for {group} Height Class per {map_type_option}"
                
            elif subset == "gre" or subset == "reg":
                title_1 = "Trend per Species"
                plot_1 = f"./figs/facet/{subset}&species_lat/{midpath}/fig-{group}-direct_bs-_100-bootstraps-centered_{centered}-normalized_{normalized}.png"
                label_1 = f"{metric_option} for region {group} per Species"
                
                title_2 = "Trend per Tree Height Class"
                plot_2 = f"./figs/facet/{subset}&tree_height_class/{midpath}/fig-{group}-direct_bs-_100-bootstraps-centered_{centered}-normalized_{normalized}.png"
                label_1 = f"{metric_option} for region {group} per Tree Height Class"
                
            # Display plots
            st.header(f"General trend")
            display_fig(plot_single, f"{metric_option} for {group}", False)
                
            st.header(title_1)
            display_fig(plot_1, f"{metric_option} for {group}", True)
            
            st.header(title_2)
            display_fig(plot_2, f"{metric_option} for {group}", True)
            
            # Show region facet if region or greco is selected
            if map_type in ["reg", "gre"]:
                plot_spatial_line = f"./figs/facet/{map_type}&{subset}/{midpath}/fig-{group}-direct_bs-_100-bootstraps-centered_{centered}-normalized_{normalized}.png"
                display_fig(plot_spatial_line, f"{metric_option} for {group} per {map_type_option}", True)
            
            # Add maps when greco or region is selected
            if map_type == "gre":
                display_fig("./figs/maps/gre_map.png", "Greater Ecoregions in France", True)
            elif map_type == "reg":
                display_fig("./figs/maps/reg_map.png", "Administrative Regions in France", True)

    st.write("")
    st.write("")
    st.info("💬 If you have any questions or feedback, please reach out to the authors via [GitHub](https://github.com/padasch/streamlit-french_nfi), [email](mailto:pascal.schneider@wsl.ch), or [X](https://x.com/padasch_).")

# Custom CSS to adjust the container size and the sidebar width
# max_width = 600  # You can adjust the max-width here
# sidebar_width = 350  # You can adjust the sidebar width here

# st.markdown(
#     f"""
#     <style>
#     .reportview-container .main .block-container {{
#         max-width: {max_width}px;
#     }}
#     .reportview-container .sidebar-content {{
#         width: {sidebar_width}px;
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True,
# )
