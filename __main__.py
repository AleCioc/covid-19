from covid_19.config.config import *

from covid_19.data_manager.cases_data_source.italy_cases_data_source import ItalyCasesDataSource

from covid_19.data_manager.config.config import *

from covid_19.data_manager.plotter.bokeh_plotter import *

italy_cases_ds = ItalyCasesDataSource()
italy_cases_ds.normalise()
italy_cases_ds.save_norm()
italy_cases_ds.load_norm()
italy_cases_ds.plot_dashboard()

#from data_manager.cases_data_source.world_cases_data_source import WorldCasesDataSource
#world_cases_ds = WorldCasesDataSource()
#world_cases_ds.normalise()
#world_cases_ds.save_norm()
#world_cases_ds.load_norm()
#world_cases_ds.normalise()

#for country in world_cases_ds.top_countries:
    #print(country)
    #world_cases_ds.plot_country_dashboard(country, True)

#world_cases_ds.plot_country_dashboard("Jordan", True)
#world_cases_ds.plot_country_dashboard("Canada", True)
#world_cases_ds.plot_country_dashboard("Italy", True)
#world_cases_ds.plot_country_dashboard("China", True)
#world_cases_ds.plot_country_dashboard("France", True)
#world_cases_ds.plot_country_dashboard("Korea, South", True)
#world_cases_ds.plot_country_dashboard("US", True)
#world_cases_ds.plot_country_dashboard("United Kingdom", True)

#for country in list(world_cases_ds.countries_df_dict.keys()):
#    print(country)
#    world_cases_ds.plot_country_dashboard(country, False)

# from utils.data_prep_utils import *
#
# import json
#
# simplified_world_df = pd.read_excel(
#     os.path.join(
#         norm_cases_paths,
#         "world",
#         "simplified_world_df.xlsx"
#     )
# )
# #print(simplified_world_df)
# simplified_world_df.datetime = pd.to_datetime(simplified_world_df.datetime)
# simplified_world_df = simplified_world_df.sort_values("datetime")
#
# input_path = os.path.join(
#     validator_params_path,
#     "default_params.json"
# )
# with open(input_path, 'r') as f:
#     validator_params_dict = json.load(f)
#
# from model_validator.model_validator import *
#
# simplified_world_df = simplified_world_df[simplified_world_df.continent == "Europe"]
#
# validators_input_dict = {
#     "country_df": simplified_world_df,
#     "validator_params_dict": validator_params_dict,
# }
#
# validator_summary = run_model_validator(validators_input_dict)
# print(validator_summary)
