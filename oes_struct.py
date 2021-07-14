# -*- coding: utf-8 -*-
from constant import *


class SocketFd(SimpleUnion):
    _fields_ = [
        ('socket_fd', c_int32),  # Socket描述符
        ('_socket_fd_filler', c_uint64),  # 按64位对齐的填充域
    ]


class SocketChannelInfo(SimpleStructure):
    _fields_ = [
        ('socket_fd', SocketFd),  # Socket描述符
        ('remote_port', c_int32),  # 套接字端口号
        ('protocol_type', c_uint8),  # 通信协议类型
        ('_is_net_byte_order', c_uint8),  # 是否使用网络字节序 (TRUE 网络字节序；FALSE 本机字节序)
        ('_is_broken', c_uint8),  # 连接是否已破裂 (用于内部处理)
        ('_is_send_broken', c_uint8),  # 标示异步发送线程的连接是否已破裂 (用于内部处理)
        ('remote_addr', c_char * SPK_MAX_URI_LEN),  # 套接字地址或DomainSocket的路径地址 (仅用于显示)

        ('connect_time', c_int64),  # 连接建立时间 (UTC时间, 即相对于1970年的秒数)
        ('_is_try_connecting', c_uint8),  # 标识是否正在尝试连接的过程中(用于内部处理)
        ('_filler', c_uint8 * 7),  # 按64位对齐的填充域
    ]


class DataBufferVar(SimpleStructure):
    _fields_ = [
        ('data_size', c_int32),  # 有效数据长度
        ('buf_size', c_int32),  # 缓存区总大小
        ('buffer', c_char_p),  # 缓存区指针
        ('_ref', c_void_p),  # 反向引用指针
    ]


class SGeneralClientChannel(SimpleStructure):
    _fields_ = [
        ('socket_fd', SocketFd),  # 1 文件描述符

        ('heart_bt_int', c_int32),  # 2 心跳间隔，单位为秒 (允许预先赋值)
        ('test_req_int', c_int32),  # 3 测试请求间隔，单位为秒
        ('protocol_type', c_uint8),  # 4 协议类型 (Binary, JSON等) (允许预先赋值)
        ('remote_set_num', c_uint8),  # 4 对端服务器的集群号
        ('remote_host_num', c_uint8),  # 5 已连接上的对端服务器的主机编号
        ('remote_is_leader', c_uint8),  # 6 对端服务器是否是'主节点'
        ('leader_host_num', c_uint8),  # 7 '主节点'的主机编号
        ('_filler1', c_uint8 * 3),  # 8 按64位对齐填充域

        ('_codec_buf', DataBufferVar),  # 9 接收缓存
        ('_recv_buf', DataBufferVar),  # 10 接收缓存
        ('_p_data_start_point', c_char_p),  # 11 数据起始位置指针
        ('_context_ptr', c_void_p),  # 12 保留给内部使用的上下文环境指针
        ('_monitor_ptr', c_void_p),  # 12 保留给内部使用的监控信息指针
        ('_custom_ptr', c_void_p),  # 12 可以由应用层自定义使用的指针变量
        ('_reaved_size', c_int32),  # 13 数据起始位置指针
        ('_custom_flag', c_int32),  # 14 可以由应用层自定义使用的指针变量

        ('_total_in_msg_size', c_int64),  # 15 ﻿累计接收到的未压缩数据大小
        ('_total_compressed_size', c_int64),  # 16 ﻿累计接收到的已压缩数据大小
        ('_total_decompress_size', c_int64),  # 17 ﻿解压缩后的数据总大小

        ('first_in_msg_seq', c_uint64),  # 18 已接收到的起始入向消息序号
        ('last_in_msg_seq', c_uint64),  # 19 实际已接收到的入向消息序号 (对应于登录应答消息的 lastOutMsgSeq)
        ('next_in_msg_seq', c_uint64),  # 20 期望的入向消息序号
        ('last_recv_time', c_int64 * DIFF_SYS_TIME_STAMP_LEN),  # 21 接收时间

        ('channel', SocketChannelInfo),  # 22 连接通道信息
        ('next_out_msg_seq', c_uint64),  # 23 出向消息序号
        ('last_out_msg_seq', c_uint64),  # 24 实际已发送的出向消息序号
        ('last_send_time', c_int64 * DIFF_SYS_TIME_STAMP_LEN),  # 25 ﻿发送时间

        ('sender_comp_id', c_char * GENERAL_CLI_MAX_COMP_ID_LEN),  # 26 发送方代码
        ('target_comp_id', c_char * GENERAL_CLI_MAX_COMP_ID_LEN),  # 27 接收方代码

        ('_magic_number', c_int32),  # 28 标识会话结构是否已经正确初始化过
        ('_magic_size', c_int32),  # 29 标识会话信息的结构体大

        ('_channel_type', c_uint8),  # 30 通道类型
        ('_cl_env_id', c_int8),  # 31 客户端环境号
        ('_group_flag', c_uint8),  # 32 通道组标志
        ('_protocol_hints', c_uint8),  # 33 协议约定信息
        ('_business_scope', c_uint8),  # 33 服务端业务范围
        ('_filler', c_uint8 * 3),  # 34 按64位对齐填充域

        ('_reserve_data', c_char * (GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE + SPK_CACHE_LINE_SIZE)),
        # 35保留给服务器或API内部使用的，用于存储自定义数据的扩展空间
        ('_ext_data', c_char * GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE),  # 36 可以由应用层自定义使用的，用于存储自定义数据的扩展空间
    ]


class OesApiClientEnv(SimpleStructure):
    _fields_ = [
        ('ord_channel', SGeneralClientChannel),  # 委托通道的会话信息
        ('rpt_channel', SGeneralClientChannel),  # 回报通道的会话信息
        ('qry_channel', SGeneralClientChannel),  # 查询通道的会话信息
    ]


class STimeval32(SimpleStructure):
    _fields_ = [('tv_sec', c_int32),
                ('tv_usec', c_int32), ]


class OesOrdReq(SimpleStructure):
    _fields_ = [
        ('cl_seq_no', c_int32),  # 客户委托流水号 (由客户端维护的递增流水, 原 ordSeqNo)
        ('mkt_id', c_uint8),  # 市场代码  @see eOesMarketIdT
        ('ord_type', c_uint8),  # 订单类型  @see eOesOrdTypeShT eOesOrdTypeSzT
        ('bs_type', c_uint8),  # 买卖类型  @see eOesBuySellTypeT
        ('_ord_base_info_filler', c_uint8),  # 按64位对齐的填充域
        ('inv_acct_id', c_char * OES_INV_ACCT_ID_MAX_LEN),  # 证券账户
        ('security_id', c_char * OES_SECURITY_ID_MAX_LEN),  # 证券代码
        ('ord_qty', c_int32),  # 委托数量
        ('ord_price', c_int32),  # 委托价格，单位精确到元后四位，即1元 = 10000
        ('orig_cl_ord_id', c_int64),  # 原始订单(待撤销的订单)的客户订单编号 (原 wthdrwUserOrdNum)
        ('user_info', UserInfo),  # 用户私有信息 (由客户端自定义填充, 并在回报数据中原样返回) 以上为 _OES_ORD_BASE_INFO_PKT
        ('_ord_req_orig_send_time', STimeval32),  # 委托请求的客户端原始发送时间 (OES内部使用, 由API在发送时自动填充)
    ]


class OesOrdCancelReq(SimpleStructure):
    _fields_ = [
        ('cl_seq_no', c_int32),  # 客户委托流水号(由客户端维护的递增流水, 用于识别重复的委托申报, 必填)
        ('mkt_id', c_uint8),  # 市场代码(必填) @ see   eOesMarketIdT
        ('_ord_cancell_base_info_filler', c_uint8 * 3),  # 按64位对齐的填充域
        ('inv_acct_id', c_char * OES_INV_ACCT_ID_MAX_LEN),  # 证券账户(选填, 若不为空则校验待撤订单是否匹配)
        ('security_id', c_char * OES_SECURITY_ID_MAX_LEN),  # 证券代码(选填, 若不为空则校验待撤订单是否匹配)
        ('ori_cl_seq_no', c_int32),  # 原始订单(待撤销的订单) 的客户委托流水号(若使用 origClOrdId, 则不必填充该字段)
        ('ori_cl_env_id', c_int8),  # 原始订单(待撤销的订单)的客户端环境号(小于等于0, 则使用当前会话的clEnvId)
        ('_ord_cancel_case_info_filler2', c_uint8 * 3),  # 按64位对齐的填充域
        ('ori_cl_ord_id', c_int64),  # 原始订单(待撤销的订单)的客户订单编号(若使用, 则不必填充该字段)
        ('user_info', UserInfo),  # 用户私有信息(由客户端自定义填充, 并在回报数据中原样返回) 以上 _OES_ORD_CANCEL_BASE_INFO_PKT
        ('_ord_req_orig_send_time', STimeval32),
        # 委托请求的客户端原始发送时间 (OES内部使用, 由API在发送时自动填充)  _OES_ORD_REQ_LATENCY_FIELDS
    ]


class OesOrdCnfm(SimpleStructure):
    _fields_ = [
        ('cl_seq_no', c_int32),  # 客户委托流水号 (由客户端维护的递增流水, 原 ordSeqNo)
        ('mkt_id', c_uint8),  # 市场代码  @see eOesMarketIdT
        ('ord_type', c_uint8),  # 订单类型  @see eOesOrdTypeShT eOesOrdTypeSzT
        ('bs_type', c_uint8),  # 买卖类型  @see eOesBuySellTypeT
        ('_ord_base_info_filler', c_uint8),  # 按64位对齐的填充域

        ('inv_acct_id', c_char * OES_INV_ACCT_ID_MAX_LEN),  # 证券账户
        ('security_id', c_char * OES_SECURITY_ID_MAX_LEN),  # 证券代码

        ('ord_qty', c_int32),  # 委托数量
        ('ord_price', c_int32),  # 委托价格，单位精确到元后四位，即1元 = 10000
        ('orig_cl_ord_id', c_int64),  # 原始订单(待撤销的订单)的客户订单编号 (原 wthdrwUserOrdNum)
        ('user_info', UserInfo),  # 用户私有信息 (由客户端自定义填充, 并在回报数据中原样返回)

        ('_ord_req_orig_send_time', STimeval32),  # 委托请求的客户端原始发送时间 (OES内部使用, 由API在发送时自动填充)

        ('cl_ord_id', c_int64),  # 客户订单编号 (在OES内具有唯一性的内部委托编号, 原 userOrdNum)
        ('client_id', c_int16),  # 客户端编号
        ('cl_env_id', c_int8),  # 客户端环境号
        ('orig_cl_env_id', c_int8),  # 原始订单(待撤销的订单)的客户端环境号 (仅适用于撤单委托)
        ('orig_cl_seq_no', c_int32),  # 原始订单(待撤销的订单)的客户委托流水号 (仅适用于撤单委托)
        ('ord_date', c_int32),  # 委托日期 (格式为 YYYYMMDD, 形如 20160830)
        ('ord_time', c_int32),  # 委托时间 (格式为 HHMMSSsss, 形如 141205000)
        ('ord_cnfm_time', c_int32),  # 委托确认时间 (格式为 HHMMSSsss, 形如 141206000)
        ('ord_status', c_uint8),  # 订单当前状态  @see eOesOrdStatusT
        ('ord_cnfm_sts', c_uint8),  # 委托确认状态  @see eOesOrdStatusT
        ('security_type', c_uint8),  # 证券类型  @see eOesSecurityTypeT
        ('sub_security_type', c_uint8),  # 证券子类型 @see eOesSubSecurityTypeT
        ('_platform_id', c_uint8),  # 平台号 (OES内部使用)  @see eOesPlatformIdT
        ('_tgw_group_no', c_uint8),  # 交易网关组序号 (OES内部使用)
        ('_tgw_partition_no', c_uint8),  # 交易网关平台分区号 (OES内部使用)
        ('product_type', c_uint8),  # 产品类型
        ("exch_ord_id", c_char * OES_EXCH_ORDER_ID_MAX_LEN),  # 交易所订单编号 (深交所的订单编号是16位的非数字字符串)
        ('_declared_flag', c_uint8),  # 已报盘标志 (OES内部使用)
        ('_repeat_flag', c_uint8),  # 重复回报标志 (OES内部使用)
        ('owner_type', c_uint8),  # 所有者类型 @see eOesOwnerTypeT
        ('frz_amt', c_int64),  # 委托当前冻结的交易金额
        ("frz_interest", c_int64),  # 委托当前的冻结利息
        ('frz_fee', c_int64),  # 委托当前冻结的交易费用
        ('cum_amt', c_int64),  # 委托累计已发生的交易金额
        ('cum_interest', c_int64),  # 委托累计已发生的利息
        ('cum_fee', c_int64),  # 委托累计已发生的交易费用
        ('cum_qty', c_int32),  # 累计执行数量 (累计成交数量)
        ('canceled_qty', c_int32),  # 已撤单数量
        ('ord_rej_reason', c_int32),  # 订单/撤单拒绝原因 (原 remark:char[16] 字段)
        ("exch_err_code", c_int32),  # 交易所错误码
        ('pbu_id', c_int32),  # PBU代码 (席位号)
        ('branch_id', c_int32),  # 营业部代码
        ('_row_num', c_int32),  # 回报记录号 (OES内部使用)
        ('_rec_num', c_uint32),  # OIW委托编号
        ("_ord_req_orig_recv_time", STimeval32),  # 委托请求的初始接收时间
        ("_ord_req_collcted_time", STimeval32),  # 委托请求的入队时间
        ("_ord_req_actual_deal_time", STimeval32),  # 委托请求的实际处理开始时间
        ("_ord_req_processed_time", STimeval32),  # 委托请求的处理完成时间
        ("_ord_cnfm_orig_recv_time", STimeval32),  # 委托确认的开始采集时间
        ("_ord_cnfm_collected_time", STimeval32),  # 委托确认的采集完成时间
        ("_ord_cnfm_actual_deal_time", STimeval32),  # 委托确认的实际处理开始时间
        ("_ord_cnfm_processed_time", STimeval32),  # 委托确认的处理完成时间
        ("_ord_declare_time", STimeval32),  # 初始报盘时间
        ("_ord_declare_done_time", STimeval32),  # 报盘完成时间
        ("_pushing_time", STimeval32),  # 消息推送时间 (写入推送缓存以后, 实际网络发送之前)
    ]


