# -*- coding: utf-8 -*-
import os

from ctypes import *
from oes_struct import OesApiClientEnv as OesApiClientEnv
from oes_struct import SGeneralClientChannel as OesApiSessionInfo
from oes_struct import OesQryOrdFilter as OesQryOrdFilter
from oes_struct import OesQryCommissionRateFilter as OesQryCommissionRateFilter
from oes_struct import OesQryCursor as OesQryCursor
from oes_struct import Head as Head
from oes_struct import OesOrdReq as OesOrdReq
from oes_struct import OesOrdCancelReq
from oes_struct import OesClientOverview
from oes_struct import OesQryStkHoldingFilter
from oes_struct import OesQryTrdFilter
from oes_struct import OesQryCashAssetFilter
from oes_struct import OesQryCustFilter
from oes_struct import OesQryInvAcctFilter
from oes_struct import OesQryLotWinningFilter
from oes_struct import OesQryIssueFilter
from oes_struct import OesQryFundTransferSerialFilter
from oes_struct import OesQryEtfFilter
from oes_struct import OesQryEtfComponentFilter
from oes_struct import OesQryStockFilter
from oes_struct import OesOrdCnfm
from oes_struct import OesTrdCnfm
from oes_struct import OesFundTrsfReq
from oes_struct import OesRspMsgBody
from oes_struct import OesOrdItem
from oes_struct import OesCashAssetItem
from oes_struct import OesStkHoldingItem
from oes_struct import OesQryMarketStateFilter
from oes_struct import OesCounterCashItem
from oes_struct import OesBrokerParamsInfo
from oes_struct import SSocketOptionConfig
from oes_struct import OesApiClientCfg
from oes_struct import OesApiRemoteCfg
from oes_struct import OesApiSubscribeInfo
from oes_struct import OesApiAddrInfo
from oes_struct import OesStockItem

# /** 默认的主配置区段名称 */
OESAPI_CFG_DEFAULT_SECTION = "oes_client"
# /** 默认的日志配置区段名称 */
OESAPI_CFG_DEFAULT_SECTION_LOGGER = "log"
# /** 默认的委托申报配置项名称 */
OESAPI_CFG_DEFAULT_KEY_ORD_ADDR = "ordServer"
# /** 默认的执行报告配置项名称 */
OESAPI_CFG_DEFAULT_KEY_RPT_ADDR = "rptServer"
# /** 默认的查询服务配置项名称 */
OESAPI_CFG_DEFAULT_KEY_QRY_ADDR = "qryServer"
# /** 默认的消息类型列表等字符串分隔符 */
OESAPI_DEFAULT_STRING_DELIM = ',;| \\t\\r\\n'

import sys
ENCODE_TYPE = 'utf-8'
if sys.platform == 'win32':
    ENCODE_TYPE = 'gbk'

