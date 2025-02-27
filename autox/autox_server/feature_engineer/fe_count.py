import warnings
import pandas as pd
warnings.filterwarnings('ignore')
import time
from autox.autox_server.util import log
from tqdm import tqdm

def fe_count(G_df_dict, G_data_info, G_hist, is_train, remain_time):
    # 对G_df_dict['BIG']表做扩展特征

    start = time.time()
    log('[+] feature engineer, count')

    Id = G_data_info['target_id']
    target = G_data_info['target_label']

    if is_train:
        G_hist['FE_count'] = {}
        G_hist['FE_count']['feature_map'] = {}

        size_of_big = G_df_dict['BIG'].shape[0]

        cnt_features = []
        for col in tqdm(G_hist['big_cols_cat']):
            if G_df_dict['BIG'][col].nunique() < size_of_big * 0.8:
                cnt_features.append(col)
        G_hist['FE_count']['cnt_features'] = cnt_features
        log("count features: {}".format(cnt_features))

        for f in tqdm(cnt_features):
            temp = pd.DataFrame(G_df_dict['BIG'][f])
            temp[f + '_cnt'] = temp.groupby([f])[f].transform('count')
            temp.index = temp[f]
            temp = temp.drop(f, axis=1)
            faeture_map = temp.to_dict()[f + '_cnt']
            G_hist['FE_count']['feature_map'][f] = faeture_map

    G_df_dict['FE_count'] = G_df_dict['BIG'][Id]
    for f in G_hist['FE_count']['cnt_features']:
        G_df_dict['FE_count'][f + "_cnt"] = G_df_dict['BIG'][f].map(G_hist['FE_count']['feature_map'][f])

    end = time.time()
    remain_time -= (end - start)
    log("remain_time: {} s".format(remain_time))
    return remain_time