class OesOrdReject(SimpleStructure):
    _fields_ = [
        ('cl_seq_no', c_int32),  # 客户委托流水号 (由客户端维护的递增流水, 原 ordSeqNo)
        ('mkt_id', c_uint8),  # 市场代码  @see eOesMarketIdT
        ('ord_type', c_uint8),  # 订单类型  @see eOesOrdTypeShT eOesOrdTypeSzT
        ('bs_type', c_uint8),  # 买卖类型  @see eOesBuySellTypeT
        ('_ord_base_info_filler', c_uint8),  # 按64位对齐的填充域
        ('inv_acct_id', c_char * OES_INV_ACCT_ID_MAX_LEN),  # 证券账户
        ('security_id', c_char * OES_SECURITY_ID_MAX_LEN),  # 证券代码
        ('ord_qty', c_int32),  # 委托数量
        ('ord_price', c_int32),  # 委托价格，单位精确到元后四位，即1元 = 10000
        ('orig_cl_ord_id', c_int64),  # 原始订单(待撤销的订单)的客户订单编号 (原 wthdrwUserOrdNum)
        ('user_info', UserInfo),  # 用户私有信息 (由客户端自定义填充, 并在回报数据中原样返回)
        ('_ord_req_orig_send_time', STimeval32),  # 委托请求的客户端原始发送时间 (OES内部使用, 由API在发送时自动填充)
        ('orig_cl_seq_no', c_int32),  # 原始订单(待撤销的订单)的客户委托流水号 (仅适用于撤单请求)
        ('orig_cl_env_id', c_int8),  # 原始订单(待撤销的订单)的客户端环境号 (仅适用于撤单请求)
        ('cl_env_id', c_int8),  # 客户端环境号
        ('client_id', c_int16),  # 客户端编号
        ('ord_date', c_int32),  # 委托日期 (格式为 YYYYMMDD, 形如 20160830)
        ('ord_time', c_int32),  # 委托时间 (格式为 HHMMSSsss, 形如 141205000)
        ('ord_rej_reason', c_int32),  # 订单拒绝原因
        ('_filler', c_int32),  # 按64位对齐的填充域
    ]


class OesQryOrdFilter(SimpleStructure):
    _fields_ = [
        ('cust_id', c_char * OES_CUST_ID_MAX_LEN),  # 客户代码，可选项
        ('inv_acct_id', c_char * OES_INV_ACCT_ID_MAX_LEN),  # 证券账户代码，可选项
        ('mkt_id', c_uint8),  # * 市场代码，可选项。如无需此过滤条件请使用 OES_MKT_ID_UNDEFINE* @see eOesMarketIdT
        ('is_unclosed_only', c_uint8),  # 是否仅查询未关闭委托（包括未全部成交或撤销的委托）
        ('cl_env_id', c_int8),  # 客户端环境号
        ('security_type', c_uint8),  # 证券类别  @see eOesSecurityTypeT
        ('bs_type', c_uint8),  # 买卖类型  @see eOesBuySellTypeT
        ('_filler', c_uint8 * 3),  # 按64位对齐填充域
        ('cl_ord_id', c_int64),  # 客户委托编号，可选项
        ('cl_seq_no', c_int64),  # 客户委托流水号，可选项
        ('start_time', c_int32),  # 查询委托的起始时间 (格式为 HHMMSSsss, 比如 141205000 表示 14:12:05.000)
        ('end_time', c_int32),  # 查询委托的结束时间 (格式为 HHMMSSsss, 比如 141205000 表示 14:12:05.000)
        ('user_info', c_int64),  # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
    ]


class OesQryCommissionRateFilter(SimpleStructure):
    _fields_ = [
        ('cust_id', c_char * OES_CUST_ID_MAX_LEN),  # 客户代码，可选项
        ('mkt_id', c_uint8),  # * 市场代码，可选项。如无需此过滤条件请使用 OES_MKT_ID_UNDEFINE* @see eOesMarketIdT
        ('security_type', c_uint8),  # * 证券类别，可选项。如无需此过滤条件请使用 OES_SECURITY_TYPE_UNDEFINE* @see eOesSecurityTypeT
        ('bs_type', c_uint8),  # * 买卖类型，可选项。如无需此过滤条件请使用 OES_BS_TYPE_UNDEFINE* @see eOesBuySellTypeT
        ('_filler', c_uint8 * 5),  # 按64位对齐填充域
        ("user_info", c_int64)
    ]


class OesCommissionRateItem(SimpleStructure):
    _fields_ = [
        ('cust_id', c_char * OES_CUST_ID_MAX_LEN),  # 客户代码，可选项
        ("security_id", c_char * OES_SECURITY_ID_MAX_LEN),  # 证券代码
        ('mkt_id', c_uint8),  # 市场  @see eOesMarketIdT
        ('security_type', c_uint8),  # 证券类别  @see eOesSecurityTypeT
        ("sub_security_type", c_uint8),  # 证券子类别
        ('bs_type', c_uint8),  # 买卖类型  @see eOesBuySellTypeT
        ('fee_type', c_uint8),  # 费用标识  @see eOesFeeTypeT
        ('curr_type', c_uint8),  # 币种  @see eOesCurrTypeT
        ('calc_fee_mode', c_uint8),  # 计算模式  @see eOesCalFeeModeT
        ('_filler', c_uint8),  # 按64位对齐填充域
        ('fee_rate', c_int64),
        # * 费率* 当 calFeeMode 为 OES_CAL_FEE_MODE_AMOUNT 时，此字段为十万分比的费率；* 当 calFeeMode 为 OES_CAL_FEE_MODE_QTY 时，
        # * 此字段为委托单位份数所产生的费用，单位万分之一元
        ('min_fee', c_int32),  # 最低费用，大于0时有效。（单位：万分之一元）
        ('max_fee', c_int32),  # 最高费用，大于0时有效。（单位：万分之一元）
    ]


# 主柜资金信息内容
class OesCounterCashItem(Structure):
    _fields_ = [
        ('cash_acct_id', c_char * OES_CASH_ACCT_ID_MAX_LEN),  # 资金账户代码
        ('cust_id', c_char * OES_CAST_ID_MAX_LEN),  # 客户代码
        ('cust_name', c_char * OES_CUST_NAME_MAX_LEN),  # 客户姓名
        ('bank_id', c_char * OES_BANK_NO_MAX_LEN),  # 银行代码
        ('cash_type', c_uint8),  # 资金账户类别
        ('cash_acct_status', c_uint8),  # 资金账户状态
        ('curr_type', c_uint8),  # 货币类型
        ('is_fund_trsf_disabled', c_uint8),  # 出入金是否禁止标示
        ('_filler', c_uint8 * 4),  # 按64位对齐填充域
        ('counter_available_bal', c_int64),  # 主柜可用余额 单位精确到元后四位 1元=10000
        ('counter_drawable_bal', c_int64),  # 主柜可取余额 单位精确到元后四位 1元=10000
        ('counter_cash_update_time', c_int64),  # 主柜资金更新时间
        ('_reserve', c_int64 * 4),  # 保留字段
    ]


class OesCashAcctOverview(SimpleStructure):
    _fields_ = [
        ('cash_acct_id', c_char * OES_CASH_ACCT_ID_MAX_LEN),  # 资金账户代码
        ('cust_id', c_char * OES_CUST_ID_MAX_LEN),  # 客户代码
        ('bank_id', c_char * OES_BANK_NO_MAX_LEN),  # 银行代码
        ('is_valid', c_uint8),  # 资金账户是否有效标识
        ('cash_type', c_uint8),  # 资金账户类别
        ('cash_acct_status', c_uint8),  # 资金账户状态
        ('curr_type', c_uint8),  # 币种
        ('is_fund_trsf_disabled', c_uint8),  # 出入金是否禁止标识
        ('_filler', c_uint8 * 3),  # 按64位对齐填充域
        ('_reserve', c_int64),  # 备用字段
    ]


class OesInvAcctOverview(SimpleStructure):
    _fields_ = [
        ('inv_acct_id', c_char * OES_INV_ACCT_ID_MAX_LEN),  # 证券账户代码
        ('mkt_id', c_uint8),  # 市场
        ('acct_type', c_uint8),  # 账户类型
        ('status', c_uint8),  # 账户状态
        ('owner_type', c_uint8),  # 股东账户的所有者类型
        ('opt_inv_level', c_uint8),  # 期权投资者级别
        ('is_trade_disable', c_uint8),  # 是否禁止交易
        ('_inv_acct_base_filler1', c_uint8 * 2),  # 按64位对齐填充域
        ('limits', c_uint64),  # 证券账户权限限制
        ('permissions', c_uint64),  # 股东权限/客户权限
        ('pbu_id', c_int32),  # 席位号
        ('subscription_quota', c_int32),  # 主板权益 (新股/配股认购限额)  # 以上对应C中的宏定义 _OES_INV_ACCT_BASE_INFO_PKT
        ('cust_id', c_char * OES_CUST_ID_MAX_LEN),  # 客户代码
        ('is_valid', c_uint8),  # 股东账户是否有效标识
        ('_filler', c_uint8 * 3),  # 按64位对齐填充域
        ('kcsubscription_quota', c_int32),  # 科创板权益 (新股/配股认购限额)
        ('trd_ord_cnd', c_int32),  # 当日累计有效交易类委托笔数统计
        ('non_trd_ord_cnd', c_int32),  # 当日累计有效非交易类委托笔数统计
        ('cancell_ord_cnd', c_int32),  # 当日累计有效撤单笔数统计
        ('oes_reject_ord_cnd', c_int32),  # 当日累计被OES拒绝的委托笔数统计
        ('exchange_reject_ord_cnd', c_int32),  # 当日累计被交易所拒绝的委托笔数统计
        ('trd_cnd', c_int32),  # 当日累计成交笔数统计
        ('_reserve', c_int64),  # 备用字段
    ]


class OesCustOverview(SimpleStructure):
    _fields_ = [
        ('cust_id', c_char * OES_CUST_ID_MAX_LEN),  # 客户代码

        ('cust_type', c_uint8),  # 客户类型
        ('status', c_uint8),  # 客户状态
        ('risk_level', c_uint8),  # 风险等级
        ('original_risk_level', c_uint8),  # 原始风险等级
        ('institution_flag', c_uint8),  # 机构标志
        ('investor_class', c_uint8),  # 投资者分类
        ('_cust_base_filler1', c_uint8 * 2),      # 按64位对齐填充域

        ('branch_id', c_int32),  # 营业部代码
        ('_cust_base_filler2', c_uint32),  # 按64位对齐填充域 # 以上代码对应C中的宏定义_OES_CUST_BASE_INFO_PKT

        ('cust_name', c_char * OES_CUST_NAME_MAX_LEN),  # 客户姓名

        ('spot_cash_acct', OesCashAcctOverview),  # 普通资金账户信息
        ('credit_cash_acct', OesCashAcctOverview),  # 信用资金账户信息
        ('option_cash_acct', OesCashAcctOverview),  # 衍生品资金账户信息
        ('sh_spot_inv_acct', OesInvAcctOverview),  # 上海现货股东账户信息
        ('sh_option_inv_acct', OesInvAcctOverview),  # 上海衍生品股东账户信息
        ('sz_spot_inv_acct', OesInvAcctOverview),  # 深圳现货股东账户信息
        ('sz_option_inv_acct', OesInvAcctOverview),  # 深圳衍生品股东账户信息
        ('_reserve', c_int64),  # 备用字段

    ]


