import pandas as pd
if __name__ == '__main__':
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
    t = pd.DataFrame(dataSet3_on_feature3[['user_id','date']])
    t = t[t['date'].notnull() == True]
    t = pd.DataFrame(t['user_id'],columns=['user_id'])
    t['user_online_buy_total'] = 1
    t = t.groupby('user_id',sort=False).agg('sum').reset_index()

    # 每个用户使用消费券消费的次数use_online_buy_coupon
    t1 = pd.DataFrame(dataSet3_on_feature3[['user_id','action','coupon_id']])
    t1 = t1[(t1['action'] == 1)&(t1['coupon_id'].notnull()==True)&(t1['coupon_id']!='fixed')]
    t1 = pd.DataFrame(t1['user_id'], columns=['user_id'])
    t1['use_online_buy_coupon'] = 1
    t1 = t1.groupby('user_id', sort=False).agg('sum').reset_index()

    # 每个用户领取的消费券的总数user_online_coupon_receivedAll
    t2 = pd.DataFrame(dataSet3_on_feature3[['user_id', 'action', 'coupon_id']])
    t2 = t2[(t2['action'] == 2) & (t2['coupon_id'].notnull() == True) & (t2['coupon_id'] != 'fixed')]
    t2 = pd.DataFrame(t2['user_id'], columns=['user_id'])
    t2['user_online_coupon_receivedAll'] = 1
    t2 = t2.groupby('user_id', sort=False).agg('sum').reset_index()

    # 每个用户在限时低价时消费的次数user_online_buy_fixed
    t3 = pd.DataFrame(dataSet3_on_feature3[['user_id', 'action', 'coupon_id']])
    t3 = t3[(t3['action'] == 1) & (t3['coupon_id'] == 'fixed')]
    t3 = pd.DataFrame(t3['user_id'], columns=['user_id'])
    t3['user_online_buy_fixed'] = 1
    t3 = t3.groupby('user_id', sort=False).agg('sum').reset_index()

    # 用户购买东西的商店的个数user_online_buy_merchantCount
    t4 = pd.DataFrame(dataSet3_on_feature3[['user_id', 'action', 'merchant_id']])
    t4 = t4[(t4['action'] == 1) & (t4['merchant_id'].notnull()==True)]
    t4 = pd.DataFrame(t4['user_id'], columns=['user_id'])
    t4['user_online_buy_merchantCount'] = 1
    t4 = t4.groupby('user_id', sort=False).agg('sum').reset_index()

    # 每个用户看过的商店的个数包括只点击user_online_action_merchantCount
    t5 = pd.DataFrame(dataSet3_on_feature3[['user_id','merchant_id']])
    t5 = t5[(t5['merchant_id'].notnull() == True)]
    t5 = pd.DataFrame(t5['user_id'], columns=['user_id'])
    t5['user_online_action_merchantCount'] = 1
    t5 = t5.groupby('user_id', sort=False).agg('sum').reset_index()

    # 每个用户行为的个数user_online_action_count
    t6 = pd.DataFrame(dataSet3_on_feature3[['user_id', 'action']])
    t6 = t6[(t6['action'].notnull() == True)]
    t6 = pd.DataFrame(t6['user_id'], columns=['user_id'])
    t6['user_online_action_count'] = 1
    t6 = t6.groupby('user_id', sort=False).agg('sum').reset_index()

    # 每个用户点击个数user_online_click_count
    t7 = pd.DataFrame(dataSet3_on_feature3[['user_id', 'action']])
    t7 = t7[(t7['action'].notnull() == True)&(t7['action']==0)]
    t7 = pd.DataFrame(t7['user_id'], columns=['user_id'])
    t7['user_online_click_count'] = 1
    t7 = t7.groupby('user_id', sort=False).agg('sum').reset_index()

    # 每个用户领取了优惠券没有使用的次数user_online_notUseReceive_coupon
    t8 = pd.DataFrame(dataSet3_on_feature3[['user_id', 'action','date']])
    t8 = t8[(t8['action'].notnull() == True) & (t8['action'] == 2)&(t8['date'].isnull()==True)]
    t8 = pd.DataFrame(t8['user_id'], columns=['user_id'])
    t8['user_online_notUseReceive_coupon'] = 1
    t8 = t8.groupby('user_id', sort=False).agg('sum').reset_index()

    # 每个用户没有使用消费券消费的次数user_online_notUse_coupon
    t9 = pd.DataFrame(dataSet3_on_feature3[['user_id', 'coupon_id', 'date']])
    t9 = t9[(t9['date'].notnull() == True) & (t9['coupon_id'].isnull() == True)]
    t9 = pd.DataFrame(t9['user_id'], columns=['user_id'])
    t9['user_online_notUse_coupon'] = 1
    t9 = t9.groupby('user_id', sort=False).agg('sum').reset_index()

    #合并数据
    left = dataSet3_on_feature3[['user_id']].drop_duplicates()
    dataSet3_on_result = pd.merge(left,t,how='left',on=['user_id'])
    dataSet3_on_result = pd.merge(dataSet3_on_result,t1,how='left',on='user_id')
    dataSet3_on_result = pd.merge(dataSet3_on_result,t2,how='left',on='user_id')
    dataSet3_on_result = pd.merge(dataSet3_on_result,t3,how='left',on='user_id')
    dataSet3_on_result = pd.merge(dataSet3_on_result,t4,how='left',on='user_id')
    dataSet3_on_result = pd.merge(dataSet3_on_result,t5,how='left',on='user_id')
    dataSet3_on_result = pd.merge(dataSet3_on_result,t6,how='left',on='user_id')
    dataSet3_on_result = pd.merge(dataSet3_on_result,t7,how='left',on='user_id')
    dataSet3_on_result = pd.merge(dataSet3_on_result,t8,how='left',on='user_id')
    dataSet3_on_result = pd.merge(dataSet3_on_result,t9,how='left',on='user_id')

    #替换每列中的Nan,用平均值来代替
    for i in dataSet3_on_result.columns:
        meanVal = dataSet3_on_result[i].mean()
        dataSet3_on_result[i].fillna(meanVal,inplace=True)

    # 使用消费券消费的次数占总消费次数的占比 user_online_buy_couponRate (use_online_buy_coupon/user_online_buy_total)
    t10 = dataSet3_on_result['use_online_buy_coupon']
    t_10 = dataSet3_on_result['user_online_buy_total']
    t10 = t10/t_10
    dataSet3_on_result['user_online_buy_couponRate'] = t10

    # 用户使用消费券占领取的消费券的比重  uses_online_coupon_buyRate (use_online_buy_coupon/user_online_coupon_receivedAll)
    t11 = dataSet3_on_result['use_online_buy_coupon']
    t_11 = dataSet3_on_result['user_online_coupon_receivedAll']
    t11 = t11/t_11
    dataSet3_on_result['uses_online_coupon_buyRate'] = t11

    # 每个用户限时低价消费占总消费的比重 user_online_buy_fixedRate (user_online_buy_fixed/user_online_buy_total)
    t12 = dataSet3_on_result['user_online_buy_fixed']
    t_12 = dataSet3_on_result['user_online_buy_total']
    t12 = t12/t_12
    dataSet3_on_result['user_online_buy_fixedRate'] = t12

    # 消费的商店占有过行为的商店的比重 user_online_merchantBuyRate (user_online_buy_merchantCount/user_online_action_merchantCount)
    t13 = dataSet3_on_result['user_online_buy_merchantCount']
    t_13 = dataSet3_on_result['user_online_action_merchantCount']
    t13 = t13/t_13
    dataSet3_on_result['user_online_merchantBuyRate'] = t13

    dataSet3_on_result.to_csv('dataSet3_on_feature.csv', index=None)

    # 对dataSet2_on_feature2

    # 每个用户消费的总次数user_online_buy_total
    t = pd.DataFrame(dataSet2_on_feature2[['user_id','date']])
    t = t[t['date'].notnull() == True]
    t = pd.DataFrame(t['user_id'],columns=['user_id'])
    t['user_online_buy_total'] = 1
    t = t.groupby('user_id',sort=False).agg('sum').reset_index()

    # 每个用户使用消费券消费的次数use_online_buy_coupon
    t1 = pd.DataFrame(dataSet2_on_feature2[['user_id','action','coupon_id']])
    t1 = t1[(t1['action'] == 1)&(t1['coupon_id'].notnull()==True)&(t1['coupon_id']!='fixed')]
    t1 = pd.DataFrame(t1['user_id'], columns=['user_id'])
    t1['use_online_buy_coupon'] = 1
    t1 = t1.groupby('user_id', sort=False).agg('sum').reset_index()

    # 每个用户领取的消费券的总数user_online_coupon_receivedAll
    t2 = pd.DataFrame(dataSet2_on_feature2[['user_id', 'action', 'coupon_id']])
    t2 = t2[(t2['action'] == 2) & (t2['coupon_id'].notnull() == True) & (t2['coupon_id'] != 'fixed')]
    t2 = pd.DataFrame(t2['user_id'], columns=['user_id'])
    t2['user_online_coupon_receivedAll'] = 1
    t2 = t2.groupby('user_id', sort=False).agg('sum').reset_index()

    # 每个用户在限时低价时消费的次数user_online_buy_fixed
    t3 = pd.DataFrame(dataSet2_on_feature2[['user_id', 'action', 'coupon_id']])
    t3 = t3[(t3['action'] == 1) & (t3['coupon_id'] == 'fixed')]
    t3 = pd.DataFrame(t3['user_id'], columns=['user_id'])
    t3['user_online_buy_fixed'] = 1
    t3 = t3.groupby('user_id', sort=False).agg('sum').reset_index()

    # 用户购买东西的商店的个数user_online_buy_merchantCount
    t4 = pd.DataFrame(dataSet2_on_feature2[['user_id', 'action', 'merchant_id']])
    t4 = t4[(t4['action'] == 1) & (t4['merchant_id'].notnull()==True)]
    t4 = pd.DataFrame(t4['user_id'], columns=['user_id'])
    t4['user_online_buy_merchantCount'] = 1
    t4 = t4.groupby('user_id', sort=False).agg('sum').reset_index()

    # 每个用户看过的商店的个数包括只点击user_online_action_merchantCount
    t5 = pd.DataFrame(dataSet2_on_feature2[['user_id','merchant_id']])
    t5 = t5[(t5['merchant_id'].notnull() == True)]
    t5 = pd.DataFrame(t5['user_id'], columns=['user_id'])
    t5['user_online_action_merchantCount'] = 1
    t5 = t5.groupby('user_id', sort=False).agg('sum').reset_index()

    # 每个用户行为的个数user_online_action_count
    t6 = pd.DataFrame(dataSet2_on_feature2[['user_id', 'action']])
    t6 = t6[(t6['action'].notnull() == True)]
    t6 = pd.DataFrame(t6['user_id'], columns=['user_id'])
    t6['user_online_action_count'] = 1
    t6 = t6.groupby('user_id', sort=False).agg('sum').reset_index()

    # 每个用户点击个数user_online_click_count
    t7 = pd.DataFrame(dataSet2_on_feature2[['user_id', 'action']])
    t7 = t7[(t7['action'].notnull() == True)&(t7['action']==0)]
    t7 = pd.DataFrame(t7['user_id'], columns=['user_id'])
    t7['user_online_click_count'] = 1
    t7 = t7.groupby('user_id', sort=False).agg('sum').reset_index()

    # 每个用户领取了优惠券没有使用的次数user_online_notUseReceive_coupon
    t8 = pd.DataFrame(dataSet2_on_feature2[['user_id', 'action','date']])
    t8 = t8[(t8['action'].notnull() == True) & (t8['action'] == 2)&(t8['date'].isnull()==True)]
    t8 = pd.DataFrame(t8['user_id'], columns=['user_id'])
    t8['user_online_notUseReceive_coupon'] = 1
    t8 = t8.groupby('user_id', sort=False).agg('sum').reset_index()

    # 每个用户没有使用消费券消费的次数user_online_notUse_coupon
    t9 = pd.DataFrame(dataSet2_on_feature2[['user_id', 'coupon_id', 'date']])
    t9 = t9[(t9['date'].notnull() == True) & (t9['coupon_id'].isnull() == True)]
    t9 = pd.DataFrame(t9['user_id'], columns=['user_id'])
    t9['user_online_notUse_coupon'] = 1
    t9 = t9.groupby('user_id', sort=False).agg('sum').reset_index()

    #合并数据
    left = dataSet2_on_feature2[['user_id']].drop_duplicates()
    data2_on_result = pd.merge(left,t,how='left',on=['user_id'])
    data2_on_result = pd.merge(data2_on_result,t1,how='left',on='user_id')
    data2_on_result = pd.merge(data2_on_result,t2,how='left',on='user_id')
    data2_on_result = pd.merge(data2_on_result,t3,how='left',on='user_id')
    data2_on_result = pd.merge(data2_on_result,t4,how='left',on='user_id')
    data2_on_result = pd.merge(data2_on_result,t5,how='left',on='user_id')
    data2_on_result = pd.merge(data2_on_result,t6,how='left',on='user_id')
    data2_on_result = pd.merge(data2_on_result,t7,how='left',on='user_id')
    data2_on_result = pd.merge(data2_on_result,t8,how='left',on='user_id')
    data2_on_result = pd.merge(data2_on_result,t9,how='left',on='user_id')

    #替换每列中的Nan,用平均值来代替
    for i in data2_on_result.columns:
        meanVal = data2_on_result[i].mean()
        data2_on_result[i].fillna(meanVal,inplace=True)

    # 使用消费券消费的次数占总消费次数的占比 user_online_buy_couponRate (use_online_buy_coupon/user_online_buy_total)
    t10 = data2_on_result['use_online_buy_coupon']
    t_10 = data2_on_result['user_online_buy_total']
    t10 = t10/t_10
    data2_on_result['user_online_buy_couponRate'] = t10

    # 用户使用消费券占领取的消费券的比重  uses_online_coupon_buyRate (use_online_buy_coupon/user_online_coupon_receivedAll)
    t11 = data2_on_result['use_online_buy_coupon']
    t_11 = data2_on_result['user_online_coupon_receivedAll']
    t11 = t11/t_11
    data2_on_result['uses_online_coupon_buyRate'] = t11

    # 每个用户限时低价消费占总消费的比重 user_online_buy_fixedRate (user_online_buy_fixed/user_online_buy_total)
    t12 = data2_on_result['user_online_buy_fixed']
    t_12 = data2_on_result['user_online_buy_total']
    t12 = t12/t_12
    data2_on_result['user_online_buy_fixedRate'] = t12

    # 消费的商店占有过行为的商店的比重 user_online_merchantBuyRate (user_online_buy_merchantCount/user_online_action_merchantCount)
    t13 = data2_on_result['user_online_buy_merchantCount']
    t_13 = data2_on_result['user_online_action_merchantCount']
    t13 = t13/t_13
    data2_on_result['user_online_merchantBuyRate'] = t13
    data2_on_result.to_csv('dataSet2_on_feature.csv', index=None)

    # dataSet1_on_feature
    # 每个用户消费的总次数user_online_buy_total
    t = pd.DataFrame(dataSet1_on_feature1[['user_id','date']])
    t = t[t['date'].notnull() == True]
    t = pd.DataFrame(t['user_id'],columns=['user_id'])
    t['user_online_buy_total'] = 1
    t = t.groupby('user_id',sort=False).agg('sum').reset_index()

    # 每个用户使用消费券消费的次数use_online_buy_coupon
    t1 = pd.DataFrame(dataSet1_on_feature1[['user_id','action','coupon_id']])
    t1 = t1[(t1['action'] == 1)&(t1['coupon_id'].notnull()==True)&(t1['coupon_id']!='fixed')]
    t1 = pd.DataFrame(t1['user_id'], columns=['user_id'])
    t1['use_online_buy_coupon'] = 1
    t1 = t1.groupby('user_id', sort=False).agg('sum').reset_index()

    # 每个用户领取的消费券的总数user_online_coupon_receivedAll
    t2 = pd.DataFrame(dataSet1_on_feature1[['user_id', 'action', 'coupon_id']])
    t2 = t2[(t2['action'] == 2) & (t2['coupon_id'].notnull() == True) & (t2['coupon_id'] != 'fixed')]
    t2 = pd.DataFrame(t2['user_id'], columns=['user_id'])
    t2['user_online_coupon_receivedAll'] = 1
    t2 = t2.groupby('user_id', sort=False).agg('sum').reset_index()

    # 每个用户在限时低价时消费的次数user_online_buy_fixed
    t3 = pd.DataFrame(dataSet1_on_feature1[['user_id', 'action', 'coupon_id']])
    t3 = t3[(t3['action'] == 1) & (t3['coupon_id'] == 'fixed')]
    t3 = pd.DataFrame(t3['user_id'], columns=['user_id'])
    t3['user_online_buy_fixed'] = 1
    t3 = t3.groupby('user_id', sort=False).agg('sum').reset_index()

    # 用户购买东西的商店的个数user_online_buy_merchantCount
    t4 = pd.DataFrame(dataSet1_on_feature1[['user_id', 'action', 'merchant_id']])
    t4 = t4[(t4['action'] == 1) & (t4['merchant_id'].notnull()==True)]
    t4 = pd.DataFrame(t4['user_id'], columns=['user_id'])
    t4['user_online_buy_merchantCount'] = 1
    t4 = t4.groupby('user_id', sort=False).agg('sum').reset_index()

    # 每个用户看过的商店的个数包括只点击user_online_action_merchantCount
    t5 = pd.DataFrame(dataSet1_on_feature1[['user_id','merchant_id']])
    t5 = t5[(t5['merchant_id'].notnull() == True)]
    t5 = pd.DataFrame(t5['user_id'], columns=['user_id'])
    t5['user_online_action_merchantCount'] = 1
    t5 = t5.groupby('user_id', sort=False).agg('sum').reset_index()

    # 每个用户行为的个数user_online_action_count
    t6 = pd.DataFrame(dataSet1_on_feature1[['user_id', 'action']])
    t6 = t6[(t6['action'].notnull() == True)]
    t6 = pd.DataFrame(t6['user_id'], columns=['user_id'])
    t6['user_online_action_count'] = 1
    t6 = t6.groupby('user_id', sort=False).agg('sum').reset_index()

    # 每个用户点击个数user_online_click_count
    t7 = pd.DataFrame(dataSet1_on_feature1[['user_id', 'action']])
    t7 = t7[(t7['action'].notnull() == True)&(t7['action']==0)]
    t7 = pd.DataFrame(t7['user_id'], columns=['user_id'])
    t7['user_online_click_count'] = 1
    t7 = t7.groupby('user_id', sort=False).agg('sum').reset_index()

    # 每个用户领取了优惠券没有使用的次数user_online_notUseReceive_coupon
    t8 = pd.DataFrame(dataSet1_on_feature1[['user_id', 'action','date']])
    t8 = t8[(t8['action'].notnull() == True) & (t8['action'] == 2)&(t8['date'].isnull()==True)]
    t8 = pd.DataFrame(t8['user_id'], columns=['user_id'])
    t8['user_online_notUseReceive_coupon'] = 1
    t8 = t8.groupby('user_id', sort=False).agg('sum').reset_index()

    # 每个用户没有使用消费券消费的次数user_online_notUse_coupon
    t9 = pd.DataFrame(dataSet1_on_feature1[['user_id', 'coupon_id', 'date']])
    t9 = t9[(t9['date'].notnull() == True) & (t9['coupon_id'].isnull() == True)]
    t9 = pd.DataFrame(t9['user_id'], columns=['user_id'])
    t9['user_online_notUse_coupon'] = 1
    t9 = t9.groupby('user_id', sort=False).agg('sum').reset_index()

    #合并数据
    left = dataSet1_on_feature1[['user_id']].drop_duplicates()
    dataSet1_on_result = pd.merge(left,t,how='left',on=['user_id'])
    dataSet1_on_result = pd.merge(dataSet1_on_result,t1,how='left',on='user_id')
    dataSet1_on_result = pd.merge(dataSet1_on_result,t2,how='left',on='user_id')
    dataSet1_on_result = pd.merge(dataSet1_on_result,t3,how='left',on='user_id')
    dataSet1_on_result = pd.merge(dataSet1_on_result,t4,how='left',on='user_id')
    dataSet1_on_result = pd.merge(dataSet1_on_result,t5,how='left',on='user_id')
    dataSet1_on_result = pd.merge(dataSet1_on_result,t6,how='left',on='user_id')
    dataSet1_on_result = pd.merge(dataSet1_on_result,t7,how='left',on='user_id')
    dataSet1_on_result = pd.merge(dataSet1_on_result,t8,how='left',on='user_id')
    dataSet1_on_result = pd.merge(dataSet1_on_result,t9,how='left',on='user_id')

    #替换每列中的Nan,用平均值来代替
    for i in dataSet1_on_result.columns:
        meanVal = dataSet1_on_result[i].mean()
        dataSet1_on_result[i].fillna(meanVal,inplace=True)

    # 使用消费券消费的次数占总消费次数的占比 user_online_buy_couponRate (use_online_buy_coupon/user_online_buy_total)
    t10 = dataSet1_on_result['use_online_buy_coupon']
    t_10 = dataSet1_on_result['user_online_buy_total']
    t10 = t10/t_10
    dataSet1_on_result['user_online_buy_couponRate'] = t10

    # 用户使用消费券占领取的消费券的比重  uses_online_coupon_buyRate (use_online_buy_coupon/user_online_coupon_receivedAll)
    t11 = dataSet1_on_result['use_online_buy_coupon']
    t_11 = dataSet1_on_result['user_online_coupon_receivedAll']
    t11 = t11/t_11
    dataSet1_on_result['uses_online_coupon_buyRate'] = t11

    # 每个用户限时低价消费占总消费的比重 user_online_buy_fixedRate (user_online_buy_fixed/user_online_buy_total)
    t12 = dataSet1_on_result['user_online_buy_fixed']
    t_12 = dataSet1_on_result['user_online_buy_total']
    t12 = t12/t_12
    dataSet1_on_result['user_online_buy_fixedRate'] = t12

    # 消费的商店占有过行为的商店的比重 user_online_merchantBuyRate (user_online_buy_merchantCount/user_online_action_merchantCount)
    t13 = dataSet1_on_result['user_online_buy_merchantCount']
    t_13 = dataSet1_on_result['user_online_action_merchantCount']
    t13 = t13/t_13
    dataSet1_on_result['user_online_merchantBuyRate'] = t13

    dataSet1_on_result.to_csv('dataSet1_on_feature.csv', index=None)











