# -*- coding: utf-8 -*-
import time
from ctypes import cast, byref
from threading import Thread
from oes_api import OesApi
from oes_struct import *


def oes_set_get(oes):
    print(f"API的发行版本号:{oes.OesApi_GetApiVersion()}")
    oes.OesApi_SetThreadUsername('user')
    print(f"当前线程使用的登录用户名:{oes.OesApi_GetThreadUsername()}")
    oes.OesApi_SetThreadPassword('123')
    oes.OesApi_SetThreadEnvId(91)
    print(f"当前线程登录OES时使用的客户端环境号:{oes.OesApi_GetThreadEnvId()}")
    oes.OesApi_SetThreadSubscribeEnvId(90)
    print(f"当前线程订阅回报时待订阅的客户端环境号:{oes.OesApi_GetThreadSubscribeEnvId()}")
    oes.OesApi_SetThreadBusinessType(eOesBusinessTypeT.OES_BUSINESS_TYPE_STOCK.value)
    print(f"当前线程登录OES时所期望对接的业务类型:{oes.OesApi_GetThreadBusinessType()}")
    oes.OesApi_SetCustomizedIpAndMac('192.168.1.11', '45:38:56:89:78:5A')
    oes.OesApi_SetCustomizedIp('192.168.1.11')
    print(f"客户端自定义的本地IP:{oes.OesApi_GetCustomizedIp()}")
    oes.OesApi_SetCustomizedMac('45:38:56:89:78:5A')
    print(f"客户端自定义的本地MAC:{oes.OesApi_GetCustomizedMac()}")
    oes.OesApi_SetCustomizedDriverId("DF13SAH8JK907")
    print(f"客户端自定义的本地设备序列号:{oes.OesApi_GetCustomizedDriverId()}")
    print(f"通道对应的客户端编号:{oes.OesApi_GetClientId(oes.ord_channel)}")
    print(f"通道对应的客户端环境号:{oes.OesApi_GetClEnvId(oes.rpt_channel)}")
    print(f"通道对应的业务类型:{oes.OesApi_GetBusinessType(oes.qry_channel)}")
    print(f"系统是否支持指定的业务类别:"
          f"{oes.OesApi_IsBusinessSupported(oes.ord_channel, eOesBusinessTypeT.OES_BUSINESS_TYPE_STOCK.value)}")
    print(f"客户端类型:{oes.OesApi_GetClientType(oes.rpt_channel)}")
    print(f"客户端状态:{oes.OesApi_GetClientStatus(oes.qry_channel)}")
    print(f"通道最近接收消息时间:{oes.OesApi_GetLastRecvTime(oes.ord_channel)}")
    print(f"通道最近发送消息时间:{oes.OesApi_GetLastSendTime(oes.rpt_channel)}")
    print(f"报通道是否还有更多已接收但尚未回调处理完成的数据:{oes.OesApi_HasMoreCachedData()}")
    print(f"委托申报通道是否已经连接且有效:{oes.OesApi_IsValidOrdChannel()}")
    print(f"回报通道是否已经连接且有效:{oes.OesApi_IsValidRptChannel()}")
    print(f"查询通道是否已经连接且有效:{oes.OesApi_IsValidQryChannel()}")
    oes.OesApi_SetLastError(1026)
    print(f"当前线程最近一次API调用失败的错误号:{oes.OesApi_GetLastError()}")
    print(f"错误号对应的错误信息:{oes.OesApi_GetErrorMsg(1026)}")
    print()