# 客户端总览信息内容
class OesClientOverview(SimpleStructure):
    _fields_ = [
        ('client_id', c_int16),  # 客户端编号
        ('client_type', c_uint8),  # 客户端类型
        ('client_status', c_uint8),  # 客户端状态
        ('is_api_forbidden', c_uint8),  # api禁用标识
        ('is_block_trader', c_uint8),  # 是否大宗交易标识
        ('business_scope', c_uint8),  # 客户端适用的业务范围 @see eOesBusinessScopeT
        ('_filler', c_uint8),  # 按64位字节对齐的填充域
        ('logon_time', c_int64),  # 客户端登录(委托接收服务)时间
        ('client_name', c_char * OES_CLIENT_NAME_MAX_LEN),  # 客户端名称
        ('client_memo', c_char * OES_CLIENT_DESC_MAX_LEN),  # 客户端说明
        ('sse_stk_pbu_id', c_int32),  # 上海现货/信用账户对应的PBU代码
        ('sse_opt_pbu_id', c_int32),  # 上海衍生品账户对应的PBU代码
        ('sse_qualification_class', c_uint8),  # 上海股东账户的投资者适当性管理分类
        ('_filler2', c_uint8 * 7),  # 按64位对齐填充域
        ('szse_stk_pbu_id', c_int32),  # 深圳现货/信用账户对应的PBU代码
        ('szse_opt_pbu_id', c_int32),  # 深圳衍生品账户对应的PBU代码
        ('szse_qualification_class', c_uint8),  # 深圳股东账户的投资者适当性管理分类
        ('_filler3', c_uint8 * 7),  # 按64位对齐填充域
        ('curr_ord_connected', c_int32),  # 当前已连接的委托通道数量
        ('curr_rpt_connected', c_int32),  # 当前已连接的回报通道数量
        ('curr_qry_connected', c_int32),  # 当前已连接的查询通道数量
        ('max_ord_connect', c_int32),  # 委托通道允许的最大同时连接数量
        ('max_rpt_connect', c_int32),  # 回报通道允许的最大同时连接数量
        ('max_qry_connect', c_int32),  # 查询通道允许的最大同时连接数量
        ('ord_traffic_limit', c_int32),  # 委托通道的流量控制
        ('qry_traffic_limit', c_int32),  # 查询通道的流量控制
        ('_reverse', c_int64),  # 备用字段
        ('associated_cust_cnt', c_int32),  # 客户端关联的客户数量
        ('_filler4', c_int32),  # 按64位字节对齐的填充域
        ('cust_items', OesCustOverview * 1)  # 客户端关联的客户列表

    ]


# 查询现货持仓过滤条件
class OesQryStkHoldingFilter(SimpleStructure):
    _fields_ = [
        ('cust_id', c_char * OES_CUST_ID_MAX_LEN),  # 客户代码, 可选项
        ('inv_acct_id', c_char * OES_INV_ACCT_ID_MAX_LEN),  # 证券账户代码, 可选项
        ('security_id', c_char * OES_SECURITY_ID_MAX_LEN),  # 证券代码, 可选项
        ('mkt_id', c_uint8),  # 市场代码
        ('security_type', c_uint8),  # 证券类别
        ('product_type', c_uint8),  # 产品类型
        ('_filler1', c_uint8 * 5),  # 按64位对齐填充域
        ('user_info', c_int64),  # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
    ]


class OesStkHoldingBaseInfo(SimpleStructure):
    _fields_ = [
        ('inv_acct_id', c_char * OES_INV_ACCT_ID_MAX_LEN),  # 账户代码
        ('security_id', c_char * OES_SECURITY_ID_MAX_LEN),  # 产品代码
        ('mkt_id', c_uint8),  # 市场代码
        ('security_type', c_uint8),  # 证券类型
        ('sub_security_type', c_uint8),  # 证券子类型
        ('product_type', c_uint8),  # 产品类型
        ('_hold_base_filler', c_uint8 * 4),  # 按64位对齐的填充域

        ('original_hld', c_int64),  # 日初持仓
        ('original_cost_amt', c_int64),  # 日初总持仓成本(日初持仓成本价=日初总持仓成本 / 日初持仓)

        ("total_buy_hld", c_int64),  # 日中累计买入持仓
        ('total_sell_hld', c_int64),  # 日中累计卖出持仓
        ('sell_frz_hld', c_int64),  # 当前卖出冻结持仓
        ('manual_frz_hld', c_int64),  # 手动冻结持仓

        ('total_buy_amt', c_int64),  # 日中累计买入金额
        ('total_sell_amt', c_int64),  # 日中累计卖出金额
        ('total_buy_fee', c_int64),  # 日中累计买入费用
        ('total_sell_fee', c_int64),  # 日中累计卖出费用

        # 日中累计转换获得持仓, ETF申赎业务使用,
        # 成分股持仓场景, 转换获得指赎回时获得的成分股持仓
        # ETF证券持仓场景, 转换获得指申购时获得的ETF证券股持仓
        ('total_trsf_in_hld', c_int64),

        # - 成分股持仓场景, 转换获得指赎回时获得的成分股持仓
        # - ETF证券持仓场景, 转换获得指申购时获得的ETF证券股持仓;
        ('total_trsf_out_hld', c_int64),  # 日中累计转换付出持仓, ETF申赎业务使用

        # - 成分股持仓场景, 转换付出指申购时使用的成分股持仓
        # - ETF证券持仓场景, 转换付出指赎回时使用的ETF证券股持仓
        ('trsf_out_frz_hld', c_int64),  # 当前转换付出冻结持仓

        ('original_lock_hld', c_int64),  # 日初锁定持仓
        ('total_lock_hld', c_int64),     # 日中累计锁定持仓
        ('total_unlock_hld', c_int64),   # 日中累计解锁持仓

        ('original_avl_hld', c_int64),   # 日初可用持仓
        ('max_reduce_quota', c_int64),  # 当日最大可减持额度
    ]


class OesStkHoldingReport(SimpleStructure):
    _fields_ = [
        ('inv_acct_id', c_char * OES_INV_ACCT_ID_MAX_LEN),  # 账户代码
        ('security_id', c_char * OES_SECURITY_ID_MAX_LEN),  # 产品代码
        ('mkt_id', c_uint8),  # 市场代码
        ('security_type', c_uint8),  # 证券类型
        ('sub_security_type', c_uint8),  # 证券子类型
        ('product_type', c_uint8),  # 产品类型
        ('_hold_base_filler', c_uint8 * 4),  # 按64位对齐的填充域

        ('original_hld', c_int64),  # 日初持仓
        ('original_cost_amt', c_int64),  # 日初总持仓成本(日初持仓成本价=日初总持仓成本 / 日初持仓)

        ("total_buy_hld", c_int64),  # 日中累计买入持仓
        ('total_sell_hld', c_int64),  # 日中累计卖出持仓
        ('sell_frz_hld', c_int64),  # 当前卖出冻结持仓
        ('manual_frz_hld', c_int64),  # 手动冻结持仓

        ('total_buy_amt', c_int64),  # 日中累计买入金额
        ('total_sell_amt', c_int64),  # 日中累计卖出金额
        ('total_buy_fee', c_int64),  # 日中累计买入费用
        ('total_sell_fee', c_int64),  # 日中累计卖出费用

        ('total_trsf_in_hld', c_int64),  # 日中累计转换获得持仓, ETF申赎业务使用,
        # - 成分股持仓场景, 转换获得指赎回时获得的成分股持仓
        # - ETF证券持仓场景, 转换获得指申购时获得的ETF证券股持仓;
        ('total_trsf_out_hld', c_int64),  # 日中累计转换付出持仓, ETF申赎业务使用

        # - 成分股持仓场景, 转换付出指申购时使用的成分股持仓
        # - ETF证券持仓场景, 转换付出指赎回时使用的ETF证券股持仓
        ('trsf_out_frz_hld', c_int64),  # 当前转换付出冻结持仓

        ('original_lock_hld', c_int64),  # 日初锁定持仓
        ('total_lock_hld', c_int64),  # 日中累计锁定持仓
        ('total_unlock_hld', c_int64),  # 日中累计解锁持仓

        ('original_avl_hld', c_int64),  # 日初可用持仓
        ('max_reduce_quota', c_int64),  # 当日最大可减持额度

        ('sell_avl_hld', c_int64),     # 当前可卖持仓
        ('trsf_out_avl_hld', c_int64), # 当前可转换付出持仓
        ('lock_avl_hld', c_int64),     # 当前可锁定持仓
        ('_filler', c_int64),          # 按64位对齐填充域
        # * 总持仓, 包括当前可用持仓、不可交易持仓和在途冻结持仓在內的汇总值
        # * 可卖持仓请参考“当前可卖持仓(sellAvlHld)”字段
        ('sum_hld', c_int64),
        ('cost_price', c_int64),       # 持仓成本价
    ]


OesStkHoldingItem = OesStkHoldingReport


# 查询成交信息过滤条件
class OesQryTrdFilter(SimpleStructure):
    _fields_ = [
        ('cust_id', c_char * OES_CUST_ID_MAX_LEN),  # 客户代码, 可选项
        ('inv_acct_id', c_char * OES_INV_ACCT_ID_MAX_LEN),  # 证券账户代码, 可选项
        ('mkt_id', c_uint8),  # 市场代码
        ('cl_env_id', c_int8),  # 客户端端环境号
        ('security_type', c_uint8),  # 证券类别
        ('bs_type', c_uint8),  # 买卖类型
        ('_filler1', c_uint32),  # 按64位对齐填充域
        ('cl_ord_id', c_int64),  # 内部委托编号
        ('cl_seq_no', c_int64),  # 客户委托流水号
        ('start_time', c_int32),  # 成交开始时间
        ('end_time', c_int32),  # 成交结束时间
        ('user_info', c_int64),  # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
    ]


class OesTrdCnfm(SimpleStructure):
    _fields_ = [
        ('exch_trd_num', c_int64),  # 交易所成交编号(以下的6个字段是成交信息的联合索引字段)
        ('mkt_id', c_uint8),  # 市场代码
        ('trd_side', c_uint8),  # 买卖类型(取值范围: 买 / 卖, 申购 / 赎回(仅深圳))
        ('_plat_form_id', c_uint8),  # 平台号(OES内部使用)
        ('_trd_cnfm_type', c_uint8),  # 成交类型(OES内部使用)
        ('_etf_trd_cnfm_seq', c_uint32),  # ETF成交回报顺序号(OES内部使用), 为区分ETF成交记录而设置(以订单为单位)

        ('inv_acct_id', c_char * OES_INV_ACCT_ID_MAX_LEN),  # 股东账户代码
        ('security_id', c_char * OES_SECURITY_ID_MAX_LEN),  # 产品代码

        ('trd_date', c_int32),  # 成交日期(格式为YYYYMMDD, 形如20160830)
        ('trd_time', c_int32),  # 成交时间(格式为HHMMSSsss, 形如141205000)
        ('trd_qty', c_int32),  # 成交数量
        ('trd_price', c_int32),  # 成交价格(单位精确到元后四位, 即: 1元 = 10000)
        ('trd_amt', c_int64),  # 成交金额(单位精确到元后四位, 即: 1元 = 10000)

        ('cl_ord_id', c_int64),  # 客户订单编号
        ('cum_qty', c_int32),  # 累计执行数量
        ('_row_num', c_int32),  # 回报记录号

        ('_tgw_grp_no', c_uint8),  # 交易网关组序号(OES内部使用)
        ('_is_trsf_in_cash_available', c_uint8),  # ETF赎回得到的替代资金是否当日可用 (OES内部使用)
        ('_tgw_partition_no', c_uint8),  # 交易网关平台分区号 (OES内部使用)
        ('product_type', c_uint8),  # 产品类型
        ('orig_ord_qty', c_int32),  # 原始委托数量

        ('pbu_id', c_int32),  # PBU代码(席位号)
        ('branch_id', c_int32),  # 营业部代码

        ('cl_seq_no', c_int32),  # 客户委托流水号
        ('client_id', c_int16),  # 客户端编号
        ('cl_env_id', c_int8),  # 客户端环境号
        ('sub_security_type', c_uint8),  # 证券子类别

        ("ord_status", c_uint8),  # 订单当前状态
        ('ord_type', c_uint8),  # 订单类型
        ('ord_buy_sell_type', c_uint8),  # 买卖类型
        ('security_type', c_uint8),  # 证券类型
        ('orig_ord_price', c_int32),  # 原始委托价格, 单位精确到元后四位, 即1元 = 10000

        ('cum_amt', c_int64),  # 累计成交金额
        ('cum_interest', c_int64),  # 累计成交利息
        ('cum_fee', c_int64),  # 累计交易费用

        ('user_info', UserInfo),  # 用户私有信息
        ('_trd_cnfm_orig_recv_time', STimeval32),  # 成交确认的开始采集时间
        ('_trd_cnfm_collected_time', STimeval32),  # 成交确认的采集完成时间
        ('_trd_cnfm_actual_deal_time', STimeval32),  # 成交确认的实际处理开始时间
        ('_trd_cnfm_processed_time', STimeval32),  # 成交确认的处理完成时间
        ('_pushing_time', STimeval32),  # 消息推送时间(写入推送缓存以后, 实际网络发送之前)
    ]


# 查询客户资金过滤条件
class OesQryCashAssetFilter(SimpleStructure):
    _fields_ = [
        ('cust_id', c_char * OES_CUST_ID_MAX_LEN),  # 客户代码，可选项
        ('cash_acct_id', c_char * OES_CASH_ACCT_ID_MAX_LEN),  # 资金账户代码，可选项
        ('user_info', c_int64),  # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
    ]


