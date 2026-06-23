import time
import logging
import functools
from typing import Callable, Any, Tuple, Optional
from playwright.sync_api import Error as PlaywrightError

logger = logging.getLogger(__name__)

NETWORK_ERRORS = (
    "net::ERR_ABORTED",
    "net::ERR_NETWORK_IO_SUSPENDED",
    "net::ERR_CONNECTION_REFUSED",
    "net::ERR_NAME_NOT_RESOLVED",
    "net::ERR_TIMED_OUT",
    "net::ERR_INTERNET_DISCONNECTED",
    "net::ERR_CERTIFICATE_ERROR",
    "net::ERR_PROXY_CONNECTION_FAILED",
)

REQUESTS_RETRYABLE_STATUS_CODES = (429, 500, 502, 503, 504)

class RetryConfig:
    DEFAULT_MAX_RETRIES = 3
    DEFAULT_DELAY = 3
    DEFAULT_BACKOFF_FACTOR = 2
    DEFAULT_MAX_DELAY = 30

def is_network_error(error: Exception) -> bool:
    """判断是否是网络错误"""
    error_str = str(error)
    return any(network_error in error_str for network_error in NETWORK_ERRORS)

def retry_on_network_error(
    max_retries: int = RetryConfig.DEFAULT_MAX_RETRIES,
    delay: int = RetryConfig.DEFAULT_DELAY,
    backoff_factor: int = RetryConfig.DEFAULT_BACKOFF_FACTOR,
    max_delay: int = RetryConfig.DEFAULT_MAX_DELAY,
    retryable_exceptions: Tuple[type, ...] = (Exception,),
):
    """
    网络错误重试装饰器
    
    Args:
        max_retries: 最大重试次数
        delay: 初始重试延迟（秒）
        backoff_factor: 退避因子（每次重试延迟乘以该因子）
        max_delay: 最大重试延迟（秒）
        retryable_exceptions: 可重试的异常类型元组
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except retryable_exceptions as e:
                    last_exception = e
                    
                    if not is_network_error(e):
                        logger.warning(f"非网络错误，不重试: {e}")
                        raise
                    
                    if attempt < max_retries:
                        logger.warning(f"网络错误，重试 {attempt + 1}/{max_retries}: {e}")
                        time.sleep(current_delay)
                        current_delay = min(current_delay * backoff_factor, max_delay)
                    else:
                        logger.error(f"网络错误重试失败 ({max_retries}次): {e}")
                        raise
            
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator

def retry_with_backoff(
    func: Callable,
    max_retries: int = RetryConfig.DEFAULT_MAX_RETRIES,
    delay: int = RetryConfig.DEFAULT_DELAY,
    backoff_factor: int = RetryConfig.DEFAULT_BACKOFF_FACTOR,
    max_delay: int = RetryConfig.DEFAULT_MAX_DELAY,
    retryable_exceptions: Tuple[type, ...] = (Exception,),
) -> Any:
    """
    带退避策略的重试函数
    
    Args:
        func: 要执行的函数
        max_retries: 最大重试次数
        delay: 初始重试延迟（秒）
        backoff_factor: 退避因子
        max_delay: 最大重试延迟
        retryable_exceptions: 可重试的异常类型
    
    Returns:
        函数执行结果
    """
    current_delay = delay
    last_exception = None
    
    for attempt in range(max_retries + 1):
        try:
            return func()
        except retryable_exceptions as e:
            last_exception = e
            
            if not is_network_error(e):
                raise
            
            if attempt < max_retries:
                logger.warning(f"网络错误，重试 {attempt + 1}/{max_retries}: {e}")
                time.sleep(current_delay)
                current_delay = min(current_delay * backoff_factor, max_delay)
            else:
                logger.error(f"网络错误重试失败 ({max_retries}次): {e}")
                raise
    
    if last_exception:
        raise last_exception

def safe_navigation(
    page,
    url: str,
    max_retries: int = RetryConfig.DEFAULT_MAX_RETRIES,
    delay: int = RetryConfig.DEFAULT_DELAY,
    wait_until: str = "load",
):
    """
    安全导航函数，处理网络错误重试
    
    Args:
        page: Playwright页面对象
        url: 目标URL
        max_retries: 最大重试次数
        delay: 重试延迟
        wait_until: 等待条件
    """
    current_delay = delay
    
    for attempt in range(max_retries + 1):
        try:
            page.goto(url, wait_until=wait_until)
            return
        except PlaywrightError as e:
            if is_network_error(e):
                if attempt < max_retries:
                    logger.warning(f"导航失败，重试 {attempt + 1}/{max_retries}: {e}")
                    time.sleep(current_delay)
                    current_delay = min(current_delay * 2, 30)
                else:
                    logger.error(f"导航失败 ({max_retries}次): {e}")
                    raise
            else:
                raise

def safe_reload(
    page,
    max_retries: int = RetryConfig.DEFAULT_MAX_RETRIES,
    delay: int = RetryConfig.DEFAULT_DELAY,
    wait_until: str = "load",
):
    """
    安全刷新函数，处理网络错误重试
    
    Args:
        page: Playwright页面对象
        max_retries: 最大重试次数
        delay: 重试延迟
        wait_until: 等待条件
    """
    current_delay = delay
    
    for attempt in range(max_retries + 1):
        try:
            page.reload(wait_until=wait_until)
            return
        except PlaywrightError as e:
            if is_network_error(e):
                if attempt < max_retries:
                    logger.warning(f"页面刷新失败，重试 {attempt + 1}/{max_retries}: {e}")
                    time.sleep(current_delay)
                    current_delay = min(current_delay * 2, 30)
                else:
                    logger.error(f"页面刷新失败 ({max_retries}次): {e}")
                    raise
            else:
                raise


def is_requests_network_error(error: Exception) -> bool:
    """判断requests库的网络错误"""
    import requests
    
    network_exceptions = (
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.ReadTimeout,
        requests.exceptions.SSLError,
    )
    
    return isinstance(error, network_exceptions)


def is_retryable_status_code(status_code: int) -> bool:
    """判断HTTP状态码是否可重试"""
    return status_code in REQUESTS_RETRYABLE_STATUS_CODES


def retry_on_requests_error(
    max_retries: int = RetryConfig.DEFAULT_MAX_RETRIES,
    delay: int = RetryConfig.DEFAULT_DELAY,
    backoff_factor: int = RetryConfig.DEFAULT_BACKOFF_FACTOR,
    max_delay: int = RetryConfig.DEFAULT_MAX_DELAY,
    retryable_status_codes: Tuple[int, ...] = REQUESTS_RETRYABLE_STATUS_CODES,
):
    """
    Requests库网络错误重试装饰器
    
    Args:
        max_retries: 最大重试次数
        delay: 初始重试延迟（秒）
        backoff_factor: 退避因子
        max_delay: 最大重试延迟（秒）
        retryable_status_codes: 可重试的HTTP状态码
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    result = func(*args, **kwargs)
                    
                    if hasattr(result, 'status_code'):
                        if result.status_code in retryable_status_codes:
                            raise requests.exceptions.HTTPError(
                                f"HTTP {result.status_code}: {result.text}"
                            )
                    return result
                except Exception as e:
                    last_exception = e
                    
                    if not is_requests_network_error(e):
                        if isinstance(e, requests.exceptions.HTTPError):
                            if hasattr(e, 'response') and e.response.status_code in retryable_status_codes:
                                logger.warning(f"HTTP错误 {e.response.status_code}，重试中...")
                            else:
                                logger.warning(f"非可重试HTTP错误，不重试: {e}")
                                raise
                        else:
                            logger.warning(f"非网络错误，不重试: {e}")
                            raise
                    
                    if attempt < max_retries:
                        logger.warning(f"网络错误，重试 {attempt + 1}/{max_retries}: {e}")
                        time.sleep(current_delay)
                        current_delay = min(current_delay * backoff_factor, max_delay)
                    else:
                        logger.error(f"网络错误重试失败 ({max_retries}次): {e}")
                        raise
            
            if last_exception:
                raise last_exception
        
        return wrapper
    return decorator


