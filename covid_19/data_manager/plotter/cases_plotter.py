from covid_19.data_manager.plotter.bokeh_plotter import *
from covid_19.data_manager.config.config import *


class ItalyCasesPlotter:

    def __init__(self, norm_country_df_ita, norm_regions_df_ita):

        self.norm_country_df_ita = norm_country_df_ita
        self.norm_regions_df_ita = norm_regions_df_ita

    def plot_dashboard_ita(self, plot_country_dashboard_flag=False, plot_regions_dashboard_flag=False):

        self.norm_country_df_ita["data"] = pd.to_datetime(self.norm_country_df_ita["data"])

        country_df = self.norm_country_df_ita
        regions_df = self.norm_regions_df_ita

        country_path = os.path.join(
            italy_figures_path,
            "country"
        )
        os.makedirs(country_path, exist_ok=True)
        plot_lines_dashboard_ita(
            country_df,
            country_path,
            "country",
            plot_country_dashboard_flag
        )
        for region, df_region in regions_df.groupby("denominazione_regione"):
            region_path = os.path.join(
                italy_figures_path,
                "regions",
                region
            )
            os.makedirs(region_path, exist_ok=True)
            plot_lines_dashboard_ita(
                df_region,
                region_path,
                region,
                plot_regions_dashboard_flag)

    def plot_regions_comparison(self, y_col, x_col, plot_dashboard_flag):
        # plot_regions_comparison(
        # 	self.norm_regions_df_ita, y_col, x_col
        # )

        df_regions_plot = pd.DataFrame(
            index=range(-100, 100)
        )

        for region, df_region in self.norm_regions_df_ita.groupby("denominazione_regione"):
            # print(df_region.set_index(x_col)[y_col])
            region_s = df_region.set_index(x_col)[y_col]
            df_regions_plot.at[
                region_s.index, region
            ] = region_s.values

        # print(df_regions_plot.index)
        df_regions_plot = df_regions_plot.loc[df_regions_plot.index.drop_duplicates()].dropna(how="all", axis=0)
        # print(df_regions_plot.index)

        df_regions_plot = df_regions_plot.dropna(how="all", axis=1)
        figures_path = os.path.join(
            italy_figures_path,
            "regions_comparison"
        )
        os.makedirs(figures_path, exist_ok=True)
        plot_comparison_df_bokeh(
            df_regions_plot.sort_index().loc[0:], [y_col],
            figures_path, y_col, True
        )
