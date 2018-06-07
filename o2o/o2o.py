import pandas as pd
from datetime import datetime
import numpy as np

if __name__ == '__main__':
    """
    使用的函数：
    """
    def cal_discount(s):
        s = str(s)
        s = s.split(':')
        if len(s)==1:
            return float(s[0])
        else:
            return round(1.0 - float(s[1]) / float(s[0]),4)


    def isweek(s):
        s = str(s)
        week = datetime.strptime(s, '%Y%m%d').weekday() + 1
        if week == 5 or week == 6 or week == 7:
            return 1
        else:
            return 0





    """
    划分数据集：
    """
    off_train = pd.read_csv('./ccf_offline_stage1_train.csv',header=0,low_memory=False)
    off_train.columns = ['user_id', 'merchant_id', 'coupon_id', 'discount_rate', 'distance', 'date_received', 'date']
    off_test = pd.read_csv('./ccf_offline_stage1_test_revised.csv',header=0,low_memory=False)
    off_test.columns = ['user_id', 'merchant_id', 'coupon_id', 'discount_rate', 'distance', 'date_received']
    on_train = pd.read_csv('./ccf_online_stage1_train.csv',header=0,low_memory=False)
    on_train.columns = ['user_id', 'merchant_id', 'action', 'coupon_id', 'discount_rate', 'date_received', 'date']

    dataSet3 = off_test
    dataSet3_off_feature3 = off_train[((off_train['date']>=20160301.0) & (off_train['date']<=20160630.0))
                                      |((off_train['date'].isnull()==True)&(off_train['date_received']>=20160301.0)
                                        &(off_train['date_received']<=20160630.0))]
    dataSet3_on_feature3 = on_train[((on_train['date']>=20160301.0) & (on_train['date']<=20160630.0))|
                                    ((on_train['date'].isnull()==True)&(on_train['date_received']>=20160301.0)
                                     &(on_train['date_received']<=20160630.0))]

    dataSet2 = off_train[(off_train['date_received']>=20160601.0)&(off_train["date_received"]<=20160630.0)]
    dataSet2_off_feature2 = off_train[((off_train['date']>=20160201.0)&(off_train['date']<=20160530.0))|
                                      ((off_train['date'].isnull()==True)&(off_train['date_received']>=20160201.0)&
                                       (off_train['date_received']<=20160530.0))]
    dataSet2_on_feature2 = on_train[((on_train['date'] >= 20160201.0) & (on_train['date'] <= 20160530.0))|
                                      ((on_train['date'].isnull() == True) & (on_train['date_received'] >= 20160201.0) &
                                       (on_train['date_received'] <= 20160530.0))]

    dataSet1 = off_train[(off_train['date_received']>=20160501.0)&(off_train["date_received"]<=20160531.0)]
    dataSet1_off_feature1 = off_train[((off_train['date'] >= 20160101.0) & (off_train['date'] <= 20160430.0)) |
                                      ((off_train['date'].isnull() == True) & (off_train['date_received'] >= 20160101.0) &
                                       (off_train['date_received'] <= 20160430.0))]
    dataSet1_on_feature1 = on_train[((on_train['date'] >= 20160101.0) & (on_train['date'] <= 20160430.0)) |
                                    ((on_train['date'].isnull() == True) & (on_train['date_received'] >= 20160101.0) &
                                     (on_train['date_received'] <= 20160430.0))]

    """"
    提取线上的特征:
        每个用户消费的总次数                              user_online_buy_total
        每个用户使用消费券消费的次数                      use_online_buy_coupon
        每个用户使用消费券消费的次数占总消费次数的占比     user_online_buy_couponRate
        每个用户领取的消费券的总数                        user_online_coupon_receivedAll
        每个用户使用消费券占领取的消费券的比重             uses_online_coupon_buyRate
        每个用户在限时低价时消费的次数                     user_online_buy_fixed
        每个用户限时低价消费占总消费的比重                 user_online_buy_fixedRate
        用户购买东西的商店的个数                          user_online_buy_merchantCount
        每个用户看过的商店的个数包括只点击                 user_online_action_merchantCount
        每个用户行为的个数（包括点击，消费，领取）         user_online_action_count
        每个用户点击个数                                  user_online_click_count
        每个用户领取了优惠券没有使用的次数                 user_online_notUseReceive_coupon
        每个用户没有使用消费券消费的次数                   user_online_notUse_coupon
        消费的商店占有过行为的商店的比重                   user_online_merchantBuyRate

    """
    # 对dataSet3_on_feature3

    # 每个用户消费的总次数user_online_buy_total
    # t = pd.DataFrame(dataSet3_on_feature3[['user_id','date']])
    # t = t[t['date'].notnull() == True]
    # t = pd.DataFrame(t['user_id'],columns=['user_id'])
    # t['user_online_buy_total'] = 1
    # t = t.groupby('user_id',sort=False).agg('sum').reset_index()
    #
    # # 每个用户使用消费券消费的次数use_online_buy_coupon
    # t1 = pd.DataFrame(dataSet3_on_feature3[['user_id','action','coupon_id']])
    # t1 = t1[(t1['action'] == 1)&(t1['coupon_id'].notnull()==True)&(t1['coupon_id']!='fixed')]
    # t1 = pd.DataFrame(t1['user_id'], columns=['user_id'])
    # t1['use_online_buy_coupon'] = 1
    # t1 = t1.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 每个用户领取的消费券的总数user_online_coupon_receivedAll
    # t2 = pd.DataFrame(dataSet3_on_feature3[['user_id', 'action', 'coupon_id']])
    # t2 = t2[(t2['action'] == 2) & (t2['coupon_id'].notnull() == True) & (t2['coupon_id'] != 'fixed')]
    # t2 = pd.DataFrame(t2['user_id'], columns=['user_id'])
    # t2['user_online_coupon_receivedAll'] = 1
    # t2 = t2.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 每个用户在限时低价时消费的次数user_online_buy_fixed
    # t3 = pd.DataFrame(dataSet3_on_feature3[['user_id', 'action', 'coupon_id']])
    # t3 = t3[(t3['action'] == 1) & (t3['coupon_id'] == 'fixed')]
    # t3 = pd.DataFrame(t3['user_id'], columns=['user_id'])
    # t3['user_online_buy_fixed'] = 1
    # t3 = t3.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 用户购买东西的商店的个数user_online_buy_merchantCount
    # t4 = pd.DataFrame(dataSet3_on_feature3[['user_id', 'action', 'merchant_id']])
    # t4 = t4[(t4['action'] == 1) & (t4['merchant_id'].notnull()==True)]
    # t4 = pd.DataFrame(t4['user_id'], columns=['user_id'])
    # t4['user_online_buy_merchantCount'] = 1
    # t4 = t4.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 每个用户看过的商店的个数包括只点击user_online_action_merchantCount
    # t5 = pd.DataFrame(dataSet3_on_feature3[['user_id','merchant_id']])
    # t5 = t5[(t5['merchant_id'].notnull() == True)]
    # t5 = pd.DataFrame(t5['user_id'], columns=['user_id'])
    # t5['user_online_action_merchantCount'] = 1
    # t5 = t5.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 每个用户行为的个数user_online_action_count
    # t6 = pd.DataFrame(dataSet3_on_feature3[['user_id', 'action']])
    # t6 = t6[(t6['action'].notnull() == True)]
    # t6 = pd.DataFrame(t6['user_id'], columns=['user_id'])
    # t6['user_online_action_count'] = 1
    # t6 = t6.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 每个用户点击个数user_online_click_count
    # t7 = pd.DataFrame(dataSet3_on_feature3[['user_id', 'action']])
    # t7 = t7[(t7['action'].notnull() == True)&(t7['action']==0)]
    # t7 = pd.DataFrame(t7['user_id'], columns=['user_id'])
    # t7['user_online_click_count'] = 1
    # t7 = t7.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 每个用户领取了优惠券没有使用的次数user_online_notUseReceive_coupon
    # t8 = pd.DataFrame(dataSet3_on_feature3[['user_id', 'action','date']])
    # t8 = t8[(t8['action'].notnull() == True) & (t8['action'] == 2)&(t8['date'].isnull()==True)]
    # t8 = pd.DataFrame(t8['user_id'], columns=['user_id'])
    # t8['user_online_notUseReceive_coupon'] = 1
    # t8 = t8.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 每个用户没有使用消费券消费的次数user_online_notUse_coupon
    # t9 = pd.DataFrame(dataSet3_on_feature3[['user_id', 'coupon_id', 'date']])
    # t9 = t9[(t9['date'].notnull() == True) & (t9['coupon_id'].isnull() == True)]
    # t9 = pd.DataFrame(t9['user_id'], columns=['user_id'])
    # t9['user_online_notUse_coupon'] = 1
    # t9 = t9.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 合并数据
    # left = dataSet3_on_feature3[['user_id']].drop_duplicates()
    # dataSet3_on_result = pd.merge(left,t,how='left',on=['user_id'])
    # dataSet3_on_result = pd.merge(dataSet3_on_result,t1,how='left',on='user_id')
    # dataSet3_on_result = pd.merge(dataSet3_on_result,t2,how='left',on='user_id')
    # dataSet3_on_result = pd.merge(dataSet3_on_result,t3,how='left',on='user_id')
    # dataSet3_on_result = pd.merge(dataSet3_on_result,t4,how='left',on='user_id')
    # dataSet3_on_result = pd.merge(dataSet3_on_result,t5,how='left',on='user_id')
    # dataSet3_on_result = pd.merge(dataSet3_on_result,t6,how='left',on='user_id')
    # dataSet3_on_result = pd.merge(dataSet3_on_result,t7,how='left',on='user_id')
    # dataSet3_on_result = pd.merge(dataSet3_on_result,t8,how='left',on='user_id')
    # dataSet3_on_result = pd.merge(dataSet3_on_result,t9,how='left',on='user_id')
    #
    # # 替换每列中的Nan,用平均值来代替
    # for i in dataSet3_on_result.columns:
    #     meanVal = dataSet3_on_result[i].mean()
    #     dataSet3_on_result[i].fillna(meanVal,inplace=True)
    #
    # # 使用消费券消费的次数占总消费次数的占比 user_online_buy_couponRate (use_online_buy_coupon/user_online_buy_total)
    # t10 = dataSet3_on_result['use_online_buy_coupon']
    # t_10 = dataSet3_on_result['user_online_buy_total']
    # t10 = t10/t_10
    # dataSet3_on_result['user_online_buy_couponRate'] = t10
    #
    # # 用户使用消费券占领取的消费券的比重  uses_online_coupon_buyRate (use_online_buy_coupon/user_online_coupon_receivedAll)
    # t11 = dataSet3_on_result['use_online_buy_coupon']
    # t_11 = dataSet3_on_result['user_online_coupon_receivedAll']
    # t11 = t11/t_11
    # dataSet3_on_result['uses_online_coupon_buyRate'] = t11
    #
    # # 每个用户限时低价消费占总消费的比重 user_online_buy_fixedRate (user_online_buy_fixed/user_online_buy_total)
    # t12 = dataSet3_on_result['user_online_buy_fixed']
    # t_12 = dataSet3_on_result['user_online_buy_total']
    # t12 = t12/t_12
    # dataSet3_on_result['user_online_buy_fixedRate'] = t12
    #
    # # 消费的商店占有过行为的商店的比重 user_online_merchantBuyRate (user_online_buy_merchantCount/user_online_action_merchantCount)
    # t13 = dataSet3_on_result['user_online_buy_merchantCount']
    # t_13 = dataSet3_on_result['user_online_action_merchantCount']
    # t13 = t13/t_13
    # dataSet3_on_result['user_online_merchantBuyRate'] = t13
    #
    # dataSet3_on_result.to_csv('dataSet3_on_feature.csv', index=None)
    #
    # # 对dataSet2_on_feature2
    #
    # # 每个用户消费的总次数user_online_buy_total
    # t = pd.DataFrame(dataSet2_on_feature2[['user_id','date']])
    # t = t[t['date'].notnull() == True]
    # t = pd.DataFrame(t['user_id'],columns=['user_id'])
    # t['user_online_buy_total'] = 1
    # t = t.groupby('user_id',sort=False).agg('sum').reset_index()
    #
    # # 每个用户使用消费券消费的次数use_online_buy_coupon
    # t1 = pd.DataFrame(dataSet2_on_feature2[['user_id','action','coupon_id']])
    # t1 = t1[(t1['action'] == 1)&(t1['coupon_id'].notnull()==True)&(t1['coupon_id']!='fixed')]
    # t1 = pd.DataFrame(t1['user_id'], columns=['user_id'])
    # t1['use_online_buy_coupon'] = 1
    # t1 = t1.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 每个用户领取的消费券的总数user_online_coupon_receivedAll
    # t2 = pd.DataFrame(dataSet2_on_feature2[['user_id', 'action', 'coupon_id']])
    # t2 = t2[(t2['action'] == 2) & (t2['coupon_id'].notnull() == True) & (t2['coupon_id'] != 'fixed')]
    # t2 = pd.DataFrame(t2['user_id'], columns=['user_id'])
    # t2['user_online_coupon_receivedAll'] = 1
    # t2 = t2.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 每个用户在限时低价时消费的次数user_online_buy_fixed
    # t3 = pd.DataFrame(dataSet2_on_feature2[['user_id', 'action', 'coupon_id']])
    # t3 = t3[(t3['action'] == 1) & (t3['coupon_id'] == 'fixed')]
    # t3 = pd.DataFrame(t3['user_id'], columns=['user_id'])
    # t3['user_online_buy_fixed'] = 1
    # t3 = t3.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 用户购买东西的商店的个数user_online_buy_merchantCount
    # t4 = pd.DataFrame(dataSet2_on_feature2[['user_id', 'action', 'merchant_id']])
    # t4 = t4[(t4['action'] == 1) & (t4['merchant_id'].notnull()==True)]
    # t4 = pd.DataFrame(t4['user_id'], columns=['user_id'])
    # t4['user_online_buy_merchantCount'] = 1
    # t4 = t4.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 每个用户看过的商店的个数包括只点击user_online_action_merchantCount
    # t5 = pd.DataFrame(dataSet2_on_feature2[['user_id','merchant_id']])
    # t5 = t5[(t5['merchant_id'].notnull() == True)]
    # t5 = pd.DataFrame(t5['user_id'], columns=['user_id'])
    # t5['user_online_action_merchantCount'] = 1
    # t5 = t5.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 每个用户行为的个数user_online_action_count
    # t6 = pd.DataFrame(dataSet2_on_feature2[['user_id', 'action']])
    # t6 = t6[(t6['action'].notnull() == True)]
    # t6 = pd.DataFrame(t6['user_id'], columns=['user_id'])
    # t6['user_online_action_count'] = 1
    # t6 = t6.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 每个用户点击个数user_online_click_count
    # t7 = pd.DataFrame(dataSet2_on_feature2[['user_id', 'action']])
    # t7 = t7[(t7['action'].notnull() == True)&(t7['action']==0)]
    # t7 = pd.DataFrame(t7['user_id'], columns=['user_id'])
    # t7['user_online_click_count'] = 1
    # t7 = t7.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 每个用户领取了优惠券没有使用的次数user_online_notUseReceive_coupon
    # t8 = pd.DataFrame(dataSet2_on_feature2[['user_id', 'action','date']])
    # t8 = t8[(t8['action'].notnull() == True) & (t8['action'] == 2)&(t8['date'].isnull()==True)]
    # t8 = pd.DataFrame(t8['user_id'], columns=['user_id'])
    # t8['user_online_notUseReceive_coupon'] = 1
    # t8 = t8.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 每个用户没有使用消费券消费的次数user_online_notUse_coupon
    # t9 = pd.DataFrame(dataSet2_on_feature2[['user_id', 'coupon_id', 'date']])
    # t9 = t9[(t9['date'].notnull() == True) & (t9['coupon_id'].isnull() == True)]
    # t9 = pd.DataFrame(t9['user_id'], columns=['user_id'])
    # t9['user_online_notUse_coupon'] = 1
    # t9 = t9.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # #合并数据
    # left = dataSet2_on_feature2[['user_id']].drop_duplicates()
    # data2_on_result = pd.merge(left,t,how='left',on=['user_id'])
    # data2_on_result = pd.merge(data2_on_result,t1,how='left',on='user_id')
    # data2_on_result = pd.merge(data2_on_result,t2,how='left',on='user_id')
    # data2_on_result = pd.merge(data2_on_result,t3,how='left',on='user_id')
    # data2_on_result = pd.merge(data2_on_result,t4,how='left',on='user_id')
    # data2_on_result = pd.merge(data2_on_result,t5,how='left',on='user_id')
    # data2_on_result = pd.merge(data2_on_result,t6,how='left',on='user_id')
    # data2_on_result = pd.merge(data2_on_result,t7,how='left',on='user_id')
    # data2_on_result = pd.merge(data2_on_result,t8,how='left',on='user_id')
    # data2_on_result = pd.merge(data2_on_result,t9,how='left',on='user_id')
    #
    # #替换每列中的Nan,用平均值来代替
    # for i in data2_on_result.columns:
    #     meanVal = data2_on_result[i].mean()
    #     data2_on_result[i].fillna(meanVal,inplace=True)
    #
    # # 使用消费券消费的次数占总消费次数的占比 user_online_buy_couponRate (use_online_buy_coupon/user_online_buy_total)
    # t10 = data2_on_result['use_online_buy_coupon']
    # t_10 = data2_on_result['user_online_buy_total']
    # t10 = t10/t_10
    # data2_on_result['user_online_buy_couponRate'] = t10
    #
    # # 用户使用消费券占领取的消费券的比重  uses_online_coupon_buyRate (use_online_buy_coupon/user_online_coupon_receivedAll)
    # t11 = data2_on_result['use_online_buy_coupon']
    # t_11 = data2_on_result['user_online_coupon_receivedAll']
    # t11 = t11/t_11
    # data2_on_result['uses_online_coupon_buyRate'] = t11
    #
    # # 每个用户限时低价消费占总消费的比重 user_online_buy_fixedRate (user_online_buy_fixed/user_online_buy_total)
    # t12 = data2_on_result['user_online_buy_fixed']
    # t_12 = data2_on_result['user_online_buy_total']
    # t12 = t12/t_12
    # data2_on_result['user_online_buy_fixedRate'] = t12
    #
    # # 消费的商店占有过行为的商店的比重 user_online_merchantBuyRate (user_online_buy_merchantCount/user_online_action_merchantCount)
    # t13 = data2_on_result['user_online_buy_merchantCount']
    # t_13 = data2_on_result['user_online_action_merchantCount']
    # t13 = t13/t_13
    # data2_on_result['user_online_merchantBuyRate'] = t13
    # data2_on_result.to_csv('dataSet2_on_feature.csv', index=None)
    #
    # # dataSet1_on_feature
    # # 每个用户消费的总次数user_online_buy_total
    # t = pd.DataFrame(dataSet1_on_feature1[['user_id','date']])
    # t = t[t['date'].notnull() == True]
    # t = pd.DataFrame(t['user_id'],columns=['user_id'])
    # t['user_online_buy_total'] = 1
    # t = t.groupby('user_id',sort=False).agg('sum').reset_index()
    #
    # # 每个用户使用消费券消费的次数use_online_buy_coupon
    # t1 = pd.DataFrame(dataSet1_on_feature1[['user_id','action','coupon_id']])
    # t1 = t1[(t1['action'] == 1)&(t1['coupon_id'].notnull()==True)&(t1['coupon_id']!='fixed')]
    # t1 = pd.DataFrame(t1['user_id'], columns=['user_id'])
    # t1['use_online_buy_coupon'] = 1
    # t1 = t1.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 每个用户领取的消费券的总数user_online_coupon_receivedAll
    # t2 = pd.DataFrame(dataSet1_on_feature1[['user_id', 'action', 'coupon_id']])
    # t2 = t2[(t2['action'] == 2) & (t2['coupon_id'].notnull() == True) & (t2['coupon_id'] != 'fixed')]
    # t2 = pd.DataFrame(t2['user_id'], columns=['user_id'])
    # t2['user_online_coupon_receivedAll'] = 1
    # t2 = t2.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 每个用户在限时低价时消费的次数user_online_buy_fixed
    # t3 = pd.DataFrame(dataSet1_on_feature1[['user_id', 'action', 'coupon_id']])
    # t3 = t3[(t3['action'] == 1) & (t3['coupon_id'] == 'fixed')]
    # t3 = pd.DataFrame(t3['user_id'], columns=['user_id'])
    # t3['user_online_buy_fixed'] = 1
    # t3 = t3.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 用户购买东西的商店的个数user_online_buy_merchantCount
    # t4 = pd.DataFrame(dataSet1_on_feature1[['user_id', 'action', 'merchant_id']])
    # t4 = t4[(t4['action'] == 1) & (t4['merchant_id'].notnull()==True)]
    # t4 = pd.DataFrame(t4['user_id'], columns=['user_id'])
    # t4['user_online_buy_merchantCount'] = 1
    # t4 = t4.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 每个用户看过的商店的个数包括只点击user_online_action_merchantCount
    # t5 = pd.DataFrame(dataSet1_on_feature1[['user_id','merchant_id']])
    # t5 = t5[(t5['merchant_id'].notnull() == True)]
    # t5 = pd.DataFrame(t5['user_id'], columns=['user_id'])
    # t5['user_online_action_merchantCount'] = 1
    # t5 = t5.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 每个用户行为的个数user_online_action_count
    # t6 = pd.DataFrame(dataSet1_on_feature1[['user_id', 'action']])
    # t6 = t6[(t6['action'].notnull() == True)]
    # t6 = pd.DataFrame(t6['user_id'], columns=['user_id'])
    # t6['user_online_action_count'] = 1
    # t6 = t6.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 每个用户点击个数user_online_click_count
    # t7 = pd.DataFrame(dataSet1_on_feature1[['user_id', 'action']])
    # t7 = t7[(t7['action'].notnull() == True)&(t7['action']==0)]
    # t7 = pd.DataFrame(t7['user_id'], columns=['user_id'])
    # t7['user_online_click_count'] = 1
    # t7 = t7.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 每个用户领取了优惠券没有使用的次数user_online_notUseReceive_coupon
    # t8 = pd.DataFrame(dataSet1_on_feature1[['user_id', 'action','date']])
    # t8 = t8[(t8['action'].notnull() == True) & (t8['action'] == 2)&(t8['date'].isnull()==True)]
    # t8 = pd.DataFrame(t8['user_id'], columns=['user_id'])
    # t8['user_online_notUseReceive_coupon'] = 1
    # t8 = t8.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # # 每个用户没有使用消费券消费的次数user_online_notUse_coupon
    # t9 = pd.DataFrame(dataSet1_on_feature1[['user_id', 'coupon_id', 'date']])
    # t9 = t9[(t9['date'].notnull() == True) & (t9['coupon_id'].isnull() == True)]
    # t9 = pd.DataFrame(t9['user_id'], columns=['user_id'])
    # t9['user_online_notUse_coupon'] = 1
    # t9 = t9.groupby('user_id', sort=False).agg('sum').reset_index()
    #
    # #合并数据
    # left = dataSet1_on_feature1[['user_id']].drop_duplicates()
    # dataSet1_on_result = pd.merge(left,t,how='left',on=['user_id'])
    # dataSet1_on_result = pd.merge(dataSet1_on_result,t1,how='left',on='user_id')
    # dataSet1_on_result = pd.merge(dataSet1_on_result,t2,how='left',on='user_id')
    # dataSet1_on_result = pd.merge(dataSet1_on_result,t3,how='left',on='user_id')
    # dataSet1_on_result = pd.merge(dataSet1_on_result,t4,how='left',on='user_id')
    # dataSet1_on_result = pd.merge(dataSet1_on_result,t5,how='left',on='user_id')
    # dataSet1_on_result = pd.merge(dataSet1_on_result,t6,how='left',on='user_id')
    # dataSet1_on_result = pd.merge(dataSet1_on_result,t7,how='left',on='user_id')
    # dataSet1_on_result = pd.merge(dataSet1_on_result,t8,how='left',on='user_id')
    # dataSet1_on_result = pd.merge(dataSet1_on_result,t9,how='left',on='user_id')
    #
    # #替换每列中的Nan,用平均值来代替
    # for i in dataSet1_on_result.columns:
    #     meanVal = dataSet1_on_result[i].mean()
    #     dataSet1_on_result[i].fillna(meanVal,inplace=True)
    #
    # # 使用消费券消费的次数占总消费次数的占比 user_online_buy_couponRate (use_online_buy_coupon/user_online_buy_total)
    # t10 = dataSet1_on_result['use_online_buy_coupon']
    # t_10 = dataSet1_on_result['user_online_buy_total']
    # t10 = t10/t_10
    # dataSet1_on_result['user_online_buy_couponRate'] = t10
    #
    # # 用户使用消费券占领取的消费券的比重  uses_online_coupon_buyRate (use_online_buy_coupon/user_online_coupon_receivedAll)
    # t11 = dataSet1_on_result['use_online_buy_coupon']
    # t_11 = dataSet1_on_result['user_online_coupon_receivedAll']
    # t11 = t11/t_11
    # dataSet1_on_result['uses_online_coupon_buyRate'] = t11
    #
    # # 每个用户限时低价消费占总消费的比重 user_online_buy_fixedRate (user_online_buy_fixed/user_online_buy_total)
    # t12 = dataSet1_on_result['user_online_buy_fixed']
    # t_12 = dataSet1_on_result['user_online_buy_total']
    # t12 = t12/t_12
    # dataSet1_on_result['user_online_buy_fixedRate'] = t12
    #
    # # 消费的商店占有过行为的商店的比重 user_online_merchantBuyRate (user_online_buy_merchantCount/user_online_action_merchantCount)
    # t13 = dataSet1_on_result['user_online_buy_merchantCount']
    # t_13 = dataSet1_on_result['user_online_action_merchantCount']
    # t13 = t13/t_13
    # dataSet1_on_result['user_online_merchantBuyRate'] = t13
    #
    # dataSet1_on_result.to_csv('dataSet1_on_feature.csv', index=None)

    """
    用户线下特征：
        用户领取优惠券的次数 user_off_couponReceive_count
        用户获得了优惠券没有使用的次数 user_off_coupon_notUse
        用户领取了优惠券使用的次数 user_off_coupon_use
        用户对于消费券的核销率 user_off_couponRate
        用户总的消费次数 user_off_buyTotal
        用户使用优惠券消费占总消费的比重 user_off_useCoupon_rate
        用户核销的消费券的平均折扣率 user_off_coupon_avgDiscount
        用户使用消费券消费的商家的平均距离 user_off_merchant_avdDistance
        用户使用了消费券的商家的数量 user_off_merchantUse_count
        用户使用消费券的平均间隔 user_off_useCoupon_avgday
        用户使用消费券是周末还是工作日居多 user_off_payisWeek
    """
    # dataSet3
    # 用户领取优惠券的次数 user_off_couponReceive_count
    t = pd.DataFrame(dataSet3_off_feature3[['user_id', 'coupon_id','date_received']])
    t = t[(t['coupon_id'].notnull() == True) & (t['date_received'].notnull() == True)]
    t = pd.DataFrame(t['user_id'],columns=['user_id'])
    t['user_off_couponReceive_count'] = 1
    t = t.groupby('user_id',sort=False).agg('sum').reset_index()

    # 用户获得了优惠券没有使用的次数 user_off_coupon_notUse
    t1 = pd.DataFrame(dataSet3_off_feature3[['user_id', 'coupon_id', 'date_received','date']])
    t1 = t1[(t1['coupon_id'].notnull() == True) & (t1['date_received'].notnull() == True) & (t1['date'].isnull() == True)]
    t1 = pd.DataFrame(t['user_id'], columns=['user_id'])
    t1['user_off_coupon_notUse'] = 1
    t1 = t1.groupby('user_id', sort=False).agg('sum').reset_index()

    # 用户领取了优惠券使用的次数 user_off_coupon_use
    t2 = pd.DataFrame(dataSet3_off_feature3[['user_id', 'coupon_id', 'date_received', 'date']])
    t2 = t2[(t2['coupon_id'].notnull() == True) & (t2['date_received'].notnull() == True) & (t2['date'].isnull() == False)]
    t2 = pd.DataFrame(t['user_id'], columns=['user_id'])
    t2['user_off_coupon_use'] = 1
    t2 = t2.groupby('user_id', sort=False).agg('sum').reset_index()

    # 用户对于消费券的核销率 user_off_couponRate
    t3 = pd.merge(t,t2,how='left',on=['user_id'])
    t3['user_off_couponRate'] = round(t3['user_off_coupon_use']/t3['user_off_couponReceive_count'],4)
    t3 = pd.DataFrame(t3[['user_id','user_off_couponRate']],columns=['user_id','user_off_couponRate'])

    # 用户总的消费次数 user_off_buyTotal
    t4 = pd.DataFrame(dataSet3_off_feature3[['user_id','date']])
    t4 = t4[t4['date'].notnull() == True]
    t4 = pd.DataFrame(t4['user_id'],columns=['user_id'])
    t4['user_off_buyTotal'] = 1
    t4 = t4.groupby('user_id',sort=False).agg('sum').reset_index()


    # 用户使用优惠券消费占总消费的比重 user_off_useCoupon_rate
    t5 = pd.merge(t4, t2, how='left', on=['user_id'])
    t5['user_off_useCoupon_rate'] = round(t5['user_off_coupon_use'] / t5['user_off_buyTotal'], 4)
    t5 = pd.DataFrame(t5[['user_id', 'user_off_useCoupon_rate']], columns=['user_id', 'user_off_useCoupon_rate'])

    # 用户核销的消费券的平均折扣率 user_off_coupon_avgDiscount
    t6 = pd.DataFrame(dataSet3_off_feature3[['user_id', 'coupon_id','discount_rate','date_received']])
    t6 = t6[(t6['coupon_id'].notnull() == True) & (t6['date_received'].notnull() == True)]
    t6['user_off_coupon_avgDiscount'] = t6['discount_rate'].apply(cal_discount)
    t6 = pd.DataFrame(t6[['user_id','user_off_coupon_avgDiscount']], columns=['user_id','user_off_coupon_avgDiscount'])
    t6 = t6.groupby('user_id', sort=False).agg('mean').reset_index()


    # 用户使用消费券消费的商家的平均距离 user_off_merchant_avdDistance
    t7 = pd.DataFrame(dataSet3_off_feature3[['user_id', 'coupon_id', 'distance','date_received','date']])
    t7 = t7[(t7['coupon_id'].notnull() == True) & (t7['date_received'].notnull() == True) & (t7['date'].notnull() == True)][['user_id','distance']]
    t7 = t7.fillna(-1)
    t7['distance'] = t7['distance'].astype('int')
    t7 = t7.groupby('user_id',sort=False).agg('mean').reset_index()
    t7.rename(columns={'distance': 'user_off_merchant_avdDistance'}, inplace=True)

    # 用户使用了消费券的商家的数量 user_off_merchantUse_count
    t8 = pd.DataFrame(dataSet3_off_feature3[['user_id', 'merchant_id','coupon_id','date_received','date']])
    t8 = t8[(t8['coupon_id'].notnull() == True) & (t8['date_received'].notnull() == True) & (t8['date'].notnull() == True)]
    t8 = pd.DataFrame(t8[['user_id','merchant_id']], columns=['user_id','merchant_id']).drop_duplicates()
    t8['user_off_merchantUse_count'] = 1
    t8 = t8.groupby('user_id', sort=False).agg('sum').reset_index()
    t8 = pd.DataFrame(t8[['user_id','user_off_merchantUse_count']],columns=['user_id','user_off_merchantUse_count'])

    # 用户使用消费券的平均间隔 user_off_useCoupon_avgday
    t9 = pd.DataFrame(dataSet3_off_feature3[['user_id', 'coupon_id', 'date_received', 'date']])
    t9 = t9[(t9['coupon_id'].notnull() == True) & (t9['date_received'].notnull() == True) & (t9['date'].notnull() == True)]
    t9['user_off_useCoupon_avgday'] = t9['date'].apply(int) - t9['date_received'].apply(int)
    t9 = t9.groupby('user_id', sort=False).agg('mean').reset_index()
    t9 = pd.DataFrame(t9[['user_id', 'user_off_useCoupon_avgday']], columns=['user_id', 'user_off_useCoupon_avgday'])

    # 用户使用消费券是周末还是工作日居多 user_off_payisWeek
    t10 = pd.DataFrame(dataSet3_off_feature3[['user_id', 'coupon_id', 'date_received', 'date']])
    t10 = t10[(t10['coupon_id'].notnull() == True) & (t10['date_received'].notnull() == True) & (t10['date'].notnull() == True)]
    t10['user_off_payisWeek'] = t10['date'].apply(int).apply(isweek)
    t10 = t10.groupby('user_id', sort=False).agg('mean').reset_index()
    t10['user_off_payisWeek'] = t10['user_off_payisWeek'].apply(round)
    t10 = pd.DataFrame(t10[['user_id', 'user_off_payisWeek']], columns=['user_id', 'user_off_payisWeek'])
    #合并数据
    left = dataSet3_off_feature3[['user_id']].drop_duplicates()
    dataSet3_off_result = pd.merge(left,t,how='left',on=['user_id'])
    dataSet3_off_result = pd.merge(dataSet3_off_result,t1,how='left',on='user_id')
    dataSet3_off_result = pd.merge(dataSet3_off_result,t2,how='left',on='user_id')
    dataSet3_off_result = pd.merge(dataSet3_off_result,t3,how='left',on='user_id')
    dataSet3_off_result = pd.merge(dataSet3_off_result,t4,how='left',on='user_id')
    dataSet3_off_result = pd.merge(dataSet3_off_result,t5,how='left',on='user_id')
    dataSet3_off_result = pd.merge(dataSet3_off_result,t6,how='left',on='user_id')
    dataSet3_off_result = pd.merge(dataSet3_off_result,t7,how='left',on='user_id')
    dataSet3_off_result = pd.merge(dataSet3_off_result,t8,how='left',on='user_id')
    dataSet3_off_result = pd.merge(dataSet3_off_result,t9,how='left',on='user_id')
    dataSet3_off_result = pd.merge(dataSet3_off_result,t10,how='left',on='user_id')

    # 计算user_off_payisWeek出现次数最多的
    a = pd.Series(t10['user_off_payisWeek']).value_counts()
    if a[0]>a[1]:
        max = 0
    else:
        max = 1
    dataSet3_off_result.fillna({'user_off_payisWeek':max},inplace=True)
    dataSet3_off_result.fillna(0,inplace=True)
    dataSet3_off_result.to_csv('dataSet3_off_result.csv', index=None)

    # dataSet2
    # 用户领取优惠券的次数 user_off_couponReceive_count
    t = pd.DataFrame(dataSet2_off_feature2[['user_id', 'coupon_id', 'date_received']])
    t = t[(t['coupon_id'].notnull() == True) & (t['date_received'].notnull() == True)]
    t = pd.DataFrame(t['user_id'], columns=['user_id'])
    t['user_off_couponReceive_count'] = 1
    t = t.groupby('user_id', sort=False).agg('sum').reset_index()

    # 用户获得了优惠券没有使用的次数 user_off_coupon_notUse
    t1 = pd.DataFrame(dataSet2_off_feature2[['user_id', 'coupon_id', 'date_received', 'date']])
    t1 = t1[
        (t1['coupon_id'].notnull() == True) & (t1['date_received'].notnull() == True) & (t1['date'].isnull() == True)]
    t1 = pd.DataFrame(t['user_id'], columns=['user_id'])
    t1['user_off_coupon_notUse'] = 1
    t1 = t1.groupby('user_id', sort=False).agg('sum').reset_index()

    # 用户领取了优惠券使用的次数 user_off_coupon_use
    t2 = pd.DataFrame(dataSet2_off_feature2[['user_id', 'coupon_id', 'date_received', 'date']])
    t2 = t2[
        (t2['coupon_id'].notnull() == True) & (t2['date_received'].notnull() == True) & (t2['date'].isnull() == False)]
    t2 = pd.DataFrame(t['user_id'], columns=['user_id'])
    t2['user_off_coupon_use'] = 1
    t2 = t2.groupby('user_id', sort=False).agg('sum').reset_index()

    # 用户对于消费券的核销率 user_off_couponRate
    t3 = pd.merge(t, t2, how='left', on=['user_id'])
    t3['user_off_couponRate'] = round(t3['user_off_coupon_use'] / t3['user_off_couponReceive_count'], 4)
    t3 = pd.DataFrame(t3[['user_id', 'user_off_couponRate']], columns=['user_id', 'user_off_couponRate'])

    # 用户总的消费次数 user_off_buyTotal
    t4 = pd.DataFrame(dataSet2_off_feature2[['user_id', 'date']])
    t4 = t4[t4['date'].notnull() == True]
    t4 = pd.DataFrame(t4['user_id'], columns=['user_id'])
    t4['user_off_buyTotal'] = 1
    t4 = t4.groupby('user_id', sort=False).agg('sum').reset_index()

    # 用户使用优惠券消费占总消费的比重 user_off_useCoupon_rate
    t5 = pd.merge(t4, t2, how='left', on=['user_id'])
    t5['user_off_useCoupon_rate'] = round(t5['user_off_coupon_use'] / t5['user_off_buyTotal'], 4)
    t5 = pd.DataFrame(t5[['user_id', 'user_off_useCoupon_rate']], columns=['user_id', 'user_off_useCoupon_rate'])

    # 用户核销的消费券的平均折扣率 user_off_coupon_avgDiscount
    t6 = pd.DataFrame(dataSet2_off_feature2[['user_id', 'coupon_id', 'discount_rate', 'date_received']])
    t6 = t6[(t6['coupon_id'].notnull() == True) & (t6['date_received'].notnull() == True)]
    t6['user_off_coupon_avgDiscount'] = t6['discount_rate'].apply(cal_discount)
    t6 = pd.DataFrame(t6[['user_id', 'user_off_coupon_avgDiscount']],
                      columns=['user_id', 'user_off_coupon_avgDiscount'])
    t6 = t6.groupby('user_id', sort=False).agg('mean').reset_index()

    # 用户使用消费券消费的商家的平均距离 user_off_merchant_avdDistance
    t7 = pd.DataFrame(dataSet2_off_feature2[['user_id', 'coupon_id', 'distance', 'date_received', 'date']])
    t7 = \
    t7[(t7['coupon_id'].notnull() == True) & (t7['date_received'].notnull() == True) & (t7['date'].notnull() == True)][
        ['user_id', 'distance']]
    t7 = t7.fillna(-1)
    t7['distance'] = t7['distance'].astype('int')
    t7 = t7.groupby('user_id', sort=False).agg('mean').reset_index()
    t7.rename(columns={'distance': 'user_off_merchant_avdDistance'}, inplace=True)

    # 用户使用了消费券的商家的数量 user_off_merchantUse_count
    t8 = pd.DataFrame(dataSet2_off_feature2[['user_id', 'merchant_id', 'coupon_id', 'date_received', 'date']])
    t8 = t8[
        (t8['coupon_id'].notnull() == True) & (t8['date_received'].notnull() == True) & (t8['date'].notnull() == True)]
    t8 = pd.DataFrame(t8[['user_id', 'merchant_id']], columns=['user_id', 'merchant_id']).drop_duplicates()
    t8['user_off_merchantUse_count'] = 1
    t8 = t8.groupby('user_id', sort=False).agg('sum').reset_index()
    t8 = pd.DataFrame(t8[['user_id', 'user_off_merchantUse_count']], columns=['user_id', 'user_off_merchantUse_count'])

    # 用户使用消费券的平均间隔 user_off_useCoupon_avgday
    t9 = pd.DataFrame(dataSet2_off_feature2[['user_id', 'coupon_id', 'date_received', 'date']])
    t9 = t9[
        (t9['coupon_id'].notnull() == True) & (t9['date_received'].notnull() == True) & (t9['date'].notnull() == True)]
    t9['user_off_useCoupon_avgday'] = t9['date'].apply(int) - t9['date_received'].apply(int)
    t9 = t9.groupby('user_id', sort=False).agg('mean').reset_index()
    t9 = pd.DataFrame(t9[['user_id', 'user_off_useCoupon_avgday']], columns=['user_id', 'user_off_useCoupon_avgday'])

    # 用户使用消费券是周末还是工作日居多 user_off_payisWeek
    t10 = pd.DataFrame(dataSet2_off_feature2[['user_id', 'coupon_id', 'date_received', 'date']])
    t10 = t10[(t10['coupon_id'].notnull() == True) & (t10['date_received'].notnull() == True) & (
                t10['date'].notnull() == True)]
    t10['user_off_payisWeek'] = t10['date'].apply(int).apply(isweek)
    t10 = t10.groupby('user_id', sort=False).agg('mean').reset_index()
    t10['user_off_payisWeek'] = t10['user_off_payisWeek'].apply(round)
    t10 = pd.DataFrame(t10[['user_id', 'user_off_payisWeek']], columns=['user_id', 'user_off_payisWeek'])
    # 合并数据
    left = dataSet2_off_feature2[['user_id']].drop_duplicates()
    dataSet2_off_result = pd.merge(left, t, how='left', on=['user_id'])
    dataSet2_off_result = pd.merge(dataSet2_off_result, t1, how='left', on='user_id')
    dataSet2_off_result = pd.merge(dataSet2_off_result, t2, how='left', on='user_id')
    dataSet2_off_result = pd.merge(dataSet2_off_result, t3, how='left', on='user_id')
    dataSet2_off_result = pd.merge(dataSet2_off_result, t4, how='left', on='user_id')
    dataSet2_off_result = pd.merge(dataSet2_off_result, t5, how='left', on='user_id')
    dataSet2_off_result = pd.merge(dataSet2_off_result, t6, how='left', on='user_id')
    dataSet2_off_result = pd.merge(dataSet2_off_result, t7, how='left', on='user_id')
    dataSet2_off_result = pd.merge(dataSet2_off_result, t8, how='left', on='user_id')
    dataSet2_off_result = pd.merge(dataSet2_off_result, t9, how='left', on='user_id')
    dataSet2_off_result = pd.merge(dataSet2_off_result, t10, how='left', on='user_id')

    # 计算user_off_payisWeek出现次数最多的
    a = pd.Series(t10['user_off_payisWeek']).value_counts()
    if a[0] > a[1]:
        max = 0
    else:
        max = 1
    dataSet2_off_result.fillna({'user_off_payisWeek': max}, inplace=True)
    dataSet2_off_result.fillna(0, inplace=True)
    dataSet2_off_result.to_csv('dataSet2_off_result.csv', index=None)

    # dataSet1
    # 用户领取优惠券的次数 user_off_couponReceive_count
    t = pd.DataFrame(dataSet1_off_feature1[['user_id', 'coupon_id', 'date_received']])
    t = t[(t['coupon_id'].notnull() == True) & (t['date_received'].notnull() == True)]
    t = pd.DataFrame(t['user_id'], columns=['user_id'])
    t['user_off_couponReceive_count'] = 1
    t = t.groupby('user_id', sort=False).agg('sum').reset_index()

    # 用户获得了优惠券没有使用的次数 user_off_coupon_notUse
    t1 = pd.DataFrame(dataSet1_off_feature1[['user_id', 'coupon_id', 'date_received', 'date']])
    t1 = t1[
        (t1['coupon_id'].notnull() == True) & (t1['date_received'].notnull() == True) & (t1['date'].isnull() == True)]
    t1 = pd.DataFrame(t['user_id'], columns=['user_id'])
    t1['user_off_coupon_notUse'] = 1
    t1 = t1.groupby('user_id', sort=False).agg('sum').reset_index()

    # 用户领取了优惠券使用的次数 user_off_coupon_use
    t2 = pd.DataFrame(dataSet1_off_feature1[['user_id', 'coupon_id', 'date_received', 'date']])
    t2 = t2[
        (t2['coupon_id'].notnull() == True) & (t2['date_received'].notnull() == True) & (t2['date'].isnull() == False)]
    t2 = pd.DataFrame(t['user_id'], columns=['user_id'])
    t2['user_off_coupon_use'] = 1
    t2 = t2.groupby('user_id', sort=False).agg('sum').reset_index()

    # 用户对于消费券的核销率 user_off_couponRate
    t3 = pd.merge(t, t2, how='left', on=['user_id'])
    t3['user_off_couponRate'] = round(t3['user_off_coupon_use'] / t3['user_off_couponReceive_count'], 4)
    t3 = pd.DataFrame(t3[['user_id', 'user_off_couponRate']], columns=['user_id', 'user_off_couponRate'])

    # 用户总的消费次数 user_off_buyTotal
    t4 = pd.DataFrame(dataSet1_off_feature1[['user_id', 'date']])
    t4 = t4[t4['date'].notnull() == True]
    t4 = pd.DataFrame(t4['user_id'], columns=['user_id'])
    t4['user_off_buyTotal'] = 1
    t4 = t4.groupby('user_id', sort=False).agg('sum').reset_index()

    # 用户使用优惠券消费占总消费的比重 user_off_useCoupon_rate
    t5 = pd.merge(t4, t2, how='left', on=['user_id'])
    t5['user_off_useCoupon_rate'] = round(t5['user_off_coupon_use'] / t5['user_off_buyTotal'], 4)
    t5 = pd.DataFrame(t5[['user_id', 'user_off_useCoupon_rate']], columns=['user_id', 'user_off_useCoupon_rate'])

    # 用户核销的消费券的平均折扣率 user_off_coupon_avgDiscount
    t6 = pd.DataFrame(dataSet1_off_feature1[['user_id', 'coupon_id', 'discount_rate', 'date_received']])
    t6 = t6[(t6['coupon_id'].notnull() == True) & (t6['date_received'].notnull() == True)]
    t6['user_off_coupon_avgDiscount'] = t6['discount_rate'].apply(cal_discount)
    t6 = pd.DataFrame(t6[['user_id', 'user_off_coupon_avgDiscount']],
                      columns=['user_id', 'user_off_coupon_avgDiscount'])
    t6 = t6.groupby('user_id', sort=False).agg('mean').reset_index()

    # 用户使用消费券消费的商家的平均距离 user_off_merchant_avdDistance
    t7 = pd.DataFrame(dataSet1_off_feature1[['user_id', 'coupon_id', 'distance', 'date_received', 'date']])
    t7 = \
    t7[(t7['coupon_id'].notnull() == True) & (t7['date_received'].notnull() == True) & (t7['date'].notnull() == True)][
        ['user_id', 'distance']]
    t7 = t7.fillna(-1)
    t7['distance'] = t7['distance'].astype('int')
    t7 = t7.groupby('user_id', sort=False).agg('mean').reset_index()
    t7.rename(columns={'distance': 'user_off_merchant_avdDistance'}, inplace=True)

    # 用户使用了消费券的商家的数量 user_off_merchantUse_count
    t8 = pd.DataFrame(dataSet1_off_feature1[['user_id', 'merchant_id', 'coupon_id', 'date_received', 'date']])
    t8 = t8[
        (t8['coupon_id'].notnull() == True) & (t8['date_received'].notnull() == True) & (t8['date'].notnull() == True)]
    t8 = pd.DataFrame(t8[['user_id', 'merchant_id']], columns=['user_id', 'merchant_id']).drop_duplicates()
    t8['user_off_merchantUse_count'] = 1
    t8 = t8.groupby('user_id', sort=False).agg('sum').reset_index()
    t8 = pd.DataFrame(t8[['user_id', 'user_off_merchantUse_count']], columns=['user_id', 'user_off_merchantUse_count'])

    # 用户使用消费券的平均间隔 user_off_useCoupon_avgday
    t9 = pd.DataFrame(dataSet1_off_feature1[['user_id', 'coupon_id', 'date_received', 'date']])
    t9 = t9[
        (t9['coupon_id'].notnull() == True) & (t9['date_received'].notnull() == True) & (t9['date'].notnull() == True)]
    t9['user_off_useCoupon_avgday'] = t9['date'].apply(int) - t9['date_received'].apply(int)
    t9 = t9.groupby('user_id', sort=False).agg('mean').reset_index()
    t9 = pd.DataFrame(t9[['user_id', 'user_off_useCoupon_avgday']], columns=['user_id', 'user_off_useCoupon_avgday'])

    # 用户使用消费券是周末还是工作日居多 user_off_payisWeek
    t10 = pd.DataFrame(dataSet1_off_feature1[['user_id', 'coupon_id', 'date_received', 'date']])
    t10 = t10[(t10['coupon_id'].notnull() == True) & (t10['date_received'].notnull() == True) & (
                t10['date'].notnull() == True)]
    t10['user_off_payisWeek'] = t10['date'].apply(int).apply(isweek)
    t10 = t10.groupby('user_id', sort=False).agg('mean').reset_index()
    t10['user_off_payisWeek'] = t10['user_off_payisWeek'].apply(round)
    t10 = pd.DataFrame(t10[['user_id', 'user_off_payisWeek']], columns=['user_id', 'user_off_payisWeek'])
    # 合并数据
    left = dataSet1_off_feature1[['user_id']].drop_duplicates()
    dataSet1_off_result = pd.merge(left, t, how='left', on=['user_id'])
    dataSet1_off_result = pd.merge(dataSet1_off_result, t1, how='left', on='user_id')
    dataSet1_off_result = pd.merge(dataSet1_off_result, t2, how='left', on='user_id')
    dataSet1_off_result = pd.merge(dataSet1_off_result, t3, how='left', on='user_id')
    dataSet1_off_result = pd.merge(dataSet1_off_result, t4, how='left', on='user_id')
    dataSet1_off_result = pd.merge(dataSet1_off_result, t5, how='left', on='user_id')
    dataSet1_off_result = pd.merge(dataSet1_off_result, t6, how='left', on='user_id')
    dataSet1_off_result = pd.merge(dataSet1_off_result, t7, how='left', on='user_id')
    dataSet1_off_result = pd.merge(dataSet1_off_result, t8, how='left', on='user_id')
    dataSet1_off_result = pd.merge(dataSet1_off_result, t9, how='left', on='user_id')
    dataSet1_off_result = pd.merge(dataSet1_off_result, t10, how='left', on='user_id')

    # 计算user_off_payisWeek出现次数最多的
    a = pd.Series(t10['user_off_payisWeek']).value_counts()
    if a[0] > a[1]:
        max = 0
    else:
        max = 1
    dataSet1_off_result.fillna({'user_off_payisWeek': max}, inplace=True)
    dataSet1_off_result.fillna(0, inplace=True)
    dataSet1_off_result.to_csv('dataSet1_off_result.csv', index=None)

    """
    商家相关的特征：
        商家被消费的次数：merchant_buy_count
        商家优惠券被领取的次数 merchant_coupon_receive
        商家优惠券被使用的次数 merchant_coupon_use
        商家优惠券没有被使用的次数 merchant_coupon_notUse
        商家的消费券的类别的个数 merchant_coupon_kinds
        商家被核销的消费券类别个数 merchant_couponUse_kinds
        商家的消费券的平均折扣率 merchant_coupon_avgDiscount
        商家的满减消费券的所需要的平均价格 merchant_coupon_avgManjian
        商家满减优惠券满减的平均金额 merchant_coupon_avgPrice
        商家满减优惠券的使用次数 merchant_manjian_useCount
        直接优惠的优惠券使用次数 merchant_zhijie_useCount
        商家的消费券从领取到消费经历的平均天数 merchant_avgDay
        商家被核销的消费券到用户的平均距离  merchant_avgDistance
        商家优惠券的使用率  merchant_coupon_useRate (merchant_coupon_use/merchant_coupon_receive)
        商家满减优惠券的核销率 merchant_manjian_useRate ( merchant_manjian_useCount/merchant_coupon_use)
        商家打折优惠券的核销率 merchant_zhijie_useRate (merchant_zhijie_useCount/merchant_coupon_use)
    """
    # dataSet3
    # 商家被消费的次数：merchant_buy_count
    # t = pd.DataFrame(dataSet3_off_feature3[['merchant_id','date']])
    # t = t[t['date'].notnull() == True]
    # t = pd.DataFrame(t['merchant_id'], columns=['merchant_id'])
    # t['merchant_buy_count'] = 1
    # t = t.groupby('merchant_id', sort=False).agg('sum').reset_index()
    #
    # # 商家优惠券被领取的次数 merchant_coupon_receive
    # t1 = pd.DataFrame(dataSet3_off_feature3[['merchant_id', 'coupon_id', 'date_received']])
    # t1 = t1[(t1['coupon_id'].notnull() == True) & (t1['date_received'].notnull()==True)]
    # t1 = pd.DataFrame(t1['merchant_id'], columns=['merchant_id'])
    # t1['merchant_coupon_receive'] = 1
    # t1 = t1.groupby('merchant_id', sort=False).agg('sum').reset_index()
    #
    # # 商家优惠券被使用的次数 merchant_coupon_use
    # t2 = pd.DataFrame(dataSet3_off_feature3[['merchant_id', 'coupon_id', 'date_received', 'date']])
    # t2 = t2[(t2['coupon_id'].notnull() == True) & (t2['date_received'].notnull()==True) & (t2['date'].notnull()==True)]
    # t2 = pd.DataFrame(t2['merchant_id'], columns=['merchant_id'])
    # t2['merchant_coupon_use'] = 1
    # t2 = t2.groupby('merchant_id', sort=False).agg('sum').reset_index()
    #
    # # 商家优惠券没有被使用的次数 merchant_coupon_notUse
    # t3 = pd.DataFrame(dataSet3_off_feature3[['merchant_id', 'coupon_id', 'date_received', 'date']])
    # t3 = t3[(t3['coupon_id'].notnull() == True) & (t3['date_received'].notnull() == True) & (t3['date'].notnull() == False)]
    # t3 = pd.DataFrame(t3['merchant_id'], columns=['merchant_id'])
    # t3['merchant_coupon_notUse'] = 1
    # t3 = t3.groupby('merchant_id', sort=False).agg('sum').reset_index()
    #
    # # 商家的消费券的类别的个数 merchant_coupon_kinds
    # t4 = pd.DataFrame(dataSet3_off_feature3[['merchant_id', 'coupon_id']])
    # t4 = t4[t4['coupon_id'].notnull() == True]
    # t4 = t4.drop_duplicates()
    # t4 = pd.DataFrame(t4['merchant_id'], columns=['merchant_id'])
    # t4['merchant_coupon_kinds'] = 1
    # t4 = t4.groupby('merchant_id', sort=False).agg('sum').reset_index()
    #
    # # 商家被核销的消费券类别个数 merchant_couponUse_kinds
    # t5 = pd.DataFrame(dataSet3_off_feature3[['merchant_id', 'coupon_id','date']])
    # t5 = t5[(t5['coupon_id'].notnull() == True) & (t5['date'].notnull()==True)]
    # t5 = t5[['merchant_id','coupon_id']]
    # t5 = t5.drop_duplicates()
    # t5 = pd.DataFrame(t5['merchant_id'], columns=['merchant_id'])
    # t5['merchant_couponUse_kinds'] = 1
    # t5 = t5.groupby('merchant_id', sort=False).agg('sum').reset_index()
    #
    # # 商家的消费券的平均折扣率 merchant_coupon_avgDiscount
    # def cal_discount(s):
    #     s = str(s)
    #     s = s.split(':')
    #     if len(s)==1:
    #         return float(s[0])
    #     else:
    #         return round(1.0 - float(s[1]) / float(s[0]),4)
    #
    # t6 = pd.DataFrame(dataSet3_off_feature3[['merchant_id', 'coupon_id','discount_rate']])
    # t6 = t6[t6['coupon_id'].notnull() == True]
    # t6['coupon_id'] = int(1)
    # t6['discount_rate'] = t6['discount_rate'].apply(cal_discount)
    # t6 = t6.groupby('merchant_id', sort=False).agg('sum').reset_index()
    # t6['merchant_coupon_avgDiscount'] = t6['discount_rate']/t6['coupon_id']
    # t6 = pd.DataFrame(t6[['merchant_id','merchant_coupon_avgDiscount']],columns=['merchant_id','merchant_coupon_avgDiscount'])
    #
    # # 商家的满减消费券的所需要的平均价格 merchant_coupon_avgManjian
    # def is_manjian(s):
    #     s = str(s)
    #     s = s.split(':')
    #     if len(s) == 1:
    #         return int(0)
    #     else:
    #         return int(s[0])
    # t7 = pd.DataFrame(dataSet3_off_feature3[['merchant_id', 'coupon_id','discount_rate']])
    # t7['discount_rate'] = t7['discount_rate'].apply(is_manjian)
    # t7 = t7[(t7['coupon_id'].notnull() == True) & (t7['discount_rate']!=0)]
    # t7['coupon_id'] = int(1)
    # t7 = t7.groupby('merchant_id', sort=False).agg('sum').reset_index()
    # t7['merchant_coupon_avgManjian'] = round(t7['discount_rate'] / t7['coupon_id'],4)
    # t7 = pd.DataFrame(t7[['merchant_id', 'merchant_coupon_avgManjian']],columns=['merchant_id', 'merchant_coupon_avgManjian'])
    #
    # # 商家满减优惠券满减的平均金额 merchant_coupon_avgPrice
    # def manjian(s):
    #     s = str(s)
    #     s = s.split(':')
    #     if len(s) == 1:
    #         return int(0)
    #     else:
    #         return int(s[1])
    # t8 = pd.DataFrame(dataSet3_off_feature3[['merchant_id', 'coupon_id', 'discount_rate']])
    # t8['discount_rate'] = t8['discount_rate'].apply(manjian)
    # t8 = t8[(t8['coupon_id'].notnull() == True) & (t8['discount_rate'] != 0)]
    # t8['coupon_id'] = int(1)
    # t8 = t8.groupby('merchant_id', sort=False).agg('sum').reset_index()
    # t8['merchant_coupon_avgPrice'] = round(t8['discount_rate'] / t8['coupon_id'], 4)
    # t8 = pd.DataFrame(t8[['merchant_id', 'merchant_coupon_avgPrice']],columns=['merchant_id', 'merchant_coupon_avgPrice'])
    #
    # # 商家满减优惠券的使用次数 merchant_manjian_useCount
    # def classify(s): # 直接优惠记为0，满减记为1
    #     s = str(s)
    #     s = s.split(':')
    #     if len(s) == 1:
    #         return 0
    #     else:
    #         return 1
    #
    #
    # t9 = pd.DataFrame(dataSet3_off_feature3[['merchant_id', 'coupon_id', 'discount_rate', 'date']])
    # t9['discount_rate'] = t9['discount_rate'].apply(classify)
    # # 满减优惠券使用次数
    # t9 = t9[(t9['coupon_id'].notnull() == True) & (t9['discount_rate'] == 1) & (t9['date'].notnull()==True)]
    # t9['merchant_manjian_useCount'] = 1
    # t9 = t9.groupby('merchant_id', sort=False).agg('sum').reset_index()
    # t9 = pd.DataFrame(t9[['merchant_id', 'merchant_manjian_useCount']],columns=['merchant_id', 'merchant_manjian_useCount'])
    #
    # # 直接优惠的优惠券使用次数 merchant_zhijie_useCount
    # t10 = pd.DataFrame(dataSet3_off_feature3[['merchant_id', 'coupon_id', 'discount_rate', 'date']])
    # t10['discount_rate'] = t10['discount_rate'].apply(classify)
    # t10 = t10[(t10['coupon_id'].notnull() == True) & (t10['discount_rate'] == 0) & (t10['date'].notnull() == True)]
    # t10['merchant_zhijie_useCount'] = 1
    # t10 = t10.groupby('merchant_id', sort=False).agg('sum').reset_index()
    # t10 = pd.DataFrame(t10[['merchant_id', 'merchant_zhijie_useCount']],columns=['merchant_id', 'merchant_zhijie_useCount'])
    #
    # # 商家的消费券从领取到消费经历的平均天数 merchant_avgDay
    # t11 = pd.DataFrame(dataSet3_off_feature3[['merchant_id', 'coupon_id', 'date_received', 'date']])
    # t11 = t11[(t11['coupon_id'].notnull() == True) & (t11['date_received'].notnull()==True) & (t11['date'].notnull() == True)]
    # t11['merchant_avgDay'] = t11['date']-t11['date_received']
    # t11['coupon_id'] = 1
    # t11 = t11.groupby('merchant_id', sort=False).agg('sum').reset_index()
    # t11['merchant_avgDay'] = round(t11['merchant_avgDay']/t11['coupon_id'],4)
    # t11 = pd.DataFrame(t11[['merchant_id', 'merchant_avgDay']],columns=['merchant_id', 'merchant_avgDay'])
    #
    # # 商家被核销的消费券到用户的平均距离  merchant_avgDistance
    # t12 = pd.DataFrame(dataSet3_off_feature3[['merchant_id', 'coupon_id', 'distance','date']])
    # t12 = t12[(t12['coupon_id'].notnull() == True) & (t12['date'].notnull() == True)][['merchant_id','distance']]
    # t12 = t12.fillna(-1)
    # t12['distance'] = t12['distance'].astype('int')
    # t12 = t12.groupby('merchant_id').agg('mean').reset_index()
    # t12.rename(columns={'distance': 'merchant_avgDistance'}, inplace=True)
    #
    # # 合并数据
    # left = dataSet3_off_feature3[['merchant_id']].drop_duplicates()
    # dataSet3_off_result = pd.merge(left,t,how='left',on=['merchant_id'])
    # dataSet3_off_result = pd.merge(dataSet3_off_result,t1,how='left',on=['merchant_id'])
    # dataSet3_off_result = pd.merge(dataSet3_off_result,t2,how='left',on=['merchant_id'])
    # dataSet3_off_result = pd.merge(dataSet3_off_result,t3,how='left',on=['merchant_id'])
    # dataSet3_off_result = pd.merge(dataSet3_off_result,t4,how='left',on=['merchant_id'])
    # dataSet3_off_result = pd.merge(dataSet3_off_result,t5,how='left',on=['merchant_id'])
    # dataSet3_off_result = pd.merge(dataSet3_off_result,t6,how='left',on=['merchant_id'])
    # dataSet3_off_result = pd.merge(dataSet3_off_result,t7,how='left',on=['merchant_id'])
    # dataSet3_off_result = pd.merge(dataSet3_off_result,t8,how='left',on=['merchant_id'])
    # dataSet3_off_result = pd.merge(dataSet3_off_result,t9,how='left',on=['merchant_id'])
    # dataSet3_off_result = pd.merge(dataSet3_off_result,t10,how='left',on=['merchant_id'])
    # dataSet3_off_result = pd.merge(dataSet3_off_result,t11,how='left',on=['merchant_id'])
    # dataSet3_off_result = pd.merge(dataSet3_off_result,t12,how='left',on=['merchant_id'])
    #
    # #填充Nan值
    # for i in dataSet3_off_result.columns:
    #     meanVal = dataSet3_off_result[i].mean()
    #     dataSet3_off_result[i].fillna(meanVal,inplace=True)
    #
    # # 商家优惠券的使用率  merchant_coupon_useRate (merchant_coupon_use/merchant_coupon_receive)
    # dataSet3_off_result['merchant_coupon_useRate'] = round(
    #                                                 dataSet3_off_result['merchant_coupon_use']/dataSet3_off_result['merchant_coupon_receive'],4)
    #
    # # 商家满减优惠券的核销率 merchant_manjian_useRate ( merchant_manjian_useCount/merchant_coupon_use)
    # dataSet3_off_result['merchant_manjian_useRate'] = round(
    #                                                 dataSet3_off_result['merchant_manjian_useCount'] / dataSet3_off_result['merchant_coupon_use'], 4)
    #
    # # 商家打折优惠券的核销率 merchant_zhijie_useRate (merchant_zhijie_useCount/merchant_coupon_use)
    # dataSet3_off_result['merchant_zhijie_useRate'] = round(
    #                                                 dataSet3_off_result['merchant_zhijie_useCount'] / dataSet3_off_result['merchant_coupon_use'], 4)
    #
    # dataSet3_off_result.to_csv('dataSet3_off_merchant_feature.csv', index=None)

    # dataSet2
    # 商家被消费的次数：merchant_buy_count
    # t = pd.DataFrame(dataSet2_off_feature2[['merchant_id','date']])
    # t = t[t['date'].notnull() == True]
    # t = pd.DataFrame(t['merchant_id'], columns=['merchant_id'])
    # t['merchant_buy_count'] = 1
    # t = t.groupby('merchant_id', sort=False).agg('sum').reset_index()
    #
    # # 商家优惠券被领取的次数 merchant_coupon_receive
    # t1 = pd.DataFrame(dataSet2_off_feature2[['merchant_id', 'coupon_id', 'date_received']])
    # t1 = t1[(t1['coupon_id'].notnull() == True) & (t1['date_received'].notnull()==True)]
    # t1 = pd.DataFrame(t1['merchant_id'], columns=['merchant_id'])
    # t1['merchant_coupon_receive'] = 1
    # t1 = t1.groupby('merchant_id', sort=False).agg('sum').reset_index()
    #
    # # 商家优惠券被使用的次数 merchant_coupon_use
    # t2 = pd.DataFrame(dataSet2_off_feature2[['merchant_id', 'coupon_id', 'date_received', 'date']])
    # t2 = t2[(t2['coupon_id'].notnull() == True) & (t2['date_received'].notnull()==True) & (t2['date'].notnull()==True)]
    # t2 = pd.DataFrame(t2['merchant_id'], columns=['merchant_id'])
    # t2['merchant_coupon_use'] = 1
    # t2 = t2.groupby('merchant_id', sort=False).agg('sum').reset_index()
    #
    # # 商家优惠券没有被使用的次数 merchant_coupon_notUse
    # t3 = pd.DataFrame(dataSet2_off_feature2[['merchant_id', 'coupon_id', 'date_received', 'date']])
    # t3 = t3[(t3['coupon_id'].notnull() == True) & (t3['date_received'].notnull() == True) & (t3['date'].notnull() == False)]
    # t3 = pd.DataFrame(t3['merchant_id'], columns=['merchant_id'])
    # t3['merchant_coupon_notUse'] = 1
    # t3 = t3.groupby('merchant_id', sort=False).agg('sum').reset_index()
    #
    # # 商家的消费券的类别的个数 merchant_coupon_kinds
    # t4 = pd.DataFrame(dataSet2_off_feature2[['merchant_id', 'coupon_id']])
    # t4 = t4[t4['coupon_id'].notnull() == True]
    # t4 = t4.drop_duplicates()
    # t4 = pd.DataFrame(t4['merchant_id'], columns=['merchant_id'])
    # t4['merchant_coupon_kinds'] = 1
    # t4 = t4.groupby('merchant_id', sort=False).agg('sum').reset_index()
    #
    # # 商家被核销的消费券类别个数 merchant_couponUse_kinds
    # t5 = pd.DataFrame(dataSet2_off_feature2[['merchant_id', 'coupon_id','date']])
    # t5 = t5[(t5['coupon_id'].notnull() == True) & (t5['date'].notnull()==True)]
    # t5 = t5[['merchant_id','coupon_id']]
    # t5 = t5.drop_duplicates()
    # t5 = pd.DataFrame(t5['merchant_id'], columns=['merchant_id'])
    # t5['merchant_couponUse_kinds'] = 1
    # t5 = t5.groupby('merchant_id', sort=False).agg('sum').reset_index()
    #
    # # 商家的消费券的平均折扣率 merchant_coupon_avgDiscount
    # def cal_discount(s):
    #     s = str(s)
    #     s = s.split(':')
    #     if len(s)==1:
    #         return float(s[0])
    #     else:
    #         return round(1.0 - float(s[1]) / float(s[0]),4)
    #
    # t6 = pd.DataFrame(dataSet2_off_feature2[['merchant_id', 'coupon_id','discount_rate']])
    # t6 = t6[t6['coupon_id'].notnull() == True]
    # t6['coupon_id'] = int(1)
    # t6['discount_rate'] = t6['discount_rate'].apply(cal_discount)
    # t6 = t6.groupby('merchant_id', sort=False).agg('sum').reset_index()
    # t6['merchant_coupon_avgDiscount'] = t6['discount_rate']/t6['coupon_id']
    # t6 = pd.DataFrame(t6[['merchant_id','merchant_coupon_avgDiscount']],columns=['merchant_id','merchant_coupon_avgDiscount'])
    #
    # # 商家的满减消费券的所需要的平均价格 merchant_coupon_avgManjian
    # def is_manjian(s):
    #     s = str(s)
    #     s = s.split(':')
    #     if len(s) == 1:
    #         return int(0)
    #     else:
    #         return int(s[0])
    # t7 = pd.DataFrame(dataSet2_off_feature2[['merchant_id', 'coupon_id','discount_rate']])
    # t7['discount_rate'] = t7['discount_rate'].apply(is_manjian)
    # t7 = t7[(t7['coupon_id'].notnull() == True) & (t7['discount_rate']!=0)]
    # t7['coupon_id'] = int(1)
    # t7 = t7.groupby('merchant_id', sort=False).agg('sum').reset_index()
    # t7['merchant_coupon_avgManjian'] = round(t7['discount_rate'] / t7['coupon_id'],4)
    # t7 = pd.DataFrame(t7[['merchant_id', 'merchant_coupon_avgManjian']],columns=['merchant_id', 'merchant_coupon_avgManjian'])
    #
    # # 商家满减优惠券满减的平均金额 merchant_coupon_avgPrice
    # def manjian(s):
    #     s = str(s)
    #     s = s.split(':')
    #     if len(s) == 1:
    #         return int(0)
    #     else:
    #         return int(s[1])
    # t8 = pd.DataFrame(dataSet2_off_feature2[['merchant_id', 'coupon_id', 'discount_rate']])
    # t8['discount_rate'] = t8['discount_rate'].apply(manjian)
    # t8 = t8[(t8['coupon_id'].notnull() == True) & (t8['discount_rate'] != 0)]
    # t8['coupon_id'] = int(1)
    # t8 = t8.groupby('merchant_id', sort=False).agg('sum').reset_index()
    # t8['merchant_coupon_avgPrice'] = round(t8['discount_rate'] / t8['coupon_id'], 4)
    # t8 = pd.DataFrame(t8[['merchant_id', 'merchant_coupon_avgPrice']],columns=['merchant_id', 'merchant_coupon_avgPrice'])
    #
    # # 商家满减优惠券的使用次数 merchant_manjian_useCount
    # def classify(s): # 直接优惠记为0，满减记为1
    #     s = str(s)
    #     s = s.split(':')
    #     if len(s) == 1:
    #         return 0
    #     else:
    #         return 1
    #
    #
    # t9 = pd.DataFrame(dataSet2_off_feature2[['merchant_id', 'coupon_id', 'discount_rate', 'date']])
    # t9['discount_rate'] = t9['discount_rate'].apply(classify)
    # # 满减优惠券使用次数
    # t9 = t9[(t9['coupon_id'].notnull() == True) & (t9['discount_rate'] == 1) & (t9['date'].notnull()==True)]
    # t9['merchant_manjian_useCount'] = 1
    # t9 = t9.groupby('merchant_id', sort=False).agg('sum').reset_index()
    # t9 = pd.DataFrame(t9[['merchant_id', 'merchant_manjian_useCount']],columns=['merchant_id', 'merchant_manjian_useCount'])
    #
    # # 直接优惠的优惠券使用次数 merchant_zhijie_useCount
    # t10 = pd.DataFrame(dataSet2_off_feature2[['merchant_id', 'coupon_id', 'discount_rate', 'date']])
    # t10['discount_rate'] = t10['discount_rate'].apply(classify)
    # t10 = t10[(t10['coupon_id'].notnull() == True) & (t10['discount_rate'] == 0) & (t10['date'].notnull() == True)]
    # t10['merchant_zhijie_useCount'] = 1
    # t10 = t10.groupby('merchant_id', sort=False).agg('sum').reset_index()
    # t10 = pd.DataFrame(t10[['merchant_id', 'merchant_zhijie_useCount']],columns=['merchant_id', 'merchant_zhijie_useCount'])
    #
    # # 商家的消费券从领取到消费经历的平均天数 merchant_avgDay
    # t11 = pd.DataFrame(dataSet2_off_feature2[['merchant_id', 'coupon_id', 'date_received', 'date']])
    # t11 = t11[(t11['coupon_id'].notnull() == True) & (t11['date_received'].notnull()==True) & (t11['date'].notnull() == True)]
    # t11['merchant_avgDay'] = t11['date']-t11['date_received']
    # t11['coupon_id'] = 1
    # t11 = t11.groupby('merchant_id', sort=False).agg('sum').reset_index()
    # t11['merchant_avgDay'] = round(t11['merchant_avgDay']/t11['coupon_id'],4)
    # t11 = pd.DataFrame(t11[['merchant_id', 'merchant_avgDay']],columns=['merchant_id', 'merchant_avgDay'])
    #
    # # 商家被核销的消费券到用户的平均距离  merchant_avgDistance
    # t12 = pd.DataFrame(dataSet2_off_feature2[['merchant_id', 'coupon_id', 'distance','date']])
    # t12 = t12[(t12['coupon_id'].notnull() == True) & (t12['date'].notnull() == True)][['merchant_id','distance']]
    # t12 = t12.fillna(-1)
    # t12['distance'] = t12['distance'].astype('int')
    # t12 = t12.groupby('merchant_id').agg('mean').reset_index()
    # t12.rename(columns={'distance': 'merchant_avgDistance'}, inplace=True)
    #
    # # 合并数据
    # left = dataSet2_off_feature2[['merchant_id']].drop_duplicates()
    # dataSet2_off_result = pd.merge(left,t,how='left',on=['merchant_id'])
    # dataSet2_off_result = pd.merge(dataSet2_off_result,t1,how='left',on=['merchant_id'])
    # dataSet2_off_result = pd.merge(dataSet2_off_result,t2,how='left',on=['merchant_id'])
    # dataSet2_off_result = pd.merge(dataSet2_off_result,t3,how='left',on=['merchant_id'])
    # dataSet2_off_result = pd.merge(dataSet2_off_result,t4,how='left',on=['merchant_id'])
    # dataSet2_off_result = pd.merge(dataSet2_off_result,t5,how='left',on=['merchant_id'])
    # dataSet2_off_result = pd.merge(dataSet2_off_result,t6,how='left',on=['merchant_id'])
    # dataSet2_off_result = pd.merge(dataSet2_off_result,t7,how='left',on=['merchant_id'])
    # dataSet2_off_result = pd.merge(dataSet2_off_result,t8,how='left',on=['merchant_id'])
    # dataSet2_off_result = pd.merge(dataSet2_off_result,t9,how='left',on=['merchant_id'])
    # dataSet2_off_result = pd.merge(dataSet2_off_result,t10,how='left',on=['merchant_id'])
    # dataSet2_off_result = pd.merge(dataSet2_off_result,t11,how='left',on=['merchant_id'])
    # dataSet2_off_result = pd.merge(dataSet2_off_result,t12,how='left',on=['merchant_id'])
    #
    # #填充Nan值
    # for i in dataSet2_off_result.columns:
    #     meanVal = dataSet2_off_result[i].mean()
    #     dataSet2_off_result[i].fillna(meanVal,inplace=True)
    #
    # # 商家优惠券的使用率  merchant_coupon_useRate (merchant_coupon_use/merchant_coupon_receive)
    # dataSet2_off_result['merchant_coupon_useRate'] = round(
    #                                                 dataSet2_off_result['merchant_coupon_use']/dataSet2_off_result['merchant_coupon_receive'],4)
    #
    # # 商家满减优惠券的核销率 merchant_manjian_useRate ( merchant_manjian_useCount/merchant_coupon_use)
    # dataSet2_off_result['merchant_manjian_useRate'] = round(
    #                                                 dataSet2_off_result['merchant_manjian_useCount'] / dataSet2_off_result['merchant_coupon_use'], 4)
    #
    # # 商家打折优惠券的核销率 merchant_zhijie_useRate (merchant_zhijie_useCount/merchant_coupon_use)
    # dataSet2_off_result['merchant_zhijie_useRate'] = round(
    #                                                 dataSet2_off_result['merchant_zhijie_useCount'] / dataSet2_off_result['merchant_coupon_use'], 4)
    #
    # dataSet2_off_result.to_csv('dataSet2_off_merchant_feature.csv', index=None)

    # dataSet1
    # 商家被消费的次数：merchant_buy_count
    # t = pd.DataFrame(dataSet1_off_feature1[['merchant_id','date']])
    # t = t[t['date'].notnull() == True]
    # t = pd.DataFrame(t['merchant_id'], columns=['merchant_id'])
    # t['merchant_buy_count'] = 1
    # t = t.groupby('merchant_id', sort=False).agg('sum').reset_index()
    #
    # # 商家优惠券被领取的次数 merchant_coupon_receive
    # t1 = pd.DataFrame(dataSet1_off_feature1[['merchant_id', 'coupon_id', 'date_received']])
    # t1 = t1[(t1['coupon_id'].notnull() == True) & (t1['date_received'].notnull()==True)]
    # t1 = pd.DataFrame(t1['merchant_id'], columns=['merchant_id'])
    # t1['merchant_coupon_receive'] = 1
    # t1 = t1.groupby('merchant_id', sort=False).agg('sum').reset_index()
    #
    # # 商家优惠券被使用的次数 merchant_coupon_use
    # t2 = pd.DataFrame(dataSet1_off_feature1[['merchant_id', 'coupon_id', 'date_received', 'date']])
    # t2 = t2[(t2['coupon_id'].notnull() == True) & (t2['date_received'].notnull()==True) & (t2['date'].notnull()==True)]
    # t2 = pd.DataFrame(t2['merchant_id'], columns=['merchant_id'])
    # t2['merchant_coupon_use'] = 1
    # t2 = t2.groupby('merchant_id', sort=False).agg('sum').reset_index()
    #
    # # 商家优惠券没有被使用的次数 merchant_coupon_notUse
    # t3 = pd.DataFrame(dataSet1_off_feature1[['merchant_id', 'coupon_id', 'date_received', 'date']])
    # t3 = t3[(t3['coupon_id'].notnull() == True) & (t3['date_received'].notnull() == True) & (t3['date'].notnull() == False)]
    # t3 = pd.DataFrame(t3['merchant_id'], columns=['merchant_id'])
    # t3['merchant_coupon_notUse'] = 1
    # t3 = t3.groupby('merchant_id', sort=False).agg('sum').reset_index()
    #
    # # 商家的消费券的类别的个数 merchant_coupon_kinds
    # t4 = pd.DataFrame(dataSet1_off_feature1[['merchant_id', 'coupon_id']])
    # t4 = t4[t4['coupon_id'].notnull() == True]
    # t4 = t4.drop_duplicates()
    # t4 = pd.DataFrame(t4['merchant_id'], columns=['merchant_id'])
    # t4['merchant_coupon_kinds'] = 1
    # t4 = t4.groupby('merchant_id', sort=False).agg('sum').reset_index()
    #
    # # 商家被核销的消费券类别个数 merchant_couponUse_kinds
    # t5 = pd.DataFrame(dataSet1_off_feature1[['merchant_id', 'coupon_id','date']])
    # t5 = t5[(t5['coupon_id'].notnull() == True) & (t5['date'].notnull()==True)]
    # t5 = t5[['merchant_id','coupon_id']]
    # t5 = t5.drop_duplicates()
    # t5 = pd.DataFrame(t5['merchant_id'], columns=['merchant_id'])
    # t5['merchant_couponUse_kinds'] = 1
    # t5 = t5.groupby('merchant_id', sort=False).agg('sum').reset_index()
    #
    # # 商家的消费券的平均折扣率 merchant_coupon_avgDiscount

    # t6 = pd.DataFrame(dataSet1_off_feature1[['merchant_id', 'coupon_id','discount_rate']])
    # t6 = t6[t6['coupon_id'].notnull() == True]
    # t6['coupon_id'] = int(1)
    # t6['discount_rate'] = t6['discount_rate'].apply(cal_discount)
    # t6 = t6.groupby('merchant_id', sort=False).agg('sum').reset_index()
    # t6['merchant_coupon_avgDiscount'] = t6['discount_rate']/t6['coupon_id']
    # t6 = pd.DataFrame(t6[['merchant_id','merchant_coupon_avgDiscount']],columns=['merchant_id','merchant_coupon_avgDiscount'])
    #
    # # 商家的满减消费券的所需要的平均价格 merchant_coupon_avgManjian
    # def is_manjian(s):
    #     s = str(s)
    #     s = s.split(':')
    #     if len(s) == 1:
    #         return int(0)
    #     else:
    #         return int(s[0])
    # t7 = pd.DataFrame(dataSet1_off_feature1[['merchant_id', 'coupon_id','discount_rate']])
    # t7['discount_rate'] = t7['discount_rate'].apply(is_manjian)
    # t7 = t7[(t7['coupon_id'].notnull() == True) & (t7['discount_rate']!=0)]
    # t7['coupon_id'] = int(1)
    # t7 = t7.groupby('merchant_id', sort=False).agg('sum').reset_index()
    # t7['merchant_coupon_avgManjian'] = round(t7['discount_rate'] / t7['coupon_id'],4)
    # t7 = pd.DataFrame(t7[['merchant_id', 'merchant_coupon_avgManjian']],columns=['merchant_id', 'merchant_coupon_avgManjian'])
    #
    # # 商家满减优惠券满减的平均金额 merchant_coupon_avgPrice
    # def manjian(s):
    #     s = str(s)
    #     s = s.split(':')
    #     if len(s) == 1:
    #         return int(0)
    #     else:
    #         return int(s[1])
    # t8 = pd.DataFrame(dataSet1_off_feature1[['merchant_id', 'coupon_id', 'discount_rate']])
    # t8['discount_rate'] = t8['discount_rate'].apply(manjian)
    # t8 = t8[(t8['coupon_id'].notnull() == True) & (t8['discount_rate'] != 0)]
    # t8['coupon_id'] = int(1)
    # t8 = t8.groupby('merchant_id', sort=False).agg('sum').reset_index()
    # t8['merchant_coupon_avgPrice'] = round(t8['discount_rate'] / t8['coupon_id'], 4)
    # t8 = pd.DataFrame(t8[['merchant_id', 'merchant_coupon_avgPrice']],columns=['merchant_id', 'merchant_coupon_avgPrice'])
    #
    # # 商家满减优惠券的使用次数 merchant_manjian_useCount
    def classify(s): # 直接优惠记为0，满减记为1
        s = str(s)
        s = s.split(':')
        if len(s) == 1:
            return 0
        else:
            return 1
    #
    #
    # t9 = pd.DataFrame(dataSet1_off_feature1[['merchant_id', 'coupon_id', 'discount_rate', 'date']])
    # t9['discount_rate'] = t9['discount_rate'].apply(classify)
    # # 满减优惠券使用次数
    # t9 = t9[(t9['coupon_id'].notnull() == True) & (t9['discount_rate'] == 1) & (t9['date'].notnull()==True)]
    # t9['merchant_manjian_useCount'] = 1
    # t9 = t9.groupby('merchant_id', sort=False).agg('sum').reset_index()
    # t9 = pd.DataFrame(t9[['merchant_id', 'merchant_manjian_useCount']],columns=['merchant_id', 'merchant_manjian_useCount'])
    #
    # # 直接优惠的优惠券使用次数 merchant_zhijie_useCount
    # t10 = pd.DataFrame(dataSet1_off_feature1[['merchant_id', 'coupon_id', 'discount_rate', 'date']])
    # t10['discount_rate'] = t10['discount_rate'].apply(classify)
    # t10 = t10[(t10['coupon_id'].notnull() == True) & (t10['discount_rate'] == 0) & (t10['date'].notnull() == True)]
    # t10['merchant_zhijie_useCount'] = 1
    # t10 = t10.groupby('merchant_id', sort=False).agg('sum').reset_index()
    # t10 = pd.DataFrame(t10[['merchant_id', 'merchant_zhijie_useCount']],columns=['merchant_id', 'merchant_zhijie_useCount'])
    #
    # # 商家的消费券从领取到消费经历的平均天数 merchant_avgDay
    # t11 = pd.DataFrame(dataSet1_off_feature1[['merchant_id', 'coupon_id', 'date_received', 'date']])
    # t11 = t11[(t11['coupon_id'].notnull() == True) & (t11['date_received'].notnull()==True) & (t11['date'].notnull() == True)]
    # t11['merchant_avgDay'] = t11['date']-t11['date_received']
    # t11['coupon_id'] = 1
    # t11 = t11.groupby('merchant_id', sort=False).agg('sum').reset_index()
    # t11['merchant_avgDay'] = round(t11['merchant_avgDay']/t11['coupon_id'],4)
    # t11 = pd.DataFrame(t11[['merchant_id', 'merchant_avgDay']],columns=['merchant_id', 'merchant_avgDay'])
    #
    # # 商家被核销的消费券到用户的平均距离  merchant_avgDistance
    # t12 = pd.DataFrame(dataSet1_off_feature1[['merchant_id', 'coupon_id', 'distance','date']])
    # t12 = t12[(t12['coupon_id'].notnull() == True) & (t12['date'].notnull() == True)][['merchant_id','distance']]
    # t12 = t12.fillna(-1)
    # t12['distance'] = t12['distance'].astype('int')
    # t12 = t12.groupby('merchant_id').agg('mean').reset_index()
    # t12.rename(columns={'distance': 'merchant_avgDistance'}, inplace=True)
    #
    # # 合并数据
    # left = dataSet1_off_feature1[['merchant_id']].drop_duplicates()
    # dataSet1_off_result = pd.merge(left,t,how='left',on=['merchant_id'])
    # dataSet1_off_result = pd.merge(dataSet1_off_result,t1,how='left',on=['merchant_id'])
    # dataSet1_off_result = pd.merge(dataSet1_off_result,t2,how='left',on=['merchant_id'])
    # dataSet1_off_result = pd.merge(dataSet1_off_result,t3,how='left',on=['merchant_id'])
    # dataSet1_off_result = pd.merge(dataSet1_off_result,t4,how='left',on=['merchant_id'])
    # dataSet1_off_result = pd.merge(dataSet1_off_result,t5,how='left',on=['merchant_id'])
    # dataSet1_off_result = pd.merge(dataSet1_off_result,t6,how='left',on=['merchant_id'])
    # dataSet1_off_result = pd.merge(dataSet1_off_result,t7,how='left',on=['merchant_id'])
    # dataSet1_off_result = pd.merge(dataSet1_off_result,t8,how='left',on=['merchant_id'])
    # dataSet1_off_result = pd.merge(dataSet1_off_result,t9,how='left',on=['merchant_id'])
    # dataSet1_off_result = pd.merge(dataSet1_off_result,t10,how='left',on=['merchant_id'])
    # dataSet1_off_result = pd.merge(dataSet1_off_result,t11,how='left',on=['merchant_id'])
    # dataSet1_off_result = pd.merge(dataSet1_off_result,t12,how='left',on=['merchant_id'])
    #
    # #填充Nan值
    # for i in dataSet1_off_result.columns:
    #     meanVal = dataSet1_off_result[i].mean()
    #     dataSet1_off_result[i].fillna(meanVal,inplace=True)
    #
    # # 商家优惠券的使用率  merchant_coupon_useRate (merchant_coupon_use/merchant_coupon_receive)
    # dataSet1_off_result['merchant_coupon_useRate'] = round(
    #                                                 dataSet1_off_result['merchant_coupon_use']/dataSet1_off_result['merchant_coupon_receive'],4)
    #
    # # 商家满减优惠券的核销率 merchant_manjian_useRate ( merchant_manjian_useCount/merchant_coupon_use)
    # dataSet1_off_result['merchant_manjian_useRate'] = round(
    #                                                 dataSet1_off_result['merchant_manjian_useCount'] / dataSet1_off_result['merchant_coupon_use'], 4)
    #
    # # 商家打折优惠券的核销率 merchant_zhijie_useRate (merchant_zhijie_useCount/merchant_coupon_use)
    # dataSet1_off_result['merchant_zhijie_useRate'] = round(
    #                                                 dataSet1_off_result['merchant_zhijie_useCount'] / dataSet1_off_result['merchant_coupon_use'], 4)
    #
    # dataSet1_off_result.to_csv('dataSet1_off_merchant_feature.csv', index=None)


    """
    优惠券特征：
        消费券的类型 coupon_kind   直接优惠记为0，满减记为1
        消费券的打折力度  coupon_discount
        消费券被用户领取的次数 coupon_receive_byUser
        消费券被用户消费的次数 coupon_use_byUser
        消费券被用户领取到消费经历的平均天数 coupon_avgDay
        消费券拥有的商家数 coupon_merchant_count
        消费券15天内被使用的占比 coupon_day_rate
        消费券被领取一般是周末还是工作日 coupon_receive_isweek
        消费券被消费一般是周末还是工作日 coupon_used_isweek
    """
    # for dataSet3

    # 消费券的类型 coupon_kind
    # t = pd.DataFrame(dataSet3_off_feature3[['coupon_id', 'discount_rate']])
    # t = t[t['discount_rate'].notnull() == True]
    # t['discount_rate'] = t['discount_rate'].apply(classify)
    # t = t.drop_duplicates()
    # t.rename(columns={'discount_rate': 'coupon_kind '}, inplace=True)
    #
    # # 消费券的打折力度  coupon_discount
    # t1 = pd.DataFrame(dataSet3_off_feature3[['coupon_id', 'discount_rate']])
    # t1 = t1[t1['discount_rate'].notnull() == True]
    # t1['discount_rate'] = t1['discount_rate'].apply(cal_discount)
    # t1 = t1.drop_duplicates()
    # t1.rename(columns={'discount_rate': 'coupon_discount '}, inplace=True)
    #
    # # 消费券被用户领取的次数 coupon_receive_byUser
    # t2 = pd.DataFrame(dataSet3_off_feature3[['coupon_id', 'date_received']])
    # t2 = t2[(t2['coupon_id'].notnull()==True) & (t2['date_received'].notnull() == True)]
    # t2['date_received'] = 1
    # t2 = t2.groupby('coupon_id').agg('sum').reset_index()
    # t2.rename(columns={'date_received': 'coupon_receive_byUser'}, inplace=True)
    #
    # # 消费券被用户消费的次数 coupon_use_byUser
    # t3 = pd.DataFrame(dataSet3_off_feature3[['coupon_id', 'date_received','date']])
    # t3 = t3[(t3['coupon_id'].notnull() == True) & (t3['date_received'].notnull() == True) & (t3['date'].notnull() == True)]
    # t3['date_received'] = 1
    # t3 = t3.groupby('coupon_id').agg('sum').reset_index()
    # t3 = pd.DataFrame(t3[['coupon_id','date_received']],columns=['coupon_id','date_received'])
    # t3.rename(columns={'date_received': 'coupon_use_byUser'}, inplace=True)
    #
    # # 消费券被用户领取到消费经历的平均天数 coupon_avgDay
    # t4 = pd.DataFrame(dataSet3_off_feature3[['coupon_id','date_received','date']])
    # t4 = t4[(t4['coupon_id'].notnull() == True) & (t4['date_received'].notnull() == True) & (t4['date'].notnull() == True)]
    # t4['coupon_avgDay'] = t4['date'] - t4['date_received']
    # t4 = t4.groupby('coupon_id',sort=False).agg('mean').reset_index()
    # t4 = pd.DataFrame(t4[['coupon_id','coupon_avgDay']],columns=['coupon_id','coupon_angDay'])
    #
    # # 消费券拥有的商家数 coupon_merchant_count
    # t5 = pd.DataFrame(dataSet3_off_feature3[['coupon_id', 'merchant_id']])
    # t5 = t5[t5['coupon_id'].notnull() == True].drop_duplicates()[['coupon_id']]
    # t5['coupon_merchant_count'] = 1
    # t5 = t5.groupby('coupon_id', sort=False).agg('sum').reset_index()
    #
    # # 消费券15天内被使用的占比 coupon_day_rate
    # t6 = pd.DataFrame(dataSet3_off_feature3[['coupon_id', 'date_received','date']])
    # t6 = t6[(t6['coupon_id'].notnull() == True) & (t6['date'].notnull() == True) & (t6['date_received'].notnull() == True)]
    # t6['spend_day'] = t6['date'] - t6['date_received']
    # t6_1 = t6[t6['spend_day']<15.0][['coupon_id','spend_day']]
    # t6_1['spend_day'] = 1
    # t6_1 = t6_1.groupby('coupon_id',sort=False).agg('sum').reset_index()
    # t6_1.rename(columns={'spend_day': 'daymin'}, inplace=True)
    # t6_2 = pd.DataFrame(t6[['coupon_id','spend_day']],columns=['coupon_id','spend_day'])
    # t6_2['spend_day'] = 1
    # t6_2 = t6_2.groupby('coupon_id',sort=False).agg('sum').reset_index()
    # t6_2.rename(columns={'spend_day': 'total_day'}, inplace=True)
    # t6 = pd.merge(t6_1,t6_2,how='left',on=['coupon_id'])
    # t6['coupon_day_rate'] = round(t6['daymin']/t6['total_day'],4)
    # t6 = pd.DataFrame(t6[['coupon_id','coupon_day_rate']],columns=['coupon_id','coupon_day_rate'])
    #
    # # 消费券被领取一般是周末还是工作日 coupon_receive_isweek
    # def isweek(s):
    #     s = str(s)
    #     week = datetime.strptime(s,'%Y%m%d').weekday()+1
    #     if week==5 or week==6 or week==7:
    #         return 1
    #     else:
    #         return 0
    #
    # t7 = pd.DataFrame(dataSet3_off_feature3[['coupon_id', 'date_received']])
    # t7 = t7[(t7['coupon_id'].notnull() == True) & (t7['date_received'].notnull() == True)]
    # t7['coupon_receive_isweek'] = t7['date_received'].apply(int).apply(isweek)
    # t7 = pd.DataFrame(t7[['coupon_id', 'coupon_receive_isweek']], columns=['coupon_id', 'coupon_receive_isweek']).drop_duplicates()
    #
    # # 消费券被消费一般是周末还是工作日 coupon_used_isweek
    # t8 = pd.DataFrame(dataSet3_off_feature3[['coupon_id', 'date_received','date']])
    # t8 = t8[(t8['coupon_id'].notnull() == True) & (t8['date_received'].notnull() == True) & (t8['date'].notnull() == True)]
    # t8['coupon_used_isweek'] = t8['date'].apply(int).apply(isweek)
    # t8 = pd.DataFrame(t8[['coupon_id', 'coupon_used_isweek']],columns=['coupon_id', 'coupon_used_isweek']).drop_duplicates()
    #
    # # 合并数据
    # left = dataSet3_off_feature3[['coupon_id']].drop_duplicates()
    # dataSet3_off_coupon = pd.merge(left,t,how='left',on=['coupon_id'])
    # dataSet3_off_coupon = pd.merge(dataSet3_off_coupon,t1,how='left',on=['coupon_id'])
    # dataSet3_off_coupon = pd.merge(dataSet3_off_coupon,t2,how='left',on=['coupon_id'])
    # dataSet3_off_coupon = pd.merge(dataSet3_off_coupon,t3,how='left',on=['coupon_id'])
    # dataSet3_off_coupon = pd.merge(dataSet3_off_coupon,t4,how='left',on=['coupon_id'])
    # dataSet3_off_coupon = pd.merge(dataSet3_off_coupon,t5,how='left',on=['coupon_id'])
    # dataSet3_off_coupon = pd.merge(dataSet3_off_coupon,t6,how='left',on=['coupon_id'])
    # dataSet3_off_coupon = pd.merge(dataSet3_off_coupon,t7,how='left',on=['coupon_id'])
    # dataSet3_off_coupon = pd.merge(dataSet3_off_coupon,t8,how='left',on=['coupon_id'])
    # # 消费券被用户的核销率 coupon_useRate
    # dataSet3_off_coupon['coupon_useRate'] = round(dataSet3_off_coupon['coupon_use_byUser']/dataSet3_off_coupon['coupon_receive_byUser'],4)
    # dataSet3_off_coupon.to_csv('dataSet3_off_coupon_feature.csv', index=None)
    #
    # # dataSet2
    # # 消费券的类型 coupon_kind
    # t = pd.DataFrame(dataSet2_off_feature2[['coupon_id', 'discount_rate']])
    # t = t[t['discount_rate'].notnull() == True]
    # t['discount_rate'] = t['discount_rate'].apply(classify)
    # t = t.drop_duplicates()
    # t.rename(columns={'discount_rate': 'coupon_kind '}, inplace=True)
    #
    # # 消费券的打折力度  coupon_discount
    # t1 = pd.DataFrame(dataSet2_off_feature2[['coupon_id', 'discount_rate']])
    # t1 = t1[t1['discount_rate'].notnull() == True]
    # t1['discount_rate'] = t1['discount_rate'].apply(cal_discount)
    # t1 = t1.drop_duplicates()
    # t1.rename(columns={'discount_rate': 'coupon_discount '}, inplace=True)
    #
    # # 消费券被用户领取的次数 coupon_receive_byUser
    # t2 = pd.DataFrame(dataSet2_off_feature2[['coupon_id', 'date_received']])
    # t2 = t2[(t2['coupon_id'].notnull() == True) & (t2['date_received'].notnull() == True)]
    # t2['date_received'] = 1
    # t2 = t2.groupby('coupon_id').agg('sum').reset_index()
    # t2.rename(columns={'date_received': 'coupon_receive_byUser'}, inplace=True)
    #
    # # 消费券被用户消费的次数 coupon_use_byUser
    # t3 = pd.DataFrame(dataSet2_off_feature2[['coupon_id', 'date_received', 'date']])
    # t3 = t3[
    #     (t3['coupon_id'].notnull() == True) & (t3['date_received'].notnull() == True) & (t3['date'].notnull() == True)]
    # t3['date_received'] = 1
    # t3 = t3.groupby('coupon_id').agg('sum').reset_index()
    # t3 = pd.DataFrame(t3[['coupon_id', 'date_received']], columns=['coupon_id', 'date_received'])
    # t3.rename(columns={'date_received': 'coupon_use_byUser'}, inplace=True)
    #
    # # 消费券被用户领取到消费经历的平均天数 coupon_avgDay
    # t4 = pd.DataFrame(dataSet2_off_feature2[['coupon_id', 'date_received', 'date']])
    # t4 = t4[
    #     (t4['coupon_id'].notnull() == True) & (t4['date_received'].notnull() == True) & (t4['date'].notnull() == True)]
    # t4['coupon_avgDay'] = t4['date'] - t4['date_received']
    # t4 = t4.groupby('coupon_id', sort=False).agg('mean').reset_index()
    # t4 = pd.DataFrame(t4[['coupon_id', 'coupon_avgDay']], columns=['coupon_id', 'coupon_angDay'])
    #
    # # 消费券拥有的商家数 coupon_merchant_count
    # t5 = pd.DataFrame(dataSet2_off_feature2[['coupon_id', 'merchant_id']])
    # t5 = t5[t5['coupon_id'].notnull() == True].drop_duplicates()[['coupon_id']]
    # t5['coupon_merchant_count'] = 1
    # t5 = t5.groupby('coupon_id', sort=False).agg('sum').reset_index()
    #
    # # 消费券15天内被使用的占比 coupon_day_rate
    # t6 = pd.DataFrame(dataSet2_off_feature2[['coupon_id', 'date_received', 'date']])
    # t6 = t6[
    #     (t6['coupon_id'].notnull() == True) & (t6['date'].notnull() == True) & (t6['date_received'].notnull() == True)]
    # t6['spend_day'] = t6['date'] - t6['date_received']
    # t6_1 = t6[t6['spend_day'] < 15.0][['coupon_id', 'spend_day']]
    # t6_1['spend_day'] = 1
    # t6_1 = t6_1.groupby('coupon_id', sort=False).agg('sum').reset_index()
    # t6_1.rename(columns={'spend_day': 'daymin'}, inplace=True)
    # t6_2 = pd.DataFrame(t6[['coupon_id', 'spend_day']], columns=['coupon_id', 'spend_day'])
    # t6_2['spend_day'] = 1
    # t6_2 = t6_2.groupby('coupon_id', sort=False).agg('sum').reset_index()
    # t6_2.rename(columns={'spend_day': 'total_day'}, inplace=True)
    # t6 = pd.merge(t6_1, t6_2, how='left', on=['coupon_id'])
    # t6['coupon_day_rate'] = round(t6['daymin'] / t6['total_day'], 4)
    # t6 = pd.DataFrame(t6[['coupon_id', 'coupon_day_rate']], columns=['coupon_id', 'coupon_day_rate'])
    #
    #
    # # 消费券被领取一般是周末还是工作日 coupon_receive_isweek
    # def isweek(s):
    #     s = str(s)
    #     week = datetime.strptime(s, '%Y%m%d').weekday() + 1
    #     if week == 5 or week == 6 or week == 7:
    #         return 1
    #     else:
    #         return 0
    #
    #
    # t7 = pd.DataFrame(dataSet2_off_feature2[['coupon_id', 'date_received']])
    # t7 = t7[(t7['coupon_id'].notnull() == True) & (t7['date_received'].notnull() == True)]
    # t7['coupon_receive_isweek'] = t7['date_received'].apply(int).apply(isweek)
    # t7 = pd.DataFrame(t7[['coupon_id', 'coupon_receive_isweek']],
    #                   columns=['coupon_id', 'coupon_receive_isweek']).drop_duplicates()
    #
    # # 消费券被消费一般是周末还是工作日 coupon_used_isweek
    # t8 = pd.DataFrame(dataSet2_off_feature2[['coupon_id', 'date_received', 'date']])
    # t8 = t8[
    #     (t8['coupon_id'].notnull() == True) & (t8['date_received'].notnull() == True) & (t8['date'].notnull() == True)]
    # t8['coupon_used_isweek'] = t8['date'].apply(int).apply(isweek)
    # t8 = pd.DataFrame(t8[['coupon_id', 'coupon_used_isweek']],
    #                   columns=['coupon_id', 'coupon_used_isweek']).drop_duplicates()
    #
    # # 合并数据
    # left = dataSet2_off_feature2[['coupon_id']].drop_duplicates()
    # dataSet2_off_coupon = pd.merge(left, t, how='left', on=['coupon_id'])
    # dataSet2_off_coupon = pd.merge(dataSet2_off_coupon, t1, how='left', on=['coupon_id'])
    # dataSet2_off_coupon = pd.merge(dataSet2_off_coupon, t2, how='left', on=['coupon_id'])
    # dataSet2_off_coupon = pd.merge(dataSet2_off_coupon, t3, how='left', on=['coupon_id'])
    # dataSet2_off_coupon = pd.merge(dataSet2_off_coupon, t4, how='left', on=['coupon_id'])
    # dataSet2_off_coupon = pd.merge(dataSet2_off_coupon, t5, how='left', on=['coupon_id'])
    # dataSet2_off_coupon = pd.merge(dataSet2_off_coupon, t6, how='left', on=['coupon_id'])
    # dataSet2_off_coupon = pd.merge(dataSet2_off_coupon, t7, how='left', on=['coupon_id'])
    # dataSet2_off_coupon = pd.merge(dataSet2_off_coupon, t8, how='left', on=['coupon_id'])
    # # 消费券被用户的核销率 coupon_useRate
    # dataSet2_off_coupon['coupon_useRate'] = round(
    #     dataSet2_off_coupon['coupon_use_byUser'] / dataSet2_off_coupon['coupon_receive_byUser'], 4)
    # dataSet2_off_coupon.to_csv('dataSet2_off_coupon_feature.csv', index=None)
    #
    #
    # # dataSet1
    # # 消费券的类型 coupon_kind
    # t = pd.DataFrame(dataSet1_off_feature1[['coupon_id', 'discount_rate']])
    # t = t[t['discount_rate'].notnull() == True]
    # t['discount_rate'] = t['discount_rate'].apply(classify)
    # t = t.drop_duplicates()
    # t.rename(columns={'discount_rate': 'coupon_kind '}, inplace=True)
    #
    # # 消费券的打折力度  coupon_discount
    # t1 = pd.DataFrame(dataSet1_off_feature1[['coupon_id', 'discount_rate']])
    # t1 = t1[t1['discount_rate'].notnull() == True]
    # t1['discount_rate'] = t1['discount_rate'].apply(cal_discount)
    # t1 = t1.drop_duplicates()
    # t1.rename(columns={'discount_rate': 'coupon_discount '}, inplace=True)
    #
    # # 消费券被用户领取的次数 coupon_receive_byUser
    # t2 = pd.DataFrame(dataSet1_off_feature1[['coupon_id', 'date_received']])
    # t2 = t2[(t2['coupon_id'].notnull() == True) & (t2['date_received'].notnull() == True)]
    # t2['date_received'] = 1
    # t2 = t2.groupby('coupon_id').agg('sum').reset_index()
    # t2.rename(columns={'date_received': 'coupon_receive_byUser'}, inplace=True)
    #
    # # 消费券被用户消费的次数 coupon_use_byUser
    # t3 = pd.DataFrame(dataSet1_off_feature1[['coupon_id', 'date_received', 'date']])
    # t3 = t3[
    #     (t3['coupon_id'].notnull() == True) & (t3['date_received'].notnull() == True) & (t3['date'].notnull() == True)]
    # t3['date_received'] = 1
    # t3 = t3.groupby('coupon_id').agg('sum').reset_index()
    # t3 = pd.DataFrame(t3[['coupon_id', 'date_received']], columns=['coupon_id', 'date_received'])
    # t3.rename(columns={'date_received': 'coupon_use_byUser'}, inplace=True)
    #
    # # 消费券被用户领取到消费经历的平均天数 coupon_avgDay
    # t4 = pd.DataFrame(dataSet1_off_feature1[['coupon_id', 'date_received', 'date']])
    # t4 = t4[
    #     (t4['coupon_id'].notnull() == True) & (t4['date_received'].notnull() == True) & (t4['date'].notnull() == True)]
    # t4['coupon_avgDay'] = t4['date'] - t4['date_received']
    # t4 = t4.groupby('coupon_id', sort=False).agg('mean').reset_index()
    # t4 = pd.DataFrame(t4[['coupon_id', 'coupon_avgDay']], columns=['coupon_id', 'coupon_angDay'])
    #
    # # 消费券拥有的商家数 coupon_merchant_count
    # t5 = pd.DataFrame(dataSet1_off_feature1[['coupon_id', 'merchant_id']])
    # t5 = t5[t5['coupon_id'].notnull() == True].drop_duplicates()[['coupon_id']]
    # t5['coupon_merchant_count'] = 1
    # t5 = t5.groupby('coupon_id', sort=False).agg('sum').reset_index()
    #
    # # 消费券15天内被使用的占比 coupon_day_rate
    # t6 = pd.DataFrame(dataSet1_off_feature1[['coupon_id', 'date_received', 'date']])
    # t6 = t6[
    #     (t6['coupon_id'].notnull() == True) & (t6['date'].notnull() == True) & (t6['date_received'].notnull() == True)]
    # t6['spend_day'] = t6['date'] - t6['date_received']
    # t6_1 = t6[t6['spend_day'] < 15.0][['coupon_id', 'spend_day']]
    # t6_1['spend_day'] = 1
    # t6_1 = t6_1.groupby('coupon_id', sort=False).agg('sum').reset_index()
    # t6_1.rename(columns={'spend_day': 'daymin'}, inplace=True)
    # t6_2 = pd.DataFrame(t6[['coupon_id', 'spend_day']], columns=['coupon_id', 'spend_day'])
    # t6_2['spend_day'] = 1
    # t6_2 = t6_2.groupby('coupon_id', sort=False).agg('sum').reset_index()
    # t6_2.rename(columns={'spend_day': 'total_day'}, inplace=True)
    # t6 = pd.merge(t6_1, t6_2, how='left', on=['coupon_id'])
    # t6['coupon_day_rate'] = round(t6['daymin'] / t6['total_day'], 4)
    # t6 = pd.DataFrame(t6[['coupon_id', 'coupon_day_rate']], columns=['coupon_id', 'coupon_day_rate'])
    #
    #
    # # 消费券被领取一般是周末还是工作日 coupon_receive_isweek
    # def isweek(s):
    #     s = str(s)
    #     week = datetime.strptime(s, '%Y%m%d').weekday() + 1
    #     if week == 5 or week == 6 or week == 7:
    #         return 1
    #     else:
    #         return 0
    #
    #
    # t7 = pd.DataFrame(dataSet1_off_feature1[['coupon_id', 'date_received']])
    # t7 = t7[(t7['coupon_id'].notnull() == True) & (t7['date_received'].notnull() == True)]
    # t7['coupon_receive_isweek'] = t7['date_received'].apply(int).apply(isweek)
    # t7 = pd.DataFrame(t7[['coupon_id', 'coupon_receive_isweek']],
    #                   columns=['coupon_id', 'coupon_receive_isweek']).drop_duplicates()
    #
    # # 消费券被消费一般是周末还是工作日 coupon_used_isweek
    # t8 = pd.DataFrame(dataSet1_off_feature1[['coupon_id', 'date_received', 'date']])
    # t8 = t8[
    #     (t8['coupon_id'].notnull() == True) & (t8['date_received'].notnull() == True) & (t8['date'].notnull() == True)]
    # t8['coupon_used_isweek'] = t8['date'].apply(int).apply(isweek)
    # t8 = pd.DataFrame(t8[['coupon_id', 'coupon_used_isweek']],
    #                   columns=['coupon_id', 'coupon_used_isweek']).drop_duplicates()
    #
    # # 合并数据
    # left = dataSet1_off_feature1[['coupon_id']].drop_duplicates()
    # dataSet1_off_coupon = pd.merge(left, t, how='left', on=['coupon_id'])
    # dataSet1_off_coupon = pd.merge(dataSet1_off_coupon, t1, how='left', on=['coupon_id'])
    # dataSet1_off_coupon = pd.merge(dataSet1_off_coupon, t2, how='left', on=['coupon_id'])
    # dataSet1_off_coupon = pd.merge(dataSet1_off_coupon, t3, how='left', on=['coupon_id'])
    # dataSet1_off_coupon = pd.merge(dataSet1_off_coupon, t4, how='left', on=['coupon_id'])
    # dataSet1_off_coupon = pd.merge(dataSet1_off_coupon, t5, how='left', on=['coupon_id'])
    # dataSet1_off_coupon = pd.merge(dataSet1_off_coupon, t6, how='left', on=['coupon_id'])
    # dataSet1_off_coupon = pd.merge(dataSet1_off_coupon, t7, how='left', on=['coupon_id'])
    # dataSet1_off_coupon = pd.merge(dataSet1_off_coupon, t8, how='left', on=['coupon_id'])
    # # 消费券被用户的核销率 coupon_useRate
    # dataSet1_off_coupon['coupon_useRate'] = round(
    #     dataSet1_off_coupon['coupon_use_byUser'] / dataSet1_off_coupon['coupon_receive_byUser'], 4)
    # dataSet1_off_coupon.to_csv('dataSet1_off_coupon_feature.csv', index=None)














