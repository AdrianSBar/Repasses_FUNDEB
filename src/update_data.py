from src.data_cleaning import *


# Atualização dos dados
def upgrade_data(fold, update=True):
    if update == True:
        try:
            download_all_excel_datas(destiny_fold=fold)
        except:
            print('Erro ao efetuar download!')
    try:
        consolidation_data(fold=fold)
        summarization_data_1()
        summarization_data_2()
    except:
        print('Erro ao gerar datasets!')