class OesCashAssetBaseInfo(SimpleStructure):
    _fields_ = [
        ('cash_acct_id', c_char * OES_CASH_ACCT_ID_MAX_LEN),  # 资金账户代码
        ('cust_id', c_char * OES_CUST_ID_MAX_LEN),  # 客户代码

        ('curr_type', c_uint8),  # 币种
        ('cash_type', c_uint8),  # 资金帐户类别(冗余自资金账户)
        ('cash_acct_status', c_uint8),  # 资金帐户状态(冗余自资金账户)
        ('is_fund_trsf_disabled', c_uint8),  # 是否禁止出入金(仅供API查询使用)
        ('_cash_asset_base_filler', c_uint8 * 4),  # 按64位对齐的填充域

        ('beginning_bal', c_int64),  # 期初余额, 单位精确到元后四位, 即1元 = 10000
        ('beginning_avl_bal', c_int64),  # 期初可用余额, 单位精确到元后四位, 即1元 = 10000
        ('beginning_drawable_bal', c_int64),  # 期初可取余额, 单位精确到元后四位, 即1元 = 10000

        ('disable_bal', c_int64),  # 不可用资金余额(既不可交易又不可提取), 单位精确到元后四位, 即1元 = 10000
        ('reversal_amt', c_int64),  # 当前冲正金额(红冲蓝补的资金净额), 取值可以为负数(表示资金调出),
        # 单位精确到元后四位(即1元=10000)
        ('manual_frz_amt', c_int64),  # 手动冻结资金, 取值在0和当前资产之间, 单位精确到元后四位(即1元=10000)

        ('total_deposit_amt', c_int64),  # 日中累计存入资金金额, 单位精确到元后四位, 即1元 = 10000
        ('total_withdraw_amt', c_int64),  # 日中累计提取资金金额, 单位精确到元后四位, 即1元 = 10000
        ('withdraw_frz_amt', c_int64),  # 当前提取冻结资金金额, 单位精确到元后四位, 即1元 = 10000

        ('total_sell_amt', c_int64),  # 日中累计卖获得资金金额, 单位精确到元后四位, 即1元 = 10000
        ('total_buy_amt', c_int64),  # 日中累计 买 / 申购 / 逆回购  使用资金金额，单位精确到元后四位，即1元 = 10000
        ('buy_frz_amt', c_int64),  # 当前交易冻结金额, 单位精确到元后四位, 即1元 = 10000

        ('total_fee_amt', c_int64),  # 日中累计交易费用金额, 单位精确到元后四位, 即1元 = 10000
        ('fee_frz_amt', c_int64),  # 当前冻结交易费用金额, 单位精确到元后四位, 即1元 = 10000

        ('margin_amt', c_int64),  # 当前维持的保证金金额, 单位精确到元后四位, 即1元 = 10000
        ('margin_frz_amt', c_int64),  # 当前冻结的保证金金额, 单位精确到元后四位, 即1元 = 10000
    ]


class OesCashAssetReport(SimpleStructure):
    _fields_ = [
        ('cash_acct_id', c_char * OES_CASH_ACCT_ID_MAX_LEN),  # 资金账户代码
        ('cust_id', c_char * OES_CUST_ID_MAX_LEN),  # 客户代码

        ('curr_type', c_uint8),  # 币种
        ('cash_type', c_uint8),  # 资金帐户类别(冗余自资金账户)
        ('cash_acct_status', c_uint8),  # 资金帐户状态(冗余自资金账户)
        ('is_fund_trsf_disabled', c_uint8),  # 是否禁止出入金(仅供API查询使用)
        ('_cash_asset_base_filler', c_uint8 * 4),  # 按64位对齐的填充域

        ('beginning_bal', c_int64),  # 期初余额, 单位精确到元后四位, 即1元 = 10000
        ('beginning_available_bal', c_int64),  # 期初可用余额, 单位精确到元后四位, 即1元 = 10000
        ('beginning_drawable_bal', c_int64),  # 期初可取余额, 单位精确到元后四位, 即1元 = 10000

        ('disable_bal', c_int64),  # 不可用资金余额(既不可交易又不可提取), 单位精确到元后四位, 即1元 = 10000
        ('reversal_amt', c_int64),  # 当前冲正金额(红冲蓝补的资金净额), 取值可以为负数(表示资金调出),
        # 单位精确到元后四位(即1元=10000)
        ('manual_frz_amt', c_int64),  # 手动冻结资金, 取值在0和当前资产之间, 单位精确到元后四位(即1元=10000)

        ('total_deposit_amt', c_int64),  # 日中累计存入资金金额, 单位精确到元后四位, 即1元 = 10000
        ('total_withdraw_amt', c_int64),  # 日中累计提取资金金额, 单位精确到元后四位, 即1元 = 10000
        ('withdraw_frz_amt', c_int64),  # 当前提取冻结资金金额, 单位精确到元后四位, 即1元 = 10000

        ('total_sell_amt', c_int64),  # 日中累计卖获得资金金额, 单位精确到元后四位, 即1元 = 10000
        ('total_buy_amt', c_int64),  # 日中累计 买 / 申购 / 逆回购  使用资金金额，单位精确到元后四位，即1元 = 10000
        ('buy_frz_amt', c_int64),  # 当前交易冻结金额, 单位精确到元后四位, 即1元 = 10000

        ('total_fee_amt', c_int64),  # 日中累计交易费用金额, 单位精确到元后四位, 即1元 = 10000
        ('fee_frz_amt', c_int64),  # 当前冻结交易费用金额, 单位精确到元后四位, 即1元 = 10000

        ('margin_amt', c_int64),  # 当前维持的保证金金额, 单位精确到元后四位, 即1元 = 10000
        ('margin_frz_amt', c_int64),  # 当前冻结的保证金金额, 单位精确到元后四位, 即1元 = 10000

        ('current_total_bal', c_int64),  # 当前余额
        ('current_available_bal', c_int64), # 当前可用余额
        ('current_drawable_bal', c_int64),  # 当前可取余额
    ]


OesCashAssetItem = OesCashAssetReport


# 查询客户信息过滤条件
class OesQryCustFilter(SimpleStructure):
    _fields_ = [
        ('cust_id', c_char * OES_CUST_ID_MAX_LEN),  # 客户代码, 可选项
        ('user_info', c_int64),  # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
    ]


class OesCustBaseInfo(SimpleStructure):
    _fields_ = [
        ('cust_id', c_char * OES_CUST_ID_MAX_LEN),  # 客户代码
        ('cust_type', c_uint8),  # 客户类型
        ('status', c_uint8),  # 客户状态 0 正常, 非0 不正常
        ('risk_level', c_uint8),  # OES风险等级
        ('origin_risk_level', c_uint8),  # 客户原始风险等级
        ('institution_flag', c_uint8),  # 机构标志(TRUE 机构投资者, FALSE 个人投资者)
        ('investor_class', c_uint8),  # 投资者分类
        ('_cust_base_filler1', c_uint8 * 2),  # 按64位对齐填充域
        ('branch_id', c_int32),  # 营业部代码
        ('_cast_base_filler2', c_uint32),  # 按64位对齐填充域

    ]


class OesInvAcctBaseInfo(SimpleStructure):
    _fields_ = [
        ('inv_acct_id', c_char * OES_INV_ACCT_ID_MAX_LEN),  # 股东账户代码
        ('mkt_id', c_uint8),  # 市场 @see eOesMarketIdT
        ('acct_type', c_uint8),  # 账户类型 @see eOesAcctTypeT
        ('status', c_uint8),  # 账户状态, 同步于主柜或者通过MON手动设置 @see eOesAcctStatusT
        ('owner_type', c_uint8),  # 股东账户的所有者类型 @see eOesOwnerTypeT
        ('opt_inv_level', c_uint8),  # 投资者期权等级 @see eOesOptInvLevelT
        ('is_trade_disabled', c_uint8),  # 是否禁止交易 (仅供API查询使用)
        ('_inv_acct_base_filler', c_uint8 * 2),  # 按64位对齐填充域
        ('limits', c_uint64),  # 证券账户权限限制 @see eOesTradingLimitT
        ('permissions', c_uint64),  # 股东权限/客户权限 @see eOesTradingPermissionT
        ('pbu_id', c_int32),  # 席位号
        ('stk_position_limit_ratio', c_int32),  # 个股持仓比例阀值, 单位精确到百万分之一, 即 200002 = 20.0002%
        ('subscription_quota', c_int32),  # 主板权益 (新股/配股认购限额)
        ('kc_subscription_quota', c_int32),  # 科创板权益 (新股/配股认购限额)
        ('_inv_acct_base_reserve', c_char * 32),  # 预留的备用字段
    ]


# 查询新股认购、中签信息过滤条件
class OesQryLotWinningFilter(SimpleStructure):
    _fields_ = [
        ('cust_id', c_char * OES_CUST_ID_MAX_LEN),  # 客户代码, 可选项
        ('inv_acct_id', c_char * OES_INV_ACCT_ID_MAX_LEN),  # 证券账户代码, 可选项
        ('mkt_id', c_uint8),  # 市场代码, 可选项。如无需此过滤条件请使用 OES_MKT_ID_UNDEFINE
        ('lot_type', c_uint8),  # 查询记录类型, 可选项。如无需此过滤条件请使用 OES_LOT_TYPE_UNDEFINE
        ('_filler', c_uint8 * 6),  # 按64位对齐填充域
        ('start_date', c_int32),  # 查询起始日期(格式为  YYYYMMDD)
        ('end_date', c_int32),  # 查询结束日期(格式为  YYYYMMDD)
        ('user_info', c_int64),  # 用户私有信息(由客户端自定义填充, 并在应答数据中原样返回)

    ]


class OesLotWinningBaseInfo(SimpleStructure):
    _fields_ = [
        ('inv_acct_id', c_char * OES_INV_ACCT_ID_MAX_LEN),  # 证券账户
        ('security_id', c_char * OES_SECURITY_ID_MAX_LEN),  # 配号代码、中签代码
        ('mkt_id', c_uint8),  # 市场代码
        ('lot_type', c_uint8),  # 记录类型
        ('rej_reason', c_uint8),  # 失败原因, 当且仅当 lotType 为  OES_LOT_TYPE_FAILED  时此字段有效
        ('_lot_winning_base_info_filler', c_int8),  # 按64位对齐填充域
        ('lot_date', c_int32),  # 配号日期 / 中签日期(格式为  YYYYMMDD, 形如 20160830)
        ('security_name', c_char * OES_SECURITY_NAME_MAX_LEN),  # 证券名称
        ('assign_num', c_int64),  # 配号首个号码。当为中签记录时此字段固定为0
        ('lot_qty', c_int32),  # 配号成功数量 / 中签股数
        ('lot_price', c_int32),  # 最终发行价, 单位精确到元后四位, 即1元 = 10000。当为配号记录时此字段值固定为0
        ('lot_amt', c_int64),  # 中签金额, 单位精确到元后四位, 即1元 = 10000。当为配号记录时此字段值固定为0
    ]


# 查询证券发行信息过滤条件
class OesQryIssueFilter(SimpleStructure):
    _fields_ = [
        ('security_id', c_char * OES_SECURITY_ID_MAX_LEN),  # 证券发行代码，可选项
        ('mkt_id', c_uint8),  # 市场代码, 可选项。如无需此过滤条件请使用 OES_MKT_ID_UNDEFINE
        ('product_type', c_uint8),  # 产品类型,
        ('_filler', c_uint8 * 6),  # 按64位对齐填充域
        ('user_info', c_int64),  # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
    ]


class OesIssueBaseInfo(SimpleStructure):
    _fields_ = [
        ('security_id', c_char * OES_SECURITY_ID_MAX_LEN),  # 证券发行代码
        ('mkt_id', c_uint8),  # 市场代码 @ see  eOesMarketIdT
        ('security_type', c_uint8),  # 证券类型
        ('sub_security_type', c_uint8),  # 证券子类型
        ('product_type', c_uint8),  # 产品类型
        ('issue_type', c_uint8),  # 发行方式
        ('is_cancell_able', c_uint8),  # 是否允许撤单
        ('is_re_apply_able', c_uint8),  # 是否允许重复认购
        ('susp_flag', c_uint8),  # 停牌标识
        ('security_attribute', c_uint32),  # 证券属性 (保留字段, 取值固定为0)
        ('is_registration', c_uint8),  # 是否注册制 (0 非注册制, 1 注册制)
        ('is_no_profit', c_uint8),  # 是否尚未盈利 (0 已盈利, 1 未盈利 (仅适用于创业板产品))
        ('is_weighted_voting_rights', c_uint8),  # 是否存在投票权差异 (0 无差异, 1 存在差异 (仅适用于创业板产品))
        ('is_vie', c_uint8),  # 是否具有协议控制框架 (0 没有, 1 有 (仅适用于创业板产品))
        ('_issue_base_reserve', c_uint8 * 8),  # 预留的备用字段
        ('start_date', c_int32),  # 发行起始日
        ('end_date', c_int32),  # 发行结束日
        ('issue_price', c_int32),  # 发行价格
        ('upper_limit_price', c_int32),  # 申购价格上限 (单位精确到元后四位, 即1元 = 10000)
        ('lower_limit_price', c_int32),  # 申购价格下限 (单位精确到元后四位, 即1元 = 10000)
        ('ord_max_qty', c_int32),  # 委托最大份数
        ('ord_min_qty', c_int32),  # 委托最小份数
        ('qty_unit', c_int32),  # 委托份数单位
        ('issue_qty', c_int64),  # 总发行量
        ('alot_record_day', c_int32),  # 配股股权登记日(仅上海市场有效)
        ('alot_ex_rights_day', c_int32),  # 配股股权除权日(仅上海市场有效)
        ('underlying_security_id', c_char * OES_SECURITY_ID_MAX_LEN),  # 证券代码 (正股代码)
        ('security_name', c_char * OES_SECURITY_NAME_MAX_LEN),  # 证券名称
        ('_issue_base_reserve2', c_char * 56),  # 预留的备用字段
        ('_issue_base_reserve3', c_char * 64),  # 预留的备用字段
    ]


