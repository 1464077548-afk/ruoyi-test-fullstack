class Assertions:
    """断言封装类"""
    
    @staticmethod
    def assert_equal(actual, expected, message=None):
        """断言相等"""
        assert actual == expected, message or f"实际值: {actual}, 期望值: {expected}"
    
    @staticmethod
    def assert_not_equal(actual, expected, message=None):
        """断言不相等"""
        assert actual != expected, message or f"实际值: {actual} 不应该等于期望值: {expected}"
    
    @staticmethod
    def assert_true(condition, message=None):
        """断言为True"""
        assert condition, message or f"条件应该为True, 实际为: {condition}"
    
    @staticmethod
    def assert_false(condition, message=None):
        """断言为False"""
        assert not condition, message or f"条件应该为False, 实际为: {condition}"
    
    @staticmethod
    def assert_in(expected, actual, message=None):
        """断言包含"""
        assert expected in actual, message or f"{expected} 应该在 {actual} 中"
    
    @staticmethod
    def assert_not_in(expected, actual, message=None):
        """断言不包含"""
        assert expected not in actual, message or f"{expected} 不应该在 {actual} 中"
    
    @staticmethod
    def assert_is_none(value, message=None):
        """断言为None"""
        assert value is None, message or f"值应该为None, 实际为: {value}"
    
    @staticmethod
    def assert_is_not_none(value, message=None):
        """断言不为None"""
        assert value is not None, message or "值不应该为None"
    
    @staticmethod
    def assert_response_status_code(response, expected_status_code, message=None):
        """断言响应状态码"""
        assert response.status_code == expected_status_code, \
            message or f"响应状态码错误: 实际 {response.status_code}, 期望 {expected_status_code}"
    
    @staticmethod
    def assert_response_json(response, expected_key, message=None):
        """断言响应JSON包含指定键"""
        assert expected_key in response.json(), \
            message or f"响应JSON中不存在键: {expected_key}"
    
    @staticmethod
    def assert_length(actual, expected_length, message=None):
        """断言长度"""
        assert len(actual) == expected_length, \
            message or f"长度错误: 实际 {len(actual)}, 期望 {expected_length}"
    
    @staticmethod
    def assert_greater_than(actual, expected, message=None):
        """断言大于"""
        assert actual > expected, message or f"{actual} 应该大于 {expected}"
    
    @staticmethod
    def assert_less_than(actual, expected, message=None):
        """断言小于"""
        assert actual < expected, message or f"{actual} 应该小于 {expected}"
    
    @staticmethod
    def assert_greater_than_or_equal(actual, expected, message=None):
        """断言大于等于"""
        assert actual >= expected, message or f"{actual} 应该大于等于 {expected}"
    
    @staticmethod
    def assert_less_than_or_equal(actual, expected, message=None):
        """断言小于等于"""
        assert actual <= expected, message or f"{actual} 应该小于等于 {expected}"

# 全局断言实例
assertions = Assertions()