def OnOesQuery(qry_channel, msg_head, msg_item, qry_cursor, callback_params):
    msg_id = msg_head.contents.msgId
    # print(msg_id)
    if msg_id == eOesMsgTypeT.OESMSG_QRYMSG_INV_ACCT.value:
        inv_acct = cast(msg_item, POINTER(OesInvAcctItemT))[0]
        print(f"股东账户代码:{inv_acct.invAcctId.decode()}, 市场:{inv_acct.mktId}, 账户类型:{inv_acct.acctType}, "
              f"账户状态:{inv_acct.status}, 客户代码:{inv_acct.custId.decode()}")
    elif msg_id == eOesMsgTypeT.OESMSG_QRYMSG_CASH_ASSET.value:
        cash_asset = cast(msg_item, POINTER(OesCashAssetItemT))[0]
        print(f"资金账户代码:{cash_asset.cashAcctId.decode()}, 客户代码:{cash_asset.custId.decode()}, "
              f"当前可用余额:{cash_asset.currentAvailableBal}, 当前可取余额:{cash_asset.currentDrawableBal}")
    elif msg_id == eOesMsgTypeT.OESMSG_QRYMSG_ORD.value:
        ord_item = cast(msg_item, POINTER(OesOrdItemT))[0]
        print(f"客户委托流水号:{ord_item.clSeqNo}, 证券代码:{ord_item.securityId.decode()}, "
              f"委托数量:{ord_item.ordQty}, 委托价格:{ord_item.ordPrice}, 委托时间:{ord_item.ordTime}, "
              f"委托确认时间:{ord_item.ordCnfmTime}, 订单当前状态:{ord_item.ordStatus}, "
              f"委托确认状态:{ord_item.ordCnfmSts}")
    elif msg_id == eOesMsgTypeT.OESMSG_QRYMSG_TRD.value:
        trd_item = cast(msg_item, POINTER(OesTrdItemT))[0]
        print(f"交易所成交编号:{trd_item.exchTrdNum}, 证券代码:{trd_item.securityId.decode()}, "
              f"成交时间:{trd_item.trdTime}, 成交数量:{trd_item.trdQty}, 成交价格:{trd_item.trdPrice}, "
              f"客户委托流水号:{trd_item.clSeqNo}, 订单当前状态:{trd_item.ordStatus}, "
              f"累计交易费用:{trd_item.cumFee}")
    elif msg_id == eOesMsgTypeT.OESMSG_QRYMSG_STK_HLD.value:
        stk_holding_item = cast(msg_item, POINTER(OesStkHoldingItemT))[0]
        print(f"账户代码:{stk_holding_item.invAcctId.decode()}, 证券代码:{stk_holding_item.securityId.decode()}, "
              f"日初持仓:{stk_holding_item.originalHld}, 当前可卖持仓:{stk_holding_item.sellAvlHld}, "
              f"总持仓:{stk_holding_item.sumHld}, 持仓成本价:{stk_holding_item.costPrice}")
    elif msg_id == eOesMsgTypeT.OESMSG_QRYMSG_STOCK.value:
        stock_item = cast(msg_item, POINTER(OesStockItemT))[0]
        print(f"证券代码:{stock_item.securityId.decode()}, 连续停牌标识:{stock_item.suspFlag}, "
              f"临时停牌标识:{stock_item.temporarySuspFlag}, 最小报价单位:{stock_item.priceTick}, "
              f"前收盘价:{stock_item.prevClose}, 总股本:{stock_item.outstandingShare}, "
              f"流通股数量:{stock_item.publicFloatShare}, 证券名称:{stock_item.securityName.decode()}")
    return 0


def oes_query1(oes):
    print(f"当前交易日:{oes.OesApi_GetTradingDay()}")
    client_overview = OesClientOverviewT()
    oes.OesApi_GetClientOverview(client_overview)
    print(f"客户端编号:{client_overview.clientId}, 客户端类型:{client_overview.clientType}, "
          f"客户端状态:{client_overview.clientStatus}, 委托通道的流量控制:{client_overview.ordTrafficLimit}, "
          f"查询通道的流量控制:{client_overview.qryTrafficLimit}, 最大委托笔数限制:{client_overview.maxOrdCount}")
    print()

    cash_asset_item = OesCashAssetItemT()
    print("查询单条资金资产信息")
    oes.OesApi_QuerySingleCashAsset(None, cash_asset_item)
    print(f"资金账户代码:{cash_asset_item.cashAcctId.decode()}, 客户代码:{cash_asset_item.custId.decode()}, "
          f"期初余额:{cash_asset_item.beginningBal}, 当前交易冻结金额:{cash_asset_item.buyFrzAmt}, "
          f"当前可用余额:{cash_asset_item.currentAvailableBal}")
    print()

    print("查询证券账户信息")
    oes.OesApi_QueryInvAcct(None, OnOesQuery, None)
    print()

    print("查询单条股票持仓信息")
    holding_item = OesStkHoldingItemT()
    oes.OesApi_QuerySingleStkHolding('A100000001', '600000', holding_item)
    print(f"账户代码:{holding_item.invAcctId.decode()}, 证券代码:{holding_item.securityId.decode()}, "
          f"当前可卖持仓:{holding_item.sumHld}, 持仓成本价:{holding_item.costPrice}")
    print()

    print("查询客户资金信息")
    oes.OesApi_QueryCashAsset(None, OnOesQuery, None)