class OesApiWrap:
    def __init__(self, lib_path, lib_name):
        # 回调函数声明
        self._ON_QRY_RSP_FUNC = CFUNCTYPE(c_int32,
                                          POINTER(OesApiSessionInfo),
                                          POINTER(Head),
                                          c_void_p,
                                          POINTER(OesQryCursor),
                                          c_void_p)

        self._ON_RPT_MSG_FUNC = CFUNCTYPE(c_int32,
                                          POINTER(OesApiSessionInfo),
                                          POINTER(Head),
                                          c_void_p,
                                          c_void_p,
                                          use_errno=True)

        self._clientEnv = OesApiClientEnv()

        # 加载动态连接库
        self._oes_api = CDLL(os.path.join(lib_path, lib_name))

        # 获取api接口函数: 初始化函数
        self._ufx_init_all = self._oes_api.OesApi_InitAll
        self._ufx_init_all.restype = c_bool
        self._ufx_init_all.argtypes = [POINTER(OesApiClientEnv),
                                       c_char_p,
                                       c_char_p,
                                       c_char_p,
                                       c_char_p,
                                       c_char_p,
                                       c_char_p,
                                       c_int64,
                                       POINTER(c_int32)]

        # 连接并登录到指定的OES节点与服务
        self._oes_api_logon = self._oes_api.OesApi_Logon
        self._oes_api_logon.restype = c_bool
        self._oes_api_logon.argtypes = [POINTER(OesApiSessionInfo),
                                        c_uint8,
                                        c_char_p,
                                        c_char_p,
                                        c_char_p,
                                        c_int8,
                                        c_int32,
                                        POINTER(SSocketOptionConfig)]

        # 发送注销消息
        self._oes_api_logout = self._oes_api.OesApi_Logout
        self._oes_api_logout.restype = c_bool
        self._oes_api_logout.argtypes = [POINTER(OesApiSessionInfo),
                                         c_bool]

        # 直接断开与服务器的连接并释放会话数据
        self._oes_api_destory = self._oes_api.OesApi_Destory
        self._oes_api_destory.argtypes = [POINTER(OesApiSessionInfo), ]

        # 获取api接口函数: 登出函数
        self._oes_api_logout_all = self._oes_api.OesApi_LogoutAll
        self._oes_api_logout_all.argtypes = [POINTER(OesApiClientEnv),
                                             c_bool]

        self._oes_api_set_user_name = self._oes_api.OesApi_SetThreadUsername
        self._oes_api_set_user_name.argtypes = [c_char_p]

        self._oes_api_get_thread_username = self._oes_api.OesApi_GetThreadUsername
        self._oes_api_get_thread_username.restype = c_char_p
        self._oes_api_get_thread_username.argtypes = []

        self._oes_api_set_passwd = self._oes_api.OesApi_SetThreadPassword
        self._oes_api_set_passwd.argtypes = [c_char_p]

        self._oes_api_set_env_id = self._oes_api.OesApi_SetThreadEnvId
        self._oes_api_set_env_id.argtypes = [c_int8]

        self._oes_api_get_env_id = self._oes_api.OesApi_GetThreadEnvId
        self._oes_api_get_env_id.restype = c_int8
        self._oes_api_get_env_id.argtypes = []

        self._oes_api_set_thread_subscribe_env_id = self._oes_api.OesApi_SetThreadSubscribeEnvId
        self._oes_api_set_thread_subscribe_env_id.argtypes = [c_int8]

        self._oes_api_get_thread_subscribe_env_id = self._oes_api.OesApi_GetThreadSubscribeEnvId
        self._oes_api_get_thread_subscribe_env_id.restype = c_int8

        # 设置客户端自定义的本地IP和MAC
        self._oes_api_set_customized_ip_and_mac = self._oes_api.OesApi_SetCustomizedIpAndMac
        self._oes_api_set_customized_ip_and_mac.restype = c_bool
        self._oes_api_set_customized_ip_and_mac.argtypes = [c_char_p, c_char_p]

        # 设置客户端自定义的本地IP地址
        self._oes_api_set_customized_ip = self._oes_api.OesApi_SetCustomizedIp
        self._oes_api_set_customized_ip.restype = c_bool
        self._oes_api_set_customized_ip.argtypes = [c_char_p, ]

        # 设置客户端自定义的本地MAC地址
        self._oes_api_set_customized_mac = self._oes_api.OesApi_SetCustomizedMac
        self._oes_api_set_customized_mac.restype = c_bool
        self._oes_api_set_customized_mac.argtypes = [c_char_p, ]

        # 获取客户端自定义的本地IP
        self._oes_api_get_customized_ip = self._oes_api.OesApi_GetCustomizedIp
        self._oes_api_get_customized_ip.restype = c_char_p
        self._oes_api_get_customized_ip.argtypes = []

        # 获取客户端自定义的本地MAC
        self._oes_api_get_customized_mac = self._oes_api.OesApi_GetCustomizedMac
        self._oes_api_get_customized_mac.restype = c_char_p
        self._oes_api_get_customized_mac.argtypes = []

        # 设置客户端自定义的本地设备序列号
        self._oes_api_set_customized_driver_id = self._oes_api.OesApi_SetCustomizedDriverId
        self._oes_api_set_customized_driver_id.restype = c_bool
        self._oes_api_set_customized_driver_id.argtypes = [c_char_p]

        # 获取客户端自定义的本地设备序列号
        self._oes_api_get_customized_driver_id = self._oes_api.OesApi_GetCustomizedDriverId
        self._oes_api_get_customized_driver_id.restype = c_char_p
        self._oes_api_get_customized_driver_id.argtypes = []

        # 返回通道对应的客户端环境号 (clEnvId)
        self._oes_api_get_cl_env_id = self._oes_api.OesApi_GetClEnvId
        self._oes_api_get_cl_env_id.restype = c_int8
        self._oes_api_get_cl_env_id.argtypes = [POINTER(OesApiSessionInfo)]

        self._oes_api_destory_all = self._oes_api.OesApi_DestoryAll
        self._oes_api_destory_all.argtypes = [POINTER(OesApiClientEnv)]

        # 执行报告接口，
        # 等待回报消息到达，并通过回调函数进行消息处理
        self._oes_api_wait_report_msg = self._oes_api.OesApi_WaitReportMsg
        self._oes_api_wait_report_msg.restype = c_int32
        self._oes_api_wait_report_msg.argtypes = [POINTER(OesApiSessionInfo),
                                                  c_int32,
                                                  self._ON_RPT_MSG_FUNC,
                                                  c_void_p]

        # 接收(一条)回报消息
        # 阻塞等待直到完整的接收到一条回报消息或者到达超时时间
        self._oes_api_recv_report_msg = self._oes_api.OesApi_RecvReportMsg
        self._oes_api_recv_report_msg.restype = c_int32
        self._oes_api_recv_report_msg.argtypes = [POINTER(OesApiSessionInfo),
                                                  POINTER(Head),
                                                  POINTER(OesRspMsgBody),
                                                  c_int32,
                                                  c_int32]

        # 获取API的发行版本号
        self._oes_api_get_api_version = self._oes_api.OesApi_GetApiVersion
        self._oes_api_get_api_version.restype = c_char_p
        self._oes_api_get_api_version.argtypes = []

        # 获取当前交易日
        self._oes_api_get_trading_day = self._oes_api.OesApi_GetTradingDay
        self._oes_api_get_trading_day.restype = c_int32
        self._oes_api_get_trading_day.argtypes = [POINTER(OesApiSessionInfo), ]

        # 获取api接口函数: 获取通道最新接受消息时间
        self._oes_api_get_last_recv_time = self._oes_api.OesApi_GetLastRecvTime
        self._oes_api_get_last_recv_time.restype = c_int64
        self._oes_api_get_last_recv_time.argtypes = [POINTER(OesApiSessionInfo)]

        # 获取通道最近发送消息时间
        self._oes_api_get_last_send_time = self._oes_api.OesApi_GetLastSendTime
        self._oes_api_get_last_send_time.restype = c_int64
        self._oes_api_get_last_send_time.argtypes = [POINTER(OesApiSessionInfo)]

        # 返回回报通道是否还有更多已接收但尚未回调处理完成的数据
        self._oes_api_has_more_cached_data = self._oes_api.OesApi_HasMoreCachedData
        self._oes_api_has_more_cached_data.restype = c_int32
        self._oes_api_has_more_cached_data.argtypes = [POINTER(OesApiSessionInfo)]

        # 返回委托申报通道是否已经连接且有效
        self._oes_api_is_valid_ord_channel = self._oes_api.OesApi_IsValidOrdChannel
        self._oes_api_is_valid_ord_channel.restype = c_bool
        self._oes_api_is_valid_ord_channel.argtypes = [POINTER(OesApiSessionInfo)]

        # 返回回报通道是否已经连接且有效
        self._oes_api_is_valid_rpt_channel = self._oes_api.OesApi_IsValidRptChannel
        self._oes_api_is_valid_rpt_channel.restype = c_bool
        self._oes_api_is_valid_rpt_channel.argtypes = [POINTER(OesApiSessionInfo)]

        # 返回查询通道是否已经连接且有效
        self._oes_api_is_valid_qry_channel = self._oes_api.OesApi_IsValidQryChannel
        self._oes_api_is_valid_qry_channel.restype = c_bool
        self._oes_api_is_valid_qry_channel.argtypes = [POINTER(OesApiSessionInfo)]

        # 返回当前线程最近一次API调用失败的错误号
        self._oes_api_get_last_error = self._oes_api.OesApi_GetLastError
        self._oes_api_get_last_error.restype = c_int32
        self._oes_api_get_last_error.argtypes = []

        # 设置当前线程的API错误号
        self._oes_api_set_last_error = self._oes_api.OesApi_SetLastError
        self._oes_api_set_last_error.argtypes = [c_int32]

        # 获取api接口函数: 获取错误信息
        self._oes_api_get_error_msg = self._oes_api.OesApi_GetErrorMsg
        self._oes_api_get_error_msg.restype = c_char_p
        self._oes_api_get_error_msg.argtypes = [c_int32]

        # 返回消息头中的状态码所对应的错误信息
        self._oes_api_get_error_msg2 = self._oes_api.OesApi_GetErrorMsg2
        self._oes_api_get_error_msg2.restype = c_char_p
        self._oes_api_get_error_msg2.argtypes = [c_uint8, c_uint8]

        # 返回现货产品是否具有指定状态
        self._oes_api_has_stock_status = self._oes_api.OesApi_HasStockStatus
        self._oes_api_has_stock_status.restype = c_bool
        self._oes_api_has_stock_status.argtypes = [POINTER(OesStockItem), c_uint8]

        # 获取api接口函数: 发送委托请求
        self._oes_api_send_order_req = self._oes_api.OesApi_SendOrderReq
        self._oes_api_send_order_req.restype = c_int32
        self._oes_api_send_order_req.argtypes = [POINTER(OesApiSessionInfo),
                                                 POINTER(OesOrdReq)]
        # 获取api接口函数:发送出入金请求
        self._oes_api_send_fund_transfer_req = self._oes_api.OesApi_SendFundTransferReq
        self._oes_api_send_fund_transfer_req.restype = c_int32
        self._oes_api_send_fund_transfer_req.argtypes = [POINTER(OesApiSessionInfo),
                                                         POINTER(OesFundTrsfReq)]

        # 获取api接口函数: 发送撤单请求
        self._oes_api_send_order_cancell_req = self._oes_api.OesApi_SendOrderCancelReq
        self._oes_api_send_order_cancell_req.restype = c_int32
        self._oes_api_send_order_cancell_req.argtypes = [POINTER(OesApiSessionInfo),
                                                         POINTER(OesOrdCancelReq)]

        # 批量发送多条委托请求
        self._oes_api_send_batch_orders_req = self._oes_api.OesApi_SendBatchOrdersReq
        self._oes_api_send_batch_orders_req.restype = c_int32
        self._oes_api_send_batch_orders_req.argtypes = [POINTER(OesApiSessionInfo),
                                                        POINTER(POINTER(OesOrdReq)),
                                                        c_int32]

        # 批量发送多条委托请求
        self._oes_api_send_batch_orders_req2 = self._oes_api.OesApi_SendBatchOrdersReq2
        self._oes_api_send_batch_orders_req2.restype = c_int32
        self._oes_api_send_batch_orders_req2.argtypes = [POINTER(OesApiSessionInfo),
                                                         POINTER(OesOrdReq),
                                                         c_int32]

        # 获取api接口函数: 查询委托
        self._oes_api_query_order_req = self._oes_api.OesApi_QueryOrder
        self._oes_api_query_order_req.restype = c_int32
        self._oes_api_query_order_req.argtypes = [POINTER(OesApiSessionInfo),
                                                  POINTER(OesQryOrdFilter),
                                                  self._ON_QRY_RSP_FUNC,
                                                  c_void_p]

        # 获取api接口函数: 查询客户佣金信息
        self._oes_api_query_comms_req = self._oes_api.OesApi_QueryCommissionRate
        self._oes_api_query_comms_req.restype = c_int32
        self._oes_api_query_comms_req.argtypes = [POINTER(OesApiSessionInfo),
                                                  POINTER(OesQryCommissionRateFilter),
                                                  self._ON_QRY_RSP_FUNC,
                                                  c_void_p]
        # 获取api接口函数：查询现货产品
        self._oes_api_query_stock_req = self._oes_api.OesApi_QueryStock
        self._oes_api_query_stock_req.restype = c_int32
        self._oes_api_query_stock_req.argtypes = [POINTER(OesApiSessionInfo),
                                                  POINTER(OesQryStockFilter),
                                                  self._ON_QRY_RSP_FUNC,
                                                  c_void_p]
        # 获取api接口函数：查询现货持仓信息
        self._oes_api_query_stk_holding_req = self._oes_api.OesApi_QueryStkHolding
        self._oes_api_query_stk_holding_req.restype = c_int32
        self._oes_api_query_stk_holding_req.argtypes = [POINTER(OesApiSessionInfo),
                                                        POINTER(OesQryStkHoldingFilter),
                                                        self._ON_QRY_RSP_FUNC,
                                                        c_void_p]

        # 获取api接口函数：查询成交信息
        self._oes_api_query_trade_req = self._oes_api.OesApi_QueryTrade
        self._oes_api_query_trade_req.restype = c_int32
        self._oes_api_query_trade_req.argtypes = [POINTER(OesApiSessionInfo),
                                                  POINTER(OesQryTrdFilter),
                                                  self._ON_QRY_RSP_FUNC,
                                                  c_void_p]

        # 获取api接口函数：查询客户资金信息
        self._oes_api_query_cash_asset_req = self._oes_api.OesApi_QueryCashAsset
        self._oes_api_query_cash_asset_req.restype = c_int32
        self._oes_api_query_cash_asset_req.argtypes = [POINTER(OesApiSessionInfo),
                                                       POINTER(OesQryCashAssetFilter),
                                                       self._ON_QRY_RSP_FUNC,
                                                       c_void_p]

        # 获取api接口函数：查询客户信息
        self._oes_api_query_cust_info_req = self._oes_api.OesApi_QueryCustInfo
        self._oes_api_query_cust_info_req.restype = c_int32
        self._oes_api_query_cust_info_req.argtypes = [POINTER(OesApiSessionInfo),
                                                      POINTER(OesQryCustFilter),
                                                      self._ON_QRY_RSP_FUNC,
                                                      c_void_p]
        # 获取api接口函数：查询证券账户信息
        self._oes_api_query_inv_acct_req = self._oes_api.OesApi_QueryInvAcct
        self._oes_api_query_inv_acct_req.restype = c_int32
        self._oes_api_query_inv_acct_req.argtypes = [POINTER(OesApiSessionInfo),
                                                     POINTER(OesQryInvAcctFilter),
                                                     self._ON_QRY_RSP_FUNC,
                                                     c_void_p]

        # 获取api接口函数：查询新股中签、配号
        self._oes_api_query_lot_winning_req = self._oes_api.OesApi_QueryLotWinning
        self._oes_api_query_lot_winning_req.restype = c_int32
        self._oes_api_query_lot_winning_req.argtypes = [POINTER(OesApiSessionInfo),
                                                        POINTER(OesQryLotWinningFilter),
                                                        self._ON_QRY_RSP_FUNC,
                                                        c_void_p]

        # 获取api接口函数：查询证券发行产品信息
        self._oes_api_query_issue_req = self._oes_api.OesApi_QueryIssue
        self._oes_api_query_issue_req.restype = c_int32
        self._oes_api_query_issue_req.argtypes = [POINTER(OesApiSessionInfo),
                                                  POINTER(OesQryIssueFilter),
                                                  self._ON_QRY_RSP_FUNC,
                                                  c_void_p]

        # 获取api接口函数：查询出入金转账流水
        self._oes_api_query_fund_transfer_serial_req = self._oes_api.OesApi_QueryFundTransferSerial
        self._oes_api_query_fund_transfer_serial_req.restype = c_int32
        self._oes_api_query_fund_transfer_serial_req.argtypes = [POINTER(OesApiSessionInfo),
                                                                 POINTER(OesQryFundTransferSerialFilter),
                                                                 self._ON_QRY_RSP_FUNC,
                                                                 c_void_p]

        # 获取api接口函数：查询ETF产品信息
        self._oes_api_query_etf_req = self._oes_api.OesApi_QueryEtf
        self._oes_api_query_etf_req.restype = c_int32
        self._oes_api_query_etf_req.argtypes = [POINTER(OesApiSessionInfo),
                                                POINTER(OesQryEtfFilter),
                                                self._ON_QRY_RSP_FUNC,
                                                c_void_p]

        # 获取api接口函数：查询ETF成分股信息
        self._oes_api_query_etf_component_req = self._oes_api.OesApi_QueryEtfComponent
        self._oes_api_query_etf_component_req.restype = c_int32
        self._oes_api_query_etf_component_req.argtypes = [POINTER(OesApiSessionInfo),
                                                          POINTER(OesQryEtfComponentFilter),
                                                          self._ON_QRY_RSP_FUNC,
                                                          c_void_p]

        # 查询市场状态信息
        self._oes_api_query_market_state_req = self._oes_api.OesApi_QueryMarketState
        self._oes_api_query_market_state_req.restype = c_int32
        self._oes_api_query_market_state_req.argtypes = [POINTER(OesApiSessionInfo),
                                                         POINTER(OesQryMarketStateFilter),
                                                         self._ON_QRY_RSP_FUNC,
                                                         c_void_p]

        # 查询主柜资金信息
        self._oes_api_query_counter_cash_req = self._oes_api.OesApi_QueryCounterCash
        self._oes_api_query_counter_cash_req.restype = c_int32
        self._oes_api_query_counter_cash_req.argtypes = [POINTER(OesApiSessionInfo),
                                                         c_char_p,
                                                         POINTER(OesCounterCashItem)]

        # 查询券商参数信息
        self._oes_api_query_broker_params_info_req = self._oes_api.OesApi_QueryBrokerParamsInfo
        self._oes_api_query_broker_params_info_req.restype = c_int32
        self._oes_api_query_broker_params_info_req.argtypes = [POINTER(OesApiSessionInfo),
                                                               POINTER(OesBrokerParamsInfo)]

        # 获取api接口函数：查询客户端总览信息
        self._oes_api_get_client_overview_req = self._oes_api.OesApi_GetClientOverview
        self._oes_api_get_client_overview_req.restype = c_int32
        self._oes_api_get_client_overview_req.argtypes = [POINTER(OesApiSessionInfo),
                                                          POINTER(OesClientOverview)]
        # 从成交回报中提取和生成委托回报信息
        self._oes_helper_extract_ord_report_from_trd = self._oes_api.OesHelper_ExtractOrdReportFromTrd
        self._oes_helper_extract_ord_report_from_trd.restype = POINTER(OesOrdCnfm)
        self._oes_helper_extract_ord_report_from_trd.argtypes = [POINTER(OesTrdCnfm),
                                                                 POINTER(OesOrdCnfm)]

        # 查询单条委托信息
        self._oes_api_query_single_order = self._oes_api.OesApi_QuerySingleOrder
        self._oes_api_query_single_order.restype = c_int32
        self._oes_api_query_single_order.argtypes = [POINTER(OesApiSessionInfo),
                                                     c_int32,
                                                     POINTER(OesOrdItem)]

        # 查询单条资金信息
        self._oes_api_query_single_cash_asset = self._oes_api.OesApi_QuerySingleCashAsset
        self._oes_api_query_single_cash_asset.restype = c_int32
        self._oes_api_query_single_cash_asset.argtypes = [POINTER(OesApiSessionInfo),
                                                          c_char_p,
                                                          POINTER(OesCashAssetItem)]

        # 查询单条股票持仓信息
        self._oes_api_query_single_stk_holding = self._oes_api.OesApi_QuerySingleStkHolding
        self._oes_api_query_single_stk_holding.restype = c_int32
        self._oes_api_query_single_stk_holding.argtypes = [POINTER(OesApiSessionInfo),
                                                           c_char_p,
                                                           c_char_p,
                                                           POINTER(OesStkHoldingItem)]

        # 发送回报同步消息
        self._oes_api_send_report_synchronization = self._oes_api.OesApi_SendReportSynchronization
        self._oes_api_send_report_synchronization.restype = c_bool
        self._oes_api_send_report_synchronization.argtypes = [POINTER(OesApiSessionInfo),
                                                              c_int8,
                                                              c_int32,
                                                              c_int64]

        # 发送心跳消息
        self._oes_api_send_heartbeat = self._oes_api.OesApi_SendHeartbeat
        self._oes_api_send_heartbeat.restype = c_bool
        self._oes_api_send_heartbeat.argtypes = [POINTER(OesApiSessionInfo), ]

        # 发送委托通道的测试请求消息
        self._oes_api_test_ord_channel = self._oes_api.OesApi_TestOrdChannel
        self._oes_api_test_ord_channel.restype = c_bool
        self._oes_api_test_ord_channel.argtypes = [POINTER(OesApiSessionInfo),
                                                   c_char_p,
                                                   c_int32]

        # 发送回报通道的测试请求消息
        self._oes_api_test_rpt_channel = self._oes_api.OesApi_TestRptChannel
        self._oes_api_test_rpt_channel.restype = c_bool
        self._oes_api_test_rpt_channel.argtypes = [POINTER(OesApiSessionInfo),
                                                   c_char_p,
                                                   c_int32]

        # 按照默认的配置名称, 完整的初始化客户端环境
        self._oes_api_init_all_by_convention = self._oes_api.OesApi_InitAllByConvention
        self._oes_api_init_all_by_convention.restype = c_bool
        self._oes_api_init_all_by_convention.argtypes = [POINTER(OesApiClientEnv),
                                                         c_char_p,
                                                         c_int64,
                                                         POINTER(c_int32)]

        # 按照配置信息结构体, 初始化客户端环境
        self._oes_api_init_all_by_cfg_struct = self._oes_api.OesApi_InitAllByCfgStruct
        self._oes_api_init_all_by_cfg_struct.restype = c_bool
        self._oes_api_init_all_by_cfg_struct.argtypes = [POINTER(OesApiClientEnv),
                                                         POINTER(OesApiClientCfg),
                                                         c_int64,
                                                         POINTER(c_int32)]

        # 初始化日志记录器
        self._oes_api_init_logger = self._oes_api.OesApi_InitLogger
        self._oes_api_init_logger.restype = c_bool
        self._oes_api_init_logger.argtypes = [c_char_p, c_char_p]

        # 重置线程级别的日志记录器名称
        self._oes_api_reset_thread_logger_name = self._oes_api.OesApi_ResetThreadLoggerName
        self._oes_api_reset_thread_logger_name.restype = c_bool
        self._oes_api_reset_thread_logger_name.argtypes = [c_char_p, ]

        # 初始化委托申报通道 (包括完整的配置解析、连接建立和登录过程)
        self._oes_api_init_ord_channel = self._oes_api.OesApi_InitOrdChannel
        self._oes_api_init_ord_channel.restype = c_bool
        self._oes_api_init_ord_channel.argtypes = [POINTER(OesApiSessionInfo),
                                                   c_char_p,
                                                   c_char_p,
                                                   c_char_p,
                                                   POINTER(c_int32)]

        # 初始化委托申报通道 (包括完整的连接建立和登录过程)
        self._oes_api_init_ord_channel2 = self._oes_api.OesApi_InitOrdChannel2
        self._oes_api_init_ord_channel2.restype = c_bool
        self._oes_api_init_ord_channel2.argtypes = [POINTER(OesApiSessionInfo),
                                                    POINTER(OesApiRemoteCfg),
                                                    POINTER(c_int32)]

        # 初始化回报通道 (包括完整的配置解析、连接建立和登录过程)
        self._oes_api_init_rpt_channel = self._oes_api.OesApi_InitRptChannel
        self._oes_api_init_rpt_channel.restype = c_bool
        self._oes_api_init_rpt_channel.argtypes = [POINTER(OesApiSessionInfo),
                                                   c_char_p,
                                                   c_char_p,
                                                   c_char_p,
                                                   c_int64]

        # 初始化回报通道 (包括完整的连接建立和登录过程)
        self._oes_api_init_rpt_channel2 = self._oes_api.OesApi_InitRptChannel2
        self._oes_api_init_rpt_channel2.restype = c_bool
        self._oes_api_init_rpt_channel2.argtypes = [POINTER(OesApiSessionInfo),
                                                    POINTER(OesApiRemoteCfg),
                                                    POINTER(OesApiSubscribeInfo),
                                                    c_int64]

        # 初始化查询通道 (包括完整的配置解析、连接建立和登录过程)
        self._oes_api_init_qry_channel = self._oes_api.OesApi_InitQryChannel
        self._oes_api_init_qry_channel.restype = c_bool
        self._oes_api_init_qry_channel.argtypes = [POINTER(OesApiSessionInfo),
                                                   c_char_p,
                                                   c_char_p,
                                                   c_char_p]

        # 初始化查询通道 (包括完整的连接建立和登录过程)
        self._oes_api_init_qry_channel2 = self._oes_api.OesApi_InitQryChannel2
        self._oes_api_init_qry_channel2.restype = c_bool
        self._oes_api_init_qry_channel2.argtypes = [POINTER(OesApiSessionInfo),
                                                    POINTER(OesApiRemoteCfg)]

        # 解析服务器地址列表字符串
        self._oes_api_parse_addr_list_string = self._oes_api.OesApi_ParseAddrListString
        self._oes_api_parse_addr_list_string.restype = c_int32
        self._oes_api_parse_addr_list_string.argtypes = [c_char_p,
                                                         POINTER(OesApiAddrInfo),
                                                         c_int32]

        # 从配置文件中解析远程主机配置
        self._oes_api_parse_config_from_file = self._oes_api.OesApi_ParseConfigFromFile
        self._oes_api_parse_config_from_file.restype = c_bool
        self._oes_api_parse_config_from_file.argtypes = [c_char_p,
                                                         c_char_p,
                                                         c_char_p,
                                                         POINTER(OesApiRemoteCfg),
                                                         POINTER(OesApiSubscribeInfo)]

        # 从配置文件中解析远程主机配置, 并可以指定是否允许配置项为空
        self._oes_api_parse_config_from_file2 = self._oes_api.OesApi_ParseConfigFromFile2
        self._oes_api_parse_config_from_file2.restype = c_bool
        self._oes_api_parse_config_from_file2.argtypes = [c_char_p,
                                                          c_char_p,
                                                          c_char_p,
                                                          POINTER(OesApiRemoteCfg),
                                                          POINTER(OesApiSubscribeInfo),
                                                          c_bool]

        # 按照默认的配置名称, 从配置文件中解析所有配置信息
        self._oes_api_parse_all_config = self._oes_api.OesApi_ParseAllConfig
        self._oes_api_parse_all_config.restype = c_bool
        self._oes_api_parse_all_config.argtypes = [c_char_p,
                                                   POINTER(OesApiClientCfg)]

    def oes_api_init_all(self, fileName, lastClSeqNo):
        return self._ufx_init_all(byref(self._clientEnv),
                                  create_string_buffer(fileName.encode(encoding=ENCODE_TYPE)),
                                  create_string_buffer(OESAPI_CFG_DEFAULT_SECTION_LOGGER.encode()),
                                  create_string_buffer(OESAPI_CFG_DEFAULT_SECTION.encode()),
                                  create_string_buffer(OESAPI_CFG_DEFAULT_KEY_ORD_ADDR.encode()),

                                  create_string_buffer(OESAPI_CFG_DEFAULT_KEY_RPT_ADDR.encode()),
                                  create_string_buffer(OESAPI_CFG_DEFAULT_KEY_QRY_ADDR.encode()),

                                  -1,
                                  byref(lastClSeqNo))

    def oes_api_set_user_name(self, username):
        return self._oes_api_set_user_name(create_string_buffer(username.encode()))

    def oes_api_set_passwd(self, passwd):
        return self._oes_api_set_passwd(create_string_buffer(str(passwd).encode()))

    def oes_api_set_env_id(self, env_id):
        return self._oes_api_set_env_id(c_int8(int(env_id)))

    def oes_api_get_env_id(self):
        return self._oes_api_get_env_id()

    # 设置硬盘序列号
    def oes_api_set_customized_driver_id(self, driver_id):
        return self._oes_api_set_customized_driver_id(create_string_buffer(str(driver_id).encode()))

    def oes_api_logout_all(self):
        return self._oes_api_logout_all(byref(self._clientEnv), 1)

    def oes_api_destory_all(self):
        return self._oes_api_destory_all(byref(self._clientEnv))

    # 委托申报
    def oes_api_send_order_req(self, req):
        return self._oes_api_send_order_req(byref(self._clientEnv.ord_channel),
                                            byref(req))

    # 出入金
    def oes_api_send_fund_transfer_req(self, req):
        return self._oes_api_send_fund_transfer_req(byref(self._clientEnv.ord_channel),
                                                    byref(req))

    # 撤单
    def oes_api_send_order_cancell_req(self, req):
        return self._oes_api_send_order_cancell_req(byref(self._clientEnv.ord_channel),
                                                    byref(req))

    # 查询委托
    def oes_api_query_order_req(self, qry_filter, func, user_info=''):
        return self._oes_api_query_order_req(byref(self._clientEnv.qry_channel),
                                             byref(qry_filter),
                                             self._ON_QRY_RSP_FUNC(func),
                                             user_info)

    # 查询客户佣金信息
    def oes_api_query_comms_req(self, qry_filter, func, user_info=''):
        return self._oes_api_query_comms_req(byref(self._clientEnv.qry_channel),
                                             byref(qry_filter),
                                             self._ON_QRY_RSP_FUNC(func),
                                             user_info)

    # 查询现货产品信息
    def oes_api_query_stock_req(self, qry_filter, func, user_info=''):
        return self._oes_api_query_stock_req(byref(self._clientEnv.qry_channel),
                                             byref(qry_filter),
                                             self._ON_QRY_RSP_FUNC(func),
                                             user_info)

    # 查询现货持仓信息
    def oes_api_query_stk_holding_req(self, qry_filter, func, user_info=''):
        return self._oes_api_query_stk_holding_req(byref(self._clientEnv.qry_channel),
                                                   byref(qry_filter),
                                                   self._ON_QRY_RSP_FUNC(func),
                                                   user_info)

    # 查询成交信息
    def oes_api_query_trd_req(self, qry_filter, func, user_info=''):
        return self._oes_api_query_trade_req(byref(self._clientEnv.qry_channel),
                                             byref(qry_filter),
                                             self._ON_QRY_RSP_FUNC(func),
                                             user_info)

    # 查询客户资金信息
    def oes_api_query_cash_asset_req(self, qry_filter, func, user_info=''):
        return self._oes_api_query_cash_asset_req(byref(self._clientEnv.qry_channel),
                                                  byref(qry_filter),
                                                  self._ON_QRY_RSP_FUNC(func),
                                                  user_info)

    # 查询客户信息
    def oes_api_query_cust_info_req(self, qry_filter, func, user_info=''):
        return self._oes_api_query_cust_info_req(byref(self._clientEnv.qry_channel),
                                                 byref(qry_filter),
                                                 self._ON_QRY_RSP_FUNC(func),
                                                 user_info)

    # 查询证券账户信息
    def oes_api_query_inv_acct_req(self, qry_filter, func, user_info=''):
        return self._oes_api_query_inv_acct_req(byref(self._clientEnv.qry_channel),
                                                byref(qry_filter),
                                                self._ON_QRY_RSP_FUNC(func),
                                                user_info)

    # 查询新股中签、配号信息
    def oes_api_query_lot_winning_req(self, qry_filter, func, user_info=''):
        return self._oes_api_query_lot_winning_req(byref(self._clientEnv.qry_channel),
                                                   byref(qry_filter),
                                                   self._ON_QRY_RSP_FUNC(func),
                                                   user_info)

    # 查询证券发行产品信息
    def oes_api_query_issue_req(self, qry_filter, func, user_info=''):
        return self._oes_api_query_issue_req(byref(self._clientEnv.qry_channel),
                                             byref(qry_filter),
                                             self._ON_QRY_RSP_FUNC(func),
                                             user_info
                                             )

    # 查询出入金流水
    def oes_api_query_fund_transfer_serial_req(self, qry_filter, func, user_info=''):
        return self._oes_api_query_fund_transfer_serial_req(byref(self._clientEnv.qry_channel),
                                                            byref(qry_filter),
                                                            self._ON_QRY_RSP_FUNC(func),
                                                            user_info
                                                            )

    # 查询ETF产品信息
    def oes_api_query_etf_req(self, qry_filter, func, user_info=''):
        return self._oes_api_query_etf_req(byref(self._clientEnv.qry_channel),
                                           byref(qry_filter),
                                           self._ON_QRY_RSP_FUNC(func),
                                           user_info
                                           )

    # 查询ETF成分股信息
    def oes_api_query_etf_component_req(self, qry_filter, func, user_info=''):
        return self._oes_api_query_etf_component_req(byref(self._clientEnv.qry_channel),
                                                     byref(qry_filter),
                                                     self._ON_QRY_RSP_FUNC(func),
                                                     user_info
                                                     )

    # 查询客户端总览信息
    def oes_api_query_client_overview_req(self, overview, func, user_info=''):
        # count = ctypes.sizeof(overview)
        # print('count', count)
        # memset(byref(overview), 0x0, count)
        ret_code = self._oes_api_get_client_overview_req(byref(self._clientEnv.qry_channel),
                                                         byref(overview))
        if ret_code >= 0:
            func(overview, user_info)
        return ret_code

    # 获取错误信息
    def oes_api_get_error_msg(self, error_no):
        return self._oes_api_get_error_msg(error_no)

    # 收取回报数据

    def oes_api_wait_rpt_msg(self, func, time_out=1000, user_info=''):
        return self._oes_api_wait_report_msg(byref(self._clientEnv.rpt_channel),
                                             time_out,
                                             self._ON_RPT_MSG_FUNC(func),
                                             user_info)

    # 获取通道最新接受消息时间
    def oes_api_get_last_recv_time(self, channel_type):
        if channel_type == "ord":
            channel = byref(self._clientEnv.ord_channel)

        elif channel_type == "rpt":
            channel = byref(self._clientEnv.rpt_channel)

        else:
            channel = byref(self._clientEnv.qry_channel)
        return self._oes_api_get_last_recv_time(channel)

    def oes_helper_extract_ord_report_from_trd(self, trd_cnfm, ord_cnfm):
        return self._oes_helper_extract_ord_report_from_trd(pointer(trd_cnfm),
                                                            pointer(ord_cnfm))

    def oes_api_logon(self, p_out_session_info, channel_type, uri, username, password, cl_env_id,
                      heart_bt_int, p_socket_options):
        return self._oes_api_logon(p_out_session_info, channel_type, uri, username, password,
                                   cl_env_id, heart_bt_int, p_socket_options)

    def oes_api_logout(self, p_session_info):
        return self._oes_api_logout(p_session_info, 1)

    def oes_api_destory(self, p_session_info):
        return self._oes_api_destory(p_session_info)

    def oes_api_get_thread_username(self):
        return self._oes_api_get_thread_username()

    def oes_api_set_thread_subscribe_env_id(self, subscribe_env_id):
        return self._oes_api_set_thread_subscribe_env_id(subscribe_env_id)

    def oes_api_get_thread_subscribe_env_id(self):
        return self._oes_api_get_thread_subscribe_env_id()

    def oes_api_set_customized_ip_and_mac(self, ip_str, mac_str):
        return self._oes_api_set_customized_ip_and_mac(ip_str, mac_str)

    def oes_api_set_customized_ip(self, ip_str):
        return self._oes_api_set_customized_ip(ip_str)

    def oes_api_set_customized_mac(self, mac_str):
        return self._oes_api_set_customized_mac(mac_str)

    def oes_api_get_customized_ip(self):
        return self._oes_api_get_customized_ip()

    def oes_api_get_customized_mac(self):
        return self._oes_api_get_customized_mac()

    def oes_api_get_customized_driver_id(self):
        return self._oes_api_get_customized_driver_id()

    def oes_api_get_cl_env_id(self, p_session_info):
        return self._oes_api_get_cl_env_id(p_session_info)

    def oes_api_recv_report_msg(self, p_out_msg_head, p_out_msg_body, buf_size, timeout_ms):
        return self._oes_api_recv_report_msg(byref(self._clientEnv.rpt_channel),
                                             p_out_msg_head,
                                             p_out_msg_body,
                                             buf_size,
                                             timeout_ms)

    def oes_api_get_api_version(self):
        return self._oes_api_get_api_version()

    def oes_api_get_trading_day(self):
        return self._oes_api_get_trading_day(byref(self._clientEnv.qry_channel))

    def oes_api_get_last_send_time(self, p_session_info):
        return self._oes_api_get_last_send_time(p_session_info)

    def oes_api_has_more_cached_data(self):
        return self._oes_api_has_more_cached_data(byref(self._clientEnv.rpt_channel))

    def oes_api_is_valid_ord_channel(self):
        return self._oes_api_is_valid_ord_channel(byref(self._clientEnv.ord_channel))

    def oes_api_is_valid_rpt_channel(self):
        return self._oes_api_is_valid_rpt_channel(byref(self._clientEnv.rpt_channel))

    def oes_api_is_valid_qry_channel(self):
        return self._oes_api_is_valid_qry_channel(byref(self._clientEnv.qry_channel))

    def oes_api_get_last_error(self):
        return self._oes_api_get_last_error()

    def oes_api_set_last_error(self, err_code):
        return self._oes_api_set_last_error(err_code)

    def oes_api_get_error_msg2(self, status, detail_status):
        return self._oes_api_get_error_msg2(status, detail_status)

    def oes_api_has_stock_status(self, p_stock_item, status):
        return self._oes_api_has_stock_status(p_stock_item, status)

    def oes_api_send_batch_orders_req(self, pp_ord_ptr_list, ord_count):
        return self._oes_api_send_batch_orders_req(byref(self._clientEnv.ord_channel),
                                                   pp_ord_ptr_list,
                                                   ord_count)

    def oes_api_send_batch_orders_req2(self, p_ord_req_array, ord_count):
        return self._oes_api_send_batch_orders_req2(byref(self._clientEnv.ord_channel),
                                                    p_ord_req_array,
                                                    ord_count)

    def oes_api_query_market_state_req(self, p_qry_filter, func, p_callback_params):
        return self._oes_api_query_market_state_req(byref(self._clientEnv.qry_channel),
                                                    p_qry_filter,
                                                    self._ON_QRY_RSP_FUNC(func),
                                                    p_callback_params)

    def oes_api_query_counter_cash_req(self, cash_acct_id, p_counter_cash_item):
        return self._oes_api_query_counter_cash_req(byref(self._clientEnv.qry_channel),
                                                    cash_acct_id,
                                                    p_counter_cash_item)

    def oes_api_query_broker_params_info_req(self, p_broker_params):
        return self._oes_api_query_broker_params_info_req(byref(self._clientEnv.qry_channel),
                                                          p_broker_params)

    def oes_api_query_single_order(self, cl_seq_no, p_ord_item):
        return self._oes_api_query_single_order(byref(self._clientEnv.qry_channel),
                                                cl_seq_no,
                                                p_ord_item)

    def oes_api_query_single_cash_asset(self, cash_acct_id, p_cash_asset_item):
        return self._oes_api_query_single_cash_asset(byref(self._clientEnv.qry_channel),
                                                     cash_acct_id,
                                                     p_cash_asset_item)

    def oes_api_query_single_stk_holding(self, inv_acct_id, security_id, p_holding_item):
        return self._oes_api_query_single_stk_holding(byref(self._clientEnv.qry_channel),
                                                      inv_acct_id,
                                                      security_id,
                                                      p_holding_item)

    def oes_api_send_report_synchronization(self, subscribe_env_id, subscribe_rpt_types, last_rpt_seq_num):
        return self._oes_api_send_report_synchronization(byref(self._clientEnv.rpt_channel),
                                                         subscribe_env_id,
                                                         subscribe_rpt_types,
                                                         last_rpt_seq_num)

    def oes_api_send_heartbeat(self, p_session_info):
        return self._oes_api_send_heartbeat(p_session_info)

    def oes_api_test_ord_channel(self, test_req_id, test_req_id_size):
        return self._oes_api_test_ord_channel(byref(self._clientEnv.ord_channel),
                                              test_req_id,
                                              test_req_id_size)

    def oes_api_test_rpt_channel(self, test_req_id, test_req_id_size):
        return self._oes_api_test_rpt_channel(byref(self._clientEnv.rpt_channel),
                                              test_req_id,
                                              test_req_id_size)

    def oes_api_init_all_by_convention(self, cfg_file, last_rpt_seq_num, p_last_cl_seq_no):
        return self._oes_api_init_all_by_convention(byref(self._clientEnv),
                                                    cfg_file,
                                                    last_rpt_seq_num,
                                                    p_last_cl_seq_no)

    def oes_api_init_all_by_cfg_struct(self, p_client_cfg, last_rpt_seq_num, p_last_cl_seq_no):
        return self._oes_api_init_all_by_cfg_struct(byref(self._clientEnv),
                                                    p_client_cfg,
                                                    last_rpt_seq_num,
                                                    p_last_cl_seq_no)

    def oes_api_init_logger(self, cfg_file, logger_section):
        return self._oes_api_init_logger(cfg_file, logger_section)

    def oes_api_reset_thread_logger_name(self, log_system_name):
        return self._oes_api_reset_thread_logger_name(log_system_name)

    def oes_api_init_ord_channel(self, cfg_file, cfg_section, addr_key, p_last_cl_seq_no):
        return self._oes_api_init_ord_channel(byref(self._clientEnv.ord_channel),
                                              cfg_file,
                                              cfg_section,
                                              addr_key,
                                              p_last_cl_seq_no)

    def oes_api_init_ord_channel2(self, p_remote_cfg, p_last_cl_seq_no):
        return self._oes_api_init_ord_channel2(byref(self._clientEnv.ord_channel),
                                               p_remote_cfg,
                                               p_last_cl_seq_no)

    def oes_api_init_rpt_channel(self, cfg_file, cfg_section, addr_key, last_rpt_seq_num):
        return self._oes_api_init_rpt_channel(byref(self._clientEnv.rpt_channel),
                                              cfg_file,
                                              cfg_section,
                                              addr_key,
                                              last_rpt_seq_num)

    def oes_api_init_rpt_channel2(self, p_remote_cfg, p_subscribe_info, last_rpt_seq_num):
        return self._oes_api_init_rpt_channel2(byref(self._clientEnv.rpt_channel),
                                               p_remote_cfg,
                                               p_subscribe_info,
                                               last_rpt_seq_num)

    def oes_api_init_qry_channel(self, cfg_file, cfg_section, addr_key):
        return self._oes_api_init_qry_channel(byref(self._clientEnv.qry_channel),
                                              cfg_file,
                                              cfg_section,
                                              addr_key)

    def oes_api_init_qry_channel2(self, p_remote_cfg):
        return self._oes_api_init_qry_channel2(byref(self._clientEnv.qry_channel),
                                               p_remote_cfg)

    def oes_api_parse_addr_list_string(self, uri_list, p_out_addr_list, addr_list_length):
        return self._oes_api_parse_addr_list_string(uri_list, p_out_addr_list, addr_list_length)

    def oes_api_parse_config_from_file(self, cfg_file, section, addr_key, p_out_remote_cfg, p_out_subscribe_info):
        return self._oes_api_parse_config_from_file(cfg_file,
                                                    section,
                                                    addr_key,
                                                    p_out_remote_cfg,
                                                    p_out_subscribe_info)

    def oes_api_parse_config_from_file2(self, cfg_file, section, addr_key, p_out_remote_cfg, p_out_subscribe_info,
                                        is_required_cfg):
        return self._oes_api_parse_config_from_file2(cfg_file,
                                                     section,
                                                     addr_key,
                                                     p_out_remote_cfg,
                                                     p_out_subscribe_info,
                                                     is_required_cfg)

    def oes_api_parse_all_config(self, cfg_file, p_out_api_cfg):
        return self._oes_api_parse_all_config(cfg_file, p_out_api_cfg)