# 查询出入金流水过滤条件
class OesQryFundTransferSerialFilter(SimpleStructure):
    _fields_ = [
        ('cust_id', c_char * OES_CUST_ID_MAX_LEN),  # 客户代码，可选项
        ('cash_acct_id', c_char * OES_CASH_ACCT_ID_MAX_LEN),  # 资金账户代码, 可选项
        ('cl_seq_no', c_int32),  # 出入金流水号
        ('cl_env_id', c_int8),  # 客户端环境号
        ('_filler', c_uint8 * 3),  # 按64位对齐填充域
        ('user_info', c_int64),  # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
    ]


class OesFundTrsfReport(SimpleStructure):
    _fields_ = [
        ('cl_seq_no', c_int32),  # 客户委托流水号 (由客户端维护的递增流水)
        ('client_id', c_int16),  # 客户端编号
        ('cl_env_id', c_int8),  # 客户端环境号
        ('direct', c_uint8),  # 划转方向
        ('cash_acct_id', c_char * OES_CASH_ACCT_ID_MAX_LEN),  # 资金账户代码
        ('occur_amt', c_int64),  # 发生金额 (都是正数), 单位精确到元后四位, 即1元 = 10000
        ('user_info', UserInfo),  # 用户私有信息 (由客户端自定义填充, 并在回报数据中原样返回)
        ('fund_trsf_id', c_int32),  # OES出入金委托编号 (在OES内具有唯一性的内部出入金委托编号)
        ('counter_entrust_no', c_int32),  # 柜台出入金委托编号
        ('oper_date', c_int32),  # 出入金委托日期(格式为 YYYYMMDD, 形如 20160830)
        ('oper_time', c_int32),  # 出入金委托时间(格式  HHMMSSsss, 形如 141205000)
        ('dclr_time', c_int32),  # 上报柜台时间(格式为HHMMSSsss, 形如141205000)
        ('done_time', c_int32),  # 柜台执行结果采集时间 (格式为 HHMMSSsss, 形如 141205000)
        ('is_allot_only', c_uint8),  # 出入金转账类型
        ('trsf_status', c_uint8),  # 出入金委托执行状态
        ('_has_counter_transfered', c_uint8),  # 是否有转账到主柜
        ('_filler', c_uint8),  # 按64位对齐填充域
        ('rej_reason', c_int32),  # 错误原因
        ('counter_err_code', c_int32),  # 主柜错误码
        ('_filler2', c_uint32),  # 按64位对齐填充域
        ('allot_serial_no', c_char * 64),  # 资金调拨流水号
        ('error_info', c_char * 64),  # 错误信息

    ]


class OesFundTrsfReject(SimpleStructure):
    _fields_ = [
        ('cl_seq_no', c_int32),  # 客户委托流水号 (由客户端维护的递增流水)
        ('direct', c_uint8),  # 划转方向
        ('is_allot_only', c_uint8),  # 出入金转账类型
        ("_fund_trsf_base_filler", c_uint8 * 2),  # 按64位对齐填充域
        ('cash_acct_id', c_char * OES_CASH_ACCT_ID_MAX_LEN),  # 资金账户代码
        ('trd_passwd', c_char * OES_PWD_MAX_LEN),  # 交易密码
        ('trsf_passwd', c_char * OES_PWD_MAX_LEN),  # 转账密码(转账方向为转入(银行转证券), 此密码为银行密码.
        # 转账方向为转出(证券转银行), 此密码为资金密码
        ('occur_amt', c_int64),  # 发生金额 (都是正数), 单位精确到元后四位, 即1元 = 10000
        ('user_info', UserInfo),  # 用户私有信息 (由客户端自定义填充, 并在回报数据中原样返回)
        ('ord_date', c_int32),  # 委托日期 (格式为 YYYYMMDD, 形如 20160830)
        ('ord_time', c_int32),  # 委托时间 (格式为 HHMMSSsss, 形如 141205000)
        ('client_id', c_int16),  # 客户端编号
        ('cl_env_id', c_int8),  # 客户端环境编号
        ('_filler', c_int8),  # 64位对齐的填充域
        ('rej_reason', c_int32),  # 错误码
        ('error_info', c_char * OES_MAX_ERROR_INFO_LEN),  # 错误信息

    ]


class OesFundTrsfReq(SimpleStructure):
    _fields_ = [
        ('cl_seq_no', c_int32),  # 客户委托流水号（由客户端维护的递增流水）
        ('direct', c_uint8),  # 划转方向  @see eOesCashDirectT
        ("is_allot_only", c_uint8),  # 是否仅调拨
        ('_fund_trsf_base_filler', c_uint8 * 2),  # 按64位对齐填充域
        ('cash_acct_id', c_char * OES_CASH_ACCT_ID_MAX_LEN),  # 资金账户代码
        ('trd_passwd', c_char * OES_PWD_MAX_LEN),  # 交易密码
        ("trsf_passwd", c_char * OES_PWD_MAX_LEN),
        ("occur_amt", c_int64),  # 发生金额（都是正数），单位精确到元后四位，即1元
        ("user_info", UserInfo),  # 用户私有信息 (由客户端自定义填充, 并在回报数据中原样返回)
    ]


# 查询证券账户过滤条件
class OesQryInvAcctFilter(SimpleStructure):
    _fields_ = [
        ('cust_id', c_char * OES_CUST_ID_MAX_LEN),  # 客户代码，可选项
        ('inv_acct_id', c_char * OES_INV_ACCT_ID_MAX_LEN),  # 证券账户代码，可选项
        ('mkt_id', c_uint8),  # 市场代码, 可选项。如无需此过滤条件请使用 OES_MKT_ID_UNDEFINE
        ('_filler', c_uint8 * 7),  # 按64位对齐填充域
        ('user_info', c_int64),  # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)

    ]


class OesInvAcctItem(SimpleStructure):
    _fields_ = [
        ('inv_acct_id', c_char * OES_INV_ACCT_ID_MAX_LEN),  # 股东账户代码
        ('mkt_id', c_uint8),  # 市场 @ see  eOesMarketIdT
        ('acct_type', c_uint8),  # 账户类型 @ see  eOesAcctTypeT
        ('status', c_uint8),  # 账户状态 @ see  eOesAcctStatusT
        ('owner_type', c_uint8),  # 股东账户的所有者类型 @ see  eOesOwnerTypeT
        ('opt_inv_level', c_uint8),  # 期权投资者级别 @ see  eOesOptInvLevelT
        ('is_trade_disabled', c_uint8),  # 是否禁止交易(仅供API查询使用)
        ('_inv_acct_base_filler', c_uint8 * 2),  # 按64位对齐填充域
        ('limits', c_uint64),  # 证券账户权限限制 @ see  eOesTradingLimitT
        ('permissions', c_uint64),  # 股东权限 / 客户权限 @ see  eOesTradingPermissionT
        ('pbu_id', c_int32),  # 席位号
        ('stk_position_limit_ratio', c_int32),  # 个股持仓比例阀值
        ('subscription_quota', c_int32),  # 新股认购限额
        ("kcsubscription_quota", c_int32),  # 科创板权益 (新股/配股认购限额)以上 _OES_INV_ACCT_BASE_INFO_PKT
        ('_inv_acct_base_reserve', c_char * 32),  # 预留的备用字段
        ('cust_id', c_char * OES_CUST_ID_MAX_LEN),  # 客户代码
    ]


# 查询ETF申赎产品信息过滤条件
class OesQryEtfFilter(SimpleStructure):
    _fields_ = [
        ('fund_id', c_char * OES_SECURITY_ID_MAX_LEN),  # 基金代码，可选项
        ('mkt_id', c_uint8),  # 市场代码, 可选项。如无需此过滤条件请使用 OES_MKT_ID_UNDEFINE
        ('_filler', c_uint8 * 7),  # 按64位对齐填充域
        ('user_info', c_int64),  # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
    ]


class OesEtfBaseInfo(SimpleStructure):
    _fields_ = [
        ('fund_id', c_char * OES_SECURITY_ID_MAX_LEN),  # Etf申赎代码
        ('security_id', c_char * OES_SECURITY_ID_MAX_LEN),  # Etf买卖代码
        ('mkt_id', c_uint8),  # 市场代码
        ('security_type', c_uint8),  # 证券类型
        ('sub_security_type', c_uint8),  # 证券子类型
        ('is_publish_iopv', c_uint8),  # 是否需要发布IOPV 1: 是;0: 否
        ('is_creation_able', c_uint8),  # 交易所 / 基金公司的允许申购标志  1: 是;0: 否
        ('is_redemption_able', c_uint8),  # 交易所/基金公司的允许赎回标志  1: 是; 0: 否
        ('is_disabled', c_uint8),  # 券商管理端的禁止交易标志  1: 是; 0: 否
        ('_etf_base_filler', c_uint8),  # 按64位对齐填充域
        ('component_cnt', c_int32),  # 成分证券数目
        ('cre_rdm_unit', c_int32),  # 每个篮子(最小申购、赎回单位) 对应的ETF份数, 即申购赎回单位
        ('max_cash_ratio', c_int32),  # 最大现金替代比例, 精确到0.00001( = 0.001 %)
        ('nav', c_int32),  # 前一日基金的单位净值
        ('nav_per_cu', c_int64),  # 前一日最小申赎单位净值
        ('dividend_per_cu', c_int64),  # 红利金额
        ('trading_day', c_int32),  # 当前交易日, 格式YYYYMMDD
        ('pre_trading_day', c_int32),  # 前一交易日, 格式YYYYMMDD
        ('esti_cash_cmpoent', c_int64),  # 每个篮子的预估现金差额
        ('cash_cmpoent', c_int64),  # 前一日现金差额
        ('creation_limit', c_int64),  # 当日申购限额
        ('redem_limit', c_int64),  # 当日赎回限额
        ('net_creation_limit', c_int64),  # 单个账户净申购总额限制
        ('net_redem_limit', c_int64),  # 单个账户净赎回总额限制

    ]


class OesEtfComponentBaseInfo(SimpleStructure):
    _fields_ = [
        ('fund_id', c_char * OES_SECURITY_ID_MAX_LEN),  # 成分股所属ETF的基金代码
        ('security_id', c_char * OES_SECURITY_ID_MAX_LEN),  # Etf成分股代码
        ('mkt_id', c_uint8),  # 市场代码 @see eOesMarketIdT
        ('fund_mkt_id', c_uint8),  # ETF基金市场代码 @see eOesMarketIdT
        ('sub_flag', c_uint8),  # 现金替代标识 @see eOesEtfSubFlagT
        ('security_type', c_uint8),  # 证券类型 @see eOesSecurityTypeT
        ('sub_security_type', c_uint8),  # 证券子类型 @see eOesSubSecurityTypeT
        ('is_trd_component', c_uint8),  # 是否是作为申赎对价的成份证券
        ('_etf_component_base_filler', c_uint8 * 2),  #按64位对齐填充域
        ('prev_close', c_int32),  # 昨日收盘价格, 单位精确到元后四位, 即1元 = 10000
        ('qty', c_int32),  # 成分证券数量
        ('premium_ratio', c_int32),  # 溢价比例, 单位精确到十万分之一, 即溢价比例10% = 10000
        ('discount_ratio', c_int32),  # 赎回折价比例, 单位精确到十万分之一, 即折价比例10% = 10000
        ('creation_sub_cash', c_int64),  # 申购替代金额, 单位精确到元后四位, 即1元 = 10000
        ('redemption_sub_cash', c_int64),  # 赎回替代金额, 单位精确到元后四位, 即1元 = 10000
    ]


# 查询ETF成分股
class OesQryEtfComponentFilter(SimpleStructure):
    _fields_ = [
        ('fund_id', c_char * OES_SECURITY_ID_MAX_LEN),  # 基金代码，可选项
        ('fund_mkt_id', c_uint8),  # ETF基金市场代码, 可选项。如无需此过滤条件请使用 OES_MKT_ID_UNDEFINE
        ('_filler', c_uint8 * 7),  # 按64位对齐填充域
        ('user_info', c_int64),  # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
    ]


