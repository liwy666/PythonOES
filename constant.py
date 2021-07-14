# -*- coding: utf-8 -*-
from enum import Enum
from ctypes import c_char
from ctypes import c_char_p
from ctypes import c_void_p

from ctypes import c_int8
from ctypes import c_uint8
from ctypes import c_int16
from ctypes import c_uint16
from ctypes import c_int32
from ctypes import c_uint32
from ctypes import c_int64
from ctypes import c_uint64
from ctypes import Union
from ctypes import Structure
from ctypes import POINTER

OES_CLIENT_NAME_MAX_LEN = 32
OES_CLIENT_DESC_MAX_LEN = 32
OES_CLIENT_TAG_MAX_LEN = 32
OES_PWD_MAX_LEN = 40
OES_VER_ID_MAX_LEN = 32
OES_MAX_COMP_ID_LEN = 32
OES_MAX_CLIENT_ENVID_COUNT = 128
OES_MAX_BATCH_ORDERS_COUNT = 500
OES_CUST_ID_MAX_LEN = 16
OES_CUST_ID_REAL_LEN = 12
OES_CUST_NAME_MAX_LEN = 64
OES_CASH_ACCT_ID_MAX_LEN = 16
OES_CASH_ACCT_ID_REAL_LEN = 12
OES_INV_ACCT_ID_MAX_LEN = 16
OES_INV_ACCT_ID_REAL_LEN = 10
OES_BRANCH_ID_MAX_LEN = 8
OES_BRANCH_ID_REAL_LEN = 6
OES_BANK_NO_MAX_LEN = 8
OES_BANK_NO_REAL_LEN = 4
OES_PBU_MAX_LEN = 8
OES_PBU_REAL_LEN = 6
OES_SECURITY_ID_MAX_LEN = 16
OES_STOCK_ID_REAL_LEN = 6
OES_OPTION_ID_REAL_LEN = 8

OES_SECURITY_NAME_MAX_LEN = 24
OES_SECURITY_NAME_REAL_LEN = 20
OES_SECURITY_LONG_NAME_MAX_LEN = 80
OES_SECURITY_ENGLISH_NAME_MAX_LEN = 48
OES_SECURITY_ISIN_CODE_MAX_LEN = 16


OES_MAX_IP_LEN = 16
OES_MAX_MAC_LEN = 20
OES_MAX_MAC_ALGIN_LEN = 24
OES_MAX_DRIVER_ID_LEN = 21
OES_MAX_DRIVER_ID_ALGIN_LEN = 24


OES_MAX_ERROR_INFO_LEN = 64
OES_MAX_ALLOT_SERIALNO_LEN = 64
OES_FEE_RATE_UNIT = 10000000
OES_ETF_CASH_RATIO_UNIT = 100000
OES_CASH_UNIT = 10000
OES_FUND_TRSF_UNIT = 100
OES_BOND_INTEREST_UNIT = 100000000

OES_STK_POSITION_LIMIT_UNIT = 1000000
OES_AUCTION_UP_DOWN_RATE_UNIT = 100
OES_MAX_BS_PRICE = OES_CASH_UNIT * 10000


OES_APPL_VER_ID = '0.15.11.3'
OES_APPL_VER_VALUE = 1001511031
OES_MIN_APPL_VER_ID = '0.15.5'
OES_APPL_NAME = "OES"
OES_MAX_ORD_ITEM_CNT_PER_PACK = 30
OES_MAX_TRD_ITEM_CNT_PER_PACK = 30
OES_MAX_CASH_ASSET_ITEM_CNT_PER_PACK = 30
OES_MAX_HOLDING_ITEM_CNT_PER_PACK = 30
OES_MAX_CUST_ITEM_CNT_PER_PACK = 30
OES_MAX_INV_ACCT_ITEM_CNT_PER_PACK = 30
OES_MAX_COMMS_RATE_ITEM_CNT_PER_PACK = 50
OES_MAX_FUND_TRSF_ITEM_CNT_PER_PACK = 30
OES_MAX_LOG_WINNING_ITEM_CNT_PER_PACK = 30
OES_MAX_ISSUE_ITEM_CNT_PER_PACK = 30
OES_MAX_STOCK_ITEM_CNT_PER_PACK = 30
OES_MAX_ETF_ITEM_CNT_PER_PACK = 30
OES_MAX_ETF_COMPONENT_ITEM_CNT_PER_PACK = 30
OES_MAX_OPTION_ITEM_CNT_PER_PACK = 30
OES_TRD_SESS_TYPE_MAX = 3
SPK_MAX_IP_LEN = 16
OES_EXCH_ORDER_ID_MAX_LEN = 17
OES_EXCH_ORDER_ID_SSE_LEN = 8
OES_EXCH_ORDER_ID_SZSE_LEN = 16
SPK_MAX_MAC_ALGIN_LEN = 24


GENERAL_CLI_MAX_COMP_ID_LEN = 32
GENERAL_CLI_MAX_SESSION_EXTDATA_SIZE = 128
SPK_MAX_URI_LEN = 128
SPK_CACHE_LINE_SIZE = 64

OES_CAST_ID_MAX_LEN = 16
OES_MAX_TEST_REQ_ID_LEN = 32
OES_MAX_SENDING_TIME_LEN = 22
OES_REAL_SENDING_TIME_LEN = 21


OES_BROKER_NAME_MAX_LEN = 128     # 券商名称最大长度
OES_BROKER_PHONE_MAX_LEN = 32     # 券商联系电话最大长度


OES_MAX_MKT_STATE_ITEM_CNT_PER_PACK = 30


OES_BROKER_WEBSITE_MAX_LEN = 256
OES_APPL_DISCARD_VERSION_MAX_COUNT = 5
OES_APPL_UPGRADE_PROTOCOL_MAX_LEN = 32
OES_MAX_VERSION_LEN = 32
OES_MAX_CUST_PER_CLIENT = 1