def oes_query2(oes):
    print("查询单条委托信息")
    ord_item = OesOrdItemT()
    oes.OesApi_QuerySingleOrder(1, ord_item)
    print(f"客户委托流水号:{ord_item.clSeqNo}, 证券代码:{ord_item.securityId.decode()}, "
          f"委托数量:{ord_item.ordQty}, 委托价格:{ord_item.ordPrice}, 委托时间:{ord_item.ordTime}, "
          f"委托确认时间:{ord_item.ordCnfmTime}, 订单当前状态:{ord_item.ordStatus}, "
          f"委托确认状态:{ord_item.ordCnfmSts}")
    print()

    print("查询所有委托信息")
    oes.OesApi_QueryOrder(None, OnOesQuery, None)
    print("查询成交信息")
    oes.OesApi_QueryTrade(None, OnOesQuery, None)
    print("查询股票持仓信息")
    oes.OesApi_QueryStkHolding(None, OnOesQuery, None)
    print("查询现货产品信息")
    oes.OesApi_QueryStock(None, OnOesQuery, None)


def OnOesMsg(session_info, msg_head, msg_item, callback_params):
    msg_id = msg_head.contents.msgId
    # print('OnOesMsg:', msg_id)
    rpt = cast(msg_item, POINTER(OesRptMsgT))[0]
    if msg_id == eOesMsgTypeT.OESMSG_RPT_ORDER_INSERT.value:
        ord_cnfm = rpt.rptBody.ordCnfm
        print(f"OES委托已生成 - 客户委托流水号:{ord_cnfm.clSeqNo}, 证券代码:{ord_cnfm.securityId.decode()}, "
              f"委托时间:{ord_cnfm.ordTime}, 委托确认时间:{ord_cnfm.ordCnfmTime}, "
              f"订单当前状态:{ord_cnfm.ordStatus}, 委托确认状态:{ord_cnfm.ordCnfmSts}")
    elif msg_id == eOesMsgTypeT.OESMSG_RPT_BUSINESS_REJECT.value:
        ord_reject = rpt.rptBody.ordRejectRsp
        print(f"OES业务拒绝 - 客户委托流水号:{ord_reject.clSeqNo}, 订单拒绝原因:{ord_reject.ordRejReason}")
    elif msg_id == eOesMsgTypeT.OESMSG_RPT_ORDER_REPORT.value:
        pass
    elif msg_id == eOesMsgTypeT.OESMSG_RPT_TRADE_REPORT.value:
        trd_cnfm = rpt.rptBody.trdCnfm
        print(f"交易所成交回报 - 交易所成交编号:{trd_cnfm.exchTrdNum}, 证券代码:{trd_cnfm.securityId.decode()}, "
              f"成交时间:{trd_cnfm.trdTime}, 成交数量:{trd_cnfm.trdQty}, 累计执行数量:{trd_cnfm.cumQty}, "
              f"原始委托数量:{trd_cnfm.origOrdQty}, 客户委托流水号:{trd_cnfm.clSeqNo}, 累计交易费用:{trd_cnfm.cumFee}")
    elif msg_id == eOesMsgTypeT.OESMSG_RPT_FUND_TRSF_REJECT.value:
        fund_trsf_reject = rpt.rptBody.fundTrsfRejectRsp
        print(f"出入金委托拒绝 - 客户委托流水号:{fund_trsf_reject.clSeqNo}, 错误码:{fund_trsf_reject.rejReason}, "
              f"错误信息:{fund_trsf_reject.errorInfo.decode()}")
    elif msg_id == eOesMsgTypeT.OESMSG_RPT_FUND_TRSF_REPORT.value:
        fund_trsf_cnfm = rpt.rptBody.fundTrsfCnfm
        print(f"出入金委托执行报告 - 客户委托流水号:{fund_trsf_cnfm.clSeqNo}, 出入金委托执行状态:{fund_trsf_cnfm.trsfStatus}, "
              f"错误原因:{fund_trsf_cnfm.rejReason}, 主柜错误码:{fund_trsf_cnfm.counterErrCode}, "
              f"错误信息:{fund_trsf_cnfm.errorInfo.decode()}")
    elif msg_id == eOesMsgTypeT.OESMSG_RPT_CASH_ASSET_VARIATION.value:
        pass
    elif msg_id == eOesMsgTypeT.OESMSG_RPT_STOCK_HOLDING_VARIATION.value:
        pass
    return 0