class OesEtfComponentItem(SimpleStructure):
    _fields_ = [
        ('fund_id', c_char * OES_SECURITY_ID_MAX_LEN),  # 成分股所属ETF的基金代码
        ('security_id', c_char * OES_SECURITY_ID_MAX_LEN),  # Etf成分股代码
        ('mkt_id', c_uint8),  # 市场代码
        ('fund_mkt_id', c_uint8),  # ETF基金市场代码
        ('sub_flag', c_uint8),  # 现金替代标识
        ('security_type', c_uint8),  # 证券类型
        ('sub_security_type', c_uint8),  # 证券子类型
        ('is_trd_component', c_uint8),  # 是否是作为申赎对价的成份证券
        ('_etf_component_base_filler', c_uint8 * 2),  # 按64位对齐填充域
        ('prev_close', c_int32),  # 昨日收盘价格
        ('qty', c_int32),  # 成分证券数量
        ('premium_ratio', c_int32),  # 申购溢价比例
        ('discount_ratio', c_int32),  # 赎回折价比例
        ('creation_sub_cash', c_int64),  # 申购替代金额
        ('redemption_sub_cash', c_int64),  # 赎回替代金额
        ('security_name', c_char * OES_SECURITY_NAME_MAX_LEN),  # 成份证券名称
        ('_reserve', c_char * 96),  # 预留的备用字段
    ]


class OesQryStockFilter(SimpleStructure):
    _fields_ = [
        ('security_id', c_char * OES_SECURITY_ID_MAX_LEN),  # 证券代码, 可选项
        ('mkt_id', c_uint8),  # 市场代码, 可选项。如无需此过滤条件请使用 OES_MKT_ID_UNDEFIN
        ('security_type', c_uint8),  # 证券类型
        ('sub_security_type', c_uint8),  # 子证券类型
        ('_filler', c_uint8 * 5),  # 按64位对齐填充域
        ('user_info', c_int64),  # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)

    ]


class OesPriceLimit(SimpleStructure):
    _fields_ = [
        ('upper_limit_price', c_int32),  # 上涨限价, 单位精确到元后四位, 即1元 = 10000
        ('lower_limit_price', c_int32),  # 下跌限价, 单位精确到元后四位, 即1元 = 10000
    ]


class OesStockBaseInfo(SimpleStructure):
    _fields_ = [
        ('security_id', c_char * OES_SECURITY_ID_MAX_LEN),  # 产品代码
        ('mkt_id', c_uint8),  # 市场代码
        ('product_type', c_uint8),  # 产品类型
        ('security_type', c_uint8),  # 证券类别
        ('sub_security_type', c_uint8),  # 证券子类型
        ('security_level', c_uint8),  # 证券级别
        ('security_risk_level', c_uint8),  # 产品风险等级
        ('curr_type', c_uint8),  # 币种
        ('qualification_class', c_uint8),  # 投资者适当性管理分类
        ('security_status', c_uint32),  # 证券状态
        ('security_attribute', c_uint32),  # 证券属性
        ('susp_flag', c_uint8),  # 连续停牌标识
        ('temporary_susp_flag', c_uint8),  # 临时停牌标识 (TRUE 已停牌, FALSE 未停牌)
        ('is_day_trading', c_uint8),  # 是否支持当日回转交易 0: 不支持; 其他: 支持
        ('is_registration', c_uint8),  # 是否注册制 (0 非注册制, 1 注册制)
        ('is_crd_collateral', c_uint8),  # 是否为融资融券担保品 (0 不是担保品, 1 是担保品)
        ('is_crd_margin_trade_underlying', c_uint8),  # 是否为融资标的 (0 不是融资标的, 1 是融资标的)
        ('is_crd_short_sell_underlying', c_uint8),  # 是否为融券标的 (0 不是融券标的, 1 是融券标的)
        ('is_no_profit', c_uint8),  # 是否尚未盈利 (0 已盈利, 1 未盈利 (仅适用于科创板和创业板产品))
        ('is_weighted_voting_rights', c_uint8),  # 是否存在投票权差异 (0 无差异, 1 存在差异 (仅适用于科创板和创业板产品))
        ('is_vie', c_uint8),  # 是否具有协议控制框架 (0 没有, 1 有 (仅适用于创业板产品))
        ('_stock_base_filler1', c_uint8 * 6),  # 按64位对齐的填充域
        ('price_limit', OesPriceLimit * OES_TRD_SESS_TYPE_MAX),  # 竞价限价参数表, 数组下标为当前时段标志
        ('price_tick', c_int32),  # 最小报价单位 (单位精确到元后四位, 即1元 = 10000)
        ('prev_close', c_int32),  # 昨日收盘价，单位精确到元后四位，即1元 = 10000
        ('lmt_buy_max_qty', c_int32),  # 单笔限价买委托数量上限
        ('lmt_buy_min_qty', c_int32),  # 单笔限价买委托数量下限
        ('lmt_buy_qty_unit', c_int32),  # 买入单位
        ('mkt_buy_max_qty', c_int32),  # 单笔市价买委托数量上限
        ('mkt_buy_min_qty', c_int32),  # 单笔市价买委托数量下限
        ('mkt_buy_qty_unit', c_int32),  # 单笔市价买入单位
        ('lmt_sell_max_qty', c_int32),  # 单笔限价卖委托数量上限
        ("lmt_sell_min_qty", c_int32),  # 单笔限价卖委托数量下限
        ('lmt_sell_qty_unit', c_int32),  # 卖出单位
        ('mkt_sell_max_qty', c_int32),  # 单笔市价卖委托数量上限
        ("mkt_sell_min_qty", c_int32),  # 单笔市价卖委托数量下限
        ("mkt_sell_qty_unit", c_int32),  # 单笔市价卖出单位
        ('bond_interest', c_int64),  # 债券的每百元应计利息额, 单位精确到元后八位
        ('par_value', c_int64),  # 面值, 单位精确到元后四位, 即1元 = 10000
        ('repo_expiration_days', c_int32),  # 逆回购期限
        ('cash_hold_days', c_int32),  # 占款天数
        ('auction_limit_type', c_uint8),  # 连续交易时段的竞价范围限制类型
        ('auction_refer_price_type', c_uint8),  # 连续交易时段的竞价范围基准价类型
        ('_stock_base_filler4', c_uint8 * 2),  # 按64位对齐的填充域
        ('auction_up_down_range', c_int32),  # 连续交易时段的竞价范围涨跌幅度 (百分比或绝对价格, 取决于'连续竞价范围限制类型')
        ('list_date', c_int32),  # 上市日期
        ('maturity_date', c_int32),  # 到期日期 (仅适用于债券等有发行期权的产品)
        ('outstanding_share', c_int64),  # 总股本 (即: 总发行数量, 上证无该字段, 取值同流通股数量)
        ('public_float_share', c_int64),  # 流通股数量
        ('underlying_security_id', c_char * OES_SECURITY_ID_MAX_LEN),  # 基础证券代码 (标的产品代码)
        ('fund_id', c_char * OES_SECURITY_ID_MAX_LEN),  # ETF基金申赎代码
        ('security_name', c_char * OES_SECURITY_NAME_MAX_LEN),  # 产品名称
        ('_stock_base_reserve1', c_char * 80),  # 预留的备用字段
        ('_stock_base_reserve2', c_char * 64),  # 预留的备用字段
    ]


class OesMarketStateInfo(SimpleStructure):
    _fields_ = [
        ('exch_id', c_uint8),  # 交交易所代码 @see eOesExchangeIdT
        ('platform_id', c_uint8),  # 交易平台类型 @see eOesPlatformIdT
        ('mkt_id', c_uint8),  # 市场代码 @see eOesMarketIdT
        ('mkt_state', c_uint8),  # 市场状态 @see eOesMarketStatusT
        ('_filler', c_uint8 * 4)  # 按64位对齐的填充域
    ]


class OesChangePasswordRsp(SimpleStructure):
    _fields_ = [
        ('encrypt_method', c_int32),  # 加密方法
        ('_filler', c_int32),  # 按64位对齐的填充域
        ('user_name', c_char * OES_CLIENT_NAME_MAX_LEN),  # 登陆用户名
        ('user_info', UserInfo),  # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
        ('client_id', c_int16),  # 客户端编号
        ('cl_env_id', c_int8),  # 客户端环境号
        ('_filler', c_int8),  # 按64位对齐的填充域
        ('trans_date', c_int32),  # 发生日期 (格式为 YYYYMMDD, 形如 20160830)
        ('trans_time', c_int32),  # 发生时间 (格式为 HHMMSSsss, 形如 141205000)
        ('rej_reason', c_int32),  # 拒绝原因

    ]


class OesTestRequestRsp(SimpleStructure):
    _fields_ = [
        ("test_req_id", c_char * OES_MAX_TEST_REQ_ID_LEN),  # 测试请求标识符
        ("orig_send_time", c_char * OES_MAX_SENDING_TIME_LEN),  #
        ("_filler1", c_char * 2),  # 按64位对齐的填充域
        ("resp_time", c_char * OES_MAX_SENDING_TIME_LEN),  # 测试请求应答的发送时间 (timeval结构或形如'YYYYMMDD-HH:mm:SS.sss'的字符串)
        ("_filler2", c_char * 2),  # 按64位对齐的填充域
        ("_recv_time", STimeval32),  # 消息实际接收时间 (开始解码等处理之前的时间)
        ("_collected_time", STimeval32),  # 消息采集处理完成时间
        ('_pushing_time', STimeval32),  # 消息推送时间 (写入推送缓存以后, 实际网络发送之前)
    ]


class OesReportSynchronizationRsp(SimpleStructure):
    _fields_ = [
        ('last_rpt_seq_num', c_int64),  # 服务端最后已发送或已忽略的回报数据的回报编号
        ('subscribe_env_id', c_int8),  # *待订阅的客户端环境号* - 大于0, 区分环境号, 仅订阅环境号对应的回报数据
        # * - 小于等于0, 不区分环境号, 订阅该客户下的所有回报数据
        ('_filler', c_uint8 * 3),  # 按64位对齐的填充域
        ('subscribe_rpt_types', c_int32),  # 已订阅的回报消息种类

    ]


class OesLogonRsp(SimpleStructure):
    _fields_ = [
        ('encrypt_method', c_int32),  # 加密方法
        ('heart_bt_int', c_int32),  # 心跳间隔
        ('user_name', c_char * OES_CLIENT_NAME_MAX_LEN),  # 登录用户名
        ('appl_ver_id', c_char * OES_VER_ID_MAX_LEN),  # 服务器端采用的协议版本号
        ('min_ver_id', c_char * OES_VER_ID_MAX_LEN),  # 服务器端兼容的最低协议版本号
        ('host_num', c_uint8),  # 服务端(执行系统)编号
        ('is_leader', c_uint8),  # 是否是'主节点'
        ('leader_host_num', c_uint8),  # 当前'主节点'的系统编号
        ('cl_env_id', c_int8),  # 客户端环境号
        ('client_type', c_uint8),  # 客户端类型 @see eOesClientTypeT
        ('client_status', c_uint8),  # 客户端状态 @see eOesClientStatusT
        ('_protocol_hints', c_uint8),  # 协议约定
        ('_filler', c_uint8),  # 按64位对齐填充域
        ('last_in_msg_seq', c_int64),  # 服务端最后接收到的入向消息序号
        ('last_out_msg_seq', c_int64),  # 服务端最后已发送的出向消息序号

    ]


class OesQryCursor(SimpleStructure):
    _fields_ = [
        ('seq_no', c_uint32),  # 查询位置
        ('is_end', c_uint8),  # 是否是当前最后一个包
        ('_filler', c_uint8 * 3),  # 按64位对齐填充域
        ('user_info', c_int64),  # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
    ]


class OesRptMsgHead(SimpleStructure):
    _fields_ = [
        ('rpt_seq_num', c_int64),  # 执行报告的消息编号
        ('rpt_msg_type', c_uint8),  # 回报消息的消息代码
        ('exec_type', c_uint8),  # 执行类型 @ see  eOesExecTypeT
        ('body_length', c_int16),  # 回报消息的消息体大小
        ('ord_rej_reason', c_int32),  # 撤单被拒绝原因
    ]


class OesRptMsgBody(SimpleUnion):
    _fields_ = [
        ('ord_insert_rsp', OesOrdCnfm),  # OES委托响应 - 委托已生成
        ('ord_reject_rsp', OesOrdReject),  # OES委托响应 - 业务拒绝
        ('ord_cnfm', OesOrdCnfm),  # 交易所委托回报
        ('trd_cnfm', OesTrdCnfm),  # 交易所成交回报
        ('fund_trsf_reject_rsp', OesFundTrsfReject),  # 出入金委托拒绝
        ('fund_trsf_cnfm', OesFundTrsfReport),  # 出入金执行报告
        ('cash_asset_rpt', OesCashAssetReport),  # 资金变动信息
        ('stk_holding_rpt', OesStkHoldingReport),  # 持仓变动信息(股票)
    ]


class OesRptMsg(SimpleStructure):
    _fields_ = [
        ('rpt_head', OesRptMsgHead),
        ('rpt_body', OesRptMsgBody)
    ]


class OesRspMsgBody(SimpleUnion):
    _fields_ = [
        ('rpt_msg', OesRptMsg),  # 执行报告回报消息
        ('mkt_state_rpt', OesMarketStateInfo),  # 市场状态消息
        ('test_request_rsp', OesTestRequestRsp),  # 测试请求的应答报文
        ('report_synchronization_rsp', OesReportSynchronizationRsp),  # 回报同步应答报文
        ('change_password_rsp', OesChangePasswordRsp),  # 修改密码应答报文
    ]


