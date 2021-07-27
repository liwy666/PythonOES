# -*- coding: utf-8 -*-
import sys
import struct
from enum import Enum
from ctypes import Structure, Union
from ctypes import sizeof, POINTER
from ctypes import c_char, c_char_p, c_void_p
from ctypes import c_int8, c_int16, c_int32, c_int64
from ctypes import c_uint8, c_uint16, c_uint32, c_uint64


OES_CLIENT_NAME_MAX_LEN = 32  # 客户端名称最大长度
OES_CLIENT_DESC_MAX_LEN = 32  # 客户端说明最大长度
OES_CLIENT_TAG_MAX_LEN = 32  # 客户端标签最大长度
OES_PWD_MAX_LEN = 40  # 密码最大长度
OES_VER_ID_MAX_LEN = 32  # 协议版本号的最大长度
OES_MAX_COMP_ID_LEN = 32  # 发送方/接收方代码字符串的最大长度
OES_MAX_CLIENT_ENVID_COUNT = 128  # 系统支持的最大客户端环境号数量
OES_MAX_BATCH_ORDERS_COUNT = 500  # 批量委托的每批次最大委托数量
OES_CUST_ID_MAX_LEN = 16  # 客户代码最大长度
OES_CUST_ID_REAL_LEN = 12  # 客户代码真实长度
OES_CUST_NAME_MAX_LEN = 64  # 客户名称最大长度
OES_CASH_ACCT_ID_MAX_LEN = 16  # 资金账户代码最大长度
OES_CASH_ACCT_ID_REAL_LEN = 12  # 资金账户代码的实际长度
OES_INV_ACCT_ID_MAX_LEN = 16  # 股东账户代码最大长度
OES_INV_ACCT_ID_REAL_LEN = 10  # 股东账户代码实际长度
OES_BRANCH_ID_MAX_LEN = 8  # 营业部代码最大长度
OES_BRANCH_ID_REAL_LEN = 6  # 营业部代码实际长度
OES_BANK_NO_MAX_LEN = 8  # 银行代码最大长度
OES_BANK_NO_REAL_LEN = 4  # 银行代码实际使用长度
OES_PBU_MAX_LEN = 8  # PBU域长度
OES_PBU_REAL_LEN = 6  # PBU实际长度
OES_SECURITY_ID_MAX_LEN = 16  # 证券代码的最大长度
OES_STOCK_ID_REAL_LEN = 6  # 实际的股票产品代码长度
OES_OPTION_ID_REAL_LEN = 8  # 实际的期权产品代码长度
OES_SECURITY_NAME_MAX_LEN = 24  # 证券名称长度
OES_SECURITY_NAME_REAL_LEN = 20  # 证券名称实际长度
OES_SECURITY_LONG_NAME_MAX_LEN = 80  # 证券长名称长度
OES_SECURITY_ENGLISH_NAME_MAX_LEN = 48  # 证券英文名称长度
OES_SECURITY_ISIN_CODE_MAX_LEN = 16  # 证券ISIN代码长度
OES_EXCH_ORDER_ID_MAX_LEN = 17  # 交易所订单编号的最大长度
OES_EXCH_ORDER_ID_SSE_LEN = 8  # 交易所订单编号的实际长度 (上证)
OES_EXCH_ORDER_ID_SZSE_LEN = 16  # 交易所订单编号的实际长度 (深证)
OES_MAX_IP_LEN = 16  # 点分十进制的IPv4, 字符串的最大长度
OES_MAX_MAC_LEN = 20  # MAC地址字符串的最大长度
OES_MAX_MAC_ALGIN_LEN = 24  # MAC地址字符串的最大长度(按64位对齐的长度)
OES_MAX_DRIVER_ID_LEN = 21  # 设备序列号字符串的最大长度
OES_MAX_DRIVER_ID_ALGIN_LEN = 24  # 设备序列号字符串的最大长度(按64位对齐的长度)
OES_MAX_TEST_REQ_ID_LEN = 32  # 测试请求标识符的最大长度
OES_MAX_SENDING_TIME_LEN = 22  # 发送时间字段(YYYYMMDD-HH:mm:SS.sss (*C21))的最大长度
OES_REAL_SENDING_TIME_LEN = 21  # 发送时间字段(YYYYMMDD-HH:mm:SS.sss (*C21))的实际有效数据长度
OES_MAX_ERROR_INFO_LEN = 64  # 错误描述信息长度
OES_MAX_ALLOT_SERIALNO_LEN = 64  # 主柜调拨流水号信息长度
OES_CASH_UNIT = 10000  # 资金的转换单位
OES_FUND_TRSF_UNIT = 100  # 出入金的金额单位
OES_FEE_RATE_UNIT = 10000000  # 费用 (佣金/固定费用) 的费率单位
OES_ETF_CASH_RATIO_UNIT = 100000  # ETF使用的资金百分比单位
OES_BOND_INTEREST_UNIT = 100000000  # 债券每张应计利息的转换单位
OES_STK_POSITION_LIMIT_UNIT = 1000000  # 个股持仓比例阀值百分比单位
OES_AUCTION_UP_DOWN_RATE_UNIT = 100  # 产品有效竞价范围涨跌幅度转换单位
OES_MAX_BS_PRICE = 10000 * OES_CASH_UNIT  # 最大买卖价格, 委托价格不能等于或超过此价格
OES_BROKER_NAME_MAX_LEN = 128  # 券商名称最大长度
OES_BROKER_PHONE_MAX_LEN = 32  # 券商联系电话最大长度
OES_BROKER_WEBSITE_MAX_LEN = 256  # 券商网址最大长度
OES_APPL_DISCARD_VERSION_MAX_COUNT = 5  # 周边应用废弃版本数目的最大个数
OES_APPL_UPGRADE_PROTOCOL_MAX_LEN = 32  # 周边应用升级协议名称的最大长度
OES_MAX_ORD_ITEM_CNT_PER_PACK = 30  # 每条查询应答报文中委托信息的最大数量
OES_MAX_TRD_ITEM_CNT_PER_PACK = 30  # 每条查询应答报文中成交信息的最大数量
OES_MAX_CASH_ASSET_ITEM_CNT_PER_PACK = 30  # 每条查询应答报文中客户资金信息的最大数量
OES_MAX_HOLDING_ITEM_CNT_PER_PACK = 30  # 每条查询应答报文中持仓信息的最大数量
OES_MAX_CUST_ITEM_CNT_PER_PACK = 30  # 每条查询应答报文中客户信息的最大数量
OES_MAX_INV_ACCT_ITEM_CNT_PER_PACK = 30  # 每条查询应答报文中证券账户信息的最大数量
OES_MAX_COMMS_RATE_ITEM_CNT_PER_PACK = 50  # 每条查询应答报文中客户佣金信息的最大数量
OES_MAX_FUND_TRSF_ITEM_CNT_PER_PACK = 30  # 每条查询应答报文中出入金流水记录的最大数量
OES_MAX_LOG_WINNING_ITEM_CNT_PER_PACK = 30  # 每条查询应答报文中新股认购、中签信息的最大数量
OES_MAX_ISSUE_ITEM_CNT_PER_PACK = 30  # 每条查询应答报文中证券发行信息的最大数量
OES_MAX_STOCK_ITEM_CNT_PER_PACK = 30  # 每条查询应答报文中现货产品信息的最大数量
OES_MAX_ETF_ITEM_CNT_PER_PACK = 30  # 每条查询应答报文中ETF申赎产品信息的最大数量
OES_MAX_ETF_COMPONENT_ITEM_CNT_PER_PACK = 30  # 每条查询应答报文中ETF成份证券的最大数量
OES_MAX_OPTION_ITEM_CNT_PER_PACK = 30  # 每条查询应答报文中期权产品的最大数量
OES_MAX_MKT_STATE_ITEM_CNT_PER_PACK = 30  # 每条查询应答报文中市场状态的最大数量
OES_MAX_CUST_PER_CLIENT = 1  # 客户端对应的最大客户数量
OES_APPL_VER_ID = "0.15.12"  # 当前采用的协议版本号
# 当前采用的协议版本号数值
# - 版本号数值的格式为 10 位整型数值, 形如: 1AABBCCDDX, 其中:
#   - AA 为主版本号
#   - BB 为副版本号
#   - CC 为发布号
#   - DD 为构建号
#   - X  0, 表示不带时间戳的正常版本; 1, 表示带时间戳的延迟测量版本
OES_APPL_VER_VALUE = 1001512001
OES_MIN_APPL_VER_ID = "0.15.5"  # 兼容的最低协议版本号
OES_APPL_NAME = "OES"  # 应用名称

# 最大路径长度
SPK_MAX_PATH_LEN = 256
# 默认的SOCKET超时时间 (毫秒)
SPK_DEFAULT_SO_TIMEOUT_MS = 15000
SPK_CACHE_LINE_SIZE = 64  # CPU缓存行大小
# 错误信息的最大长度
SPK_MAX_ERRMSG_LEN = 96

SPK_MAX_IP_LEN = 16  # IP字符串的最大长度
SPK_MAX_IPV6_LEN = 40  # IPv6字符串的最大长度
SPK_MAX_URI_LEN = 128  # URI最大长度
SPK_MAX_PROTOCOL_NAME_LEN = 32  # 通信协议类型名称的最大长度
SPK_MAX_PROTOCOL_MEMO_LEN = 64  # 通信协议类型描述的最大长度
SPK_MAC_SEGS_CNT = 6  # 十六进制整数格式的MAC地址的字节数
SPK_MAX_MAC_LEN = 20  # MAC地址字符串的最大长度
SPK_MAX_MAC_ALGIN_LEN = 24  # MAC地址字符串的最大长度(按64位对齐的长度)
SPK_MAX_DRIVER_ID_LEN = 24  # 设备序列号字符串的最大长度
SPK_MAX_SO_BACKLOG = 128  # 最大同时连接请求数
SPK_DEFAULT_SO_BACKLOG = SPK_MAX_SO_BACKLOG  # 默认的最大同时连接请求数
SPK_DEFAULT_SO_RCVBUF = 1024  # 默认的接收缓存大小（单位: K）
SPK_DEFAULT_SO_SNDBUF = 1024  # 默认的发送缓存大小（单位: K）
SPK_DEFAULT_TCP_NODELAY = 1  # 默认的SO_NODELAY取值
SPK_DEFAULT_SO_REUSEADDR = 1  # 默认的SO_REUSEADDR取值
SPK_DEFAULT_CONN_TIMEOUT_MS = 10000  # 默认的连接操作的超时时间 (毫秒)
SPK_MAX_CONN_TIMEOUT_MS = 60000  # 最大的连接操作的超时时间 (毫秒)
SPK_SHORT_SO_TIMEOUT_MS = 5000  # 常用的较短的SOCKET超时时间 (毫秒)
SPK_SHORTEST_SO_TIMEOUT_MS = 1000  # 常用的最短的SOCKET超时时间 (毫秒)
SPK_LONG_SO_TIMEOUT_MS = 30000  # 常用的较长的SOCKET超时时间 (毫秒)
SPK_LONGEST_SO_TIMEOUT_MS = 60000  # 常用的最长的SOCKET超时时间 (毫秒)
SPK_DEFAULT_SO_KEEPALIVE = 1  # 默认的SO_KEEPALIVE取值
SPK_DEFAULT_TCP_KEEPIDLE = 300  # 默认的TCP_KEEPIDLE取值
SPK_DEFAULT_TCP_KEEPINTVL = 30  # 默认的TCP_KEEPINTVL取值
SPK_DEFAULT_TCP_KEEPCNT = 9  # 默认的TCP_KEEPCNT取值

GENERAL_CLI_DEFAULT_HEARTBEAT_INTERVAL = 30  # 默认的心跳间隔(秒)
GENERAL_CLI_MIN_HEARTBEAT_INTERVAL = 5  # 最小的心跳间隔(秒)
GENERAL_CLI_MAX_HEARTBEAT_INTERVAL = 3600  # 最大的心跳间隔(秒)
GENERAL_CLI_DEFAULT_UDP_HEARTBEAT_INTERVAL = 30  # 默认的UDP连接的心跳间隔(秒)
GENERAL_CLI_MAX_UDP_ALIVE_INTERVAL = 180  # 最大的UDP连接的心跳间隔/最大空闲时间(秒)
GENERAL_CLI_DEFAULT_TIMEOUT_MS = SPK_DEFAULT_SO_TIMEOUT_MS  # 默认的超时时间(毫秒)
GENERAL_CLI_MAX_RSPMSG_SIZE = 4 * 1024 * 1024  # 最大的单个应答消息大小
GENERAL_CLI_DEFAULT_TCP_RECVBUF_SIZE = 8 * 1024 * 1024  # 默认的TCP接收缓存大小
GENERAL_CLI_DEFAULT_UDP_RECVBUF_SIZE = 4 * 1024 * 1024  # 默认的UDP接收缓存大小
GENERAL_CLI_MIN_RECVBUF_SURPLUS_SIZE = 128 * 1024  # 最小的接收缓存剩余可用空间大小
GENERAL_CLI_DEFAULT_CODEC_BUF_SIZE = 512 * 1024  # 默认的编解码缓存大小
GENERAL_CLI_MAX_HOST_NUM = 9  # 最大的主机编号
GENERAL_CLI_MAX_REMOTE_CNT = 8  # 可连接的最大远程服务器数量
GENERAL_CLI_MAX_CHANNEL_GROUP_SIZE = 256  # 连接通道组的最大连接数量
GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE = 128  # 会话信息中用于存储自定义数据的扩展空间大小
GENERAL_CLI_MAX_NAME_LEN = 32  # 客户端名称最大长度
GENERAL_CLI_MAX_DESC_LEN = 32  # 客户端说明最大长度
GENERAL_CLI_MAX_PWD_LEN = 40  # 密码最大长度
GENERAL_CLI_MAX_COMP_ID_LEN = 32  # 发送方/接收方代码字符串的最大长度

OESAPI_CFG_DEFAULT_SECTION = "oes_client"  # 默认的主配置区段名称
OESAPI_CFG_DEFAULT_SECTION_LOGGER = "log"  # 默认的日志配置区段名称
OESAPI_CFG_DEFAULT_KEY_ORD_ADDR = "ordServer"  # 默认的委托申报配置项名称
OESAPI_CFG_DEFAULT_KEY_RPT_ADDR = "rptServer"  # 默认的执行报告配置项名称
OESAPI_CFG_DEFAULT_KEY_QRY_ADDR = "qryServer"  # 默认的查询服务配置项名称
OESAPI_DEFAULT_STRING_DELIM = ",;| = \t\r\n"  # 默认的消息类型列表等字符串分隔符

if sys.platform == 'win32':
    if struct.calcsize("P") * 8 == 64:
        CONNECT_DESCRIPTOR_SET_SIZE = 4096
        TIMESPEC_SIZE = 16
        SPK_SOCKET = c_int64
    else:
        CONNECT_DESCRIPTOR_SET_SIZE = 2048
        TIMESPEC_SIZE = 8
        SPK_SOCKET = c_int32
else:
    CONNECT_DESCRIPTOR_SET_SIZE = 2048
    TIMESPEC_SIZE = 16
    SPK_SOCKET = c_int32


# 交易所代码定义
class eOesExchangeIdT(Enum):
    OES_EXCH_UNDEFINE = 0  # 未定义的交易所代码
    OES_EXCH_SSE = 1  # 上海证券交易所
    OES_EXCH_SZSE = 2  # 深圳证券交易所
    __MAX_OES_EXCH = 3
    # 上海证券交易所 @deprecated 已过时, 请使用 OES_EXCH_SSE
    OES_EXCHANGE_TYPE_SSE = OES_EXCH_SSE
    # 深圳证券交易所 @deprecated 已过时, 请使用 OES_EXCH_SZSE
    OES_EXCHANGE_TYPE_SZSE = OES_EXCH_SZSE
    __OES_EXCH_ID_MAX_ALIGNED4 = 4  # 交易所代码最大值 (按4字节对齐的大小)
    __OES_EXCH_ID_MAX_ALIGNED8 = 8  # 交易所代码最大值 (按8字节对齐的大小)


# 市场类型定义
class eOesMarketIdT(Enum):
    OES_MKT_UNDEFINE = 0  # 未定义的市场类型
    OES_MKT_SH_ASHARE = 1  # 上海A股
    OES_MKT_SZ_ASHARE = 2  # 深圳A股
    OES_MKT_SH_OPTION = 3  # 上海期权
    __OES_MKT_ID_MAX = 4  # 市场类型最大值
    __OES_MKT_ID_MAX_ALIGNED4 = 4  # 市场类型最大值 (按4字节对齐的大小)
    __OES_MKT_ID_MAX_ALIGNED8 = 8  # 市场类型最大值 (按8字节对齐的大小)
    # 扩展的外部市场定义 (仅用于查询)
    OES_MKT_EXT_HK = 11  # 港股, 仅用于跨沪深港ETF的成分股查询
    __OES_MKT_EXT_MAX = 12  # 扩展市场类型的最大值
    # 未定义的市场类型 @deprecated 已过时, 请使用 OES_MKT_UNDEFINE
    OES_MKT_ID_UNDEFINE = OES_MKT_UNDEFINE
    # 上海A股 @deprecated 已过时, 请使用 OES_MKT_SH_ASHARE
    OES_MKT_ID_SH_A = OES_MKT_SH_ASHARE
    # 深圳A股 @deprecated 已过时, 请使用 OES_MKT_SZ_ASHARE
    OES_MKT_ID_SZ_A = OES_MKT_SZ_ASHARE
    # 上海期权 @deprecated 已过时, 请使用 OES_MKT_SH_OPTION
    OES_MKT_ID_SH_OPT = OES_MKT_SH_OPTION


# 交易平台类型定义
class eOesPlatformIdT(Enum):
    OES_PLATFORM_UNDEFINE = 0  # 未定义的交易平台类型
    OES_PLATFORM_CASH_AUCTION = 1  # 现货集中竞价交易平台
    OES_PLATFORM_FINANCIAL_SERVICES = 2  # 综合金融服务平台
    OES_PLATFORM_NON_TRADE = 3  # 非交易处理平台
    OES_PLATFORM_DERIVATIVE_AUCTION = 4  # 衍生品集中竞价交易平台
    __OES_PLATFORM_ID_MAX = 5  # 平台号的最大值
    __OES_PLATFORM_ID_MAX_ALIGNED8 = 8  # 平台号的最大值 (按8字节对齐的大小)


# 市场状态定义
class eOesMarketStateT(Enum):
    OES_MKT_STATE_UNDEFINE = 0  # 未定义的市场状态
    OES_MKT_STATE_PRE_OPEN = 1  # 未开放 (PreOpen)
    OES_MKT_STATE_OPEN_UP_COMING = 2  # 即将开放 (OpenUpComing)
    OES_MKT_STATE_OPEN = 3  # 开放 (Open)
    OES_MKT_STATE_HALT = 4  # 暂停开放 (Halt)
    OES_MKT_STATE_CLOSE = 5  # 关闭 (Close)
    __OES_MKT_STATE_MAX = 6  # 市场状态最大值


# OES 竞价时段定义
class eOesTrdSessTypeT(Enum):
    OES_TRD_SESS_TYPE_O = 0  # 开盘集合竞价时段
    OES_TRD_SESS_TYPE_T = 1  # 连续竞价时段
    OES_TRD_SESS_TYPE_C = 2  # 收盘集合竞价
    __OES_TRD_SESS_TYPE_MAX = 3  # 时段类型最大值 (时段类型数量)


# 产品类型 (high-level category)
class eOesProductTypeT(Enum):
    OES_PRODUCT_TYPE_UNDEFINE = 0  # 未定义的产品类型
    OES_PRODUCT_TYPE_EQUITY = 1  # 普通股票/存托凭证/债券/基金/科创板
    OES_PRODUCT_TYPE_BOND_STD = 2  # 逆回购标准券
    OES_PRODUCT_TYPE_IPO = 3  # 新股认购
    OES_PRODUCT_TYPE_ALLOTMENT = 4  # 配股认购
    OES_PRODUCT_TYPE_OPTION = 5  # 期权
    __OES_PRODUCT_TYPE_MAX = 6  # 产品类型最大值


# 证券类别
class eOesSecurityTypeT(Enum):
    OES_SECURITY_TYPE_UNDEFINE = 0  # 未定义的证券类型
    OES_SECURITY_TYPE_STOCK = 1  # 股票
    OES_SECURITY_TYPE_BOND = 2  # 债券
    OES_SECURITY_TYPE_ETF = 3  # ETF
    OES_SECURITY_TYPE_FUND = 4  # 基金
    OES_SECURITY_TYPE_OPTION = 5  # 期权
    OES_SECURITY_TYPE_MGR = 9  # 管理类
    __OES_SECURITY_TYPE_MAX = 10  # 证券类型最大值
    __OES_SECURITY_TYPE_NOT_SUPPORT = 100  # 不支持的证券类别


# 证券子类别
class eOesSubSecurityTypeT(Enum):
    OES_SUB_SECURITY_TYPE_UNDEFINE = 0  # 未定义的证券子类型
    __OES_SUB_SECURITY_TYPE_STOCK_MIN = 10  # 股票类证券子类型最小值
    OES_SUB_SECURITY_TYPE_STOCK_ASH = 11  # A股股票, A Share
    OES_SUB_SECURITY_TYPE_STOCK_SME = 12  # 中小板股票, Small & Medium Enterprise (SME) Board
    OES_SUB_SECURITY_TYPE_STOCK_GEM = 13  # 创业板股票, Growth Enterprise Market (GEM)
    OES_SUB_SECURITY_TYPE_STOCK_KSH = 14  # 科创板股票
    OES_SUB_SECURITY_TYPE_STOCK_KCDR = 15  # 科创板存托凭证
    OES_SUB_SECURITY_TYPE_STOCK_CDR = 16  # 存托凭证, Chinese Depository Receipt (CDR)
    OES_SUB_SECURITY_TYPE_STOCK_HLTCDR = 17  # 沪伦通CDR本地交易业务产品
    OES_SUB_SECURITY_TYPE_STOCK_GEMCDR = 18  # 创业板存托凭证
    __OES_SUB_SECURITY_TYPE_STOCK_MAX = 19  # 股票类证券子类型最大值
    __OES_SUB_SECURITY_TYPE_BOND_MIN = 20  # 债券类证券子类型最小值
    OES_SUB_SECURITY_TYPE_BOND_GBF = 21  # 国债
    OES_SUB_SECURITY_TYPE_BOND_CBF = 22  # 企业债
    OES_SUB_SECURITY_TYPE_BOND_CPF = 23  # 公司债
    OES_SUB_SECURITY_TYPE_BOND_CCF = 24  # 可转换债券
    OES_SUB_SECURITY_TYPE_BOND_FBF = 25  # 金融机构发行债券
    OES_SUB_SECURITY_TYPE_BOND_PRP = 26  # 债券质押式回购
    OES_SUB_SECURITY_TYPE_BOND_STD = 27  # 债券标准券
    OES_SUB_SECURITY_TYPE_BOND_EXG = 28  # 可交换债券
    __OES_SUB_SECURITY_TYPE_BOND_MAX = 29  # 债券类证券子类型最大值
    __OES_SUB_SECURITY_TYPE_ETF_MIN = 30  # ETF类证券子类型最小值
    OES_SUB_SECURITY_TYPE_ETF_SINGLE_MKT = 31  # 单市场股票ETF
    OES_SUB_SECURITY_TYPE_ETF_CROSS_MKT = 32  # 跨市场股票ETF
    OES_SUB_SECURITY_TYPE_ETF_BOND = 33  # 实物债券ETF
    OES_SUB_SECURITY_TYPE_ETF_CURRENCY = 34  # 货币ETF
    OES_SUB_SECURITY_TYPE_ETF_CROSS_BORDER = 35  # 跨境ETF
    OES_SUB_SECURITY_TYPE_ETF_GOLD = 36  # 黄金ETF
    OES_SUB_SECURITY_TYPE_ETF_COMMODITY_FUTURES = 37  # 商品期货ETF
    __OES_SUB_SECURITY_TYPE_ETF_MAX = 38  # ETF类证券子类型最大值
    __OES_SUB_SECURITY_TYPE_FUND_MIN = 40  # 基金类证券子类型最小值
    OES_SUB_SECURITY_TYPE_FUND_LOF = 41  # LOF基金
    OES_SUB_SECURITY_TYPE_FUND_CEF = 42  # 封闭式基金, Close-end Fund
    OES_SUB_SECURITY_TYPE_FUND_OEF = 43  # 开放式基金, Open-end Fund
    OES_SUB_SECURITY_TYPE_FUND_GRADED = 44  # 分级子基金
    OES_SUB_SECURITY_TYPE_FUND_REITS = 45  # 基础设施基金
    __OES_SUB_SECURITY_TYPE_FUND_MAX = 46  # 基金类证券子类型最大值
    __OES_SUB_SECURITY_TYPE_OPTION_MIN = 50  # 期权类证券子类型最小值
    OES_SUB_SECURITY_TYPE_OPTION_ETF = 51  # ETF期权
    OES_SUB_SECURITY_TYPE_OPTION_STOCK = 52  # 个股期权
    __OES_SUB_SECURITY_TYPE_OPTION_MAX = 53  # 期权类证券子类型最大值
    __OES_SUB_SECURITY_TYPE_MGR_MIN = 90  # 管理类证券子类型最小值
    OES_SUB_SECURITY_TYPE_MGR_SSE_DESIGNATION = 91  # 指定登记
    OES_SUB_SECURITY_TYPE_MGR_SSE_RECALL_DESIGNATION = 92  # 指定撤消
    OES_SUB_SECURITY_TYPE_MGR_SZSE_DESIGNATION = 93  # 托管注册
    OES_SUB_SECURITY_TYPE_MGR_SZSE_CANCEL_DESIGNATION = 94  # 托管撤消
    __OES_SUB_SECURITY_TYPE_MGR_MAX = 95  # 管理类证券子类型最大值
    __OES_SUB_SECURITY_TYPE_MAX = __OES_SUB_SECURITY_TYPE_MGR_MAX