SPK_MAX_PATH_LEN = 256
GENERAL_CLI_MAX_NAME_LEN = 32
GENERAL_CLI_MAX_PWD_LEN = 40
GENERAL_CLI_MAX_REMOTE_CNT = 8

# 不同平台时间戳字段长度不同
import sys

DIFF_SYS_TIME_STAMP_LEN = 2
if sys.platform == 'win32':
    DIFF_SYS_TIME_STAMP_LEN = 1


class SimpleStructure(Structure):
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


class SimpleUnion(Union):
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


class Head(SimpleStructure):
    """
    消息头定义.
    """
    _fields_ = [('msg_flag', c_uint8),  # 消息标志
                ('msg_id', c_uint8),  # 消息代码
                ('status', c_uint8),  # 状态码
                ('detail_status', c_uint8),  # 明细状态代码
                ('msg_size', c_int32)]  # 消息大小


class OesApiChannelType(Enum):
    OESAPI_CHANNEL_TYPE_ORDER = 1  # 委托申报通道
    OESAPI_CHANNEL_TYPE_REPORT = 2  # 回报通道
    OESAPI_CHANNEL_TYPE_QUERY = 3  # 查询通道


class OesCurrType(Enum):
    OES_CURR_TYPE_RMB = 0  # 人民币
    OES_CURR_TYPE_HKD = 1  # 港币
    OES_CURR_TYPE_USD = 2  # 美元
    _OES_CURR_TYPE_MAX = OES_CURR_TYPE_USD + 1  # 货币种类最大值


class OesExchangeId(Enum):
    OES_EXCH_UNDEFINE = 0  # 未定义的交易所代码
    OES_EXCH_SSE = 1  # 上海证券交易所
    OES_EXCH_SZSE = 2  # 深圳证券交易所
    _MAX_OES_EXCH = 3
    OES_EXCHANGE_TYPE_SSE = OES_EXCH_SSE  # 上海证券交易所 @depricated 已过时, 请使用 OES_EXCH_SSE
    OES_EXCHANGE_TYPE_SZS = OES_EXCH_SZSE  # 深圳证券交易所 @depricated 已过时, 请使用 OES_EXCH_SZSE
    _OES_EXCH_ID_MAX_ALIGNED4 = 4  # 交易所代码最大值 (按4字节对齐的大小)
    _OES_EXCH_ID_MAX_ALIGNED8 = 8  # 交易所代码最大值 (按8字节对齐的大小)


class OesEtfSubFlag(Enum):
    OES_ETF_SUBFLAG_FORBID_SUB = 0  # 禁止现金替代(必须有证券)
    OES_ETF_SUBFLAG_MUST_SUB = 2  # 必须用现金替代
    OES_ETF_SUBFLAG_ALLOW_SUB = 1  # 可以进行现金替代(先用证券,如证券不足可用现金替代)
    OES_ETF_SUBFLAG_SZ_REFUND_SUB = 3  # 该证券为深市证券, 退补现金替代
    OES_ETF_SUBFLAG_SZ_MUST_SUB = 4  # 该证券为深市证券, 必须现金替代
    OES_ETF_SUBFLAG_OTHER_REFUND_SUB = 5  # 非沪深市场成分证券退补现金替代
    OES_ETF_SUBFLAG_OTHER_MUST_SUB = 6  # 非沪深市场成份证券必须现金替代
    OES_ETF_SUBFLAG_HK_REFUND_SUB = 7  # 港市退补现金替代 (仅适用于跨沪深港ETF产品)
    OES_ETF_SUBFLAG_HK_MUST_SUB = 8  # 港市必须现金替代 (仅适用于跨沪深港ETF产品)


class OesMarketId(Enum):
    OES_MKT_UNDEFINE = 0  # 未定义的市场类型
    OES_MKT_SH_ASHARE = 1  # 上海A股
    OES_MKT_SZ_ASHARE = 2  # 深圳A股
    OES_MKT_SH_OPTION = 3  # 上海期权
    OES_MKT_ID_MAX = OES_MKT_SH_OPTION + 1

    OES_MKT_ID_UNDEFINE = OES_MKT_UNDEFINE  # 未定义的市场类型 @depricated 已过时, 请使用 OES_MKT_UNDEFINE
    OES_MKT_ID_SH_A = OES_MKT_SH_ASHARE  # 上海A股 @depricated 已过时, 请使用 OES_MKT_SH_ASHARE
    OES_MKT_ID_SZ_A = OES_MKT_SZ_ASHARE  # 深圳A股 @depricated 已过时, 请使用 OES_MKT_SZ_ASHARE
    OES_MKT_ID_SH_OPT = OES_MKT_SH_OPTION  # 上海期权 @depricated 已过时, 请使用 OES_MKT_SH_OPTION


class OesPlatformId(Enum):
    """交易平台类型定义"""
    OES_PLATFORM_UNDEFINE = 0  # 未定义的交易平台类型
    OES_PLATFORM_CASH_AUCTION = 1  # 现货集中竞价交易平台
    OES_PLATFORM_FINANCIAL_SERVICES = 2  # 综合金融服务平台
    OES_PLATFORM_NON_TRADE = 3  # 非交易处理平台
    OES_PLATFORM_DERIVATIVE_AUCTION = 4  # 衍生品集中竞价交易平台
    _OES_PLATFORM_ID_MAX = OES_PLATFORM_DERIVATIVE_AUCTION + 1  # 平台号的最大值
    _OES_PLATFORM_ID_MAX_ALIGNED8 = 8  # 平台号的最大值 (按8字节对齐的大小)