class OesReportSynchronizationReq(SimpleStructure):
    _fields_ = [
        # 客户端最后接收到的回报数据的回报编号
        # - 等于0, 从头开始推送回报数据
        # - 大于0, 从指定的回报编号开始推送回报数据
        # - 小于0, 从最新的数据开始推送回报数据
        ('last_rpt_seq_num', c_int64),
        # 待订阅的客户端环境号
        # - 大于0, 区分环境号, 仅订阅环境号对应的回报数据
        # - 小于等于0, 不区分环境号, 订阅该客户下的所有回报数据
        ('subscribe_env_id', c_int8),
        ('_filler', c_uint8 * 3),  # 按64位对齐的填充域
        ('subscribe_rpt_types', c_int32),  # 待订阅的回报消息种类
    ]


class OesTrdBaseInfo(SimpleStructure):
    _fields_ = [
        ('exch_trd_num', c_int64),  # 交易所成交编号 (以下的6个字段是成交信息的联合索引字段)
        ('mkt_id', c_uint8),  # 市场代码 @see eOesMarketIdT
        ('trd_side', c_uint8),  # 买卖类型 (取值范围: 买/卖, 申购/赎回(仅深圳)) @see eOesBuySellTypeT
        ('_platform_id', c_uint8),  # 平台号 (OES内部使用) @see eOesPlatformIdT
        ('_trd_cnfm_type', c_uint8),  # 成交类型 (OES内部使用) @see eOesEtfTrdCnfmTypeT
        ('_etf_trd_cnfm_seq', c_uint32),  # ETF成交回报顺序号 (OES内部使用), 为区分ETF成交记录而设置 (以订单为单位)
        ('inv_acct_id', c_char * OES_INV_ACCT_ID_MAX_LEN),  # 股东账户代码
        ('security_id', c_char * OES_SECURITY_ID_MAX_LEN),  # 产品代码
        ('trd_date', c_int32),  # 成交日期 (格式为 YYYYMMDD, 形如 20160830)
        ('trd_time', c_int32),  # 成交时间 (格式为 HHMMSSsss, 形如 141205000)
        ('trd_qty', c_int32),  # 成交数量
        ('trd_price', c_int32),  # 成交价格 (单位精确到元后四位, 即: 1元=10000)
        ('trd_amt', c_int64),  # 成交金额 (单位精确到元后四位, 即: 1元=10000)
        ('cl_ord_id', c_int64),  # 客户订单编号
        ('cum_qty', c_int32),  # 累计执行数量
        ('_rowNum', c_int32),  # 回报记录号 (OES内部使用)
        ('_tgw_grp_no', c_uint8),  # 交易网关组序号 (OES内部使用)
        ('_is_trsf_in_cash_available', c_uint8),  # ETF赎回得到的替代资金是否当日可用 (OES内部使用)
        ('_tgw_partition_no', c_uint8),  # 交易网关平台分区号 (OES内部使用)
        ('product_type', c_uint8),  # 产品类型 @see eOesProductTypeT
        ('orig_ord_qty', c_int32),  # 原始委托数量
        ('pbu_id', c_int32),  # PBU代码 (席位号)
        ('branch_id', c_int32),  # 营业部代码
    ]


class OesFundTrsfBaseInfo(SimpleStructure):
    _fields_ = OesFundTrsfReq._fields_


class OesTestRequestReq(SimpleStructure):
    _fields_ = [
        ('test_req_id', c_char * OES_MAX_TEST_REQ_ID_LEN),  # 测试请求标识符
        ('send_time', c_char * OES_MAX_SENDING_TIME_LEN),  # 发送时间 (timeval结构或形如'YYYYMMDD-HH:mm:SS.sss'的字符串)
        ('_filler', c_char * 2),  # 按64位对齐的填充域
    ]


class OesChangePasswordReq(SimpleStructure):
    _fields_ = [
        ('encrypt_method', c_int32),  # 加密方法
        ('_filler', c_int32),  # 按64位对齐的填充域
        ('username', c_char * OES_CLIENT_NAME_MAX_LEN),  # 登录用户名
        ('userinfo', UserInfo),  # 用户私有信息 (由客户端自定义填充, 并在回报数据中原样返回)
        ('old_password', c_char * OES_PWD_MAX_LEN),  # 之前的登录密码
        ('new_password', c_char * OES_PWD_MAX_LEN),  # 新的登录密码
    ]


class OesBatchOrdersHead(SimpleStructure):
    _fields_ = [
        ('item_count', c_int32),  # 本批次的委托请求数量
        ('_filler', c_int32),  # 按64位对齐的填充域
    ]


class OesBatchOrdersReq(SimpleStructure):
    _fields_ = [
        ('batch_head', OesBatchOrdersHead),  # 批量委托请求的批次消息头
        ('items', OesOrdReq * 1),  # 委托请求列表
    ]


class OesReqMsgBody(SimpleUnion):
    _fields_ = [
        ('ord_req', OesOrdReq),  # 委托申报请求报文
        ('ord_cancel_req', OesOrdCancelReq),  # 撤单请求请求报文
        ('batch_orders_req', OesBatchOrdersReq),  # 批量委托请求报文
        ('fund_trsf_req', OesFundTrsfReq),  # 出入金请求报文
        ('change_password_req', OesChangePasswordReq),  # 修改密码请求报文
        ('test_request_req', OesTestRequestReq),  # 测试请求报文
        ('rpt_sync_req', OesReportSynchronizationReq),  # 回报同步请求报文
    ]


OesOrdItem = OesOrdCnfm


class OesQryOrdReq(SimpleStructure):
    _fields_ = [
        ('req_head', OesQryReqHead),  # 查询请求消息头
        ('qry_filter', OesQryOrdFilter),  # 查询过滤条件
    ]


class OesQryOrdRsp(SimpleStructure):
    _fields_ = [
        ('rsp_head', OesQryRspHead),  # 查询应答消息头
        ('qry_items', OesOrdItem * OES_MAX_ORD_ITEM_CNT_PER_PACK),  # 委托信息数组
    ]


OesTrdItem = OesTrdCnfm


class OesQryTrdReq(SimpleStructure):
    _fields_ = [
        ('req_head', OesQryReqHead),  # 查询请求消息头
        ('qry_filter', OesQryTrdFilter),  # 查询过滤条件
    ]


class OesQryTrdRsp(SimpleStructure):
    _fields_ = [
        ('rsp_head', OesQryRspHead),  # 查询应答消息头
        ('qry_items', OesTrdItem * OES_MAX_TRD_ITEM_CNT_PER_PACK),  # 成交信息数组
    ]


class OesQryCashAssetReq(SimpleStructure):
    _fields_ = [
        ('req_head', OesQryReqHead),  # 查询请求消息头
        ('qry_filter', OesQryCashAssetFilter),  # 查询过滤条件
    ]


class OesQryCashAssetRsp(SimpleStructure):
    _fields_ = [
        ('rsp_head', OesQryRspHead),  # 查询应答消息头
        ('qry_items', OesCashAssetItem * OES_MAX_CASH_ASSET_ITEM_CNT_PER_PACK),  # 客户资金信息数组
    ]


class OesQryCounterCashReq(SimpleStructure):
    _fields_ = [
        ('cash_acct_id', c_char * OES_CASH_ACCT_ID_MAX_LEN),  # 资金账号, 必输项
    ]


class OesQryCounterCashRsp(SimpleStructure):
    _fields_ = [
        ('counter_cash_item', OesCounterCashItem),  # 主柜资金信息
    ]


class OesQryStkHoldingReq(SimpleStructure):
    _fields_ = [
        ('req_head', OesQryReqHead),  # 查询请求消息头
        ('qry_filter', OesQryStkHoldingFilter),  # 查询过滤条件
    ]


class OesQryStkHoldingRsp(SimpleStructure):
    _fields_ = [
        ('rsp_head', OesQryRspHead),  # 查询应答消息头
        ('qry_items', OesStkHoldingItem * OES_MAX_HOLDING_ITEM_CNT_PER_PACK),  # 持仓信息数组
    ]


OesCustItem = OesCustBaseInfo


class OesQryCustReq(SimpleStructure):
    _fields_ = [
        ('req_head', OesQryReqHead),  # 查询请求消息头
        ('qry_filter', OesQryCustFilter),  # 查询过滤条件
    ]


class OesQryCustRsp(SimpleStructure):
    _fields_ = [
        ('rsp_head', OesQryRspHead),  # 查询应答消息头
        ('qry_items', OesCustItem * OES_MAX_CUST_ITEM_CNT_PER_PACK),  # 持仓信息数组
    ]


class OesQryInvAcctReq(SimpleStructure):
    _fields_ = [
        ('req_head', OesQryReqHead),  # 查询请求消息头
        ('qry_filter', OesQryInvAcctFilter),  # 查询过滤条件
    ]


class OesQryInvAcctRsp(SimpleStructure):
    _fields_ = [
        ('rsp_head', OesQryRspHead),  # 查询应答消息头
        ('qry_items', OesInvAcctItem * OES_MAX_INV_ACCT_ITEM_CNT_PER_PACK),  # 证券账户信息数组
    ]


class OesQryCommissionRateReq(SimpleStructure):
    _fields_ = [
        ('req_head', OesQryReqHead),  # 查询请求消息头
        ('qry_filter', OesQryCommissionRateFilter),  # 查询过滤条件
    ]


class OesQryCommissionRateRsp(SimpleStructure):
    _fields_ = [
        ('rsp_head', OesQryRspHead),  # 查询应答消息头
        ('qry_items', OesCommissionRateItem * OES_MAX_COMMS_RATE_ITEM_CNT_PER_PACK),  # 客户佣金信息数组
    ]


OesFundTransferSerialItem = OesFundTrsfReport


class OesQryFundTransferSerialReq(SimpleStructure):
    _fields_ = [
        ('req_head', OesQryReqHead),  # 查询请求消息头
        ('qry_filter', OesQryFundTransferSerialFilter),  # 查询过滤条件
    ]


class OesQryFundTransferSerialRsp(SimpleStructure):
    _fields_ = [
        ('rsp_head', OesQryRspHead),  # 查询应答消息头
        ('qry_items', OesFundTransferSerialItem * OES_MAX_FUND_TRSF_ITEM_CNT_PER_PACK),  # 客户佣金信息数组
    ]


OesLotWinningItem = OesLotWinningBaseInfo


class OesQryLotWinningReq(SimpleStructure):
    _fields_ = [
        ('req_head', OesQryReqHead),  # 查询请求消息头
        ('qry_filter', OesQryLotWinningFilter),  # 查询过滤条件
    ]


class OesQryLotWinningRsp(SimpleStructure):
    _fields_ = [
        ('rsp_head', OesQryRspHead),  # 查询应答消息头
        ('qry_items', OesLotWinningItem * OES_MAX_LOG_WINNING_ITEM_CNT_PER_PACK),  # 新股认购、中签信息数组
    ]


OesIssueItem = OesIssueBaseInfo


class OesQryIssueReq(SimpleStructure):
    _fields_ = [
        ('req_head', OesQryReqHead),  # 查询请求消息头
        ('qry_filter', OesQryIssueFilter),  # 查询过滤条件
    ]


class OesQryIssueRsp(SimpleStructure):
    _fields_ = [
        ('rsp_head', OesQryRspHead),  # 查询应答消息头
        ('qry_items', OesIssueItem * OES_MAX_ISSUE_ITEM_CNT_PER_PACK),  # 新股认购、中签信息数组
    ]


OesStockItem = OesStockBaseInfo


class OesQryStockReq(SimpleStructure):
    _fields_ = [
        ('req_head', OesQryReqHead),  # 查询请求消息头
        ('qry_filter', OesQryStockFilter),  # 查询过滤条件
    ]


class OesQryStockRsp(SimpleStructure):
    _fields_ = [
        ('rsp_head', OesQryRspHead),  # 查询应答消息头
        ('qry_items', OesStockItem * OES_MAX_STOCK_ITEM_CNT_PER_PACK),  # 现货产品信息数组
    ]


OesEtfItem = OesEtfBaseInfo


class OesQryEtfReq(SimpleStructure):
    _fields_ = [
        ('req_head', OesQryReqHead),  # 查询请求消息头
        ('qry_filter', OesQryEtfFilter),  # 查询过滤条件
    ]


class OesQryEtfRsp(SimpleStructure):
    _fields_ = [
        ('rsp_head', OesQryRspHead),  # 查询应答消息头
        ('qry_items', OesEtfItem * OES_MAX_ETF_ITEM_CNT_PER_PACK),  # ETF申赎产品信息数组
    ]


class OesQryEtfComponentReq(SimpleStructure):
    _fields_ = [
        ('req_head', OesQryReqHead),  # 查询请求消息头
        ('qry_filter', OesQryEtfComponentFilter),  # 查询过滤条件
    ]


class OesQryEtfComponentRsp(SimpleStructure):
    _fields_ = [
        ('rsp_head', OesQryRspHead),  # 查询应答消息头
        ('qry_items', OesEtfComponentItem * OES_MAX_ETF_COMPONENT_ITEM_CNT_PER_PACK),  # EtfComponent成分股信息数组
    ]