# 证券级别
class eOesSecurityLevelT(Enum):
    OES_SECURITY_LEVEL_UNDEFINE = 0
    OES_SECURITY_LEVEL_N = 1  # 正常证券
    OES_SECURITY_LEVEL_XST = 2  # *ST股
    OES_SECURITY_LEVEL_ST = 3  # ST股
    OES_SECURITY_LEVEL_P = 4  # 退市整理证券
    OES_SECURITY_LEVEL_T = 5  # 退市转让证券
    OES_SECURITY_LEVEL_U = 6  # 优先股
    OES_SECURITY_LEVEL_B = 7  # B级基金
    __OES_SECURITY_LEVEL_MAX = 8


# 证券风险等级
class eOesSecurityRiskLevelT(Enum):
    OES_RISK_LEVEL_VERY_LOW = 0  # 最低风险
    OES_RISK_LEVEL_LOW = 1  # 低风险
    OES_RISK_LEVEL_MEDIUM_LOW = 2  # 中低风险
    OES_RISK_LEVEL_MEDIUM = 3  # 中风险
    OES_RISK_LEVEL_MEDIUM_HIGH = 4  # 中高风险
    OES_RISK_LEVEL_HIGH = 5  # 高风险
    OES_RISK_LEVEL_VERY_HIGH = 6  # 极高风险
    __OES_RISK_LEVEL_MAX = 7


# 证券停复牌标识类别
class eOesSecuritySuspFlagT(Enum):
    OES_SUSPFLAG_NONE = 0x0  # 无停牌标识
    OES_SUSPFLAG_EXCHANGE = 0x1  # 交易所连续停牌
    OES_SUSPFLAG_BROKER = 0x2  # 券商人工停牌
    __OES_SUSPFLAG_OTHER = 3


# 证券状态的枚举值定义
class eOesSecurityStatusT(Enum):
    OES_SECURITY_STATUS_NONE = 0  # 无特殊状态
    OES_SECURITY_STATUS_FIRST_LISTING = 1 << 0  # 上市首日
    OES_SECURITY_STATUS_RESUME_FIRST_LISTING = 1 << 1  # 恢复上市首日
    OES_SECURITY_STATUS_NEW_LISTING = 1 << 2  # 上市初期
    OES_SECURITY_STATUS_EXCLUDE_RIGHT = 1 << 3  # 除权
    OES_SECURITY_STATUS_EXCLUDE_DIVIDEN = 1 << 4  # 除息
    OES_SECURITY_STATUS_SUSPEND = 1 << 5  # 证券连续停牌
    OES_SECURITY_STATUS_SPECIAL_TREATMENT = 1 << 6  # ST股
    OES_SECURITY_STATUS_X_SPECIAL_TREATMENT = 1 << 7  # *ST股
    OES_SECURITY_STATUS_DELIST_PERIOD = 1 << 8  # 退市整理期
    OES_SECURITY_STATUS_DELIST_TRANSFER = 1 << 9  # 退市转让期


# 证券属性的枚举值定义
class eOesSecurityAttributeT(Enum):
    OES_SECURITY_ATTR_NONE = 0  # 无特殊属性
    OES_SECURITY_ATTR_INNOVATION = 1 << 0  # 创新企业
    OES_SECURITY_ATTR_KSH = 1 << 1  # 科创板标记
    # 科创板ETF/科创板LOF @deprecated 已过时, 请使用 OES_SECURITY_ATTR_KSH
    OES_SECURITY_ATTR_KSH_FUND = OES_SECURITY_ATTR_KSH


# 有效竞价范围限制类型
class eOesAuctionLimitTypeT(Enum):
    OES_AUCTION_LIMIT_TYPE_NONE = 0  # 无竞价范围限制
    OES_AUCTION_LIMIT_TYPE_RATE = 1  # 按幅度限制 (百分比)
    OES_AUCTION_LIMIT_TYPE_ABSOLUTE = 2  # 按价格限制 (绝对值)


# 有效竞价范围基准价类型
class eOesAuctionReferPriceTypeT(Enum):
    OES_AUCTION_REFER_PRICE_TYPE_LAST = 1  # 最近价
    OES_AUCTION_REFER_PRICE_TYPE_BEST = 2  # 对手方最优价


# OES中签、配号记录类型
class eOesLotTypeT(Enum):
    OES_LOT_TYPE_UNDEFINE = 0  # 未定义的中签、配号记录类型
    OES_LOT_TYPE_FAILED = 1  # 配号失败记录
    OES_LOT_TYPE_ASSIGNMENT = 2  # 配号成功记录
    OES_LOT_TYPE_LOTTERY = 3  # 中签记录
    __OES_LOT_TYPE_MAX = 4  # 中签、配号记录类型最大值


# OES配号失败原因
class eOesLotRejReasonT(Enum):
    OES_LOT_REJ_REASON_DUPLICATE = 1  # 配号失败-重复申购
    OES_LOT_REJ_REASON_INVALID_DUPLICATE = 2  # 配号失败-违规重复
    OES_LOT_REJ_REASON_OFFLINE_FIRST = 3  # 配号失败-网下在先
    OES_LOT_REJ_REASON_BAD_RECORD = 4  # 配号失败-不良记录
    OES_LOT_REJ_REASON_UNKNOW = 5  # 配号失败-未知原因


# 产品发行方式
class eOesSecurityIssueTypeT(Enum):
    OES_ISSUE_TYPE_UNDEFINE = 0  # 未定义的发行方式
    OES_ISSUE_TYPE_MKT_QUOTA = 1  # 按市值限额申购 (检查认购限额, 不预冻结资金)
    OES_ISSUE_TYPE_CASH = 2  # 增发资金申购 (不检查认购限额, 预冻结资金)
    OES_ISSUE_TYPE_CREDIT = 3  # 信用申购 (不检查认购限额, 不预冻结资金)


# 订单执行状态定义
class eOesOrdStatusT(Enum):
    OES_ORD_STATUS_UNDEFINE = 0  # 未定义
    OES_ORD_STATUS_NEW = 1  # 新订单 (风控通过)
    OES_ORD_STATUS_DECLARED = 2  # 已确认
    OES_ORD_STATUS_PARTIALLY_FILLED = 3  # 部分成交
    __OES_ORD_STATUS_FINAL_MIN = 4  # 订单终结状态判断标志
    OES_ORD_STATUS_CANCEL_DONE = 5  # 撤单指令已执行 (适用于撤单请求, 并做为撤单请求的终结状态)
    OES_ORD_STATUS_PARTIALLY_CANCELED = 6  # 部分撤单 (部分成交, 剩余撤单)
    OES_ORD_STATUS_CANCELED = 7  # 已撤单
    OES_ORD_STATUS_FILLED = 8  # 已成交 (全部成交)
    __OES_ORD_STATUS_VALID_MAX = 9
    __OES_ORD_STATUS_INVALID_MIN = 10  # 废单判断标志
    OES_ORD_STATUS_INVALID_OES = 11  # OES内部废单
    OES_ORD_STATUS_INVALID_SH_F = 12  # 上证后台判断该订单为废单
    OES_ORD_STATUS_INVALID_SH_E = 13  # 上证前台判断该订单为废单
    OES_ORD_STATUS_INVALID_SH_COMM = 14  # 通信故障
    OES_ORD_STATUS_INVALID_SZ_F = 15  # 深证前台废单
    OES_ORD_STATUS_INVALID_SZ_E = 16  # 深证后台废单
    OES_ORD_STATUS_INVALID_SZ_REJECT = 17  # 深证业务拒绝
    OES_ORD_STATUS_INVALID_SZ_TRY_AGAIN = 18  # 深证平台未开放(需尝试重报)
    __OES_ORD_STATUS_INVALID_MAX = 19
    # 以下订单状态定义已废弃, 只是为了兼容之前的版本而暂时保留
    OES_ORD_STATUS_NORMAL = OES_ORD_STATUS_NEW
    OES_ORD_STATUS_DECLARING = OES_ORD_STATUS_NEW
    __OES_ORD_STATUS_INVALID_OES = OES_ORD_STATUS_INVALID_OES


# 委托类型
#
# 部分缩写解释如下:
#  - LMT (Limit)           : 限价
#  - MTL (Market To Limit) : 剩余转限价(市价)
#  - FAK (Fill and Kill)   : 剩余转撤销(市价)
#  - FOK (Fill or Kill)    : 全部成交或全部撤销(市价/限价)
#
# 上海A股支持类型:
#      1. OES_ORD_TYPE_LMT
#      2. OES_ORD_TYPE_MTL_BEST_5
#      3. OES_ORD_TYPE_FAK_BEST_5
#      4. OES_ORD_TYPE_MTL_BEST (仅适用于科创板)
#      5. OES_ORD_TYPE_MTL_SAMEPARTY_BEST (仅适用于科创板)
#
# 上海期权支持市价类型:
#      1. OES_ORD_TYPE_LMT
#      2. OES_ORD_TYPE_LMT_FOK
#      3. OES_ORD_TYPE_MTL
#      4. OES_ORD_TYPE_FAK
#      5. OES_ORD_TYPE_FOK
#
# 深圳A股支持市价类型:
#      1. OES_ORD_TYPE_LMT
#      2. OES_ORD_TYPE_MTL_BEST
#      3. OES_ORD_TYPE_MTL_SAMEPARTY_BEST
#      4. OES_ORD_TYPE_FAK_BEST_5
#      5. OES_ORD_TYPE_FAK
#      6. OES_ORD_TYPE_FOK
#
# 深圳期权支持市价类型:
#      1. OES_ORD_TYPE_LMT
#      2. OES_ORD_TYPE_LMT_FOK
#      3. OES_ORD_TYPE_MTL_BEST
#      4. OES_ORD_TYPE_MTL_SAMEPARTY_BEST
#      5. OES_ORD_TYPE_FAK_BEST_5
#      6. OES_ORD_TYPE_FAK
#      7. OES_ORD_TYPE_FOK
class eOesOrdTypeT(Enum):
    OES_ORD_TYPE_LMT = 0  # 限价委托
    OES_ORD_TYPE_LMT_FOK = 1  # 限价全部成交或全部撤销委托
    __OES_ORD_TYPE_LMT_MAX = 2
    OES_ORD_TYPE_MTL_BEST_5 = 10  # 最优五档即时成交剩余转限价委托
    OES_ORD_TYPE_MTL_BEST = 11  # 对手方最优价格委托
    OES_ORD_TYPE_MTL_SAMEPARTY_BEST = 12  # 本方最优价格委托
    OES_ORD_TYPE_MTL = 13  # 市价剩余转限价委托
    __OES_ORD_TYPE_MTL_MAX = 14
    OES_ORD_TYPE_FAK_BEST_5 = 20  # 最优五档即时成交剩余撤销委托
    OES_ORD_TYPE_FAK = 21  # 即时成交剩余撤销委托
    __OES_ORD_TYPE_FAK_MAX = 22
    OES_ORD_TYPE_FOK = 30  # 市价全部成交或全部撤销委托
    __OES_ORD_TYPE_FOK_MAX = 31
    __OES_ORD_TYPE_MAX = 32
    __OES_ORD_TYPE_MAX_ALIGNED = 32  # 委托类型最大值 (按8字节对齐的大小)


# 上证委托类型
#
# 部分缩写解释如下:
#  - LMT (Limit)           : 限价
#  - MTL (Market To Limit) : 剩余转限价(市价)
#  - FAK (Fill and Kill)   : 剩余转撤销(市价)
#  - FOK (Fill or Kill)    : 全部成交或全部撤销(市价/限价)
class eOesOrdTypeShT(Enum):
    # 限价, 0
    OES_ORD_TYPE_SH_LMT = eOesOrdTypeT.OES_ORD_TYPE_LMT.value
    # 最优五档即时成交剩余转限价委托, 10
    OES_ORD_TYPE_SH_MTL_BEST_5 = eOesOrdTypeT.OES_ORD_TYPE_MTL_BEST_5.value
    # 对手方最优价格委托(仅适用于科创板), 11
    OES_ORD_TYPE_SH_MTL_BEST = eOesOrdTypeT.OES_ORD_TYPE_MTL_BEST.value
    # 本方最优价格委托(仅适用于科创板), 12
    OES_ORD_TYPE_SH_MTL_SAMEPARTY_BEST = eOesOrdTypeT.OES_ORD_TYPE_MTL_SAMEPARTY_BEST.value
    # 最优五档即时成交剩余撤销委托, 20
    OES_ORD_TYPE_SH_FAK_BEST_5 = eOesOrdTypeT.OES_ORD_TYPE_FAK_BEST_5.value


# 上证期权业务委托类型
#
# 部分缩写解释如下:
#  - LMT (Limit)           : 限价
#  - MTL (Market To Limit) : 剩余转限价(市价)
#  - FAK (Fill and Kill)   : 剩余转撤销(市价)
#  - FOK (Fill or Kill)    : 全部成交或全部撤销(市价/限价)
class eOesOrdTypeShOptT(Enum):
    # 限价, 0
    OES_ORD_TYPE_SHOPT_LMT = eOesOrdTypeT.OES_ORD_TYPE_LMT.value
    # 限价全部成交或全部撤销委托, 1
    OES_ORD_TYPE_SHOPT_LMT_FOK = eOesOrdTypeT.OES_ORD_TYPE_LMT_FOK.value
    # 市价剩余转限价委托, 13
    OES_ORD_TYPE_SHOPT_MTL = eOesOrdTypeT.OES_ORD_TYPE_MTL.value
    # 即时成交剩余撤销委托, 21
    OES_ORD_TYPE_SHOPT_FAK = eOesOrdTypeT.OES_ORD_TYPE_FAK.value
    # 市价全部成交或全部撤销委托, 30
    OES_ORD_TYPE_SHOPT_FOK = eOesOrdTypeT.OES_ORD_TYPE_FOK.value
    # 以下委托类型已废弃, 只是为了兼容之前的版本而暂时保留
    OES_ORD_TYPE_SH_LMT_FOK = OES_ORD_TYPE_SHOPT_LMT_FOK
    OES_ORD_TYPE_SH_FOK = OES_ORD_TYPE_SHOPT_FOK


# 深证委托类型
#
# 部分缩写解释如下:
#  - LMT (Limit)           : 限价
#  - MTL (Market To Limit) : 剩余转限价(市价)
#  - FAK (Fill and Kill)   : 剩余转撤销(市价)
#  - FOK (Fill or Kill)    : 全部成交或全部撤销(市价/限价)
class eOesOrdTypeSzT(Enum):
    # 限价, 0
    OES_ORD_TYPE_SZ_LMT = eOesOrdTypeT.OES_ORD_TYPE_LMT.value
    # 限价全部成交或全部撤销委托(仅适用于期权), 1
    OES_ORD_TYPE_SZ_LMT_FOK = eOesOrdTypeT.OES_ORD_TYPE_LMT_FOK.value
    # 对手方最优价格委托, 11
    OES_ORD_TYPE_SZ_MTL_BEST = eOesOrdTypeT.OES_ORD_TYPE_MTL_BEST.value
    # 本方最优价格委托, 12
    OES_ORD_TYPE_SZ_MTL_SAMEPARTY_BEST = eOesOrdTypeT.OES_ORD_TYPE_MTL_SAMEPARTY_BEST.value
    # 最优五档即时成交剩余撤销委托, 20
    OES_ORD_TYPE_SZ_FAK_BEST_5 = eOesOrdTypeT.OES_ORD_TYPE_FAK_BEST_5.value
    # 即时成交剩余撤销委托, 21
    OES_ORD_TYPE_SZ_FAK = eOesOrdTypeT.OES_ORD_TYPE_FAK.value
    # 市价全部成交或全部撤销委托, 30
    OES_ORD_TYPE_SZ_FOK = eOesOrdTypeT.OES_ORD_TYPE_FOK.value


# 买卖类型
class eOesBuySellTypeT(Enum):
    OES_BS_TYPE_UNDEFINE = 0  # 未定义的买卖类型
    OES_BS_TYPE_BUY = 1  # 买入
    OES_BS_TYPE_SELL = 2  # 卖出
    OES_BS_TYPE_CREATION = 3  # 申购
    OES_BS_TYPE_REDEMPTION = 4  # 赎回
    OES_BS_TYPE_REVERSE_REPO = 6  # 质押式逆回购
    OES_BS_TYPE_SUBSCRIPTION = 7  # 新股/可转债/可交换债认购
    OES_BS_TYPE_ALLOTMENT = 8  # 配股/配债认购
    __OES_BS_TYPE_MAX_SPOT = 9  # 现货交易的买卖类型最大值
    # -------------------------
    __OES_BS_TYPE_MIN_OPTION = 10  # 期权交易的买卖类型最小值
    OES_BS_TYPE_BUY_OPEN = 11  # 期权买入开仓
    OES_BS_TYPE_SELL_CLOSE = 12  # 期权卖出平仓
    OES_BS_TYPE_SELL_OPEN = 13  # 期权卖出开仓
    OES_BS_TYPE_BUY_CLOSE = 14  # 期权买入平仓
    OES_BS_TYPE_COVERED_OPEN = 15  # 期权备兑开仓
    OES_BS_TYPE_COVERED_CLOSE = 16  # 期权备兑平仓
    OES_BS_TYPE_OPTION_EXERCISE = 17  # 期权行权
    OES_BS_TYPE_UNDERLYING_FREEZE = 18  # 期权标的锁定
    OES_BS_TYPE_UNDERLYING_UNFREEZE = 19  # 期权标的解锁
    __OES_BS_TYPE_MAX_OPTION = 20  # 期权交易的买卖类型最大值
    # -------------------------
    OES_BS_TYPE_CANCEL = 30  # 撤单
    __OES_BS_TYPE_MAX_TRADING = 31  # 对外开放的交易类业务的买卖类型最大值
    # -------------------------
    __OES_BS_TYPE_MIN_MGR = 40  # 管理端非交易指令的买卖类型最小值
    OES_BS_TYPE_SSE_DESIGNATION = 41  # 指定登记
    OES_BS_TYPE_SSE_RECALL_DESIGNATION = 42  # 指定撤消
    OES_BS_TYPE_SZSE_DESIGNATION = 43  # 托管注册
    OES_BS_TYPE_SZSE_CANCEL_DESIGNATION = 44  # 托管撤消
    __OES_BS_TYPE_MAX_MGR = 45  # 管理端非交易指令的买卖类型最大值
    __OES_BS_TYPE_MAX = __OES_BS_TYPE_MAX_MGR
    # -------------------------
    # 以下买卖类型定义已废弃, 只是为了兼容之前的版本而暂时保留
    # 仅用于兼容之前版本的质押式逆回购, 不可用于‘信用融券卖出’交易
    OES_BS_TYPE_CREDIT_SELL = OES_BS_TYPE_REVERSE_REPO
    # 已废弃, 即将删除
    OES_BS_TYPE_CREDIT_BUY = 5
    OES_BS_TYPE_B = OES_BS_TYPE_BUY
    OES_BS_TYPE_S = OES_BS_TYPE_SELL
    OES_BS_TYPE_KB = OES_BS_TYPE_CREATION
    OES_BS_TYPE_KS = OES_BS_TYPE_REDEMPTION
    OES_BS_TYPE_CB = OES_BS_TYPE_CREDIT_BUY
    OES_BS_TYPE_CS = OES_BS_TYPE_CREDIT_SELL
    OES_BS_TYPE_BO = OES_BS_TYPE_BUY_OPEN
    OES_BS_TYPE_BC = OES_BS_TYPE_BUY_CLOSE
    OES_BS_TYPE_SO = OES_BS_TYPE_SELL_OPEN
    OES_BS_TYPE_SC = OES_BS_TYPE_SELL_CLOSE
    OES_BS_TYPE_CO = OES_BS_TYPE_COVERED_OPEN
    OES_BS_TYPE_CC = OES_BS_TYPE_COVERED_CLOSE
    OES_BS_TYPE_TE = OES_BS_TYPE_OPTION_EXERCISE
    OES_BS_TYPE_UF = OES_BS_TYPE_UNDERLYING_FREEZE
    OES_BS_TYPE_UU = OES_BS_TYPE_UNDERLYING_UNFREEZE


# 订单的买卖方向 (内部使用)
class eOesOrdDirT(Enum):
    OES_ORD_DIR_BUY = 0  # 买
    OES_ORD_DIR_SELL = 1  # 卖
    __OES_ORD_DIR_MAX = 2  # 买卖方向最大值


# ETF成交回报记录的成交类型
# 上证接口规范 (IS103_ETFInterface_CV14_20130123) 中规定如下:
# - 二级市场记录表示一笔申购/赎回交易连续记录的开始,对一笔申购/赎回交易而言,有且只有一条;
# - 一级市场记录不再表示对应申购/赎回交易连续记录的结束,对一笔申购/赎回交易而言,有且只有一条。
class eOesEtfTrdCnfmTypeT(Enum):
    OES_ETF_TRDCNFM_TYPE_NONE = 0  # 无意义
    OES_ETF_TRDCNFM_TYPE_ETF_FIRST = 1  # 二级市场记录
    OES_ETF_TRDCNFM_TYPE_CMPOENT = 2  # 成份股记录
    OES_ETF_TRDCNFM_TYPE_CASH = 3  # 资金记录
    OES_ETF_TRDCNFM_TYPE_ETF_LAST = 4  # 一级市场记录
    __OES_ETF_TRDCNFM_TYPE_MAX = 5  # ETF成交类型的最大值


# ETF成份证券现金替代标志
class eOesEtfSubFlagT(Enum):
    OES_ETF_SUBFLAG_FORBID_SUB = 0  # 禁止现金替代 (必须有证券)
    OES_ETF_SUBFLAG_ALLOW_SUB = 1  # 可以进行现金替代(先用证券, 如证券不足可用现金替代)
    OES_ETF_SUBFLAG_MUST_SUB = 2  # 必须用现金替代
    OES_ETF_SUBFLAG_SZ_REFUND_SUB = 3  # 该证券为深市证券, 退补现金替代
    OES_ETF_SUBFLAG_SZ_MUST_SUB = 4  # 该证券为深市证券, 必须现金替代
    OES_ETF_SUBFLAG_OTHER_REFUND_SUB = 5  # 非沪深市场成份证券退补现金替代
    OES_ETF_SUBFLAG_OTHER_MUST_SUB = 6  # 非沪深市场成份证券必须现金替代
    OES_ETF_SUBFLAG_HK_REFUND_SUB = 7  # 港市退补现金替代 (仅适用于跨沪深港ETF产品)
    OES_ETF_SUBFLAG_HK_MUST_SUB = 8  # 港市必须现金替代 (仅适用于跨沪深港ETF产品)


# OES执行类型
class eOesExecTypeT(Enum):
    OES_EXECTYPE_UNDEFINE = 0  # 未定义的执行类型
    OES_EXECTYPE_INSERT = 1  # 已接收 (OES已接收)
    OES_EXECTYPE_CONFIRMED = 2  # 已确认 (交易所已确认/出入金主柜台已确认)
    OES_EXECTYPE_CANCELLED = 3  # 已撤单 (原始委托的撤单完成回报)
    OES_EXECTYPE_AUTO_CANCELLED = 4  # 自动撤单 (市价委托发生自动撤单后的委托回报)
    OES_EXECTYPE_REJECT = 5  # 拒绝 (OES拒绝/交易所废单/出入金主柜台拒绝)
    OES_EXECTYPE_TRADE = 6  # 成交 (成交回报)
    __OES_EXECTYPE_MAX = 7  # 执行类型最大值


# 货币类型
class eOesCurrTypeT(Enum):
    OES_CURR_TYPE_RMB = 0  # 人民币
    OES_CURR_TYPE_HKD = 1  # 港币
    OES_CURR_TYPE_USD = 2  # 美元
    __OES_CURR_TYPE_MAX = 3  # 货币种类最大值


# 费用类型标识符
class eOesFeeTypeT(Enum):
    __OES_FEE_TYPE_UNDEFINE = 0  # 未定义的费用类型
    OES_FEE_TYPE_EXCHANGE_STAMP = 0x1  # 交易所固定费用-印花税
    OES_FEE_TYPE_EXCHANGE_TRANSFER = 0x2  # 交易所固定费用-过户费
    OES_FEE_TYPE_EXCHANGE_SETTLEMENT = 0x3  # 交易所固定费用-结算费
    OES_FEE_TYPE_EXCHANGE_TRADE_RULE = 0x4  # 交易所固定费用-交易规费
    OES_FEE_TYPE_EXCHANGE_EXCHANGE = 0x5  # 交易所固定费用-经手费
    OES_FEE_TYPE_EXCHANGE_ADMINFER = 0x6  # 交易所固定费用-证管费
    OES_FEE_TYPE_EXCHANGE_OTHER = 0x7  # 交易所固定费用-其他费
    __OES_FEE_TYPE_EXCHANGE_MAX = 8  # 交易所固定费用最大值
    OES_FEE_TYPE_BROKER_BACK_END = 0x11  # 券商佣金-后台费用


