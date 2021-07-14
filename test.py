# -*- coding: utf-8 -*-
from oes_struct import OesQryEtfComponentFilter
from oes_struct import OesQryEtfFilter
from oes_struct import OesQryInvAcctFilter
from oes_struct import OesQryIssueFilter
from oes_struct import OesQryLotWinningFilter
from oes_struct import OesQryTrdFilter
from oes_struct import OesQryCommissionRateFilter
from oes_struct import OesQryOrdFilter
from oes_struct import OesClientOverview
from oes_struct import OesQryStkHoldingFilter
from oes_struct import OesQryCashAssetFilter
from oes_struct import OesQryCustFilter
from oes_struct import OesQryFundTransferSerialFilter
from oes_struct import OesMarketId
from oes_struct import OesBuySellType
from oes_struct import OesOrdType
from oes_struct import OesOrdReq
from oes_struct import OesOrdCancelReq
from oes_struct import OesEtfComponentItem
from oes_struct import OesQryStockFilter
from oes_struct import OesStockBaseInfo as OesStockItem

from oes_struct import OesCommissionRateItem
from oes_struct import OesOrdCnfm as OesOrdItem
from oes_struct import OesOrdReject
from oes_struct import OesStkHoldingItem
from oes_struct import OesTrdCnfm as OesTrdItem
from oes_struct import OesCashAssetItem
from oes_struct import OesCustBaseInfo as OesCustItem
from oes_struct import OesLotWinningBaseInfo as OesLotWinningItem
from oes_struct import OesIssueBaseInfo as OesIssueItem
from oes_struct import OesFundTrsfReport as OesFundTransferSerialItem
from oes_struct import OesInvAcctItem
from oes_struct import OesEtfBaseInfo as OesEtfItem

from oes_struct import OesMsgType
from oes_struct import OesRptMsg

from oes_struct import Head
from oes_api import OesApiWrap
from threading import Thread

from ctypes import *
import time
import datetime
import errno
import logging


def test_demo(overview):
    print('''client overviewer 
    cust_id={0},cust_name={1}'''.format(overview.client_id,
                                        overview.client_name.decode("utf-8", "ignore")))
    cust_cnt = len(overview.cust_items)
    for i in range(0, cust_cnt):
        print("""cust_name= {},
        status = {},
        risk_level = {},
        cust_name = {}
        """.format(overview.cust_items[i].cust_name.decode("utf-8", "ignore"), overview.cust_items[i].status,
                   overview.cust_items[i].risk_level,
                   overview.cust_items[i].cust_name.decode("utf-8", "ignore")))


def on_comms_qry_rsp(session, msg_head, msg, qry_cursor, user_info):
    comms_item = cast(msg, POINTER(OesCommissionRateItem))
    print('消息代码: {}'.format(msg_head.contents.msg_id))
    print('fee_rate: {} 证券代码: {}'.format(
        comms_item.contents.fee_rate,
        comms_item.contents.security_id.decode('utf-8', 'ignore')))
    return 0


def on_order_qry_rsp(session, msg_head, msg, qry_cursor, user_info):
    ord_item = cast(msg, POINTER(OesOrdItem))
    print('消息代码: {}'.format(msg_head.contents.msg_id))
    print('委托序号: {} 证券代码: {}   cl_ord_id:{}, ord_date ;{}  cum_qty:{}, rejson:{},bs_type:{}'.format(
        ord_item.contents.cl_seq_no,
        ord_item.contents.security_id.decode('utf-8', 'ignore'),
        ord_item.contents.cl_ord_id,
        ord_item.contents.ord_date,
        ord_item.contents.cum_qty,
        ord_item.contents.ord_rej_reason,
        ord_item.contents.bs_type
    ))
    print('__tgw_partition_no {0}'.format(ord_item.contents.__tgw_partition_no))
    return 0


def on_stk_holding_qry_rsp(session, msg_head, msg, qry_cursor, user_info):
    stk_hld_item = cast(msg, POINTER(OesStkHoldingItem))
    print('消息代码: {}'.format(msg_head.contents.msg_id))
    print("""
              证券代码:{} ,
              日初持仓：{}，
              当前可卖持仓：{} """.format(
        stk_hld_item.contents.security_id.decode('utf-8', 'ignore'),
        stk_hld_item.contents.original_hld,
        stk_hld_item.contents.sell_avl_hld, ))

    # ))
    return 0