class OesMarketState(Enum):
    """市场状态定义"""
    OES_MKT_STATE_UNDEFINE = 0  # 未定义的市场状态
    OES_MKT_STATE_PRE_OPEN = 1  # 未开放 (PreOpen)
    OES_MKT_STATE_OPEN_UP_COMING = 2  # 即将开放 (OpenUpComing)
    OES_MKT_STATE_OPEN = 3  # 开放 (Open)
    OES_MKT_STATE_HALT = 4  # 暂停开放 (Halt)
    OES_MKT_STATE_CLOSE = 5  # 关闭 (Close)
    _OES_MKT_STATE_MAX = OES_MKT_STATE_CLOSE + 1


class OesAcctType(Enum):
    OES_ACCT_TYPE_NORMAL = 0  # 普通账户
    OES_ACCT_TYPE_CREDIT = 1  # 信用账户
    OES_ACCT_TYPE_OPTION = 2  # 衍生品账户 * /
    OES_ACCT_TYPE_MAX = 3  # 账户类别最大值 * /


class OesCashType(Enum):
    OES_CASH_TYPE_SPOT = 0  # 普通账户资金 / 现货资金
    OES_CASH_TYPE_CREDIT = 1  # 信用账户资金 / 信用资金
    OES_CASH_TYPE_OPTION = 2  # 衍生品账户资金 / 期权保证金
    OES_CASH_TYPE_MAX = 3


class OesTrdSessType(Enum):
    OES_TRD_SESS_TYPE_O = 0  # 开盘集合竞价时段
    OES_TRD_SESS_TYPE_T = 1  # 连续竞价时段
    OES_TRD_SESS_TYPE_C = 2  # 收盘集合竞价
    OES_TRD_SESS_TYPE_MAX = 3  # 时段类型最大值


class OesSecurityType(Enum):
    OES_SECURITY_TYPE_UNDEFINE = 0  # 未定义的证券类型
    OES_SECURITY_TYPE_STOCK = 1  # 股票
    OES_SECURITY_TYPE_BOND = 2  # 债券
    OES_SECURITY_TYPE_ETF = 3  # ETF
    OES_SECURITY_TYPE_FUND = 4  # 基金
    OES_SECURITY_TYPE_OPTION = 5  # 期权
    OES_SECURITY_TYPE_MGR = 9  # 管理类
    # _OES_SECURITY_TYPE_MAX = 6  # 证券类型最大值
    # _OES_SECURITY_TYPE_NOT_SUPPORT = 100  # 不支持的证券类别


class OesProductType(Enum):
    OES_PRODUCT_TYPE_UNDEFINE = 0  # 未定义的产品类型 * /
    OES_PRODUCT_TYPE_EQUITY = 1  # 普通股票 / 存托凭证 / 债券 / 基金 * /
    OES_PRODUCT_TYPE_BOND_STD = 2  # 逆回购标准券 * /
    OES_PRODUCT_TYPE_IPO = 3  # 新股认购 * /
    OES_PRODUCT_TYPE_ALLOTMENT = 4  # 配股认购 * /
    OES_PRODUCT_TYPE_OPTION = 5  # 期权 * /

    _OES_PRODUCT_TYPE_MAX = OES_PRODUCT_TYPE_OPTION + 1  # 产品类型最大值 * /


class OesSubSecurityType(Enum):
    OES_SUB_SECURITY_TYPE_UNDEFINE = 0  # 未定义的证券子类型

    # _OES_SUB_SECURITY_TYPE_STOCK_MIN = 10  # 股票类证券子类型最小值
    OES_SUB_SECURITY_TYPE_STOCK_ASH = 11  # A股股票，A Share
    OES_SUB_SECURITY_TYPE_STOCK_SME = 12  # 中小板股票，Small & Medium Enterprise (SME) Board
    OES_SUB_SECURITY_TYPE_STOCK_GEM = 13  # 创业板股票，Growth Enterprise Market (GEM)
    OES_SUB_SECURITY_TYPE_STOCK_KSH = 14  # 科创板股票
    OES_SUB_SECURITY_TYPE_STOCK_KCDR = 15  # 科创板存托凭证
    OES_SUB_SECURITY_TYPE_STOCK_CDR = 16  # 存托凭证, Chinese Depository Receipt (CDR)
    OES_SUB_SECURITY_TYPE_STOCK_HLTCDR = 17  # 沪伦通CDR本地交易业务产品
    OES_SUB_SECURITY_TYPE_STOCK_GEMCDR = 18  # 创业板存托凭证
    # _OES_SUB_SECURITY_TYPE_STOCK_MAX = 15  # 股票类证券子类型最大值

    # _OES_SUB_SECURITY_TYPE_BOND_MIN = 20  # 债券类证券子类型最小值
    OES_SUB_SECURITY_TYPE_BOND_GBF = 21  # 国债
    OES_SUB_SECURITY_TYPE_BOND_CBF = 22  # 企业债
    OES_SUB_SECURITY_TYPE_BOND_CPF = 23  # 公司债
    OES_SUB_SECURITY_TYPE_BOND_CCF = 24  # 可转换债券
    OES_SUB_SECURITY_TYPE_BOND_FBF = 25  # 金融机构发行债券
    OES_SUB_SECURITY_TYPE_BOND_PRP = 26  # 债券质押式回购
    OES_SUB_SECURITY_TYPE_BOND_STD = 27  # 债券标准券
    OES_SUB_SECURITY_TYPE_BOND_EXG = 28  # 可交换债券
    # _OES_SUB_SECURITY_TYPE_BOND_MAX = 28  # 债券类证券子类型最大值

    # _OES_SUB_SECURITY_TYPE_ETF_MIN = 30  # ETF类证券子类型最小值
    OES_SUB_SECURITY_TYPE_ETF_SINGLE_MKT = 31  # 单市场股票ETF
    OES_SUB_SECURITY_TYPE_ETF_CROSS_MKT = 32  # 跨市场股票ETF
    OES_SUB_SECURITY_TYPE_ETF_BOND = 33  # 实物债券ETF
    OES_SUB_SECURITY_TYPE_ETF_CURRENCY = 34  # 货币ETF
    OES_SUB_SECURITY_TYPE_ETF_CROSS_BORDER = 35  # 跨境ETF
    OES_SUB_SECURITY_TYPE_ETF_GOLD = 36  # 黄金ETF
    OES_SUB_SECURITY_TYPE_ETF_COMMODITY_FUTURES = 37  # 商品期货ETF
    # _OES_SUB_SECURITY_TYPE_ETF_MAX = 37  # ETF类证券子类型最大值

    # _OES_SUB_SECURITY_TYPE_FUND_MIN = 40  # 基金类证券子类型最小值
    OES_SUB_SECURITY_TYPE_FUND_LOF = 41  # LOF基金
    OES_SUB_SECURITY_TYPE_FUND_CEF = 42  # 封闭式基金，Close-end Fund
    OES_SUB_SECURITY_TYPE_FUND_OEF = 43  # 开放式基金，Open-end Fund
    OES_SUB_SECURITY_TYPE_FUND_GRADED = 44  # 分级子基金
    # _OES_SUB_SECURITY_TYPE_FUND_MAX = 45  # 基金类证券子类型最大值

    # _OES_SUB_SECURITY_TYPE_OPTION_MIN = 50  # 期权类证券子类型最小值
    OES_SUB_SECURITY_TYPE_OPTION_STOCK = 52  # 个股期权
    OES_SUB_SECURITY_TYPE_OPTION_ETF = 51  # ETF期权
    # _OES_SUB_SECURITY_TYPE_OPTION_MAX = 53  # 期权类证券子类型最大值

    OES_SUB_SECURITY_TYPE_MGR_SSE_DESIGNATION = 91  # 指定登记
    OES_SUB_SECURITY_TYPE_MGR_SSE_RECALL_DESIGNATION = 92  # 指定撤消
    OES_SUB_SECURITY_TYPE_MGR_SZSE_DESIGNATION = 93  # 托管注册
    OES_SUB_SECURITY_TYPE_MGR_SZSE_CANCEL_DESIGNATION = 94  # 托管撤消


