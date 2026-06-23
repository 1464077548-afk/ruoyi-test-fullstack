# 测试级别定义

class TestLevels:
    # L1: 单接口测试 - 测试单个接口的基本功能
    L1 = "L1"
    
    # L2: 接口模块测试 - 测试接口模块的集成功能
    L2 = "L2"
    
    # L3: 接口业务流测试 - 测试完整的业务流程
    L3 = "L3"
    
    # UI L1: 组件测试 - 测试UI组件的基本功能
    UI_L1 = "UI_L1"
    
    # UI L2: 单模块测试 - 测试UI单模块的功能
    UI_L2 = "UI_L2"
    
    # UI L3: 业务流测试 - 测试完整的UI业务流程
    UI_L3 = "UI_L3"
    
    # 集成测试 - 测试UI与API的集成
    INTEGRATION = "INTEGRATION"
    
    # 性能测试 - 测试系统性能
    PERFORMANCE = "PERFORMANCE"
    
    # 安全测试 - 测试系统安全
    SECURITY = "SECURITY"

# 测试级别映射
TEST_LEVELS = {
    "L1": TestLevels.L1,
    "L2": TestLevels.L2,
    "L3": TestLevels.L3,
    "UI_L1": TestLevels.UI_L1,
    "UI_L2": TestLevels.UI_L2,
    "UI_L3": TestLevels.UI_L3,
    "INTEGRATION": TestLevels.INTEGRATION,
    "PERFORMANCE": TestLevels.PERFORMANCE,
    "SECURITY": TestLevels.SECURITY
}