# 费用 (佣金/固定费用) 计算模式
class eOesCalcFeeModeT(Enum):
    OES_CALC_FEE_MODE_AMOUNT = 0  # 按金额
    OES_CALC_FEE_MODE_QTY = 1  # 按份额
    OES_CALC_FEE_MODE_ORD = 2  # 按笔数


# 出入金方向定义
class eOesFundTrsfDirectT(Enum):
    OES_FUND_TRSF_DIRECT_IN = 0  # 转入OES (入金)
    OES_FUND_TRSF_DIRECT_OUT = 1  # 转出OES (出金)


# 出入金转账类型定义
class eOesFundTrsfTypeT(Enum):
    OES_FUND_TRSF_TYPE_OES_BANK = 0  # OES和银行之间转账
    OES_FUND_TRSF_TYPE_OES_COUNTER = 1  # OES和主柜之间划拨资金
    OES_FUND_TRSF_TYPE_COUNTER_BANK = 2  # 主柜和银行之间转账
    __OES_FUND_TRSF_TYPE_MAX = 3  # 出入金转账类型最大值


# 出入金委托状态
class eOesFundTrsfStatusT(Enum):
    OES_FUND_TRSF_STS_UNDECLARED = 0  # 尚未上报到主柜
    OES_FUND_TRSF_STS_DECLARED = 1  # 已上报到主柜
    OES_FUND_TRSF_STS_WAIT_DONE = 2  # 主柜处理完成, 等待事务结束
    OES_FUND_TRSF_STS_DONE = 3  # 出入金处理完成
    __OES_FUND_TRSF_STS_ROLLBACK_MIN = 5  # 废单判断标志
    OES_FUND_TRSF_STS_UNDECLARED_ROLLBACK = 6  # 待回滚(未上报到主柜前)
    OES_FUND_TRSF_STS_DECLARED_ROLLBACK = 7  # 待回滚(已上报到主柜后)
    __OES_FUND_TRSF_STS_INVALID_MIN = 10  # 废单判断标志
    OES_FUND_TRSF_STS_INVALID_OES = 11  # OES内部判断为废单
    OES_FUND_TRSF_STS_INVALID_COUNTER = 12  # 主柜判断为废单
    OES_FUND_TRSF_STS_SUSPENDED = 13  # 挂起状态 (主柜的出入金执行状态未知, 待人工干预处理)


# 业务类型定义
class eOesBusinessTypeT(Enum):
    OES_BUSINESS_TYPE_UNDEFINE = 0x0  # 未定义的业务范围
    OES_BUSINESS_TYPE_STOCK = 0x01  # 现货业务
    OES_BUSINESS_TYPE_OPTION = 0x02  # 期权业务
    OES_BUSINESS_TYPE_CREDIT = 0x04  # 信用业务
    _OES_BUSINESS_TYPE_MAX = 5  # 业务范围最大值 (单一业务)
    _OES_BUSINESS_TYPE_MAX_ALIGNED8 = 0x08  # 业务范围最大值 (单一业务, 按8字节对齐的大小)
    OES_BUSINESS_TYPE_ALL = 0xFF  # 所有业务


# 交易业务范围
# @deprecated 已废弃, 改为使用 eOesBusinessTypeT
class eOesBusinessScopeT(Enum):
    # 未定义的业务范围 @deprecated 已废弃
    OES_BIZ_SCOPE_UNDEFINE = eOesBusinessTypeT.OES_BUSINESS_TYPE_UNDEFINE.value
    # 现货业务 @deprecated 已废弃
    OES_BIZ_SCOPE_STOCK = eOesBusinessTypeT.OES_BUSINESS_TYPE_STOCK.value
    # 期权业务 @deprecated 已废弃
    OES_BIZ_SCOPE_OPTION = eOesBusinessTypeT.OES_BUSINESS_TYPE_OPTION.value
    # 所有业务 @deprecated 已废弃
    OES_BIZ_SCOPE_ALL = eOesBusinessTypeT.OES_BUSINESS_TYPE_ALL.value


# 账户类别定义
# 资金账户类别与证券账户类别定义相同
class eOesAcctTypeT(Enum):
    OES_ACCT_TYPE_NORMAL = 0  # 普通账户
    OES_ACCT_TYPE_CREDIT = 1  # 信用账户
    OES_ACCT_TYPE_OPTION = 2  # 衍生品账户
    __OES_ACCT_TYPE_MAX = 3  # 账户类别最大值
    __OES_ACCT_TYPE_MAX_ALIGNED4 = 4  # 账户类别最大值 (按4字节对齐的大小)
    __OES_ACCT_TYPE_MAX_ALIGNED8 = 8  # 账户类别最大值 (按8字节对齐的大小)


# 资金类型定义
# @see eOesAcctTypeT
class eOesCashTypeT(Enum):
    # 普通账户资金/现货资金
    OES_CASH_TYPE_SPOT = eOesAcctTypeT.OES_ACCT_TYPE_NORMAL.value
    # 信用账户资金/信用资金
    OES_CASH_TYPE_CREDIT = eOesAcctTypeT.OES_ACCT_TYPE_CREDIT.value
    # 衍生品账户资金/期权保证金
    OES_CASH_TYPE_OPTION = eOesAcctTypeT.OES_ACCT_TYPE_OPTION.value
    # 资金类型最大值
    __OES_CASH_TYPE_MAX = eOesAcctTypeT._eOesAcctTypeT__OES_ACCT_TYPE_MAX.value
    # 资金类型最大值 (按4字节对齐的大小)
    __OES_CASH_TYPE_MAX_ALIGNED4 = eOesAcctTypeT._eOesAcctTypeT__OES_ACCT_TYPE_MAX_ALIGNED4.value
    # 资金类型最大值 (按8字节对齐的大小)
    __OES_CASH_TYPE_MAX_ALIGNED8 = eOesAcctTypeT._eOesAcctTypeT__OES_ACCT_TYPE_MAX_ALIGNED8.value
    # 兼容性定义, 即将废弃
    OES_CASH_TYPE_CRE = OES_CASH_TYPE_CREDIT
    OES_CASH_TYPE_OPT = OES_CASH_TYPE_OPTION


# 客户状态/证券帐户/资金账户状态
class eOesAcctStatusT(Enum):
    OES_ACCT_STATUS_NORMAL = 0  # 正常
    OES_ACCT_STATUS_DISABLED = 1  # 非正常
    OES_ACCT_STATUS_LOCKED = 2  # 已锁定


# 交易权限的枚举值定义
class eOesTradingPermissionT(Enum):
    OES_PERMIS_MARKET_ORDER = 1 << 1  # 市价委托
    OES_PERMIS_STRUCTURED_FUND = 1 << 2  # 分级基金适当性
    OES_PERMIS_BOND_QUALIFIED_INVESTOR = 1 << 3  # 债券合格投资者
    OES_PERMIS_XXX4 = 1 << 4  # 融资行权
    OES_PERMIS_DELISTING = 1 << 5  # 退市整理股票
    OES_PERMIS_RISK_WARNING = 1 << 6  # 风险警示股票
    OES_PERMIS_SINGLE_MARKET_ETF = 1 << 7  # 单市场ETF申赎
    OES_PERMIS_CROSS_BORDER_ETF = 1 << 8  # 跨境ETF申赎
    OES_PERMIS_CROSS_MARKET_ETF = 1 << 9  # 跨市场ETF申赎
    OES_PERMIS_CURRENCY_ETF = 1 << 10  # 货币ETF申赎
    OES_PERMIS_GEMCDR = 1 << 11  # 创业板存托凭证
    OES_PERMIS_GEM_REGISTRATION = 1 << 12  # 注册制创业板交易
    OES_PERMIS_GEM_UNREGISTRATION = 1 << 13  # 核准制创业板交易
    OES_PERMIS_SH_HK_STOCK_CONNECT = 1 << 14  # 沪港通
    OES_PERMIS_SZ_HK_STOCK_CONNECT = 1 << 15  # 深港通
    OES_PERMIS_HLTCDR = 1 << 16  # 沪伦通存托凭证
    OES_PERMIS_CDR = 1 << 17  # 存托凭证
    OES_PERMIS_INNOVATION = 1 << 18  # 创新企业股票
    OES_PERMIS_KSH = 1 << 19  # 科创板交易
    OES_PERMIS_BOND_ETF = 1 << 20  # 债券ETF申赎
    OES_PERMIS_GOLD_ETF = 1 << 21  # 黄金ETF申赎
    OES_PERMIS_COMMODITY_FUTURES_ETF = 1 << 22  # 商品期货ETF申赎
    OES_PERMIS_GEM_INNOVATION = 1 << 23  # 创业板创新企业股票
    OES_PERMIS_CONVERTIBLE_BOND = 1 << 24  # 可转换公司债券
    OES_PERMIS_REITS = 1 << 25  # 基础设施基金
    __OES_PERMIS_ALL = 0xFFFFFFFF  # 全部权限
    # 以下定义已废弃, 只是为了兼容之前的版本而暂时保留
    OES_PERMIS_GEM = OES_PERMIS_GEM_UNREGISTRATION


# 交易限制的枚举值定义
class eOesTradingLimitT(Enum):
    OES_LIMIT_BUY = 1 << 1  # 禁止买入
    OES_LIMIT_SELL = 1 << 2  # 禁止卖出
    OES_LIMIT_RECALL_DESIGNATION = 1 << 3  # 禁撤销指定
    OES_LIMIT_DESIGNATION = 1 << 4  # 禁止转托管
    OES_LIMIT_REPO = 1 << 5  # 禁止回购融资
    OES_LIMIT_REVERSE_REPO = 1 << 6  # 禁止质押式逆回购
    OES_LIMIT_SUBSCRIPTION = 1 << 7  # 禁止普通申购 (新股认购)
    OES_LIMIT_CREDIT_BUY = 1 << 8  # 禁止融资买入
    OES_LIMIT_CREDIT_SELL = 1 << 9  # 禁止融券卖出
    __OES_LIMIT_ALL = 0xFFFFFFFF  # 全部限制
    # 现货开仓相关的交易限制集合
    __OES_LIMIT_OPEN_POSITION_STK = OES_LIMIT_BUY | OES_LIMIT_REPO | OES_LIMIT_REVERSE_REPO
    # 现货平仓相关的交易限制集合
    __OES_LIMIT_CLOSE_POSITION_STK = OES_LIMIT_SELL
    # 开仓相关的所有交易限制集合
    __OES_LIMIT_OPEN_POSITION_ALL = __OES_LIMIT_OPEN_POSITION_STK
    # 平仓相关的所有交易限制集合
    __OES_LIMIT_CLOSE_POSITION_ALL = __OES_LIMIT_CLOSE_POSITION_STK


# 投资者适当性管理分类
class eOesQualificationClassT(Enum):
    OES_QUALIFICATION_PUBLIC_INVESTOR = 0  # 公众投资者
    OES_QUALIFICATION_QUALIFIED_INVESTOR = 1  # 合格投资者(个人投资者)
    OES_QUALIFICATION_QUALIFIED_INSTITUTIONAL = 2  # 合格投资者(机构投资者)


# 投资者分类
#
# A类专业投资者: 满足《证券期货投资者适当性管理办法》第八条 (一)、 (二)、 (三) 点,
#      比如证券公司、期货公司、基金管理公司、商业银行、保险公司、发行的理财产品等
# B类专业投资者: 满足《证券期货投资者适当性管理办法》第八条 (四)、 (五) 点,
#      可以是法人或者其他组织、自然人, 满足一定的净资产和金融资产的要求, 具有相关的投资经验
# C类专业投资者: 满足《证券期货投资者适当性管理办法》第十一条 (一)、 (二) 点,
#      由普通投资者主动申请转化而来, 满足一定的净资产和金融资产的要求, 具有相关的投资经验
class eOesInvestorClassT(Enum):
    OES_INVESTOR_CLASS_NORMAL = 0  # 普通投资者
    OES_INVESTOR_CLASS_PROFESSIONAL_A = 1  # A类专业投资者
    OES_INVESTOR_CLASS_PROFESSIONAL_B = 2  # B类专业投资者
    OES_INVESTOR_CLASS_PROFESSIONAL_C = 3  # C类专业投资者
    __OES_INVESTOR_CLASS_MAX = 4  # 投资者分类的最大值


# 客户类型定义
class eOesCustTypeT(Enum):
    OES_CUST_TYPE_PERSONAL = 0  # 个人
    OES_CUST_TYPE_INSTITUTION = 1  # 机构
    OES_CUST_TYPE_PROPRIETARY = 2  # 自营
    OES_CUST_TYPE_PRODUCT = 3  # 产品
    OES_CUST_TYPE_MKT_MAKER = 4  # 做市商
    OES_CUST_TYPE_OTHERS = 5  # 其他
    __OES_CUST_TYPE_MAX = 6  # 客户类型的最大值


# 所有者类型 (内部使用)
class eOesOwnerTypeT(Enum):
    OES_OWNER_TYPE_UNDEFINE = 0  # 未定义
    OES_OWNER_TYPE_PERSONAL = 1  # 个人投资者
    OES_OWNER_TYPE_EXCHANGE = 101  # 交易所
    OES_OWNER_TYPE_MEMBER = 102  # 会员
    OES_OWNER_TYPE_INSTITUTION = 103  # 机构投资者
    OES_OWNER_TYPE_PROPRIETARY = 104  # 自营
    OES_OWNER_TYPE_MKT_MAKER = 105  # 做市商
    OES_OWNER_TYPE_SETTLEMENT = 106  # 结算机构
    __OES_OWNER_TYPE_MAX = 107  # 所有者类型的最大值


# 客户端类型定义 (内部使用)
class eOesClientTypeT(Enum):
    OES_CLIENT_TYPE_UNDEFINED = 0  # 客户端类型-未定义
    OES_CLIENT_TYPE_INVESTOR = 1  # 普通投资人
    OES_CLIENT_TYPE_VIRTUAL = 2  # 虚拟账户 (仅开通行情, 不可交易)


# 客户端状态定义 (内部使用)
class eOesClientStatusT(Enum):
    OES_CLIENT_STATUS_UNACTIVATED = 0  # 未激活 (不加载)
    OES_CLIENT_STATUS_ACTIVATED = 1  # 已激活 (正常加载)
    OES_CLIENT_STATUS_PAUSE = 2  # 已暂停 (正常加载, 不可交易)
    OES_CLIENT_STATUS_SUSPENDED = 3  # 已挂起 (正常加载, 不可交易、不可出入金)
    OES_CLIENT_STATUS_CANCELLED = 4  # 已注销 (不加载)


# 投资者期权等级
class eOesOptInvLevelT(Enum):
    OES_OPT_INV_LEVEL_UNDEFINE = 0  # 未定义 (机构投资者)
    OES_OPT_INV_LEVEL_1 = 1  # 个人投资者-一级交易权限
    OES_OPT_INV_LEVEL_2 = 2  # 个人投资者-二级交易权限
    OES_OPT_INV_LEVEL_3 = 3  # 个人投资者-三级交易权限
    __OES_OPT_INV_LEVEL_MAX = 4  # 期权投资人级别最大值


# 通信消息的消息类型定义
class eOesMsgTypeT(Enum):
    # 交易类消息
    OESMSG_ORD_NEW_ORDER = 0x01  # 0x01/01  委托申报消息
    OESMSG_ORD_CANCEL_REQUEST = 0x02  # 0x02/02  撤单请求消息
    OESMSG_ORD_BATCH_ORDERS = 0x03  # 0x03/03  批量委托消息
    __OESMSG_ORD_MAX = 4  # 最大的委托消息类型
    # 执行报告类消息
    __OESMSG_RPT_MIN = 0x0F  # 0x0F/15  最小的执行报告消息类型
    OESMSG_RPT_MARKET_STATE = 0x10  # 0x10/16  市场状态信息
    OESMSG_RPT_REPORT_SYNCHRONIZATION = 0x11  # 0x11/17  回报同步的应答消息
    OESMSG_RPT_BUSINESS_REJECT = 0x12  # 0x12/18  OES业务拒绝 (因未通过风控检查等原因而被OES拒绝)
    OESMSG_RPT_ORDER_INSERT = 0x13  # 0x13/19  OES委托已生成 (已通过风控检查)
    OESMSG_RPT_ORDER_REPORT = 0x14  # 0x14/20  交易所委托回报 (包括交易所委托拒绝、委托确认和撤单完成通知)
    OESMSG_RPT_TRADE_REPORT = 0x15  # 0x15/21  交易所成交回报
    OESMSG_RPT_FUND_TRSF_REJECT = 0x16  # 0x16/22  出入金委托拒绝
    OESMSG_RPT_FUND_TRSF_REPORT = 0x17  # 0x17/23  出入金委托执行报告
    OESMSG_RPT_CASH_ASSET_VARIATION = 0x18  # 0x18/24  资金变动信息
    OESMSG_RPT_STOCK_HOLDING_VARIATION = 0x19  # 0x19/25  持仓变动信息 (股票)
    OESMSG_RPT_OPTION_HOLDING_VARIATION = 0x1A  # 0x1A/26  持仓变动信息 (期权)
    OESMSG_RPT_SERVICE_STATE = 0x1B  # 0x1B/27  OES服务状态信息 (暂不支持订阅推送)
    __OESMSG_RPT_MAX = 28  # 最大的回报消息类型
    # 非交易类消息
    __OESMSG_NONTRD_MIN = 0x20  # 0x20/32  最小的非交易消息类型
    OESMSG_NONTRD_FUND_TRSF_REQ = 0x21  # 0x21/33  出入金委托
    OESMSG_NONTRD_CHANGE_PASSWORD = 0x22  # 0x22/34  修改客户端登录密码
    __OESMSG_NONTRD_MAX = 35  # 最大的非交易消息类型
    # 查询类消息
    __OESMSG_QRYMSG_MIN = 0x2F  # 0x2F/47  最小的查询消息类型
    OESMSG_QRYMSG_CLIENT_OVERVIEW = 0x30  # 0x30/48  查询客户端总览信息
    OESMSG_QRYMSG_ORD = 0x31  # 0x31/49  查询委托信息
    OESMSG_QRYMSG_TRD = 0x32  # 0x32/50  查询成交信息
    OESMSG_QRYMSG_CASH_ASSET = 0x33  # 0x33/51  查询客户资金信息
    OESMSG_QRYMSG_STK_HLD = 0x34  # 0x34/52  查询股票持仓信息
    OESMSG_QRYMSG_OPT_HLD = 0x35  # 0x35/53  查询期权持仓信息
    OESMSG_QRYMSG_CUST = 0x36  # 0x36/54  查询客户信息
    OESMSG_QRYMSG_COMMISSION_RATE = 0x38  # 0x38/56  查询客户佣金信息
    OESMSG_QRYMSG_FUND_TRSF = 0x39  # 0x39/57  查询出入金信息
    OESMSG_QRYMSG_ETF = 0x3B  # 0x3B/59  查询ETF申赎产品信息
    OESMSG_QRYMSG_OPTION = 0x3D  # 0x3D/61  查询期权产品信息
    OESMSG_QRYMSG_LOT_WINNING = 0x3F  # 0x3F/63  查询新股配号、中签信息
    OESMSG_QRYMSG_TRADING_DAY = 0x40  # 0x40/64  查询当前交易日
    OESMSG_QRYMSG_MARKET_STATE = 0x41  # 0x41/65  查询市场状态
    OESMSG_QRYMSG_COUNTER_CASH = 0x42  # 0x42/66  查询客户主柜资金信息
    OESMSG_QRYMSG_BROKER_PARAMS = 0x48  # 0x48/72  查询券商参数信息
    OESMSG_QRYMSG_INV_ACCT = 0x51  # 0x51/81  查询证券账户信息 (0x37的更新版本, @since 0.15.9)
    OESMSG_QRYMSG_ISSUE = 0x57  # 0x57/87  查询证券发行信息 (0x3E的更新版本, @since 0.15.11)
    OESMSG_QRYMSG_STOCK = 0x58  # 0x58/88  查询现货产品信息 (0x52的更新版本, @since 0.15.11)
    OESMSG_QRYMSG_ETF_COMPONENT = 0x59  # 0x59/89  查询ETF成份证券信息 (0x3C的更新版本, @since 0.15.11)
    __OESMSG_QRYMSG_MAX = 90  # 最大的查询消息类型
    # 公共的会话类消息
    OESMSG_SESS_HEARTBEAT = 0xFA  # 0xFA/250 心跳消息
    OESMSG_SESS_TEST_REQUEST = 0xFB  # 0xFB/251 测试请求消息
    OESMSG_SESS_LOGIN_EXTEND = 0xFC  # 0xFC/252 登录扩展消息
    OESMSG_SESS_LOGOUT = 0xFE  # 0xFE/254 登出消息
    # 以下消息类型定义已废弃, 只是为了兼容之前的版本而暂时保留
    OESMSG_RPT_ORDER_REJECT = OESMSG_RPT_BUSINESS_REJECT


# 可订阅的回报消息类型定义
# - 0:      默认回报 (等价于: 0x01,0x02,0x04,0x08,0x10,0x20,0x40)
# - 0x0001: OES业务拒绝 (未通过风控检查等)
# - 0x0002: OES委托已生成 (已通过风控检查)
# - 0x0004: 交易所委托回报 (包括交易所委托拒绝、委托确认和撤单完成通知)
# - 0x0008: 交易所成交回报
# - 0x0010: 出入金委托执行报告 (包括出入金委托拒绝、出入金委托回报)
# - 0x0020: 资金变动信息
# - 0x0040: 持仓变动信息
# - 0x0080: 市场状态信息
# - 0xFFFF: 所有回报
class eOesSubscribeReportTypeT(Enum):
    # 默认回报
    OES_SUB_RPT_TYPE_DEFAULT = 0
    # OES业务拒绝 (未通过风控检查等)
    OES_SUB_RPT_TYPE_BUSINESS_REJECT = 0x01
    # OES委托已生成 (已通过风控检查)
    OES_SUB_RPT_TYPE_ORDER_INSERT = 0x02
    # 交易所委托回报 (包括交易所委托拒绝、委托确认和撤单完成通知)
    OES_SUB_RPT_TYPE_ORDER_REPORT = 0x04
    # 交易所成交回报
    OES_SUB_RPT_TYPE_TRADE_REPORT = 0x08
    # 出入金委托执行报告 (包括出入金委托拒绝、出入金委托回报)
    OES_SUB_RPT_TYPE_FUND_TRSF_REPORT = 0x10
    # 资金变动信息
    OES_SUB_RPT_TYPE_CASH_ASSET_VARIATION = 0x20
    # 持仓变动信息
    OES_SUB_RPT_TYPE_HOLDING_VARIATION = 0x40
    # 市场状态信息
    OES_SUB_RPT_TYPE_MARKET_STATE = 0x80
    # 所有回报
    OES_SUB_RPT_TYPE_ALL = 0xFFFF
    __MAX_OES_SUB_RPT_TYPE = 0x7FFFFFFF


# 可指定的协议约定类型定义
# - 0:     默认的协议约定类型
# - 0x80:  约定以压缩方式传输数据
# - 0xFF:  无任何协议约定
class eOesProtocolHintsTypeT(Enum):
    # 默认的协议约定类型
    OES_PROT_HINTS_TYPE_DEFAULT = 0
    # 协议约定以压缩方式传输数据
    OES_PROT_HINTS_TYPE_COMPRESS = 0x80
    # 无任何协议约定
    OES_PROT_HINTS_TYPE_NONE = 0xFF
    __MAX_OES_PROT_HINTS_TYPE = 0xFF


# 协议类型, 用于在消息标志中标识消息的协议类型
class eSMsgProtocolTypeT(Enum):
    SMSG_PROTO_BINARY = 0x00  # 协议类型-二进制
    SMSG_PROTO_JSON = 0x01  # 协议类型-JSON
    SMSG_PROTO_FIX = 0x02  # 协议类型-FIX
    SMSG_PROTO_PROTOBUF = 0x03  # 协议类型-ProtocolBuffers
    __MAX_SMSG_PROTO_TYPE = 4


# 消息标志, 用于在消息标志中标识消息的请求/应答类型
# 与协议类型复用相同的字段, 通过高4位/低4位进行区分
class eSMsgFlagT(Enum):
    SMSG_MSGFLAG_NONE = 0x00  # 消息标志-无
    SMSG_MSGFLAG_REQ = 0x00  # 消息标志-请求消息
    SMSG_MSGFLAG_RSP = 0x50  # 消息标志-应答消息 TODO refactor => 0x10
    SMSG_MSGFLAG_NESTED = 0x20  # 消息标志-嵌套的组合消息 (消息体由一到多条包含消息头的完整消息组成)
    SMSG_MSGFLAG_COMPRESSED = 0x80  # 消息标志-消息体已压缩
    SMSG_MSGFLAG_MASK_RSPFLAG = 0xF0  # 消息标志掩码-请求/应答标志的掩码
    SMSG_MSGFLAG_MASK_PROTOCOL = 0x0F  # 消息标志掩码-协议类型的掩码


# 通道类型定义
class eOesApiChannelTypeT(Enum):
    OESAPI_CHANNEL_TYPE_ORDER = 1  # 委托申报通道
    OESAPI_CHANNEL_TYPE_REPORT = 2  # 回报通道
    OESAPI_CHANNEL_TYPE_QUERY = 3  # 查询通道