class OesSecurityLevel(Enum):
    OES_SECURITY_LEVEL_UNDEFINE = 0
    OES_SECURITY_LEVEL_N = 1  # 正常证券
    OES_SECURITY_LEVEL_XST = 2  # *ST股
    OES_SECURITY_LEVEL_ST = 3  # ST股
    OES_SECURITY_LEVEL_P = 4  # 退市整理证券
    OES_SECURITY_LEVEL_T = 5  # 退市转让证券
    OES_SECURITY_LEVEL_U = 6  # 优先股
    OES_SECURITY_LEVEL_B = 7  # B级基金


class OesSecurityRiskLevel(Enum):
    OES_RISK_LEVEL_VERY_LOW = 0  # 极低风险
    OES_RISK_LEVEL_LOW = 1  # 低风险
    OES_RISK_LEVEL_MEDIUM_LOW = 2  # 中低风险
    OES_RISK_LEVEL_MEDIUM = 3  # 中风险
    OES_RISK_LEVEL_MEDIUM_HIGH = 4  # 中高风险
    OES_RISK_LEVEL_HIGH = 5  # 高风险
    OES_RISK_LEVEL_VERY_HIGH = 6  # 极高风险
    # _OES_RISK_LEVEL_MAX = 7


class OesSecuritySuspFlag(Enum):
    OES_SUSPFLAG_NONE = 0x0  # 无停牌标识
    OES_SUSPFLAG_EXCHANGE = 0x1  # 交易所连续停牌
    OES_SUSPFLAG_BROKER = 0x2  # 券商人工停牌


class OesSecurityStatus(Enum):
    OES_SECURITY_STATUS_NONE = 0  # 无特殊状态
    OES_SECURITY_STATUS_FIRST_LISTING = (1 << 0)  # 上市首日
    OES_SECURITY_STATUS_RESUME_FIRST_LISTING = (1 << 1)  # 恢复上市首日
    OES_SECURITY_STATUS_NEW_LISTING = (1 << 2)  # 上市初期
    OES_SECURITY_STATUS_EXCLUDE_RIGHT = (1 << 3)  # 除权
    OES_SECURITY_STATUS_EXCLUDE_DIVIDEN = (1 << 4)  # 除息
    OES_SECURITY_STATUS_SUSPEND = (1 << 5)  # 证券连续停牌
    OES_SECURITY_STATUS_SPECIAL_TREATMENT = (1 << 6)  # ST股
    OES_SECURITY_STATUS_X_SPECIAL_TREATMENT = (1 << 7)  # *ST股
    OES_SECURITY_STATUS_DELIST_PERIOD = (1 << 8)  # 退市整理期
    OES_SECURITY_STATUS_DELIST_TRANSFER = (1 << 9)  # 退市转让期


class OesAuctionReferPriceType(Enum):
    OES_AUCTION_REFER_PRICE_TYPE_LAST = 1  # 最近价
    OES_AUCTION_REFER_PRICE_TYPE_BEST = 2  # 对手方最优价


class OesAuctionLimitType(Enum):
    OES_AUCTION_LIMIT_TYPE_NONE = 0  # 无竞价范围限制
    OES_AUCTION_LIMIT_TYPE_RATE = 1  # 按幅度限制 (百分比)
    OES_AUCTION_LIMIT_TYPE_ABSOLUTE = 2  # 按价格限制 (绝对值)


class OesLotType(Enum):
    OES_LOT_TYPE_UNDEFINE = 0  # 未定义的中签、配号记录类型
    OES_LOT_TYPE_FAILED = 1  # 配号失败记录
    OES_LOT_TYPE_ASSIGNMENT = 2  # 配号成功记录
    OES_LOT_TYPE_LOTTERY = 3  # 中签记录


