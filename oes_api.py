# -*- coding: utf-8 -*-
from ctypes import CDLL, CFUNCTYPE, POINTER
from ctypes import byref, create_string_buffer
from ctypes import c_char, c_char_p, c_void_p
from ctypes import c_int, c_int8, c_int16, c_int32, c_int64
from ctypes import c_uint8, c_uint16, c_uint32, c_uint64
from oes_struct import *


class OesApi(object):
    def __init__(self, libname):
        self.api = CDLL(libname)
        self.client_env = OesApiClientEnvT()
        self.ord_channel = self.client_env.ordChannel
        self.rpt_channel = self.client_env.rptChannel
        self.qry_channel = self.client_env.qryChannel

        # 对接收到的应答或回报消息进行处理的回调函数的函数原型定义
        # pSessionInfo, pMsgHead, pMsgItem, pCallbackParams
        self.F_OESAPI_ON_RPT_MSG_T = CFUNCTYPE(c_int32,
                                               POINTER(OesApiSessionInfoT),
                                               POINTER(SMsgHeadT),
                                               c_void_p,
                                               c_void_p)

        # 对查询结果进行处理的回调函数的函数原型定义
        # pQryChannel, pMsgHead, pMsgItem, pQryCursor, pCallbackParams
        self.F_OESAPI_ON_QRY_MSG_T = CFUNCTYPE(c_int32,
                                               POINTER(OesApiSessionInfoT),
                                               POINTER(SMsgHeadT),
                                               c_void_p,
                                               POINTER(OesQryCursorT),
                                               c_void_p)

        # 发送委托申报请求
        self._OesApi_SendOrderReq = self.api.OesApi_SendOrderReq
        self._OesApi_SendOrderReq.restype = c_int32
        self._OesApi_SendOrderReq.argtypes = [POINTER(OesApiSessionInfoT),
                                              POINTER(OesOrdReqT)]

        # 发送撤单请求
        self._OesApi_SendOrderCancelReq = self.api.OesApi_SendOrderCancelReq
        self._OesApi_SendOrderCancelReq.restype = c_int32
        self._OesApi_SendOrderCancelReq.argtypes = [POINTER(OesApiSessionInfoT),
                                                    POINTER(OesOrdCancelReqT)]

        # 批量发送多条委托请求
        self._OesApi_SendBatchOrdersReq2 = self.api.OesApi_SendBatchOrdersReq2
        self._OesApi_SendBatchOrdersReq2.restype = c_int32
        self._OesApi_SendBatchOrdersReq2.argtypes = [POINTER(OesApiSessionInfoT),
                                                     POINTER(OesOrdReqT),
                                                     c_int32]

        # 发送出入金委托请求
        self._OesApi_SendFundTransferReq = self.api.OesApi_SendFundTransferReq
        self._OesApi_SendFundTransferReq.restype = c_int32
        self._OesApi_SendFundTransferReq.argtypes = [POINTER(OesApiSessionInfoT),
                                                     POINTER(OesFundTrsfReqT)]

        # 等待回报消息到达, 并通过回调函数进行消息处理
        self._OesApi_WaitReportMsg = self.api.OesApi_WaitReportMsg
        self._OesApi_WaitReportMsg.restype = c_int32
        self._OesApi_WaitReportMsg.argtypes = [POINTER(OesApiSessionInfoT),
                                               c_int32,
                                               self.F_OESAPI_ON_RPT_MSG_T,
                                               c_void_p]

        # 接收(一条)回报消息
        self._OesApi_RecvReportMsg = self.api.OesApi_RecvReportMsg
        self._OesApi_RecvReportMsg.restype = c_int32
        self._OesApi_RecvReportMsg.argtypes = [POINTER(OesApiSessionInfoT),
                                               POINTER(SMsgHeadT),
                                               POINTER(OesRspMsgBodyT),
                                               c_int32,
                                               c_int32]

        # 获取API的发行版本号
        self._OesApi_GetApiVersion = self.api.OesApi_GetApiVersion
        self._OesApi_GetApiVersion.restype = c_char_p
        self._OesApi_GetApiVersion.argtypes = []

        # 获取当前交易日
        self._OesApi_GetTradingDay = self.api.OesApi_GetTradingDay
        self._OesApi_GetTradingDay.restype = c_int32
        self._OesApi_GetTradingDay.argtypes = [POINTER(OesApiSessionInfoT)]

        # 获取客户端总览信息
        self._OesApi_GetClientOverview = self.api.OesApi_GetClientOverview
        self._OesApi_GetClientOverview.restype = c_int32
        self._OesApi_GetClientOverview.argtypes = [POINTER(OesApiSessionInfoT),
                                                   POINTER(OesClientOverviewT)]

        # 查询单条资金资产信息
        self._OesApi_QuerySingleCashAsset = self.api.OesApi_QuerySingleCashAsset
        self._OesApi_QuerySingleCashAsset.restype = c_int32
        self._OesApi_QuerySingleCashAsset.argtypes = [POINTER(OesApiSessionInfoT),
                                                      c_char_p,
                                                      POINTER(OesCashAssetItemT)]

        # 查询单条股票持仓信息
        self._OesApi_QuerySingleStkHolding = self.api.OesApi_QuerySingleStkHolding
        self._OesApi_QuerySingleStkHolding.restype = c_int32
        self._OesApi_QuerySingleStkHolding.argtypes = [POINTER(OesApiSessionInfoT),
                                                       c_char_p,
                                                       c_char_p,
                                                       POINTER(OesStkHoldingItemT)]

        # 查询单条委托信息
        self._OesApi_QuerySingleOrder = self.api.OesApi_QuerySingleOrder
        self._OesApi_QuerySingleOrder.restype = c_int32
        self._OesApi_QuerySingleOrder.argtypes = [POINTER(OesApiSessionInfoT),
                                                  c_int32,
                                                  POINTER(OesOrdItemT)]

        # 查询所有委托信息
        self._OesApi_QueryOrder = self.api.OesApi_QueryOrder
        self._OesApi_QueryOrder.restype = c_int32
        self._OesApi_QueryOrder.argtypes = [POINTER(OesApiSessionInfoT),
                                            POINTER(OesQryOrdFilterT),
                                            self.F_OESAPI_ON_QRY_MSG_T,
                                            c_void_p]

        # 查询成交信息
        self._OesApi_QueryTrade = self.api.OesApi_QueryTrade
        self._OesApi_QueryTrade.restype = c_int32
        self._OesApi_QueryTrade.argtypes = [POINTER(OesApiSessionInfoT),
                                            POINTER(OesQryTrdFilterT),
                                            self.F_OESAPI_ON_QRY_MSG_T,
                                            c_void_p]

        # 查询客户资金信息
        self._OesApi_QueryCashAsset = self.api.OesApi_QueryCashAsset
        self._OesApi_QueryCashAsset.restype = c_int32
        self._OesApi_QueryCashAsset.argtypes = [POINTER(OesApiSessionInfoT),
                                                POINTER(OesQryCashAssetFilterT),
                                                self.F_OESAPI_ON_QRY_MSG_T,
                                                c_void_p]

        # 查询股票持仓信息
        self._OesApi_QueryStkHolding = self.api.OesApi_QueryStkHolding
        self._OesApi_QueryStkHolding.restype = c_int32
        self._OesApi_QueryStkHolding.argtypes = [POINTER(OesApiSessionInfoT),
                                                 POINTER(OesQryStkHoldingFilterT),
                                                 self.F_OESAPI_ON_QRY_MSG_T,
                                                 c_void_p]

        # 查询新股配号、中签信息
        self._OesApi_QueryLotWinning = self.api.OesApi_QueryLotWinning
        self._OesApi_QueryLotWinning.restype = c_int32
        self._OesApi_QueryLotWinning.argtypes = [POINTER(OesApiSessionInfoT),
                                                 POINTER(OesQryLotWinningFilterT),
                                                 self.F_OESAPI_ON_QRY_MSG_T,
                                                 c_void_p]

        # 查询客户信息
        self._OesApi_QueryCustInfo = self.api.OesApi_QueryCustInfo
        self._OesApi_QueryCustInfo.restype = c_int32
        self._OesApi_QueryCustInfo.argtypes = [POINTER(OesApiSessionInfoT),
                                               POINTER(OesQryCustFilterT),
                                               self.F_OESAPI_ON_QRY_MSG_T,
                                               c_void_p]

        # 查询证券账户信息
        self._OesApi_QueryInvAcct = self.api.OesApi_QueryInvAcct
        self._OesApi_QueryInvAcct.restype = c_int32
        self._OesApi_QueryInvAcct.argtypes = [POINTER(OesApiSessionInfoT),
                                              POINTER(OesQryInvAcctFilterT),
                                              self.F_OESAPI_ON_QRY_MSG_T,
                                              c_void_p]

        # 查询佣金信息
        self._OesApi_QueryCommissionRate = self.api.OesApi_QueryCommissionRate
        self._OesApi_QueryCommissionRate.restype = c_int32
        self._OesApi_QueryCommissionRate.argtypes = [POINTER(OesApiSessionInfoT),
                                                     POINTER(OesQryCommissionRateFilterT),
                                                     self.F_OESAPI_ON_QRY_MSG_T,
                                                     c_void_p]

        # 查询出入金流水
        self._OesApi_QueryFundTransferSerial = self.api.OesApi_QueryFundTransferSerial
        self._OesApi_QueryFundTransferSerial.restype = c_int32
        self._OesApi_QueryFundTransferSerial.argtypes = [POINTER(OesApiSessionInfoT),
                                                         POINTER(OesQryFundTransferSerialFilterT),
                                                         self.F_OESAPI_ON_QRY_MSG_T,
                                                         c_void_p]

        # 查询证券发行产品信息
        self._OesApi_QueryIssue = self.api.OesApi_QueryIssue
        self._OesApi_QueryIssue.restype = c_int32
        self._OesApi_QueryIssue.argtypes = [POINTER(OesApiSessionInfoT),
                                            POINTER(OesQryIssueFilterT),
                                            self.F_OESAPI_ON_QRY_MSG_T,
                                            c_void_p]

        # 查询现货产品信息
        self._OesApi_QueryStock = self.api.OesApi_QueryStock
        self._OesApi_QueryStock.restype = c_int32
        self._OesApi_QueryStock.argtypes = [POINTER(OesApiSessionInfoT),
                                            POINTER(OesQryStockFilterT),
                                            self.F_OESAPI_ON_QRY_MSG_T,
                                            c_void_p]

        # 查询ETF申赎产品信息
        self._OesApi_QueryEtf = self.api.OesApi_QueryEtf
        self._OesApi_QueryEtf.restype = c_int32
        self._OesApi_QueryEtf.argtypes = [POINTER(OesApiSessionInfoT),
                                          POINTER(OesQryEtfFilterT),
                                          self.F_OESAPI_ON_QRY_MSG_T,
                                          c_void_p]

        # 查询ETF成份证券信息
        self._OesApi_QueryEtfComponent = self.api.OesApi_QueryEtfComponent
        self._OesApi_QueryEtfComponent.restype = c_int32
        self._OesApi_QueryEtfComponent.argtypes = [POINTER(OesApiSessionInfoT),
                                                   POINTER(OesQryEtfComponentFilterT),
                                                   self.F_OESAPI_ON_QRY_MSG_T,
                                                   c_void_p]

        # 查询市场状态信息
        self._OesApi_QueryMarketState = self.api.OesApi_QueryMarketState
        self._OesApi_QueryMarketState.restype = c_int32
        self._OesApi_QueryMarketState.argtypes = [POINTER(OesApiSessionInfoT),
                                                  POINTER(OesQryMarketStateFilterT),
                                                  self.F_OESAPI_ON_QRY_MSG_T,
                                                  c_void_p]

        # 查询主柜资金信息
        self._OesApi_QueryCounterCash = self.api.OesApi_QueryCounterCash
        self._OesApi_QueryCounterCash.restype = c_int32
        self._OesApi_QueryCounterCash.argtypes = [POINTER(OesApiSessionInfoT),
                                                  c_char_p,
                                                  POINTER(OesCounterCashItemT)]

        # 查询券商参数信息
        self._OesApi_QueryBrokerParamsInfo = self.api.OesApi_QueryBrokerParamsInfo
        self._OesApi_QueryBrokerParamsInfo.restype = c_int32
        self._OesApi_QueryBrokerParamsInfo.argtypes = [POINTER(OesApiSessionInfoT),
                                                       POINTER(OesBrokerParamsInfoT)]

        # 发送回报同步消息
        self._OesApi_SendReportSynchronization = self.api.OesApi_SendReportSynchronization
        self._OesApi_SendReportSynchronization.restype = c_int
        self._OesApi_SendReportSynchronization.argtypes = [POINTER(OesApiSessionInfoT),
                                                           c_int8,
                                                           c_int32,
                                                           c_int64]

        # 完整的初始化客户端环境
        self._OesApi_InitAll = self.api.OesApi_InitAll
        self._OesApi_InitAll.restype = c_int
        self._OesApi_InitAll.argtypes = [POINTER(OesApiClientEnvT),
                                         c_char_p,
                                         c_char_p,
                                         c_char_p,
                                         c_char_p,
                                         c_char_p,
                                         c_char_p,
                                         c_int64,
                                         POINTER(c_int32)]

        # 注销并关闭所有的客户端会话
        self._OesApi_LogoutAll = self.api.OesApi_LogoutAll
        self._OesApi_LogoutAll.argtypes = [POINTER(OesApiClientEnvT),
                                           c_int]

        # 直接断开与服务器的连接并释放会话数据
        self._OesApi_DestoryAll = self.api.OesApi_DestoryAll
        self._OesApi_DestoryAll.argtypes = [POINTER(OesApiClientEnvT)]

        # 设置当前线程登录OES时使用的登录用户名
        self._OesApi_SetThreadUsername = self.api.OesApi_SetThreadUsername
        self._OesApi_SetThreadUsername.argtypes = [c_char_p]

        # 返回当前线程登录OES时使用的登录用户名
        self._OesApi_GetThreadUsername = self.api.OesApi_GetThreadUsername
        self._OesApi_GetThreadUsername.restype = c_char_p
        self._OesApi_GetThreadUsername.argtypes = []

        # 设置当前线程登录OES时使用的登录密码
        self._OesApi_SetThreadPassword = self.api.OesApi_SetThreadPassword
        self._OesApi_SetThreadPassword.argtypes = [c_char_p]

        # 设置当前线程登录OES时使用的客户端环境号
        self._OesApi_SetThreadEnvId = self.api.OesApi_SetThreadEnvId
        self._OesApi_SetThreadEnvId.argtypes = [c_int8]

        # 返回当前线程登录OES时使用的客户端环境号
        self._OesApi_GetThreadEnvId = self.api.OesApi_GetThreadEnvId
        self._OesApi_GetThreadEnvId.restype = c_int8
        self._OesApi_GetThreadEnvId.argtypes = []

        # 设置当前线程订阅回报时待订阅的客户端环境号
        self._OesApi_SetThreadSubscribeEnvId = self.api.OesApi_SetThreadSubscribeEnvId
        self._OesApi_SetThreadSubscribeEnvId.argtypes = [c_int8]

        # 返回当前线程订阅回报时待订阅的客户端环境号
        self._OesApi_GetThreadSubscribeEnvId = self.api.OesApi_GetThreadSubscribeEnvId
        self._OesApi_GetThreadSubscribeEnvId.restype = c_int8
        self._OesApi_GetThreadSubscribeEnvId.argtypes = []

        # 设置当前线程登录OES时所期望对接的业务类型
        self._OesApi_SetThreadBusinessType = self.api.OesApi_SetThreadBusinessType
        self._OesApi_SetThreadBusinessType.argtypes = [c_int32]

        # 返回当前线程登录OES时所期望对接的业务类型
        self._OesApi_GetThreadBusinessType = self.api.OesApi_GetThreadBusinessType
        self._OesApi_GetThreadBusinessType.restype = c_int32
        self._OesApi_GetThreadBusinessType.argtypes = []

        # 设置客户端自定义的本地IP和MAC
        self._OesApi_SetCustomizedIpAndMac = self.api.OesApi_SetCustomizedIpAndMac
        self._OesApi_SetCustomizedIpAndMac.restype = c_int
        self._OesApi_SetCustomizedIpAndMac.argtypes = [c_char_p,
                                                       c_char_p]

        # 设置客户端自定义的本地IP地址
        self._OesApi_SetCustomizedIp = self.api.OesApi_SetCustomizedIp
        self._OesApi_SetCustomizedIp.restype = c_int
        self._OesApi_SetCustomizedIp.argtypes = [c_char_p]

        # 获取客户端自定义的本地IP
        self._OesApi_GetCustomizedIp = self.api.OesApi_GetCustomizedIp
        self._OesApi_GetCustomizedIp.restype = c_char_p
        self._OesApi_GetCustomizedIp.argtypes = []

        # 设置客户端自定义的本地MAC地址
        self._OesApi_SetCustomizedMac = self.api.OesApi_SetCustomizedMac
        self._OesApi_SetCustomizedMac.restype = c_int
        self._OesApi_SetCustomizedMac.argtypes = [c_char_p]

        # 获取客户端自定义的本地MAC
        self._OesApi_GetCustomizedMac = self.api.OesApi_GetCustomizedMac
        self._OesApi_GetCustomizedMac.restype = c_char_p
        self._OesApi_GetCustomizedMac.argtypes = []

        # 设置客户端自定义的本地设备序列号
        self._OesApi_SetCustomizedDriverId = self.api.OesApi_SetCustomizedDriverId
        self._OesApi_SetCustomizedDriverId.restype = c_int
        self._OesApi_SetCustomizedDriverId.argtypes = [c_char_p]

        # 获取客户端自定义的本地设备序列号
        self._OesApi_GetCustomizedDriverId = self.api.OesApi_GetCustomizedDriverId
        self._OesApi_GetCustomizedDriverId.restype = c_char_p
        self._OesApi_GetCustomizedDriverId.argtypes = []

        # 返回通道对应的客户端编号 (clientId)
        self._OesApi_GetClientId = self.api.OesApi_GetClientId
        self._OesApi_GetClientId.restype = c_int16
        self._OesApi_GetClientId.argtypes = [POINTER(OesApiSessionInfoT)]

        # 返回通道对应的客户端环境号 (clEnvId)
        self._OesApi_GetClEnvId = self.api.OesApi_GetClEnvId
        self._OesApi_GetClEnvId.restype = c_int8
        self._OesApi_GetClEnvId.argtypes = [POINTER(OesApiSessionInfoT)]

        # 返回通道对应的业务类型
        self._OesApi_GetBusinessType = self.api.OesApi_GetBusinessType
        self._OesApi_GetBusinessType.restype = c_uint32
        self._OesApi_GetBusinessType.argtypes = [POINTER(OesApiSessionInfoT)]

        # 返回系统是否支持指定的业务类别
        self._OesApi_IsBusinessSupported = self.api.OesApi_IsBusinessSupported
        self._OesApi_IsBusinessSupported.restype = c_int
        self._OesApi_IsBusinessSupported.argtypes = [POINTER(OesApiSessionInfoT),
                                                     c_uint32]

        # 获取客户端类型
        self._OesApi_GetClientType = self.api.OesApi_GetClientType
        self._OesApi_GetClientType.restype = c_uint8
        self._OesApi_GetClientType.argtypes = [POINTER(OesApiSessionInfoT)]

        # 获取客户端状态
        self._OesApi_GetClientStatus = self.api.OesApi_GetClientStatus
        self._OesApi_GetClientStatus.restype = c_uint8
        self._OesApi_GetClientStatus.argtypes = [POINTER(OesApiSessionInfoT)]

        # 获取通道最近接收消息时间
        self._OesApi_GetLastRecvTime = self.api.OesApi_GetLastRecvTime
        self._OesApi_GetLastRecvTime.restype = c_int64
        self._OesApi_GetLastRecvTime.argtypes = [POINTER(OesApiSessionInfoT)]

        # 获取通道最近发送消息时间
        self._OesApi_GetLastSendTime = self.api.OesApi_GetLastSendTime
        self._OesApi_GetLastSendTime.restype = c_int64
        self._OesApi_GetLastSendTime.argtypes = [POINTER(OesApiSessionInfoT)]

        # 返回回报通道是否还有更多已接收但尚未回调处理完成的数据
        self._OesApi_HasMoreCachedData = self.api.OesApi_HasMoreCachedData
        self._OesApi_HasMoreCachedData.restype = c_int32
        self._OesApi_HasMoreCachedData.argtypes = [POINTER(OesApiSessionInfoT)]

        # 返回委托申报通道是否已经连接且有效
        self._OesApi_IsValidOrdChannel = self.api.OesApi_IsValidOrdChannel
        self._OesApi_IsValidOrdChannel.restype = c_int
        self._OesApi_IsValidOrdChannel.argtypes = [POINTER(OesApiSessionInfoT)]

        # 返回回报通道是否已经连接且有效
        self._OesApi_IsValidRptChannel = self.api.OesApi_IsValidRptChannel
        self._OesApi_IsValidRptChannel.restype = c_int
        self._OesApi_IsValidRptChannel.argtypes = [POINTER(OesApiSessionInfoT)]

        # 返回查询通道是否已经连接且有效
        self._OesApi_IsValidQryChannel = self.api.OesApi_IsValidQryChannel
        self._OesApi_IsValidQryChannel.restype = c_int
        self._OesApi_IsValidQryChannel.argtypes = [POINTER(OesApiSessionInfoT)]

        # 返回当前线程最近一次API调用失败的错误号
        self._OesApi_GetLastError = self.api.OesApi_GetLastError
        self._OesApi_GetLastError.restype = c_int32
        self._OesApi_GetLastError.argtypes = []

        # 设置当前线程的API错误号
        self._OesApi_SetLastError = self.api.OesApi_SetLastError
        self._OesApi_SetLastError.argtypes = [c_int32]

        # 返回错误号对应的错误信息
        self._OesApi_GetErrorMsg = self.api.OesApi_GetErrorMsg
        self._OesApi_GetErrorMsg.restype = c_char_p
        self._OesApi_GetErrorMsg.argtypes = [c_int32]

        # 返回消息头中的状态码所对应的错误信息
        self._OesApi_GetErrorMsg2 = self.api.OesApi_GetErrorMsg2
        self._OesApi_GetErrorMsg2.restype = c_char_p
        self._OesApi_GetErrorMsg2.argtypes = [c_uint8,
                                              c_uint8]

        # 返回现货产品是否具有指定状态
        self._OesApi_HasStockStatus = self.api.OesApi_HasStockStatus
        self._OesApi_HasStockStatus.restype = c_int
        self._OesApi_HasStockStatus.argtypes = [POINTER(OesStockItemT),
                                                c_uint32]

        # 从成交回报中提取和生成委托回报信息
        self._OesHelper_ExtractOrdReportFromTrd = self.api.OesHelper_ExtractOrdReportFromTrd
        self._OesHelper_ExtractOrdReportFromTrd.restype = POINTER(OesOrdCnfmT)
        self._OesHelper_ExtractOrdReportFromTrd.argtypes = [POINTER(OesTrdCnfmT),
                                                            POINTER(OesOrdCnfmT)]

    def OesApi_SendOrderReq(self, ord_req):
        """发送委托申报请求"""
        return self._OesApi_SendOrderReq(byref(self.ord_channel),
                                         None if ord_req is None else byref(ord_req))

    def OesApi_SendOrderCancelReq(self, cancel_req):
        """发送撤单请求"""
        return self._OesApi_SendOrderCancelReq(byref(self.ord_channel),
                                               None if cancel_req is None else byref(cancel_req))

    def OesApi_SendBatchOrdersReq2(self, ord_req_array, ord_count):
        """批量发送多条委托请求"""
        return self._OesApi_SendBatchOrdersReq2(byref(self.ord_channel),
                                                None if ord_req_array is None else byref(ord_req_array),
                                                c_int32(ord_count))

    def OesApi_SendFundTransferReq(self, fund_trsf_req):
        """发送出入金委托请求"""
        return self._OesApi_SendFundTransferReq(byref(self.ord_channel),
                                                None if fund_trsf_req is None else byref(fund_trsf_req))

    def OesApi_WaitReportMsg(self, timeout_ms, fn_on_msg_callback, callback_params):
        """等待回报消息到达, 并通过回调函数进行消息处理"""
        return self._OesApi_WaitReportMsg(byref(self.rpt_channel),
                                          c_int32(timeout_ms),
                                          self.F_OESAPI_ON_RPT_MSG_T(fn_on_msg_callback),
                                          None if callback_params is None else byref(callback_params))

    def OesApi_RecvReportMsg(self, out_msg_head, out_msg_body, buf_size, timeout_ms):
        """接收(一条)回报消息"""
        return self._OesApi_RecvReportMsg(byref(self.rpt_channel),
                                          None if out_msg_head is None else byref(out_msg_head),
                                          None if out_msg_body is None else byref(out_msg_body),
                                          c_int32(buf_size),
                                          c_int32(timeout_ms))

    def OesApi_GetApiVersion(self):
        """获取API的发行版本号"""
        return self._OesApi_GetApiVersion().decode()

    def OesApi_GetTradingDay(self):
        """获取当前交易日"""
        return self._OesApi_GetTradingDay(byref(self.qry_channel))

    def OesApi_GetClientOverview(self, out_client_overview):
        """获取客户端总览信息"""
        return self._OesApi_GetClientOverview(byref(self.qry_channel),
                                              None if out_client_overview is None else byref(out_client_overview))

    def OesApi_QuerySingleCashAsset(self, cash_acct_id, out_cash_asset_item):
        """查询单条资金资产信息"""
        return self._OesApi_QuerySingleCashAsset(byref(self.qry_channel),
                                                 None if cash_acct_id is None else create_string_buffer(cash_acct_id.encode()),
                                                 None if out_cash_asset_item is None else byref(out_cash_asset_item))

    def OesApi_QuerySingleStkHolding(self, inv_acct_id, security_id, out_holding_item):
        """查询单条股票持仓信息"""
        return self._OesApi_QuerySingleStkHolding(byref(self.qry_channel),
                                                  None if inv_acct_id is None else create_string_buffer(inv_acct_id.encode()),
                                                  None if security_id is None else create_string_buffer(security_id.encode()),
                                                  None if out_holding_item is None else byref(out_holding_item))

    def OesApi_QuerySingleOrder(self, cl_seq_no, out_ord_item):
        """查询单条委托信息"""
        return self._OesApi_QuerySingleOrder(byref(self.qry_channel),
                                             c_int32(cl_seq_no),
                                             None if out_ord_item is None else byref(out_ord_item))

    def OesApi_QueryOrder(self, qry_filter, fn_qry_msg_callback, callback_params):
        """查询所有委托信息"""
        return self._OesApi_QueryOrder(byref(self.qry_channel),
                                       None if qry_filter is None else byref(qry_filter),
                                       self.F_OESAPI_ON_QRY_MSG_T(fn_qry_msg_callback),
                                       None if callback_params is None else byref(callback_params))

    def OesApi_QueryTrade(self, qry_filter, fn_qry_msg_callback, callback_params):
        """查询成交信息"""
        return self._OesApi_QueryTrade(byref(self.qry_channel),
                                       None if qry_filter is None else byref(qry_filter),
                                       self.F_OESAPI_ON_QRY_MSG_T(fn_qry_msg_callback),
                                       None if callback_params is None else byref(callback_params))

    def OesApi_QueryCashAsset(self, qry_filter, fn_qry_msg_callback, callback_params):
        """查询客户资金信息"""
        return self._OesApi_QueryCashAsset(byref(self.qry_channel),
                                           None if qry_filter is None else byref(qry_filter),
                                           self.F_OESAPI_ON_QRY_MSG_T(fn_qry_msg_callback),
                                           None if callback_params is None else byref(callback_params))

    def OesApi_QueryStkHolding(self, qry_filter, fn_qry_msg_callback, callback_params):
        """查询股票持仓信息"""
        return self._OesApi_QueryStkHolding(byref(self.qry_channel),
                                            None if qry_filter is None else byref(qry_filter),
                                            self.F_OESAPI_ON_QRY_MSG_T(fn_qry_msg_callback),
                                            None if callback_params is None else byref(callback_params))

    def OesApi_QueryLotWinning(self, qry_filter, fn_qry_msg_callback, callback_params):
        """查询新股配号、中签信息"""
        return self._OesApi_QueryLotWinning(byref(self.qry_channel),
                                            None if qry_filter is None else byref(qry_filter),
                                            self.F_OESAPI_ON_QRY_MSG_T(fn_qry_msg_callback),
                                            None if callback_params is None else byref(callback_params))

    def OesApi_QueryCustInfo(self, qry_filter, fn_qry_msg_callback, callback_params):
        """查询客户信息"""
        return self._OesApi_QueryCustInfo(byref(self.qry_channel),
                                          None if qry_filter is None else byref(qry_filter),
                                          self.F_OESAPI_ON_QRY_MSG_T(fn_qry_msg_callback),
                                          None if callback_params is None else byref(callback_params))

    def OesApi_QueryInvAcct(self, qry_filter, fn_qry_msg_callback, callback_params):
        """查询证券账户信息"""
        return self._OesApi_QueryInvAcct(byref(self.qry_channel),
                                         None if qry_filter is None else byref(qry_filter),
                                         self.F_OESAPI_ON_QRY_MSG_T(fn_qry_msg_callback),
                                         None if callback_params is None else byref(callback_params))

    def OesApi_QueryCommissionRate(self, qry_filter, fn_qry_msg_callback, callback_params):
        """查询佣金信息"""
        return self._OesApi_QueryCommissionRate(byref(self.qry_channel),
                                                None if qry_filter is None else byref(qry_filter),
                                                self.F_OESAPI_ON_QRY_MSG_T(fn_qry_msg_callback),
                                                None if callback_params is None else byref(callback_params))

    def OesApi_QueryFundTransferSerial(self, qry_filter, fn_qry_msg_callback, callback_params):
        """查询出入金流水"""
        return self._OesApi_QueryFundTransferSerial(byref(self.qry_channel),
                                                    None if qry_filter is None else byref(qry_filter),
                                                    self.F_OESAPI_ON_QRY_MSG_T(fn_qry_msg_callback),
                                                    None if callback_params is None else byref(callback_params))

    def OesApi_QueryIssue(self, qry_filter, fn_qry_msg_callback, callback_params):
        """查询证券发行产品信息"""
        return self._OesApi_QueryIssue(byref(self.qry_channel),
                                       None if qry_filter is None else byref(qry_filter),
                                       self.F_OESAPI_ON_QRY_MSG_T(fn_qry_msg_callback),
                                       None if callback_params is None else byref(callback_params))

    def OesApi_QueryStock(self, qry_filter, fn_qry_msg_callback, callback_params):
        """查询现货产品信息"""
        return self._OesApi_QueryStock(byref(self.qry_channel),
                                       None if qry_filter is None else byref(qry_filter),
                                       self.F_OESAPI_ON_QRY_MSG_T(fn_qry_msg_callback),
                                       None if callback_params is None else byref(callback_params))

    def OesApi_QueryEtf(self, qry_filter, fn_qry_msg_callback, callback_params):
        """查询ETF申赎产品信息"""
        return self._OesApi_QueryEtf(byref(self.qry_channel),
                                     None if qry_filter is None else byref(qry_filter),
                                     self.F_OESAPI_ON_QRY_MSG_T(fn_qry_msg_callback),
                                     None if callback_params is None else byref(callback_params))

    def OesApi_QueryEtfComponent(self, qry_filter, fn_qry_msg_callback, callback_params):
        """查询ETF成份证券信息"""
        return self._OesApi_QueryEtfComponent(byref(self.qry_channel),
                                              None if qry_filter is None else byref(qry_filter),
                                              self.F_OESAPI_ON_QRY_MSG_T(fn_qry_msg_callback),
                                              None if callback_params is None else byref(callback_params))

    def OesApi_QueryMarketState(self, qry_filter, fn_qry_msg_callback, callback_params):
        """查询市场状态信息"""
        return self._OesApi_QueryMarketState(byref(self.qry_channel),
                                             None if qry_filter is None else byref(qry_filter),
                                             self.F_OESAPI_ON_QRY_MSG_T(fn_qry_msg_callback),
                                             None if callback_params is None else byref(callback_params))

    def OesApi_QueryCounterCash(self, cash_acct_id, out_counter_cash_item):
        """查询主柜资金信息"""
        return self._OesApi_QueryCounterCash(byref(self.qry_channel),
                                             None if cash_acct_id is None else create_string_buffer(cash_acct_id.encode()),
                                             None if out_counter_cash_item is None else byref(out_counter_cash_item))

    def OesApi_QueryBrokerParamsInfo(self, out_broker_params):
        """查询券商参数信息"""
        return self._OesApi_QueryBrokerParamsInfo(byref(self.qry_channel),
                                                  None if out_broker_params is None else byref(out_broker_params))

    def OesApi_SendReportSynchronization(self, subscribe_env_id, subscribe_rpt_types, last_rpt_seq_num):
        """发送回报同步消息"""
        return self._OesApi_SendReportSynchronization(byref(self.rpt_channel),
                                                      c_int8(subscribe_env_id),
                                                      c_int32(subscribe_rpt_types),
                                                      c_int64(last_rpt_seq_num))

    def OesApi_InitAll(self, cfg_file, last_rpt_seq_num, last_cl_seq_no):
        """完整的初始化客户端环境"""
        return self._OesApi_InitAll(byref(self.client_env),
                                    None if cfg_file is None else create_string_buffer(cfg_file.encode()),
                                    create_string_buffer(OESAPI_CFG_DEFAULT_SECTION_LOGGER.encode()),
                                    create_string_buffer(OESAPI_CFG_DEFAULT_SECTION.encode()),
                                    create_string_buffer(OESAPI_CFG_DEFAULT_KEY_ORD_ADDR.encode()),
                                    create_string_buffer(OESAPI_CFG_DEFAULT_KEY_RPT_ADDR.encode()),
                                    create_string_buffer(OESAPI_CFG_DEFAULT_KEY_QRY_ADDR.encode()),
                                    last_rpt_seq_num,
                                    None if last_cl_seq_no is None else byref(last_cl_seq_no))

    def OesApi_LogoutAll(self, is_destory):
        """注销并关闭所有的客户端会话"""
        return self._OesApi_LogoutAll(byref(self.client_env),
                                      c_int(is_destory))

    def OesApi_DestoryAll(self):
        """直接断开与服务器的连接并释放会话数据"""
        return self._OesApi_DestoryAll(byref(self.client_env))

    def OesApi_SetThreadUsername(self, username):
        """设置当前线程登录OES时使用的登录用户名"""
        return self._OesApi_SetThreadUsername(None if username is None else create_string_buffer(username.encode()))

    def OesApi_GetThreadUsername(self):
        """返回当前线程登录OES时使用的登录用户名"""
        return self._OesApi_GetThreadUsername().decode()

    def OesApi_SetThreadPassword(self, password):
        """设置当前线程登录OES时使用的登录密码"""
        return self._OesApi_SetThreadPassword(None if password is None else create_string_buffer(password.encode()))

    def OesApi_SetThreadEnvId(self, cl_env_id):
        """设置当前线程登录OES时使用的客户端环境号"""
        return self._OesApi_SetThreadEnvId(c_int8(cl_env_id))

    def OesApi_GetThreadEnvId(self):
        """返回当前线程登录OES时使用的客户端环境号"""
        return self._OesApi_GetThreadEnvId()

    def OesApi_SetThreadSubscribeEnvId(self, subscribe_env_id):
        """设置当前线程订阅回报时待订阅的客户端环境号"""
        return self._OesApi_SetThreadSubscribeEnvId(c_int8(subscribe_env_id))

    def OesApi_GetThreadSubscribeEnvId(self):
        """返回当前线程订阅回报时待订阅的客户端环境号"""
        return self._OesApi_GetThreadSubscribeEnvId()

    def OesApi_SetThreadBusinessType(self, business_type):
        """设置当前线程登录OES时所期望对接的业务类型"""
        return self._OesApi_SetThreadBusinessType(c_int32(business_type))

    def OesApi_GetThreadBusinessType(self):
        """返回当前线程登录OES时所期望对接的业务类型"""
        return self._OesApi_GetThreadBusinessType()

    def OesApi_SetCustomizedIpAndMac(self, ip_str, mac_str):
        """设置客户端自定义的本地IP和MAC"""
        return self._OesApi_SetCustomizedIpAndMac(None if ip_str is None else create_string_buffer(ip_str.encode()),
                                                  None if mac_str is None else create_string_buffer(mac_str.encode()))

    def OesApi_SetCustomizedIp(self, ip_str):
        """设置客户端自定义的本地IP地址"""
        return self._OesApi_SetCustomizedIp(None if ip_str is None else create_string_buffer(ip_str.encode()))

    def OesApi_GetCustomizedIp(self):
        """获取客户端自定义的本地IP"""
        return self._OesApi_GetCustomizedIp().decode()

    def OesApi_SetCustomizedMac(self, mac_str):
        """设置客户端自定义的本地MAC地址"""
        return self._OesApi_SetCustomizedMac(None if mac_str is None else create_string_buffer(mac_str.encode()))

    def OesApi_GetCustomizedMac(self):
        """获取客户端自定义的本地MAC"""
        return self._OesApi_GetCustomizedMac().decode()

    def OesApi_SetCustomizedDriverId(self, driver_id):
        """设置客户端自定义的本地设备序列号"""
        return self._OesApi_SetCustomizedDriverId(None if driver_id is None else create_string_buffer(driver_id.encode()))

    def OesApi_GetCustomizedDriverId(self):
        """获取客户端自定义的本地设备序列号"""
        return self._OesApi_GetCustomizedDriverId().decode()

    def OesApi_GetClientId(self, session_info):
        """返回通道对应的客户端编号 (clientId)"""
        return self._OesApi_GetClientId(None if session_info is None else byref(session_info))

    def OesApi_GetClEnvId(self, session_info):
        """返回通道对应的客户端环境号 (clEnvId)"""
        return self._OesApi_GetClEnvId(None if session_info is None else byref(session_info))

    def OesApi_GetBusinessType(self, session_info):
        """返回通道对应的业务类型"""
        return self._OesApi_GetBusinessType(None if session_info is None else byref(session_info))

    def OesApi_IsBusinessSupported(self, session_info, business_type):
        """返回系统是否支持指定的业务类别"""
        return self._OesApi_IsBusinessSupported(None if session_info is None else byref(session_info),
                                                c_uint32(business_type))

    def OesApi_GetClientType(self, session_info):
        """获取客户端类型"""
        return self._OesApi_GetClientType(None if session_info is None else byref(session_info))

    def OesApi_GetClientStatus(self, session_info):
        """获取客户端状态"""
        return self._OesApi_GetClientStatus(None if session_info is None else byref(session_info))

    def OesApi_GetLastRecvTime(self, session_info):
        """获取通道最近接收消息时间"""
        return self._OesApi_GetLastRecvTime(None if session_info is None else byref(session_info))

    def OesApi_GetLastSendTime(self, session_info):
        """获取通道最近发送消息时间"""
        return self._OesApi_GetLastSendTime(None if session_info is None else byref(session_info))

    def OesApi_HasMoreCachedData(self):
        """返回回报通道是否还有更多已接收但尚未回调处理完成的数据"""
        return self._OesApi_HasMoreCachedData(byref(self.rpt_channel))

    def OesApi_IsValidOrdChannel(self):
        """返回委托申报通道是否已经连接且有效"""
        return self._OesApi_IsValidOrdChannel(byref(self.ord_channel))

    def OesApi_IsValidRptChannel(self):
        """返回回报通道是否已经连接且有效"""
        return self._OesApi_IsValidRptChannel(byref(self.rpt_channel))

    def OesApi_IsValidQryChannel(self):
        """返回查询通道是否已经连接且有效"""
        return self._OesApi_IsValidQryChannel(byref(self.qry_channel))

    def OesApi_GetLastError(self):
        """返回当前线程最近一次API调用失败的错误号"""
        return self._OesApi_GetLastError()

    def OesApi_SetLastError(self, err_code):
        """设置当前线程的API错误号"""
        return self._OesApi_SetLastError(c_int32(err_code))

    def OesApi_GetErrorMsg(self, err_code):
        """返回错误号对应的错误信息"""
        return self._OesApi_GetErrorMsg(c_int32(err_code)).decode()

    def OesApi_GetErrorMsg2(self, status, detail_status):
        """返回消息头中的状态码所对应的错误信息"""
        return self._OesApi_GetErrorMsg2(c_uint8(status),
                                         c_uint8(detail_status)).decode()

    def OesApi_HasStockStatus(self, stock_item, status):
        """返回现货产品是否具有指定状态"""
        return self._OesApi_HasStockStatus(None if stock_item is None else byref(stock_item),
                                           c_uint32(status))

    def OesHelper_ExtractOrdReportFromTrd(self, trd_report, out_ord_report):
        """从成交回报中提取和生成委托回报信息"""
        return self._OesHelper_ExtractOrdReportFromTrd(None if trd_report is None else byref(trd_report),
                                                       None if out_ord_report is None else byref(out_ord_report))
