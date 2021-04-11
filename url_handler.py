from req import parse
from preparation import form_query_to_model
import pandas as pd
from classifier import train_and_predict
from service import get_error_encode


def handle_url(url):
    df_trained = pd.read_csv('train_server.csv')
    cols = ['description','tel', 'address', 'ftl', 'sc', 'ads', 'cart', 'sign', 'login', 'ar2k', 'ln20k', 'cloud', 'target']
    url_list = url.split()
    print(url_list)
    parsed_list = []
    is_df_created = False
    unparsed_list = []
    result_dict = dict()
    if len(url_list) > 5:
        return get_error_encode(204)
    for i in range(len(url_list)):
        content = parse(url_list[i])
        if type(content) is str:
            query = form_query_to_model(url_list[i], content)
            parsed_list.append(url_list[i]) 
            if not is_df_created:
                df_pred = pd.DataFrame([query], columns = cols, copy=False)
                is_df_created = True
            else:
                df_pred.loc[len(df_pred)] = query
        else:
            unparsed_list.append(url_list[i])
    try:
        result_df = train_and_predict(df_trained, df_pred)
        res_list = result_df['target'].to_list()
        for u in range(len(parsed_list)):
            result_dict[parsed_list[u]] = res_list[u]
        for j in range(len(unparsed_list)):
            result_dict[unparsed_list[j]] = 'None'
        return result_dict
    except Exception:
        for url in unparsed_list:
            result_dict[url] = 'None'
        return result_dict