class PrintableStructure(Structure):
    def __str__(self):
        result = "<" + self.__class__.__name__ + "("
        for name, _ in self._fields_:
            result = result + name + "=" + str(getattr(self, name)) + ", "
        return result[:-2] + ")>"

    def to_dict(self):
        new_d = {}
        for name, _ in self._fields_:
            val = getattr(self, name)
            if isinstance(val, bytes):
                val = val.decode('utf-8', "ignore")
            new_d[name] = val
        return new_d


class PrintableUnion(Union):
    def __str__(self):
        result = "<" + self.__class__.__name__ + "("
        for name, _ in self._fields_:
            result = result + name + "=" + str(getattr(self, name)) + ", "
        return result[:-2] + ")>"

    def to_dict(self):
        new_d = {}
        for name, _ in self._fields_:
            val = getattr(self, name)
            if isinstance(val, bytes):
                val = val.decode('utf-8', "ignore")
            new_d[name] = val
        return new_d


class STimespec32T(PrintableStructure):
    _fields_ = [
        ('tv_sec', c_int32),
        ('tv_nsec', c_int32),
    ]


class userInfo(PrintableUnion):
    _fields_ = [
        ('u64', c_uint64),  # uint64 类型的用户私有信息
        ('i64', c_int64),  # int64 类型的用户私有信息
        ('u32', c_uint32 * 2),  # uint32[2] 类型的用户私有信息
        ('i32', c_int32 * 2),  # int32[2] 类型的用户私有信息
        ('c8', c_char * 8),  # char[8] 类型的用户私有信息
    ]


# 委托请求的结构体定义
class OesOrdReqT(PrintableStructure):
    _fields_ = [
        # 客户委托流水号 (由客户端维护的递增流水, 用于识别重复的委托申报)
        ('clSeqNo', c_int32),
        # 市场代码 @see eOesMarketIdT
        ('mktId', c_uint8),
        # 订单类型 @see eOesOrdTypeShT eOesOrdTypeSzT
        ('ordType', c_uint8),
        # 买卖类型 @see eOesBuySellTypeT
        ('bsType', c_uint8),
        # 按64位对齐的填充域
        ('__ORD_BASE_INFO_filler', c_uint8),
        # 证券账户
        ('invAcctId', c_char * OES_INV_ACCT_ID_MAX_LEN),
        # 证券代码
        ('securityId', c_char * OES_SECURITY_ID_MAX_LEN),
        # 委托数量
        ('ordQty', c_int32),
        # 委托价格, 单位精确到元后四位, 即1元 = 10000
        ('ordPrice', c_int32),
        # 原始订单(待撤销的订单)的客户订单编号
        ('origClOrdId', c_int64),
        # 用户私有信息 (由客户端自定义填充, 并在回报数据中原样返回)
        ('userInfo', userInfo),
        # 委托请求的客户端原始发送时间 (OES内部使用, 由API在发送时自动填充)
        ('__ordReqOrigSendTime', STimespec32T),
    ]


# 撤单请求的结构体定义
class OesOrdCancelReqT(PrintableStructure):
    _fields_ = [
        # 客户委托流水号 (由客户端维护的递增流水, 用于识别重复的委托申报, 必填)
        ('clSeqNo', c_int32),
        # 市场代码 (必填) @see eOesMarketIdT
        ('mktId', c_uint8),
        # 按64位对齐的填充域
        ('__ORD_CANCEL_BASE_INFO_filler1', c_uint8 * 3),
        # 证券账户 (选填, 若不为空则校验待撤订单是否匹配)
        ('invAcctId', c_char * OES_INV_ACCT_ID_MAX_LEN),
        # 证券代码 (选填, 若不为空则校验待撤订单是否匹配)
        ('securityId', c_char * OES_SECURITY_ID_MAX_LEN),
        # 原始订单(待撤销的订单)的客户委托流水号 (若使用 origClOrdId, 则不必填充该字段)
        ('origClSeqNo', c_int32),
        # 原始订单(待撤销的订单)的客户端环境号 (小于等于0, 则使用当前会话的 clEnvId)
        ('origClEnvId', c_int8),
        # 按64位对齐的填充域
        ('__ORD_CANCEL_BASE_INFO_filler2', c_uint8 * 3),
        # 原始订单(待撤销的订单)的客户订单编号 (若使用 origClSeqNo, 则不必填充该字段)
        ('origClOrdId', c_int64),
        # 用户私有信息 (由客户端自定义填充, 并在回报数据中原样返回)
        ('userInfo', userInfo),
        # 委托请求的客户端原始发送时间 (OES内部使用, 由API在发送时自动填充)
        ('__ordReqOrigSendTime', STimespec32T),
    ]


# 委托拒绝(OES业务拒绝)的结构体定义
class OesOrdRejectT(PrintableStructure):
    _fields_ = [
        # 客户委托流水号 (由客户端维护的递增流水, 用于识别重复的委托申报)
        ('clSeqNo', c_int32),
        # 市场代码 @see eOesMarketIdT
        ('mktId', c_uint8),
        # 订单类型 @see eOesOrdTypeShT eOesOrdTypeSzT
        ('ordType', c_uint8),
        # 买卖类型 @see eOesBuySellTypeT
        ('bsType', c_uint8),
        # 按64位对齐的填充域
        ('__ORD_BASE_INFO_filler', c_uint8),
        # 证券账户
        ('invAcctId', c_char * OES_INV_ACCT_ID_MAX_LEN),
        # 证券代码
        ('securityId', c_char * OES_SECURITY_ID_MAX_LEN),
        # 委托数量
        ('ordQty', c_int32),
        # 委托价格, 单位精确到元后四位, 即1元 = 10000
        ('ordPrice', c_int32),
        # 原始订单(待撤销的订单)的客户订单编号
        ('origClOrdId', c_int64),
        # 用户私有信息 (由客户端自定义填充, 并在回报数据中原样返回)
        ('userInfo', userInfo),
        # 委托请求的客户端原始发送时间 (OES内部使用, 由API在发送时自动填充)
        ('__ordReqOrigSendTime', STimespec32T),
        # 原始订单(待撤销的订单)的客户委托流水号 (仅适用于撤单请求)
        ('origClSeqNo', c_int32),
        # 原始订单(待撤销的订单)的客户端环境号 (仅适用于撤单请求)
        ('origClEnvId', c_int8),
        # 客户端环境号
        ('clEnvId', c_int8),
        # 客户端编号
        ('clientId', c_int16),
        # 委托日期 (格式为 YYYYMMDD, 形如 20160830)
        ('ordDate', c_int32),
        # 委托时间 (格式为 HHMMSSsss, 形如 141205000)
        ('ordTime', c_int32),
        # 订单拒绝原因
        ('ordRejReason', c_int32),
        # 按64位对齐的填充域
        ('__filler', c_int32),
    ]


# 委托确认的结构体定义
class OesOrdCnfmT(PrintableStructure):
    _fields_ = [
        # 客户委托流水号 (由客户端维护的递增流水, 用于识别重复的委托申报)
        ('clSeqNo', c_int32),
        # 市场代码 @see eOesMarketIdT
        ('mktId', c_uint8),
        # 订单类型 @see eOesOrdTypeShT eOesOrdTypeSzT
        ('ordType', c_uint8),
        # 买卖类型 @see eOesBuySellTypeT
        ('bsType', c_uint8),
        # 按64位对齐的填充域
        ('__ORD_BASE_INFO_filler', c_uint8),
        # 证券账户
        ('invAcctId', c_char * OES_INV_ACCT_ID_MAX_LEN),
        # 证券代码
        ('securityId', c_char * OES_SECURITY_ID_MAX_LEN),
        # 委托数量
        ('ordQty', c_int32),
        # 委托价格, 单位精确到元后四位, 即1元 = 10000
        ('ordPrice', c_int32),
        # 原始订单(待撤销的订单)的客户订单编号
        ('origClOrdId', c_int64),
        # 用户私有信息 (由客户端自定义填充, 并在回报数据中原样返回)
        ('userInfo', userInfo),
        # 委托请求的客户端原始发送时间 (OES内部使用, 由API在发送时自动填充)
        ('__ordReqOrigSendTime', STimespec32T),
        # 客户订单编号 (在OES内具有唯一性的内部委托编号)
        ('clOrdId', c_int64),
        # 客户端编号
        ('clientId', c_int16),
        # 客户端环境号
        ('clEnvId', c_int8),
        # 原始订单(待撤销的订单)的客户端环境号 (仅适用于撤单委托)
        ('origClEnvId', c_int8),
        # 原始订单(待撤销的订单)的客户委托流水号 (仅适用于撤单委托)
        ('origClSeqNo', c_int32),
        # 委托日期 (格式为 YYYYMMDD, 形如 20160830)
        ('ordDate', c_int32),
        # 委托时间 (格式为 HHMMSSsss, 形如 141205000)
        ('ordTime', c_int32),
        # 委托确认时间 (格式为 HHMMSSsss, 形如 141206000)
        ('ordCnfmTime', c_int32),
        # 订单当前状态 @see eOesOrdStatusT
        ('ordStatus', c_uint8),
        # 委托确认状态 (交易所返回的回报状态, 仅供参考)  @see eOesOrdStatusT
        ('ordCnfmSts', c_uint8),
        # 证券类型 @see eOesSecurityTypeT
        ('securityType', c_uint8),
        # 证券子类型 @see eOesSubSecurityTypeT
        ('subSecurityType', c_uint8),
        # 平台号 (OES内部使用) @see eOesPlatformIdT
        ('__platformId', c_uint8),
        # 交易网关组序号 (OES内部使用)
        ('__tgwGrpNo', c_uint8),
        # 交易网关平台分区号 (OES内部使用)
        ('__tgwPartitionNo', c_uint8),
        # 产品类型 @see eOesProductTypeT
        ('productType', c_uint8),
        # 交易所订单编号 (深交所的订单编号是16位的非数字字符串)
        ('exchOrdId', c_char * OES_EXCH_ORDER_ID_MAX_LEN),
        # 已报盘标志 (OES内部使用)
        ('__declareFlag', c_uint8),
        # 重复回报标志 (OES内部使用)
        ('__repeatFlag', c_uint8),
        # 所有者类型 @see eOesOwnerTypeT
        ('ownerType', c_uint8),
        # 委托当前冻结的交易金额
        ('frzAmt', c_int64),
        # 委托当前冻结的利息
        ('frzInterest', c_int64),
        # 委托当前冻结的交易费用
        ('frzFee', c_int64),
        # 委托累计已发生的交易金额
        ('cumAmt', c_int64),
        # 委托累计已发生的利息
        ('cumInterest', c_int64),
        # 委托累计已发生的交易费用
        ('cumFee', c_int64),
        # 累计执行数量 (累计成交数量)
        ('cumQty', c_int32),
        # 已撤单数量
        ('canceledQty', c_int32),
        # 订单/撤单拒绝原因
        ('ordRejReason', c_int32),
        # 交易所错误码
        ('exchErrCode', c_int32),
        # PBU代码 (席位号)
        ('pbuId', c_int32),
        # 营业部代码
        ('branchId', c_int32),
        # 回报记录号 (OES内部使用)
        ('__rowNum', c_int32),
        # OIW委托编号 (OES内部使用)
        ('__recNum', c_uint32),
        # 委托请求的初始接收时间
        ('__ordReqOrigRecvTime', STimespec32T),
        # 委托请求的入队时间
        ('__ordReqCollectedTime', STimespec32T),
        # 委托请求的实际处理开始时间
        ('__ordReqActualDealTime', STimespec32T),
        # 委托请求的处理完成时间
        ('__ordReqProcessedTime', STimespec32T),
        # 委托确认的开始采集时间
        ('__ordCnfmOrigRecvTime', STimespec32T),
        # 委托确认的采集完成时间
        ('__ordCnfmCollectedTime', STimespec32T),
        # 委托确认的实际处理开始时间
        ('__ordCnfmActualDealTime', STimespec32T),
        # 委托确认的处理完成时间
        ('__ordCnfmProcessedTime', STimespec32T),
        # 初始报盘时间
        ('__ordDeclareTime', STimespec32T),
        # 报盘完成时间
        ('__ordDeclareDoneTime', STimespec32T),
        # 消息推送时间 (写入推送缓存以后, 实际网络发送之前)
        ('__pushingTime', STimespec32T),
    ]


# 成交基础信息的结构体定义
class OesTrdBaseInfoT(PrintableStructure):
    _fields_ = [
        # 交易所成交编号 (以下的6个字段是成交信息的联合索引字段)
        ('exchTrdNum', c_int64),
        # 市场代码 @see eOesMarketIdT
        ('mktId', c_uint8),
        # 买卖类型 (取值范围: 买/卖, 申购/赎回(仅深圳)) @see eOesBuySellTypeT
        ('trdSide', c_uint8),
        # 平台号 (OES内部使用) @see eOesPlatformIdT
        ('__platformId', c_uint8),
        # 成交类型 (OES内部使用) @see eOesEtfTrdCnfmTypeT
        ('__trdCnfmType', c_uint8),
        # ETF成交回报顺序号 (OES内部使用), 为区分ETF成交记录而设置 (以订单为单位)
        ('__etfTrdCnfmSeq', c_uint32),
        # 股东账户代码
        ('invAcctId', c_char * OES_INV_ACCT_ID_MAX_LEN),
        # 证券代码
        ('securityId', c_char * OES_SECURITY_ID_MAX_LEN),
        # 成交日期 (格式为 YYYYMMDD, 形如 20160830)
        ('trdDate', c_int32),
        # 成交时间 (格式为 HHMMSSsss, 形如 141205000)
        ('trdTime', c_int32),
        # 成交数量
        ('trdQty', c_int32),
        # 成交价格 (单位精确到元后四位, 即: 1元=10000)
        ('trdPrice', c_int32),
        # 成交金额 (单位精确到元后四位, 即: 1元=10000)
        ('trdAmt', c_int64),
        # 客户订单编号
        ('clOrdId', c_int64),
        # 累计执行数量
        ('cumQty', c_int32),
        # 回报记录号 (OES内部使用)
        ('__rowNum', c_int32),
        # 交易网关组序号 (OES内部使用)
        ('__tgwGrpNo', c_uint8),
        # ETF赎回得到的替代资金是否当日可用 (OES内部使用)
        ('__isTrsfInCashAvailable', c_uint8),
        # 交易网关平台分区号 (OES内部使用)
        ('__tgwPartitionNo', c_uint8),
        # 产品类型 @see eOesProductTypeT
        ('productType', c_uint8),
        # 原始委托数量
        ('origOrdQty', c_int32),
        # PBU代码 (席位号)
        ('pbuId', c_int32),
        # 营业部代码
        ('branchId', c_int32),
    ]


# 成交回报结构体定义
class OesTrdCnfmT(PrintableStructure):
    _fields_ = [
        # 交易所成交编号 (以下的6个字段是成交信息的联合索引字段)
        ('exchTrdNum', c_int64),
        # 市场代码 @see eOesMarketIdT
        ('mktId', c_uint8),
        # 买卖类型 (取值范围: 买/卖, 申购/赎回(仅深圳)) @see eOesBuySellTypeT
        ('trdSide', c_uint8),
        # 平台号 (OES内部使用) @see eOesPlatformIdT
        ('__platformId', c_uint8),
        # 成交类型 (OES内部使用) @see eOesEtfTrdCnfmTypeT
        ('__trdCnfmType', c_uint8),
        # ETF成交回报顺序号 (OES内部使用), 为区分ETF成交记录而设置 (以订单为单位)
        ('__etfTrdCnfmSeq', c_uint32),
        # 股东账户代码
        ('invAcctId', c_char * OES_INV_ACCT_ID_MAX_LEN),
        # 证券代码
        ('securityId', c_char * OES_SECURITY_ID_MAX_LEN),
        # 成交日期 (格式为 YYYYMMDD, 形如 20160830)
        ('trdDate', c_int32),
        # 成交时间 (格式为 HHMMSSsss, 形如 141205000)
        ('trdTime', c_int32),
        # 成交数量
        ('trdQty', c_int32),
        # 成交价格 (单位精确到元后四位, 即: 1元=10000)
        ('trdPrice', c_int32),
        # 成交金额 (单位精确到元后四位, 即: 1元=10000)
        ('trdAmt', c_int64),
        # 客户订单编号
        ('clOrdId', c_int64),
        # 累计执行数量
        ('cumQty', c_int32),
        # 回报记录号 (OES内部使用)
        ('__rowNum', c_int32),
        # 交易网关组序号 (OES内部使用)
        ('__tgwGrpNo', c_uint8),
        # ETF赎回得到的替代资金是否当日可用 (OES内部使用)
        ('__isTrsfInCashAvailable', c_uint8),
        # 交易网关平台分区号 (OES内部使用)
        ('__tgwPartitionNo', c_uint8),
        # 产品类型 @see eOesProductTypeT
        ('productType', c_uint8),
        # 原始委托数量
        ('origOrdQty', c_int32),
        # PBU代码 (席位号)
        ('pbuId', c_int32),
        # 营业部代码
        ('branchId', c_int32),
        # 客户委托流水号
        ('clSeqNo', c_int32),
        # 客户端编号
        ('clientId', c_int16),
        # 客户端环境号
        ('clEnvId', c_int8),
        # 证券子类别 (为保持兼容而位置凌乱, 后续会做调整) @see eOesSubSecurityTypeT
        ('subSecurityType', c_uint8),
        # 订单当前状态 @see eOesOrdStatusT
        ('ordStatus', c_uint8),
        # 订单类型 @see eOesOrdTypeShT eOesOrdTypeSzT
        ('ordType', c_uint8),
        # 买卖类型 @see eOesBuySellTypeT
        ('ordBuySellType', c_uint8),
        # 证券类型 @see eOesSecurityTypeT
        ('securityType', c_uint8),
        # 原始委托价格, 单位精确到元后四位, 即1元 = 10000
        ('origOrdPrice', c_int32),
        # 累计成交金额
        ('cumAmt', c_int64),
        # 累计成交利息
        ('cumInterest', c_int64),
        # 累计交易费用
        ('cumFee', c_int64),
        # 用户私有信息 (由客户端自定义填充, 并在回报数据中原样返回)
        ('userInfo', userInfo),
        # 成交确认的开始采集时间
        ('__trdCnfmOrigRecvTime', STimespec32T),
        # 成交确认的采集完成时间
        ('__trdCnfmCollectedTime', STimespec32T),
        # 成交确认的实际处理开始时间
        ('__trdCnfmActualDealTime', STimespec32T),
        # 成交确认的处理完成时间
        ('__trdCnfmProcessedTime', STimespec32T),
        # 消息推送时间 (写入推送缓存以后, 实际网络发送之前)
        ('__pushingTime', STimespec32T),
    ]


# 新股配号、中签记录信息定义
class OesLotWinningBaseInfoT(PrintableStructure):
    _fields_ = [
        # 证券账户
        ('invAcctId', c_char * OES_INV_ACCT_ID_MAX_LEN),
        # 配号代码/中签代码
        ('securityId', c_char * OES_SECURITY_ID_MAX_LEN),
        # 市场代码 @see eOesMarketIdT
        ('mktId', c_uint8),
        # 记录类型 @see eOesLotTypeT
        ('lotType', c_uint8),
        # 失败原因, 当且仅当 lotType 为 OES_LOT_TYPE_FAILED 时此字段有效
        # @see eOesLotRejReasonT
        ('rejReason', c_uint8),
        # 按64位对齐填充域
        ('__LOT_WINNING_BASE_INFO_filler', c_int8),
        # 配号日期/中签日期 (格式为 YYYYMMDD, 形如 20160830)
        ('lotDate', c_int32),
        # 证券名称 (UTF-8 编码)
        ('securityName', c_char * OES_SECURITY_NAME_MAX_LEN),
        # 配号首个号码。当为中签记录时此字段固定为0
        ('assignNum', c_int64),
        # 配号成功数量/中签股数
        ('lotQty', c_int32),
        # 最终发行价, 单位精确到元后四位, 即1元 = 10000。当为配号记录时此字段值固定为0
        ('lotPrice', c_int32),
        # 中签金额, 单位精确到元后四位, 即1元 = 10000。当为配号记录时此字段值固定为0
        ('lotAmt', c_int64),
    ]


# 出入金委托的基础信息结构体定义
class OesFundTrsfBaseInfoT(PrintableStructure):
    _fields_ = [
        # 客户委托流水号 (由客户端维护的递增流水)
        ('clSeqNo', c_int32),
        # 划转方向 @see eOesFundTrsfDirectT
        ('direct', c_uint8),
        # 出入金转账类型 @see eOesFundTrsfTypeT
        ('isAllotOnly', c_uint8),
        # 按64位对齐填充域
        ('__FUND_TRSF_BASE_filler', c_uint8 * 2),
        # 资金账户代码
        ('cashAcctId', c_char * OES_CASH_ACCT_ID_MAX_LEN),
        # 交易密码
        ('trdPasswd', c_char * OES_PWD_MAX_LEN),
        # 转账密码(转账方向为转入(银行转证券), 此密码为银行密码.
        # 转账方向为转出(证券转银行), 此密码为资金密码
        ('trsfPasswd', c_char * OES_PWD_MAX_LEN),
        # 发生金额 (都是正数), 单位精确到元后四位, 即1元 = 10000
        ('occurAmt', c_int64),
        # 用户私有信息 (由客户端自定义填充, 并在回报数据中原样返回)
        ('userInfo', userInfo),
    ]


# 出入金请求定义
class OesFundTrsfReqT(PrintableStructure):
    _fields_ = [
        # 客户委托流水号 (由客户端维护的递增流水)
        ('clSeqNo', c_int32),
        # 划转方向 @see eOesFundTrsfDirectT
        ('direct', c_uint8),
        # 出入金转账类型 @see eOesFundTrsfTypeT
        ('isAllotOnly', c_uint8),
        # 按64位对齐填充域
        ('__FUND_TRSF_BASE_filler', c_uint8 * 2),
        # 资金账户代码
        ('cashAcctId', c_char * OES_CASH_ACCT_ID_MAX_LEN),
        # 交易密码
        ('trdPasswd', c_char * OES_PWD_MAX_LEN),
        # 转账密码(转账方向为转入(银行转证券), 此密码为银行密码.
        # 转账方向为转出(证券转银行), 此密码为资金密码
        ('trsfPasswd', c_char * OES_PWD_MAX_LEN),
        # 发生金额 (都是正数), 单位精确到元后四位, 即1元 = 10000
        ('occurAmt', c_int64),
        # 用户私有信息 (由客户端自定义填充, 并在回报数据中原样返回)
        ('userInfo', userInfo),
    ]


# 出入金拒绝的回报结构定义 (因风控检查未通过而被OES拒绝)
class OesFundTrsfRejectT(PrintableStructure):
    _fields_ = [
        # 客户委托流水号 (由客户端维护的递增流水)
        ('clSeqNo', c_int32),
        # 划转方向 @see eOesFundTrsfDirectT
        ('direct', c_uint8),
        # 出入金转账类型 @see eOesFundTrsfTypeT
        ('isAllotOnly', c_uint8),
        # 按64位对齐填充域
        ('__FUND_TRSF_BASE_filler', c_uint8 * 2),
        # 资金账户代码
        ('cashAcctId', c_char * OES_CASH_ACCT_ID_MAX_LEN),
        # 交易密码
        ('trdPasswd', c_char * OES_PWD_MAX_LEN),
        # 转账密码(转账方向为转入(银行转证券), 此密码为银行密码.
        # 转账方向为转出(证券转银行), 此密码为资金密码
        ('trsfPasswd', c_char * OES_PWD_MAX_LEN),
        # 发生金额 (都是正数), 单位精确到元后四位, 即1元 = 10000
        ('occurAmt', c_int64),
        # 用户私有信息 (由客户端自定义填充, 并在回报数据中原样返回)
        ('userInfo', userInfo),
        # 委托日期 (格式为 YYYYMMDD, 形如 20160830)
        ('ordDate', c_int32),
        # 委托时间 (格式为 HHMMSSsss, 形如 141205000)
        ('ordTime', c_int32),
        # 客户端编号
        ('clientId', c_int16),
        # 客户端环境号
        ('clEnvId', c_int8),
        # 64位对齐的填充域
        ('__filler', c_int8),
        # 错误码
        ('rejReason', c_int32),
        # 错误信息
        ('errorInfo', c_char * OES_MAX_ERROR_INFO_LEN),
    ]