class OesLotRejReason(Enum):
    OES_LOT_REJ_REASON_DUPLICATE = 1  # 配号失败-重复申购
    OES_LOT_REJ_REASON_INVALID_DUPLICATE = 2  # 配号失败-违规重复
    OES_LOT_REJ_REASON_OFFLINE_FIRST = 3  # 配号失败-网下在先
    OES_LOT_REJ_REASON_BAD_RECORD = 4  # 配号失败-不良记录
    OES_LOT_REJ_REASON_UNKNOW = 5  # 配号失败-未知原因


class OesOrdStatus(Enum):
    OES_ORD_STATUS_UNDEFINE = 0  # 未定义
    OES_ORD_STATUS_NEW = 1  # 新订单(尚未上报)

    OES_ORD_STATUS_DECLARED = 2  # 已确认
    OES_ORD_STATUS_PARTIALLY_FILLED = 3  # 部分成交

    # _OES_ORD_STATUS_FINAL_MIN = 4  # 订单终结状态判断标志
    OES_ORD_STATUS_CANCEL_DONE = 5  # 撤单指令已执行 (适用于撤单请求, 并做为撤单请求的终结状态)
    OES_ORD_STATUS_PARTIALLY_CANCELED = 6  # 部分撤单
    OES_ORD_STATUS_CANCELED = 7  # 已撤单
    OES_ORD_STATUS_FILLED = 8  # 已成交
    # _OES_ORD_STATUS_VALID_MAX = 9

    # _OES_ORD_STATUS_INVALID_MIN = 10  # 废单判断标志
    OES_ORD_STATUS_INVALID_OES = 11  # OES内部废单
    OES_ORD_STATUS_INVALID_SH_F = 12  # 上证后台判断该订单为废单
    OES_ORD_STATUS_INVALID_SH_E = 13  # 上证前台判断该订单为废单
    OES_ORD_STATUS_INVALID_SH_COMM = 14  # 通信故障
    OES_ORD_STATUS_INVALID_SZ_F = 15  # 深证前台废单
    OES_ORD_STATUS_INVALID_SZ_E = 16  # 深证后台废单
    OES_ORD_STATUS_INVALID_SZ_REJECT = 17  # 深证业务拒绝
    OES_ORD_STATUS_INVALID_SZ_TRY_AGAIN = 18  # 深证平台未开放(需尝试重报)
    # _OES_ORD_STATUS_INVALID_MAX = 19

    # 以下订单状态定义已废弃, 只是为了兼容之前的版本而暂时保留
    OES_ORD_STATUS_NORMAL = OES_ORD_STATUS_NEW
    OES_ORD_STATUS_DECLARING = OES_ORD_STATUS_NEW


class OesOrdType(Enum):
    OES_ORD_TYPE_LMT = 0  # 限价
    OES_ORD_TYPE_LMT_FOK = 1  # 限价FOK

    OES_ORD_TYPE_MTL_BEST_5 = 10  # 最优五档即时成交剩余转限价
    OES_ORD_TYPE_MTL_BEST = 11  # 对手方最优价格申报
    OES_ORD_TYPE_MTL_SAMEPARTY_BEST = 12  # 本方最优价格申报
    OES_ORD_TYPE_MTL = 13  # 市价剩余转限价委托

    OES_ORD_TYPE_FAK_BEST_5 = 20  # 最优五档即时成交剩余撤销
    OES_ORD_TYPE_FAK = 21  # 即时成交剩余撤销

    OES_ORD_TYPE_FOK = 30  # 市价全部成交或全部撤销 (期权)


class OesOrdTypeSh(Enum):
    OES_ORD_TYPE_SH_LMT = OesOrdType.OES_ORD_TYPE_LMT.value  #
    OES_ORD_TYPE_SH_MTL_BEST_5 = OesOrdType.OES_ORD_TYPE_MTL_BEST_5.value  #
    OES_ORD_TYPE_SH_MTL_BEST = OesOrdType.OES_ORD_TYPE_MTL_BEST.value  # 对手方最优价格申报(仅适用于科创板),
    OES_ORD_TYPE_SH_MTL_SAMEPARTY_BEST = OesOrdType.OES_ORD_TYPE_MTL_SAMEPARTY_BEST.value  # 本方最优价格申报(仅适用于科创板),
    OES_ORD_TYPE_SH_FAK_BEST_5 = OesOrdType.OES_ORD_TYPE_FAK_BEST_5.value  #


class OesOrdTypeSz(Enum):
    OES_ORD_TYPE_SZ_LMT = OesOrdType.OES_ORD_TYPE_LMT.value  #
    OES_ORD_TYPE_SZ_MTL_BEST = OesOrdType.OES_ORD_TYPE_MTL_BEST.value  #
    OES_ORD_TYPE_SZ_MTL_SAMEPARTY_BEST = OesOrdType.OES_ORD_TYPE_MTL_SAMEPARTY_BEST.value  #
    OES_ORD_TYPE_SZ_FAK_BEST_5 = OesOrdType.OES_ORD_TYPE_FAK_BEST_5.value  #
    OES_ORD_TYPE_SZ_FAK = OesOrdType.OES_ORD_TYPE_FAK.value  #
    OES_ORD_TYPE_SZ_FOK = OesOrdType.OES_ORD_TYPE_FOK.value  #
    OES_ORD_TYPE_SZ_LMT_FOK = OesOrdType.OES_ORD_TYPE_LMT_FOK.value  #


# 上海期权委托类型
class OesOrdTypeShOpt(Enum):
    OES_ORD_TYPE_SHOPT_LMT = OesOrdType.OES_ORD_TYPE_LMT.value         # 0 限价
    OES_ORD_TYPE_SHOPT_LMT_FOK = OesOrdType.OES_ORD_TYPE_LMT_FOK.value # 1 限价全部成交或全部撤销委托
    OES_ORD_TYPE_SHOPT_MTL = OesOrdType.OES_ORD_TYPE_MTL.value         # 13 市价剩余转限价委托
    OES_ORD_TYPE_SHOPT_FAK = OesOrdType.OES_ORD_TYPE_FAK.value         # 21 即时成交剩余撤销委托
    OES_ORD_TYPE_SHOPT_FOK = OesOrdType.OES_ORD_TYPE_FOK.value         # 30 市价全部成交或全部撤销委托


