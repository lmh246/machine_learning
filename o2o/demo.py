import pandas as pd
if __name__ == '__main__':
    off_train = pd.read_csv("./ccf_offline_stage1_train.csv")
    print("------------------------------针对线下的数据表------------------------------------")
    print("数据总量：",off_train.__len__())
    #print("领取了优惠券的记录：",off_train['Date_received'].dropna().__len__())
    print("优惠券的种类：",off_train['Coupon_id'].drop_duplicates().__len__())
    print("用户个数：",off_train['User_id'].drop_duplicates().__len__())
    print("商户个数：",off_train['Merchant_id'].drop_duplicates().__len__())

    print("------------------------------针对线上的数据表------------------------------------")
    onn_train = pd.read_csv('./ccf_online_stage1_train.csv')
    print("数据总量：",onn_train.__len__())
    print("用户个数：",onn_train['User_id'].drop_duplicates().__len__())
    off_user = off_train['User_id'].drop_duplicates()
    onn_user = onn_train['User_id'].drop_duplicates()
    numCount = 0
    for item in onn_user:
        if item in off_user:
            numCount = numCount + 1
    print("与线下用户重复的用户个数：",numCount)
    off_mer = off_train['Merchant_id'].drop_duplicates()
    onn_mer = onn_train['Merchant_id'].drop_duplicates()
    print("商户个数：",onn_mer.__len__())
    merCount = 0
    for item in onn_mer:
        if item in off_mer:
            merCount = merCount + 1
    print("与线下商户重复的商户个数：",merCount)

    print("------------------------------线下预测的数据表------------------------------------")
    off_test = pd.read_csv('./ccf_offline_stage1_test_revised.csv')
    print("数据总量：",off_test.__len__())
    test_user = off_test['User_id'].drop_duplicates()
    print("需要预测的用户的总量：",test_user.__len__())
    testUser = 0
    for item in test_user:
        if item in off_user:
            testUser = testUser + 1
    print("用户与线下用户重复的个数：",testUser)
    test_mer = off_test['Merchant_id'].drop_duplicates()
    print("预测样本中商户的个数：",test_mer.__len__())
    testmer = 0
    for item in test_mer:
        if item in off_mer:
            testmer = testmer + 1
    print("预测样本中商户与线下商户重复的个数：",testmer)

    test_con = off_test['Coupon_id'].drop_duplicates()
    train_con = off_train['Coupon_id'].drop_duplicates()
    print("预测的优惠券的数量：",test_con.__len__())
    conCount = 0
    for item in test_con:
        if item in train_con:
            conCount = conCount + 1
    print("预测样本中优惠券与线下中优惠券重复的个数：",conCount)

    date_test = off_test['Date_received'].drop_duplicates()
    print(date_test.sort_values())