def safe_request(
    session,
    method: str,
    url: str,
    max_retries: int = RetryConfig.DEFAULT_MAX_RETRIES,
    delay: int = RetryConfig.DEFAULT_DELAY,
    backoff_factor: int = RetryConfig.DEFAULT_BACKOFF_FACTOR,
    max_delay: int = RetryConfig.DEFAULT_MAX_DELAY,
    retryable_status_codes: Tuple[int, ...] = REQUESTS_RETRYABLE_STATUS_CODES,
    **kwargs
):
    """
    安全请求函数，处理网络错误重试
    
    Args:
        session: requests.Session对象
        method: HTTP方法
        url: 请求URL
        max_retries: 最大重试次数
        delay: 初始重试延迟
        backoff_factor: 退避因子
        max_delay: 最大重试延迟
        retryable_status_codes: 可重试的HTTP状态码
        **kwargs: 其他请求参数
    
    Returns:
        requests.Response对象
    """
    import requests
    
    current_delay = delay
    
    for attempt in range(max_retries + 1):
        try:
            response = session.request(method.upper(), url, **kwargs)
            
            if response.status_code in retryable_status_codes:
                raise requests.exceptions.HTTPError(
                    f"HTTP {response.status_code}: {response.text}"
                )
            
            return response
        except requests.exceptions.RequestException as e:
            is_retryable = is_requests_network_error(e)
            
            if not is_retryable:
                if isinstance(e, requests.exceptions.HTTPError):
                    if hasattr(e, 'response') and e.response.status_code in retryable_status_codes:
                        is_retryable = True
            
            if is_retryable:
                if attempt < max_retries:
                    logger.warning(f"请求失败，重试 {attempt + 1}/{max_retries}: {e}")
                    time.sleep(current_delay)
                    current_delay = min(current_delay * backoff_factor, max_delay)
                else:
                    logger.error(f"请求失败 ({max_retries}次): {e}")
                    raise
            else:
                logger.error(f"请求失败（非可重试）: {e}")
                raise