def on_trade_qry_rsp(session, msg_head, msg, qry_cursor, user_info):
    trd_item = cast(msg, POINTER(OesTrdItem))
    print('消息代码: {}'.format(msg_head.contents.msg_id))
    print('客户订单编号: {} 证券代码: {} 成交数量 : {},成交金额:{},订单状态:{},订单类型：{}买卖类型：{}，证券类别:{},'
          '证券子类别：{},累计成交金额：{}'.format(
        trd_item.contents.cl_ord_id,
        trd_item.contents.security_id.decode('utf-8', 'ignore'),
        trd_item.contents.trd_qty,
        trd_item.contents.trd_amt,
        trd_item.contents.ord_status,
        trd_item.contents.ord_type,
        trd_item.contents.ord_buy_sell_type,
        trd_item.contents.security_type,
        trd_item.contents.sub_security_type,
        trd_item.contents.cum_amt
    ))
    print('__tgw_partition_no {}'.format(trd_item.contents.__tgw_partition_no))
    return 0


def on_cash_asset_qry_rsp(session, msg_head, msg, qry_cursor, user_info):
    cash_asset_item = cast(msg, POINTER(OesCashAssetItem))
    print('消息代码: {}'.format(msg_head.contents.msg_id))
    print('客户代码：{}，资金账户代码: {} 期初可用余额: {} 当前可用余额 : {},日中累计买，申购、逆回购使用资金{}'.format(
        cash_asset_item.contents.cust_id.decode("utf-8", 'ignore'),
        cash_asset_item.contents.cash_acct_id.decode("utf-8", 'ignore'),
        cash_asset_item.contents.beginning_available_bal,
        cash_asset_item.contents.current_available_bal,
        cash_asset_item.contents.total_buy_amt,
    ))
    return 0


def on_cust_info_qry_rsp(session, msg_head, msg, qry_cursor, user_info):
    cust_item = cast(msg, POINTER(OesCustItem))
    print('消息代码: {}'.format(msg_head.contents.msg_id))
    print('客户代码：{}，客户状态: {} 营业部代码: {} '.format(
        cust_item.contents.cust_id.decode("utf-8", 'ignore'),
        cust_item.contents.status,
        cust_item.contents.branch_id,
    ))
    return 0


def on_lot_winning_qry_rsp(session, msg_head, msg, qry_cursor, user_info):
    lot_wining_item = cast(msg, POINTER(OesLotWinningItem))
    print('消息代码: {}'.format(msg_head.contents.msg_id))
    print('证券账户：{}，配号或中签代码: {},证券名称:{}'.format(
        lot_wining_item.contents.inv_acct_id.decode("utf-8", 'ignore'),
        lot_wining_item.contents.security_id.decode("utf-8", 'ignore'),
        lot_wining_item.contents.security_name.decode("utf-8", 'ignore'),

    ))
    return 0


def on_issue_qry_rsp(session, msg_head, msg, qry_cursor, user_info):
    issue_item = cast(msg, POINTER(OesIssueItem))
    print('消息代码: {}'.format(msg_head.contents.msg_id))
    print('证券发行代码：{}，证券代码: {},总发行量：{}'.format(
        issue_item.contents.security_id.decode("utf-8", 'ignore'),
        issue_item.contents.underlying_security_id.decode("utf-8", 'ignore'),
        issue_item.contents.issue_qty

    ))
    return 0


def on_fund_transfer_serial_qry_rsp(session, msg_head, msg, qry_cursor, user_info):
    fund_transfer_serial_item = cast(msg, POINTER(OesFundTransferSerialItem))
    print('消息代码: {}'.format(msg_head.contents.msg_id))
    print('划转方向：{}，发生金额：{}'.format(
        fund_transfer_serial_item.contents.direct,
        fund_transfer_serial_item.contents.occur_amt

    ))
    return 0


def on_inv_acct_qry_rsp(session, msg_head, msg, qry_cursor, user_info):
    inv_acct_item = cast(msg, POINTER(OesInvAcctItem))
    print('消息代码: {}'.format(msg_head.contents.msg_id))
    print('客户代码：{}，证券账户代码：{}, 市场：{}'.format(
        inv_acct_item.contents.cust_id.decode("utf-8", 'ignore'),
        inv_acct_item.contents.inv_acct_id.decode("utf-8", 'ignore'),
        inv_acct_item.contents.mkt_id

    ))
    return 0


