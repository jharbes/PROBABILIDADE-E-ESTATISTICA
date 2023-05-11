from more_itertools import collapse

SELIC= quandl.get('BCB/432',start_date = data_inicio, end_date = data_fim, collapse = 'monthly')
IPCA = quandl.get('BCB/13522',start_date = data_inicio, end_date = data_fim, collapse = 'monthly')
IGPM = quandl.get('BCB/189',start_date = data_inicio, end_date = data_fim, collapse = 'monthly')
PIB_BRASIL = quandl.get('BCB/4380',start_date = data_inicio, end_date = data_fim, collapse = 'monthly')
CONF = quandl.get('BCB/4393',start_date = data_inicio, end_date = data_fim, collapse = 'monthly')
DOLAR = quandl.get('BCB/10813',start_date = data_inicio, end_date = data_fim, collapse = 'monthly')

df = pd.concat([SELIC,IPCA,IGPM,PIB_BRASIL, CONF, DOLAR], axis = 1)

df.columns=['SELIC', 'IPCA', 'IGPM', 'PIB_BRASIL', 'CONF', 'Dolar']