class OesBuySellType(Enum):
    OES_BS_TYPE_UNDEFINE = 0  # 未定义的买卖类型

    OES_BS_TYPE_BUY = 1  # 买入
    OES_BS_TYPE_SELL = 2  # 卖出
    OES_BS_TYPE_CREATION = 3  # 申购
    OES_BS_TYPE_REDEMPTION = 4  # 赎回
    OES_BS_TYPE_CREDIT_BUY = 5  # 融资买入
    OES_BS_TYPE_CREDIT_SELL = 6  # 融券卖出，质押式逆回购
    OES_BS_TYPE_SUBSCRIPTION = 7  # 新股认购
    OES_BS_TYPE_ALLOTMENT = 8  # 配股认购

    OES_BS_TYPE_BUY_OPEN = 11  # 期权买入开仓
    OES_BS_TYPE_SELL_CLOSE = 12  # 期权卖出平仓
    OES_BS_TYPE_SELL_OPEN = 13  # 期权卖出开仓
    OES_BS_TYPE_BUY_CLOSE = 14  # 期权买入平仓
    OES_BS_TYPE_COVERED_OPEN = 15  # 期权备兑开仓
    OES_BS_TYPE_COVERED_CLOSE = 16  # 期权备兑平仓
    OES_BS_TYPE_OPTION_EXERCISE = 17  # 期权行权
    OES_BS_TYPE_UNDERLYING_FREEZE = 18  # 期权标的锁定
    OES_BS_TYPE_UNDERLYING_UNFREEZE = 19  # 期权标的解锁

    OES_BS_TYPE_CANCEL = 30  # 撤单
    # _OES_BS_TYPE_MAX_TRADING = 31  # 对外开放的交易类业务的买卖类型最大值

    OES_BS_TYPE_SSE_DESIGNATION = 41  # 指定登记
    OES_BS_TYPE_SSE_RECALL_DESIGNATION = 42  # 指定撤消
    OES_BS_TYPE_SZSE_DESIGNATION = 43  # 托管注册
    OES_BS_TYPE_SZSE_CANCEL_DESIGNATION = 44  # 托管撤消


class OesOrdDir(Enum):
    OES_ORD_DIR_BUY = 0  # 买
    OES_ORD_DIR_SELL = 1  # 卖


class OesEtfTrdCnfmType(Enum):
    OES_ETF_TRDCNFM_TYPE_NONE = 0  # 无意义
    OES_ETF_TRDCNFM_TYPE_ETF_FIRST = 1  # 二级市场记录
    OES_ETF_TRDCNFM_TYPE_CMPOENT = 2  # 成份股记录
    OES_ETF_TRDCNFM_TYPE_CASH = 3  # 资金记录
    OES_ETF_TRDCNFM_TYPE_ETF_LAST = 4  # 一级市场记录


class OesFundTrsfStatus(Enum):
    OES_FUND_TRSF_STS_UNDECLARED = 0  # 尚未上报到主柜
    OES_FUND_TRSF_STS_DECLARED = 1  # 已上报到主柜
    OES_FUND_TRSF_STS_WAIT_DONE = 2  # 主柜处理完成，等待事务结束
    OES_FUND_TRSF_STS_DONE = 3  # 出入金处理完成

    _OES_FUND_TRSF_STS_ROLLBACK_MIN = 5  # 废单判断标志
    OES_FUND_TRSF_STS_UNDECLARED_ROLLBACK = 6  # 待回滚(未上报到主柜前)
    OES_FUND_TRSF_STS_DECLARED_ROLLBACK = 7  # 待回滚(已上报到主柜后)

    _OES_FUND_TRSF_STS_INVALID_MIN = 10  # 废单判断标志
    OES_FUND_TRSF_STS_INVALID_OES = 11  # OES内部判断为废单
    OES_FUND_TRSF_STS_INVALID_COUNTER = 12  # 主柜判断为废单
    OES_FUND_TRSF_STS_SUSPENDED = 13  # 挂起状态 (主柜的出入金执行状态未知，待人工干预处理)


class OesBusinessScope(Enum):
    OES_BIZ_SCOPE_UNDEFINE = 0x0  # 未定义的业务范围
    OES_BIZ_SCOPE_STOCK = 0x01  # 现货业务/信用业务
    OES_BIZ_SCOPE_OPTION = 0x02  # 期权业务
    OES_BIZ_SCOPE_ALL = 0xFF  # 所有业务


class OesTradingPermission(Enum):
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
    OES_PERMIS_GEM_REGISTRATION = 1 << 12  # 注册制创业板交易
    OES_PERMIS_GEM_UNREGISTRATION = 1 << 13  # 非注册制创业板交易
    OES_PERMIS_SH_HK_STOCK_CONNECT = 1 << 14  # 沪港通
    OES_PERMIS_SZ_HK_STOCK_CONNECT = 1 << 15  # 深港通
    OES_PERMIS_HLTCDR = 1 << 16  # 沪伦通存托凭证
    OES_PERMIS_CDR = 1 << 17  # 存托凭证
    OES_PERMIS_INNOVATION = 1 << 18  # 创新企业股票
    OES_PERMIS_KSH = 1 << 19  # 科创板交易
    OES_PERMIS_BOND_ETF = 1 << 20  # 债券ETF申赎
    OES_PERMIS_GOLD_ETF = 1 << 21  # 黄金ETF申赎
    OES_PERMIS_COMMODITY_FUTURES_ETF = 1 << 22  # 商品期货ETF申赎
    OES_PERMIS_ALL = 0xFFFFFFFF  # 全部权限