def on_etf_qry_rsp(session, msg_head, msg, qry_cursor, user_info):
    etf_item = cast(msg, POINTER(OesEtfItem))
    print('消息代码: {}'.format(msg_head.contents.msg_id))
    print('ETF申赎代码：{}，ETF买卖代码：{}, 申购赎回单位：{}'.format(
        etf_item.contents.fund_id.decode("utf-8", 'ignore'),
        etf_item.contents.security_id.decode("utf-8", 'ignore'),
        etf_item.contents.cre_rdm_unit

    ))
    return 0


def on_etf_component_qry_rsp(session, msg_head, msg, qry_cursor, user_info):
    etf_cmp_item = cast(msg, POINTER(OesEtfComponentItem))
    print('消息代码: {}'.format(msg_head.contents.msg_id))
    print('ETF成分股代码：{}，成分股数量：{}, 现金替代标识：{}'.format(
        etf_cmp_item.contents.security_id.decode("utf-8", 'ignore'),
        etf_cmp_item.contents.qty,
        etf_cmp_item.contents.sub_flag

    ))
    return 0


def on_stock_qry_rsp(session, msg_head, msg, qry_cursor, user_info):
    stock_item = cast(msg, POINTER(OesStockItem))
    print(stock_item.contents.to_dict())
    # print('消息代码: {}'.format(msg_head.contents.msg_id))
    # print('证券代码：{}，市场代码：{}, 当日回转标志：{}, 证券类别：{}，证券子类别：{}, 产品类型：{}'.format(
    #     stock_item.contents.security_id.decode("utf-8", 'ignore'),
    #     stock_item.contents.mkt_id,
    #     stock_item.contents.is_day_trading,
    #     stock_item.contents.security_type,
    #     stock_item.contents.sub_security_type,
    #     stock_item.contents.product_type,
    #
    # ))
    return 0


def send_cancell_ord(oes_api_handle, lastClSeqNo):
    req = OesOrdCancelReq()
    req.cl_seq_no = c_int32(lastClSeqNo.value + 1)
    req.mkt_id = OesMarketId.OES_MKT_ID_SH_A.value
    req.orig_cl_ord_id = 5200100002
    time.sleep(1)
    ret_code = oes_api_handle.oes_api_send_order_cancell_req(req)
    print("撤单发送结果, ret_code: {}".format(ret_code))


def send_order(oes_api_handle, lastClSeqNo):
    # 报单
    req = OesOrdReq()
    req.cl_seq_no = c_int32(lastClSeqNo.value + 1)
    req.mkt_id = OesMarketId.OES_MKT_ID_SH_A.value
    req.ord_type = OesOrdType.OES_ORD_TYPE_LMT.value
    req.bs_type = OesBuySellType.OES_BS_TYPE_BUY.value
    req.security_id = bytes('600000', encoding='utf-8')
    req.ord_qty = 100
    req.ord_price = int(8908 * 10000)
    req.orig_cl_ord_id = 0

    time.sleep(1)
    ret_code = oes_api_handle.oes_api_send_order_req(req)
    print("委托发送结果, ret_code: {}".format(ret_code))


def handler_report_msg(session, msg_head, msg_body, user_info):
    msg_head_i = cast(msg_head, POINTER(Head))
    msg_id = msg_head_i.contents.msg_id
    OesRspMsgBody = cast(msg_body, POINTER(OesRptMsg))
    OesRptMsgBody = OesRspMsgBody.contents.rpt_body
    print(msg_id)

    if msg_id == OesMsgType.OESMSG_SESS_HEARTBEAT.value:
        return 0

    elif msg_id == OesMsgType.OESMSG_RPT_REPORT_SYNCHRONIZATION.value:
        return 0

    elif msg_id == OesMsgType.OESMSG_RPT_ORDER_INSERT.value:
        # OES委托响应-委托已生成
        oes_ord_cnfm = OesRptMsgBody.ord_insert_rsp
        print(oes_ord_cnfm)
        return 0

    elif msg_id == OesMsgType.OESMSG_RPT_ORDER_REJECT.value:
        # OES委托响应-业务拒绝
        oes_ord_reject = OesRptMsgBody.ord_reject_rsp
        print(oes_ord_reject)
        return 0

    elif msg_id == OesMsgType.OESMSG_RPT_ORDER_REPORT.value:
        # 交易所执行报告-委托确认
        oes_ord_cnfm = OesRptMsgBody.ord_cnfm
        print(oes_ord_cnfm)
        return 0

    elif msg_id == OesMsgType.OESMSG_RPT_TRADE_REPORT.value:
        # 交易所执行报告-成交回报
        oes_trd_cnfm = OesRptMsgBody.trd_cnfm
        print(oes_trd_cnfm)
        return 0

    elif msg_id == OesMsgType.OESMSG_RPT_FUND_TRSF_REPORT.value:
        # 出入金委托执行报告
        oes_fund_trsf_reject_rsp = OesRptMsgBody.fund_trsf_reject_rsp
        print(oes_fund_trsf_reject_rsp)
        return 0

    elif msg_id == OesMsgType.OESMSG_RPT_FUND_TRSF_REJECT.value:
        # 出入金委托拒绝
        oes_fund_trsf_cnfm = OesRptMsgBody.fund_trsf_cnfm
        print(oes_fund_trsf_cnfm)
        return 0

    elif msg_id == OesMsgType.OESMSG_RPT_CASH_ASSET_VARIATION.value:
        # 资金变动信息
        cash_asset_rpt = OesRptMsgBody.cash_asset_rpt
        print(cash_asset_rpt)
        return 0

    elif msg_id == OesMsgType.OESMSG_RPT_STOCK_HOLDING_VARIATION.value:
        # 持仓变动信息(股票)
        stk_holding_rpt = OesRptMsgBody.stk_holding_rpt
        print(stk_holding_rpt)
        return 0

    elif msg_id == OesMsgType.OESMSG_RPT_OPTION_HOLDING_VARIATION.value:
        # 持仓变动信息(期权)
        opt_holding_rpt = OesRptMsgBody.opt_holding_rpt
        print(opt_holding_rpt)
        return 0

    else:
        em = "invalid msg_id {}".format(msg_id)
        print(em)
    return 0