# 出入金委托执行状态回报的结构体定义
class OesFundTrsfReportT(PrintableStructure):
    _fields_ = [
        # 客户委托流水号 (由客户端维护的递增流水)
        ('clSeqNo', c_int32),
        # 客户端编号
        ('clientId', c_int16),
        # 客户端环境号
        ('clEnvId', c_int8),
        # 划转方向 @see eOesFundTrsfDirectT
        ('direct', c_uint8),
        # 资金账户代码
        ('cashAcctId', c_char * OES_CASH_ACCT_ID_MAX_LEN),
        # 发生金额 (都是正数), 单位精确到元后四位, 即1元 = 10000
        ('occurAmt', c_int64),
        # 用户私有信息 (由客户端自定义填充, 并在回报数据中原样返回)
        ('userInfo', userInfo),
        # OES出入金委托编号 (在OES内具有唯一性的内部出入金委托编号)
        ('fundTrsfId', c_int32),
        # 柜台出入金委托编号
        ('counterEntrustNo', c_int32),
        # 出入金委托日期 (格式为 YYYYMMDD, 形如 20160830)
        ('operDate', c_int32),
        # 出入金委托时间 (格式为 HHMMSSsss, 形如 141205000)
        ('operTime', c_int32),
        # 上报柜台时间 (格式为 HHMMSSsss, 形如 141205000)
        ('dclrTime', c_int32),
        # 柜台执行结果采集时间 (格式为 HHMMSSsss, 形如 141205000)
        ('doneTime', c_int32),
        # 出入金转账类型 @see eOesFundTrsfTypeT
        ('isAllotOnly', c_uint8),
        # 出入金委托执行状态 @see eOesFundTrsfStatusT
        ('trsfStatus', c_uint8),
        # 是否有转账到主柜
        ('__hasCounterTransfered', c_uint8),
        # 按64位对齐填充域
        ('__filler', c_uint8),
        # 错误原因
        ('rejReason', c_int32),
        # 主柜错误码
        ('counterErrCode', c_int32),
        # 按64位对齐填充域
        ('__filler2', c_uint32),
        # 资金调拨流水号
        ('allotSerialNo', c_char * OES_MAX_ALLOT_SERIALNO_LEN),
        # 错误信息
        ('errorInfo', c_char * OES_MAX_ERROR_INFO_LEN),
    ]


# 证券发行基础信息的结构体定义
class OesIssueBaseInfoT(PrintableStructure):
    _fields_ = [
        # 证券发行代码
        ('securityId', c_char * OES_SECURITY_ID_MAX_LEN),
        # 市场代码 @see eOesMarketIdT
        ('mktId', c_uint8),
        # 证券类型 @see eOesSecurityTypeT
        ('securityType', c_uint8),
        # 证券子类型 @see eOesSubSecurityTypeT
        ('subSecurityType', c_uint8),
        # 产品类型 @see eOesProductTypeT
        ('productType', c_uint8),
        # 发行方式 @see eOesSecurityIssueTypeT
        ('issueType', c_uint8),
        # 是否允许撤单
        ('isCancelAble', c_uint8),
        # 是否允许重复认购
        ('isReApplyAble', c_uint8),
        # 停牌标识 @see eOesSecuritySuspFlagT
        ('suspFlag', c_uint8),
        # 证券属性 @see eOesSecurityAttributeT
        ('securityAttribute', c_uint32),
        # 是否注册制 (0 核准制, 1 注册制)
        ('isRegistration', c_uint8),
        # 是否尚未盈利 (0 已盈利, 1 未盈利 (仅适用于创业板产品))
        ('isNoProfit', c_uint8),
        # 是否存在投票权差异 (0 无差异, 1 存在差异 (仅适用于创业板产品))
        ('isWeightedVotingRights', c_uint8),
        # 是否具有协议控制框架 (0 没有, 1 有 (仅适用于创业板产品))
        ('isVie', c_uint8),
        # 按64位对齐的填充域
        ('__ISSUE_BASE_filler', c_uint8 * 8),
        # 发行起始日
        ('startDate', c_int32),
        # 发行结束日
        ('endDate', c_int32),
        # 发行价格
        ('issuePrice', c_int32),
        # union {
        # 申购价格上限 (单位精确到元后四位, 即1元 = 10000)
        ('upperLimitPrice', c_int32),
        # 申购价格上限 @deprecated 已废弃, 为了兼容旧版本而保留
        # ('ceilPrice', c_int32),
        # };
        # union {
        # 申购价格下限 (单位精确到元后四位, 即1元 = 10000)
        ('lowerLimitPrice', c_int32),
        # 申购价格下限 @deprecated 已废弃, 为了兼容旧版本而保留
        # ('floorPrice', c_int32),
        # };
        # 委托最大份数
        ('ordMaxQty', c_int32),
        # 委托最小份数
        ('ordMinQty', c_int32),
        # 委托份数单位
        ('qtyUnit', c_int32),
        # 总发行量
        ('issueQty', c_int64),
        # 配股股权登记日(仅上海市场有效)
        ('alotRecordDay', c_int32),
        # 配股股权除权日(仅上海市场有效)
        ('alotExRightsDay', c_int32),
        # 基础证券代码 (正股代码)
        ('underlyingSecurityId', c_char * OES_SECURITY_ID_MAX_LEN),
        # 证券名称 (UTF-8 编码)
        ('securityName', c_char * OES_SECURITY_NAME_MAX_LEN),
        # 预留的备用字段
        ('__ISSUE_BASE_reserve1', c_char * 56),
        # 预留的备用字段
        ('__ISSUE_BASE_reserve2', c_char * 64),
    ]


# 竞价交易的限价参数(涨停价/跌停价)定义
class OesPriceLimitT(PrintableStructure):
    _fields_ = [
        # union {
        # 涨停价 (单位精确到元后四位, 即1元 = 10000)
        ('upperLimitPrice', c_int32),
        # 涨停价 @deprecated 已废弃, 为了兼容旧版本而保留
        # ('ceilPrice', c_int32),
        # };
        # union {
        # 跌停价 (单位精确到元后四位, 即1元 = 10000)
        ('lowerLimitPrice', c_int32),
        # 跌停价 @deprecated 已废弃, 为了兼容旧版本而保留
        # ('floorPrice', c_int32),
        # };
    ]


# 现货产品基础信息的结构体定义
class OesStockBaseInfoT(PrintableStructure):
    _fields_ = [
        # 证券代码
        ('securityId', c_char * OES_SECURITY_ID_MAX_LEN),
        # 市场代码 @see eOesMarketIdT
        ('mktId', c_uint8),
        # 产品类型 @see eOesProductTypeT
        ('productType', c_uint8),
        # 证券类型 @see eOesSecurityTypeT
        ('securityType', c_uint8),
        # 证券子类型 @see eOesSubSecurityTypeT
        ('subSecurityType', c_uint8),
        # 证券级别 @see eOesSecurityLevelT
        ('securityLevel', c_uint8),
        # 证券风险等级 @see eOesSecurityRiskLevelT
        ('securityRiskLevel', c_uint8),
        # 币种 @see eOesCurrTypeT
        ('currType', c_uint8),
        # 投资者适当性管理分类 @see eOesQualificationClassT
        ('qualificationClass', c_uint8),
        # 证券状态 @see eOesSecurityStatusT
        ('securityStatus', c_uint32),
        # 证券属性 @see eOesSecurityAttributeT
        ('securityAttribute', c_uint32),
        # 连续停牌标识 @see eOesSecuritySuspFlagT
        # - 上海市场, 是否禁止交易 (0: 正常交易; 非0: 禁止交易)
        # - 深圳市场, 是否连续停牌 (0: 未连续停牌; 非0: 连续停牌)
        ('suspFlag', c_uint8),
        # 临时停牌标识 (0 未停牌, 1 已停牌)
        ('temporarySuspFlag', c_uint8),
        # 是否支持当日回转交易 (0 不支持, 1 支持)
        ('isDayTrading', c_uint8),
        # 是否注册制 (0 核准制, 1 注册制)
        ('isRegistration', c_uint8),
        # 是否为融资融券担保品 (0 不是担保品, 1 是担保品)
        ('isCrdCollateral', c_uint8),
        # 是否为融资标的 (0 不是融资标的, 1 是融资标的)
        ('isCrdMarginTradeUnderlying', c_uint8),
        # 是否为融券标的 (0 不是融券标的, 1 是融券标的)
        ('isCrdShortSellUnderlying', c_uint8),
        # 是否尚未盈利 (0 已盈利, 1 未盈利 (仅适用于科创板和创业板产品))
        ('isNoProfit', c_uint8),
        # 是否存在投票权差异 (0 无差异, 1 存在差异 (仅适用于科创板和创业板产品))
        ('isWeightedVotingRights', c_uint8),
        # 是否具有协议控制框架 (0 没有, 1 有 (仅适用于创业板产品))
        ('isVie', c_uint8),
        # 按64位对齐的填充域
        ('__STOCK_BASE_filler', c_uint8 * 6),
        # 限价参数表 (涨/跌停价格, 数组下标为当前时段标志 @see eOesTrdSessTypeT)
        ('priceLimit', OesPriceLimitT * eOesTrdSessTypeT._eOesTrdSessTypeT__OES_TRD_SESS_TYPE_MAX.value),
        # union {
        # 最小报价单位 (单位精确到元后四位, 即1元 = 10000)
        ('priceTick', c_int32),
        # 最小报价单位 @deprecated 已废弃, 为了兼容旧版本而保留
        # ('priceUnit', c_int32),
        # };
        # 前收盘价, 单位精确到元后四位, 即1元 = 10000
        ('prevClose', c_int32),
        # union {
        # 单笔限价买委托数量上限
        ('lmtBuyMaxQty', c_int32),
        # 单笔限价买委托数量上限 @deprecated 已废弃, 为了兼容旧版本而保留
        # ('buyOrdMaxQty', c_int32),
        # };
        # union {
        # 单笔限价买委托数量下限
        ('lmtBuyMinQty', c_int32),
        # 单笔限价买委托数量下限 @deprecated 已废弃, 为了兼容旧版本而保留
        # ('buyOrdMinQty', c_int32),
        # };
        # union {
        # 单笔限价买入单位
        ('lmtBuyQtyUnit', c_int32),
        # 单笔限价买入单位 @deprecated 已废弃, 为了兼容旧版本而保留
        # ('buyQtyUnit', c_int32),
        # };
        # 单笔市价买委托数量上限
        ('mktBuyMaxQty', c_int32),
        # 单笔市价买委托数量下限
        ('mktBuyMinQty', c_int32),
        # 单笔市价买入单位
        ('mktBuyQtyUnit', c_int32),
        # union {
        # 单笔限价卖委托数量上限
        ('lmtSellMaxQty', c_int32),
        # 单笔限价卖委托数量上限 @deprecated 已废弃, 为了兼容旧版本而保留
        # ('sellOrdMaxQty', c_int32),
        # };
        # union {
        # 单笔限价卖委托数量下限
        ('lmtSellMinQty', c_int32),
        # 单笔限价卖委托数量下限 @deprecated 已废弃, 为了兼容旧版本而保留
        # ('sellOrdMinQty', c_int32),
        # };
        # union {
        # 单笔限价卖出单位
        ('lmtSellQtyUnit', c_int32),
        # 单笔限价卖出单位 @deprecated 已废弃, 为了兼容旧版本而保留
        # ('sellQtyUnit', c_int32),
        # };
        # 单笔市价卖委托数量上限
        ('mktSellMaxQty', c_int32),
        # 单笔市价卖委托数量下限
        ('mktSellMinQty', c_int32),
        # 单笔市价卖出单位
        ('mktSellQtyUnit', c_int32),
        # 债券的每张应计利息, 单位精确到元后八位, 即应计利息1元 = 100000000
        ('bondInterest', c_int64),
        # union {
        # 面值, 单位精确到元后四位, 即1元 = 10000
        ('parValue', c_int64),
        # 面值, 单位精确到元后四位, 即1元 = 10000 @deprecated 已废弃, 为了兼容旧版本而保留
        # ('parPrice', c_int64),
        # };
        # 逆回购期限
        ('repoExpirationDays', c_int32),
        # 占款天数
        ('cashHoldDays', c_int32),
        # 连续交易时段的有效竞价范围限制类型 @see eOesAuctionLimitTypeT
        ('auctionLimitType', c_uint8),
        # 连续交易时段的有效竞价范围基准价类型 @see eOesAuctionReferPriceTypeT
        ('auctionReferPriceType', c_uint8),
        # 按64位对齐的填充域
        ('__STOCK_BASE_filler1', c_uint8 * 2),
        # 连续交易时段的有效竞价范围涨跌幅度 (百分比或绝对价格, 取决于'有效竞价范围限制类型')
        ('auctionUpDownRange', c_int32),
        # 上市日期
        ('listDate', c_int32),
        # 到期日期 (仅适用于债券等有发行期限的产品)
        ('maturityDate', c_int32),
        # 总股本 (即: 总发行数量, 上证无该字段, 未额外维护时取值同流通股数量)
        ('outstandingShare', c_int64),
        # 流通股数量
        ('publicFloatShare', c_int64),
        # 基础证券代码 (标的产品代码)
        ('underlyingSecurityId', c_char * OES_SECURITY_ID_MAX_LEN),
        # ETF基金申赎代码
        ('fundId', c_char * OES_SECURITY_ID_MAX_LEN),
        # 证券名称 (UTF-8 编码)
        ('securityName', c_char * OES_SECURITY_NAME_MAX_LEN),
        # 预留的备用字段
        ('__STOCK_BASE_reserve1', c_char * 80),
        # 预留的备用字段
        ('__STOCK_BASE_reserve2', c_char * 64),
    ]


# ETF申赎产品基础信息的结构体定义
class OesEtfBaseInfoT(PrintableStructure):
    _fields_ = [
        # ETF基金申赎代码
        ('fundId', c_char * OES_SECURITY_ID_MAX_LEN),
        # ETF基金买卖代码
        ('securityId', c_char * OES_SECURITY_ID_MAX_LEN),
        # ETF基金市场代码 @see eOesMarketIdT
        ('mktId', c_uint8),
        # 证券类型 @see eOesSecurityTypeT
        ('securityType', c_uint8),
        # 证券子类型 @see eOesSubSecurityTypeT
        ('subSecurityType', c_uint8),
        # 是否需要发布IOPV  1: 是; 0: 否
        ('isPublishIOPV', c_uint8),
        # 交易所/基金公司的允许申购标志  1: 是; 0: 否
        ('isCreationAble', c_uint8),
        # 交易所/基金公司的允许赎回标志  1: 是; 0: 否
        ('isRedemptionAble', c_uint8),
        # 券商管理端的禁止交易标志  1: 是; 0: 否
        ('isDisabled', c_uint8),
        # 按64位对齐填充域
        ('__ETF_BASE_filler', c_uint8),
        # 成份证券数目
        ('componentCnt', c_int32),
        # 每个篮子 (最小申购、赎回单位) 对应的ETF份数, 即申购赎回单位
        ('creRdmUnit', c_int32),
        # 最大现金替代比例, 单位精确到十万分之一, 即替代比例50% = 50000
        ('maxCashRatio', c_int32),
        # 前一日基金的单位净值, 单位精确到元后四位, 即1元 = 10000
        ('nav', c_int32),
        # 前一日最小申赎单位净值, 单位精确到元后四位, 即1元 = 10000
        ('navPerCU', c_int64),
        # 红利金额, 单位精确到元后四位, 即1元 = 10000
        ('dividendPerCU', c_int64),
        # 当前交易日, 格式YYYYMMDD
        ('tradingDay', c_int32),
        # 前一交易日, 格式YYYYMMDD
        ('preTradingDay', c_int32),
        # 每个篮子的预估现金差额, 单位精确到元后四位, 即1元 = 10000
        ('estiCashCmpoent', c_int64),
        # 前一日现金差额, 单位精确到元后四位, 即1元 = 10000
        ('cashCmpoent', c_int64),
        # 单个账户当日累计申购总额限制
        ('creationLimit', c_int64),
        # 单个账户当日累计赎回总额限制
        ('redemLimit', c_int64),
        # 单个账户当日净申购总额限制
        ('netCreationLimit', c_int64),
        # 单个账户当日净赎回总额限制
        ('netRedemLimit', c_int64),
    ]


# ETF成份证券基础信息的结构体定义
class OesEtfComponentBaseInfoT(PrintableStructure):
    _fields_ = [
        # ETF基金申赎代码
        ('fundId', c_char * OES_SECURITY_ID_MAX_LEN),
        # 成份证券代码
        ('securityId', c_char * OES_SECURITY_ID_MAX_LEN),
        # 成份证券市场代码 @see eOesMarketIdT
        ('mktId', c_uint8),
        # ETF基金市场代码 @see eOesMarketIdT
        ('fundMktId', c_uint8),
        # 现金替代标识 @see eOesEtfSubFlagT
        ('subFlag', c_uint8),
        # 成份证券的证券类型 @see eOesSecurityTypeT
        ('securityType', c_uint8),
        # 成份证券的证券子类型 @see eOesSubSecurityTypeT
        ('subSecurityType', c_uint8),
        # 是否是作为申赎对价的成份证券
        # @note 注意事项:
        # - 非申赎对价的成份证券信息仅供参考, 申赎时不能对该类成份证券进行股份计算
        # 或现金替代处理。
        # - 例如: 深交所跨市场ETF中的沪市成份证券信息就属于非申赎对价的成份证券信息,
        # 对深交所跨市场ETF进行申赎时应使用 159900 虚拟成份券进行沪市成份证券份额
        # 的现金替代处理
        ('isTrdComponent', c_uint8),
        # 按64位对齐填充域
        ('__ETF_COMPONENT_BASE_filler', c_uint8 * 2),
        # 前收盘价格, 单位精确到元后四位, 即1元 = 10000
        ('prevClose', c_int32),
        # 成份证券数量
        ('qty', c_int32),
        # union {
        # 申购溢价比例, 单位精确到十万分之一, 即溢价比例10% = 10000
        ('premiumRatio', c_int32),
        # 申购溢价比例 @deprecated 已废弃, 为了兼容旧版本而保留
        # ('premiumRate', c_int32),
        # };
        # 赎回折价比例, 单位精确到十万分之一, 即折价比例10% = 10000
        ('discountRatio', c_int32),
        # 申购替代金额, 单位精确到元后四位, 即1元 = 10000
        ('creationSubCash', c_int64),
        # union {
        # 赎回替代金额, 单位精确到元后四位, 即1元 = 10000
        ('redemptionSubCash', c_int64),
        # 赎回替代金额 @deprecated 已废弃, 为了兼容旧版本而保留
        # ('redemptionCashSub', c_int64),
        # };
    ]


# 客户资金基础信息结构体定义
class OesCashAssetBaseInfoT(PrintableStructure):
    _fields_ = [
        # 资金账户代码
        ('cashAcctId', c_char * OES_CASH_ACCT_ID_MAX_LEN),
        # 客户代码
        ('custId', c_char * OES_CUST_ID_MAX_LEN),
        # 币种 @see eOesCurrTypeT
        ('currType', c_uint8),
        # 资金帐户类别(冗余自资金账户) @see eOesCashTypeT
        ('cashType', c_uint8),
        # 资金帐户状态(冗余自资金账户) @see eOesAcctStatusT
        ('cashAcctStatus', c_uint8),
        # 是否禁止出入金 (仅供API查询使用)
        ('isFundTrsfDisabled', c_uint8),
        # 按64位对齐的填充域
        ('__CASH_ASSET_BASE_filler', c_uint8 * 4),
        # 期初余额, 单位精确到元后四位, 即1元 = 10000
        ('beginningBal', c_int64),
        # 期初可用余额, 单位精确到元后四位, 即1元 = 10000
        ('beginningAvailableBal', c_int64),
        # 期初可取余额, 单位精确到元后四位, 即1元 = 10000
        ('beginningDrawableBal', c_int64),
        # 不可用资金余额(既不可交易又不可提取), 单位精确到元后四位, 即1元 = 10000
        ('disableBal', c_int64),
        # 当前冲正金额(红冲蓝补的资金净额), 取值可以为负数(表示资金调出), 单位精确到元后四位(即1元 = 10000)
        ('reversalAmt', c_int64),
        # 手动冻结资金, 取值在0和当前资产之间, 单位精确到元后四位(即1元 = 10000)
        ('manualFrzAmt', c_int64),
        # 日中累计存入资金金额, 单位精确到元后四位, 即1元 = 10000
        ('totalDepositAmt', c_int64),
        # 日中累计提取资金金额, 单位精确到元后四位, 即1元 = 10000
        ('totalWithdrawAmt', c_int64),
        # 当前提取冻结资金金额, 单位精确到元后四位, 即1元 = 10000
        ('withdrawFrzAmt', c_int64),
        # 日中累计 卖/赎回 获得的可用资金金额, 单位精确到元后四位, 即1元 = 10000
        ('totalSellAmt', c_int64),
        # 日中累计 买/申购/逆回购 使用资金金额, 单位精确到元后四位, 即1元 = 10000
        ('totalBuyAmt', c_int64),
        # 当前交易冻结金额, 单位精确到元后四位, 即1元 = 10000
        ('buyFrzAmt', c_int64),
        # 日中累计交易费用金额, 单位精确到元后四位, 即1元 = 10000
        ('totalFeeAmt', c_int64),
        # 当前冻结交易费用金额, 单位精确到元后四位, 即1元 = 10000
        ('feeFrzAmt', c_int64),
        # 当前维持的保证金(衍生品账户时指开仓保证金)金额, 单位精确到元后四位, 即1元 = 10000
        ('marginAmt', c_int64),
        # 当前冻结的保证金(衍生品账户时指开仓在途冻结保证金)金额, 单位精确到元后四位, 即1元 = 10000
        ('marginFrzAmt', c_int64),
    ]


# 客户基础信息的结构体定义
class OesCustBaseInfoT(PrintableStructure):
    _fields_ = [
        # 客户代码
        ('custId', c_char * OES_CUST_ID_MAX_LEN),
        # 客户类型 @see eOesCustTypeT
        ('custType', c_uint8),
        # 客户状态 (0:正常, 非0:不正常)
        ('status', c_uint8),
        # OES风险等级 @see eOesSecurityRiskLevelT
        ('riskLevel', c_uint8),
        # 客户原始风险等级
        ('originRiskLevel', c_uint8),
        # 机构标志 (0:个人投资者, 1:机构投资者)
        ('institutionFlag', c_uint8),
        # 投资者分类 @see eOesInvestorClassT
        ('investorClass', c_uint8),
        # 按64位对齐填充域
        ('__CUST_BASE_filler1', c_uint8 * 2),
        # 营业部代码
        ('branchId', c_int32),
        # 按64位对齐填充域
        ('__CUST_BASE_filler2', c_uint32),
    ]


# 证券账户基础信息的结构体定义
class OesInvAcctBaseInfoT(PrintableStructure):
    _fields_ = [
        # 股东账户代码
        ('invAcctId', c_char * OES_INV_ACCT_ID_MAX_LEN),
        # 市场 @see eOesMarketIdT
        ('mktId', c_uint8),
        # 账户类型 @see eOesAcctTypeT
        ('acctType', c_uint8),
        # 账户状态, 同步于主柜或者通过MON手动设置 @see eOesAcctStatusT
        ('status', c_uint8),
        # 股东账户的所有者类型 @see eOesOwnerTypeT
        ('ownerType', c_uint8),
        # 投资者期权等级 @see eOesOptInvLevelT
        ('optInvLevel', c_uint8),
        # 是否禁止交易 (仅供API查询使用)
        ('isTradeDisabled', c_uint8),
        # 按64位对齐填充域
        ('__INV_ACCT_BASE_filler', c_uint8 * 2),
        # 证券账户权限限制 @see eOesTradingLimitT
        ('limits', c_uint64),
        # 股东权限/客户权限 @see eOesTradingPermissionT
        ('permissions', c_uint64),
        # 席位号
        ('pbuId', c_int32),
        # 个股持仓比例阀值, 单位精确到百万分之一, 即 200002 = 20.0002%
        ('stkPositionLimitRatio', c_int32),
        # 主板权益 (新股认购限额)
        ('subscriptionQuota', c_int32),
        # 科创板权益 (新股认购限额)
        ('kcSubscriptionQuota', c_int32),
        # 预留的备用字段
        ('__INV_ACCT_BASE_reserve', c_char * 32),
    ]


# 股票持仓基础信息的结构体定义
class OesStkHoldingBaseInfoT(PrintableStructure):
    _fields_ = [
        # 账户代码
        ('invAcctId', c_char * OES_INV_ACCT_ID_MAX_LEN),
        # 证券代码
        ('securityId', c_char * OES_SECURITY_ID_MAX_LEN),
        # 市场代码 @see eOesMarketIdT
        ('mktId', c_uint8),
        # 证券类型 @see eOesSecurityTypeT
        ('securityType', c_uint8),
        # 证券子类型 @see eOesSubSecurityTypeT
        ('subSecurityType', c_uint8),
        # 产品类型 @see eOesProductTypeT
        ('productType', c_uint8),
        # 按64位对齐的填充域
        ('__HOLD_BASE_filler', c_uint8 * 4),
        # 日初持仓
        ('originalHld', c_int64),
        # 日初总持仓成本 (日初持仓成本价 = 日初总持仓成本 / 日初持仓)
        ('originalCostAmt', c_int64),
        # 日中累计买入持仓
        ('totalBuyHld', c_int64),
        # 日中累计卖出持仓
        ('totalSellHld', c_int64),
        # 当前卖出冻结持仓
        ('sellFrzHld', c_int64),
        # 手动冻结持仓
        ('manualFrzHld', c_int64),
        # 日中累计买入金额
        ('totalBuyAmt', c_int64),
        # 日中累计卖出金额
        ('totalSellAmt', c_int64),
        # 日中累计买入费用
        ('totalBuyFee', c_int64),
        # 日中累计卖出费用
        ('totalSellFee', c_int64),
        # 日中累计转换获得持仓, ETF申赎业务使用
        # - 成份证券持仓场景, 转换获得指赎回时获得的成份证券持仓;
        # - ETF证券持仓场景, 转换获得指申购时获得的ETF证券股持仓;
        ('totalTrsfInHld', c_int64),
        # 日中累计转换付出持仓, ETF申赎业务使用
        # - 成份证券持仓场景, 转换付出指申购时使用的成份证券持仓;
        # - ETF证券持仓场景, 转换付出指赎回时使用的ETF证券股持仓;
        ('totalTrsfOutHld', c_int64),
        # 当前转换付出冻结持仓
        ('trsfOutFrzHld', c_int64),
        # 日初锁定持仓
        ('originalLockHld', c_int64),
        # 日中累计锁定持仓
        ('totalLockHld', c_int64),
        # 日中累计解锁持仓
        ('totalUnlockHld', c_int64),
        # 日初可用持仓
        ('originalAvlHld', c_int64),
        # 当日最大可减持额度
        # - 小于0, 不进行减持额度控制
        # - 大于或等于0, 最大可减持额度
        ('maxReduceQuota', c_int64),
    ]