class OesTradingLimit(Enum):
    OES_LIMIT_BUY = 1 << 1  # 禁止买入
    OES_LIMIT_SELL = 1 << 2  # 禁止卖出
    OES_LIMIT_RECALL_DESIGNATION = 1 << 3  # 禁撤销指定
    OES_LIMIT_DESIGNATION = 1 << 4  # 禁止转托管
    OES_LIMIT_REPO = 1 << 5  # 禁止回购融资
    OES_LIMIT_REVERSE_REPO = 1 << 6  # 禁止质押式逆回购
    OES_LIMIT_SUBSCRIPTION = 1 << 7  # 禁止普通申购 (新股认购)
    OES_LIMIT_CREDIT_BUY = 1 << 8  # 禁止融资买入
    OES_LIMIT_CREDIT_SELL = 1 << 9  # 禁止融券卖出
    OES_LIMIT_ALL = 0xFFFFFFFF  # 全部限制


class OesAcctStatus(Enum):
    OES_ACCT_STATUS_NORMAL = 0  # 正常
    OES_ACCT_STATUS_DISABLED = 1  # 非正常
    OES_ACCT_STATUS_LOCKED = 2  # 已锁定


class OesQualificationClass(Enum):
    OES_QUALIFICATION_PUBLIC_INVESTOR = 0  # 公众投资者
    OES_QUALIFICATION_QUALIFIED_INVESTOR = 1  # 合格投资者(个人投资者)
    OES_QUALIFICATION_QUALIFIED_INSTITUTIONAL = 2  # 合格投资者(机构投资者)


class OesInvestorClass(Enum):
    OES_INVESTOR_CLASS_NORMAL = 0  # 普通投资者
    OES_INVESTOR_CLASS_PROFESSIONAL_A = 1  # A类专业投资者
    OES_INVESTOR_CLASS_PROFESSIONAL_B = 2  # B类专业投资者
    OES_INVESTOR_CLASS_PROFESSIONAL_C = 3  # C类专业投资者


class OesCustType(Enum):
    OES_CUST_TYPE_PERSONAL = 0  # 个人
    OES_CUST_TYPE_INSTITUTION = 1  # 机构
    OES_CUST_TYPE_PROPRIETARY = 2  # 自营
    OES_CUST_TYPE_PRODUCT = 3  # 产品
    OES_CUST_TYPE_MKT_MAKER = 4  # 做市商
    OES_CUST_TYPE_OTHERS = 5  # 其他


class OesOwnerType(Enum):
    OES_OWNER_TYPE_UNDEFINE = 0  # 未定义
    OES_OWNER_TYPE_PERSONAL = 1  # 个人投资者
    OES_OWNER_TYPE_EXCHANGE = 101  # 交易所
    OES_OWNER_TYPE_MEMBER = 102  # 会员
    OES_OWNER_TYPE_INSTITUTION = 103  # 机构投资者
    OES_OWNER_TYPE_PROPRIETARY = 104  # 自营
    OES_OWNER_TYPE_MKT_MAKER = 105  # 做市商
    OES_OWNER_TYPE_SETTLEMENT = 106  # 结算机构


class OesClientType(Enum):
    OES_CLIENT_TYPE_UNDEFINED = 0  # 客户端类型-未定义
    OES_CLIENT_TYPE_INVESTOR = 1  # 普通投资人
    OES_CLIENT_TYPE_VIRTUAL = 2  # 虚拟账户 (仅开通行情, 不可交易)


class OesClientStatus(Enum):
    OES_CLIENT_STATUS_UNACTIVATED = 0  # 未激活 (不加载)
    OES_CLIENT_STATUS_ACTIVATED = 1  # 已激活 (正常加载)
    OES_CLIENT_STATUS_PAUSE = 2  # 已暂停 (正常加载, 不可交易)
    OES_CLIENT_STATUS_SUSPENDED = 3  # 已挂起 (正常加载, 不可交易、不可出入金)
    OES_CLIENT_STATUS_CANCELLED = 4  # 已注销 (不加载)


class OesOptInvLevel(Enum):
    OES_OPT_INV_LEVEL_UNDEFINE = 0  # 未定义 (机构投资者)
    OES_OPT_INV_LEVEL_1 = 1  # 个人投资者-一级交易权限
    OES_OPT_INV_LEVEL_2 = 2  # 个人投资者-二级交易权限
    OES_OPT_INV_LEVEL_3 = 3  # 个人投资者-三级交易权限


class OesMsgType(Enum):
    # 交易类消息
    OESMSG_ORD_NEW_ORDER = 0x01  # 0x01/01  委托申报消息
    OESMSG_ORD_CANCEL_REQUEST = 0x02  # 0x02/02  撤单请求消息
    OESMSG_ORD_BATCH_ORDERS = 0x03  # 0x03/03  批量委托消息
    # 执行报告类消息
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
    # 非交易类消息
    OESMSG_NONTRD_FUND_TRSF_REQ = 0x21  # 0x21/33  出入金委托
    OESMSG_NONTRD_CHANGE_PASSWORD = 0x22  # 0x22/34  修改客户端登录密码
    # 查询类消息
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
    # 公共的会话类消息
    OESMSG_SESS_HEARTBEAT = 0xFA  # 0xFA/250 心跳消息
    OESMSG_SESS_TEST_REQUEST = 0xFB  # 0xFB/251 测试请求消息
    OESMSG_SESS_LOGIN_EXTEND = 0xFC  # 0xFC/252 登录扩展消息
    OESMSG_SESS_LOGOUT = 0xFE  # 0xFE/254 登出消息