class OesQryTradingDayRsp(SimpleStructure):
    _fields_ = [
        ('trading_day', c_int32),  # 交易日
        ('_filler', c_int32),  # 按64位对齐填充域
    ]


class OesQryMarketStateFilter(SimpleStructure):
    _fields_ = [
        ('exch_id', c_uint8),  # 交易所代码 (可选项, 为 0 则匹配所有交易所)
        ('platform_id', c_uint8),  # 交易平台代码 (可选项, 为 0 则匹配所有交易平台)
        ('_filler', c_uint8 * 6),  # 按64位对齐填充域
        ('user_info', c_int64),  # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
    ]


OesMarketStateItem = OesMarketStateInfo


class OesQryMarketStateReq(SimpleStructure):
    _fields_ = [
        ('req_head', OesQryReqHead),  # 查询请求消息头
        ('qry_filter', OesQryMarketStateFilter),  # 查询过滤条件
    ]


class OesQryMarketStateRsp(SimpleStructure):
    _fields_ = [
        ('rsp_head', OesQryRspHead),  # 查询应答消息头
        ('qry_items', OesMarketStateItem * OES_MAX_MKT_STATE_ITEM_CNT_PER_PACK),  # 市场状态信息数组
    ]


class OesBrokerParamsInfo(SimpleStructure):
    _fields_ = [
        ('broker_name', c_char * OES_BROKER_NAME_MAX_LEN),  # 券商名称
        ('broker_phone', c_char * OES_BROKER_PHONE_MAX_LEN),  # 券商联系电话
        ('broker_website', c_char * OES_BROKER_WEBSITE_MAX_LEN),  # 券商网址
        ('api_version', c_char * OES_MAX_VERSION_LEN),  # 当前API协议版本号
        ('_filler1', c_char * 8),  # 为兼容协议而添加的填充域
        ('api_min_version', c_char * OES_MAX_VERSION_LEN),  # API兼容的最低协议版本号
        ('_filler2', c_char * 8),  # 为兼容协议而添加的填充域
        ('client_version', c_char * OES_MAX_VERSION_LEN),  # 客户端最新的版本号
        ('_filler3', c_char * 8),  # 为兼容协议而添加的填充域
        ('change_pwd_limit_time', c_int32),  # 允许客户端修改密码的开始时间 (HHMMSSsss)
        ('min_client_password_len', c_int32),  # 客户端密码允许的最小长度
        ('client_password_strength', c_int32),  # 客户端密码强度级别,密码强度范围[0~4]
        ('_filler4', c_uint8 * 4),  # 按64位对齐填充域
        ('_reserve', c_char * 256),  # 预留的备用字段
    ]


class OesQryBrokerParamsInfoRsp(SimpleStructure):
    _fields_ = [
        ('broker_params', OesBrokerParamsInfo),  # 查询券商参数信息应答
    ]


class OesQryReqMsg(SimpleUnion):
    _fields_ = [
        ('qry_ord', OesQryOrdReq),  # 查询委托信息请求
        ('qry_trd', OesQryTrdReq),  # 查询成交信息请求
        ('qry_cash_asset', OesQryCashAssetReq),  # 查询客户资金信息请求
        ('qry_stk_holding', OesQryStkHoldingReq),  # 查询股票持仓信息请求
        ('qry_cust', OesQryCustReq),  # 查询客户信息请求
        ('qry_inv_acct', OesQryInvAcctReq),  # 查询证券账户请求
        ('qry_comms', OesQryCommissionRateReq),  # 查询客户佣金信息请求
        ('qry_fund_trsf', OesQryFundTransferSerialReq),  # 查询出入金信息请求
        ('qry_lot_winning', OesQryLotWinningReq),  # 查询新股配号、中签信息请求
        ('qry_issue', OesQryIssueReq),  # 查询证券发行信息请求
        ('qry_stock', OesQryStockReq),  # 查询现货产品信息请求
        ('qry_etf', OesQryEtfReq),  # 查询ETF申赎产品信息请求
        ('qry_etf_component', OesQryEtfComponentReq),  # 查询ETF成分股信息请求
        ('qry_mkt_state', OesQryMarketStateReq),  # 查询市场状态信息请求
        ('qry_counter_cash', OesQryCounterCashReq),  # 查询主柜资金信息请求
    ]


class OesApplUpgradeSource(SimpleStructure):
    """应用程序升级源信息"""
    _fields_ = [
        ('ip_address', c_char * OES_MAX_IP_LEN),  # IP地址
        ('protocol', c_char * OES_APPL_UPGRADE_PROTOCOL_MAX_LEN),  # 协议名称
        ('username', c_char * OES_CLIENT_NAME_MAX_LEN),  # 用户名
        ('password', c_char * OES_PWD_MAX_LEN),  # 登录密码
        ('encrypt_method', c_int32),  # 登录密码的加密方法
        ('_filler', c_int32),  # 按64位对齐的填充域
        ('home_path', c_char * SPK_MAX_PATH_LEN),  # 根目录地址
        ('file_name', c_char * SPK_MAX_PATH_LEN),  # 文件名称
    ]


class OesApplUpgradeItem(SimpleStructure):
    """单个应用程序升级信息"""
    _fields_ = [
        ('appl_name', c_char * OES_MAX_COMP_ID_LEN),  # 应用程序名称
        ('min_appl_ver_id', c_char * OES_VER_ID_MAX_LEN),  # 应用程序的最低协议版本号
        ('max_appl_ver_id', c_char * OES_VER_ID_MAX_LEN),  # 应用程序的最高协议版本号
        ('discard_appl_ver_id', c_char * OES_VER_ID_MAX_LEN * OES_APPL_DISCARD_VERSION_MAX_COUNT),  # 废弃的应用版本号列表
        ('discard_ver_count', c_int32),  # 废弃版本号的数目
        ('new_appl_ver_date', c_int32),  # 最新协议版本的日期
        ('new_appl_ver_id', c_char * OES_VER_ID_MAX_LEN),  # 应用程序的最新协议版本号
        ('new_appl_ver_tag', c_char * OES_CLIENT_TAG_MAX_LEN),  # 最新协议版本的标签信息
        ('primary_source', OesApplUpgradeSource),  # 主用升级源配置信息
        ('secondary_source', OesApplUpgradeSource),  # 备用升级源配置信息
    ]


class OesApplUpgradeInfo(SimpleStructure):
    """OES周边应用程序升级信息"""
    _fields_ = [
        ('client_upgrade_info', OesApplUpgradeItem),  # 客户端升级配置信息
        ('c_api_upgrade_info', OesApplUpgradeItem),  # C_API升级配置信息
        ('java_api_upgrade_info', OesApplUpgradeItem),  # JAVA_API升级配置信息
    ]


class OesQryApplUpgradeInfoRsp(SimpleStructure):
    _fields_ = [
        ('appl_upgrade_info', OesApplUpgradeInfo),  # 查询券商参数信息应答
    ]


class OesQryRspMsg(SimpleUnion):
    _fields_ = [
        ('ord_rsp', OesQryOrdRsp),  # 查询委托信息应答
        ('trd_rsp', OesQryTrdRsp),  # 查询成交信息应答
        ('cash_asset_rsp', OesQryCashAssetRsp),  # 查询客户资金信息应答
        ('stk_holding_rsp', OesQryStkHoldingRsp),  # 查询股票持仓信息应答
        ('cust_rsp', OesQryCustRsp),  # 查询客户信息应答
        ('inv_acct_rsp', OesQryInvAcctRsp),  # 查询证券账户应答
        ('comms_rate_rsp', OesQryCommissionRateRsp),  # 查询客户佣金信息应答
        ('fund_trsf_rsp', OesQryFundTransferSerialRsp),  # 查询出入金流水信息应答
        ('lot_winning_rsp', OesQryLotWinningRsp),  # 查询新股配号、中签信息应答
        ('issue_rsp', OesQryIssueRsp),  # 查询证券发行信息应答
        ('stock_rsp', OesQryStockRsp),  # 查询现货产品信息应答
        ('etf_rsp', OesQryEtfRsp),  # 查询ETF申赎产品信息应答
        ('etf_component_rsp', OesQryEtfComponentRsp),  # 查询ETF成分股信息应答
        ('trading_day', OesQryTradingDayRsp),  # 查询当前交易日信息应答
        ('mkt_state_rsp', OesQryMarketStateRsp),  # 查询市场状态信息应答
        ('client_overview', OesClientOverview),  # 客户端总览信息
        ('counter_cash_rsp', OesQryCounterCashRsp),  # 客户主柜资金信息
        ('broker_params_rsp', OesQryBrokerParamsInfoRsp),  # 查询券商参数信息应答
        ('appl_upgrade_rsp', OesQryApplUpgradeInfoRsp),  # 周边应用升级信息
    ]


OesApiSessionInfo = SGeneralClientChannel


class SGeneralClientAddrInfo(SimpleStructure):
    _fields_ = [
        ('uri', c_char * SPK_MAX_URI_LEN),  # 地址信息
        ('target_comp_id', c_char * GENERAL_CLI_MAX_COMP_ID_LEN),  # 接收方代码
        ('username', c_char * GENERAL_CLI_MAX_NAME_LEN),  # 用户名
        ('password', c_char * GENERAL_CLI_MAX_PWD_LEN),  # 密码
        ('host_num', c_uint8),  # 主机编号
        ('_filler', c_uint8 * 7),  # 按64位对齐的填充域
    ]


OesApiAddrInfo = SGeneralClientAddrInfo


class SSocketOptionConfig(SimpleStructure):
    _fields_ = [
        ('so_rcvbuf', c_int32),
        ('so_sndbuf', c_int32),
        ('tcp_nodelay', c_int8),
        ('quick_ack', c_int8),
        ('mcast_ttl_num', c_int8),
        ('mcast_loopback_disabled', c_int8),
        ('so_backlog', c_uint16),
        ('conn_timeout_ms', c_uint16),
        ('keep_idle', c_int16),
        ('keep_intvl', c_int16),
        ('keepalive', c_int8),
        ('keep_cnt', c_int8),
        ('_filler', c_int8 * 6),
        ('local_sending_port', c_int32),
        ('local_sending_ip', c_char * (SPK_MAX_IP_LEN + 4)),
        ('mcast_interface_ip', c_char * (SPK_MAX_IP_LEN + 4)),
    ]


class SGeneralClientRemoteCfg(SimpleStructure):
    _fields_ = [
        ('addr_cnt', c_int32),  # 服务器地址的数量
        ('heart_bt_int', c_int32),  # 心跳间隔,单位为秒
        ('cluster_type', c_uint8),  # 服务器集群的集群类型 (0:对等节点, 1:复制集)
        ('cl_env_id', c_int8),  # 客户端环境号
        ('target_set_num', c_uint8),  # 远程主机的集群号
        ('_filler', c_uint8 * 5),  # 按64位对齐的填充域
        ('sender_comp_id', c_char * GENERAL_CLI_MAX_COMP_ID_LEN),  # 发送方代码
        ('target_comp_id', c_char * GENERAL_CLI_MAX_COMP_ID_LEN),  # 接收方代码
        ('username', c_char * GENERAL_CLI_MAX_NAME_LEN),  # 用户名
        ('password', c_char * GENERAL_CLI_MAX_PWD_LEN),  # 密码
        ('addr_list', SGeneralClientAddrInfo * GENERAL_CLI_MAX_REMOTE_CNT),  # 服务器地址列表
        ('socket_opt', SSocketOptionConfig),  # 套接口选项配置
    ]


OesApiRemoteCfg = SGeneralClientRemoteCfg


class SGeneralClientAddrCursor(SimpleStructure):
    _fields_ = [
        ('addr_cnt', c_int32),  # 服务器地址的数量
        ('last_connect_idx', c_int32),  # 最近一次连接的主机地址顺序号
        ('last_connect_result', c_int32),  # 最近一次连接的连接结果
        ('last_host_num', c_uint8),  # 最近一次连接的主机编号
        ('is_last', c_uint8),  # 是否遍历完成
        ('_filler1', c_uint8 * 2),  # 按64位对齐的填充域
        ('socket_fd', SocketFd),  # Socket描述符
        ('p_last_addr_info', POINTER(SGeneralClientAddrInfo)),  # 最近一次连接的主机地址信息
        ('_filler2', c_void_p),  # 按64位对齐的填充域
    ]


OesApiAddrCursor = SGeneralClientAddrCursor


class OesApiSubscribeInfo(SimpleStructure):
    _fields_ = [
        ('cl_env_id', c_int8),  # 待订阅的客户端环境号
        ('_filler', c_uint8 * 3),  # 按64位对齐的填充域
        ('rpt_types', c_int32),  # 待订阅的回报消息种类
    ]


class OesApiClientCfg(SimpleStructure):
    _fields_ = [
        ('ord_channel_cfg', OesApiRemoteCfg),  # 委托服务配置
        ('rpt_channel_cfg', OesApiRemoteCfg),  # 回报服务配置
        ('qry_channel_cfg', OesApiRemoteCfg),  # 查询服务配置
        ('subscribe_info', OesApiSubscribeInfo),  # 回报订阅参数
    ]