# 市场状态信息的结构体定义
class OesMarketStateInfoT(PrintableStructure):
    _fields_ = [
        ('exchId', c_uint8),  # 交易所代码 @see eOesExchangeIdT
        ('platformId', c_uint8),  # 交易平台类型 @see eOesPlatformIdT
        ('mktId', c_uint8),  # 市场代码 @see eOesMarketIdT
        ('mktState', c_uint8),  # 市场状态 @see eOesMarketStateT
        ('__filler', c_uint8 * 4),  # 按64位对齐的填充域
    ]


# 查询定位的游标结构
class OesQryCursorT(PrintableStructure):
    _fields_ = [
        # 查询位置
        ('seqNo', c_int32),
        # 是否是当前最后一个包
        ('isEnd', c_int8),
        # 按64位对齐填充域
        ('__filler', c_int8 * 3),
        # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
        ('userInfo', c_int64),
    ]


# 查询请求的消息头定义
class OesQryReqHeadT(PrintableStructure):
    _fields_ = [
        # 查询窗口大小
        ('maxPageSize', c_int32),
        # 查询起始位置
        ('lastPosition', c_int32),
    ]


# 查询应答的消息头定义
class OesQryRspHeadT(PrintableStructure):
    _fields_ = [
        # 查询到的信息条目数
        ('itemCount', c_int32),
        # 查询到的最后一条信息的位置
        ('lastPosition', c_int32),
        # 是否是当前查询最后一个包
        ('isEnd', c_int8),
        # 按64位对齐填充域
        ('__filler', c_uint8 * 7),
        # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
        ('userInfo', c_int64),
    ]


# 查询委托信息过滤条件
class OesQryOrdFilterT(PrintableStructure):
    _fields_ = [
        # 客户代码, 可选项
        ('custId', c_char * OES_CUST_ID_MAX_LEN),
        # 证券账户代码, 可选项
        ('invAcctId', c_char * OES_INV_ACCT_ID_MAX_LEN),
        # 市场代码, 可选项。如无需此过滤条件请使用 OES_MKT_ID_UNDEFINE
        # @see eOesMarketIdT
        ('mktId', c_uint8),
        # 是否仅查询未关闭委托 (包括未全部成交或撤销的委托)
        ('isUnclosedOnly', c_uint8),
        # 客户端环境号
        ('clEnvId', c_int8),
        # 证券类别  @see eOesSecurityTypeT
        ('securityType', c_uint8),
        # 买卖类型  @see eOesBuySellTypeT
        ('bsType', c_uint8),
        # 按64位对齐填充域
        ('__filler', c_uint8 * 3),
        # 客户委托编号, 可选项
        ('clOrdId', c_int64),
        # 客户委托流水号, 可选项
        ('clSeqNo', c_int64),
        # 查询委托的起始时间 (格式为 HHMMSSsss, 比如 141205000 表示 14:12:05.000)
        ('startTime', c_int32),
        # 查询委托的结束时间 (格式为 HHMMSSsss, 比如 141205000 表示 14:12:05.000)
        ('endTime', c_int32),
        # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
        ('userInfo', c_int64),
    ]


# 查询到的委托信息内容
OesOrdItemT = OesOrdCnfmT


# 查询委托信息请求
class OesQryOrdReqT(PrintableStructure):
    _fields_ = [
        # 查询请求消息头
        ('reqHead', OesQryReqHeadT),
        # 查询过滤条件
        ('qryFilter', OesQryOrdFilterT),
    ]


# 查询委托信息应答
class OesQryOrdRspT(PrintableStructure):
    _fields_ = [
        # 查询应答消息头
        ('rspHead', OesQryRspHeadT),
        # 委托信息数组
        ('qryItems', OesOrdItemT * OES_MAX_ORD_ITEM_CNT_PER_PACK),
    ]


# 查询成交信息过滤条件
class OesQryTrdFilterT(PrintableStructure):
    _fields_ = [
        # 客户代码, 可选项
        ('custId', c_char * OES_CUST_ID_MAX_LEN),
        # 证券账户代码, 可选项
        ('invAcctId', c_char * OES_INV_ACCT_ID_MAX_LEN),
        # 市场代码, 可选项。如无需此过滤条件请使用 OES_MKT_ID_UNDEFINE
        # @see eOesMarketIdT
        ('mktId', c_uint8),
        # 客户端环境号
        ('clEnvId', c_int8),
        # 证券类别  @see eOesSecurityTypeT
        ('securityType', c_uint8),
        # 买卖类型  @see eOesBuySellTypeT
        ('bsType', c_uint8),
        # 按64位对齐填充域
        ('__filler', c_uint32),
        # 内部委托编号, 可选项
        ('clOrdId', c_int64),
        # 客户委托流水号, 可选项
        ('clSeqNo', c_int64),
        # 成交开始时间 (格式为 HHMMSSsss, 形如 141205000)
        ('startTime', c_int32),
        # 成交结束时间
        ('endTime', c_int32),
        # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
        ('userInfo', c_int64),
    ]


# 查询到的成交信息内容
OesTrdItemT = OesTrdCnfmT


# 查询成交信息请求
class OesQryTrdReqT(PrintableStructure):
    _fields_ = [
        # 查询请求消息头
        ('reqHead', OesQryReqHeadT),
        # 查询过滤条件
        ('qryFilter', OesQryTrdFilterT),
    ]


# 查询成交信息应答
class OesQryTrdRspT(PrintableStructure):
    _fields_ = [
        # 查询应答消息头
        ('rspHead', OesQryRspHeadT),
        # 成交信息数组
        ('qryItems', OesTrdItemT * OES_MAX_TRD_ITEM_CNT_PER_PACK),
    ]


# 查询客户资金信息过滤条件
class OesQryCashAssetFilterT(PrintableStructure):
    _fields_ = [
        # 客户代码, 可选项
        ('custId', c_char * OES_CUST_ID_MAX_LEN),
        # 资金账户代码, 可选项
        ('cashAcctId', c_char * OES_CASH_ACCT_ID_MAX_LEN),
        # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
        ('userInfo', c_int64),
    ]


# 客户资金信息内容
class OesCashAssetItemT(PrintableStructure):
    _fields_ = [
        # 资金账户代码
        ('cashAcctId', c_char * OES_CASH_ACCT_ID_MAX_LEN),
        # 客户代码
        ('custId', c_char * OES_CUST_ID_MAX_LEN),
        # 币种 @see eOesCurrTypeT
        ('currType', c_uint8),
        # 资金帐户类别(冗余自资金账户) @see eOesCashTypeT
        ('cashType', c_uint8),
        # 资金帐户状态(冗余自资金账户) @see eOesAcctStatusT
        ('cashAcctStatus', c_uint8),
        # 是否禁止出入金 (仅供API查询使用)
        ('isFundTrsfDisabled', c_uint8),
        # 按64位对齐的填充域
        ('__CASH_ASSET_BASE_filler', c_uint8 * 4),
        # 期初余额, 单位精确到元后四位, 即1元 = 10000
        ('beginningBal', c_int64),
        # 期初可用余额, 单位精确到元后四位, 即1元 = 10000
        ('beginningAvailableBal', c_int64),
        # 期初可取余额, 单位精确到元后四位, 即1元 = 10000
        ('beginningDrawableBal', c_int64),
        # 不可用资金余额(既不可交易又不可提取), 单位精确到元后四位, 即1元 = 10000
        ('disableBal', c_int64),
        # 当前冲正金额(红冲蓝补的资金净额), 取值可以为负数(表示资金调出), 单位精确到元后四位(即1元 = 10000)
        ('reversalAmt', c_int64),
        # 手动冻结资金, 取值在0和当前资产之间, 单位精确到元后四位(即1元 = 10000)
        ('manualFrzAmt', c_int64),
        # 日中累计存入资金金额, 单位精确到元后四位, 即1元 = 10000
        ('totalDepositAmt', c_int64),
        # 日中累计提取资金金额, 单位精确到元后四位, 即1元 = 10000
        ('totalWithdrawAmt', c_int64),
        # 当前提取冻结资金金额, 单位精确到元后四位, 即1元 = 10000
        ('withdrawFrzAmt', c_int64),
        # 日中累计 卖/赎回 获得的可用资金金额, 单位精确到元后四位, 即1元 = 10000
        ('totalSellAmt', c_int64),
        # 日中累计 买/申购/逆回购 使用资金金额, 单位精确到元后四位, 即1元 = 10000
        ('totalBuyAmt', c_int64),
        # 当前交易冻结金额, 单位精确到元后四位, 即1元 = 10000
        ('buyFrzAmt', c_int64),
        # 日中累计交易费用金额, 单位精确到元后四位, 即1元 = 10000
        ('totalFeeAmt', c_int64),
        # 当前冻结交易费用金额, 单位精确到元后四位, 即1元 = 10000
        ('feeFrzAmt', c_int64),
        # 当前维持的保证金(衍生品账户时指开仓保证金)金额, 单位精确到元后四位, 即1元 = 10000
        ('marginAmt', c_int64),
        # 当前冻结的保证金(衍生品账户时指开仓在途冻结保证金)金额, 单位精确到元后四位, 即1元 = 10000
        ('marginFrzAmt', c_int64),
        # 当前余额, 包括当前可用余额和在途冻结资金在內的汇总值
        # 可用余额请参考“当前可用余额(currentAvailableBal)”字段
        ('currentTotalBal', c_int64),
        # 当前可用余额
        ('currentAvailableBal', c_int64),
        # 当前可取余额
        ('currentDrawableBal', c_int64),
    ]


# 查询客户资金信息请求
class OesQryCashAssetReqT(PrintableStructure):
    _fields_ = [
        # 查询请求消息头
        ('reqHead', OesQryReqHeadT),
        # 查询过滤条件
        ('qryFilter', OesQryCashAssetFilterT),
    ]


# 查询客户资金信息应答
class OesQryCashAssetRspT(PrintableStructure):
    _fields_ = [
        # 查询应答消息头
        ('rspHead', OesQryRspHeadT),
        # 客户资金信息数组
        ('qryItems', OesCashAssetItemT * OES_MAX_CASH_ASSET_ITEM_CNT_PER_PACK),
    ]


# 主柜资金信息内容
class OesCounterCashItemT(PrintableStructure):
    _fields_ = [
        # 资金账户代码
        ('cashAcctId', c_char * OES_CASH_ACCT_ID_MAX_LEN),
        # 客户代码
        ('custId', c_char * OES_CUST_ID_MAX_LEN),
        # 客户姓名
        ('custName', c_char * OES_CUST_NAME_MAX_LEN),
        # 银行代码
        ('bankId', c_char * OES_BANK_NO_MAX_LEN),
        ('cashType', c_uint8),  # 资金账户类别 @see eOesCashTypeT
        ('cashAcctStatus', c_uint8),  # 资金账户状态 @see eOesAcctStatusT
        ('currType', c_uint8),  # 币种类型 @see eOesCurrTypeT
        ('isFundTrsfDisabled', c_uint8),  # 出入金是否禁止标识
        ('__filler', c_uint8 * 4),  # 按64位对齐填充域
        ('counterAvailableBal', c_int64),  # 主柜可用余额，单位精确到元后四位，即1元 = 10000
        ('counterDrawableBal', c_int64),  # 主柜可取余额，单位精确到元后四位，即1元 = 10000
        ('counterCashUpdateTime', c_int64),  # 主柜资金更新时间 (seconds since the Epoch)
        ('__reserve', c_int64 * 4),  # 保留字段
    ]


# 查询主柜资金信息请求
class OesQryCounterCashReqT(PrintableStructure):
    _fields_ = [
        # 资金账号, 必输项
        ('cashAcctId', c_char * OES_CASH_ACCT_ID_MAX_LEN),
    ]


# 查询主柜资金信息应答
class OesQryCounterCashRspT(PrintableStructure):
    _fields_ = [
        # 主柜资金信息
        ('counterCashItem', OesCounterCashItemT),
    ]


# 查询股票持仓信息过滤条件
class OesQryStkHoldingFilterT(PrintableStructure):
    _fields_ = [
        # 客户代码, 可选项
        ('custId', c_char * OES_CUST_ID_MAX_LEN),
        # 证券账户代码, 可选项
        ('invAcctId', c_char * OES_INV_ACCT_ID_MAX_LEN),
        # 证券代码, 可选项
        ('securityId', c_char * OES_SECURITY_ID_MAX_LEN),
        # 市场代码  @see eOesMarketIdT
        ('mktId', c_uint8),
        # 证券类别  @see eOesSecurityTypeT
        ('securityType', c_uint8),
        # 产品类型 @see eOesProductTypeT
        ('productType', c_uint8),
        # 按64位对齐填充域
        ('__filler', c_uint8 * 5),
        # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
        ('userInfo', c_int64),
    ]


# 查询到的股票持仓信息内容
class OesStkHoldingItemT(PrintableStructure):
    _fields_ = [
        # 账户代码
        ('invAcctId', c_char * OES_INV_ACCT_ID_MAX_LEN),
        # 证券代码
        ('securityId', c_char * OES_SECURITY_ID_MAX_LEN),
        # 市场代码 @see eOesMarketIdT
        ('mktId', c_uint8),
        # 证券类型 @see eOesSecurityTypeT
        ('securityType', c_uint8),
        # 证券子类型 @see eOesSubSecurityTypeT
        ('subSecurityType', c_uint8),
        # 产品类型 @see eOesProductTypeT
        ('productType', c_uint8),
        # 按64位对齐的填充域
        ('__HOLD_BASE_filler', c_uint8 * 4),
        # 日初持仓
        ('originalHld', c_int64),
        # 日初总持仓成本 (日初持仓成本价 = 日初总持仓成本 / 日初持仓)
        ('originalCostAmt', c_int64),
        # 日中累计买入持仓
        ('totalBuyHld', c_int64),
        # 日中累计卖出持仓
        ('totalSellHld', c_int64),
        # 当前卖出冻结持仓
        ('sellFrzHld', c_int64),
        # 手动冻结持仓
        ('manualFrzHld', c_int64),
        # 日中累计买入金额
        ('totalBuyAmt', c_int64),
        # 日中累计卖出金额
        ('totalSellAmt', c_int64),
        # 日中累计买入费用
        ('totalBuyFee', c_int64),
        # 日中累计卖出费用
        ('totalSellFee', c_int64),
        # 日中累计转换获得持仓, ETF申赎业务使用
        # - 成份证券持仓场景, 转换获得指赎回时获得的成份证券持仓;
        # - ETF证券持仓场景, 转换获得指申购时获得的ETF证券股持仓;
        ('totalTrsfInHld', c_int64),
        # 日中累计转换付出持仓, ETF申赎业务使用
        # - 成份证券持仓场景, 转换付出指申购时使用的成份证券持仓;
        # - ETF证券持仓场景, 转换付出指赎回时使用的ETF证券股持仓;
        ('totalTrsfOutHld', c_int64),
        # 当前转换付出冻结持仓
        ('trsfOutFrzHld', c_int64),
        # 日初锁定持仓
        ('originalLockHld', c_int64),
        # 日中累计锁定持仓
        ('totalLockHld', c_int64),
        # 日中累计解锁持仓
        ('totalUnlockHld', c_int64),
        # 日初可用持仓
        ('originalAvlHld', c_int64),
        # 当日最大可减持额度
        # - 小于0, 不进行减持额度控制
        # - 大于或等于0, 最大可减持额度
        ('maxReduceQuota', c_int64),
        # 当前可卖持仓
        ('sellAvlHld', c_int64),
        # 当前可转换付出持仓
        ('trsfOutAvlHld', c_int64),
        # 当前可锁定持仓
        ('lockAvlHld', c_int64),
        # 保留字段
        ('__filler', c_int64),
        # 总持仓, 包括当前可用持仓、不可交易持仓和在途冻结持仓在內的汇总值
        # 可卖持仓请参考“当前可卖持仓(sellAvlHld)”字段
        ('sumHld', c_int64),
        # 持仓成本价
        ('costPrice', c_int64),
    ]


# 查询股票持仓信息请求
class OesQryStkHoldingReqT(PrintableStructure):
    _fields_ = [
        # 查询请求消息头
        ('reqHead', OesQryReqHeadT),
        # 查询过滤条件
        ('qryFilter', OesQryStkHoldingFilterT),
    ]


# 查询股票持仓信息应答
class OesQryStkHoldingRspT(PrintableStructure):
    _fields_ = [
        # 查询应答消息头
        ('qryHead', OesQryRspHeadT),
        # 持仓信息数组
        ('qryItems', OesStkHoldingItemT * OES_MAX_HOLDING_ITEM_CNT_PER_PACK),
    ]


# 查询客户信息过滤条件
class OesQryCustFilterT(PrintableStructure):
    _fields_ = [
        # 客户代码, 可选项
        ('custId', c_char * OES_CUST_ID_MAX_LEN),
        # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
        ('userInfo', c_int64),
    ]


# 客户信息内容
OesCustItemT = OesCustBaseInfoT


# 查询客户信息请求
class OesQryCustReqT(PrintableStructure):
    _fields_ = [
        # 查询请求消息头
        ('reqHead', OesQryReqHeadT),
        # 查询过滤条件
        ('qryFilter', OesQryCustFilterT),
    ]


# 查询客户信息应答
class OesQryCustRspT(PrintableStructure):
    _fields_ = [
        # 查询应答消息头
        ('rspHead', OesQryRspHeadT),
        # 客户信息数组
        ('qryItems', OesCustItemT * OES_MAX_CUST_ITEM_CNT_PER_PACK),
    ]


# 查询证券账户信息过滤条件
class OesQryInvAcctFilterT(PrintableStructure):
    _fields_ = [
        # 客户代码, 可选项
        ('custId', c_char * OES_CUST_ID_MAX_LEN),
        # 证券账户代码, 可选项
        ('invAcctId', c_char * OES_INV_ACCT_ID_MAX_LEN),
        # 市场代码, 可选项。如无需此过滤条件请使用 OES_MKT_ID_UNDEFINE
        # @see eOesMarketIdT
        ('mktId', c_uint8),
        # 按64位对齐填充域
        ('__filler', c_uint8 * 7),
        # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
        ('userInfo', c_int64),
    ]


# 证券账户内容
class OesInvAcctItemT(PrintableStructure):
    _fields_ = [
        # 股东账户代码
        ('invAcctId', c_char * OES_INV_ACCT_ID_MAX_LEN),
        # 市场 @see eOesMarketIdT
        ('mktId', c_uint8),
        # 账户类型 @see eOesAcctTypeT
        ('acctType', c_uint8),
        # 账户状态, 同步于主柜或者通过MON手动设置 @see eOesAcctStatusT
        ('status', c_uint8),
        # 股东账户的所有者类型 @see eOesOwnerTypeT
        ('ownerType', c_uint8),
        # 投资者期权等级 @see eOesOptInvLevelT
        ('optInvLevel', c_uint8),
        # 是否禁止交易 (仅供API查询使用)
        ('isTradeDisabled', c_uint8),
        # 按64位对齐填充域
        ('__INV_ACCT_BASE_filler', c_uint8 * 2),
        # 证券账户权限限制 @see eOesTradingLimitT
        ('limits', c_uint64),
        # 股东权限/客户权限 @see eOesTradingPermissionT
        ('permissions', c_uint64),
        # 席位号
        ('pbuId', c_int32),
        # 个股持仓比例阀值, 单位精确到百万分之一, 即 200002 = 20.0002%
        ('stkPositionLimitRatio', c_int32),
        # 主板权益 (新股认购限额)
        ('subscriptionQuota', c_int32),
        # 科创板权益 (新股认购限额)
        ('kcSubscriptionQuota', c_int32),
        # 预留的备用字段
        ('__INV_ACCT_BASE_reserve', c_char * 32),
        # 客户代码
        ('custId', c_char * OES_CUST_ID_MAX_LEN),
    ]


# 查询证券账户信息请求
class OesQryInvAcctReqT(PrintableStructure):
    _fields_ = [
        # 查询请求消息头
        ('reqHead', OesQryReqHeadT),
        # 查询过滤条件
        ('qryFilter', OesQryInvAcctFilterT),
    ]


# 查询证券账户信息应答
class OesQryInvAcctRspT(PrintableStructure):
    _fields_ = [
        # 查询应答消息头
        ('rspHead', OesQryRspHeadT),
        # 证券账户信息数组
        ('qryItems', OesInvAcctItemT * OES_MAX_INV_ACCT_ITEM_CNT_PER_PACK),
    ]


# 股东账户总览信息内容
class OesInvAcctOverviewT(PrintableStructure):
    _fields_ = [
        # 股东账户代码
        ('invAcctId', c_char * OES_INV_ACCT_ID_MAX_LEN),
        # 市场 @see eOesMarketIdT
        ('mktId', c_uint8),
        # 账户类型 @see eOesAcctTypeT
        ('acctType', c_uint8),
        # 账户状态 @see eOesAcctStatusT
        ('status', c_uint8),
        # 股东账户的所有者类型 @see eOesOwnerTypeT
        ('ownerType', c_uint8),
        # 投资者期权等级 @see eOesOptInvLevelT
        ('optInvLevel', c_uint8),
        # 是否禁止交易 (仅供API查询使用)
        ('isTradeDisabled', c_uint8),
        # 按64位对齐填充域
        ('__INV_ACCT_BASE_filler', c_uint8 * 2),
        # 证券账户权限限制 @see eOesTradingLimitT
        ('limits', c_uint64),
        # 股东权限/客户权限 @see eOesTradingPermissionT
        ('permissions', c_uint64),
        # 席位号
        ('pbuId', c_int32),
        # 主板权益 (新股/配股认购限额)
        ('subscriptionQuota', c_int32),
        # 客户代码
        ('custId', c_char * OES_CUST_ID_MAX_LEN),
        ('isValid', c_uint8),  # 股东账户是否有效标识
        ('__filler', c_uint8 * 3),  # 按64位对齐的填充域
        ('kcSubscriptionQuota', c_int32),  # 科创板权益 (新股/配股认购限额)
        ('trdOrdCnt', c_int32),  # 当日累计有效交易类委托笔数统计
        ('nonTrdOrdCnt', c_int32),  # 当日累计有效非交易类委托笔数统计
        ('cancelOrdCnt', c_int32),  # 当日累计有效撤单笔数统计
        ('oesRejectOrdCnt', c_int32),  # 当日累计被OES拒绝的委托笔数统计
        ('exchRejectOrdCnt', c_int32),  # 当日累计被交易所拒绝的委托笔数统计
        ('trdCnt', c_int32),  # 当日累计成交笔数统计
        ('__reserve', c_int64),  # 备用字段
    ]


# 资金账户总览信息内容
class OesCashAcctOverviewT(PrintableStructure):
    _fields_ = [
        # 资金账户代码
        ('cashAcctId', c_char * OES_CASH_ACCT_ID_MAX_LEN),
        # 客户代码
        ('custId', c_char * OES_CUST_ID_MAX_LEN),
        # 银行代码
        ('bankId', c_char * OES_BANK_NO_MAX_LEN),
        ('isValid', c_uint8),  # 资金账户是否有效标识
        ('cashType', c_uint8),  # 资金账户类别 @see eOesCashTypeT
        ('cashAcctStatus', c_uint8),  # 资金账户状态 @see eOesAcctStatusT
        ('currType', c_uint8),  # 币种类型 @see eOesCurrTypeT
        ('isFundTrsfDisabled', c_uint8),  # 出入金是否禁止标识
        ('__filler', c_uint8 * 3),  # 按64位对齐的填充域
        ('__reserve', c_int64),  # 备用字段
    ]


# 客户总览信息内容
class OesCustOverviewT(PrintableStructure):
    _fields_ = [
        # 客户代码
        ('custId', c_char * OES_CUST_ID_MAX_LEN),
        # 客户类型 @see eOesCustTypeT
        ('custType', c_uint8),
        # 客户状态 (0:正常, 非0:不正常)
        ('status', c_uint8),
        # OES风险等级 @see eOesSecurityRiskLevelT
        ('riskLevel', c_uint8),
        # 客户原始风险等级
        ('originRiskLevel', c_uint8),
        # 机构标志 (0:个人投资者, 1:机构投资者)
        ('institutionFlag', c_uint8),
        # 投资者分类 @see eOesInvestorClassT
        ('investorClass', c_uint8),
        # 按64位对齐填充域
        ('__CUST_BASE_filler1', c_uint8 * 2),
        # 营业部代码
        ('branchId', c_int32),
        # 按64位对齐填充域
        ('__CUST_BASE_filler2', c_uint32),
        # 客户姓名
        ('custName', c_char * OES_CUST_NAME_MAX_LEN),
        ('spotCashAcct', OesCashAcctOverviewT),  # 普通资金账户信息
        ('creditCashAcct', OesCashAcctOverviewT),  # 信用资金账户信息
        ('optionCashAcct', OesCashAcctOverviewT),  # 衍生品资金账户信息
        ('shSpotInvAcct', OesInvAcctOverviewT),  # 上海现货股东账户信息
        ('shOptionInvAcct', OesInvAcctOverviewT),  # 上海衍生品股东账户信息
        ('szSpotInvAcct', OesInvAcctOverviewT),  # 深圳现货股东账户信息
        ('szOptionInvAcct', OesInvAcctOverviewT),  # 深圳衍生品股东账户信息
        ('__reserve', c_int64),  # 备用字段
    ]