def on_time_out(oes_api_handler, channel_type):
    if channel_type == "rpt":
        channel = oes_api_handler._clientEnv.rpt_channel
    elif channel_type == "ord":
        channel = oes_api_handler._clientEnv.ord_channel
    else:
        channel = oes_api_handler._clientEnv.qry_channel

    last_recv_time = oes_api_handler.oes_api_get_last_recv_time(channel_type)
    interval = time.time() - last_recv_time
    if channel.heart_bt_int > 0:
        if interval > channel.heart_bt_int * 2:
            em = "会话已超时, 将主动断开与服务器的连接! " \
                 "lastRecvTime: {}" \
                 "lastSendTime: {}, " \
                 "heartBtInt: {}, " \
                 "recvInterval: {}".format(
                channel.last_recv_time,
                channel.last_send_time,
                channel.heart_bt_int,
                interval)
            print(em)
            logging.error(em)
            return errno.ETIMEDOUT
    return 0


def report_thread_main(oes_api_handler):
    thread_terminated_flag = 1
    while thread_terminated_flag:
        ret_code = oes_api_handler.oes_api_wait_rpt_msg(handler_report_msg)
        if ret_code < 0:
            # 检查会话消息是否已经超时：
            print(ret_code)
            if abs(ret_code) == errno.ETIMEDOUT:
                if on_time_out(oes_api_handler, "rpt") == 0:
                    continue
                else:
                    thread_terminated_flag = 0
                    return False
            if abs(ret_code) == errno.EPIPE:
                thread_terminated_flag = 0
                return False
    return True


