"""用户权限"""
ROLE_YW = 1
ROLE_ZG = 2
ROLE_SW = 3
ROLE_JL = 4
ROLE_RS = 5
USER_ROLE = (
    (ROLE_YW, '业务'),
    (ROLE_ZG, '主管'),
    (ROLE_SW, '商务'),
    (ROLE_JL, '经理'),
    (ROLE_RS, '人事'),
)

"""客户等级分类"""
RANK_NORMAL = 1
RANK_COMMONLY = 2
RANK_ORDINARY = 3
CUSTOMER_RANK = (
    (RANK_NORMAL, '重点客户'),
    (RANK_COMMONLY, '一般客户'),
    (RANK_ORDINARY, '普通客户'),
)

"""客户规模"""
SCALE_TEN = 1
SCALE_FIF = 2
SCALE_HUN = 3
SCALE_THO = 4
SCALE_MORE = 5
CUSTOMER_SCALE = (
    (SCALE_TEN, '0~10人'),
    (SCALE_FIF, '10~50人'),
    (SCALE_HUN, '50~100人'),
    (SCALE_THO, '100~1000人'),
    (SCALE_MORE, '1000人及以上')
)

"""客户性质"""
NATURE_GY = 1
NATURE_JT = 2
NATURE_SY = 3
NATURE_GT = 4
NATURE_HH = 5
NATURE_LY = 6
NATURE_GFHZ = 7
NATURE_YX = 8
NATURE_GF = 9
CUSTOMER_NATURE = (
    (NATURE_YX, '有限责任公司'),
    (NATURE_GF, '股份有限公司'),
    (NATURE_GY, '国有企业'),
    (NATURE_JT, '集体企业'),
    (NATURE_SY, '私营企业'),
    (NATURE_GT, '个体工商户'),
    (NATURE_HH, '合伙企业'),
    (NATURE_LY, '联营企业'),
    (NATURE_GFHZ, '股份合作制企业'),
)

"""客户行业"""
INDUSTRY_JTSB = 1
INDUSTRY_SCZZ = 2
INDUSTRY_XTJC = 3
INDUSTRY_FX = 4
INDUSTRY_QT = 5
CUSTOMER_INDUSTRY = (
    (INDUSTRY_JTSB, '机台设备制造商'),
    (INDUSTRY_SCZZ, '生产制造型企业'),
    (INDUSTRY_XTJC, '系统集成商'),
    (INDUSTRY_FX, '分销商'),
    (INDUSTRY_QT, '其它'),
)

"""联系人是否在职"""
INJOB_YES = 1
INJOB_NO = 0
LIAISON_INJOB = (
    (INJOB_YES, '在职'),
    (INJOB_NO, '离职'),
)

"""联系人职称"""
JOB_BUSINESS = 1
JOB_MANAGER = 2
JOB_PURCHASE = 3
JOB_TECHNOLOGY = 4
JOB_AFTERSALE = 5
JOB_OTHER = 6
LIAISON_JOB = (
    (JOB_MANAGER, '经理'),
    (JOB_PURCHASE, '采购'),
    (JOB_TECHNOLOGY, '技术'),
    (JOB_AFTERSALE, '售后'),
    (JOB_BUSINESS, '业务'),
    (JOB_OTHER, '其他'),
)


"""客户拜访方式"""
STATUS_XS = 1
STATUS_XX = 2
RECORD_STATUS = (
    (STATUS_XS, '电联'),
    (STATUS_XX, '拜访'),
)


"""商机赢单率"""
WINNING_NONE = 1
WINNING_ERSHI = 2
WINNING_WUSHI = 3
WINNING_BASHI = 4
WINNING_DONE = 5
BUSINESS_WINNING = (
    (WINNING_NONE, '0%'),
    (WINNING_ERSHI, '20%'),
    (WINNING_WUSHI, '50%'),
    (WINNING_BASHI, '80%'),
    (WINNING_DONE, '100%')
)