# 客户端总览信息内容
class OesClientOverviewT(PrintableStructure):
    _fields_ = [
        ('clientId', c_int16),  # 客户端编号
        ('clientType', c_uint8),  # 客户端类型  @see eOesClientTypeT
        ('clientStatus', c_uint8),  # 客户端状态  @see eOesClientStatusT
        ('isApiForbidden', c_uint8),  # API禁用标识
        ('isBlockTrader', c_uint8),  # 是否大宗交易标识
        ('businessScope', c_uint8),  # 客户端适用的业务范围 @see eOesBusinessTypeT
        ('__filler', c_uint8),  # 按64位对齐的填充域
        ('logonTime', c_int64),  # 客户端登录(委托接收服务)时间
        # 客户端名称
        ('clientName', c_char * OES_CLIENT_NAME_MAX_LEN),
        # 客户端说明
        ('clientMemo', c_char * OES_CLIENT_DESC_MAX_LEN),
        ('sseStkPbuId', c_int32),  # 上海现货/信用账户对应的PBU代码
        ('sseOptPbuId', c_int32),  # 上海衍生品账户对应的PBU代码
        ('sseQualificationClass', c_uint8),  # 上海股东账户的投资者适当性管理分类 @see eOesQualificationClassT
        ('__filler2', c_uint8 * 7),  # 按64位对齐填充域
        ('szseStkPbuId', c_int32),  # 深圳现货/信用账户对应的PBU代码
        ('szseOptPbuId', c_int32),  # 深圳衍生品账户对应的PBU代码
        ('szseQualificationClass', c_uint8),  # 深圳股东账户的投资者适当性管理分类 @see eOesQualificationClassT
        ('__filler3', c_uint8 * 7),  # 按64位对齐填充域
        ('currOrdConnected', c_int32),  # 当前已连接的委托通道数量
        ('currRptConnected', c_int32),  # 当前已连接的回报通道数量
        ('currQryConnected', c_int32),  # 当前已连接的查询通道数量
        ('maxOrdConnect', c_int32),  # 委托通道允许的最大同时连接数量
        ('maxRptConnect', c_int32),  # 回报通道允许的最大同时连接数量
        ('maxQryConnect', c_int32),  # 查询通道允许的最大同时连接数量
        ('ordTrafficLimit', c_int32),  # 委托通道的流量控制
        ('qryTrafficLimit', c_int32),  # 查询通道的流量控制
        ('maxOrdCount', c_int32),  # 最大委托笔数限制
        ('__reserve', c_int32),  # 备用字段
        ('associatedCustCnt', c_int32),  # 客户端关联的客户数量
        ('__filler4', c_int32),  # 按64位对齐的填充域
        # 客户端关联的客户列表
        ('custItems', OesCustOverviewT * OES_MAX_CUST_PER_CLIENT),
    ]


# 查询客户佣金信息过滤条件
class OesQryCommissionRateFilterT(PrintableStructure):
    _fields_ = [
        # 客户代码, 可选项
        ('custId', c_char * OES_CUST_ID_MAX_LEN),
        # 市场代码, 可选项。如无需此过滤条件请使用 OES_MKT_ID_UNDEFINE
        # @see eOesMarketIdT
        ('mktId', c_uint8),
        # 证券类别, 可选项。如无需此过滤条件请使用 OES_SECURITY_TYPE_UNDEFINE
        # @see eOesSecurityTypeT
        ('securityType', c_uint8),
        # 买卖类型, 可选项。如无需此过滤条件请使用 OES_BS_TYPE_UNDEFINE
        # @see eOesBuySellTypeT
        ('bsType', c_uint8),
        # 按64位对齐填充域
        ('__filler', c_uint8 * 5),
        # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
        ('userInfo', c_int64),
    ]


# 客户佣金信息内容定义
class OesCommissionRateItemT(PrintableStructure):
    _fields_ = [
        # 客户代码
        ('custId', c_char * OES_CUST_ID_MAX_LEN),
        # 证券代码
        ('securityId', c_char * OES_SECURITY_ID_MAX_LEN),
        # 市场 @see eOesMarketIdT
        ('mktId', c_uint8),
        # 证券类别 @see eOesSecurityTypeT
        ('securityType', c_uint8),
        # 证券子类别 @see eOesSubSecurityTypeT
        ('subSecurityType', c_uint8),
        # 买卖类型 @see eOesBuySellTypeT
        ('bsType', c_uint8),
        # 费用标识 @see eOesFeeTypeT
        ('feeType', c_uint8),
        # 币种 @see eOesCurrTypeT
        ('currType', c_uint8),
        # 计算模式 @see eOesCalcFeeModeT
        ('calcFeeMode', c_uint8),
        # 按64位对齐填充域
        ('__filler', c_uint8),
        # 费率, 单位精确到千万分之一, 即费率0.02% = 2000
        ('feeRate', c_int64),
        # 最低费用, 大于0时有效 (单位：万分之一元)
        ('minFee', c_int32),
        # 最高费用, 大于0时有效 (单位：万分之一元)
        ('maxFee', c_int32),
    ]


# 查询客户佣金信息请求
class OesQryCommissionRateReqT(PrintableStructure):
    _fields_ = [
        # 查询请求消息头
        ('reqHead', OesQryReqHeadT),
        # 查询过滤条件
        ('qryFilter', OesQryCommissionRateFilterT),
    ]


# 查询客户佣金信息应答
class OesQryCommissionRateRspT(PrintableStructure):
    _fields_ = [
        # 查询应答消息头
        ('rspHead', OesQryRspHeadT),
        # 客户佣金信息数组
        ('qryItems', OesCommissionRateItemT * OES_MAX_COMMS_RATE_ITEM_CNT_PER_PACK),
    ]


# 查询出入金流水信息过滤条件
class OesQryFundTransferSerialFilterT(PrintableStructure):
    _fields_ = [
        # 客户代码, 可选项
        ('custId', c_char * OES_CUST_ID_MAX_LEN),
        # 资金账户代码, 可选项
        ('cashAcctId', c_char * OES_CASH_ACCT_ID_MAX_LEN),
        # 出入金流水号, 可选项
        ('clSeqNo', c_int32),
        # 客户端环境号
        ('clEnvId', c_int8),
        # 按64位对齐填充域
        ('__filler', c_uint8 * 3),
        # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
        ('userInfo', c_int64),
    ]


# 查询出入金流水信息应答
OesFundTransferSerialItemT = OesFundTrsfReportT


# 查询出入金流水信息请求
class OesQryFundTransferSerialReqT(PrintableStructure):
    _fields_ = [
        # 查询请求消息头
        ('reqHead', OesQryReqHeadT),
        # 查询过滤条件
        ('qryFilter', OesQryFundTransferSerialFilterT),
    ]


# 查询出入金流水信息应答
class OesQryFundTransferSerialRspT(PrintableStructure):
    _fields_ = [
        # 查询应答消息头
        ('rspHead', OesQryRspHeadT),
        # 出入金流水信息数组
        ('qryItems', OesFundTransferSerialItemT * OES_MAX_FUND_TRSF_ITEM_CNT_PER_PACK),
    ]


# 查询新股配号、中签信息过滤条件
class OesQryLotWinningFilterT(PrintableStructure):
    _fields_ = [
        # 客户代码, 可选项
        ('custId', c_char * OES_CUST_ID_MAX_LEN),
        # 证券账户代码, 可选项
        ('invAcctId', c_char * OES_INV_ACCT_ID_MAX_LEN),
        # 市场代码, 可选项。如无需此过滤条件请使用 OES_MKT_ID_UNDEFINE
        # @see eOesMarketIdT
        ('mktId', c_uint8),
        # 中签、配号记录类型, 可选项。如无需此过滤条件请使用 OES_LOT_TYPE_UNDEFINE
        # @see eOesLotTypeT
        ('lotType', c_uint8),
        # 按64位对齐填充域
        ('__filler', c_uint8 * 6),
        # 查询起始日期 (格式为 YYYYMMDD)
        ('startDate', c_int32),
        # 查询结束日期 (格式为 YYYYMMDD)
        ('endDate', c_int32),
        # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
        ('userInfo', c_int64),
    ]


# 新股配号、中签信息内容
OesLotWinningItemT = OesLotWinningBaseInfoT


# 查询新股认购、中签信息请求
class OesQryLotWinningReqT(PrintableStructure):
    _fields_ = [
        # 查询请求消息头
        ('reqHead', OesQryReqHeadT),
        # 查询过滤条件
        ('qryFilter', OesQryLotWinningFilterT),
    ]


# 查询新股配号、中签信息应答
class OesQryLotWinningRspT(PrintableStructure):
    _fields_ = [
        # 查询应答消息头
        ('rspHead', OesQryRspHeadT),
        # 新股认购、中签信息数组
        ('qryItems', OesLotWinningItemT * OES_MAX_LOG_WINNING_ITEM_CNT_PER_PACK),
    ]


# 查询证券发行信息过滤条件
class OesQryIssueFilterT(PrintableStructure):
    _fields_ = [
        # 证券发行代码, 可选项
        ('securityId', c_char * OES_SECURITY_ID_MAX_LEN),
        # 市场代码, 可选项。如无需此过滤条件请使用 OES_MKT_UNDEFINE
        # @see eOesMarketIdT
        ('mktId', c_uint8),
        # 产品类型, 默认类型为 OES_PRODUCT_TYPE_IPO
        # @see eOesProductTypeT
        ('productType', c_uint8),
        # 按64位对齐填充域
        ('__filler', c_uint8 * 6),
        # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
        ('userInfo', c_int64),
    ]


# 证券发行信息内容
OesIssueItemT = OesIssueBaseInfoT


# 查询证券发行信息请求
class OesQryIssueReqT(PrintableStructure):
    _fields_ = [
        # 查询请求消息头
        ('reqHead', OesQryReqHeadT),
        # 查询过滤条件
        ('qryFilter', OesQryIssueFilterT),
    ]


# 查询证券发行信息应答
class OesQryIssueRspT(PrintableStructure):
    _fields_ = [
        # 查询应答消息头
        ('rspHead', OesQryRspHeadT),
        # 证券发行信息数组
        ('qryItems', OesIssueItemT * OES_MAX_ISSUE_ITEM_CNT_PER_PACK),
    ]


# 查询现货产品信息过滤条件
class OesQryStockFilterT(PrintableStructure):
    _fields_ = [
        # 证券代码, 可选项
        ('securityId', c_char * OES_SECURITY_ID_MAX_LEN),
        # 市场代码, 可选项。如无需此过滤条件请使用 OES_MKT_ID_UNDEFINE
        # @see eOesMarketIdT
        ('mktId', c_uint8),
        # 证券类别  @see eOesSecurityTypeT
        ('securityType', c_uint8),
        # 证券子类别  @see eOesSubSecurityTypeT
        ('subSecurityType', c_uint8),
        # 按64位对齐填充域
        ('__filler', c_uint8 * 5),
        # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
        ('userInfo', c_int64),
    ]


# 现货产品信息内容
OesStockItemT = OesStockBaseInfoT


# 查询现货产品信息请求
class OesQryStockReqT(PrintableStructure):
    _fields_ = [
        # 查询请求消息头
        ('reqHead', OesQryReqHeadT),
        # 查询过滤条件
        ('qryFilter', OesQryStockFilterT),
    ]


# 查询现货产品信息应答
class OesQryStockRspT(PrintableStructure):
    _fields_ = [
        # 查询应答消息头
        ('rspHead', OesQryRspHeadT),
        # 现货产品信息数组
        ('qryItems', OesStockItemT * OES_MAX_STOCK_ITEM_CNT_PER_PACK),
    ]


# 查询ETF申赎产品信息过滤条件
class OesQryEtfFilterT(PrintableStructure):
    _fields_ = [
        # ETF基金申赎代码, 可选项
        ('fundId', c_char * OES_SECURITY_ID_MAX_LEN),
        # ETF基金市场代码, 可选项。如无需此过滤条件请使用 OES_MKT_ID_UNDEFINE
        # @see eOesMarketIdT
        ('mktId', c_uint8),
        # 按64位对齐填充域
        ('__filler', c_uint8 * 7),
        # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
        ('userInfo', c_int64),
    ]


# ETF申赎产品信息内容
OesEtfItemT = OesEtfBaseInfoT


# 查询ETF申赎产品信息请求
class OesQryEtfReqT(PrintableStructure):
    _fields_ = [
        # 查询请求消息头
        ('reqHead', OesQryReqHeadT),
        # 查询过滤条件
        ('qryFilter', OesQryEtfFilterT),
    ]


# 查询ETF申赎产品信息应答
class OesQryEtfRspT(PrintableStructure):
    _fields_ = [
        # 查询应答消息头
        ('rspHead', OesQryRspHeadT),
        # ETF申赎产品信息数组
        ('qryItems', OesEtfItemT * OES_MAX_ETF_ITEM_CNT_PER_PACK),
    ]


# 查询ETF成份证券信息过滤条件
class OesQryEtfComponentFilterT(PrintableStructure):
    _fields_ = [
        # ETF基金申赎代码
        ('fundId', c_char * OES_SECURITY_ID_MAX_LEN),
        # ETF基金市场代码, 可选项。如无需此过滤条件请使用 OES_MKT_ID_UNDEFINE
        # @see eOesMarketIdT
        ('fundMktId', c_uint8),
        # 按64位对齐填充域
        ('__filler', c_uint8 * 7),
        # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
        ('userInfo', c_int64),
    ]


# ETF基金成份证券信息内容
class OesEtfComponentItemT(PrintableStructure):
    _fields_ = [
        # ETF基金申赎代码
        ('fundId', c_char * OES_SECURITY_ID_MAX_LEN),
        # 成份证券代码
        ('securityId', c_char * OES_SECURITY_ID_MAX_LEN),
        # 成份证券市场代码 @see eOesMarketIdT
        ('mktId', c_uint8),
        # ETF基金市场代码 @see eOesMarketIdT
        ('fundMktId', c_uint8),
        # 现金替代标识 @see eOesEtfSubFlagT
        ('subFlag', c_uint8),
        # 成份证券的证券类型 @see eOesSecurityTypeT
        ('securityType', c_uint8),
        # 成份证券的证券子类型 @see eOesSubSecurityTypeT
        ('subSecurityType', c_uint8),
        # 是否是作为申赎对价的成份证券
        # @note 注意事项:
        # - 非申赎对价的成份证券信息仅供参考, 申赎时不能对该类成份证券进行股份计算
        # 或现金替代处理。
        # - 例如: 深交所跨市场ETF中的沪市成份证券信息就属于非申赎对价的成份证券信息,
        # 对深交所跨市场ETF进行申赎时应使用 159900 虚拟成份券进行沪市成份证券份额
        # 的现金替代处理
        ('isTrdComponent', c_uint8),
        # 按64位对齐填充域
        ('__ETF_COMPONENT_BASE_filler', c_uint8 * 2),
        # 前收盘价格, 单位精确到元后四位, 即1元 = 10000
        ('prevClose', c_int32),
        # 成份证券数量
        ('qty', c_int32),
        # union {
        # 申购溢价比例, 单位精确到十万分之一, 即溢价比例10% = 10000
        ('premiumRatio', c_int32),
        # 申购溢价比例 @deprecated 已废弃, 为了兼容旧版本而保留
        # ('premiumRate', c_int32),
        # };
        # 赎回折价比例, 单位精确到十万分之一, 即折价比例10% = 10000
        ('discountRatio', c_int32),
        # 申购替代金额, 单位精确到元后四位, 即1元 = 10000
        ('creationSubCash', c_int64),
        # union {
        # 赎回替代金额, 单位精确到元后四位, 即1元 = 10000
        ('redemptionSubCash', c_int64),
        # 赎回替代金额 @deprecated 已废弃, 为了兼容旧版本而保留
        # ('redemptionCashSub', c_int64),
        # };
        # 成份证券名称
        ('securityName', c_char * OES_SECURITY_NAME_MAX_LEN),
        # 预留的备用字段
        ('__reserve', c_char * 96),
    ]


# 查询ETF基金成份证券信息请求
class OesQryEtfComponentReqT(PrintableStructure):
    _fields_ = [
        # 查询请求消息头
        ('reqHead', OesQryReqHeadT),
        # 查询过滤条件
        ('qryFilter', OesQryEtfComponentFilterT),
    ]


# 查询ETF基金成份证券信息应答
class OesQryEtfComponentRspT(PrintableStructure):
    _fields_ = [
        # 查询应答消息头
        ('rspHead', OesQryRspHeadT),
        # ETF基金成份证券信息数组
        ('qryItems', OesEtfComponentItemT * OES_MAX_ETF_COMPONENT_ITEM_CNT_PER_PACK),
    ]


# 查询当前交易日信息应答
class OesQryTradingDayRspT(PrintableStructure):
    _fields_ = [
        # 交易日
        ('tradingDay', c_int32),
        # 按64位对齐填充域
        ('__filler', c_int32),
    ]


# 查询市场状态信息过滤条件
class OesQryMarketStateFilterT(PrintableStructure):
    _fields_ = [
        # 交易所代码 (可选项, 为 0 则匹配所有交易所)
        # @see eOesExchangeIdT
        ('exchId', c_uint8),
        # 交易平台代码 (可选项, 为 0 则匹配所有交易平台)
        # @see eOesPlatformIdT
        ('platformId', c_uint8),
        # 按64位对齐填充域
        ('__filler', c_uint8 * 6),
        # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
        ('userInfo', c_int64),
    ]


# 市场状态信息内容
OesMarketStateItemT = OesMarketStateInfoT


# 查询市场状态信息请求
class OesQryMarketStateReqT(PrintableStructure):
    _fields_ = [
        # 查询请求消息头
        ('reqHead', OesQryReqHeadT),
        # 查询过滤条件
        ('qryFilter', OesQryMarketStateFilterT),
    ]


# 查询市场状态信息应答
class OesQryMarketStateRspT(PrintableStructure):
    _fields_ = [
        # 查询应答消息头
        ('rspHead', OesQryRspHeadT),
        # 市场状态信息数组
        ('qryItems', OesMarketStateItemT * OES_MAX_MKT_STATE_ITEM_CNT_PER_PACK),
    ]


# 券商参数信息内容
class OesBrokerParamsInfoT(PrintableStructure):
    _fields_ = [
        # 券商名称
        ('brokerName', c_char * OES_BROKER_NAME_MAX_LEN),
        # 券商联系电话
        ('brokerPhone', c_char * OES_BROKER_PHONE_MAX_LEN),
        # 券商网址
        ('brokerWebsite', c_char * OES_BROKER_WEBSITE_MAX_LEN),
        # 当前API协议版本号
        ('apiVersion', c_char * OES_VER_ID_MAX_LEN),
        # 为兼容协议而添加的填充域
        ('__filler1', c_char * 8),
        # API兼容的最低协议版本号
        ('apiMinVersion', c_char * OES_VER_ID_MAX_LEN),
        # 为兼容协议而添加的填充域
        ('__filler2', c_char * 8),
        # 客户端最新的版本号
        ('clientVersion', c_char * OES_VER_ID_MAX_LEN),
        # 为兼容协议而添加的填充域
        ('__filler3', c_char * 8),
        # 允许客户端修改密码的开始时间 (HHMMSSsss)
        ('changePwdLimitTime', c_int32),
        # 客户端密码允许的最小长度
        ('minClientPasswordLen', c_int32),
        # 客户端密码强度级别
        # 密码强度范围[0~4]，密码含有字符种类(大写字母、小写字母、数字、有效符号)的个数
        ('clientPasswordStrength', c_int32),
        # 按64位对齐填充域
        ('__filler4', c_uint8 * 4),
        # 预留的备用字段
        ('__reserve', c_char * 256),
    ]


# 查询券商参数信息应答
class OesQryBrokerParamsInfoRspT(PrintableStructure):
    _fields_ = [
        ('brokerParams', OesBrokerParamsInfoT),
    ]


# 应用程序升级源信息
class OesApplUpgradeSourceT(PrintableStructure):
    _fields_ = [
        # IP地址
        ('ipAddress', c_char * OES_MAX_IP_LEN),
        # 协议名称
        ('protocol', c_char * OES_APPL_UPGRADE_PROTOCOL_MAX_LEN),
        # 用户名
        ('username', c_char * OES_CLIENT_NAME_MAX_LEN),
        # 登录密码
        ('password', c_char * OES_PWD_MAX_LEN),
        # 登录密码的加密方法
        ('encryptMethod', c_int32),
        # 按64位对齐的填充域
        ('__filler', c_int32),
        # 根目录地址
        ('homePath', c_char * SPK_MAX_PATH_LEN),
        # 文件名称
        ('fileName', c_char * SPK_MAX_PATH_LEN),
    ]


# 单个应用程序升级信息
class OesApplUpgradeItemT(PrintableStructure):
    _fields_ = [
        # 应用程序名称
        ('applName', c_char * OES_MAX_COMP_ID_LEN),
        # 应用程序的最低协议版本号
        ('minApplVerId', c_char * OES_VER_ID_MAX_LEN),
        # 应用程序的最高协议版本号
        ('maxApplVerId', c_char * OES_VER_ID_MAX_LEN),
        # 废弃的应用版本号列表
        ('discardApplVerId', c_char * OES_VER_ID_MAX_LEN * OES_APPL_DISCARD_VERSION_MAX_COUNT),
        # 废弃版本号的数目
        ('discardVerCount', c_int32),
        # 最新协议版本的日期
        ('newApplVerDate', c_int32),
        # 应用程序的最新协议版本号
        ('newApplVerId', c_char * OES_VER_ID_MAX_LEN),
        # 最新协议版本的标签信息
        ('newApplVerTag', c_char * OES_CLIENT_TAG_MAX_LEN),
        # 主用升级源配置信息
        ('primarySource', OesApplUpgradeSourceT),
        # 备用升级源配置信息
        ('secondarySource', OesApplUpgradeSourceT),
    ]


# OES周边应用程序升级信息
class OesApplUpgradeInfoT(PrintableStructure):
    _fields_ = [
        # 客户端升级配置信息
        ('clientUpgradeInfo', OesApplUpgradeItemT),
        # C_API升级配置信息
        ('cApiUpgradeInfo', OesApplUpgradeItemT),
        # JAVA_API升级配置信息
        ('javaApiUpgradeInfo', OesApplUpgradeItemT),
    ]


# 查询周边应用升级配置信息应答
class OesQryApplUpgradeInfoRspT(PrintableStructure):
    _fields_ = [
        ('applUpgradeInfo', OesApplUpgradeInfoT),
    ]


# 统一的查询请求消息定义
class OesQryReqMsgT(PrintableUnion):
    _fields_ = [
        ('qryOrd', OesQryOrdReqT),  # 查询委托信息请求
        ('qryTrd', OesQryTrdReqT),  # 查询成交信息请求
        ('qryCashAsset', OesQryCashAssetReqT),  # 查询客户资金信息请求
        ('qryStkHolding', OesQryStkHoldingReqT),  # 查询股票持仓信息请求
        ('qryCust', OesQryCustReqT),  # 查询客户信息请求
        ('qryInvAcct', OesQryInvAcctReqT),  # 查询证券账户请求
        ('qryComms', OesQryCommissionRateReqT),  # 查询客户佣金信息请求
        ('qryFundTrsf', OesQryFundTransferSerialReqT),  # 查询出入金信息请求
        ('qryLotWinning', OesQryLotWinningReqT),  # 查询新股配号、中签信息请求
        ('qryIssue', OesQryIssueReqT),  # 查询证券发行信息请求
        ('qryStock', OesQryStockReqT),  # 查询现货产品信息请求
        ('qryEtf', OesQryEtfReqT),  # 查询ETF申赎产品信息请求
        ('qryEtfComponent', OesQryEtfComponentReqT),  # 查询ETF基金成份证券信息请求
        ('qryMktState', OesQryMarketStateReqT),  # 查询市场状态信息请求
        ('qryCounterCash', OesQryCounterCashReqT),  # 查询主柜资金信息请求
    ]


# 统一的查询应答消息定义
class OesQryRspMsgT(PrintableUnion):
    _fields_ = [
        ('ordRsp', OesQryOrdRspT),  # 查询委托信息应答
        ('trdRsp', OesQryTrdRspT),  # 查询成交信息应答
        ('cashAssetRsp', OesQryCashAssetRspT),  # 查询客户资金信息应答
        ('stkHoldingRsp', OesQryStkHoldingRspT),  # 查询股票持仓信息应答
        ('custRsp', OesQryCustRspT),  # 查询客户信息应答W
        ('invAcctRsp', OesQryInvAcctRspT),  # 查询证券账户应答
        ('commsRateRsp', OesQryCommissionRateRspT),  # 查询客户佣金信息应答
        ('fundTrsfRsp', OesQryFundTransferSerialRspT),  # 查询出入金流水信息应答
        ('lotWinningRsp', OesQryLotWinningRspT),  # 查询新股配号、中签信息应答
        ('issueRsp', OesQryIssueRspT),  # 查询证券发行信息应答
        ('stockRsp', OesQryStockRspT),  # 查询现货产品信息应答
        ('etfRsp', OesQryEtfRspT),  # 查询ETF申赎产品信息应答
        ('etfComponentRsp', OesQryEtfComponentRspT),  # 查询ETF基金成份证券信息应答
        ('tradingDay', OesQryTradingDayRspT),  # 查询当前交易日信息应答
        ('mktStateRsp', OesQryMarketStateRspT),  # 查询市场状态信息应答
        ('clientOverview', OesClientOverviewT),  # 客户端总览信息
        ('counterCashRsp', OesQryCounterCashRspT),  # 客户主柜资金信息
        ('brokerParamsRsp', OesQryBrokerParamsInfoRspT),  # 查询券商参数信息应答
        ('applUpgradeRsp', OesQryApplUpgradeInfoRspT),  # 周边应用升级信息
    ]