# OES执行类型
class OesExecType(Enum):
    # 未定义的执行类型
    OES_EXECTYPE_UNDEFINE = 0
    # 已接收 (OES已接收)
    OES_EXECTYPE_INSERT = 1
    # 已确认 (交易所已确认/出入金主柜台已确认)
    OES_EXECTYPE_CONFIRMED = 2
    # 已撤单 (原始委托的撤单完成回报)
    OES_EXECTYPE_CANCELLED = 3
    # 自动撤单 (市价委托发生自动撤单后的委托回报)
    OES_EXECTYPE_AUTO_CANCELLED = 4
    # 拒绝 (OES拒绝/交易所废单/出入金主柜台拒绝)
    OES_EXECTYPE_REJECT = 5
    # 成交 (成交回报)
    OES_EXECTYPE_TRADE = 6
    # 执行类型最大值
    _OES_EXECTYPE_MAX = 7


class OesFeeType(Enum):
    OES_FEE_TYPE_EXCHANGE_STAMP = 0x1  # 交易所固定费用-印花税
    OES_FEE_TYPE_EXCHANGE_TRANSFER = 0x2  # 交易所固定费用 - 过户费
    OES_FEE_TYPE_EXCHANGE_SETTLEMENT = 0x3  # 交易所固定费用 - 结算费
    OES_FEE_TYPE_EXCHANGE_TRADE_RULE = 0x4  # 交易所固定费用 - 交易规费
    OES_FEE_TYPE_EXCHANGE_EXCHANGE = 0x5  # 交易所固定费用 - 经手费
    OES_FEE_TYPE_EXCHANGE_ADMINFER = 0x6  # 交易所固定费用 - 证管费
    OES_FEE_TYPE_EXCHANGE_OTHER = 0x7  # 交易所固定费用 - 其他费
    OES_FEE_TYPE_BROKER_BACK_END = 0x11  # 券商佣金 - 后台费用


class OesCalcFeeMode(Enum):
    OES_CALC_FEE_MODE_AMOUNT = 0  # 按金额
    OES_CALC_FEE_MODE_QTY = 1  # 按份额
    OES_CALC_FEE_MODE_ORD = 2  # 按笔数


class OesFundTrsfDirect(Enum):
    OES_FUND_TRSF_DIRECT_IN = 0  # 转入OES (入金)
    OES_FUND_TRSF_DIRECT_OUT = 1  # 转出OES (出金)


class OesFundTrsfType(Enum):
    OES_FUND_TRSF_TYPE_OES_BANK = 0  # OES和银行之间转账
    OES_FUND_TRSF_TYPE_OES_COUNTER = 1  # OES和主柜之间划拨资金
    OES_FUND_TRSF_TYPE_COUNTER_BANK = 2  # 主柜和银行之间转账
    _OES_FUND_TRSF_TYPE_MAX = OES_FUND_TRSF_TYPE_COUNTER_BANK + 1  # 出入金转值


class OesSubscribeReportType(Enum):
    OES_SUB_RPT_TYPE_DEFAULT = 0  # 默认回报
    OES_SUB_RPT_TYPE_BUSINESS_REJECT = 0x01  # OES业务拒绝 (未通过风控检查等)
    OES_SUB_RPT_TYPE_ORDER_INSERT = 0x02  # OES委托已生成 (已通过风控检查)
    OES_SUB_RPT_TYPE_ORDER_REPORT = 0x04  # 交易所委托回报 (包括交易所委托拒绝、委托确认和撤单完成通知)
    OES_SUB_RPT_TYPE_TRADE_REPORT = 0x08  # 交易所成交回报
    OES_SUB_RPT_TYPE_FUND_TRSF_REPORT = 0x10  # 出入金委托执行报告 (包括出入金委托拒绝、出入金委托回报)
    OES_SUB_RPT_TYPE_CASH_ASSET_VARIATION = 0x20  # 资金变动信息
    OES_SUB_RPT_TYPE_HOLDING_VARIATION = 0x40  # 持仓变动信息
    OES_SUB_RPT_TYPE_MARKET_STATE = 0x80  # 市场状态信息
    # OES_SUB_RPT_TYPE_NOTIFY_INFO = 0x100  # 通知消息
    # OES_SUB_RPT_TYPE_SETTLEMETN_CONFIRMED = 0x200  # 结算单确认消息
    OES_SUB_RPT_TYPE_ALL = 0xFFFF  # 所有回报


class OesProtocolHintsType(Enum):
    OES_PROT_HINTS_TYPE_DEFAULT = 0  # 默认的协议约定类型
    OES_PROT_HINTS_TYPE_COMPRESS = 0x80  # 协议约定以压缩方式传输数据
    OES_PROT_HINTS_TYPE_NONE = 0xFF  # 无任何协议约定


class OesSecurityIssueType(Enum):
    OES_ISSUE_TYPE_UNDEFINE = 0  # 未定义的发行方式
    OES_ISSUE_TYPE_MKT_QUOTA = 1  # 按市值限额申购
    OES_ISSUE_TYPE_CASH = 2  # 增发资金申购 (仅上证使用)
    OES_ISSUE_TYPE_CREDIT = 3  # 信用申购 (仅上证使用)


class UserInfo(SimpleUnion):
    _fields_ = [
        ('u64', c_uint64),  # uint64 类型的用户私有信息
        ('i64', c_int64),  # int64 类型的用户私有信息
        ('u32', c_uint32 * 2),  # uint32[2] 类型的用户私有信息
        ('i32', c_int32 * 2),  # int32[2] 类型的用户私有信息
        ("c8", c_char * 8)  # char[8] 类型的用户私有信息
    ]


class OesQryReqHead(SimpleStructure):
    _fields_ = [
        ('max_page_size', c_int32),  # 查询窗口大小
        ('last_position', c_int32),  # 查询起始位置
    ]


class OesQryRspHead(SimpleStructure):
    _fields_ = [
        ('item_count', c_int32),  # 查询到的信息条目数
        ('last_position', c_int32),  # 查询到的最后一条信息的位置
        ('is_end', c_int8),  # 是否是当前查询最后一个包
        ('_filler', c_uint8 * 7),  # 按64位对齐填充域
        ('user_info', c_int64),  # 用户私有信息 (由客户端自定义填充, 并在应答数据中原样返回)
    ]

