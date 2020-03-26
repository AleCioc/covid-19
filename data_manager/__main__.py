from data_manager.cases_data_source.italy_cases_data_source import ItalyCasesDataSource

italy_cases_ds = ItalyCasesDataSource()
italy_cases_ds.normalise()
italy_cases_ds.save_norm()