# 回报同步请求消息
class OesReportSynchronizationReqT(PrintableStructure):
    _fields_ = [
        # 客户端最后接收到的回报数据的回报编号
        # - 等于0, 从头开始推送回报数据
        # - 大于0, 从指定的回报编号开始推送回报数据
        # - 小于0, 从最新的数据开始推送回报数据
        ('lastRptSeqNum', c_int64),
        # 待订阅的客户端环境号
        # - 大于0, 区分环境号, 仅订阅环境号对应的回报数据
        # - 小于等于0, 不区分环境号, 订阅该客户下的所有回报数据
        ('subscribeEnvId', c_int8),
        # 按64位对齐的填充域
        ('__filler', c_uint8 * 3),
        # 待订阅的回报消息种类
        # - 0:      默认回报 (等价于: 0x01,0x02,0x04,0x08,0x10,0x20,0x40)
        # - 0x0001: OES业务拒绝 (未通过风控检查等)
        # - 0x0002: OES委托已生成 (已通过风控检查)
        # - 0x0004: 交易所委托回报 (包括交易所委托拒绝、委托确认和撤单完成通知)
        # - 0x0008: 交易所成交回报
        # - 0x0010: 出入金委托执行报告 (包括出入金委托拒绝、出入金委托回报)
        # - 0x0020: 资金变动信息
        # - 0x0040: 持仓变动信息
        # - 0x0080: 市场状态信息
        # - 0xFFFF: 所有回报
        # @see eOesSubscribeReportTypeT
        ('subscribeRptTypes', c_int32),
    ]


# 回报同步应答消息
class OesReportSynchronizationRspT(PrintableStructure):
    _fields_ = [
        # 服务端最后已发送或已忽略的回报数据的回报编号
        ('lastRptSeqNum', c_int64),
        # 待订阅的客户端环境号
        # - 大于0, 区分环境号, 仅订阅环境号对应的回报数据
        # - 小于等于0, 不区分环境号, 订阅该客户下的所有回报数据
        ('subscribeEnvId', c_int8),
        # 按64位对齐的填充域
        ('__filler', c_uint8 * 3),
        # 已订阅的回报消息种类
        ('subscribeRptTypes', c_int32),
    ]


# 测试请求报文
class OesTestRequestReqT(PrintableStructure):
    _fields_ = [
        # 测试请求标识符
        ('testReqId', c_char * OES_MAX_TEST_REQ_ID_LEN),
        # 发送时间 (timeval结构或形如'YYYYMMDD-HH:mm:SS.sss'的字符串)
        ('sendTime', c_char * OES_MAX_SENDING_TIME_LEN),
        # 按64位对齐的填充域
        ('__filler', c_char * 2),
    ]


# 测试请求的应答报文
class OesTestRequestRspT(PrintableStructure):
    _fields_ = [
        # 测试请求标识符
        ('testReqId', c_char * OES_MAX_TEST_REQ_ID_LEN),
        # 测试请求的原始发送时间 (timeval结构或形如'YYYYMMDD-HH:mm:SS.sss'的字符串)
        ('origSendTime', c_char * OES_MAX_SENDING_TIME_LEN),
        # 按64位对齐的填充域
        ('__filler1', c_char * 2),
        # 测试请求应答的发送时间 (timeval结构或形如'YYYYMMDD-HH:mm:SS.sss'的字符串)
        ('respTime', c_char * OES_MAX_SENDING_TIME_LEN),
        # 按64位对齐的填充域
        ('__filler2', c_char * 2),
        # 消息实际接收时间 (开始解码等处理之前的时间)
        ('__recvTime', STimespec32T),
        # 消息采集处理完成时间
        ('__collectedTime', STimespec32T),
        # 消息推送时间 (写入推送缓存以后, 实际网络发送之前)
        ('__pushingTime', STimespec32T),
    ]


# 修改密码请求报文
class OesChangePasswordReqT(PrintableStructure):
    _fields_ = [
        # 加密方法
        ('encryptMethod', c_int32),
        # 按64位对齐的填充域
        ('__filler', c_int32),
        # 登录用户名
        ('username', c_char * OES_CLIENT_NAME_MAX_LEN),
        # 用户私有信息 (由客户端自定义填充, 并在回报数据中原样返回)
        ('userInfo', userInfo),
        # 之前的登录密码
        ('oldPassword', c_char * OES_PWD_MAX_LEN),
        # 新的登录密码
        ('newPassword', c_char * OES_PWD_MAX_LEN),
    ]


# 修改密码应答报文
class OesChangePasswordRspT(PrintableStructure):
    _fields_ = [
        # 加密方法
        ('encryptMethod', c_int32),
        # 按64位对齐的填充域
        ('__filler', c_int32),
        # 登录用户名
        ('username', c_char * OES_CLIENT_NAME_MAX_LEN),
        # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
        ('userInfo', userInfo),
        # 客户端编号
        ('clientId', c_int16),
        # 客户端环境号
        ('clEnvId', c_int8),
        # 按64位对齐的填充域
        ('__filler2', c_int8),
        # 发生日期 (格式为 YYYYMMDD, 形如 20160830)
        ('transDate', c_int32),
        # 发生时间 (格式为 HHMMSSsss, 形如 141205000)
        ('transTime', c_int32),
        # 拒绝原因
        ('rejReason', c_int32),
    ]


# 批量委托请求的消息头
class OesBatchOrdersHeadT(PrintableStructure):
    _fields_ = [
        # 本批次的委托请求数量
        ('itemCount', c_int32),
        # 按64位对齐的填充域
        ('__filler', c_int32),
    ]


# 批量委托请求的完整请求报文
# (只有请求报文, 没有独立的应答报文)
class OesBatchOrdersReqT(PrintableStructure):
    _fields_ = [
        # 批量委托请求的批次消息头
        ('batchHead', OesBatchOrdersHeadT),
        # 委托请求列表
        ('items', OesOrdReqT * 1),
    ]


# 回报消息的消息头定义
class OesRptMsgHeadT(PrintableStructure):
    _fields_ = [
        ('rptSeqNum', c_int64),  # 回报消息的编号
        ('rptMsgType', c_uint8),  # 回报消息的消息代码 @see eOesMsgTypeT
        ('execType', c_uint8),  # 执行类型 @see eOesExecTypeT
        ('bodyLength', c_int16),  # 回报消息的消息体大小
        ('ordRejReason', c_int32),  # 订单/撤单被拒绝原因
    ]


# 回报消息的消息体定义
class OesRptMsgBodyT(PrintableUnion):
    _fields_ = [
        ('ordInsertRsp', OesOrdCnfmT),  # OES委托响应-委托已生成
        ('ordRejectRsp', OesOrdRejectT),  # OES委托响应-业务拒绝
        ('ordCnfm', OesOrdCnfmT),  # 交易所委托回报
        ('trdCnfm', OesTrdCnfmT),  # 交易所成交回报
        ('fundTrsfRejectRsp', OesFundTrsfRejectT),  # 出入金委托拒绝
        ('fundTrsfCnfm', OesFundTrsfReportT),  # 出入金执行报告
        ('cashAssetRpt', OesCashAssetItemT),  # 资金变动信息
        ('stkHoldingRpt', OesStkHoldingItemT),  # 持仓变动信息 (股票)
    ]


# 完整的回报消息定义
class OesRptMsgT(PrintableStructure):
    _fields_ = [
        ('rptHead', OesRptMsgHeadT),  # 回报消息的消息头
        ('rptBody', OesRptMsgBodyT),  # 回报消息的消息体
    ]


# 汇总的请求消息的消息体定义
class OesReqMsgBodyT(PrintableUnion):
    _fields_ = [
        # 委托申报请求报文
        ('ordReq', OesOrdReqT),
        # 撤单请求请求报文
        ('ordCancelReq', OesOrdCancelReqT),
        # 批量委托请求报文
        ('batchOrdersReq', OesBatchOrdersReqT),
        # 出入金请求报文
        ('fundTrsfReq', OesFundTrsfReqT),
        # 修改密码请求报文
        ('changePasswordReq', OesChangePasswordReqT),
        # 测试请求报文
        ('testRequestReq', OesTestRequestReqT),
        # 回报同步请求报文
        ('rptSyncReq', OesReportSynchronizationReqT),
    ]


# 汇总的应答消息的消息体定义
class OesRspMsgBodyT(PrintableUnion):
    _fields_ = [
        # 执行报告回报消息
        ('rptMsg', OesRptMsgT),
        # 市场状态消息
        ('mktStateRpt', OesMarketStateInfoT),
        # 测试请求的应答报文
        ('testRequestRsp', OesTestRequestRspT),
        # 回报同步应答报文
        ('reportSynchronizationRsp', OesReportSynchronizationRspT),
        # 修改密码应答报文
        ('changePasswordRsp', OesChangePasswordRspT),
    ]


# 通用消息头
# @see eSMsgFlagT
class SMsgHeadT(PrintableStructure):
    _fields_ = [
        ('msgFlag', c_uint8),  # 消息标志 @see eSMsgFlagT
        ('msgId', c_uint8),  # 消息代码
        ('status', c_uint8),  # 状态码
        ('detailStatus', c_uint8),  # 明细状态代码 (@note 当消息为嵌套的组合消息时, 复用该字段记录消息体中的消息条数)
        ('msgSize', c_int32),  # 消息大小
    ]


class _SocketDescriptor(PrintableUnion):
    _fields_ = [
        # Socket描述符
        ('socketFd', c_int32),
        # 按64位对齐的填充域
        ('__socket_fd_filler', c_uint64),
    ]


# 支持动态内存分配的数据缓存的结构体别名 (为了消除某些情况下的编译警告)
class _SDataBufferVar(PrintableStructure):
    _fields_ = [
        ('dataSize', c_int32),  # 有效数据长度
        ('bufSize', c_int32),  # 缓存区总大小
        ('buffer', c_char_p),  # 缓存区指针
        ('__ref', c_void_p),  # 反向引用指针
    ]


STimespecT = c_char * TIMESPEC_SIZE


# Socket 连接通道信息
class SSocketChannelInfoT(PrintableStructure):
    _fields_ = [
        ('socketDescriptor', _SocketDescriptor),
        # 套接字端口号
        ('remotePort', c_int32),
        # 整数类型的对端IP地址 (网络字节序)
        ('origRemoteIp', c_uint32),
        # 通信协议类型
        # @see eSSocketProtocolTypeT
        ('protocolType', c_uint8),
        # 是否使用网络字节序 (TRUE 网络字节序；FALSE 本机字节序)
        ('_isNetByteOrder', c_uint8),
        # 连接是否已破裂 (用于内部处理)
        ('_isBroken', c_uint8),
        # 标示异步发送线程的连接是否已破裂 (用于内部处理)
        ('_isSendBroken', c_uint8),
        # 标识是否正在尝试连接的过程中 (用于内部处理)
        ('_isTryConnecting', c_uint8),
        # 按64位对齐的填充域
        ('__filler', c_uint8 * 3),
        # 连接建立时间 (UTC时间, 即相对于1970年的秒数)
        ('connectTime', c_int64),
        # 套接字地址或DomainSocket的路径地址 (仅用于显示)
        ('remoteAddr', c_char * SPK_MAX_URI_LEN),
    ]


class _reserveData(PrintableUnion):
    _fields_ = [
        ('buf', c_char * GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE),
        ('i8', c_int8 * GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE),
        ('u8', c_uint8 * GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE),
        ('i16', c_int16 * int(GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE / 2)),
        ('u16', c_uint16 * int(GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE / 2)),
        ('i32', c_int32 * int(GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE / 4)),
        ('u32', c_uint32 * int(GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE / 4)),
        ('i64', c_int64 * int(GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE / 8)),
        ('u64', c_uint64 * int(GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE / 8)),
        ('ptr', c_void_p * int(GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE / 8)),
        ('__padding', c_char * (GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE + SPK_CACHE_LINE_SIZE)),
    ]


class _extData(PrintableUnion):
    _fields_ = [
        ('buf', c_char * GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE),
        ('i8', c_int8 * GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE),
        ('u8', c_uint8 * GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE),
        ('i16', c_int16 * int(GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE / 2)),
        ('u16', c_uint16 * int(GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE / 2)),
        ('i32', c_int32 * int(GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE / 4)),
        ('u32', c_uint32 * int(GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE / 4)),
        ('i64', c_int64 * int(GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE / 8)),
        ('u64', c_uint64 * int(GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE / 8)),
        ('ptr', c_void_p * int(GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE / 8)),
    ]


# 通用的客户端会话信息（连接通道信息）定义
class SGeneralClientChannelT(PrintableStructure):
    _fields_ = [
        ('socketDescriptor', _SocketDescriptor),
        ('heartBtInt', c_int32),  # 心跳间隔, 单位为秒 (允许预先赋值)
        ('testReqInt', c_int32),  # 测试请求间隔, 单位为秒
        ('protocolType', c_uint8),  # 协议类型 (Binary, JSON等) (允许预先赋值)
        ('remoteSetNum', c_uint8),  # 对端服务器的集群号
        ('remoteHostNum', c_uint8),  # 已连接上的对端服务器的主机编号
        ('remoteIsLeader', c_uint8),  # 对端服务器是否是'主节点'
        ('leaderHostNum', c_uint8),  # '主节点'的主机编号
        ('__filler1', c_uint8 * 3),  # 按64位对齐填充域
        ('__codecBuf', _SDataBufferVar),  # 编解码缓存
        ('__recvBuf', _SDataBufferVar),  # 接收缓存
        ('__pDataStartPoint', c_char_p),  # 数据起始位置指针
        ('__contextPtr', c_void_p),  # 保留给内部使用的上下文环境指针
        ('__monitorPtr', c_void_p),  # 保留给内部使用的监控信息指针
        ('__customPtr', c_void_p),  # 可以由应用层自定义使用的指针变量
        ('__reavedSize', c_int32),  # 已接收到但尚未处理的数据长度
        ('__customFlag', c_int32),  # 可以由应用层自定义使用的整型变量
        # 累计接收到的未压缩数据大小
        ('__totalInMsgSize', c_int64),
        # 累计接收到的已压缩数据大小
        ('__totalCompressedSize', c_int64),
        # 解压缩后的数据总大小
        ('__totalDecompressSize', c_int64),
        ('firstInMsgSeq', c_uint64),  # 已接收到的起始入向消息序号
        ('lastInMsgSeq', c_uint64),  # 实际已接收到的入向消息序号 (对应于登录应答消息的 lastOutMsgSeq)
        ('nextInMsgSeq', c_uint64),  # 期望的入向消息序号
        ('lastRecvTime', STimespecT),  # 接收时间
        ('channel', SSocketChannelInfoT),  # 连接通道信息
        ('nextOutMsgSeq', c_uint64),  # 出向消息序号
        ('lastOutMsgSeq', c_uint64),  # 实际已发送的出向消息序号 (对应于登录应答消息的 lastInMsgSeq)
        ('lastSendTime', STimespecT),  # 发送时间
        # 发送方代码
        ('senderCompId', c_char * GENERAL_CLI_MAX_COMP_ID_LEN),
        # 接收方代码
        ('targetCompId', c_char * GENERAL_CLI_MAX_COMP_ID_LEN),
        ('__magicNumber', c_int32),  # 标识会话结构是否已经正确初始化过
        ('__clientId', c_int32),  # 客户端编号
        ('__channelType', c_uint8),  # 通道类型
        ('__clEnvId', c_int8),  # 客户端环境号
        ('__groupFlag', c_uint8),  # 通道组标志
        ('__protocolHints', c_uint8),  # 协议约定信息
        ('__businessType', c_uint8),  # 通道对应的业务类型
        ('__lastConnectIdx', c_uint8),  # 最近一次连接的主机地址顺序号
        ('__filler', c_uint8 * 2),  # 按64位对齐填充域
        # 保留给服务器或API内部使用的, 用于存储自定义数据的扩展空间
        ('__reserveData', _reserveData),
        # 可以由应用层自定义使用的, 用于存储自定义数据的扩展空间
        ('__extData', _extData),
    ]


# 通用的连接通道组定义（多个连接通道的集合）
class SGeneralClientChannelGroupT(PrintableStructure):
    _fields_ = [
        # 连接通道数量
        ('channelCount', c_int32),
        # 可以由应用层自定义使用的整型变量
        ('__customFlag', c_int32),
        # 连接通道信息列表
        ('channelList', POINTER(SGeneralClientChannelT) * GENERAL_CLI_MAX_CHANNEL_GROUP_SIZE),
        # 最大的连接描述符 (仅供系统内部使用)
        ('__maxFd', c_int32),
        # 最大的连接描述符集合大小 (仅供系统内部使用)
        ('__maxFdCnt', c_int16),
        # 通道组标志 (仅供系统内部使用)
        ('__groupFlag', c_uint8),
        # 按64位对齐的填充域
        ('__filler', c_uint8),
        # 连接描述符集合 (仅供系统内部使用)
        ('__connect_descriptor_set', c_char * CONNECT_DESCRIPTOR_SET_SIZE),
        # union {
        # ('__fdArray', SPollfdT * GENERAL_CLI_MAX_CHANNEL_GROUP_SIZE),
        # ('__fdSet', fd_set),
        # };
    ]


# Socket URI地址信息
class SGeneralClientAddrInfoT(PrintableStructure):
    _fields_ = [
        # 地址信息
        ('uri', c_char * SPK_MAX_URI_LEN),
        # 接收方代码
        ('targetCompId', c_char * GENERAL_CLI_MAX_COMP_ID_LEN),
        # 用户名
        ('username', c_char * GENERAL_CLI_MAX_NAME_LEN),
        # 密码
        ('password', c_char * GENERAL_CLI_MAX_PWD_LEN),
        # 主机编号
        ('hostNum', c_uint8),
        # 按64位对齐的填充域
        ('__filler', c_uint8 * 7),
    ]


# 套接口选项配置
class SSocketOptionConfigT(PrintableStructure):
    _fields_ = [
        # socket SO_RCVBUF size (KB)
        ('soRcvbuf', c_int32),
        # socket SO_SNDBUF size (KB)
        ('soSndbuf', c_int32),
        # socket TCP_NODELAY option, 0 or 1
        ('tcpNodelay', c_int8),
        # socket TCP_QUICKACK option, 0 or 1
        ('quickAck', c_int8),
        # mutilcast TTL number
        ('mcastTtlNum', c_int8),
        # disable mutilcast loopback, 0 or 1
        ('mcastLoopbackDisabled', c_int8),
        # BACKLOG size for listen
        ('soBacklog', c_uint16),
        # 连接操作(connect)的超时时间 (毫秒)
        ('connTimeoutMs', c_uint16),
        # socket TCP_KEEPIDLE option, 超时时间(秒)
        ('keepIdle', c_int16),
        # socket TCP_KEEPINTVL option, 间隔时间(秒)
        ('keepIntvl', c_int16),
        # socket SO_KEEPALIVE option, 0 or 1
        ('keepalive', c_int8),
        # socket TCP_KEEPCNT option, 尝试次数
        ('keepCnt', c_int8),
        # 按64位对齐的填充域
        ('__filler', c_int8 * 6),
        # 本地绑定的端口地址 (适用于发送端)
        ('localSendingPort', c_int32),
        # 本地绑定的网络设备接口的IP地址 (适用于发送端)
        ('localSendingIp', c_char * (SPK_MAX_IP_LEN + 4)),
        # 用于组播接收和发送的特定网络设备接口的IP地址
        ('mcastInterfaceIp', c_char * (SPK_MAX_IP_LEN + 4)),
    ]


# 远程主机配置信息
class SGeneralClientRemoteCfgT(PrintableStructure):
    _fields_ = [
        ('addrCnt', c_int32),  # 服务器地址的数量
        ('heartBtInt', c_int32),  # 心跳间隔,单位为秒
        ('clusterType', c_uint8),  # 服务器集群的集群类型 (0:默认, 1:复制集, 2:对等节点)
        ('clEnvId', c_int8),  # 客户端环境号
        ('targetSetNum', c_uint8),  # 远程主机的集群号
        ('businessType', c_uint8),  # 期望对接的业务类型
        ('__filler', c_uint8 * 4),  # 按64位对齐的填充域
        # 发送方代码
        ('senderCompId', c_char * GENERAL_CLI_MAX_COMP_ID_LEN),
        # 接收方代码
        ('targetCompId', c_char * GENERAL_CLI_MAX_COMP_ID_LEN),
        # 用户名
        ('username', c_char * GENERAL_CLI_MAX_NAME_LEN),
        # 密码
        ('password', c_char * GENERAL_CLI_MAX_PWD_LEN),
        # 服务器地址列表
        ('addrList', SGeneralClientAddrInfoT * GENERAL_CLI_MAX_REMOTE_CNT),
        # 套接口选项配置
        ('socketOpt', SSocketOptionConfigT),
    ]


# 主机地址列表的游标信息
class SGeneralClientAddrCursorT(PrintableStructure):
    _fields_ = [
        ('addrCnt', c_int32),  # 服务器地址的数量
        ('lastConnectIdx', c_int32),  # 最近一次连接的主机地址顺序号
        ('lastConnectResult', c_int32),  # 最近一次连接的连接结果
        ('lastHostNum', c_uint8),  # 最近一次连接的主机编号
        ('isLast', c_uint8),  # 是否遍历完成
        ('__filler1', c_uint8 * 2),  # 按64位对齐的填充域
        ('socketDescriptor', _SocketDescriptor),
        ('pLastAddrInfo', POINTER(SGeneralClientAddrInfoT)),  # 最近一次连接的主机地址信息
        ('__filler2', c_void_p),  # 按64位对齐的填充域
    ]


# 通信接口错误信息结构体定义
class SErrMsgT(PrintableStructure):
    _fields_ = [
        ('__index', c_int16),  # 序号, 为方便识别而设
        ('MODULE', c_uint8),  # 模块代码 (取值范围: 0~99)
        ('CODE', c_uint8),  # 明细错误号 (取值范围: 0~99)
        ('__errCode', c_uint16),  # 合并后的错误编号 (自动计算)
        ('__msgSize', c_int16),  # 错误信息长度 (自动计算)
        # 错误信息
        ('MSG', c_char * SPK_MAX_ERRMSG_LEN),
    ]


# 客户端会话信息 (连接通道信息) 定义
OesApiSessionInfoT = SGeneralClientChannelT
# 客户端会话的连接通道组定义 (多个连接通道的集合)
OesApiChannelGroupT = SGeneralClientChannelGroupT
# Socket URI地址信息
OesApiAddrInfoT = SGeneralClientAddrInfoT
# 远程主机配置信息
OesApiRemoteCfgT = SGeneralClientRemoteCfgT
# 主机地址列表的游标信息
OesApiAddrCursorT = SGeneralClientAddrCursorT


# 回报订阅的订阅参数信息
class OesApiSubscribeInfoT(PrintableStructure):
    _fields_ = [
        # 待订阅的客户端环境号
        # - 大于0, 区分环境号, 仅订阅环境号对应的回报数据
        # - 小于等于0, 不区分环境号, 订阅该客户下的所有回报数据
        ('clEnvId', c_int8),
        # 按64位对齐的填充域
        ('__filler', c_uint8 * 3),
        # 待订阅的回报消息种类
        # - 0:      默认回报 (等价于: 0x01,0x02,0x04,0x08,0x10,0x20,0x40)
        # - 0x0001: OES业务拒绝 (未通过风控检查等)
        # - 0x0002: OES委托已生成 (已通过风控检查)
        # - 0x0004: 交易所委托回报 (包括交易所委托拒绝、委托确认和撤单完成通知)
        # - 0x0008: 交易所成交回报
        # - 0x0010: 出入金委托执行报告 (包括出入金委托拒绝、出入金委托回报)
        # - 0x0020: 资金变动信息
        # - 0x0040: 持仓变动信息
        # - 0x0080: 市场状态信息
        # - 0xFFFF: 所有回报
        # @see eOesSubscribeReportTypeT
        ('rptTypes', c_int32),
    ]


# 完整的OES客户端配置信息
class OesApiClientCfgT(PrintableStructure):
    _fields_ = [
        ('ordChannelCfg', OesApiRemoteCfgT),  # 委托服务配置
        ('rptChannelCfg', OesApiRemoteCfgT),  # 回报服务配置
        ('qryChannelCfg', OesApiRemoteCfgT),  # 查询服务配置
        ('subscribeInfo', OesApiSubscribeInfoT),  # 回报订阅参数
    ]


# OES客户端运行时环境
class OesApiClientEnvT(PrintableStructure):
    _fields_ = [
        ('ordChannel', OesApiSessionInfoT),  # 委托通道的会话信息
        ('rptChannel', OesApiSessionInfoT),  # 回报通道的会话信息
        ('qryChannel', OesApiSessionInfoT),  # 查询通道的会话信息
    ]