def main():
    oes_api_handle = OesApiWrap('.', 'liboes_api.so')

    user_name = '******'
    passwd = '******'

    oes_api_handle.oes_api_set_user_name(user_name)
    oes_api_handle.oes_api_set_passwd(passwd)

    lastClSeqNo = c_int32()
    if not oes_api_handle.oes_api_init_all('配置文件.conf', lastClSeqNo):
        print('登录失败')
        return
    print("登录成功, lastClSeqNo: {}".format(lastClSeqNo.value))

    # 收回报数据
    if 0:
        thread = Thread(target=report_thread_main, kwargs={"oes_api_handler": oes_api_handle})
        thread.start()
        thread.join()
    if 0:
        last_recv_time = oes_api_handle.oes_api_get_last_recv_time('rpt')
        print("recv", last_recv_time)
        print(time.time())
        time_interval = time.time() - last_recv_time
        print(time_interval)

    # 查询委托
    if 0:
        start_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime())
        ord_filter = OesQryOrdFilter()
        ord_filter.bs_type = 8
        ret_code = oes_api_handle.oes_api_query_order_req(ord_filter, on_order_qry_rsp)
        print("委托查询结果, ret_code: {}".format(ret_code))
        end_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime())
        print("开始时间: ", start_time)
        print("结束时间: ", end_time)

    # 查询费率
    if 0:
        comms_filter = OesQryCommissionRateFilter()
        ret_code = oes_api_handle.oes_api_query_comms_req(comms_filter, on_comms_qry_rsp)
        print("费率查询结果, ret_code: {}".format(ret_code))

    # 查询总览信息
    if 0:
        overview = OesClientOverview()
        oes_api_handle.oes_api_query_client_overview_req(overview, test_demo)
        ret_code = oes_api_handle.oes_api_query_client_overview_req(overview, test_demo)
        print("客户总览查询结果， ret_code :{}".format(ret_code))

    # 查询现货产品信息
    if 1:
        stk_hld_filter = OesQryStockFilter()
        ret_code = oes_api_handle.oes_api_query_stock_req(stk_hld_filter, on_stock_qry_rsp)
        # print("现货持仓查询结果，ret_code:{}".format(ret_code))
        # print(ret_code.to_dict())
    # 查询现货持仓
    if 0:
        stk_hld_filter = OesQryStkHoldingFilter()
        stk_hld_filter.mkt_id = 2
        stk_hld_filter.security_type = 1
        ret_code = oes_api_handle.oes_api_query_stk_holding_req(stk_hld_filter, on_stk_holding_qry_rsp)
        print("现货持仓查询结果，ret_code:{}".format(ret_code))

    # # 查询成交回报
    if 0:
        trd_filter = OesQryTrdFilter()
        ret_code = oes_api_handle.oes_api_query_trd_req(trd_filter, on_trade_qry_rsp)
        print('成交回报查询结果，ret_code:{}'.format(ret_code))

    # 查询客户资金信息
    if 0:
        cash_asset_fiter = OesQryCashAssetFilter()
        ret_code = oes_api_handle.oes_api_query_cash_asset_req(cash_asset_fiter, on_cash_asset_qry_rsp)
        print('资金账户查询结果，ret_code: {}'.format(ret_code))

    # 查询客户信息
    if 0:
        cust_info_filter = OesQryCustFilter()
        ret_code = oes_api_handle.oes_api_query_cust_info_req(cust_info_filter, on_cust_info_qry_rsp)
        print("客户信息查询结果，ret_code: {}".format(ret_code))

    # 查询证券账户信息
    if 0:
        inv_acct_filter = OesQryInvAcctFilter()
        ret_code = oes_api_handle.oes_api_query_inv_acct_req(inv_acct_filter, on_inv_acct_qry_rsp)
        print("证券账户信息查询结果， ret_code:{}".format(ret_code))

    # 查询新股中签配号信息
    if 0:
        lot_winning_filter = OesQryLotWinningFilter()
        ret_code = oes_api_handle.oes_api_query_lot_winning_req(lot_winning_filter, on_lot_winning_qry_rsp)
        print("新股中签配号信息查询结果，ret_code: {}".format(ret_code))

    # 查询证券发行
    if 0:
        issue_filter = OesQryIssueFilter()
        ret_code = oes_api_handle.oes_api_query_issue_req(issue_filter, on_issue_qry_rsp)
        print("发行产品信息查询结果， ret_code: {}".format(ret_code))

    # 查询出入金流水
    if 0:
        fund_transfer_serial_filter = OesQryFundTransferSerialFilter()
        ret_code = oes_api_handle.oes_api_query_fund_transfer_serial_req(fund_transfer_serial_filter,
                                                                         on_fund_transfer_serial_qry_rsp)
        print("出入金流水查询结果,ret_code:{}".format(ret_code))

    # 查询ETF信息
    if 0:
        etf_filter = OesQryEtfFilter()
        ret_code = oes_api_handle.oes_api_query_etf_req(etf_filter, on_etf_qry_rsp)
        print("ETF产品查询结果，ret_code : {}".format(ret_code))

    # 查询ETF成分股信息
    if 0:
        etf_component_filter = OesQryEtfComponentFilter()
        etf_component_filter.fund_id = bytes("510051", encoding="utf-8")
        ret_code = oes_api_handle.oes_api_query_etf_component_req(etf_component_filter, on_etf_component_qry_rsp)
        print("ETF 成分股 查询结果，ret_code : {}".format(ret_code))

    # 报单
    if 0:
        send_order(oes_api_handle, lastClSeqNo)

    # 撤单
    if 0:
        send_cancell_ord(oes_api_handle, lastClSeqNo)

    time.sleep(1)
    oes_api_handle.oes_api_logout_all()
    oes_api_handle.oes_api_destory_all()


if __name__ == '__main__':
    main()