def oes_wait(oes):
    while True:
        oes.OesApi_WaitReportMsg(SPK_DEFAULT_SO_TIMEOUT_MS, OnOesMsg, None)


def oes_order(oes, cl_seq_no):
    thread = Thread(target=oes_wait, args=(oes, ))
    thread.setDaemon(True)
    thread.start()
    time.sleep(1)

    print("发送委托申报请求")
    ord_req = OesOrdReqT()
    cl_seq_no += 1
    ord_req.clSeqNo = c_int32(cl_seq_no)
    ord_req.mktId = eOesMarketIdT.OES_MKT_SH_ASHARE.value
    ord_req.ordType = eOesOrdTypeT.OES_ORD_TYPE_LMT.value
    ord_req.bsType = eOesBuySellTypeT.OES_BS_TYPE_BUY.value
    ord_req.securityId = b'600000'
    ord_req.ordQty = 100
    ord_req.ordPrice = 96500
    ord_req.origClOrdId = 0
    oes.OesApi_SendOrderReq(ord_req)

    time.sleep(1)
    print("发送撤单请求")
    ord_cancel_req = OesOrdCancelReqT()
    cl_seq_no += 1
    ord_cancel_req.clSeqNo = c_int32(cl_seq_no)
    ord_cancel_req.mktId = eOesMarketIdT.OES_MKT_SH_ASHARE.value
    ord_cancel_req.origClSeqNo = c_int32(cl_seq_no - 1)
    oes.OesApi_SendOrderCancelReq(ord_cancel_req)

    print("批量发送多条委托请求")
    ord_req1 = OesOrdReqT()
    cl_seq_no += 1
    ord_req1.clSeqNo = c_int32(cl_seq_no)
    ord_req1.mktId = eOesMarketIdT.OES_MKT_SH_ASHARE.value
    ord_req1.ordType = eOesOrdTypeT.OES_ORD_TYPE_LMT.value
    ord_req1.bsType = eOesBuySellTypeT.OES_BS_TYPE_BUY.value
    ord_req1.securityId = b'600000'
    ord_req1.ordQty = 200
    ord_req1.ordPrice = 96300
    ord_req1.origClOrdId = 0

    ord_req2 = OesOrdReqT()
    cl_seq_no += 1
    ord_req2.clSeqNo = c_int32(cl_seq_no)
    ord_req2.mktId = eOesMarketIdT.OES_MKT_SZ_ASHARE.value
    ord_req2.ordType = eOesOrdTypeT.OES_ORD_TYPE_LMT.value
    ord_req2.bsType = eOesBuySellTypeT.OES_BS_TYPE_BUY.value
    ord_req2.securityId = b'000001'
    ord_req2.ordQty = 100
    ord_req2.ordPrice = 237100
    ord_req2.origClOrdId = 0

    ord_req_array = (OesOrdReqT * 2)()
    ord_req_array[0] = ord_req1
    ord_req_array[1] = ord_req2
    oes.OesApi_SendBatchOrdersReq2(ord_req_array[0], 2)

    print("发送出入金委托请求")
    fund_trsf_req = OesFundTrsfReqT()
    cl_seq_no += 1
    fund_trsf_req.clSeqNo = c_int32(cl_seq_no)
    fund_trsf_req.direct = eOesFundTrsfDirectT.OES_FUND_TRSF_DIRECT_OUT.value
    fund_trsf_req.isAllotOnly = eOesFundTrsfTypeT.OES_FUND_TRSF_TYPE_OES_COUNTER.value
    fund_trsf_req.cashAcctId = b"1000000001"
    fund_trsf_req.occurAmt = 10000
    oes.OesApi_SendFundTransferReq(fund_trsf_req)


def main():
    oes = OesApi('./liboes_api.so')
    c_cl_seq_no = c_int32()
    # 完整的初始化客户端环境
    if oes.OesApi_InitAll('./oes_client_sample.conf', -1, c_cl_seq_no):
        print('OES登陆成功')
        cl_seq_no = c_cl_seq_no.value
        oes_set_get(oes)
        oes_query1(oes)
        oes_order(oes, cl_seq_no)
        oes_query2(oes)
        input()
        # 注销并关闭所有的客户端会话
        oes.OesApi_LogoutAll(0)
    else:
        print('OES登陆失败')
    # 直接断开与服务器的连接并释放会话数据
    oes.OesApi_DestoryAll()


if __name__ == '__main__':
    main()
